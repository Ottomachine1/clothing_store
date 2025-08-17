from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Designer(models.Model):
    """设计师模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='designer_profile')
    name = models.CharField(max_length=100, verbose_name='设计师姓名')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='电话')
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')
    avatar = models.ImageField(upload_to='designer_avatars/', blank=True, null=True, verbose_name='头像')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '设计师'
        verbose_name_plural = '设计师'

    def __str__(self):
        return self.name

class Category(models.Model):
    """服装分类模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    description = models.TextField(blank=True, null=True, verbose_name='分类描述')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='父分类')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '服装分类'
        verbose_name_plural = '服装分类'

    def __str__(self):
        return self.name

class Tag(models.Model):
    """标签模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='标签颜色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name

class Season(models.Model):
    """季节模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='季节名称')
    description = models.TextField(blank=True, null=True, verbose_name='季节描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '季节'
        verbose_name_plural = '季节'

    def __str__(self):
        return self.name

class Material(models.Model):
    """面料模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='面料名称')
    description = models.TextField(blank=True, null=True, verbose_name='面料描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '面料'
        verbose_name_plural = '面料'

    def __str__(self):
        return self.name

class Clothing(models.Model):
    """服装模型"""
    GENDER_CHOICES = [
        ('M', '男装'),
        ('F', '女装'),
        ('U', '中性'),
    ]
    
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    ]

    # 基本信息
    name = models.CharField(max_length=200, verbose_name='服装名称')
    style_number = models.CharField(max_length=50, unique=True, verbose_name='款式号')
    description = models.TextField(verbose_name='服装描述')
    
    # 分类信息
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='服装分类')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U', verbose_name='性别')
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True, verbose_name='适用季节')
    
    # 设计信息
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name='clothes', verbose_name='设计师')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    materials = models.ManyToManyField(Material, blank=True, verbose_name='面料')
    
    # 物理属性
    color = models.CharField(max_length=100, verbose_name='颜色')
    size_range = models.CharField(max_length=100, blank=True, null=True, verbose_name='尺码范围')
    price_range = models.CharField(max_length=100, blank=True, null=True, verbose_name='价格范围')
    
    # 媒体文件
    main_image = models.ImageField(upload_to='clothing_images/', verbose_name='主图')
    additional_images = models.JSONField(default=list, blank=True, verbose_name='附加图片')
    
    # 状态和时间
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')
    
    # 权限控制
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    view_permissions = models.ManyToManyField(User, blank=True, related_name='viewable_clothes', verbose_name='查看权限')

    class Meta:
        verbose_name = '服装'
        verbose_name_plural = '服装'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.style_number})"

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

class ClothingHistory(models.Model):
    """服装修改历史模型"""
    clothing = models.ForeignKey(Clothing, on_delete=models.CASCADE, related_name='history', verbose_name='服装')
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, verbose_name='设计师')
    action = models.CharField(max_length=50, verbose_name='操作类型')
    description = models.TextField(blank=True, null=True, verbose_name='修改描述')
    changes = models.JSONField(default=dict, verbose_name='修改内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '服装修改历史'
        verbose_name_plural = '服装修改历史'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.clothing.name} - {self.action} - {self.created_at}"

class UserPermission(models.Model):
    """用户权限模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    clothing = models.ForeignKey(Clothing, on_delete=models.CASCADE, verbose_name='服装')
    can_view = models.BooleanField(default=False, verbose_name='可查看')
    can_edit = models.BooleanField(default=False, verbose_name='可编辑')
    can_delete = models.BooleanField(default=False, verbose_name='可删除')
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='granted_permissions', verbose_name='授权人')
    granted_at = models.DateTimeField(auto_now_add=True, verbose_name='授权时间')
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name='过期时间')

    class Meta:
        verbose_name = '用户权限'
        verbose_name_plural = '用户权限'
        unique_together = ['user', 'clothing']

    def __str__(self):
        return f"{self.user.username} - {self.clothing.name}"
