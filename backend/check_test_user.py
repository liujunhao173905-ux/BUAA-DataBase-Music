#!/usr/bin/env python
"""
检查测试用户信息的脚本
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

def check_test_user():
    """检查测试用户信息"""
    try:
        print("检查测试用户 'test_singer'...")
        
        # 查询所有用户
        users = User.objects.all()
        print(f"\n数据库中有 {users.count()} 个用户:")
        for user in users:
            print(f"- 用户ID: {user.user_id}, 用户名: {user.user_name}, 用户类型: {user.user_type}, 激活状态: {user.is_active}")
        
        # 检查特定用户
        test_singer = User.objects.filter(user_name='test_singer').first()
        if test_singer:
            print(f"\n找到测试用户 'test_singer':")
            print(f"- 用户ID: {test_singer.user_id}")
            print(f"- 用户名: {test_singer.user_name}")
            print(f"- 用户类型: {test_singer.user_type} (1=歌手)")
            print(f"- 密码哈希: {test_singer.password}")
            print(f"- 激活状态: {test_singer.is_active}")
            print(f"- 注册时间: {test_singer.date_joined}")
            
            # 检查密码是否正确
            print(f"- 密码是否为 '123456': {test_singer.check_password('123456')}")
            
            # 检查用户的歌曲数量
            song_count = test_singer.songs.count()
            print(f"- 拥有的歌曲数量: {song_count}")
        else:
            print(f"\n未找到测试用户 'test_singer'")
            
    except Exception as e:
        print(f"检查用户失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_test_user()
