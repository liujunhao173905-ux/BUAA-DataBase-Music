import requests
import json

# 测试API的基础URL
BASE_URL = 'http://127.0.0.1:8000/api'

# 测试用户的令牌（需要先登录获取）
# 注意：这里需要替换为实际登录后的令牌
TEST_TOKEN = 'your_test_token_here'

# 测试用户ID和歌单ID
TEST_USER_ID = 2  # 假设这是一个歌手的ID
TEST_PLAYLIST_ID = 1  # 假设这是一个歌单的ID

# 创建请求头
def get_headers():
    return {
        'Authorization': f'Bearer {TEST_TOKEN}',
        'Content-Type': 'application/json'
    }

# 测试关注歌手API
def test_follow_user():
    print("=== 测试关注歌手API ===")
    url = f'{BASE_URL}/users/{TEST_USER_ID}/follow/'
    response = requests.post(url, headers=get_headers())
    print(f"关注歌手状态码: {response.status_code}")
    print(f"关注歌手响应: {response.json()}")
    return response.status_code

# 测试检查关注状态API
def test_check_follow():
    print("\n=== 测试检查关注状态API ===")
    url = f'{BASE_URL}/users/{TEST_USER_ID}/follow/'
    response = requests.get(url, headers=get_headers())
    print(f"检查关注状态码: {response.status_code}")
    print(f"检查关注响应: {response.json()}")
    return response.status_code

# 测试取消关注歌手API
def test_unfollow_user():
    print("\n=== 测试取消关注歌手API ===")
    url = f'{BASE_URL}/users/{TEST_USER_ID}/follow/'
    response = requests.delete(url, headers=get_headers())
    print(f"取消关注状态码: {response.status_code}")
    print(f"取消关注响应: {response.json()}")
    return response.status_code

# 测试收藏歌单API
def test_star_playlist():
    print("\n=== 测试收藏歌单API ===")
    url = f'{BASE_URL}/playlists/{TEST_PLAYLIST_ID}/star/'
    response = requests.post(url, headers=get_headers())
    print(f"收藏歌单状态码: {response.status_code}")
    print(f"收藏歌单响应: {response.json()}")
    return response.status_code

# 测试检查收藏状态API
def test_check_star():
    print("\n=== 测试检查收藏状态API ===")
    url = f'{BASE_URL}/playlists/{TEST_PLAYLIST_ID}/check_star/'
    response = requests.get(url, headers=get_headers())
    print(f"检查收藏状态码: {response.status_code}")
    print(f"检查收藏响应: {response.json()}")
    return response.status_code

# 测试取消收藏歌单API
def test_unstar_playlist():
    print("\n=== 测试取消收藏歌单API ===")
    url = f'{BASE_URL}/playlists/{TEST_PLAYLIST_ID}/unstar/'
    response = requests.delete(url, headers=get_headers())
    print(f"取消收藏状态码: {response.status_code}")
    print(f"取消收藏响应: {response.json()}")
    return response.status_code

# 测试获取关注列表API
def test_get_following_list():
    print("\n=== 测试获取关注列表API ===")
    url = f'{BASE_URL}/users/me/following/'
    response = requests.get(url, headers=get_headers())
    print(f"获取关注列表状态码: {response.status_code}")
    print(f"获取关注列表响应: {response.json()}")
    return response.status_code

# 测试获取收藏歌单列表API
def test_get_starred_playlists():
    print("\n=== 测试获取收藏歌单列表API ===")
    url = f'{BASE_URL}/playlists/my_starred/'
    response = requests.get(url, headers=get_headers())
    print(f"获取收藏歌单列表状态码: {response.status_code}")
    print(f"获取收藏歌单列表响应: {response.json()}")
    return response.status_code

if __name__ == '__main__':
    # 注意：需要先设置有效的TEST_TOKEN才能运行测试
    if TEST_TOKEN == 'your_test_token_here':
        print("请先登录获取有效的令牌，并替换TEST_TOKEN变量的值")
        print("可以通过访问登录API获取令牌:")
        print("POST /api/users/login/ with {\"user_name\": \"your_username\", \"password\": \"your_password\"}")
    else:
        # 运行所有测试
        test_follow_user()
        test_check_follow()
        test_get_following_list()
        test_star_playlist()
        test_check_star()
        test_get_starred_playlists()
        test_unfollow_user()
        test_unstar_playlist()