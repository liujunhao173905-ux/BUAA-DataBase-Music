<template>
    <div class="social-hub">
        <!-- 头部导航 -->
        <header class="hub-header">
            <h1>
                <svg viewBox="0 0 24 24" fill="currentColor" class="header-icon">
                    <path d="M12 12.75c1.63 0 3.07.39 4.24.9 1.08.48 1.76 1.56 1.76 2.73V18H6v-1.61c0-1.18.68-2.26 1.76-2.74 1.17-.51 2.61-.9 4.24-.9zM4 13c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm1.13 1.1c-.37-.06-.74-.1-1.13-.1C2.48 14 0 14.81 0 16.25V18h4.5v-1.61c0-.83.23-1.61.63-2.29zM20 13c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm-.63 1.1c.4.68.63 1.46.63 2.29V18H24v-1.75C24 14.81 21.52 14 20 14c-.39 0-.76.04-1.13.1zM12 6c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3z"/>
                </svg>
                社交管理
            </h1>
            <button @click="$router.push('/dashboard')" class="back-btn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.42-1.41L7.83 13H20v-2z"/>
                </svg>
                返回首页
            </button>
        </header>

        <!-- 社交功能导航 -->
        <nav class="social-nav">
            <button
                v-for="tab in tabs"
                :key="tab.key"
                @click="handleTabClick(tab.key)"
                :class="['nav-btn', { active: activeTab === tab.key }]"
            >
                <svg viewBox="0 0 24 24" fill="currentColor" class="nav-icon">
                    <path v-if="tab.icon === 'users'" d="M12 12.75c1.63 0 3.07.39 4.24.9 1.08.48 1.76 1.56 1.76 2.73V18H6v-1.61c0-1.18.68-2.26 1.76-2.74 1.17-.51 2.61-.9 4.24-.9zM4 13c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm1.13 1.1c-.37-.06-.74-.1-1.13-.1C2.48 14 0 14.81 0 16.25V18h4.5v-1.61c0-.83.23-1.61.63-2.29zM20 13c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm-.63 1.1c.4.68.63 1.46.63 2.29V18H24v-1.75C24 14.81 21.52 14 20 14c-.39 0-.76.04-1.13.1zM12 6c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3z"/>
                    <path v-else-if="tab.icon === 'mail'" d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                    <path v-else-if="tab.icon === 'plus'" d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
                    <path v-else-if="tab.icon === 'chat'" d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                    <path v-else-if="tab.icon === 'activity'" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
                {{ tab.label }}
                <span v-if="tab.badge && getBadgeCount(tab.key) > 0" class="nav-badge">
                    {{ getBadgeCount(tab.key) }}
                </span>
            </button>
        </nav>

        <!-- 内容区域 -->
        <main class="hub-content">
            <!-- 好友列表 -->
            <div v-if="activeTab === 'friends'" class="content-section">
                <div class="section-header">
                    <h2>我的好友</h2>
                    <div class="friends-stats">
                        <span>共 {{ friendsList.length }} 位好友</span>
                    </div>
                </div>

                <div v-if="friendsList.length === 0" class="no-data">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M16 4c0-1.11.89-2 2-2s2 .89 2 2-.89 2-2 2-2-.89-2-2zM4 18v-1c0-1.1.9-2 2-2h2.5c.83 0 1.58.41 2.03 1.05C11.03 16.68 11.5 17 12 17s.97-.32 1.47-.95C13.92 15.41 14.67 15 15.5 15H18c1.1 0 2 .9 2 2v1H4z"/>
                    </svg>
                    <p>还没有好友，快去添加好友吧！</p>
                </div>

                <div v-else class="friends-grid">
                    <div v-for="friend in friendsList" :key="friend.id" class="friend-card">
                        <div class="friend-avatar">
                            {{ (friend.friend_info?.username || '未知').charAt(0).toUpperCase() }}
                        </div>
                        <div class="friend-info">
                            <h3>{{ friend.friend_info?.username || '未知用户' }}</h3>
                            <p>已添加 {{ formatRelativeTime(friend.created_at) }}</p>
                        </div>
                        <div class="friend-actions">
                            <button @click="viewFriendProfile(friend.friend_info?.id)" class="action-btn view-btn">
                                查看动态
                            </button>
                            <button @click="deleteFriend(friend.id)" class="action-btn delete-btn">
                                删除好友
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 好友请求 -->
            <div v-if="activeTab === 'requests'" class="content-section">
                <div class="section-header">
                    <h2>好友请求</h2>
                    <div class="requests-stats">
                        <span>{{ pendingRequests.length }} 个待处理请求</span>
                    </div>
                </div>

                <div v-if="pendingRequests.length === 0" class="no-data">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    <p>暂无好友请求</p>
                </div>

                <div v-else class="requests-list">
                    <div v-for="request in pendingRequests" :key="request.id" class="request-item">
                        <div class="request-avatar">
                            {{ request.from_user.charAt(0).toUpperCase() }}
                        </div>
                        <div class="request-info">
                            <h3>{{ request.from_user }}</h3>
                            <p>{{ formatTime(request.created_at) }} 申请加你为好友</p>
                        </div>
                        <div class="request-actions">
                            <button @click="acceptRequest(request.id)" class="action-btn accept-btn">
                                接受
                            </button>
                            <button @click="rejectRequest(request.id)" class="action-btn reject-btn">
                                拒绝
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 添加好友 -->
            <div v-if="activeTab === 'add'" class="content-section">
                <div class="section-header">
                    <h2>添加好友</h2>
                </div>

                <div class="add-friend-form">
                    <div class="form-group">
                        <label>用户名</label>
                        <div class="input-group">
                            <input
                                v-model="newFriendUsername"
                                type="text"
                                placeholder="请输入要添加的用户名"
                                @keyup.enter="sendFriendRequest"
                            >
                            <button @click="sendFriendRequest" :disabled="!newFriendUsername.trim()" class="add-btn">
                                发送请求
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 最近发送的请求 -->
                <div v-if="sentRequests.length > 0" class="sent-requests">
                    <h3>最近发送的请求</h3>
                    <div class="sent-list">
                        <div v-for="request in sentRequests" :key="request.id" class="sent-item">
                            <span class="sent-username">{{ request.to_user }}</span>
                            <span class="sent-status" :class="request.status">
                                {{ getStatusText(request.status) }}
                            </span>
                            <span class="sent-time">{{ formatTime(request.created_at) }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 社交反馈 -->
            <div v-if="activeTab === 'feedback'" class="content-section">
                <div class="section-header">
                    <h2>社交反馈</h2>
                    <div class="feedback-stats">
                        <div class="stat-item">
                            <span class="stat-number">{{ totalLikes }}</span>
                            <span class="stat-label">收到点赞</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">{{ totalComments }}</span>
                            <span class="stat-label">收到评论</span>
                        </div>
                    </div>
                </div>

                <!-- 反馈类型切换 -->
                <div class="feedback-tabs">
                    <button
                        v-for="feedbackTab in feedbackTabs"
                        :key="feedbackTab.key"
                        @click="activeFeedbackTab = feedbackTab.key"
                        :class="['feedback-tab', { active: activeFeedbackTab === feedbackTab.key }]"
                    >
                        {{ feedbackTab.label }}
                    </button>
                </div>

                <!-- 点赞列表 -->
                <div v-if="activeFeedbackTab === 'likes'" class="feedback-content">
                    <div v-if="recentLikes.length === 0" class="no-data">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                        </svg>
                        <p>还没有收到点赞，继续努力！</p>
                    </div>
                    <div v-else class="feedback-list">
                        <div v-for="like in recentLikes" :key="like.id" class="feedback-item">
                            <div class="feedback-avatar">
                                {{ like.user.charAt(0).toUpperCase() }}
                            </div>
                            <div class="feedback-content">
                                <div class="feedback-header">
                                    <span class="user-name">{{ like.user }}</span>
                                    <span class="feedback-time">{{ formatTime(like.created_at) }}</span>
                                </div>
                                <div class="feedback-action">
                                    <svg viewBox="0 0 24 24" fill="currentColor" class="like-icon">
                                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                                    </svg>
                                    点赞了你的{{ getRecordTypeName(like.content_type) }}记录
                                </div>
                                <div class="feedback-record" v-if="like.record">
                                    <span :class="{ 'privacy-protected': like.record.privacy_protected }">
                                        {{ getRecordSummary(like.record, like.content_type) }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 评论列表 -->
                <div v-if="activeFeedbackTab === 'comments'" class="feedback-content">
                    <div v-if="recentComments.length === 0" class="no-data">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                        </svg>
                        <p>还没有收到评论</p>
                    </div>
                    <div v-else class="feedback-list">
                        <div v-for="comment in recentComments" :key="comment.id" class="feedback-item">
                            <div class="feedback-avatar">
                                {{ comment.author.charAt(0).toUpperCase() }}
                            </div>
                            <div class="feedback-content">
                                <div class="feedback-header">
                                    <span class="user-name">{{ comment.author }}</span>
                                    <span class="feedback-time">{{ formatTime(comment.created_at) }}</span>
                                </div>
                                <div class="feedback-action">
                                    <svg viewBox="0 0 24 24" fill="currentColor" class="comment-icon">
                                        <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                                    </svg>
                                    评论了你的{{ getRecordTypeName(comment.content_type) }}记录
                                </div>
                                <div class="comment-text">
                                    "{{ comment.content }}"
                                </div>
                                <div class="feedback-record" v-if="comment.record">
                                    <span :class="{ 'privacy-protected': comment.record.privacy_protected }">
                                        {{ getRecordSummary(comment.record, comment.content_type) }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'SocialHub',
    data() {
        return {
            activeTab: 'friends',
            activeFeedbackTab: 'likes',
            tabs: [
                { key: 'friends', label: '好友列表', icon: 'users', badge: false },
                { key: 'requests', label: '好友请求', icon: 'mail', badge: true },
                { key: 'add', label: '添加好友', icon: 'plus', badge: false },
                { key: 'feedback', label: '社交反馈', icon: 'chat', badge: true },
                { key: 'my-activity', label: '我的健康动态', icon: 'activity', badge: false }
            ],
            feedbackTabs: [
                { key: 'likes', label: '最新点赞' },
                { key: 'comments', label: '最新评论' }
            ],
            // 好友相关数据
            friendsList: [],
            pendingRequests: [],
            sentRequests: [],
            newFriendUsername: '',
            // 社交反馈数据
            totalLikes: 0,
            totalComments: 0,
            recentLikes: [],
            recentComments: [],
            // 收件箱未读社交反馈数量
            unreadFeedbackCount: 0
        };
    },
    mounted() {
        // 检查路由参数中是否指定了tab
        if (this.$route.query.tab) {
            const validTabs = ['friends', 'requests', 'add', 'feedback'];
            if (validTabs.includes(this.$route.query.tab)) {
                this.activeTab = this.$route.query.tab;
            }
        }
        this.loadAllData();
    },
    watch: {
        activeTab() {
            this.loadTabData();
        }
    },
    methods: {
        handleTabClick(tabKey) {
            if (tabKey === 'my-activity') {
                // 跳转到我的健康动态页面
                this.$router.push('/my-activity');
            } else {
                // 普通标签切换
                this.activeTab = tabKey;
            }
        },

        async loadAllData() {
            await Promise.all([
                this.loadFriendsList(),
                this.loadPendingRequests(),
                this.loadSocialFeedback(),
                this.loadUnreadFeedbackCount()
            ]);
        },

        async loadTabData() {
            switch (this.activeTab) {
                case 'friends':
                    await this.loadFriendsList();
                    break;
                case 'requests':
                    await this.loadPendingRequests();
                    break;
                case 'feedback':
                    await this.loadSocialFeedback();
                    // 当用户点击社交反馈时，标记相关消息为已读
                    await this.markSocialFeedbackAsRead();
                    break;
            }
        },

        async markSocialFeedbackAsRead() {
            try {
                // 标记点赞和评论类型的消息为已读
                await axios.post('/api/inbox/mark_feedback_read/');
                // 清除本地计数，让徽章消失
                this.totalLikes = 0;
                this.totalComments = 0;
                // 清除未读反馈计数
                this.unreadFeedbackCount = 0;
            } catch (error) {
                console.error('标记社交反馈为已读失败：', error);
            }
        },

        async loadUnreadFeedbackCount() {
            try {
                const response = await axios.get('/api/inbox/summary/');
                const typeCounts = response.data.type_counts || {};
                this.unreadFeedbackCount = (typeCounts.like_received || 0) + (typeCounts.comment_received || 0);
            } catch (error) {
                console.error('加载未读反馈计数失败：', error);
                this.unreadFeedbackCount = 0;
            }
        },

        // 好友列表相关方法
        async loadFriendsList() {
            try {
                const response = await axios.get('/api/friendship/friends_list/');
                this.friendsList = response.data;
            } catch (error) {
                console.error('加载好友列表失败：', error);
                this.friendsList = [];
            }
        },

        async loadPendingRequests() {
            try {
                const response = await axios.get('/api/friendship/requests_list/');
                this.pendingRequests = response.data;
            } catch (error) {
                console.error('加载好友请求失败：', error);
                this.pendingRequests = [];
            }
        },

        async sendFriendRequest() {
            if (!this.newFriendUsername.trim()) return;

            try {
                await axios.post('/api/friendship/send_request/', {
                    to_user: this.newFriendUsername
                });
                this.$message?.success?.('好友请求已发送');
                this.newFriendUsername = '';
                // 刷新发送的请求列表
                await this.loadSentRequests();
            } catch (error) {
                console.error('发送好友请求失败：', error);
                const message = error.response?.data?.detail || '发送失败，请稍后重试';
                this.$message?.error?.(message);
            }
        },

        async acceptRequest(requestId) {
            try {
                await axios.post(`/api/friendship/${requestId}/accept_request/`);
                this.$message?.success?.('已接受好友请求');
                await this.loadPendingRequests();
                await this.loadFriendsList();
            } catch (error) {
                console.error('接受好友请求失败：', error);
                this.$message?.error?.('操作失败，请稍后重试');
            }
        },

        async rejectRequest(requestId) {
            try {
                await axios.post(`/api/friendship/${requestId}/reject_request/`);
                this.$message?.success?.('已拒绝好友请求');
                await this.loadPendingRequests();
            } catch (error) {
                console.error('拒绝好友请求失败：', error);
                this.$message?.error?.('操作失败，请稍后重试');
            }
        },

        async deleteFriend(friendshipId) {
            if (!confirm('确定要删除这个好友吗？')) return;

            try {
                await axios.post(`/api/friendship/${friendshipId}/delete_friend/`);
                this.$message?.success?.('已删除好友');
                await this.loadFriendsList();
            } catch (error) {
                console.error('删除好友失败：', error);
                this.$message?.error?.('操作失败，请稍后重试');
            }
        },

        viewFriendProfile(friendId) {
            this.$router.push(`/friend-profile/${friendId}`);
        },

        async loadSentRequests() {
            // 这里需要后端提供发送的请求接口
            // 暂时留空，等待后端实现
        },

        // 社交反馈相关方法
        async loadSocialFeedback() {
            try {
                await Promise.all([
                    this.loadReceivedLikes(),
                    this.loadReceivedComments()
                ]);
            } catch (error) {
                console.error('加载社交反馈失败：', error);
            }
        },

        async loadReceivedLikes() {
            try {
                const response = await axios.get('/api/social/received-likes/');
                this.recentLikes = response.data.results || response.data || [];
                this.totalLikes = response.data.total || this.recentLikes.length;
            } catch (error) {
                console.error('加载点赞数据失败：', error);
                this.recentLikes = [];
                this.totalLikes = 0;
            }
        },

        async loadReceivedComments() {
            try {
                const response = await axios.get('/api/social/received-comments/');
                this.recentComments = response.data.results || response.data || [];
                this.totalComments = response.data.total || this.recentComments.length;
            } catch (error) {
                console.error('加载评论数据失败：', error);
                this.recentComments = [];
                this.totalComments = 0;
            }
        },

        // 工具方法
        getBadgeCount(tabKey) {
            switch (tabKey) {
                case 'requests':
                    return this.pendingRequests.length;
                case 'feedback':
                    return this.unreadFeedbackCount;
                default:
                    return 0;
            }
        },

        formatTime(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            const now = new Date();
            const diffTime = Math.abs(now - date);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays === 1) {
                return '今天';
            } else if (diffDays === 2) {
                return '昨天';
            } else if (diffDays <= 7) {
                return `${diffDays - 1}天前`;
            } else {
                return date.toLocaleDateString('zh-CN');
            }
        },

        formatRelativeTime(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            const now = new Date();
            const diffTime = Math.abs(now - date);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays <= 30) {
                return `${diffDays}天`;
            } else if (diffDays <= 365) {
                return `${Math.ceil(diffDays / 30)}个月`;
            } else {
                return `${Math.ceil(diffDays / 365)}年`;
            }
        },

        getStatusText(status) {
            const statusMap = {
                'pending': '等待回复',
                'accepted': '已接受',
                'declined': '已拒绝'
            };
            return statusMap[status] || status;
        },

        getRecordTypeName(contentType) {
            // 根据content_type返回记录类型的中文名称
            const typeMap = {
                11: '睡眠',  // SleepRecord
                8: '运动',   // ExerciseRecord
                7: '饮食'    // DietRecord
            };
            return typeMap[contentType] || '健康';
        },

        getRecordSummary(record, contentType) {
            // 根据记录类型返回简要描述
            if (!record) return '';

            // 如果记录被隐私保护，显示保护信息
            if (record.privacy_protected) {
                return record.message || '该用户已停止分享此记录';
            }

            if (contentType === 11) { // 睡眠记录
                return `${this.formatDate(record.sleep_time)} 睡眠时长 ${record.duration_hours || 0}小时`;
            } else if (contentType === 8) { // 运动记录
                return `${this.formatDate(record.record_datetime)} ${record.exercise_type_cn} ${record.duration_minutes}分钟`;
            } else if (contentType === 7) { // 饮食记录
                // 餐次类型中英文映射
                const mealTypeMap = {
                    'breakfast': '早餐',
                    'lunch': '午餐',
                    'dinner': '晚餐',
                    'snack': '零食'
                };
                const mealTypeCn = mealTypeMap[record.meal_type] || record.meal_type;

                // 构建显示信息：日期 + 餐次 + 食物名称 + 分量
                let summary = `${this.formatDate(record.record_date)} ${mealTypeCn} ${record.food_name}`;

                // 如果有分量信息，添加到显示中
                if (record.quantity) {
                    summary += ` ${record.quantity}`;
                }

                return summary;
            }
            return '';
        },

        formatDate(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleDateString('zh-CN', {
                month: 'short',
                day: 'numeric'
            });
        },
    }
};
</script>

