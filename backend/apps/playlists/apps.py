from django.apps import AppConfig


class PlaylistsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.playlists'
    verbose_name = '歌单管理'
    
    def ready(self):
        # 导入信号处理器
        import apps.playlists.signals

