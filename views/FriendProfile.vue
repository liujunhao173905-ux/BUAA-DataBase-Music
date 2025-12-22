<template>
    <div class="friend-profile-container">
        <!-- 顶部导航栏 -->
        <header class="header">
            <div class="header-content">
                <button @click="$router.back()" class="back-btn">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
                    </svg>
                    返回
                </button>
                <h1>{{ friendInfo.username }} 的健康动态</h1>
                <div></div>
            </div>
        </header>

        <main class="main-content">
            <!-- 加载状态 -->
            <div v-if="loading" class="loading-state">
                <div class="spinner"></div>
                <p>加载中...</p>
            </div>

            <!-- 错误状态 -->
            <div v-else-if="errorMessage" class="error-state">
                <div class="error-icon">⚠️</div>
                <h3>{{ errorMessage }}</h3>
                <button @click="fetchFriendData" class="retry-btn">重试</button>
            </div>

            <!-- 好友动态内容 -->
            <div v-else class="friend-dashboard">
                <!-- 好友基本信息 -->
                <div class="friend-info-card">
                    <div class="friend-avatar">
                        {{ friendInfo.username?.charAt(0).toUpperCase() }}
                    </div>
                    <div class="friend-details">
                        <h2>{{ friendInfo.username }}</h2>
                        <p class="join-date">加入时间：{{ formatDate(friendInfo.date_joined) }}</p>
                    </div>
                </div>

                <!-- 健康记录列表 -->
                <div class="health-records">
                    <h3>最近健康记录</h3>

                    <!-- 睡眠记录 -->
                    <div v-if="dashboardData.recent_sleep && dashboardData.recent_sleep.length > 0" class="record-section">
                        <h4 class="section-title">
                            <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" />
                            </svg>
                            睡眠记录
                        </h4>
                        <div class="records-list">
                            <div v-for="record in dashboardData.recent_sleep" :key="record.id" class="record-item sleep-record">
                                <div class="record-content">
                                    <div class="record-header">
                                        <span class="record-date">{{ formatDate(record.sleep_time) }}</span>
                                        <span class="record-duration">{{ formatSleepDuration(record.sleep_time, record.wake_time) }}</span>
                                    </div>
                                    <div class="record-details">
                                        <span class="detail-item">
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                                            </svg>
                                            入睡：{{ formatTime(record.sleep_time) }}
                                        </span>
                                        <span class="detail-item">
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 6c0-.55.45-1 1-1s1 .45 1 1-1-.45-1 1v2.47l1.21.13c.33.03.55.3.55.63 0 .3-.21.57-.5.63L12 13.13V15c0 .55-.45 1-1 1s-1-.45-1-1V12c0-.55.45-1 1-1z"/>
                                            </svg>
                                            起床：{{ formatTime(record.wake_time) }}
                                        </span>
                                    </div>
                                </div>
                                <RecordActions
                                    :record="record"
                                    record-type="sleeprecord"
                                    @like-updated="updateLikes"
                                    @comment-added="updateComments"
                                />
                            </div>
                        </div>
                    </div>

                    <!-- 运动记录 -->
                    <div v-if="dashboardData.recent_exercise && dashboardData.recent_exercise.length > 0" class="record-section">
                        <h4 class="section-title">
                            <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                                <path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z" />
                            </svg>
                            运动记录
                        </h4>
                        <div class="records-list">
                            <div v-for="record in dashboardData.recent_exercise" :key="record.id" class="record-item exercise-record">
                                <div class="record-content">
                                    <div class="record-header">
                                        <span class="record-date">{{ formatDate(record.record_datetime) }}</span>
                                        <span class="record-calories">{{ record.calories_burned }}卡路里</span>
                                    </div>
                                    <div class="record-details">
                                        <span class="detail-item">
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z"/>
                                            </svg>
                                            {{ record.exercise_type_cn }}
                                        </span>
                                        <span class="detail-item">
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
                                            </svg>
                                            {{ record.duration_minutes }}分钟
                                        </span>
                                        <span class="detail-item">
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"/>
                                            </svg>
                                            {{ getIntensityText(record.intensity) }}
                                        </span>
                                    </div>
                                </div>
                                <RecordActions
                                    :record="record"
                                    record-type="exerciserecord"
                                    @like-updated="updateLikes"
                                    @comment-added="updateComments"
                                />
                            </div>
                        </div>
                    </div>

                    <!-- 饮食记录 -->
                    <div v-if="dashboardData.recent_diet && dashboardData.recent_diet.length > 0" class="record-section">
                        <h4 class="section-title">
                            <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                                <path d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z" />
                            </svg>
                            饮食记录
                        </h4>
                        <div class="records-list">
                            <div v-for="record in dashboardData.recent_diet" :key="record.id" class="record-item diet-record">
                                <div class="record-content">
                                    <div class="record-header">
                                        <span class="record-date">{{ formatDate(record.record_date) }}</span>
                                        <span class="record-calories">{{ record.calories }}卡路里</span>
                                    </div>
                                    <div class="record-details">
                                        <span class="detail-item">
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path d="M8.1 13.34l2.83-2.83L3.91 3.5c-1.56 1.56-1.56 4.09 0 5.66l4.19 4.18zm6.78-1.81c1.53.71 3.68.21 5.27-1.38 1.91-1.91 2.28-4.65.81-6.12-1.46-1.46-4.20-1.10-6.12.81-1.59 1.59-2.09 3.74-1.38 5.27L3.7 19.87l1.41 1.41L12 14.41l6.88 6.88 1.41-1.41L13.41 13l1.47-1.47z"/>
                                            </svg>
                                            {{ record.food_name }}
                                        </span>
                                        <span class="detail-item">
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/>
                                            </svg>
                                            {{ record.quantity }}
                                        </span>
                                        <span class="detail-item">
                                            🕐 {{ getMealTypeName(record.meal_type) }}
                                        </span>
                                    </div>
                                    <div class="nutrition-info">
                                        <span class="nutrition-item">蛋白质: {{ record.protein }}g</span>
                                        <span class="nutrition-item">碳水: {{ record.carbs }}g</span>
                                        <span class="nutrition-item">脂肪: {{ record.fat }}g</span>
                                    </div>
                                </div>
                                <RecordActions
                                    :record="record"
                                    record-type="dietrecord"
                                    @like-updated="updateLikes"
                                    @comment-added="updateComments"
                                />
                            </div>
                        </div>
                    </div>

                    <!-- 无记录状态 -->
                    <div v-if="!hasAnyRecords" class="empty-state">
                        <svg viewBox="0 0 24 24" fill="currentColor" class="empty-icon">
                            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                        </svg>
                        <h3>暂无健康记录</h3>
                        <p>{{ friendInfo.username }} 还没有分享任何健康数据</p>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import axios from 'axios'
