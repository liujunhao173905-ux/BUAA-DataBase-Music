#!/usr/bin/env python
"""
为测试歌手用户创建测试歌曲的脚本
"""

import os
import sys
import random
from datetime import datetime

# 添加Django项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# 导入模型
from apps.users.models import User
from apps.music.models import Song

# 测试歌曲数据
test_songs = [
    {
        'song_name': '测试歌曲1',
        'song_singer_id': None,  # 稍后会设置为测试歌手的ID
        'song_duration': 225,  # 歌曲时长，单位：秒
        'song_price': 0.00,  # 歌曲价格
        'is_active': True  # 立即上架
    },
    {
        'song_name': '测试歌曲2',
        'song_singer_id': None,
        'song_duration': 252,  # 歌曲时长，单位：秒
        'song_price': 0.00,
        'is_active': True
    },
    {
        'song_name': '测试歌曲3',
        'song_singer_id': None,
        'song_duration': 238,  # 歌曲时长，单位：秒
        'song_price': 1.00,
        'is_active': True
    },
    {
        'song_name': '测试歌曲4',
        'song_singer_id': None,
        'song_duration': 270,  # 歌曲时长，单位：秒
        'song_price': 1.00,
        'is_active': True
    },
    {
        'song_name': '测试歌曲5',
        'song_singer_id': None,
        'song_duration': 320,  # 歌曲时长，单位：秒
        'song_price': 0.00,
        'is_active': True
    }
]

def create_test_songs():
    """为测试歌手用户创建测试歌曲"""
    try:
        # 获取测试歌手用户
        test_singer = User.objects.get(user_name='test_singer')
        print(f"获取到测试歌手: {test_singer.user_name}, 用户ID: {test_singer.user_id}")
        
        # 为每首测试歌曲设置歌手ID并创建
        created_count = 0
        for song_data in test_songs:
            # 设置歌手ID
            song_data['song_singer_id'] = test_singer.user_id
            
            # 检查歌曲是否已存在
            existing_song = Song.objects.filter(
                song_name=song_data['song_name'],
                song_singer_id=test_singer.user_id
            ).first()
            
            if existing_song:
                print(f"歌曲 '{song_data['song_name']}' 已存在")
            else:
                # 创建歌曲（使用模拟的文件路径）
                song_data['song_file'] = 'songs/test_song.mp3'  # 模拟文件路径
                song_data['song_cover'] = 'covers/test_cover.jpg'  # 模拟封面路径
                
                # 创建歌曲
                song = Song.objects.create(**song_data)
                print(f"创建歌曲成功: '{song.song_name}', 歌曲ID: {song.song_id}")
                created_count += 1
        
        print(f"\n创建完成！共创建 {created_count} 首歌曲")
        print(f"测试歌手 '{test_singer.user_name}' 的歌曲总数: {Song.objects.filter(song_singer_id=test_singer.user_id).count()}")
        
    except User.DoesNotExist:
        print("测试歌手用户不存在，请先运行 create_test_singer.py 创建测试歌手")
    except Exception as e:
        print(f"创建测试歌曲失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_songs()
