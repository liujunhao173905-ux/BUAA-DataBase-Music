<template>
    <div class="my-activity-container">
        <!-- 顶部导航栏 -->
        <header class="header">
            <div class="header-content">
                <button @click="$router.back()" class="back-btn">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
                    </svg>
                    返回
                </button>
                <h1>我的健康动态</h1>
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
                <button @click="fetchMyData" class="retry-btn">重试</button>
            </div>

            <!-- 我的健康动态内容 -->
            <div v-else class="my-dashboard">
                <!-- 个人基本信息 -->
                <div class="user-info-card">
                    <div class="user-avatar">
                        {{ userInfo.username?.charAt(0).toUpperCase() }}
                    </div>
                    <div class="user-details">
                        <h2>{{ userInfo.username }}</h2>
                        <p class="join-date">加入时间：{{ formatDate(userInfo.date_joined) }}</p>
                        <p class="records-summary">共{{ getTotalRecordsCount() }}条健康记录</p>
                    </div>
                </div>

                <!-- 健康记录列表 -->
                <div class="health-records">
                    <h3>最近健康记录</h3>

                    <!-- 睡眠记录卡片 -->
                    <div class="record-card sleep-card">
                        <div class="card-header" @click="toggleSection('sleep')">
                            <div class="header-left">
                                <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                                    <path d="M12 3C9.23 3 7 5.23 7 8s2.23 5 5 5 5-2.23 5-5-2.23-5-5-5zm0 8c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm0 2c-2.67 0-8 1.34-8 4v3h16v-3c0-2.66-5.33-4-8-4z"/>
                                </svg>
                                <h4>睡眠记录</h4>
                                <span class="record-count">({{ dashboardData.recent_sleep?.length || 0 }}条)</span>
                            </div>
                            <svg viewBox="0 0 24 24" fill="currentColor" class="expand-icon" :class="{ 'expanded': expandedSections.sleep }">
                                <path d="M7 10l5 5 5-5z"/>
                            </svg>
                        </div>
                        <div v-show="expandedSections.sleep" class="card-content">
                            <div v-if="!dashboardData.recent_sleep || dashboardData.recent_sleep.length === 0" class="no-data">
                                暂无睡眠记录
                            </div>
                            <div v-else class="records-list">
                                <div v-for="record in dashboardData.recent_sleep" :key="record.id" class="record-item">
                                    <div class="record-main">
                                        <div class="record-header">
                                            <h5>{{ formatDate(record.sleep_time) }}</h5>
                                            <span class="record-status">{{ record.duration }}小时</span>
                                        </div>
                                        <div class="record-details">
                                            <span class="detail-item">
                                                <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm3.5 6L12 10.5 8.5 8 12 5.5 15.5 8zM8.5 16L12 13.5 15.5 16 12 18.5 8.5 16z"/>
                                                </svg>
                                                入睡：{{ formatTime(record.sleep_time) }}
                                            </span>
                                            <span class="detail-item">
                                                <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                    <path d="M7 12l3-3 3 3-3 3z"/>
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
                    </div>

                    <!-- 运动记录卡片 -->
                    <div class="record-card exercise-card">
                        <div class="card-header" @click="toggleSection('exercise')">
                            <div class="header-left">
                                <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                                    <path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29l-1.43-1.43z"/>
                                </svg>
                                <h4>运动记录</h4>
                                <span class="record-count">({{ dashboardData.recent_exercise?.length || 0 }}条)</span>
                            </div>
                            <svg viewBox="0 0 24 24" fill="currentColor" class="expand-icon" :class="{ 'expanded': expandedSections.exercise }">
                                <path d="M7 10l5 5 5-5z"/>
                            </svg>
                        </div>
                        <div v-show="expandedSections.exercise" class="card-content">
                            <div v-if="!dashboardData.recent_exercise || dashboardData.recent_exercise.length === 0" class="no-data">
                                暂无运动记录
                            </div>
                            <div v-else class="records-list">
                                <div v-for="record in dashboardData.recent_exercise" :key="record.id" class="record-item">
                                    <div class="record-main">
                                        <div class="record-header">
                                            <h5>{{ record.exercise_type_cn }}</h5>
                                            <span class="record-status">{{ record.calories_burned }}千卡</span>
                                        </div>
                                        <div class="record-details">
                                            <span class="detail-item">
                                                <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                                </svg>
                                                时长：{{ record.duration_minutes }}分钟
                                            </span>
                                            <span class="detail-item">
                                                <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
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
                    </div>

                    <!-- 饮食记录卡片 -->
                    <div class="record-card diet-card">
                        <div class="card-header" @click="toggleSection('diet')">
                            <div class="header-left">
                                <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                                    <path d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z" />
                                </svg>
                                <h4>饮食记录</h4>
                                <span class="record-count">({{ dashboardData.recent_diet?.length || 0 }}条)</span>
                            </div>
                            <svg viewBox="0 0 24 24" fill="currentColor" class="expand-icon" :class="{ 'expanded': expandedSections.diet }">
                                <path d="M7 10l5 5 5-5z"/>
                            </svg>
                        </div>
                        <div v-show="expandedSections.diet" class="card-content">
                            <div v-if="!dashboardData.recent_diet || dashboardData.recent_diet.length === 0" class="no-data">
                                暂无饮食记录
                            </div>
                            <div v-else class="records-list">
                                <div v-for="record in dashboardData.recent_diet" :key="record.id" class="record-item">
                                    <div class="record-main">
                                        <div class="record-header">
                                            <h5>{{ record.food_name }}</h5>
                                            <span class="record-status">{{ record.calories }}千卡</span>
                                        </div>
                                        <div class="record-details">
                                            <span class="detail-item">
                                                <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                                </svg>
                                                数量：{{ record.quantity }}
                                            </span>
                                            <span class="detail-item">
                                                <svg viewBox="0 0 24 24" fill="currentColor" class="detail-icon">
                                                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                                                </svg>
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
                    </div>

                    <!-- 无记录状态 -->
                    <div v-if="!hasAnyRecords" class="empty-state">
                        <svg viewBox="0 0 24 24" fill="currentColor" class="empty-icon">
                            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                        </svg>
                        <h3>暂无健康记录</h3>
                        <p>开始记录您的健康数据吧！</p>
                        <div class="quick-actions">
                            <button @click="$router.push('/sleep')" class="quick-btn">记录睡眠</button>
                            <button @click="$router.push('/exercise')" class="quick-btn">记录运动</button>
                            <button @click="$router.push('/diet')" class="quick-btn">记录饮食</button>
                        </div>
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
    name: 'MyActivity',
    components: {
        RecordActions
    },
    data() {
        return {
            userInfo: {},
            dashboardData: {},
            loading: true,
            errorMessage: '',
            expandedSections: {
                sleep: false,
                exercise: false,
                diet: false
            }
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
        await this.fetchMyData()
    },
    methods: {
        toggleSection(sectionName) {
            this.expandedSections[sectionName] = !this.expandedSections[sectionName]
        },

        async fetchMyData() {
            this.loading = true
            this.errorMessage = ''

            try {
                // 获取用户自己的数据
                console.log('正在获取我的健康动态数据')

                // 获取用户基本信息
                const userResponse = await axios.get('/api/profile/my_profile/')
                this.userInfo = {
                    username: localStorage.getItem('username'),
                    date_joined: userResponse.data.created_at || new Date().toISOString()
                }

                // 获取最近的健康记录，并为每条记录加载社交数据
                const [sleepResponse, exerciseResponse, dietResponse] = await Promise.all([
                    axios.get('/api/sleep/recent/').catch(() => ({ data: [] })),
                    axios.get('/api/exercise/recent/').catch(() => ({ data: [] })),
                    axios.get('/api/diet/recent/').catch(() => ({ data: [] }))
                ])

                // 为每条记录加载社交数据（点赞数、评论数等）
                const enrichedSleep = await this.enrichRecordsWithSocialData(sleepResponse.data, 'sleeprecord')
                const enrichedExercise = await this.enrichRecordsWithSocialData(exerciseResponse.data, 'exerciserecord')
                const enrichedDiet = await this.enrichRecordsWithSocialData(dietResponse.data, 'dietrecord')

                this.dashboardData = {
                    recent_sleep: enrichedSleep,
                    recent_exercise: enrichedExercise,
                    recent_diet: enrichedDiet
                }

                console.log('获取我的健康动态成功:', this.dashboardData)
            } catch (error) {
                console.error('获取我的健康动态失败：', error)
                this.errorMessage = '获取健康动态失败，请重试'
            } finally {
                this.loading = false
            }
        },

        async enrichRecordsWithSocialData(records, recordType) {
            // 为每条记录添加社交数据
            const enrichedRecords = []

            // 获取ContentType ID的映射
            const contentTypeMapping = {
                'sleeprecord': null,
                'exerciserecord': null,
                'dietrecord': null
            }

            // 尝试从后端获取ContentType ID
            try {
                const contentTypesResponse = await axios.get('/api/debug/content-types/')
                const contentTypes = contentTypesResponse.data

                // 直接使用返回的映射对象
                Object.assign(contentTypeMapping, contentTypes)

            } catch (error) {
                console.warn('无法获取ContentType映射，将跳过社交数据加载:', error)
                // 如果无法获取ContentType映射，返回原始记录
                return records.map(record => ({
                    ...record,
                    likes_count: 0,
                    comments_count: 0,
                    social_data: { likes: [], comments: [] }
                }))
            }

            const contentTypeId = contentTypeMapping[recordType]
            if (!contentTypeId) {
                console.warn(`无法找到${recordType}的ContentType ID`)
                return records.map(record => ({
                    ...record,
                    likes_count: 0,
                    comments_count: 0,
                    social_data: { likes: [], comments: [] }
                }))
            }

            for (const record of records) {
                try {
                    // 获取点赞数据
                    const likesResponse = await axios.get('/api/likes/', {
                        params: {
                            content_type: contentTypeId,
                            object_id: record.id
                        }
                    })

                    // 获取评论数据（包括回复）
                    const commentsResponse = await axios.get('/api/comments/', {
                        params: {
                            content_type: contentTypeId,
                            object_id: record.id
                        }
                    })

                    // 添加社交数据到记录中
                    const enrichedRecord = {
                        ...record,
                        likes_count: (likesResponse.data.results || likesResponse.data || []).length,
                        comments_count: this.countCommentsWithReplies(commentsResponse.data.results || commentsResponse.data || []),
                        social_data: {
                            likes: likesResponse.data.results || likesResponse.data || [],
                            comments: commentsResponse.data.results || commentsResponse.data || []
                        }
                    }

                    enrichedRecords.push(enrichedRecord)
                } catch (error) {
                    console.error(`获取记录${record.id}的社交数据失败:`, error)
                    // 如果获取社交数据失败，仍然添加记录但不包含社交数据
                    enrichedRecords.push({
                        ...record,
                        likes_count: 0,
                        comments_count: 0,
                        social_data: { likes: [], comments: [] }
                    })
                }
            }

            return enrichedRecords
        },

        countCommentsWithReplies(comments) {
            // 递归计算评论总数（包括回复）
            let count = comments.length
            for (const comment of comments) {
                if (comment.replies && comment.replies.length > 0) {
                    count += this.countCommentsWithReplies(comment.replies)
                }
            }
            return count
        },        updateLikes(recordId, recordType, likesCount) {
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

        getTotalRecordsCount() {
            let total = 0
            if (this.dashboardData.recent_sleep) total += this.dashboardData.recent_sleep.length
            if (this.dashboardData.recent_exercise) total += this.dashboardData.recent_exercise.length
            if (this.dashboardData.recent_diet) total += this.dashboardData.recent_diet.length
            return total
        },

        formatDate(dateString) {
            const date = new Date(dateString)
            return date.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            })
        },

        formatTime(timeString) {
            const date = new Date(timeString)
            return date.toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit'
            })
        },

        getIntensityText(intensity) {
            const intensityMap = {
                'low': '轻度',
                'moderate': '中度',
                'high': '高强度'
            }
            return intensityMap[intensity] || intensity
        },

        getMealTypeName(mealType) {
            const mealTypeMap = {
                'breakfast': '早餐',
                'lunch': '午餐',
                'dinner': '晚餐',
                'snack': '加餐'
            }
            return mealTypeMap[mealType] || mealType
        }
    }
}
</script>

