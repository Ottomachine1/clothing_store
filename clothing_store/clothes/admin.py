from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Designer, Category, Tag, Season, Material, 
    Clothing, ClothingHistory, UserPermission
)

@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'name', 'email', 'phone', 'bio', 'avatar')
        }),
        ('状态信息', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'description', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

class ClothingHistoryInline(admin.TabularInline):
    model = ClothingHistory
    extra = 0
    readonly_fields = ['designer', 'action', 'description', 'changes', 'created_at']
    can_delete = False

@admin.register(Clothing)
class ClothingAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'style_number', 'designer', 'category', 'gender', 
        'season', 'status', 'is_public', 'created_at'
    ]
    list_filter = [
        'category', 'gender', 'season', 'status', 'is_public', 
        'designer', 'created_at'
    ]
    search_fields = ['name', 'style_number', 'description', 'color']
    readonly_fields = ['created_at', 'updated_at', 'published_at']
    filter_horizontal = ['tags', 'materials', 'view_permissions']
    inlines = [ClothingHistoryInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'style_number', 'description', 'main_image', 'additional_images')
        }),
        ('分类信息', {
            'fields': ('category', 'gender', 'season')
        }),
        ('设计信息', {
            'fields': ('designer', 'tags', 'materials')
        }),
        ('物理属性', {
            'fields': ('color', 'size_range', 'price_range')
        }),
        ('状态控制', {
            'fields': ('status', 'is_public', 'view_permissions')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('designer', 'category', 'season')

@admin.register(ClothingHistory)
class ClothingHistoryAdmin(admin.ModelAdmin):
    list_display = ['clothing', 'designer', 'action', 'created_at']
    list_filter = ['action', 'designer', 'created_at']
    search_fields = ['clothing__name', 'designer__name', 'description']
    readonly_fields = ['clothing', 'designer', 'action', 'description', 'changes', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'clothing', 'can_view', 'can_edit', 'can_delete', 
        'granted_by', 'granted_at', 'expires_at'
    ]
    list_filter = ['can_view', 'can_edit', 'can_delete', 'granted_at']
    search_fields = ['user__username', 'clothing__name', 'granted_by__username']
    readonly_fields = ['granted_at']
    
    fieldsets = (
        ('权限信息', {
            'fields': ('user', 'clothing', 'can_view', 'can_edit', 'can_delete')
        }),
        ('授权信息', {
            'fields': ('granted_by', 'granted_at', 'expires_at')
        }),
    )
