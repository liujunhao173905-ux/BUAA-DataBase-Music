"""
用户视图
实现用户注册、登录、资料管理等功能
"""
from rest_framework import status, permissions, parsers, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Follow, LoginLog
from .serializers import (
    UserSerializer, 
    UserRegisterSerializer, 
    UserProfileSerializer,
    FollowSerializer,
    LoginLogSerializer
)


class RegisterView(APIView):
    """用户注册视图"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """用户注册"""
        # 复制请求数据，避免直接修改原始数据
        request_data = request.data.copy()
        desired_user_type = request_data.get('user_type', 0)
        
        # 如果用户注册的是歌手类型，先将其注册为普通用户，等待审核通过后再改为歌手
        if desired_user_type == 1:
            request_data['user_type'] = 0  # 先注册为普通用户
        
        serializer = UserRegisterSerializer(data=request_data)
        if serializer.is_valid():
            user = serializer.save()
            
            # 如果用户期望注册为歌手类型，创建审核记录
            if desired_user_type == 1:
                from apps.audit.models import CheckUserLog
                CheckUserLog.objects.create(
                    check_user=user,
                    check_user_name=user.user_name,
                    check_user_mobile=user.user_mobile or '',
                    check_user_avatar=str(user.user_avatar) if user.user_avatar else '',
                    check_user_type=1,  # 记录期望的用户类型
                    check_status=0  # 待审核
                )
            # 记录登录日志
            LoginLog.objects.create(
                log_user=user,
                log_user_name=user.user_name,
                log_user_type=user.user_type
            )
            # 生成JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': '注册成功',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """用户登录视图"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """用户登录"""
        user_name = request.data.get('user_name')
        password = request.data.get('password')
        
        if not user_name or not password:
            return Response(
                {'error': '用户名和密码不能为空'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 使用自定义用户模型认证
        try:
            user = User.objects.get(user_name=user_name)
            if user.check_password(password):
                if not user.is_active:
                    return Response(
                        {'error': '账户已被禁用'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                # 记录登录日志
                LoginLog.objects.create(
                    log_user=user,
                    log_user_name=user.user_name,
                    log_user_type=user.user_type
                )
                # 更新最后登录时间
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                # 生成JWT token
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': '登录成功',
                    'user': UserProfileSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': '用户名或密码错误'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return Response(
                {'error': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserProfileView(APIView):
    """用户资料视图"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]
    
    def get(self, request):
        """获取当前用户资料"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """更新当前用户资料"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '更新成功',
                'user': UserProfileSerializer(request.user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """用户详情视图（查看其他用户）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        """获取指定用户资料"""
        try:
            user = User.objects.get(user_id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class SingerListView(APIView):
    """歌手列表视图"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """获取歌手列表，支持搜索和分页"""
        from django.db.models import Q
        from django.core.paginator import Paginator
        
        # 获取搜索参数
        search = request.query_params.get('search', '')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        # 构建查询集
        queryset = User.objects.filter(user_type=1)
        
        # 搜索功能
        if search:
            queryset = queryset.filter(
                Q(user_name__icontains=search)
            )
        
        # 分页
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        # 序列化数据
        serializer = UserProfileSerializer(page_obj, many=True)
        
        # 返回结果
        return Response({
            'count': paginator.count,
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'results': serializer.data
        })


class FollowView(APIView):
    """关注/取消关注视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        """关注用户"""
        try:
            following = User.objects.get(user_id=user_id)
            if following == request.user:
                return Response(
                    {'error': '不能关注自己'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            follow, created = Follow.objects.get_or_create(
                follower=request.user,
                following=following
            )
            
            if created:
                return Response({
                    'message': '关注成功',
                    'follow': FollowSerializer(follow).data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': '已经关注过该用户'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, user_id):
        """取消关注"""
        try:
            following = User.objects.get(user_id=user_id)
            follow = Follow.objects.filter(
                follower=request.user,
                following=following
            ).first()
            
            if follow:
                follow.delete()
                return Response(
                    {'message': '取消关注成功'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': '未关注该用户'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, user_id):
        """检查是否已关注用户"""
        try:
            following = User.objects.get(user_id=user_id)
            is_following = Follow.objects.filter(
                follower=request.user,
                following=following
            ).exists()
            return Response({'is_following': is_following}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class FollowersListView(APIView):
    """粉丝列表视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        """获取用户的粉丝列表"""
        try:
            user = User.objects.get(user_id=user_id)
            followers = Follow.objects.filter(following=user)
            serializer = FollowSerializer(followers, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class FollowingListView(APIView):
    """关注列表视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        """获取用户的关注列表"""
        try:
            user = User.objects.get(user_id=user_id)
            following = Follow.objects.filter(follower=user)
            serializer = FollowSerializer(following, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class MyFollowingListView(APIView):
    """获取当前用户的关注列表"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取当前用户的关注列表"""
        try:
            # 获取当前用户
            user = request.user
            # 获取当前用户关注的所有用户
            following = Follow.objects.filter(follower=user).select_related('following')
            
            # 分页处理
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(following, request)
            
            # 提取关注的用户信息
            following_users = [item.following for item in result_page]
            serializer = UserProfileSerializer(following_users, many=True)
            
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    登录日志视图集
    """
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        根据用户类型过滤
        管理员可以看到所有日志
        普通用户只能看自己的（虽然一般不需要）
        """
        user = self.request.user
        if user.user_type == 2:  # 管理员
            return LoginLog.objects.all().order_by('-log_time')
        return LoginLog.objects.filter(log_user=user).order_by('-log_time')
