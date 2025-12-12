#!/usr/bin/env python
"""
创建测试歌手用户的脚本
"""

import os
import sys

# 添加Django项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# 导入User模型
from apps.users.models import User

# 创建测试歌手用户
try:
    # 检查用户是否已存在
    existing_user = User.objects.filter(user_name='test_singer').first()
    if existing_user:
        print(f"用户 'test_singer' 已存在，用户ID: {existing_user.user_id}")
        print(f"用户类型: {existing_user.user_type} (1=歌手)")
        # 如果不是歌手，更新为歌手
        if existing_user.user_type != 1:
            existing_user.user_type = 1
            existing_user.save()
            print("已将用户更新为歌手类型")
    else:
        # 创建新用户
        user = User.objects.create_user(
            user_name='test_singer',
            password='123456',
            user_type=1,  # 设置为歌手类型
            is_active=True
        )
        print(f"创建歌手用户成功，用户ID: {user.user_id}")
        print(f"用户名: {user.user_name}")
        print(f"用户类型: {user.user_type} (1=歌手)")
except Exception as e:
    print(f"创建用户失败: {str(e)}")