import RecordActions from '../components/RecordActions.vue'

export default {
    name: 'FriendProfile',
    components: {
        RecordActions
    },
    data() {
        return {
            friendId: null,
            friendInfo: {},
            dashboardData: {},
            loading: true,
            errorMessage: ''
        }
    },
    computed: {
        hasAnyRecords() {
            return (this.dashboardData.recent_sleep && this.dashboardData.recent_sleep.length > 0) ||
                   (this.dashboardData.recent_exercise && this.dashboardData.recent_exercise.length > 0) ||
                   (this.dashboardData.recent_diet && this.dashboardData.recent_diet.length > 0)
        }
    },
    async mounted() {
        this.friendId = this.$route.params.id
        await this.fetchFriendData()
    },
    methods: {
        async fetchFriendData() {
            this.loading = true
            this.errorMessage = ''

            try {
                console.log('正在获取好友动态，好友ID:', this.friendId)
                const response = await axios.get(`/api/friends/${this.friendId}/`)
                console.log('获取好友动态成功:', response.data)
                console.log('运动记录数据:', response.data.recent_exercise)
                console.log('睡眠记录数据:', response.data.recent_sleep)
                console.log('饮食记录数据:', response.data.recent_diet)
                this.dashboardData = response.data
                this.friendInfo = response.data.user
            } catch (error) {
                console.error('获取好友动态失败：', error)
                console.error('错误详情:', {
                    status: error.response?.status,
                    statusText: error.response?.statusText,
                    data: error.response?.data,
                    url: error.config?.url
                })
                if (error.response?.status === 403) {
                    this.errorMessage = error.response.data.detail || '无权查看该用户的健康动态'
                } else if (error.response?.status === 404) {
                    this.errorMessage = '用户不存在'
                } else {
                    this.errorMessage = '获取好友动态失败，请重试'
                }
            } finally {
                this.loading = false
            }
        },

        updateLikes(recordId, recordType, likesCount) {
            // 更新对应记录的点赞数
            const recordsList = this.getRecordsList(recordType)
            if (recordsList) {
                const record = recordsList.find(r => r.id === recordId)
                if (record) {
                    record.likes_count = likesCount
                }
            }
        },

        updateComments(recordId, recordType, commentsCount) {
            // 更新对应记录的评论数
            const recordsList = this.getRecordsList(recordType)
            if (recordsList) {
                const record = recordsList.find(r => r.id === recordId)
                if (record) {
                    record.comments_count = commentsCount
                }
            }
        },

        getRecordsList(recordType) {
            switch (recordType) {
                case 'sleeprecord':
                    return this.dashboardData.recent_sleep
                case 'exerciserecord':
                    return this.dashboardData.recent_exercise
                case 'dietrecord':
                    return this.dashboardData.recent_diet
                default:
                    return null
            }
        },

        formatDate(dateString) {
            if (!dateString) return ''
            const date = new Date(dateString)
            return date.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            })
        },

        formatTime(timeString) {
            if (!timeString) return ''
            const date = new Date(timeString)
            return date.toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit'
            })
        },

        formatSleepDuration(sleepTime, wakeTime) {
            if (!sleepTime || !wakeTime) return ''
            const sleep = new Date(sleepTime)
            const wake = new Date(wakeTime)
            const diff = wake - sleep
            const hours = Math.floor(diff / (1000 * 60 * 60))
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
            return `${hours}小时${minutes}分钟`
        },

        getIntensityText(intensity) {
            const intensityMap = {
                'low': '低强度',
                'moderate': '中等强度',
                'high': '高强度'
            }
            return intensityMap[intensity] || intensity
        },

        getMealTypeName(mealType) {
            const mealTypeMap = {
                'breakfast': '早餐',
                'lunch': '午餐',
                'dinner': '晚餐',
                'snack': '零食'
            }
            return mealTypeMap[mealType] || mealType
        }
    }
}
</script>