<style scoped>
.social-hub {
    min-height: 100vh;
    background: #f5f7fa;
    padding-bottom: 40px;
}

/* 头部样式 */
.hub-header {
    background: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.hub-header h1 {
    margin: 0;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 24px;
}

.header-icon {
    width: 28px;
    height: 28px;
    color: #3b82f6;
}

.back-btn {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    transition: background-color 0.3s;
}

.back-btn:hover {
    background: #337ecc;
}

.back-btn svg {
    width: 16px;
    height: 16px;
}

/* 导航样式 */
.social-nav {
    background: white;
    padding: 0 20px;
    display: flex;
    gap: 0;
    border-bottom: 1px solid #e1e8ed;
}

.nav-btn {
    background: none;
    border: none;
    padding: 16px 24px;
    cursor: pointer;
    color: #666;
    border-bottom: 3px solid transparent;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    transition: all 0.3s;
    position: relative;
}

.nav-btn:hover {
    color: #3b82f6;
    background: #f8f9fa;
}

.nav-btn.active {
    color: #3b82f6;
    border-bottom-color: #3b82f6;
    background: #f8f9fa;
}

.nav-icon {
    width: 18px;
    height: 18px;
}

.nav-badge {
    background: #ff4757;
    color: white;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 10px;
    min-width: 16px;
    text-align: center;
    line-height: 1.2;
}

/* 内容区域 */
.hub-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 30px 20px;
}

