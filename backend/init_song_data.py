#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化歌曲数据脚本
用于创建测试歌手和歌曲数据
"""
import os
import sys
import django
import random
from django.conf import settings
from django.utils import timezone

# 添加项目路径到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# 导入所需的模型
from apps.users.models import User
from apps.music.models import Song
from apps.audit.models import CheckSongLog, CheckUserLog

# 模拟歌曲数据
song_data = [
    {
        'song_name': '春日部',
        'song_duration': 240,
        'song_price': 2.00,
        'song_cover_path': 'covers/spring_town.jpg',
        'song_file_path': 'songs/spring_town.mp3'
    },
    {
        'song_name': '星空漫步',
        'song_duration': 210,
        'song_price': 0.00,
        'song_cover_path': 'covers/stars_walk.jpg',
        'song_file_path': 'songs/stars_walk.mp3'
    },
    {
        'song_name': '夏日回忆',
        'song_duration': 270,
        'song_price': 3.00,
        'song_cover_path': 'covers/summer_memory.jpg',
        'song_file_path': 'songs/summer_memory.mp3'
    },
    {
        'song_name': '午夜旋律',
        'song_duration': 180,
        'song_price': 1.50,
        'song_cover_path': 'covers/midnight_melody.jpg',
        'song_file_path': 'songs/midnight_melody.mp3'
    },
    {
        'song_name': '雨巷',
        'song_duration': 225,
        'song_price': 2.50,
        'song_cover_path': 'covers/rainy_alley.jpg',
        'song_file_path': 'songs/rainy_alley.mp3'
    }
]

# 歌手数据
singer_data = [
    {
        'user_name': 'singer_zhang',
        'password': '123456',
        'user_type': 1,
        'user_mobile': '13800138001'
    },
    {
        'user_name': 'singer_li',
        'password': '123456',
        'user_type': 1,
        'user_mobile': '13800138002'
    },
    {
        'user_name': 'singer_wang',
        'password': '123456',
        'user_type': 1,
        'user_mobile': '13800138003'
    }
]

def create_test_singers():
    """创建测试歌手用户"""
    print("开始创建测试歌手...")
    singers = []
    
    for singer_info in singer_data:
        # 检查用户是否已存在
        try:
            singer = User.objects.get(user_name=singer_info['user_name'])
            print(f"歌手 {singer_info['user_name']} 已存在")
        except User.DoesNotExist:
            # 创建新歌手
            singer = User.objects.create_user(
                user_name=singer_info['user_name'],
                password=singer_info['password'],
                user_type=singer_info['user_type'],
                user_mobile=singer_info['user_mobile']
            )
            print(f"创建歌手 {singer_info['user_name']} 成功")
            
            # 创建歌手审核记录
            CheckUserLog.objects.create(
                check_user=singer,
                check_user_name=singer.user_name,
                check_user_mobile=singer.user_mobile or '',
                check_user_type=singer.user_type,
                check_status=1  # 直接审核通过
            )
        
        singers.append(singer)
    
    return singers

def create_test_songs(singers):
    """创建测试歌曲"""
    print("开始创建测试歌曲...")
    
    # 确保媒体目录存在
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'covers'), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'songs'), exist_ok=True)
    
    for i, song_info in enumerate(song_data):
        # 随机选择一个歌手
        singer = random.choice(singers)
        
        # 检查歌曲是否已存在
        try:
            existing_song = Song.objects.get(song_name=song_info['song_name'])
            print(f"歌曲 {song_info['song_name']} 已存在")
            continue
        except Song.DoesNotExist:
            # 创建空文件作为占位符
            cover_file_path = os.path.join(settings.MEDIA_ROOT, song_info['song_cover_path'])
            song_file_path = os.path.join(settings.MEDIA_ROOT, song_info['song_file_path'])
            
            # 创建空文件
            with open(cover_file_path, 'w') as f:
                f.write('This is a placeholder for song cover')
            
            with open(song_file_path, 'w') as f:
                f.write('This is a placeholder for song audio')
            
            # 创建歌曲记录
            song = Song.objects.create(
                song_name=song_info['song_name'],
                song_duration=song_info['song_duration'],
                song_price=song_info['song_price'],
                song_singer=singer,
                is_active=True  # 直接激活，无需审核
            )
            
            # 设置文件路径（在实际应用中，这些会通过文件上传设置）
            song.song_cover = song_info['song_cover_path']
            song.song_file = song_info['song_file_path']
            song.save()
            
            print(f"创建歌曲 {song_info['song_name']} 成功，歌手：{singer.user_name}")
            
            # 创建审核记录并直接审核通过
            check_log = CheckSongLog.objects.create(
                check_song=song,
                check_song_name=song.song_name,
                check_song_cover=str(song.song_cover) if song.song_cover else '',
                check_song_file=str(song.song_file),
                check_song_duration=song.song_duration,
                check_song_price=song.song_price,
                check_status=1  # 直接审核通过
            )

def main():
    """主函数"""
    print("开始初始化歌曲数据...")
    
    # 首先创建歌手
    singers = create_test_singers()
    
    # 然后创建歌曲
    create_test_songs(singers)
    
    print("\n歌曲数据初始化完成！")
    print("\n可使用以下账户登录：")
    print("歌手账户:")
    for singer_info in singer_data:
        print(f"  用户名: {singer_info['user_name']}, 密码: {singer_info['password']}")
    print("\n已初始化5首歌曲，可以通过前端界面查看")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"初始化过程中发生错误: {e}")
        sys.exit(1)