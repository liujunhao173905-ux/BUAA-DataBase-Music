"""
统计分析视图
"""
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum
from django.db.models.functions import ExtractHour
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
import pytz
import io
import os

# ---------------------- 导入导出库检查 ----------------------
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

try:
    import docx
    from docx.shared import Pt, RGBColor, Inches, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn  # 关键：用于设置中文字体
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

from apps.users.models import LoginLog, User
from apps.music.models import Song, StarSong, BuySong, PlayHistory
from apps.playlists.models import Playlist, StarPlaylist


# ==============================================================================
# 统一字体配置接口 (核心修改)
# ==============================================================================

def get_best_font_config():
    """
    统一返回最优字体配置
    优先级：微软雅黑 (msyh.ttf) -> 黑体 (simhei.ttf) -> 系统后备
    返回: {'path': 字体文件路径, 'name': 字体在软件中显示的名称}
    """
    # 候选列表：(文件路径, Word/Excel中对应的字体名)
    candidates = [
        # Windows 微软雅黑 (首选)
        (r'C:\Windows\Fonts\msyh.ttc', 'Microsoft YaHei'),
        (r'C:\Windows\Fonts\msyhbd.ttc', 'Microsoft YaHei'), # 粗体备选
        (r'C:\Windows\Fonts\msyh.ttf', 'Microsoft YaHei'),
        (r'C:\Windows\Fonts\msyhbd.ttf', 'Microsoft YaHei'), # 粗体备选
        # Windows 黑体 (次选)
        (r'C:\Windows\Fonts\simhei.ttf', 'SimHei'),
        # Mac / Linux 备选
        ('/System/Library/Fonts/STHeiti Light.ttc', 'STHeiti'),
        ('/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf', 'Droid Sans Fallback'),
        # 项目内嵌字体 (如果有)
        ('./static/fonts/msyh.ttf', 'Microsoft YaHei')
    ]

    for path, name in candidates:
        if os.path.exists(path):
            return {'path': path, 'name': name}
    
    # 默认兜底
    return {'path': None, 'name': 'Arial'}


# ==============================================================================
# 数据获取逻辑
# ==============================================================================

def get_user_report_data(user, use_30h_clock=False):
    """
    获取用户听歌报告数据
    :param user: 用户对象
    :param use_30h_clock: 是否使用30小时制
    """
    # 1. 总体统计
    play_history = PlayHistory.objects.filter(user=user)
    total_plays = play_history.count()
    
    total_duration_seconds = play_history.aggregate(total=Sum('play_duration'))['total'] or 0
    hours = total_duration_seconds // 3600
    minutes = (total_duration_seconds % 3600) // 60
    total_duration_display = f"{hours}小时{minutes}分"
    
    # 2. Top 10 歌曲
    top_songs = play_history.values(
        'song__song_id', 'song__song_name', 'song__song_singer__user_name'
    ).annotate(play_count=Count('history_id')).order_by('-play_count')[:10]
    
    # 3. Top 5 歌手
    top_singers = play_history.values(
        'song__song_singer__user_name'
    ).annotate(play_count=Count('history_id')).order_by('-play_count')[:5]
    
    # 4. 听歌时间段分布
    hour_distribution = play_history.annotate(
        hour=ExtractHour('play_time')
    ).values('hour').annotate(
        count=Count('history_id')
    ).order_by('hour')
    
    raw_stats = {i: 0 for i in range(24)}
    for item in hour_distribution:
        h = item.get('hour')
        if h is not None:
            raw_stats[h] = item['count']
    
    final_chart_data = []
    
    # --- 辅助函数：处理坐标轴显示 (去除前导零) ---
    def format_hour_label(h):
        return str(h) # 直接转字符串，不使用 zfill(2)，满足 0-9 显示一位的要求
    
    if use_30h_clock:
        # 30小时制：6...23, 0...5 (显示为 24...29)
        hours_order = list(range(6, 24)) + list(range(0, 6))
        for h in hours_order:
            display_h = h if h >= 6 else h + 24
            final_chart_data.append({
                'hour': str(display_h), # 30小时制数字较大，直接转字符串即可
                'count': raw_stats[h]
            })
    else:
        # 24小时制：0...23
        for h in range(24):
            final_chart_data.append({
                'hour': format_hour_label(h), # 这里会生成 '0', '1', ... '10'
                'count': raw_stats[h]
            })

    # --- 修正日期为东八区 ---
    tz = pytz.timezone('Asia/Shanghai')
    # 将 UTC 时间转换为上海时间
    local_now = timezone.now().astimezone(tz)
    
    return {
        'user_name': user.user_name,
        'report_date': local_now.date(), # 使用转换后的日期
        'total_plays': total_plays,
        'total_duration_display': total_duration_display,
        'top_songs': list(top_songs),
        'top_singers': list(top_singers),
        'hour_distribution': final_chart_data,
        'is_30h': use_30h_clock
    }


