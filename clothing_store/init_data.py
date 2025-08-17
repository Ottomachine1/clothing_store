#!/usr/bin/env python
"""
数据初始化脚本
用于创建基础的分类、季节、面料等数据
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()

from clothes.models import Category, Season, Material, Tag
from django.contrib.auth.models import User

def create_categories():
    """创建服装分类"""
    categories_data = [
        {'name': '上衣', 'description': '各种上衣类型'},
        {'name': '裤子', 'description': '各种裤子类型'},
        {'name': '裙子', 'description': '各种裙子类型'},
        {'name': '外套', 'description': '各种外套类型'},
        {'name': '内衣', 'description': '各种内衣类型'},
        {'name': '配饰', 'description': '各种配饰类型'},
    ]
    
    for data in categories_data:
        category, created = Category.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        if created:
            print(f"创建分类: {category.name}")
        else:
            print(f"分类已存在: {category.name}")

def create_seasons():
    """创建季节数据"""
    seasons_data = [
        {'name': '春季', 'description': '春季服装'},
        {'name': '夏季', 'description': '夏季服装'},
        {'name': '秋季', 'description': '秋季服装'},
        {'name': '冬季', 'description': '冬季服装'},
        {'name': '四季', 'description': '四季通用服装'},
    ]
    
    for data in seasons_data:
        season, created = Season.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        if created:
            print(f"创建季节: {season.name}")
        else:
            print(f"季节已存在: {season.name}")

def create_materials():
    """创建面料数据"""
    materials_data = [
        {'name': '棉质', 'description': '天然棉质面料'},
        {'name': '丝绸', 'description': '天然丝绸面料'},
        {'name': '羊毛', 'description': '天然羊毛面料'},
        {'name': '聚酯纤维', 'description': '合成纤维面料'},
        {'name': '尼龙', 'description': '合成尼龙面料'},
        {'name': '牛仔布', 'description': '牛仔面料'},
        {'name': '针织', 'description': '针织面料'},
        {'name': '蕾丝', 'description': '蕾丝面料'},
    ]
    
    for data in materials_data:
        material, created = Material.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        if created:
            print(f"创建面料: {material.name}")
        else:
            print(f"面料已存在: {material.name}")

def create_tags():
    """创建标签数据"""
    tags_data = [
        {'name': '时尚', 'color': '#FF6B6B'},
        {'name': '经典', 'color': '#4ECDC4'},
        {'name': '休闲', 'color': '#45B7D1'},
        {'name': '商务', 'color': '#96CEB4'},
        {'name': '运动', 'color': '#FFEAA7'},
        {'name': '优雅', 'color': '#DDA0DD'},
        {'name': '可爱', 'color': '#FFB6C1'},
        {'name': '复古', 'color': '#DEB887'},
        {'name': '简约', 'color': '#F0F8FF'},
        {'name': '奢华', 'color': '#FFD700'},
    ]
    
    for data in tags_data:
        tag, created = Tag.objects.get_or_create(
            name=data['name'],
            defaults={'color': data['color']}
        )
        if created:
            print(f"创建标签: {tag.name}")
        else:
            print(f"标签已存在: {tag.name}")

def create_superuser():
    """创建超级用户"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("创建超级用户: admin (密码: admin123)")
    else:
        print("超级用户已存在")

def main():
    """主函数"""
    print("开始初始化数据...")
    
    try:
        create_categories()
        create_seasons()
        create_materials()
        create_tags()
        create_superuser()
        
        print("\n数据初始化完成！")
        print("您可以使用以下账号登录管理后台:")
        print("用户名: admin")
        print("密码: admin123")
        
    except Exception as e:
        print(f"初始化过程中出现错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