<style scoped>
/* 复用FriendProfile的所有样式，只修改颜色主题 */
.my-activity-container {
    min-height: 100vh;
    background: #f5f7fa;
    display: flex;
    flex-direction: column;
}

.header {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
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
    color: #667eea;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 6px;
    transition: background-color 0.2s;
}

.back-btn:hover {
    background: rgba(102, 126, 234, 0.1);
}

.back-btn svg {
    width: 20px;
    height: 20px;
}

.header h1 {
    color: #333;
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
}

.main-content {
    flex: 1;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    width: 100%;
}

.loading-state, .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    color: white;
    text-align: center;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top: 4px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
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
    background: white;
    color: #667eea;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    margin-top: 1rem;
    transition: all 0.2s;
}

.retry-btn:hover {
    background: #f8f9ff;
    transform: translateY(-1px);
}

.my-dashboard {
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.user-info-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.user-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: bold;
    border: 3px solid rgba(255, 255, 255, 0.3);
}

.user-details h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.8rem;
    font-weight: 600;
}

.join-date, .records-summary {
    margin: 0.25rem 0;
    opacity: 0.9;
    font-size: 0.9rem;
}

.health-records {
    padding: 2rem;
}

.health-records h3 {
    color: #333;
    margin: 0 0 1.5rem 0;
    font-size: 1.3rem;
    font-weight: 600;
}

