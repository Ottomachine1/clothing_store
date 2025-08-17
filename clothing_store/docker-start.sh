#!/bin/bash

echo "🚀 启动服装管理平台 (Docker版本)"
echo "=================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

echo "✅ Docker环境检查通过"

# 选择运行模式
echo ""
echo "请选择运行模式："
echo "1) 开发模式 (使用Django开发服务器)"
echo "2) 生产模式 (使用Gunicorn + Nginx)"
echo "3) 仅数据库 (只启动PostgreSQL和Redis)"
read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo "🔧 启动开发模式..."
        docker-compose -f docker-compose.dev.yml up --build
        ;;
    2)
        echo "🚀 启动生产模式..."
        docker-compose up --build
        ;;
    3)
        echo "🗄️ 启动数据库服务..."
        docker-compose -f docker-compose.dev.yml up db redis
        ;;
    *)
        echo "❌ 无效选择，退出"
        exit 1
        ;;
esac
