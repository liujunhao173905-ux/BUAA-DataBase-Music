<template>
    <div class="social-feedback">
        <!-- 顶部导航栏 -->
        <header class="header">
            <div class="header-content">
                <button @click="$router.go(-1)" class="back-btn">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
                    </svg>
                    返回
                </button>
                <h1>社交反馈</h1>
                <div class="header-right">
                    <div class="user-info">
                        <span>{{ username }}</span>
                        <button @click="$router.push('/profile')" class="profile-btn">个人信息</button>
                        <button @click="handleLogout" class="logout-btn">退出登录</button>
                    </div>
                </div>
            </div>
        </header>

        <!-- 主要内容 -->
        <main class="main-content">
            <!-- 统计概览 -->
            <section class="stats-section">
                <h2>互动统计</h2>
                <div class="stats-cards">
                    <div class="stat-card likes-card">
                        <div class="stat-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                            </svg>
                        </div>
                        <div class="stat-content">
                            <h3>收到点赞</h3>
                            <p class="stat-value">{{ totalLikes }}</p>
                        </div>
                    </div>
                    <div class="stat-card comments-card">
                        <div class="stat-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                            </svg>
                        </div>
                        <div class="stat-content">
                            <h3>收到评论</h3>
                            <p class="stat-value">{{ totalComments }}</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 反馈列表 -->
            <section class="feedback-section">
                <div class="tabs">
                    <button 
                        v-for="tab in tabs" 
                        :key="tab.key" 
                        @click="activeTab = tab.key"
                        :class="['tab-btn', { active: activeTab === tab.key }]"
                    >
                        {{ tab.label }}
                    </button>
                </div>

                <div class="feedback-content">
                    <!-- 最新点赞 -->
                    <div v-if="activeTab === 'likes'" class="feedback-list">
                        <div v-if="recentLikes.length === 0" class="no-data">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                            </svg>
                            <p>还没有收到点赞，继续努力！</p>
                        </div>
                        <div v-else>
                            <div v-for="like in recentLikes" :key="like.id" class="feedback-item like-item">
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

                    <!-- 最新评论 -->
                    <div v-if="activeTab === 'comments'" class="feedback-list">
                        <div v-if="recentComments.length === 0" class="no-data">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                            </svg>
                            <p>还没有收到评论，继续分享你的健康动态！</p>
                        </div>
                        <div v-else>
                            <div v-for="comment in recentComments" :key="comment.id" class="feedback-item comment-item">
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

                    <!-- 健康报告（未来功能） -->
                    <div v-if="activeTab === 'reports'" class="feedback-list">
                        <div class="coming-soon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                            </svg>
                            <h3>健康报告</h3>
                            <p>个人健康报告功能即将上线，敬请期待！</p>
                            <p class="coming-soon-desc">
                                将根据您的睡眠、运动和饮食数据生成详细的健康分析报告，
                                并提供个性化的健康建议。
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'SocialFeedback',
    data() {
        return {
            username: localStorage.getItem('username') || '用户',
            activeTab: 'likes',
            totalLikes: 0,
            totalComments: 0,
            recentLikes: [],
            recentComments: [],
            tabs: [
                { key: 'likes', label: '最新点赞' },
                { key: 'comments', label: '最新评论' },
                { key: 'reports', label: '健康报告' }
            ]
        }
    },
    mounted() {
        this.loadFeedbackData()
    },
    methods: {
        async loadFeedbackData() {
            try {
                // 获取用户收到的点赞和评论
                await Promise.all([
                    this.loadReceivedLikes(),
                    this.loadReceivedComments()
                ])
            } catch (error) {
                console.error('加载反馈数据失败:', error)
            }
        },
        
        async loadReceivedLikes() {
            try {
                const response = await axios.get('/api/social/received-likes/')
                this.recentLikes = response.data.results || response.data || []
                this.totalLikes = response.data.total || this.recentLikes.length
            } catch (error) {
                console.error('加载点赞数据失败:', error)
                this.recentLikes = []
                this.totalLikes = 0
            }
        },
        
        async loadReceivedComments() {
            try {
                const response = await axios.get('/api/social/received-comments/')
                this.recentComments = response.data.results || response.data || []
                this.totalComments = response.data.total || this.recentComments.length
            } catch (error) {
                console.error('加载评论数据失败:', error)
                this.recentComments = []
                this.totalComments = 0
            }
        },
        
        getRecordTypeName(contentType) {
            // 根据content_type返回记录类型的中文名称
            const typeMap = {
                11: '睡眠',  // SleepRecord
                8: '运动',   // ExerciseRecord 
                7: '饮食'    // DietRecord
            }
            return typeMap[contentType] || '健康'
        },
        
        getRecordSummary(record, contentType) {
            // 根据记录类型返回简要描述
            if (!record) return ''
            
            // 如果记录被隐私保护，显示保护信息
            if (record.privacy_protected) {
                return record.message || '该用户已停止分享此记录'
            }
            
            if (contentType === 11) { // 睡眠记录
                return `${this.formatDate(record.sleep_time)} 睡眠时长 ${record.duration_hours || 0}小时`
            } else if (contentType === 8) { // 运动记录
                return `${this.formatDate(record.record_datetime)} ${record.exercise_type_cn} ${record.duration_minutes}分钟`
            } else if (contentType === 7) { // 饮食记录
                // 餐次类型中英文映射
                const mealTypeMap = {
                    'breakfast': '早餐',
                    'lunch': '午餐', 
                    'dinner': '晚餐',
                    'snack': '零食'
                }
                const mealTypeCn = mealTypeMap[record.meal_type] || record.meal_type
                
                // 构建显示信息：日期 + 餐次 + 食物名称 + 分量
                let summary = `${this.formatDate(record.record_date)} ${mealTypeCn} ${record.food_name}`
                
                // 如果有分量信息，添加到显示中
                if (record.quantity) {
                    summary += ` ${record.quantity}`
                }
                
                return summary
            }
            return ''
        },
        
        formatTime(dateString) {
            if (!dateString) return ''
            const date = new Date(dateString)
            const now = new Date()
            const diffMs = now - date
            const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
            const diffDays = Math.floor(diffHours / 24)
            
            if (diffHours < 1) {
                const diffMinutes = Math.floor(diffMs / (1000 * 60))
                return `${diffMinutes}分钟前`
            } else if (diffHours < 24) {
                return `${diffHours}小时前`
            } else if (diffDays < 7) {
                return `${diffDays}天前`
            } else {
                return date.toLocaleDateString('zh-CN')
            }
        },
        
        formatDate(dateString) {
            if (!dateString) return ''
            const date = new Date(dateString)
            return date.toLocaleDateString('zh-CN', {
                month: 'short',
                day: 'numeric'
            })
        },
        
        handleLogout() {
            localStorage.removeItem('token')
            localStorage.removeItem('username')
            this.$router.push('/login')
        }
    }
}
</script>

