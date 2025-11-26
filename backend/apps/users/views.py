"""
用户视图
实现用户注册、登录、资料管理等功能
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Follow, LoginLog
from .serializers import (
    UserSerializer, 
    UserRegisterSerializer, 
    UserProfileSerializer,
    FollowSerializer
)


class RegisterView(APIView):
    """用户注册视图"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """用户注册"""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 如果是歌手类型，需要审核
            if user.user_type == 1:
                from apps.audit.models import CheckUserLog
                CheckUserLog.objects.create(
                    check_user=user,
                    check_user_name=user.user_name,
                    check_user_mobile=user.user_mobile or '',
                    check_user_avatar=str(user.user_avatar) if user.user_avatar else '',
                    check_user_type=user.user_type,
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
                return Response({'message': '取消关注成功'}, status=status.HTTP_200_OK)
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