# ==============================================================================
# 视图类
# ==============================================================================

class UserReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        use_30h = request.query_params.get('time_system') == '30h'
        data = get_user_report_data(request.user, use_30h_clock=use_30h)
        return Response(data)


class ExportReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        export_type = request.query_params.get('export_type', 'excel')
        if not export_type or export_type == 'excel':
            format_param = request.query_params.get('format')
            if format_param: export_type = format_param
        
        use_30h = request.query_params.get('time_system') == '30h'
        data = get_user_report_data(request.user, use_30h_clock=use_30h)
        
        date_str = timezone.now().strftime('%Y%m%d')
        mode_str = "30h" if use_30h else "24h"
        filename = f"Report_{request.user.user_name}_{date_str}_{mode_str}"
        
        # 获取全局统一字体配置
        font_config = get_best_font_config()
        
        if export_type == 'pdf':
            if not HAS_REPORTLAB: return Response({'error': '缺少依赖: reportlab'}, status=501)
            return self._generate_pdf(data, filename, font_config)
        elif export_type == 'word':
            if not HAS_DOCX: return Response({'error': '缺少依赖: python-docx'}, status=501)
            return self._generate_word(data, filename, font_config)
        else:
            if not HAS_OPENPYXL: return Response({'error': '缺少依赖: openpyxl'}, status=501)
            return self._generate_excel(data, filename, font_config)

    # -------------------------------------------------------------------------
    # PDF 生成 (使用 font_config['path'])
    # -------------------------------------------------------------------------
    def _generate_pdf(self, data, filename, font_config):
        buffer = io.BytesIO()
        
        # 字体注册逻辑
        pdf_font_name = 'CustomFont'
        if font_config['path']:
            try:
                pdfmetrics.registerFont(TTFont(pdf_font_name, font_config['path']))
            except Exception:
                pdf_font_name = 'Helvetica'
        else:
            pdf_font_name = 'Helvetica'

        # 页面设置
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            rightMargin=2*cm, leftMargin=2*cm,
            topMargin=3*cm, bottomMargin=2*cm
        )
        
        # 定义主题色
        THEME_COLOR = colors.HexColor('#409EFF')
        
        # 页眉背景绘制
        def draw_header_bg(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(THEME_COLOR) # 使用天蓝色
            # 顶部色块
            canvas.rect(0, A4[1] - 2.5*cm, A4[0], 2.5*cm, fill=1, stroke=0)
            # 页脚页码
            canvas.setFont(pdf_font_name, 9)
            canvas.setFillColor(colors.grey)
            canvas.drawRightString(A4[0] - 2*cm, 1*cm, f"Page {canvas.getPageNumber()}")
            canvas.restoreState()

        elements = []
        
        # --- 样式定义 ---
        # 主标题
        style_title = ParagraphStyle(
            'Title', fontName=pdf_font_name, 
            fontSize=26, leading=32, 
            textColor=colors.HexColor('#303133'), 
            alignment=TA_CENTER, spaceAfter=10
        )
        
        # 副标题 (删除了时间制式)
        style_subtitle = ParagraphStyle(
            'SubTitle', fontName=pdf_font_name, 
            fontSize=11, leading=14, 
            textColor=colors.grey, 
            alignment=TA_CENTER, spaceAfter=30
        )
        
        # 分段标题 (H2) - 缩小字号，保持黑色
        style_h2 = ParagraphStyle(
            'H2', fontName=pdf_font_name, 
            fontSize=14, leading=18,  # 字号从 16/18 缩小到 14
            textColor=colors.HexColor('#303133'), # 保持深灰色/黑色
            spaceBefore=20, spaceAfter=10,
            borderWidth=0
        )
        
        # 列表表格样式 (用于 Top 10)
        modern_table_style = TableStyle([
            ('FONTNAME', (0,0), (-1,-1), pdf_font_name),
            ('FONTSIZE', (0,0), (-1,0), 11),
            ('FONTSIZE', (0,1), (-1,-1), 10),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('BACKGROUND', (0,0), (-1,0), THEME_COLOR), # 表头天蓝色
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F7FA')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#EBEEF5')),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ])

        # --- 内容构建 ---
        
        # 1. 标题区域
        elements.append(Paragraph(f"{data['user_name']} 的个人听歌报告", style_title))
        # 副标题仅显示日期，去除时间制式
        elements.append(Paragraph(f"统计日期: {data['report_date']}", style_subtitle))
        
        # 2. 概览数据卡片 (样式修正)
        summary_data = [
            ['累计听歌', '累计时长'],
            [f"{data['total_plays']} 首", data['total_duration_display']]
        ]
        t_summary = Table(summary_data, colWidths=[8*cm, 8*cm])
        t_summary.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), pdf_font_name),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            
            # 第一行 (表头): 黑色，放大，加一点下边距
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#303133')), # 黑色
            ('FONTSIZE', (0,0), (-1,0), 13), # 放大
            ('BOTTOMPADDING', (0,0), (-1,0), 10), # 表头和数字拉开一点距离
            
            # 第二行 (数值): 蓝色，缩小，垂直居中
            ('TEXTCOLOR', (0,1), (-1,1), THEME_COLOR), # 天蓝色
            ('FONTSIZE', (0,1), (-1,1), 16), # 缩小 (原18)
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), # 垂直居中
            
            # 增加边框内边距，解决“碰到底部”的问题
            ('TOPPADDING', (0,0), (-1,-1), 15), 
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            
            # 边框样式
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#DCDFE6')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#EBEEF5'))
        ]))
        elements.append(t_summary)
        
        # 3. 听歌时段分布图表
        elements.append(Paragraph("▎听歌时段分布", style_h2))
        
        chart_vals = [d['count'] for d in data['hour_distribution']]
        chart_cats = [d['hour'] for d in data['hour_distribution']] # 这里已经是处理过 0-9 的字符串了
        
        if chart_vals:
            # 调整图表容器大小
            drawing = Drawing(450, 160)
            bc = VerticalBarChart()
            bc.x = 20
            bc.y = 20
            bc.height = 120
            bc.width = 410
            bc.data = [chart_vals]
            
            # 图表样式优化
            bc.strokeColor = None # 去掉柱子边框，更扁平
            bc.bars[0].fillColor = THEME_COLOR # 柱子使用天蓝色
            
            # Y轴设置
            bc.valueAxis.valueMin = 0
            max_val = max(chart_vals) if chart_vals else 10
            bc.valueAxis.valueMax = max_val + (1 if max_val < 5 else max_val * 0.1) # 留出顶部空间
            bc.valueAxis.visibleGrid = 1
            bc.valueAxis.gridStrokeColor = colors.HexColor('#EBEEF5')
            bc.valueAxis.labels.fontName = pdf_font_name
            bc.valueAxis.labels.fontSize = 8
            
            # X轴设置
            bc.categoryAxis.labels.boxAnchor = 'n' # 文字锚点在上方
            bc.categoryAxis.labels.dy = -5 # 向下偏移
            bc.categoryAxis.labels.fontName = pdf_font_name
            bc.categoryAxis.labels.fontSize = 8
            bc.categoryAxis.categoryNames = chart_cats
            
            drawing.add(bc)
            elements.append(drawing)
        else:
            elements.append(Paragraph("暂无数据", style_subtitle))
            
        elements.append(Spacer(1, 10))

        # 4. Top 10 歌曲
        elements.append(Paragraph("▎最常听的歌曲 Top 10", style_h2))
        if data['top_songs']:
            table_data = [['排名', '歌曲', '歌手', '次数']]
            for i, s in enumerate(data['top_songs'], 1):
                table_data.append([str(i), s['song__song_name'], s['song__song_singer__user_name'], str(s['play_count'])])
            
            t_songs = Table(table_data, colWidths=[1.5*cm, 7.5*cm, 5*cm, 2*cm])
            t_songs.setStyle(modern_table_style)
            elements.append(t_songs)
        else:
            elements.append(Paragraph("暂无数据", style_subtitle))

        # 5. Top 5 歌手
        elements.append(Paragraph("▎最常听的歌手 Top 5", style_h2))
        if data['top_singers']:
            table_data = [['排名', '歌手', '次数']]
            for i, s in enumerate(data['top_singers'], 1):
                table_data.append([str(i), s['song__song_singer__user_name'], str(s['play_count'])])
            
            t_singers = Table(table_data, colWidths=[2*cm, 10*cm, 4*cm])
            t_singers.setStyle(modern_table_style)
            elements.append(t_singers)

        doc.build(elements, onFirstPage=draw_header_bg, onLaterPages=draw_header_bg)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
        return response

    # -------------------------------------------------------------------------
    # Word 生成 (使用 font_config['name'] + eastAsia 配置)
    # -------------------------------------------------------------------------
    def _generate_word(self, data, filename, font_config):
        # 必须导入 Cm 用于设置列宽

        doc = docx.Document()
        target_font_name = font_config['name']
        
        # --- 辅助函数：设置单元格文本、字体、对齐和宽度 ---
        def set_cell_text(cell, text, is_bold=False, width=None):
            # 1. 设置内容和字体
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 核心：强制水平居中
            run = p.add_run(str(text))
            run.font.name = target_font_name
            run.font.bold = is_bold
            run.element.rPr.rFonts.set(qn('w:eastAsia'), target_font_name)
            
            # 2. 设置列宽 (如果有指定)
            if width:
                cell.width = width

        # --- 1. 标题区域 ---
        heading = doc.add_heading('', 0)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = heading.add_run(f"{data['user_name']} 的听歌报告")
        run.font.name = target_font_name
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        run.element.rPr.rFonts.set(qn('w:eastAsia'), target_font_name)
        
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # 删除时间制式显示，只保留日期
        run = p.add_run(f"统计日期: {data['report_date']}")
        run.font.name = target_font_name
        run.element.rPr.rFonts.set(qn('w:eastAsia'), target_font_name)

        # --- 2. 概览数据 ---
        table = doc.add_table(rows=2, cols=2)
        table.style = 'Table Grid'
        table.autofit = False # 关闭自动调整，以便让居中生效更稳定
        
        # 设置概览列宽 (平分)
        col_width = Cm(8)
        for row in table.rows:
            row.cells[0].width = col_width
            row.cells[1].width = col_width

        # 填充内容 (全居中)
        set_cell_text(table.cell(0, 0), '累计听歌数量', is_bold=True)
        set_cell_text(table.cell(0, 1), '累计听歌时长', is_bold=True)
        set_cell_text(table.cell(1, 0), f"{data['total_plays']} 首")
        set_cell_text(table.cell(1, 1), data['total_duration_display'])
        
        doc.add_paragraph()

        # --- 定义通用列宽 ---
        # 总宽度约 16cm (A4除去页边距)
        WIDTH_RANK = Cm(1.5)
        WIDTH_INFO = Cm(11.0)
        WIDTH_COUNT = Cm(3.5)

        # --- 3. 最常听的歌曲 Top 10 ---
        h_song = doc.add_heading('', level=1)
        r_song = h_song.add_run('▎最常听的歌曲 Top 10')
        r_song.font.name = target_font_name
        r_song.font.bold = True
        r_song.font.color.rgb = RGBColor(0, 0, 0)
        r_song.element.rPr.rFonts.set(qn('w:eastAsia'), target_font_name)

        if data['top_songs']:
            t_songs = doc.add_table(rows=1, cols=3)
            t_songs.style = 'Table Grid'
            t_songs.autofit = False 

            # 表头
            hdr = t_songs.rows[0].cells
            set_cell_text(hdr[0], '排名', is_bold=True, width=WIDTH_RANK)
            set_cell_text(hdr[1], '歌曲信息', is_bold=True, width=WIDTH_INFO)
            set_cell_text(hdr[2], '播放次数', is_bold=True, width=WIDTH_COUNT)
            
            # 数据
            for idx, s in enumerate(data['top_songs'], 1):
                row = t_songs.add_row().cells
                song_info = f"{s['song__song_name']} - {s['song__song_singer__user_name']}"
                set_cell_text(row[0], str(idx), width=WIDTH_RANK)
                set_cell_text(row[1], song_info, width=WIDTH_INFO)
                set_cell_text(row[2], str(s['play_count']), width=WIDTH_COUNT)
        else:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run("暂无数据")
            run.font.name = target_font_name
            run.element.rPr.rFonts.set(qn('w:eastAsia'), target_font_name)
        
        doc.add_paragraph()

        # --- 4. 最常听的歌手 Top 5 ---
        h_singer = doc.add_heading('', level=1)
        r_singer = h_singer.add_run('▎最常听的歌手 Top 5')
        r_singer.font.name = target_font_name
        r_singer.font.bold = True
        r_singer.font.color.rgb = RGBColor(0, 0, 0)
        r_singer.element.rPr.rFonts.set(qn('w:eastAsia'), target_font_name)

        if data['top_singers']:
            # 改为 3 列 (排名, 歌手, 次数) 以对齐上面的表格
            t_singers = doc.add_table(rows=1, cols=3)
            t_singers.style = 'Table Grid'
            t_singers.autofit = False

            # 表头
            hdr = t_singers.rows[0].cells
            set_cell_text(hdr[0], '排名', is_bold=True, width=WIDTH_RANK)
            set_cell_text(hdr[1], '歌手', is_bold=True, width=WIDTH_INFO) # 增加宽度
            set_cell_text(hdr[2], '次数', is_bold=True, width=WIDTH_COUNT)
            
            # 数据
            for idx, s in enumerate(data['top_singers'], 1):
                row = t_singers.add_row().cells
                set_cell_text(row[0], str(idx), width=WIDTH_RANK)
                set_cell_text(row[1], s['song__song_singer__user_name'], width=WIDTH_INFO)
                set_cell_text(row[2], str(s['play_count']), width=WIDTH_COUNT)
        else:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run("暂无数据")
            run.font.name = target_font_name
            run.element.rPr.rFonts.set(qn('w:eastAsia'), target_font_name)

        doc.add_paragraph()

        # --- 5. 听歌时段分布 (移至最后，纵向分布) ---
        h_dist = doc.add_heading('', level=1)
        r_dist = h_dist.add_run('▎听歌时段分布')
        r_dist.font.name = target_font_name
        r_dist.font.bold = True
        r_dist.font.color.rgb = RGBColor(0, 0, 0)
        r_dist.element.rPr.rFonts.set(qn('w:eastAsia'), target_font_name)

        # 创建 4 列表格 (时段, 次数 | 时段, 次数)
        dist_table = doc.add_table(rows=1, cols=4)
        dist_table.style = 'Table Grid'
        dist_table.autofit = False
        
        # 设置时段表格宽度
        w_time = Cm(3)
        w_count = Cm(3)
        
        hdr = dist_table.rows[0].cells
        for i in range(4):
            hdr[i].width = w_count if i % 2 != 0 else w_time # 简单的宽度分配
            
        set_cell_text(hdr[0], '时段', is_bold=True)
        set_cell_text(hdr[1], '次数', is_bold=True)
        set_cell_text(hdr[2], '时段', is_bold=True)
        set_cell_text(hdr[3], '次数', is_bold=True)

        items = data['hour_distribution']
        total_items = len(items)
        mid_point = (total_items + 1) // 2 # 计算分割点 (例如 24/2 = 12)

        # 纵向分布循环
        # 左侧取 0 ~ mid-1
        # 右侧取 mid ~ total-1
        for i in range(mid_point):
            row = dist_table.add_row().cells
            
            # 左侧数据
            if i < total_items:
                set_cell_text(row[0], f"{items[i]['hour']}:00")
                set_cell_text(row[1], str(items[i]['count']))
            
            # 右侧数据
            right_idx = i + mid_point
            if right_idx < total_items:
                set_cell_text(row[2], f"{items[right_idx]['hour']}:00")
                set_cell_text(row[3], str(items[right_idx]['count']))
            else:
                # 如果没有右侧数据（奇数个总数的情况），填空
                set_cell_text(row[2], "")
                set_cell_text(row[3], "")

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{filename}.docx"'
        return response

    # -------------------------------------------------------------------------
    # Excel 生成 (使用 font_config['name'])
    # -------------------------------------------------------------------------
    def _generate_excel(self, data, filename, font_config):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "听歌报告"
        
        target_name = font_config['name']
        
        # 样式定义
        title_font = Font(name=target_name, size=16, bold=True, color="FFFFFF")
        title_fill = PatternFill(start_color="409EFF", end_color="409EFF", fill_type="solid") # 深灰背景
        
        header_font = Font(name=target_name, size=11, bold=True)
        header_fill = PatternFill(start_color="D9ECFF", end_color="D9ECFF", fill_type="solid")
        
        normal_font = Font(name=target_name, size=10)
        center = Alignment(horizontal='center', vertical='center')
        
        # 应用
        ws.merge_cells('A1:D1')
        ws['A1'] = f"{data['user_name']} 的听歌报告"
        ws['A1'].font = title_font; ws['A1'].fill = title_fill; ws['A1'].alignment = center
        
        ws.merge_cells('A2:D2')
        ws['A2'] = f"日期: {data['report_date']}"
        ws['A2'].font = normal_font; ws['A2'].alignment = center
        
        ws['A3'] = "累计听歌"; ws['A3'].alignment = center; ws['B3'] = f"{data['total_plays']} 首"; ws['B3'].alignment = center
        ws['C3'] = "总时长"; ws['C3'].alignment = center; ws['D3'] = data['total_duration_display']; ws['D3'].alignment = center
        for c in ['A3','B3','C3','D3']: ws[c].font = normal_font

        # Top 10
        row = 6
        ws[f'A{row}'] = "▎最常听的歌曲 Top 10"
        ws[f'A{row}'].font = Font(name=target_name, bold=True, color="000000")
        row += 1
        headers = ['排名', '歌曲名', '歌手', '次数']
        for col, val in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=val)
            cell.font = header_font; cell.fill = header_fill; cell.alignment = center
        row += 1
        for idx, s in enumerate(data['top_songs'], 1):
            cell = ws.cell(row=row, column=1, value=idx); cell.font = normal_font; cell.alignment = center
            cell = ws.cell(row=row, column=2, value=s['song__song_name']); cell.font = normal_font; cell.alignment = center
            cell = ws.cell(row=row, column=3, value=s['song__song_singer__user_name']); cell.font = normal_font; cell.alignment = center
            cell = ws.cell(row=row, column=4, value=s['play_count']); cell.font = normal_font; cell.alignment = center
            row += 1
        
        # Top 5 歌手
        row += 2
        ws[f'A{row}'] = "▎最常听的歌手 Top 5"
        ws[f'A{row}'].font = Font(name=target_name, bold=True, color="000000")
        row += 1
        headers_singer = ['排名', '歌手名', '次数']
        for col, val in enumerate(headers_singer, 1):
            cell = ws.cell(row=row, column=col, value=val)
            cell.font = header_font; cell.fill = header_fill; cell.alignment = center
        row += 1
        for idx, s in enumerate(data['top_singers'], 1):
            cell = ws.cell(row=row, column=1, value=idx); cell.font = normal_font; cell.alignment = center
            cell = ws.cell(row=row, column=2, value=s['song__song_singer__user_name']); cell.font = normal_font; cell.alignment = center
            cell = ws.cell(row=row, column=3, value=s['play_count']); cell.font = normal_font; cell.alignment = center
            row += 1

        # 分布
        row += 2
        ws[f'A{row}'] = "▎听歌时段分布"
        ws[f'A{row}'].font = Font(name=target_name, bold=True, color="000000")
        row += 1
        headers_count = ['时段', '次数']
        for col, val in enumerate(headers_count, 1):
            cell = ws.cell(row=row, column=col, value=val)
            cell.font = header_font; cell.fill = header_fill; cell.alignment = center
        row += 1
        for item in data['hour_distribution']:
            c1 = ws.cell(row=row, column=1, value=f"{item['hour']}:00"); c1.font = normal_font; c1.alignment = center
            c2 = ws.cell(row=row, column=2, value=item['count']); c2.font = normal_font; c2.alignment = center
            row += 1

        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 30
        ws.column_dimensions['C'].width = 20
        ws.column_dimensions['D'].width = 15

        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        return response


