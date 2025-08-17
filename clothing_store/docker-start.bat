@echo off
echo 🚀 启动服装管理平台 (Docker版本)
echo ==================================

REM 检查Docker是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未安装，请先安装Docker
    pause
    exit /b 1
)

REM 检查Docker Compose是否安装
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose未安装，请先安装Docker Compose
    pause
    exit /b 1
)

echo ✅ Docker环境检查通过

echo.
echo 请选择运行模式：
echo 1) 开发模式 (使用Django开发服务器)
echo 2) 生产模式 (使用Gunicorn + Nginx)
echo 3) 仅数据库 (只启动PostgreSQL和Redis)
set /p choice=请输入选择 (1-3): 

if "%choice%"=="1" (
    echo 🔧 启动开发模式...
    docker-compose -f docker-compose.dev.yml up --build
) else if "%choice%"=="2" (
    echo 🚀 启动生产模式...
    docker-compose up --build
) else if "%choice%"=="3" (
    echo 🗄️ 启动数据库服务...
    docker-compose -f docker-compose.dev.yml up db redis
) else (
    echo ❌ 无效选择，退出
    pause
    exit /b 1
)

pause
