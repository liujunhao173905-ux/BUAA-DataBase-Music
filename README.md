# BUAA-DataBase-Music
# 音乐平台系统

基于Vue 3 + Django + SQLite的三端音乐平台（用户端、歌手端、管理员端）

## 项目结构

```
music-platform/
├── backend/                 # Django后端
│   ├── apps/
│   │   ├── users/           # 用户管理
│   │   ├── music/           # 音乐管理
│   │   ├── playlists/       # 歌单管理
│   │   ├── audit/           # 审核系统
│   │   └── analytics/       # 统计分析
│   ├── config/              # Django配置
│   └── manage.py
├── frontend/                # Vue 3前端
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   ├── components/      # 通用组件
│   │   ├── stores/          # Pinia状态管理
│   │   ├── api/             # API接口
│   │   └── router/          # 路由配置
│   └── package.json
└── README.md
```

## 技术栈

### 后端
- Django 4.2.7
- Django REST Framework 3.14.0
- JWT认证 (djangorestframework-simplejwt)
- SQLite数据库
- Pillow (图片处理)

### 前端
- Vue 3 (Composition API)
- TypeScript
- Vite
- Pinia (状态管理)
- Element Plus (UI组件)
- Axios (HTTP客户端)

## 数据库设计

系统包含12张表，满足3NF范式：

1. **用户表 (User)** - 用户基本信息
2. **歌单表 (Playlist)** - 歌单信息
3. **歌曲表 (Song)** - 歌曲信息和文件路径
4. **歌单歌曲表 (PlaylistSong)** - 歌单与歌曲关联
5. **用户收藏歌单表 (StarPlaylist)** - 用户收藏的歌单
6. **用户收藏歌曲表 (StarSong)** - 用户收藏的歌曲
7. **用户购买歌曲表 (BuySong)** - 用户购买的收费歌曲
8. **用户关注表 (Follow)** - 用户之间的关注关系
9. **用户登录日志 (LoginLog)** - 登录记录
10. **歌单审核日志 (CheckPlaylistLog)** - 歌单审核历史
11. **歌曲审核日志 (CheckSongLog)** - 歌曲审核历史
12. **用户审核日志 (CheckUserLog)** - 用户（歌手）审核历史

## 快速开始

### 1. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

后端服务将在 `http://localhost:8000` 启动

### 2. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

## 用户类型与权限

### 普通用户 (user_type=0)
- 浏览和搜索歌曲
- 播放免费歌曲
- 购买收费歌曲
- 收藏歌曲和歌单
- 关注歌手
- 创建和管理自己的歌单

### 歌手 (user_type=1)
- 拥有普通用户的所有权限
- 上传和管理自己的歌曲
- 查看歌曲统计数据（收藏数、购买数、收入等）
- 歌曲需要管理员审核后才能上架

### 管理员 (user_type=2)
- 拥有所有权限
- 审核歌曲、歌单、用户注册申请
- 查看系统统计数据
- 查看登录日志
- 管理所有数据

## API接口说明

### 用户认证
- `POST /api/users/register/` - 用户注册
- `POST /api/users/login/` - 用户登录
- `GET /api/users/profile/` - 获取当前用户资料
- `PUT /api/users/profile/` - 更新用户资料

### 音乐管理
- `GET /api/music/songs/` - 获取歌曲列表（支持搜索、筛选）
- `GET /api/music/songs/{id}/` - 获取歌曲详情
- `POST /api/music/songs/` - 上传歌曲（歌手）
- `PUT /api/music/songs/{id}/` - 更新歌曲（歌手）
- `DELETE /api/music/songs/{id}/` - 删除歌曲（歌手）
- `POST /api/music/songs/{id}/star/` - 收藏歌曲
- `DELETE /api/music/songs/{id}/unstar/` - 取消收藏
- `POST /api/music/songs/{id}/buy/` - 购买歌曲
- `GET /api/music/songs/my_songs/` - 获取我的歌曲（歌手）
- `GET /api/music/songs/starred/` - 获取收藏的歌曲
- `GET /api/music/songs/bought/` - 获取购买的歌曲
- `GET /api/music/songs/{id}/statistics/` - 获取歌曲统计（歌手）