# ==============================================================================
# 管理员统计视图 (必须保留)
# ==============================================================================

class LoginStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        if request.user.user_type != 2: return Response({'error': 'Forbid'}, status=403)
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        logs = LoginLog.objects.filter(log_time__gte=start_date)
        stats_by_type = logs.values('log_user_type').annotate(count=Count('log_id')).order_by('log_user_type')
        stats_by_date = logs.extra(select={'date': "DATE(log_time)"}).values('date').annotate(count=Count('log_id')).order_by('date')
        active_users = User.objects.filter(login_logs__log_time__gte=start_date).distinct().count()
        return Response({'period_days': days, 'total_logins': logs.count(), 'active_users': active_users, 'stats_by_type': list(stats_by_type), 'stats_by_date': list(stats_by_date)})

class UserStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        if request.user.user_type != 2: return Response({'error': 'Forbid'}, status=403)
        stats_by_type = User.objects.values('user_type').annotate(count=Count('user_id')).order_by('user_type')
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        recent_users = User.objects.filter(date_joined__gte=start_date).count()
        return Response({'total_users': User.objects.count(), 'recent_users': recent_users, 'stats_by_type': list(stats_by_type)})

class MusicStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        if request.user.user_type != 2: return Response({'error': 'Forbid'}, status=403)
        total_revenue = BuySong.objects.aggregate(total=Sum('buy_price'))['total'] or 0
        stats_by_singer = Song.objects.values('song_singer__user_name').annotate(song_count=Count('song_id'), star_count=Count('starred_by'), buy_count=Count('bought_by')).order_by('-song_count')[:10]
        return Response({'total_songs': Song.objects.count(), 'active_songs': Song.objects.filter(song_status=1).count(), 'total_stars': StarSong.objects.count(), 'total_buys': BuySong.objects.count(), 'total_revenue': float(total_revenue), 'stats_by_singer': list(stats_by_singer)})

class PlaylistStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        if request.user.user_type != 2: return Response({'error': 'Forbid'}, status=403)
        stats_by_creator = Playlist.objects.values('playlist_creator__user_name').annotate(playlist_count=Count('playlist_id'), star_count=Count('starred_by')).order_by('-playlist_count')[:10]
        return Response({'total_playlists': Playlist.objects.count(), 'active_playlists': Playlist.objects.filter(playlist_status=1).count(), 'total_stars': StarPlaylist.objects.count(), 'stats_by_creator': list(stats_by_creator)})