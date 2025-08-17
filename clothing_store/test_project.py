#!/usr/bin/env python
"""
项目测试脚本
用于验证项目配置和基本功能是否正常
"""

import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings

def test_django_setup():
    """测试Django设置"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
        django.setup()
        print("✓ Django设置正常")
        return True
    except Exception as e:
        print(f"✗ Django设置失败: {e}")
        return False

def test_database_connection():
    """测试数据库连接"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✓ 数据库连接正常")
        return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return False

def test_models():
    """测试模型导入"""
    try:
        from clothes.models import Clothing, Designer, Category, Tag, Season, Material
        print("✓ 模型导入正常")
        return True
    except Exception as e:
        print(f"✗ 模型导入失败: {e}")
        return False

def test_admin():
    """测试管理后台配置"""
    try:
        from clothes.admin import ClothingAdmin, DesignerAdmin
        print("✓ 管理后台配置正常")
        return True
    except Exception as e:
        print(f"✗ 管理后台配置失败: {e}")
        return False

def test_urls():
    """测试URL配置"""
    try:
        from django.urls import reverse
        from django.test import Client
        client = Client()
        response = client.get('/')
        print("✓ URL配置正常")
        return True
    except Exception as e:
        print(f"✗ URL配置失败: {e}")
        return False

def run_tests():
    """运行Django测试"""
    try:
        test_runner = get_runner(settings)
        test_runner = test_runner()
        failures = test_runner.run_tests(["clothes"])
        if failures:
            print(f"✗ 测试失败: {failures}")
            return False
        else:
            print("✓ 所有测试通过")
            return True
    except Exception as e:
        print(f"✗ 测试运行失败: {e}")
        return False

def main():
    """主函数"""
    print("开始项目测试...")
    print("=" * 50)
    
    tests = [
        ("Django设置", test_django_setup),
        ("数据库连接", test_database_connection),
        ("模型导入", test_models),
        ("管理后台", test_admin),
        ("URL配置", test_urls),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n测试 {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"测试 {test_name} 失败")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 项目配置正常，可以开始使用！")
        print("\n下一步:")
        print("1. 运行 'python init_data.py' 初始化数据")
        print("2. 运行 'python manage.py runserver' 启动服务器")
        print("3. 访问 http://127.0.0.1:8000/ 查看前端页面")
        print("4. 访问 http://127.0.0.1:8000/admin/ 进入管理后台")
    else:
        print("❌ 项目配置存在问题，请检查错误信息")
        sys.exit(1)

if __name__ == '__main__':
    main()