.record-section {
    margin-bottom: 2rem;
}

/* 卡片样式 */
.record-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
    overflow: hidden;
    transition: all 0.3s ease;
    border-left: 4px solid #e9ecef;
}

.record-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

/* 睡眠记录主题色 - 紫色 */
.sleep-card {
    border-left-color: #9b59b6;
}

.sleep-card .card-header {
    background: rgba(155, 89, 182, 0.05);
    border-bottom-color: rgba(155, 89, 182, 0.1);
}

.sleep-card .section-icon {
    color: #9b59b6;
}

.sleep-card .header-left h4 {
    color: #9b59b6;
}

.sleep-card .record-status {
    background: #9b59b6;
}

.sleep-card .detail-icon {
    color: #9b59b6;
}

/* 运动记录主题色 - 绿色 */
.exercise-card {
    border-left-color: #27ae60;
}

.exercise-card .card-header {
    background: rgba(39, 174, 96, 0.05);
    border-bottom-color: rgba(39, 174, 96, 0.1);
}

.exercise-card .section-icon {
    color: #27ae60;
}

.exercise-card .header-left h4 {
    color: #27ae60;
}

.exercise-card .record-status {
    background: #27ae60;
}

.exercise-card .detail-icon {
    color: #27ae60;
}

/* 饮食记录主题色 - 橙色 */
.diet-card {
    border-left-color: #e67e22;
}