<style scoped>
.social-feedback {
    min-height: 100vh;
    background-color: #f5f7fa;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.back-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

.back-btn:hover {
    background: rgba(255, 255, 255, 0.3);
}

.back-btn svg {
    width: 1.2rem;
    height: 1.2rem;
}

.header h1 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 600;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.profile-btn, .logout-btn {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

.profile-btn:hover, .logout-btn:hover {
    background: rgba(255, 255, 255, 0.3);
}

.main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.stats-section {
    margin-bottom: 2rem;
}

.stats-section h2 {
    color: #2d3748;
    margin-bottom: 1rem;
    font-size: 1.5rem;
    font-weight: 600;
}

.stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    display: flex;
    align-items: center;
    gap: 1rem;
}

.stat-icon {
    width: 3rem;
    height: 3rem;
    border-radius: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.likes-card .stat-icon {
    background: linear-gradient(135deg, #ff6b6b, #ee5a24);
    color: white;
}

.comments-card .stat-icon {
    background: linear-gradient(135deg, #4ecdc4, #44a08d);
    color: white;
}

.stat-icon svg {
    width: 1.5rem;
    height: 1.5rem;
}

.stat-content h3 {
    margin: 0 0 0.5rem 0;
    color: #4a5568;
    font-size: 0.9rem;
    font-weight: 500;
}

.stat-value {
    margin: 0;
    font-size: 2rem;
    font-weight: 700;
    color: #2d3748;
}

.feedback-section {
    background: white;
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    overflow: hidden;
}

.tabs {
    display: flex;
    border-bottom: 1px solid #e2e8f0;
}

.tab-btn {
    flex: 1;
    padding: 1rem;
    background: none;
    border: none;
    color: #718096;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    border-bottom: 3px solid transparent;
}

.tab-btn:hover {
    background: #f7fafc;
}

.tab-btn.active {
    color: #667eea;
    border-bottom-color: #667eea;
    background: #f7fafc;
}

.feedback-content {
    padding: 1.5rem;
}

.feedback-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.no-data {
    text-align: center;
    padding: 3rem;
    color: #a0aec0;
}

.no-data svg {
    width: 4rem;
    height: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.feedback-item {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    border-radius: 0.75rem;
    background: #f7fafc;
    transition: background-color 0.3s;
}

.feedback-item:hover {
    background: #edf2f7;
}

.feedback-avatar {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1rem;
    flex-shrink: 0;
}

.feedback-content {
    flex: 1;
    min-width: 0;
}

.feedback-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.user-name {
    font-weight: 600;
    color: #2d3748;
}

.feedback-time {
    font-size: 0.8rem;
    color: #a0aec0;
}

.feedback-action {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #4a5568;
    margin-bottom: 0.5rem;
}

.like-icon {
    width: 1rem;
    height: 1rem;
    color: #ff6b6b;
}

.comment-icon {
    width: 1rem;
    height: 1rem;
    color: #4ecdc4;
}

.comment-text {
    background: white;
    padding: 0.75rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    font-style: italic;
    color: #2d3748;
    border-left: 3px solid #4ecdc4;
}

.feedback-record {
    font-size: 0.8rem;
    color: #718096;
    background: white;
    padding: 0.5rem;
    border-radius: 0.375rem;
    border: 1px solid #e2e8f0;
}

.privacy-protected {
    color: #a0aec0;
    font-style: italic;
}

.coming-soon {
    text-align: center;
    padding: 3rem;
    color: #4a5568;
}

.coming-soon svg {
    width: 4rem;
    height: 4rem;
    margin-bottom: 1rem;
    color: #a0aec0;
}

.coming-soon h3 {
    margin: 1rem 0;
    font-size: 1.5rem;
    color: #2d3748;
}

.coming-soon-desc {
    max-width: 600px;
    margin: 1rem auto 0;
    line-height: 1.6;
    color: #718096;
}

@media (max-width: 768px) {
    .header-content {
        padding: 0 1rem;
        flex-direction: column;
        gap: 1rem;
    }
    
    .header h1 {
        font-size: 1.5rem;
    }
    
    .main-content {
        padding: 1rem;
    }
    
    .stats-cards {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .feedback-item {
        padding: 0.75rem;
    }
    
    .feedback-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.25rem;
    }
}
</style> 