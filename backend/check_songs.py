import os
import django

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.music.models import Song

# 打印所有歌曲信息
print("数据库中的歌曲列表:")
for song in Song.objects.all():
    print(f"ID: {song.song_id}")
    print(f"名称: {song.song_name}")
    print(f"歌手: {song.song_singer.user_name if song.song_singer else '未知'}")
    print(f"价格: {song.song_price}")
    print("-" * 30)

# 测试搜索功能
print("\n测试搜索功能:")
from django.db.models import Q
search_term = "夏"
search_results = Song.objects.filter(
    Q(song_name__icontains=search_term) |
    Q(song_singer__user_name__icontains=search_term)
)
print(f"搜索'{search_term}'结果数量: {search_results.count()}")
for song in search_results:
    print(f"  - {song.song_id}: {song.song_name} by {song.song_singer.user_name}")
