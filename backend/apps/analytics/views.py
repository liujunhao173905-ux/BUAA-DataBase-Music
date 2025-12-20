"""
统计分析视图
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Q
from django.db.models.functions import ExtractHour
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
import io
import os

# 导入导出相关库
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

try:
    import docx
    from docx.shared import Pt, Inches
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

from apps.users.models import LoginLog, User
from apps.music.models import Song, StarSong, BuySong, PlayHistory
from apps.playlists.models import Playlist, StarPlaylist


def get_user_report_data(user):
    """获取用户听歌报告数据的辅助函数"""
    # 1. 总体统计
    play_history = PlayHistory.objects.filter(user=user)
    total_plays = play_history.count()
    
    # 总听歌时长（秒）
    total_duration_seconds = play_history.aggregate(
        total=Sum('play_duration')
    )['total'] or 0
    
    # 转换时长显示格式
    hours = total_duration_seconds // 3600
    minutes = (total_duration_seconds % 3600) // 60
    total_duration_display = f"{hours}小时{minutes}分"
    
    # 2. 最常听的歌曲 (Top 10)
    top_songs = play_history.values(
        'song__song_id', 'song__song_name', 'song__song_singer__user_name'
    ).annotate(
        play_count=Count('history_id')
    ).order_by('-play_count')[:10]
    
    # 3. 最常听的歌手 (Top 5)
    top_singers = play_history.values(
        'song__song_singer__user_name'
    ).annotate(
        play_count=Count('history_id')
    ).order_by('-play_count')[:5]
    
    # 4. 听歌时间段分布
    # 使用 ExtractHour 提取小时 (数据库无关)
    hour_distribution = play_history.annotate(
        hour=ExtractHour('play_time')
    ).values('hour').annotate(
        count=Count('history_id')
    ).order_by('hour')
    
    # 补全0-23点的数据
    hour_stats = {str(i).zfill(2): 0 for i in range(24)}
    for item in hour_distribution:
        h = item.get('hour')
        if h is not None:
            # ExtractHour 返回整数，转换为填充零的字符串
            key = str(h).zfill(2)
            if key in hour_stats:
                hour_stats[key] = item['count']
    
    hour_chart_data = [
        {'hour': h, 'count': c} 
        for h, c in hour_stats.items()
    ]
    
    return {
        'user_name': user.user_name,
        'report_date': timezone.now().date(),
        'total_plays': total_plays,
        'total_duration_display': total_duration_display,
        'top_songs': list(top_songs),
        'top_singers': list(top_singers),
        'hour_distribution': hour_chart_data
    }


class UserReportView(APIView):
    """用户听歌报告视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取用户听歌报告数据"""
        data = get_user_report_data(request.user)
        return Response(data)


class ExportReportView(APIView):
    """导出用户听歌报告视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """导出报告"""
        # 使用 export_type 代替 format，避免与 DRF 的内容协商冲突
        export_type = request.query_params.get('export_type', 'excel')
        # 兼容旧的 format 参数（如果 DRF 没有拦截的话）
        if not export_type or export_type == 'excel':
            format_param = request.query_params.get('format')
            if format_param:
                export_type = format_param

        data = get_user_report_data(request.user)
        filename = f"music_report_{request.user.user_name}_{timezone.now().strftime('%Y%m%d')}"
        
        if export_type == 'pdf':
            if not HAS_REPORTLAB:
                return Response({'error': '服务器未安装PDF生成库'}, status=status.HTTP_501_NOT_IMPLEMENTED)
            return self._generate_pdf(data, filename)
        elif export_type == 'word':
            if not HAS_DOCX:
                return Response({'error': '服务器未安装Word生成库'}, status=status.HTTP_501_NOT_IMPLEMENTED)
            return self._generate_word(data, filename)
        else: # excel
            if not HAS_OPENPYXL:
                return Response({'error': '服务器未安装Excel生成库'}, status=status.HTTP_501_NOT_IMPLEMENTED)
            return self._generate_excel(data, filename)

    def _generate_pdf(self, data, filename):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # 注册中文字体 (尝试使用Windows自带字体)
        font_name = 'Helvetica'
        try:
            # 尝试常见的中文字体路径
            font_paths = [
                'C:\\Windows\\Fonts\\simhei.ttf', # 黑体
                'C:\\Windows\\Fonts\\msyh.ttf',   # 微软雅黑
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf' # Linux常见
            ]
            for path in font_paths:
                if os.path.exists(path):
                    pdfmetrics.registerFont(TTFont('ChineseFont', path))
                    font_name = 'ChineseFont'
                    break
        except Exception:
            pass

        # 标题
        p.setFont(font_name, 24)
        p.drawString(100, height - 100, f"{data['user_name']} 的听歌报告")
        
        p.setFont(font_name, 12)
        y = height - 150
        
        # 基础数据
        p.drawString(100, y, f"报告日期: {data['report_date']}")
        y -= 20
        p.drawString(100, y, f"累计听歌: {data['total_plays']} 首")
        y -= 20
        p.drawString(100, y, f"听歌总时长: {data['total_duration_display']}")
        y -= 40
        
        # Top 歌曲
        p.setFont(font_name, 16)
        p.drawString(100, y, "最常听的歌曲 Top 10")
        y -= 25
        p.setFont(font_name, 12)
        for idx, song in enumerate(data['top_songs'], 1):
            text = f"{idx}. {song['song__song_name']} - {song['song__song_singer__user_name']} ({song['play_count']}次)"
            p.drawString(120, y, text)
            y -= 20
            if y < 50:
                p.showPage()
                p.setFont(font_name, 12)
                y = height - 50
        
        y -= 20
        # Top 歌手
        p.setFont(font_name, 16)
        p.drawString(100, y, "最常听的歌手 Top 5")
        y -= 25
        p.setFont(font_name, 12)
        for idx, singer in enumerate(data['top_singers'], 1):
            text = f"{idx}. {singer['song__song_singer__user_name']} ({singer['play_count']}次)"
            p.drawString(120, y, text)
            y -= 20
            if y < 50:
                p.showPage()
                p.setFont(font_name, 12)
                y = height - 50

        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
        return response

    def _generate_word(self, data, filename):
        doc = docx.Document()
        doc.add_heading(f"{data['user_name']} 的听歌报告", 0)
        
        doc.add_paragraph(f"报告日期: {data['report_date']}")
        doc.add_paragraph(f"累计听歌: {data['total_plays']} 首")
        doc.add_paragraph(f"听歌总时长: {data['total_duration_display']}")
        
        doc.add_heading('最常听的歌曲 Top 10', level=1)
        for idx, song in enumerate(data['top_songs'], 1):
            doc.add_paragraph(
                f"{idx}. {song['song__song_name']} - {song['song__song_singer__user_name']} ({song['play_count']}次)",
                style='List Number'
            )
            
        doc.add_heading('最常听的歌手 Top 5', level=1)
        for idx, singer in enumerate(data['top_singers'], 1):
            doc.add_paragraph(
                f"{idx}. {singer['song__song_singer__user_name']} ({singer['play_count']}次)",
                style='List Number'
            )
            
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        response = HttpResponse(
            buffer, 
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.docx"'
        return response

    def _generate_excel(self, data, filename):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "听歌报告"
        
        ws['A1'] = f"{data['user_name']} 的听歌报告"
        ws['A2'] = f"报告日期: {data['report_date']}"
        ws['A3'] = f"累计听歌: {data['total_plays']} 首"
        ws['A4'] = f"听歌总时长: {data['total_duration_display']}"
        
        ws['A6'] = "最常听的歌曲 Top 10"
        ws.append(['排名', '歌曲名', '歌手', '播放次数'])
        for idx, song in enumerate(data['top_songs'], 1):
            ws.append([
                idx, 
                song['song__song_name'], 
                song['song__song_singer__user_name'], 
                song['play_count']
            ])
            
        ws.append([])
        ws.append(['最常听的歌手 Top 5'])
        ws.append(['排名', '歌手名', '播放次数'])
        for idx, singer in enumerate(data['top_singers'], 1):
            ws.append([
                idx, 
                singer['song__song_singer__user_name'], 
                singer['play_count']
            ])
            
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        response = HttpResponse(
            buffer, 
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        return response



class LoginStatisticsView(APIView):
    """登录统计视图（管理员端）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取登录统计"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以查看登录统计'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 时间范围参数
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # 按用户类型统计
        logs = LoginLog.objects.filter(log_time__gte=start_date)
        stats_by_type = logs.values('log_user_type').annotate(
            count=Count('log_id')
        ).order_by('log_user_type')
        
        # 按日期统计
        stats_by_date = logs.extra(
            select={'date': "DATE(log_time)"}
        ).values('date').annotate(
            count=Count('log_id')
        ).order_by('date')
        
        # 总登录次数
        total_logins = logs.count()
        
        # 活跃用户数（最近N天有登录的用户）
        active_users = User.objects.filter(
            login_logs__log_time__gte=start_date
        ).distinct().count()
        
        return Response({
            'period_days': days,
            'total_logins': total_logins,
            'active_users': active_users,
            'stats_by_type': list(stats_by_type),
            'stats_by_date': list(stats_by_date),
        })


class UserStatisticsView(APIView):
    """用户统计视图（管理员端）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取用户统计"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以查看用户统计'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 按用户类型统计
        stats_by_type = User.objects.values('user_type').annotate(
            count=Count('user_id')
        ).order_by('user_type')
        
        # 总用户数
        total_users = User.objects.count()
        
        # 最近注册的用户数（最近30天）
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        recent_users = User.objects.filter(date_joined__gte=start_date).count()
        
        return Response({
            'total_users': total_users,
            'recent_users': recent_users,
            'stats_by_type': list(stats_by_type),
        })


class MusicStatisticsView(APIView):
    """音乐统计视图（管理员端）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取音乐统计"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以查看音乐统计'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 总歌曲数
        total_songs = Song.objects.count()
        
        # 已上架歌曲数
        active_songs = Song.objects.filter(is_active=True).count()
        
        # 总收藏数
        total_stars = StarSong.objects.count()
        
        # 总购买数
        total_buys = BuySong.objects.count()
        
        # 总销售额
        total_revenue = BuySong.objects.aggregate(
            total=Sum('buy_price')
        )['total'] or 0
        
        # 按歌手统计
        stats_by_singer = Song.objects.values(
            'song_singer__user_name'
        ).annotate(
            song_count=Count('song_id'),
            star_count=Count('starred_by'),
            buy_count=Count('bought_by')
        ).order_by('-song_count')[:10]
        
        return Response({
            'total_songs': total_songs,
            'active_songs': active_songs,
            'total_stars': total_stars,
            'total_buys': total_buys,
            'total_revenue': float(total_revenue),
            'stats_by_singer': list(stats_by_singer),
        })


class PlaylistStatisticsView(APIView):
    """歌单统计视图（管理员端）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取歌单统计"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以查看歌单统计'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 总歌单数
        total_playlists = Playlist.objects.count()
        
        # 公开歌单数
        active_playlists = Playlist.objects.filter(is_active=True).count()
        
        # 总收藏数
        total_stars = StarPlaylist.objects.count()
        
        # 按创建者统计
        stats_by_creator = Playlist.objects.values(
            'playlist_creator__user_name'
        ).annotate(
            playlist_count=Count('playlist_id'),
            star_count=Count('starred_by')
        ).order_by('-playlist_count')[:10]
        
        return Response({
            'total_playlists': total_playlists,
            'active_playlists': active_playlists,
            'total_stars': total_stars,
            'stats_by_creator': list(stats_by_creator),
        })

