#!/usr/bin/env python
"""
歌单应用信号处理器
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Playlist
from apps.audit.models import CheckPlaylistLog


@receiver(post_save, sender=Playlist)
def create_playlist_check_log(sender, instance, created, **kwargs):
    """创建歌单时自动生成审核日志"""
    if created and not instance.is_active:
        # 新创建且未激活的歌单需要审核
        CheckPlaylistLog.objects.create(
            check_playlist=instance,
            check_playlist_name=instance.playlist_name,
            check_playlist_cover=str(instance.playlist_cover) if instance.playlist_cover else '',
            check_playlist_intro=instance.playlist_intro
        )
