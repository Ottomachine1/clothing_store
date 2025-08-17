from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Designer, Category, Tag, Season, Material, 
    Clothing, ClothingHistory, UserPermission
)

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']

class DesignerSerializer(serializers.ModelSerializer):
    """设计师序列化器"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Designer
        fields = [
            'id', 'user', 'user_id', 'name', 'email', 'phone', 'bio', 
            'avatar', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'parent_name', 'created_at']
        read_only_fields = ['id', 'created_at']

class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'created_at']
        read_only_fields = ['id', 'created_at']

class SeasonSerializer(serializers.ModelSerializer):
    """季节序列化器"""
    class Meta:
        model = Season
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class MaterialSerializer(serializers.ModelSerializer):
    """面料序列化器"""
    class Meta:
        model = Material
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class ClothingSerializer(serializers.ModelSerializer):
    """服装序列化器"""
    designer_name = serializers.CharField(source='designer.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    season_name = serializers.CharField(source='season.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    
    class Meta:
        model = Clothing
        fields = [
            'id', 'name', 'style_number', 'description', 'category', 'category_name',
            'gender', 'season', 'season_name', 'designer', 'designer_name', 'tags',
            'materials', 'color', 'size_range', 'price_range', 'main_image',
            'additional_images', 'status', 'created_at', 'updated_at', 'published_at',
            'is_public'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'published_at']

class ClothingListSerializer(serializers.ModelSerializer):
    """服装列表序列化器（简化版）"""
    designer_name = serializers.CharField(source='designer.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    season_name = serializers.CharField(source='season.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Clothing
        fields = [
            'id', 'name', 'style_number', 'designer_name', 'category_name',
            'season_name', 'gender', 'color', 'main_image', 'tags', 'status',
            'created_at', 'updated_at', 'is_public'
        ]

class ClothingCreateSerializer(serializers.ModelSerializer):
    """服装创建序列化器"""
    class Meta:
        model = Clothing
        fields = [
            'name', 'style_number', 'description', 'category', 'gender', 'season',
            'tags', 'materials', 'color', 'size_range', 'price_range', 'main_image',
            'additional_images', 'status', 'is_public'
        ]

class ClothingHistorySerializer(serializers.ModelSerializer):
    """服装历史序列化器"""
    designer_name = serializers.CharField(source='designer.name', read_only=True)
    
    class Meta:
        model = ClothingHistory
        fields = [
            'id', 'clothing', 'designer', 'designer_name', 'action', 'description',
            'changes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class UserPermissionSerializer(serializers.ModelSerializer):
    """用户权限序列化器"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    clothing_name = serializers.CharField(source='clothing.name', read_only=True)
    granted_by_username = serializers.CharField(source='granted_by.username', read_only=True)
    
    class Meta:
        model = UserPermission
        fields = [
            'id', 'user', 'user_username', 'clothing', 'clothing_name',
            'can_view', 'can_edit', 'can_delete', 'granted_by', 'granted_by_username',
            'granted_at', 'expires_at'
        ]
        read_only_fields = ['id', 'granted_at']