### 歌单管理
- `GET /api/playlists/playlists/` - 获取歌单列表
- `GET /api/playlists/playlists/{id}/` - 获取歌单详情
- `POST /api/playlists/playlists/` - 创建歌单
- `PUT /api/playlists/playlists/{id}/` - 更新歌单
- `DELETE /api/playlists/playlists/{id}/` - 删除歌单
- `POST /api/playlists/playlists/{id}/add_song/` - 向歌单添加歌曲
- `DELETE /api/playlists/playlists/{id}/remove_song/` - 从歌单移除歌曲
- `POST /api/playlists/playlists/{id}/star/` - 收藏歌单
- `GET /api/playlists/playlists/my_playlists/` - 获取我的歌单
- `GET /api/playlists/playlists/starred/` - 获取收藏的歌单

### 审核系统
- `GET /api/audit/songs/` - 获取歌曲审核列表
- `GET /api/audit/songs/{id}/` - 获取审核详情
- `POST /api/audit/songs/{id}/approve/` - 审核通过（管理员）
- `POST /api/audit/songs/{id}/reject/` - 审核拒绝（管理员）
- `GET /api/audit/playlists/` - 获取歌单审核列表
- `POST /api/audit/playlists/{id}/approve/` - 审核通过（管理员）
- `GET /api/audit/users/` - 获取用户审核列表
- `POST /api/audit/users/{id}/approve/` - 审核通过（管理员）

### 统计分析
- `GET /api/analytics/login/` - 登录统计（管理员）
- `GET /api/analytics/users/` - 用户统计（管理员）
- `GET /api/analytics/music/` - 音乐统计（管理员）
- `GET /api/analytics/playlists/` - 歌单统计（管理员）

## 核心功能

### 1. 用户认证系统
- JWT Token认证
- 用户注册、登录、登出
- 用户资料管理
- 权限控制（用户/歌手/管理员）

### 2. 音乐管理
- 歌曲上传（支持音频文件和封面图片）
- 歌曲列表浏览和搜索
- 歌曲播放（支持音频播放）
- 歌曲收藏和购买
- 歌曲统计（收藏数、购买数、收入等）

### 3. 歌单管理
- 歌单创建和管理
- 向歌单添加/移除歌曲
- 歌单收藏
- 歌单审核

### 4. 审核系统
- 歌曲审核（上传/修改后需审核）
- 歌单审核（创建/修改后需审核）
- 用户审核（歌手注册需审核）
- 审核历史记录

### 5. 统计分析
- 登录统计
- 用户统计
- 音乐统计
- 歌单统计

## 开发说明

### 数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 查看迁移状态
python manage.py showmigrations
```

### 创建测试数据

```bash
# 进入Django shell
python manage.py shell

# 创建测试用户
from apps.users.models import User
user = User.objects.create_user('testuser', password='test123')
singer = User.objects.create_user('singer', password='test123', user_type=1)
admin = User.objects.create_user('admin', password='admin123', user_type=2)
```

### 媒体文件配置

上传的音频文件和图片会存储在 `backend/media/` 目录下：
- `media/songs/` - 音频文件
- `media/covers/` - 封面图片
- `media/avatars/` - 用户头像

## 注意事项

1. **SQLite限制**：SQLite适合开发和小型项目，生产环境建议使用PostgreSQL或MySQL
2. **文件上传**：确保 `media/` 目录有写入权限
3. **CORS配置**：开发环境已配置允许所有来源，生产环境需要修改
4. **JWT Token**：Token有效期24小时，刷新Token有效期7天
5. **审核流程**：歌曲和歌单创建/修改后自动创建审核记录，需要管理员审核通过后才能上架

## 项目特点

- ✅ 完整的12张数据库表设计（满足3NF）
- ✅ 三端权限系统（用户/歌手/管理员）
- ✅ JWT认证和权限控制
- ✅ 完整的CRUD API
- ✅ 审核流程实现
- ✅ 统计分析功能
- ✅ 文件上传支持
- ✅ 搜索和筛选功能
- ✅ TypeScript类型安全
- ✅ 详细的代码注释

## 许可证

本项目为课程作业项目，仅供学习使用。

## 作者

- 刘明昊 (23373440)
- 刘峻昊 (23373452)
- 程嘉烨 (23373532)