.content-section {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding: 0 4px;
}

.section-header h2 {
    margin: 0;
    color: #2c3e50;
    font-size: 20px;
}

.friends-stats, .requests-stats {
    color: #666;
    font-size: 14px;
}

.feedback-stats {
    display: flex;
    gap: 24px;
}

.stat-item {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: 20px;
    font-weight: bold;
    color: #3b82f6;
}

.stat-label {
    font-size: 12px;
    color: #666;
}

/* 无数据状态 */
.no-data {
    text-align: center;
    padding: 60px 20px;
    color: #999;
}

.no-data svg {
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}

.no-data p {
    margin: 0;
    font-size: 16px;
}

/* 好友网格 */
.friends-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 20px;
}

.friend-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 16px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.friend-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.friend-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6, #67c23a);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 18px;
}

.friend-info {
    flex: 1;
}

.friend-info h3 {
    margin: 0 0 4px 0;
    color: #2c3e50;
    font-size: 16px;
}

.friend-info p {
    margin: 0;
    color: #666;
    font-size: 14px;
}

.friend-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.action-btn {
    padding: 6px 12px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.3s;
    white-space: nowrap;
}

.view-btn {
    background: #3b82f6;
    color: white;
}

.view-btn:hover {
    background: #2563eb;
}

.delete-btn {
    background: #f56c6c;
    color: white;
}

