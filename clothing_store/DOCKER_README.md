# Docker部署指南

本文档详细说明如何使用Docker部署服装管理平台。

## 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少2GB可用内存
- 至少5GB可用磁盘空间

## 快速开始

### 1. 一键启动（推荐）

**Windows用户：**
```bash
docker-start.bat
```

**Linux/Mac用户：**
```bash
chmod +x docker-start.sh
./docker-start.sh
```

### 2. 手动启动

**开发模式：**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

**生产模式：**
```bash
docker-compose up --build
```

**仅数据库：**
```bash
docker-compose -f docker-compose.dev.yml up db redis
```

## 服务说明

### 核心服务

| 服务名 | 端口 | 说明 |
|--------|------|------|
| web | 8000 | Django应用服务器 |
| db | 5432 | PostgreSQL数据库 |
| redis | 6379 | Redis缓存 |
| nginx | 80,443 | Nginx反向代理（生产模式） |

### 可选服务

| 服务名 | 说明 |
|--------|------|
| celery | 异步任务处理 |
| celery-beat | 定时任务调度 |

## 环境配置

### 环境变量

复制 `env.example` 为 `.env` 并修改配置：

```bash
cp env.example .env
```

主要环境变量：

```bash
# Django设置
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# 数据库设置
DATABASE_URL=postgresql://postgres:postgres123@db:5432/clothing_store_db

# Redis设置
REDIS_URL=redis://redis:6379/0
```

### 生产环境配置

生产环境需要修改以下配置：

```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## 数据管理

### 数据持久化

项目使用Docker卷来持久化数据：

- `postgres_data`: PostgreSQL数据库数据
- `media_files`: 上传的媒体文件
- `static_files`: 静态文件

### 数据备份

**备份数据库：**
```bash
docker exec -t clothing_store_db_1 pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
```

**恢复数据库：**
```bash
cat dump_file.sql | docker exec -i clothing_store_db_1 psql -U postgres -d clothing_store_db
```

### 数据初始化

首次启动后，运行数据初始化脚本：

```bash
docker exec -it clothing_store_web_1 python docker-init.py
```

## 常用命令

### 服务管理

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启特定服务
docker-compose restart web

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs web
docker-compose logs -f web  # 实时日志
```

### 容器管理

```bash
# 进入容器
docker exec -it clothing_store_web_1 bash

# 执行Django命令
docker exec -it clothing_store_web_1 python manage.py migrate
docker exec -it clothing_store_web_1 python manage.py createsuperuser

# 查看容器资源使用
docker stats
```

### 镜像管理

```bash
# 重新构建镜像
docker-compose build --no-cache

# 清理未使用的镜像
docker image prune

# 清理所有未使用的资源
docker system prune -a
```

## 故障排除

### 常见问题

#### 1. 端口冲突
**问题：** 端口8000、5432、6379已被占用

**解决：** 修改 `docker-compose.yml` 中的端口映射

```yaml
ports:
  - "8001:8000"  # 改为8001
```

#### 2. 权限问题
**问题：** 无法创建目录或文件

**解决：** 检查Docker权限，确保有足够权限访问项目目录

#### 3. 数据库连接失败
**问题：** Django无法连接到PostgreSQL

**解决：** 
1. 检查数据库服务是否启动
2. 等待数据库完全启动（首次启动需要时间）
3. 检查环境变量配置

#### 4. 静态文件404
**问题：** 静态文件无法访问

**解决：**
```bash
docker exec -it clothing_store_web_1 python manage.py collectstatic --noinput
```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# 实时查看日志
docker-compose logs -f web
```

### 性能监控

```bash
# 查看容器资源使用
docker stats

# 查看系统资源使用
docker system df

# 查看卷使用情况
docker volume ls
docker volume inspect clothing_store_postgres_data
```

## 生产部署

### 1. 安全配置

- 修改默认密码
- 设置强密钥
- 配置SSL证书
- 限制访问IP

### 2. 性能优化

- 调整Gunicorn工作进程数
- 配置Nginx缓存
- 启用Redis缓存
- 优化数据库查询

### 3. 监控告警

- 配置日志轮转
- 设置资源监控
- 配置健康检查
- 设置告警通知

### 4. 备份策略

- 定期备份数据库
- 备份媒体文件
- 配置自动备份
- 测试恢复流程

## 扩展功能

### 添加新服务

在 `docker-compose.yml` 中添加新服务：

```yaml
services:
  new_service:
    image: service_image
    ports:
      - "8080:8080"
    networks:
      - clothing_network
    depends_on:
      - db
```

### 自定义Nginx配置

修改 `nginx/conf.d/default.conf` 添加新的路由规则。

### 配置SSL

在Nginx配置中添加SSL证书配置。

## 技术支持

如遇到问题，请：

1. 查看日志文件
2. 检查环境配置
3. 参考故障排除部分
4. 提交Issue或联系技术支持

---

**注意：** 生产环境部署前请仔细阅读安全配置部分，确保系统安全。
