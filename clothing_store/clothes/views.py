from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

from .models import (
    Designer, Category, Tag, Season, Material, 
    Clothing, ClothingHistory, UserPermission
)
from .serializers import (
    UserSerializer, DesignerSerializer, CategorySerializer, TagSerializer,
    SeasonSerializer, MaterialSerializer, ClothingSerializer, ClothingListSerializer,
    ClothingCreateSerializer, ClothingHistorySerializer, UserPermissionSerializer
)
from .permissions import IsDesignerOrReadOnly, IsOwnerOrReadOnly

# 传统Django视图
def clothing_list(request):
    """服装列表页面"""
    # 获取查询参数
    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    gender = request.GET.get('gender', '')
    season_id = request.GET.get('season', '')
    color = request.GET.get('color', '')
    
    # 构建查询集
    queryset = Clothing.objects.all()
    
    # 应用筛选条件
    if q:
        queryset = queryset.filter(
            Q(name__icontains=q) |
            Q(style_number__icontains=q) |
            Q(description__icontains=q)
        )
    
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    
    if gender:
        queryset = queryset.filter(gender=gender)
    
    if season_id:
        queryset = queryset.filter(season_id=season_id)
    
    if color:
        queryset = queryset.filter(color__icontains=color)
    
    # 排序
    queryset = queryset.order_by('-created_at')
    
    # 分页
    paginator = Paginator(queryset, 12)  # 每页12个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 获取筛选选项
    categories = Category.objects.all()
    seasons = Season.objects.all()
    
    context = {
        'clothes': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'categories': categories,
        'seasons': seasons,
    }
    
    return render(request, 'clothes/clothing_list.html', context)

def clothing_detail(request, pk):
    """服装详情页面"""
    clothing = get_object_or_404(Clothing, pk=pk)
    history = ClothingHistory.objects.filter(clothing=clothing).order_by('-created_at')
    
    context = {
        'clothing': clothing,
        'history': history,
    }
    
    return render(request, 'clothes/clothing_detail.html', context)

def designer_list(request):
    """设计师列表页面"""
    designers = Designer.objects.filter(is_active=True).order_by('name')
    
    context = {
        'designers': designers,
    }
    
    return render(request, 'clothes/designer_list.html', context)

def designer_detail(request, pk):
    """设计师详情页面"""
    designer = get_object_or_404(Designer, pk=pk)
    clothes = Clothing.objects.filter(designer=designer).order_by('-created_at')
    
    context = {
        'designer': designer,
        'clothes': clothes,
    }
    
    return render(request, 'clothes/designer_detail.html', context)

# API视图集
class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']

