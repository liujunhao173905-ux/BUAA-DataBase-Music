"""
自定义分页类
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CustomPageNumberPagination(PageNumberPagination):
    """自定义分页类：当页码超出范围时返回空结果集而不是404错误"""
    page_size = 15  # 默认每页15条数据
    page_size_query_param = 'page_size'  # 允许客户端通过query参数指定每页数量
    max_page_size = 100  # 客户端最大可请求每页100条数据
    page_query_param = 'page'  # 页码参数名

    def paginate_queryset(self, queryset, request, view=None):
        """重写分页查询方法，处理页码超出范围的情况"""
        # 获取请求的页码和每页数量
        page_size = self.get_page_size(request)
        page_number = request.query_params.get(self.page_query_param, 1)
        
        # 确保页码是整数
        if page_number in ['last', 'last_page']:
            page_number = 'last'
        else:
            try:
                page_number = int(page_number)
            except (TypeError, ValueError):
                page_number = 1
        
        # 使用Django的Paginator
        self.paginator = Paginator(queryset, page_size)
        
        try:
            # 尝试获取指定页
            self.page = self.paginator.page(page_number)
        except EmptyPage:
            # 当页码超出范围时，设置self.page为None
            self.page = None
            return []
        except PageNotAnInteger:
            # 当页码不是整数时，返回第一页
            self.page = self.paginator.page(1)
        
        # 设置分页上下文
        if self.paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True
            
        self.request = request
        return list(self.page) if self.page else []
    
    def get_paginated_response(self, data):
        """重写分页响应方法，确保当页码超出范围时返回正确的空结果集"""
        if self.page is None:
            # 当页码超出范围时，返回空结果集但保留正确的总数
            return Response({
                'count': self.paginator.count,
                'next': None,
                'previous': self.paginator.num_pages if self.paginator.num_pages > 0 else None,
                'results': []
            })
        return super().get_paginated_response(data)
