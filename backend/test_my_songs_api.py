#!/usr/bin/env python
"""
测试'my_songs'接口的脚本
"""

import requests
import json

def test_my_songs_api():
    """测试'my_songs'接口"""
    # 后端API基础URL
    base_url = 'http://127.0.0.1:8000/api'
    
    # 登录信息
    login_data = {
        'user_name': 'test_singer',
        'password': '123456'
    }
    
    try:
        print("1. 登录测试歌手账号...")
        # 登录获取token
        login_response = requests.post(
            f'{base_url}/users/login/',
            json=login_data
        )
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            access_token = login_result['tokens']['access']
            print(f"   登录成功！获取到访问令牌: {access_token[:20]}...")
            
            # 设置认证头
            auth_headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # 获取当前用户信息
            print("\n2. 获取当前用户信息...")
            profile_response = requests.get(
                f'{base_url}/users/profile/',
                headers=auth_headers
            )
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"   用户信息: {profile['user_name']}, 用户类型: {profile['user_type']} (1=歌手)")
                print(f"   用户ID: {profile['user_id']}")
            else:
                print(f"   获取用户信息失败: {profile_response.status_code}")
                print(f"   错误信息: {profile_response.text}")
            
            # 调用'my_songs'接口
            print("\n3. 调用'my_songs'接口...")
            my_songs_response = requests.get(
                f'{base_url}/music/songs/my_songs/?page=1&page_size=10',
                headers=auth_headers
            )
            
            if my_songs_response.status_code == 200:
                songs_result = my_songs_response.json()
                print(f"   接口调用成功！状态码: {my_songs_response.status_code}")
                
                # 打印返回结果
                print(f"\n4. 接口返回结果:")
                print(f"   - 总歌曲数: {songs_result.get('count', 0)}")
                print(f"   - 当前页码: {songs_result.get('page', 1)}")
                print(f"   - 每页数量: {songs_result.get('page_size', 10)}")
                print(f"   - 总页数: {songs_result.get('total_pages', 1)}")
                
                # 打印歌曲列表
                songs = songs_result.get('results', [])
                print(f"\n5. 歌曲列表 (共 {len(songs)} 首):")
                for i, song in enumerate(songs, 1):
                    print(f"   {i}. {song.get('song_name', '未知歌曲')}")
                    print(f"      - 歌曲ID: {song.get('song_id', 'N/A')}")
                    print(f"      - 歌手: {song.get('song_singer_name', '未知歌手')} (ID: {song.get('song_singer_id', 'N/A')})")
                    print(f"      - 时长: {song.get('song_duration', 'N/A')}秒")
                    print(f"      - 价格: {song.get('song_price', 'N/A')}元")
                    print(f"      - 是否上架: {'是' if song.get('is_active') else '否'}")
                
                print(f"\n测试完成！'my_songs'接口工作正常")
                return True
            else:
                print(f"   接口调用失败: {my_songs_response.status_code}")
                print(f"   错误信息: {my_songs_response.text}")
                return False
        else:
            print(f"   登录失败: {login_response.status_code}")
            print(f"   错误信息: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_my_songs_api()
