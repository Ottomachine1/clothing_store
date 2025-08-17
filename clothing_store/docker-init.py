#!/usr/bin/env python
"""
Docker环境下的数据初始化脚本
用于在Docker容器中初始化基础数据
"""

import os
import sys
import django
import time

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')

def wait_for_database():
    """等待数据库连接就绪"""
    from django.db import connection
    from django.db.utils import OperationalError
    
    print("等待数据库连接...")
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            print("✅ 数据库连接成功")
            return True
        except OperationalError:
            attempt += 1
            print(f"⏳ 等待数据库连接... ({attempt}/{max_attempts})")
            time.sleep(2)
    
    print("❌ 数据库连接失败")
    return False

def create_superuser():
    """创建超级用户"""
    from django.contrib.auth.models import User
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ 创建超级用户: admin (密码: admin123)")
    else:
        print("ℹ️ 超级用户已存在")

def create_initial_data():
    """创建初始数据"""
    from clothes.models import Category, Season, Material, Tag
    
    # 创建分类
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
            print(f"✅ 创建分类: {category.name}")
        else:
            print(f"ℹ️ 分类已存在: {category.name}")
    
    # 创建季节
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
            print(f"✅ 创建季节: {season.name}")
        else:
            print(f"ℹ️ 季节已存在: {season.name}")
    
    # 创建面料
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
            print(f"✅ 创建面料: {material.name}")
        else:
            print(f"ℹ️ 面料已存在: {material.name}")
    
    # 创建标签
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
            defaults={'color': data['description']}
        )
        if created:
            print(f"✅ 创建标签: {tag.name}")
        else:
            print(f"ℹ️ 标签已存在: {tag.name}")

def main():
    """主函数"""
    print("🚀 开始Docker环境数据初始化...")
    print("=" * 50)
    
    try:
        # 等待数据库连接
        if not wait_for_database():
            sys.exit(1)
        
        # 设置Django
        django.setup()
        
        # 创建初始数据
        create_initial_data()
        create_superuser()
        
        print("\n" + "=" * 50)
        print("🎉 数据初始化完成！")
        print("\n访问信息:")
        print("前端页面: http://localhost:8000/")
        print("管理后台: http://localhost:8000/admin/")
        print("默认账号: admin")
        print("默认密码: admin123")
        
    except Exception as e:
        print(f"❌ 初始化过程中出现错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
