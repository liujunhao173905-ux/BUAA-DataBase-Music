<template>
    <div class="friends-container">
        <!-- 顶部导航栏 -->
        <header class="header">
            <div class="header-content">
                <button @click="$router.back()" class="back-btn">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
                    </svg>
                    返回
                </button>
                <h1>好友管理</h1>
                <div></div>
            </div>
        </header>

        <main class="main-content">
            <!-- 标签页切换 -->
            <div class="tabs">
                <button @click="activeTab = 'friends'" :class="{ active: activeTab === 'friends' }" class="tab-btn">
                    好友列表 ({{ friendsList.length }})
                </button>
                <button @click="activeTab = 'requests'" :class="{ active: activeTab === 'requests' }" class="tab-btn">
                    好友请求 ({{ pendingRequests.length }})
                </button>
                <button @click="activeTab = 'add'" :class="{ active: activeTab === 'add' }" class="tab-btn">
                    添加好友
                </button>
            </div>

            <!-- 好友列表标签页 -->
            <div v-if="activeTab === 'friends'" class="tab-content">
                <div v-if="friendsList.length === 0" class="empty-state">
                    <div class="empty-icon">👥</div>
                    <p>还没有好友，快去添加一些吧！</p>
                </div>
                <div v-else class="friends-list">
                    <div v-for="friend in friendsList" :key="friend.id" class="friend-item">
                        <div class="friend-avatar">
                            {{ friend.friend_info.username.charAt(0).toUpperCase() }}
                        </div>
                        <div class="friend-info">
                            <h3>{{ friend.friend_info.username }}</h3>
                            <p class="friend-since">好友关系建立于 {{ formatDate(friend.created_at) }}</p>
                        </div>
                        <div class="friend-actions">
                            <button @click="viewFriendProfile(friend.friend_info.id)" class="action-btn view-btn">
                                查看动态
                            </button>
                            <button @click="deleteFriend(friend)" class="action-btn delete-btn">
                                删除好友
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 好友请求标签页 -->
            <div v-if="activeTab === 'requests'" class="tab-content">
                <div v-if="pendingRequests.length === 0" class="empty-state">
                    <div class="empty-icon">📬</div>
                    <p>暂无好友请求</p>
                </div>
                <div v-else class="requests-list">
                    <div v-for="request in pendingRequests" :key="request.id" class="request-item">
                        <div class="request-avatar">
                            {{ request.from_user.charAt(0).toUpperCase() }}
                        </div>
                        <div class="request-info">
                            <h3>{{ request.from_user }}</h3>
                            <p class="request-time">{{ formatDate(request.created_at) }} 发送请求</p>
                        </div>
                        <div class="request-actions">
                            <button @click="acceptRequest(request)" class="action-btn accept-btn">
                                接受
                            </button>
                            <button @click="rejectRequest(request)" class="action-btn reject-btn">
                                拒绝
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 添加好友标签页 -->
            <div v-if="activeTab === 'add'" class="tab-content">
                <div class="add-friend-form">
                    <h3>搜索并添加好友</h3>
                    <div class="form-group">
                        <label>用户名</label>
                        <input 
                            v-model="searchUsername" 
                            type="text" 
                            placeholder="请输入要添加的好友用户名"
                            @keyup.enter="sendFriendRequest"
                        />
                    </div>
                    <button @click="sendFriendRequest" :disabled="!searchUsername || loading" class="send-request-btn">
                        {{ loading ? '发送中...' : '发送好友请求' }}
                    </button>
                </div>
            </div>

            <!-- 成功/错误提示 -->
            <div v-if="successMessage" class="success-message">
                <span>{{ successMessage }}</span>
                <button @click="successMessage = ''" class="close-btn">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                    </svg>
                </button>
            </div>

            <div v-if="errorMessage" class="error-message">
                <span>{{ errorMessage }}</span>
                <button @click="errorMessage = ''" class="close-btn">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                    </svg>
                </button>
            </div>
        </main>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Friends',
    data() {
        return {
            activeTab: 'friends', // friends, requests, add
            friendsList: [],
            pendingRequests: [],
            searchUsername: '',
            loading: false,
            successMessage: '',
            errorMessage: ''
        }
    },
    async mounted() {
        // 检查URL查询参数，支持直接跳转到指定标签页
        if (this.$route.query.tab) {
            this.activeTab = this.$route.query.tab;
        }
        
        await this.fetchFriends()
        await this.fetchPendingRequests()
    },
    methods: {
        async fetchFriends() {
            try {
                const response = await axios.get('/api/friendship/friends_list/')
                this.friendsList = response.data
            } catch (error) {
                console.error('获取好友列表失败：', error)
                this.errorMessage = '获取好友列表失败'
            }
        },

        async fetchPendingRequests() {
            try {
                const response = await axios.get('/api/friendship/requests_list/')
                this.pendingRequests = response.data
            } catch (error) {
                console.error('获取好友请求失败：', error)
                this.errorMessage = '获取好友请求失败'
            }
        },

        async sendFriendRequest() {
            if (!this.searchUsername.trim()) {
                this.errorMessage = '请输入用户名'
                return
            }

            this.loading = true
            this.errorMessage = ''

            try {
                await axios.post('/api/friendship/send_request/', {
                    to_user: this.searchUsername.trim()
                })
                this.successMessage = '好友请求发送成功！'
                this.searchUsername = ''
            } catch (error) {
                console.error('发送好友请求失败：', error)
                if (error.response?.data?.detail) {
                    this.errorMessage = error.response.data.detail
                } else {
                    this.errorMessage = '发送好友请求失败，请重试'
                }
            } finally {
                this.loading = false
            }
        },

        async acceptRequest(request) {
            try {
                await axios.post(`/api/friendship/${request.id}/accept_request/`)
                this.successMessage = `已接受 ${request.from_user} 的好友请求`
                await this.fetchFriends()
                await this.fetchPendingRequests()
            } catch (error) {
                console.error('接受好友请求失败：', error)
                this.errorMessage = '接受好友请求失败'
            }
        },

        async rejectRequest(request) {
            try {
                await axios.post(`/api/friendship/${request.id}/reject_request/`)
                this.successMessage = `已拒绝 ${request.from_user} 的好友请求`
                await this.fetchPendingRequests()
            } catch (error) {
                console.error('拒绝好友请求失败：', error)
                this.errorMessage = '拒绝好友请求失败'
            }
        },

        async deleteFriend(friend) {
            if (!confirm(`确定要删除好友 ${friend.friend_info.username} 吗？`)) {
                return
            }

            try {
                await axios.post(`/api/friendship/${friend.id}/delete_friend/`)
                this.successMessage = `已删除好友 ${friend.friend_info.username}`
                await this.fetchFriends()
            } catch (error) {
                console.error('删除好友失败：', error)
                this.errorMessage = '删除好友失败'
            }
        },

        viewFriendProfile(friendId) {
            // 跳转到好友动态页面（待实现）
            this.$router.push(`/friend-profile/${friendId}`)
        },

        formatDate(dateString) {
            const date = new Date(dateString)
            return date.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            })
        }
    }
}
</script>

