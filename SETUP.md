# 项目启动指南

## 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

## 详细启动步骤

### 1. 后端启动

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（Windows）
python -m venv venv
venv\Scripts\activate

# 2. 创建虚拟环境（Linux/Mac）
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库（首次搭环境务必执行）
# 4.1 如果仓库中已有迁移文件，直接 migrate
python manage.py migrate

# 4.2 如果提示缺少业务表（如 songs），说明迁移文件未生成
# 针对缺失的 APP 生成迁移再执行 migrate
python manage.py makemigrations users music playlists
python manage.py migrate

# 4.3 若看到 “Migration admin.0001_initial is applied before its dependency users.0001_initial”
# 说明旧数据库状态和新迁移不一致，可按常见问题章节处理（删除 db.sqlite3 或使用 --fake）

# 5. 创建管理员账户（可选）
python manage.py createsuperuser
# 输入用户名、邮箱（可选）、密码

# 6. 启动开发服务器
python manage.py runserver
```

后端服务将在 `http://localhost:8000` 启动

### 2. 前端启动

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install
# 或使用 yarn
yarn install

# 3. 启动开发服务器
npm run dev
# 或
yarn dev
```

前端服务将在 `http://localhost:3000` 启动

### 3. 访问系统

- 前端地址：http://localhost:3000
- 后端API：http://localhost:8000
- 管理后台：http://localhost:8000/admin

## 测试账户

### 创建测试用户

```bash
# 进入Django shell
python manage.py shell
```

```python
from apps.users.models import User

# 创建普通用户
user = User.objects.create_user('user1', password='123456', user_type=0)

# 创建歌手（需要审核）
singer = User.objects.create_user('singer1', password='123456', user_type=1)

# 创建管理员
admin = User.objects.create_user('admin', password='admin123', user_type=2)
admin.is_staff = True
admin.is_superuser = True
admin.save()
```

## 常见问题

### 1. 数据库迁移失败

**情况 A：首次搭环境/没有重要数据**

```bash
# 停掉 runserver 后删除 SQLite 文件（Windows 请使用 del）
rm db.sqlite3

# 重新迁移（若提示缺表，先针对 APP 生成迁移）
python manage.py makemigrations users music playlists
python manage.py migrate
```

**情况 B：提示 “Migration admin.0001_initial is applied before its dependency users.0001_initial”**

- 原因：数据库中已经记录 admin 的迁移，但 users/music 等迁移刚生成，顺序不一致。
- 解决：最简单是按照 **情况 A** 清空数据库重跑；如果必须保留数据，可使用 `--fake` 先标记依赖，再检查表结构是否完整：

```bash
python manage.py migrate users 0001 --fake
python manage.py migrate music 0001 --fake
python manage.py migrate playlists 0001 --fake
python manage.py migrate
```

**情况 C：运行 API 返回 “no such table: songs”**

- 表示迁移未执行或失败，参考上面步骤重新生成并应用迁移即可。

### 2. 媒体文件无法访问

确保 `backend/media/` 目录存在且有写入权限：

```bash
mkdir -p backend/media/songs
mkdir -p backend/media/covers
mkdir -p backend/media/avatars
```

### 3. CORS错误

检查 `backend/config/settings.py` 中的 CORS 配置：

```python
CORS_ALLOW_ALL_ORIGINS = True  # 开发环境
```

### 4. 前端无法连接后端

检查 `frontend/vite.config.ts` 中的代理配置：

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  },
}
```

## 生产环境部署

### 后端部署

1. 修改 `settings.py`：
   - `DEBUG = False`
   - 配置 `ALLOWED_HOSTS`
   - 使用 PostgreSQL 或 MySQL
   - 配置静态文件和媒体文件服务

2. 收集静态文件：
```bash
python manage.py collectstatic
```

### 前端部署

```bash
# 构建生产版本
npm run build

# 构建文件在 dist/ 目录
```

## 开发建议

1. 使用虚拟环境隔离依赖
2. 定期备份数据库
3. 使用版本控制（Git）
4. 遵循代码规范
5. 编写单元测试

