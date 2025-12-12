#!/usr/bin/env python
"""
重置测试用户密码的脚本
"""

import os
import sys

# 添加Django项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# 导入User模型
from apps.users.models import User

def reset_test_user_password():
    """重置测试用户密码"""
    try:
        # 找到测试用户
        test_singer = User.objects.get(user_name='test_singer')
        print(f"找到测试用户: {test_singer.user_name}, 用户ID: {test_singer.user_id}")
        
        # 重置密码
        new_password = '123456'
        test_singer.set_password(new_password)
        test_singer.save()
        
        print(f"密码已重置为: {new_password}")
        print(f"密码重置成功！")
        
        # 验证密码是否正确
        print(f"密码验证: {test_singer.check_password(new_password)}")
        
    except User.DoesNotExist:
        print("测试用户不存在")
    except Exception as e:
        print(f"密码重置失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reset_test_user_password()
