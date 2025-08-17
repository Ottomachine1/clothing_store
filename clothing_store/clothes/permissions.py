from rest_framework import permissions
from django.utils import timezone
from .models import UserPermission

class IsDesignerOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只有设计师可以编辑，其他用户可以查看
    """
    
    def has_permission(self, request, view):
        # 允许所有用户查看
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 检查用户是否是设计师
        return hasattr(request.user, 'designer_profile')

    def has_object_permission(self, request, view, obj):
        # 允许所有用户查看
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 检查用户是否是设计师
        return hasattr(request.user, 'designer_profile')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只有对象所有者可以编辑，其他用户可以查看
    """
    
    def has_object_permission(self, request, view, obj):
        # 允许所有用户查看
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 检查用户是否是对象所有者
        if hasattr(obj, 'designer'):
            return obj.designer.user == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False

class IsDesignerOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只有服装的设计师可以编辑，其他用户可以查看
    """
    
    def has_object_permission(self, request, view, obj):
        # 允许所有用户查看
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 检查用户是否是服装的设计师
        return obj.designer.user == request.user

class CanViewClothing(permissions.BasePermission):
    """
    自定义权限：检查用户是否可以查看特定服装
    """
    
    def has_object_permission(self, request, view, obj):
        # 管理员可以查看所有服装
        if request.user.is_staff:
            return True
        
        # 公开的服装所有人都可以查看
        if obj.is_public:
            return True
        
        # 设计师可以查看自己设计的服装
        if hasattr(request.user, 'designer_profile') and obj.designer.user == request.user:
            return True
        
        # 检查是否有特殊查看权限
        try:
            permission = UserPermission.objects.get(
                user=request.user,
                clothing=obj,
                can_view=True
            )
            # 检查权限是否过期
            if permission.expires_at is None or permission.expires_at > timezone.now():
                return True
        except UserPermission.DoesNotExist:
            pass
        
        return False
