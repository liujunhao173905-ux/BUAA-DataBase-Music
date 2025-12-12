#!/usr/bin/env python
"""
初始化脚本：生成已上架的测试歌曲数据
"""
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.users.models import User
from apps.music.models import Song

def create_test_songs():
    """创建已上架的测试歌曲"""
    print("=== 开始生成已上架的测试歌曲 ===")
    
    # 创建或获取歌手用户
    try:
        singer = User.objects.get(user_name='popular_singer')
        print(f"歌手用户已存在：{singer.user_name}")
    except User.DoesNotExist:
        singer = User.objects.create_user(
            user_name='popular_singer',
            password='singer123',
            user_type=1
        )
        print(f"歌手用户创建成功：{singer.user_name}")
    
    # 测试歌曲列表
    test_songs = [
        {"song_name": "晴天", "song_duration": 268, "song_price": 9.99},
        {"song_name": "七里香", "song_duration": 364, "song_price": 12.99},
        {"song_name": "青花瓷", "song_duration": 237, "song_price": 10.99},
        {"song_name": "夜曲", "song_duration": 231, "song_price": 8.99},
        {"song_name": "以父之名", "song_duration": 514, "song_price": 15.99},
        {"song_name": "稻香", "song_duration": 324, "song_price": 11.99},
        {"song_name": "东风破", "song_duration": 301, "song_price": 10.99},
        {"song_name": "双截棍", "song_duration": 242, "song_price": 9.99},
        {"song_name": "安静", "song_duration": 255, "song_price": 8.99},
        {"song_name": "轨迹", "song_duration": 293, "song_price": 10.99},
        {"song_name": "珊瑚海", "song_duration": 286, "song_price": 12.99},
        {"song_name": "借口", "song_duration": 359, "song_price": 11.99},
    ]
    
    # 创建已上架的歌曲（is_active=True）
    created_count = 0
    for song_data in test_songs:
        # 检查歌曲是否已存在
        if not Song.objects.filter(song_name=song_data['song_name'], song_singer=singer).exists():
            Song.objects.create(
                song_name=song_data['song_name'],
                song_singer=singer,
                song_duration=song_data['song_duration'],
                song_price=song_data['song_price'],
                is_active=True  # 已上架，无需审核
            )
            created_count += 1
            print(f"创建歌曲成功：{song_data['song_name']}")
        else:
            print(f"歌曲已存在：{song_data['song_name']}")
    
    print(f"\n=== 初始化完成！创建了 {created_count} 首已上架的测试歌曲 ===")
    
    # 显示所有已上架的歌曲
    print("\n=== 已上架歌曲列表 ===")
    songs = Song.objects.filter(is_active=True).order_by('song_name')
    for song in songs:
        print(f"{song.song_name} - {song.song_singer.user_name} - 时长: {song.song_duration}秒 - 价格: {song.song_price}元")

def main():
    """主函数"""
    create_test_songs()

if __name__ == '__main__':
    main()