.delete-btn:hover {
    background: #f04747;
}

.accept-btn {
    background: #67c23a;
    color: white;
}

.accept-btn:hover {
    background: #5daf34;
}

.reject-btn {
    background: #e6a23c;
    color: white;
}

.reject-btn:hover {
    background: #cf9236;
}

/* 请求列表 */
.requests-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.request-item {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 16px;
}

.request-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #e6a23c, #f56c6c);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 18px;
}

.request-info {
    flex: 1;
}

.request-info h3 {
    margin: 0 0 4px 0;
    color: #2c3e50;
    font-size: 16px;
}

.request-info p {
    margin: 0;
    color: #666;
    font-size: 14px;
}

.request-actions {
    display: flex;
    gap: 8px;
}

/* 添加好友表单 */
.add-friend-form {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 24px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #2c3e50;
    font-weight: 500;
}

.input-group {
    display: flex;
    gap: 12px;
}

.input-group input {
    flex: 1;
    padding: 12px 16px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.3s;
}

.input-group input:focus {
    outline: none;
    border-color: #3b82f6;
}

.add-btn {
    padding: 12px 24px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
    white-space: nowrap;
}

.add-btn:hover:not(:disabled) {
    background: #2563eb;
}

.add-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

/* 已发送请求 */
.sent-requests {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sent-requests h3 {
    margin: 0 0 16px 0;
    color: #2c3e50;
}

.sent-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.sent-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 8px;
}