<style scoped>
.friends-container {
    min-height: 100vh;
    background: #f5f7fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.back-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: none;
    border: none;
    color: #333;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 8px;
    transition: background-color 0.2s;
}

.back-btn:hover {
    background: rgba(0, 0, 0, 0.05);
}

.back-btn svg {
    width: 20px;
    height: 20px;
}

h1 {
    color: #333;
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
}

.main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
}

.tabs {
    display: flex;
    background: white;
    border-radius: 12px;
    padding: 4px;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tab-btn {
    flex: 1;
    padding: 1rem;
    background: none;
    border: none;
    color: #666;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.tab-btn.active {
    background: #409eff;
    color: white;
    transform: translateY(-1px);
}

.tab-btn:hover:not(.active) {
    color: #333;
    background: rgba(0, 0, 0, 0.05);
}

.tab-content {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.empty-state {
    text-align: center;
    padding: 3rem;
    color: #666;
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.friends-list, .requests-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.friend-item, .request-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.friend-item:hover, .request-item:hover {
    transform: translateY(-2px);
}

.friend-avatar, .request-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 1.2rem;
}

.friend-info, .request-info {
    flex: 1;
}

.friend-info h3, .request-info h3 {
    margin: 0 0 0.5rem 0;
    color: #333;
    font-size: 1.1rem;
}

.friend-since, .request-time {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
}

.friend-actions, .request-actions {
    display: flex;
    gap: 0.5rem;
}

.action-btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}

.view-btn {
    background: #667eea;
    color: white;
}

.view-btn:hover {
    background: #5a6fd8;
}

.delete-btn, .reject-btn {
    background: #ff6b6b;
    color: white;
}

.delete-btn:hover, .reject-btn:hover {
    background: #ff5252;
}

.accept-btn {
    background: #51cf66;
    color: white;
}

.accept-btn:hover {
    background: #40c057;
}

.add-friend-form {
    max-width: 500px;
    margin: 0 auto;
}

.add-friend-form h3 {
    text-align: center;
    color: #333;
    margin-bottom: 2rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
    font-weight: 500;
}

.form-group input {
    width: 100%;
    padding: 1rem;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s ease;
}

.form-group input:focus {
    outline: none;
    border-color: #667eea;
}

.send-request-btn {
    width: 100%;
    padding: 1rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.send-request-btn:hover:not(:disabled) {
    transform: translateY(-2px);
}

.send-request-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.success-message, .error-message {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    color: white;
    font-weight: 500;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-width: 300px;
    max-width: 500px;
}

.success-message {
    background: #51cf66;
}

.error-message {
    background: #ff6b6b;
}

.close-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 2px;
    color: white;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-left: 10px;
}

.close-btn svg {
    width: 12px;
    height: 12px;
}

.close-btn:hover {
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 2px;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .tabs {
        flex-direction: column;
        gap: 2px;
    }
    
    .friend-item, .request-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .friend-actions, .request-actions {
        width: 100%;
        justify-content: center;
    }
    
    .action-btn {
        flex: 1;
    }
}
</style> 