class DesignerViewSet(viewsets.ModelViewSet):
    """设计师管理视图集"""
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'bio']
    ordering_fields = ['name', 'created_at']

    @action(detail=True, methods=['get'])
    def clothes(self, request, pk=None):
        """获取设计师的所有服装"""
        designer = self.get_object()
        clothes = Clothing.objects.filter(designer=designer)
        serializer = ClothingListSerializer(clothes, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    """分类管理视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class TagViewSet(viewsets.ModelViewSet):
    """标签管理视图集"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

class SeasonViewSet(viewsets.ModelViewSet):
    """季节管理视图集"""
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class MaterialViewSet(viewsets.ModelViewSet):
    """面料管理视图集"""
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class ClothingViewSet(viewsets.ModelViewSet):
    """服装管理视图集"""
    queryset = Clothing.objects.all()
    serializer_class = ClothingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'gender', 'season', 'designer', 'status', 'is_public']
    search_fields = ['name', 'style_number', 'description', 'color']
    ordering_fields = ['created_at', 'updated_at', 'name', 'style_number']

    def get_serializer_class(self):
        if self.action == 'create':
            return ClothingCreateSerializer
        elif self.action == 'list':
            return ClothingListSerializer
        return ClothingSerializer

    def get_queryset(self):
        """根据用户权限过滤服装"""
        user = self.request.user
        if user.is_staff:
            return Clothing.objects.all()
        
        # 普通用户只能看到公开的服装
        queryset = Clothing.objects.filter(is_public=True)
        
        # 设计师可以看到自己设计的服装
        try:
            designer = user.designer_profile
            queryset = queryset | Clothing.objects.filter(designer=designer)
        except Designer.DoesNotExist:
            pass
        
        # 有特殊权限的服装
        user_permissions = UserPermission.objects.filter(
            user=user, 
            can_view=True,
            expires_at__isnull=True
        )
        if user_permissions.exists():
            permitted_clothes = Clothing.objects.filter(
                userpermission__in=user_permissions
            )
            queryset = queryset | permitted_clothes
        
        return queryset.distinct()

    def perform_create(self, serializer):
        """创建服装时自动设置设计师"""
        designer = get_object_or_404(Designer, user=self.request.user)
        serializer.save(designer=designer)
        
        # 记录创建历史
        ClothingHistory.objects.create(
            clothing=serializer.instance,
            designer=designer,
            action='创建',
            description='创建新服装'
        )

    def perform_update(self, serializer):
        """更新服装时记录修改历史"""
        old_instance = self.get_object()
        serializer.save()
        
        # 记录修改历史
        designer = get_object_or_404(Designer, user=self.request.user)
        changes = {}
        for field in serializer.fields:
            if field in serializer.validated_data:
                old_value = getattr(old_instance, field, None)
                new_value = serializer.validated_data[field]
                if old_value != new_value:
                    changes[field] = {
                        'old': str(old_value),
                        'new': str(new_value)
                    }
        
        if changes:
            ClothingHistory.objects.create(
                clothing=serializer.instance,
                designer=designer,
                action='修改',
                description='更新服装信息',
                changes=changes
            )

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布服装"""
        clothing = self.get_object()
        if request.user != clothing.designer.user and not request.user.is_staff:
            return Response(
                {'error': '只有设计师本人或管理员可以发布服装'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        clothing.status = 'published'
        clothing.published_at = timezone.now()
        clothing.save()
        
        # 记录发布历史
        designer = get_object_or_404(Designer, user=request.user)
        ClothingHistory.objects.create(
            clothing=clothing,
            designer=designer,
            action='发布',
            description='发布服装'
        )
        
        return Response({'message': '服装发布成功'})

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """获取服装修改历史"""
        clothing = self.get_object()
        history = ClothingHistory.objects.filter(clothing=clothing)
        serializer = ClothingHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """高级搜索服装"""
        query = request.query_params.get('q', '')
        category = request.query_params.get('category')
        gender = request.query_params.get('gender')
        season = request.query_params.get('season')
        color = request.query_params.get('color')
        tags = request.query_params.getlist('tags')
        materials = request.query_params.getlist('materials')
        
        queryset = self.get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(style_number__icontains=query) |
                Q(description__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        if gender:
            queryset = queryset.filter(gender=gender)
        
        if season:
            queryset = queryset.filter(season_id=season)
        
        if color:
            queryset = queryset.filter(color__icontains=color)
        
        if tags:
            queryset = queryset.filter(tags__id__in=tags)
        
        if materials:
            queryset = queryset.filter(materials__id__in=materials)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ClothingListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ClothingListSerializer(queryset, many=True)
        return Response(serializer.data)

class ClothingHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """服装历史视图集"""
    queryset = ClothingHistory.objects.all()
    serializer_class = ClothingHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['clothing', 'designer', 'action']
    ordering_fields = ['created_at']

class UserPermissionViewSet(viewsets.ModelViewSet):
    """用户权限视图集"""
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'clothing', 'can_view', 'can_edit', 'can_delete']
    ordering_fields = ['granted_at']

    def perform_create(self, serializer):
        """创建权限时自动设置授权人"""
        serializer.save(granted_by=self.request.user)