.sent-username {
    font-weight: 500;
    color: #2c3e50;
}

.sent-status {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 12px;
}

.sent-status.pending {
    background: #fff3cd;
    color: #856404;
}

.sent-status.accepted {
    background: #d1e7dd;
    color: #0f5132;
}

.sent-status.declined {
    background: #f8d7da;
    color: #721c24;
}

.sent-time {
    color: #666;
    font-size: 12px;
}

/* 反馈相关样式 */
.feedback-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 24px;
}

.feedback-tab {
    padding: 10px 20px;
    background: white;
    border: 1px solid #e1e8ed;
    border-radius: 6px;
    cursor: pointer;
    color: #666;
    transition: all 0.3s;
}

.feedback-tab.active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.feedback-tab:hover:not(.active) {
    background: #f5f7fa;
}

.feedback-content {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 24px;
}

.feedback-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.feedback-item {
    display: flex;
    gap: 16px;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
}

.feedback-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6, #67c23a);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 14px;
    flex-shrink: 0;
}

.feedback-content {
    flex: 1;
}

.feedback-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.user-name {
    font-weight: 500;
    color: #2c3e50;
}

.feedback-time {
    color: #666;
    font-size: 12px;
}

.feedback-action {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #666;
    font-size: 14px;
    margin-bottom: 8px;
}

