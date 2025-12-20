"""
主URL配置
基于系统设计报告的路由设计
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/music/', include('apps.music.urls')),
    path('api/playlists/', include('apps.playlists.urls')),
    path('api/audit/', include('apps.audit.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

# 开发环境下的媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