<style scoped>
.friend-profile-container {
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

.loading-state, .error-state {
    text-align: center;
    padding: 4rem 2rem;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #409eff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.error-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.retry-btn {
    background: #409eff;
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.retry-btn:hover {
    background: #337ecc;
}

.friend-info-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.friend-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #409eff, #667eea);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 2rem;
    font-weight: bold;
}

.friend-details h2 {
    margin: 0 0 0.5rem 0;
    color: #333;
    font-size: 1.5rem;
}

.join-date {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
}

.health-records {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.health-records > h3 {
    margin: 0 0 2rem 0;
    color: #333;
    font-size: 1.3rem;
}

.record-section {
    margin-bottom: 2rem;
}

.record-section:last-child {
    margin-bottom: 0;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 0 1rem 0;
    color: #409eff;
    font-size: 1.1rem;
    font-weight: 600;
}

.section-icon {
    width: 20px;
    height: 20px;
}

.records-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.record-item {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1.5rem;
    border-left: 4px solid;
    transition: transform 0.2s ease;
}

.record-item:hover {
    transform: translateY(-2px);
}

.sleep-record {
    border-left-color: #9c88ff;
}

.exercise-record {
    border-left-color: #51cf66;
}

.diet-record {
    border-left-color: #ff8a65;
}

.record-content {
    margin-bottom: 1rem;
}

.record-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.record-date {
    font-weight: 600;
    color: #333;
}

.record-duration, .record-calories {
    background: #409eff;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
}

.record-details {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.detail-item {
    color: #666;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

.detail-icon {
    width: 14px;
    height: 14px;
    color: #7b1fa2;
}

.nutrition-info {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
}

.nutrition-item {
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    font-size: 0.8rem;
}

.empty-state {
    text-align: center;
    padding: 3rem;
    color: #666;
}

.empty-icon {
    width: 64px;
    height: 64px;
    margin-bottom: 1rem;
    color: #7b1fa2;
    opacity: 0.6;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .friend-info-card {
        flex-direction: column;
        text-align: center;
    }

    .record-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .record-details {
        flex-direction: column;
        gap: 0.5rem;
    }

    .nutrition-info {
        flex-direction: column;
        gap: 0.5rem;
    }
}
</style>