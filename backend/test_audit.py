#!/usr/bin/env python
"""
测试脚本：生成管理员用户和待审核歌曲，用于测试审核功能
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.music.models import Song
from apps.audit.models import CheckSongLog

def create_test_admin():
    """创建测试管理员用户"""
    try:
        # 检查是否已存在管理员用户
        admin = User.objects.get(user_name='admin')
        print(f"管理员用户已存在：{admin.user_name}")
        return admin
    except User.DoesNotExist:
        # 创建管理员用户
        admin = User.objects.create_superuser(
            user_name='admin',
            password='admin123',
            user_type=2
        )
        print(f"管理员用户创建成功：{admin.user_name}")
        return admin

def create_test_song():
    """创建测试待审核歌曲"""
    # 先创建一个歌手用户
    try:
        singer = User.objects.get(user_name='test_singer')
        print(f"歌手用户已存在：{singer.user_name}")
    except User.DoesNotExist:
        singer = User.objects.create_user(
            user_name='test_singer',
            password='singer123',
            user_type=1
        )
        print(f"歌手用户创建成功：{singer.user_name}")
    
    # 创建待审核歌曲（is_active=False表示需要审核）
    song = Song.objects.create(
        song_name='测试歌曲',
        song_singer=singer,
        song_duration=180,
        song_price=9.99,
        is_active=False  # 未激活，需要审核
    )
    print(f"待审核歌曲创建成功：{song.song_name}")
    
    # 检查是否生成了审核记录
    check_log = CheckSongLog.objects.filter(check_song=song).first()
    if check_log:
        print(f"审核记录生成成功：ID={check_log.check_id}, 状态={check_log.check_status}")
    else:
        print("警告：审核记录未生成！")
    
    return song

def list_check_songs():
    """列出所有待审核歌曲"""
    print("\n=== 待审核歌曲列表 ===")
    check_logs = CheckSongLog.objects.filter(check_status=0)  # 待审核状态
    if check_logs:
        for log in check_logs:
            print(f"ID: {log.check_id}, 歌曲: {log.check_song_name}, 提交时间: {log.check_submit_time}")
    else:
        print("暂无待审核歌曲")

def main():
    """主函数"""
    print("=== 审核功能测试脚本 ===")
    
    # 创建管理员用户
    create_test_admin()
    
    # 创建测试歌曲
    create_test_song()
    
    # 列出待审核歌曲
    list_check_songs()
    
    print("\n=== 测试完成 ===")
    print("管理员登录信息：")
    print("用户名：admin")
    print("密码：admin123")
    print("请使用此账号登录前端系统，访问 http://localhost:3001/admin/songs 查看待审核歌曲")

if __name__ == '__main__':
    main()
