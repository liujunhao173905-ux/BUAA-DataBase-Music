import os
import django
import time
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.music.models import Song
from apps.playlists.models import Playlist, PlaylistSong

def verify_trigger():
    print(">>> 开始验证数据库触发器...")
    
    # 1. 创建测试数据
    user = User.objects.create_user(user_name='trigger_test_user', password='password')
    song = Song.objects.create(song_name='Test Song', song_singer=user, song_file='test.mp3')
    playlist = Playlist.objects.create(playlist_name='Test Playlist', playlist_creator=user)
    
    print(f"Initial Playlist Time: {playlist.playlist_updatetime}")
    initial_time = playlist.playlist_updatetime
    
    # 确保时间流逝，以便 update_time 变化明显
    time.sleep(2)
    
    # 2. 触发触发器：向歌单添加歌曲
    print(">>> 向歌单添加歌曲...")
    PlaylistSong.objects.create(playlist=playlist, song=song)
    
    # 3. 重新获取歌单并检查时间
    playlist.refresh_from_db()
    new_time = playlist.playlist_updatetime
    print(f"Updated Playlist Time: {new_time}")
    
    if new_time > initial_time:
        print("✅ 验证成功：触发器正常工作，歌单更新时间已自动刷新！")
    else:
        print("❌ 验证失败：歌单更新时间未变化。")
        
    # 清理数据
    user.delete()
    print(">>> 测试数据已清理")

if __name__ == '__main__':
    try:
        verify_trigger()
    except Exception as e:
        print(f"❌ 发生错误: {e}")