.diet-card .card-header {
    background: rgba(230, 126, 34, 0.05);
    border-bottom-color: rgba(230, 126, 34, 0.1);
}

.diet-card .section-icon {
    color: #e67e22;
}

.diet-card .header-left h4 {
    color: #e67e22;
}

.diet-card .record-status {
    background: #e67e22;
}

.diet-card .detail-icon {
    color: #e67e22;
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem;
    background: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
    cursor: pointer;
    transition: all 0.3s ease;
}

.card-header:hover {
    background: #e9ecef;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.header-left h4 {
    margin: 0;
    color: #2c3e50;
    font-size: 1.1rem;
    font-weight: 600;
}

.record-count {
    color: #6c757d;
    font-size: 0.9rem;
    font-weight: 400;
}

.expand-icon {
    width: 20px;
    height: 20px;
    color: #6c757d;
    transition: transform 0.3s ease;
}

.expand-icon.expanded {
    transform: rotate(180deg);
}

.card-content {
    padding: 0;
}

.no-data {
    text-align: center;
    padding: 2rem;
    color: #6c757d;
    font-style: italic;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #667eea;
    margin: 0 0 1rem 0;
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
}

.record-item {
    border-bottom: 1px solid #f0f0f0;
    padding: 1.5rem;
    transition: all 0.2s ease;
}

.record-item:last-child {
    border-bottom: none;
}

.record-item:hover {
    background: #f8f9fa;
}

.record-main {
    margin-bottom: 1rem;
}

.record-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
}

.record-header h5 {
    margin: 0;
    color: #333;
    font-size: 1rem;
    font-weight: 600;
}

.record-status {
    background: #667eea;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
}

.record-details {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
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
    color: #667eea;
}

.nutrition-info {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
    flex-wrap: wrap;
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
    padding: 4rem 2rem;
    color: #666;
}

.empty-icon {
    width: 64px;
    height: 64px;
    margin-bottom: 1rem;
    color: #667eea;
    opacity: 0.6;
}

.empty-state h3 {
    color: #333;
    margin-bottom: 0.5rem;
}

.quick-actions {
    margin-top: 2rem;
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.quick-btn {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s;
}

.quick-btn:hover {
    background: #5a6fd8;
    transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
    .main-content {
        padding: 1rem;
    }

    .user-info-card {
        flex-direction: column;
        text-align: center;
        padding: 1.5rem;
    }

    .user-avatar {
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
    }

    .record-details {
        flex-direction: column;
        gap: 0.5rem;
    }

    .quick-actions {
        flex-direction: column;
        align-items: center;
    }

    .quick-btn {
        width: 200px;
    }
}
</style>
