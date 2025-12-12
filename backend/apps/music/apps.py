from django.apps import AppConfig


class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.music'
    verbose_name = '音乐管理'
    
    def ready(self):
        # 导入信号处理器
        import apps.music.signals

