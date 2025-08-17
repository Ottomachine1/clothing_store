@echo off
echo 启动服装管理平台...
echo.

REM 检查虚拟环境是否存在
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo 虚拟环境创建完成！
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate

REM 安装依赖
echo 安装依赖包...
pip install -r requirements.txt

REM 运行数据库迁移
echo 运行数据库迁移...
python manage.py makemigrations
python manage.py migrate

REM 初始化基础数据
echo 初始化基础数据...
python init_data.py

REM 启动开发服务器
echo 启动开发服务器...
echo.
echo 访问地址:
echo 前端页面: http://127.0.0.1:8000/
echo 管理后台: http://127.0.0.1:8000/admin/
echo 默认账号: admin
echo 默认密码: admin123
echo.
echo 按 Ctrl+C 停止服务器
echo.
python manage.py runserver

pause
