#!/usr/bin/env python
"""
音乐应用信号处理器
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Song
from apps.audit.models import CheckSongLog


@receiver(post_save, sender=Song)
def create_song_check_log(sender, instance, created, **kwargs):
    """创建歌曲时自动生成审核日志"""
    if created and instance.song_status == 0:
        # 新创建且未激活的歌曲需要审核
        CheckSongLog.objects.create(
            check_song=instance,
            check_song_name=instance.song_name,
            check_song_cover=str(instance.song_cover) if instance.song_cover else '',
            check_song_file=str(instance.song_file),
            check_song_duration=instance.song_duration,
            check_song_price=instance.song_price
        )