.like-icon, .comment-icon {
    width: 16px;
    height: 16px;
}

.like-icon {
    color: #ff4757;
}

.comment-icon {
    color: #3b82f6;
}

.comment-text {
    background: white;
    padding: 12px;
    border-radius: 8px;
    border-left: 3px solid #3b82f6;
    margin-bottom: 8px;
    font-style: italic;
    color: #2c3e50;
}

.feedback-record {
    color: #666;
    font-size: 12px;
    padding: 8px 12px;
    background: white;
    border-radius: 6px;
}

.privacy-protected {
    color: #999;
    font-style: italic;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .hub-header {
        padding: 16px;
    }

    .hub-header h1 {
        font-size: 20px;
    }

    .social-nav {
        padding: 0 10px;
        overflow-x: auto;
    }

    .nav-btn {
        padding: 12px 16px;
        font-size: 14px;
        white-space: nowrap;
    }

    .friends-grid {
        grid-template-columns: 1fr;
    }

    .friend-card {
        flex-direction: column;
        text-align: center;
    }

    .friend-actions {
        flex-direction: row;
        width: 100%;
    }

    .request-item {
        flex-direction: column;
        align-items: stretch;
    }

    .request-actions {
        width: 100%;
        justify-content: space-between;
    }

    .input-group {
        flex-direction: column;
    }

    .feedback-stats {
        justify-content: space-around;
    }

    .feedback-item {
        flex-direction: column;
    }

    .feedback-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }
}
</style>