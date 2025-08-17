# 服装管理平台

一个基于Django的服装管理平台，支持前后端分离，用于管理公司内部设计的服装作品。

## 功能特性

### 前端功能
- 服装展示页面，支持网格布局
- 设计师作品展示
- 多维度搜索和筛选（颜色、特点、季节、款式号、面料等）
- 设计师作品上传和管理
- 标签系统
- 响应式设计

### 后端功能
- 用户管理和权限控制
- 设计师管理
- 服装CRUD操作
- 分类、标签、季节、面料管理
- 修改历史记录
- 权限管理系统
- RESTful API支持

## 技术栈

- **后端**: Django 5.0 + Django REST Framework
- **数据库**: PostgreSQL (生产) / SQLite (开发)
- **前端**: Bootstrap 5 + Font Awesome
- **管理后台**: Django SimpleUI
- **权限**: Django内置权限系统 + 自定义权限
- **容器化**: Docker + Docker Compose
- **缓存**: Redis
- **异步任务**: Celery

## 快速开始

### 方式一：Docker部署（推荐）

#### 1. 安装Docker和Docker Compose
确保您的系统已安装Docker和Docker Compose。

#### 2. 克隆项目
```bash
git clone <repository-url>
cd clothing_store
```

#### 3. 启动项目
**Windows用户：**
```bash
docker-start.bat
```

**Linux/Mac用户：**
```bash
chmod +x docker-start.sh
./docker-start.sh
```

**手动启动：**
```bash
# 开发模式
docker-compose -f docker-compose.dev.yml up --build

# 生产模式
docker-compose up --build

# 仅数据库
docker-compose -f docker-compose.dev.yml up db redis
```

#### 4. 访问应用
- **前端页面**: http://localhost:8000/
- **管理后台**: http://localhost:8000/admin/
- **默认账号**: admin
- **默认密码**: admin123

### 方式二：传统部署

#### 1. 克隆项目
```bash
git clone <repository-url>
cd clothing_store
```

#### 2. 创建虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量
复制 `env.example` 为 `.env` 并修改配置：
```bash
cp env.example .env
# 编辑 .env 文件
```

#### 5. 运行数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. 初始化数据
```bash
python init_data.py
```

#### 7. 启动开发服务器
```bash
python manage.py runserver
```

## Docker配置说明

### 服务架构
- **web**: Django应用服务器
- **db**: PostgreSQL数据库
- **redis**: Redis缓存
- **nginx**: Nginx反向代理（生产模式）
- **celery**: 异步任务处理（可选）

### 环境变量
主要环境变量说明：
- `DEBUG`: 调试模式开关
- `SECRET_KEY`: Django密钥
- `DATABASE_URL`: 数据库连接字符串
- `REDIS_URL`: Redis连接字符串
- `ALLOWED_HOSTS`: 允许的主机名

### 数据持久化
- PostgreSQL数据存储在 `postgres_data` 卷中
- 媒体文件存储在 `media_files` 卷中
- 静态文件存储在 `static_files` 卷中

## 项目结构

```
clothing_store/
├── clothing_store/          # 项目配置
│   ├── settings.py         # 项目设置
│   ├── urls.py            # 主URL配置
│   ├── wsgi.py            # WSGI配置
│   └── celery.py          # Celery配置
├── clothes/                # 主应用
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图和API
│   ├── serializers.py     # 序列化器
│   ├── permissions.py     # 权限类
│   ├── admin.py           # 管理后台配置
│   └── urls.py            # 应用URL配置
├── templates/              # HTML模板
├── nginx/                  # Nginx配置
│   ├── nginx.conf         # 主配置
│   └── conf.d/            # 站点配置
├── docker-compose.yml      # 生产环境配置
├── docker-compose.dev.yml  # 开发环境配置
├── Dockerfile              # Docker镜像构建
├── requirements.txt        # 项目依赖
├── docker-start.sh         # Docker启动脚本(Linux/Mac)
├── docker-start.bat        # Docker启动脚本(Windows)
├── docker-init.py          # Docker数据初始化
└── README.md               # 项目说明
```

## 数据模型

### 核心模型
- **User**: 用户基础信息
- **Designer**: 设计师信息
- **Clothing**: 服装信息
- **Category**: 服装分类
- **Tag**: 标签系统
- **Season**: 季节信息
- **Material**: 面料信息
- **ClothingHistory**: 修改历史
- **UserPermission**: 用户权限

## API接口

### 主要端点
- `GET /api/clothes/` - 获取服装列表
- `POST /api/clothes/` - 创建新服装
- `GET /api/clothes/{id}/` - 获取服装详情
- `PUT /api/clothes/{id}/` - 更新服装
- `DELETE /api/clothes/{id}/` - 删除服装
- `POST /api/clothes/{id}/publish/` - 发布服装
- `GET /api/clothes/{id}/history/` - 获取修改历史

### 筛选和搜索
- 支持按分类、性别、季节、颜色等筛选
- 全文搜索（名称、款式号、描述）
- 标签和面料筛选
- 分页支持

## 权限系统

### 用户角色
- **超级管理员**: 完全访问权限
- **设计师**: 可以管理自己的作品
- **普通用户**: 只能查看公开内容

### 权限控制
- 服装查看权限
- 编辑权限（仅设计师本人）
- 删除权限（仅设计师本人或管理员）
- 特殊权限授予系统

## 部署说明

### 开发环境
使用 `docker-compose.dev.yml` 配置文件，包含：
- Django开发服务器
- PostgreSQL数据库
- Redis缓存
- 热重载支持

### 生产环境
使用 `docker-compose.yml` 配置文件，包含：
- Gunicorn应用服务器
- Nginx反向代理
- PostgreSQL数据库
- Redis缓存
- Celery异步任务处理

### 环境变量配置
1. 复制 `env.example` 为 `.env`
2. 修改生产环境配置
3. 设置安全的 `SECRET_KEY`
4. 配置数据库连接字符串

## 开发说明

### 添加新功能
1. 在 `models.py` 中定义数据模型
2. 在 `serializers.py` 中创建序列化器
3. 在 `views.py` 中实现视图逻辑
4. 在 `admin.py` 中配置管理后台
5. 在 `urls.py` 中添加路由
6. 创建相应的模板文件

### 代码规范
- 使用中文注释
- 遵循PEP 8代码风格
- 编写单元测试
- 使用类型提示

## 常见问题

### Docker相关问题
1. **端口冲突**: 修改 `docker-compose.yml` 中的端口映射
2. **权限问题**: 确保Docker有足够权限访问项目目录
3. **数据丢失**: 使用 `docker-compose down -v` 会删除数据卷

### 数据库相关问题
1. **连接失败**: 检查数据库服务是否启动
2. **迁移失败**: 删除数据库卷重新创建
3. **数据初始化**: 运行 `docker-init.py` 脚本

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 参与讨论

---

**注意**: 这是一个初始版本，后续会根据需求进行进一步改进和完善。
