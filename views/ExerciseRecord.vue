<template>
    <div class="exercise-record-container">
        <header class="report-header">
            <h1>
                <svg viewBox="0 0 24 24" fill="currentColor" class="header-icon">
                    <path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z"/>
                </svg>
                运动记录
            </h1>
            <button @click="$router.push('/dashboard')" class="back-btn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.42-1.41L7.83 13H20v-2z"/>
                </svg>
                返回首页
            </button>
        </header>

        <main class="main-content">
            <!-- 记录表单 -->
            <div class="record-form-card">
                <h2>
                    <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                        <path
                            d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z" />
                    </svg>
                    记录今日运动
                </h2>

                <form @submit.prevent="submitExercise" class="exercise-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label>运动类型</label>
                            <div class="input-with-suggestions">
                                <input v-model="exerciseData.exercise_type_cn" type="text"
                                    placeholder="输入运动类型，如：跑步、游泳、篮球等" required @input="filterExerciseTypes"
                                    @focus="showSuggestions = true" />
                                <div v-if="showSuggestions && filteredExerciseTypes.length > 0" class="suggestions">
                                    <div v-for="type in filteredExerciseTypes" :key="type.value"
                                        @click="selectExerciseType(type)" class="suggestion-item">
                                        {{ type.label }}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>运动日期</label>
                            <input v-model="exerciseData.record_date" type="date" required :max="getCurrentDate()" />
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>运动时长（分钟）</label>
                            <input v-model.number="exerciseData.duration_minutes" type="number" min="1" max="600"
                                required placeholder="输入运动时长" />
                        </div>
                        <div class="form-group">
                            <label>运动强度</label>
                            <select v-model="exerciseData.intensity">
                                <option value="low">低强度</option>
                                <option value="moderate">中等强度</option>
                                <option value="high">高强度</option>
                            </select>
                        </div>
                    </div>

                    <div class="calories-display" v-if="estimatedCalories">
                        <p>预计消耗热量：<span class="calories-value">{{ estimatedCalories }} 卡路里</span></p>
                        <small>*基于运动类型和时长的估算值</small>
                    </div>

                    <div class="form-group">
                        <label>运动备注（可选）</label>
                        <textarea v-model="exerciseData.notes" placeholder="记录运动感受、地点或其他相关信息..." rows="3"></textarea>
                    </div>

                    <div class="form-actions">
                        <button v-if="isEditMode" type="button" @click="cancelEdit" class="cancel-btn">
                            取消编辑
                        </button>
                        <button type="submit" :disabled="loading" class="submit-btn">
                            {{ loading ? '保存中...' : (isEditMode ? '更新运动记录' : '保存运动记录') }}
                        </button>
                    </div>
                </form>
            </div>

            <!-- 历史记录 -->
            <div class="history-card">
                <div class="history-header">
                    <h2>
                        <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                            <path
                                d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z" />
                        </svg>
                        最近运动记录
                    </h2>
                    <button @click="showAllHistory" class="view-all-btn">
                        查看全部
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M9 5l7 7-7 7" />
                        </svg>
                    </button>
                </div>

                <div v-if="loading" class="loading">
                    <p>加载中...</p>
                </div>

                <div v-else-if="exerciseHistory.length === 0" class="no-data">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path
                            d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z" />
                    </svg>
                    <p>暂无运动记录</p>
                </div>

                <div v-else class="history-list">
                    <div v-for="record in exerciseHistory" :key="record.id" class="history-item">
                        <div class="record-date">
                            <span class="date-text">{{ formatDate(record.record_datetime) }}</span>
                            <span class="weekday">{{ getWeekday(record.record_datetime) }}</span>
                        </div>

                        <div class="record-details">
                            <div class="exercise-info">
                                <span class="exercise-type">{{ record.exercise_type_cn }}</span>
                                <span class="intensity" :class="getIntensityClass(record.intensity)">
                                    {{ getIntensityText(record.intensity) }}
                                </span>
                            </div>
                            <div class="duration-calories">
                                <span class="duration">{{ record.duration_minutes }}分钟</span>
                                <span class="calories">{{ Math.round(record.calories_burned) }}卡路里</span>
                            </div>
                            <div v-if="record.notes" class="notes">{{ record.notes }}</div>
                        </div>

                        <div class="record-actions">
                            <button @click="editRecord(record)" class="edit-btn">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                                </svg>
                            </button>
                            <button @click="deleteRecord(record.id)" class="delete-btn">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 运动统计 -->
            <div class="stats-card">
                <h2>
                    <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                        <path
                            d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" />
                    </svg>
                    本周运动统计
                </h2>

                <div class="stats-grid">
                    <div class="stat-item">
                        <h3>总运动时间</h3>
                        <p class="stat-value">{{ weeklyStats.totalDuration }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>总消耗热量</h3>
                        <p class="stat-value">{{ weeklyStats.totalCalories }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>运动天数</h3>
                        <p class="stat-value">{{ weeklyStats.exerciseDays }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>平均强度</h3>
                        <p class="stat-value">{{ weeklyStats.averageIntensity }}</p>
                    </div>
                </div>
            </div>
        </main>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="error-message">
            <span>{{ errorMessage }}</span>
            <button @click="errorMessage = ''" class="close-btn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
            </button>
        </div>

        <!-- 成功提示 -->
        <div v-if="successMessage" class="success-message">
            <span>{{ successMessage }}</span>
            <button @click="successMessage = ''" class="close-btn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
            </button>
        </div>

        <!-- 历史记录管理弹窗 -->
        <HistoryManager
            :visible="showHistoryManager"
            recordType="exercise"
            @close="showHistoryManager = false"
            @edit="handleEditFromHistory"
            @deleted="handleRecordDeleted"
            @error="handleError"
        />

        <!-- 饮食推荐模态框 -->
        <div v-if="showDietRecommendations" class="diet-recommendations-modal">
            <div class="modal-overlay" @click="closeDietRecommendations"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h3>
                        基于运动的饮食建议
                    </h3>
                    <button @click="closeDietRecommendations" class="close-btn">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                        </svg>
                    </button>
                </div>

                <div class="modal-body">
                    <div v-if="loadingRecommendations" class="loading-section">
                    <div class="loading-spinner"></div>
                    <p>正在生成个性化饮食建议...</p>
                </div>

                <div v-else-if="dietRecommendations" class="recommendations-content">
                    <!-- 运动摘要 -->
                    <div class="exercise-summary">
                        <h4>您刚完成的运动：</h4>
                        <div class="summary-stats">
                            <div class="stat-item">
                                <span class="stat-label">运动类型</span>
                                <span class="stat-value">{{ dietRecommendations.exercise_summary?.type || '未知' }}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">运动时长</span>
                                <span class="stat-value">{{ dietRecommendations.exercise_summary?.duration_minutes || 0 }}分钟</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">消耗热量</span>
                                <span class="stat-value">{{ Math.round(dietRecommendations.exercise_summary?.calories_burned || 0) }}卡路里</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">建议补充</span>
                                <span class="stat-value recommend">{{ dietRecommendations.recommended_calories || 0 }}卡路里</span>
                            </div>
                        </div>
                    </div>

                    <!-- 饮食推荐分类 -->
                    <div class="recommendations-sections">
                        <!-- 立即食用推荐 -->
                        <div v-if="dietRecommendations.recommendations && dietRecommendations.recommendations.immediate && dietRecommendations.recommendations.immediate.length > 0" class="recommendation-category">
                            <h5>
                                <svg viewBox="0 0 24 24" fill="currentColor" class="category-icon">
                                    <path d="M7 2v11h3v9l7-12h-4l4-8z"/>
                                </svg>
                                运动后立即补充
                            </h5>
                            <div class="recommendation-list">
                                <div v-for="(item, index) in dietRecommendations.recommendations.immediate" :key="index" class="recommendation-item">
                                    <div class="item-header">
                                        <span class="item-name">{{ item.name }}</span>
                                    </div>
                                    <p class="item-description">{{ item.description }}</p>
                                    <div class="item-examples">
                                        <span v-for="(example, idx) in (item.examples || [])" :key="idx" class="example-tag">
                                            {{ example }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 下一餐推荐 -->
                        <div v-if="dietRecommendations.recommendations && dietRecommendations.recommendations.next_meal && dietRecommendations.recommendations.next_meal.length > 0" class="recommendation-category">
                            <h5>
                                <svg viewBox="0 0 24 24" fill="currentColor" class="category-icon">
                                    <path d="M8.1 13.34l2.83-2.83L3.91 3.5c-1.56 1.56-1.56 4.09 0 5.66l4.19 4.18zm6.78-1.81c1.53.71 3.68.21 5.27-1.38 1.91-1.91 2.28-4.65.81-6.12-1.46-1.46-4.20-1.10-6.12.81-1.59 1.59-2.09 3.74-1.38 5.27L3.7 19.87l1.41 1.41L12 14.41l6.88 6.88 1.41-1.41L13.41 13l1.47-1.47z"/>
                                </svg>
                                下一餐建议
                            </h5>
                            <div class="recommendation-list">
                                <div v-for="(item, index) in dietRecommendations.recommendations.next_meal" :key="index" class="recommendation-item">
                                    <div class="item-header">
                                        <span class="item-name">{{ item.name }}</span>
                                    </div>
                                    <p class="item-description">{{ item.description }}</p>
                                    <div class="item-examples">
                                        <span v-for="(example, idx) in (item.examples || [])" :key="idx" class="example-tag">
                                            {{ example }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 一般建议 -->
                        <div v-if="dietRecommendations.recommendations && dietRecommendations.recommendations.general && dietRecommendations.recommendations.general.length > 0" class="recommendation-category">
                            <h5>
                                <svg viewBox="0 0 24 24" fill="currentColor" class="category-icon">
                                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                </svg>
                                营养提醒
                            </h5>
                            <div class="recommendation-list">
                                <div v-for="(item, index) in dietRecommendations.recommendations.general" :key="index" class="recommendation-item">
                                    <div class="item-header">
                                        <span class="item-name">{{ item.name }}</span>
                                    </div>
                                    <p class="item-description">{{ item.description }}</p>
                                    <div class="item-examples">
                                        <span v-for="(example, idx) in (item.examples || [])" :key="idx" class="example-tag">
                                            {{ example }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 操作按钮 -->
                    <div class="modal-actions">
                        <button @click="$router.push('/diet')" class="action-btn primary">
                            按推荐记录饮食
                        </button>
                        <button @click="closeDietRecommendations" class="action-btn secondary">
                            已了解
                        </button>
                    </div>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import HistoryManager from '../components/HistoryManager.vue';

export default {
    name: 'ExerciseRecord',
    components: {
        HistoryManager
    },
    data() {
        return {
            exerciseData: {
                exercise_type_cn: '',
                record_date: '',
                duration_minutes: null,
                intensity: 'moderate',
                notes: ''
            },
            exerciseHistory: [],
            loading: false,
            errorMessage: '',
            successMessage: '',
            // 编辑模式状态管理
            isEditMode: false,
            editingRecordId: null,
            showSuggestions: false,
            filteredExerciseTypes: [],
            exerciseTypes: [
                { value: 'running', label: '跑步' },
                { value: 'walking', label: '步行' },
                { value: 'cycling', label: '骑行' },
                { value: 'swimming', label: '游泳' },
                { value: 'basketball', label: '篮球' },
                { value: 'football', label: '足球' },
                { value: 'badminton', label: '羽毛球' },
                { value: 'tennis', label: '网球' },
                { value: 'yoga', label: '瑜伽' },
                { value: 'fitness', label: '健身' },
                { value: 'dancing', label: '舞蹈' },
                { value: 'climbing', label: '爬山' },
                { value: 'boxing', label: '拳击' }
            ],
            showHistoryManager: false,
            // 饮食推荐相关
            showDietRecommendations: false,
            dietRecommendations: null,
            loadingRecommendations: false
        };
    },
    computed: {
        estimatedCalories() {
            return 0; // 后端API会自动计算卡路里
        },

        weeklyStats() {
            if (this.exerciseHistory.length === 0) {
                return {
                    totalDuration: '0分钟',
                    totalCalories: '0卡路里',
                    exerciseDays: '0天',
                    averageIntensity: '无数据'
                };
            }

            // 获取本周的开始（周一）和结束（周日）
            const today = new Date();
            const dayOfWeek = today.getDay(); // 0是周日，1-6是周一到周六
            const daysSinceMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

            const weekStart = new Date(today);
            weekStart.setDate(today.getDate() - daysSinceMonday);
            weekStart.setHours(0, 0, 0, 0);

            const weekEnd = new Date(weekStart);
            weekEnd.setDate(weekStart.getDate() + 6);
            weekEnd.setHours(23, 59, 59, 999);

            // 过滤本周的记录（周一到周日）
            const weeklyRecords = this.exerciseHistory.filter(record => {
                const recordDate = new Date(record.record_datetime);
                return recordDate >= weekStart && recordDate <= weekEnd;
            });

            if (weeklyRecords.length === 0) {
                return {
                    totalDuration: '0分钟',
                    totalCalories: '0卡路里',
                    exerciseDays: '0天',
                    averageIntensity: '无数据'
                };
            }

            const totalMinutes = weeklyRecords.reduce((sum, record) => sum + record.duration_minutes, 0);
            const totalCalories = weeklyRecords.reduce((sum, record) => sum + record.calories_burned, 0);

            // 计算不同日期的天数
            const uniqueDates = new Set(weeklyRecords.map(record => record.record_datetime?.split('T')[0]));
            const exerciseDays = uniqueDates.size;

            // 计算平均强度
            const intensityValues = { low: 1, moderate: 2, high: 3 };
            const avgIntensityValue = weeklyRecords.reduce((sum, record) =>
                sum + (intensityValues[record.intensity] || 2), 0) / weeklyRecords.length;

            let avgIntensityText = '中等强度';
            if (avgIntensityValue <= 1.5) avgIntensityText = '低强度';
            else if (avgIntensityValue >= 2.5) avgIntensityText = '高强度';

            return {
                totalDuration: `${totalMinutes}分钟`,
                totalCalories: `${Math.round(totalCalories)}卡路里`,
                exerciseDays: `${exerciseDays}天`,
                averageIntensity: avgIntensityText
            };
        }
    },
    async mounted() {
        await this.fetchExerciseHistory();
        this.setDefaultDate();
        // 点击外部关闭建议
        document.addEventListener('click', this.handleClickOutside);
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    methods: {
        async fetchExerciseHistory() {
            try {
                const response = await axios.get('/api/exercise/recent/');
                this.exerciseHistory = response.data.slice(0, 7);
            } catch (error) {
                console.error('获取运动记录失败：', error);
                this.exerciseHistory = [];
            }
        },

        filterExerciseTypes() {
            const input = this.exerciseData.exercise_type_cn.toLowerCase();
            this.filteredExerciseTypes = this.exerciseTypes.filter(type =>
                type.label.toLowerCase().includes(input)
            );
        },

        selectExerciseType(type) {
            this.exerciseData.exercise_type_cn = type.label;
            this.showSuggestions = false;
            this.filteredExerciseTypes = [];
        },

        handleClickOutside(event) {
            if (!this.$el.querySelector('.input-with-suggestions').contains(event.target)) {
                this.showSuggestions = false;
            }
        },

        async submitExercise() {
            if (!this.exerciseData.exercise_type_cn || !this.exerciseData.duration_minutes) {
                this.errorMessage = '请填写完整的运动信息';
                return;
            }

            this.loading = true;
            this.errorMessage = '';

            try {
                // 准备提交数据，将record_date转换为record_datetime
                const submitData = {
                    ...this.exerciseData,
                    record_datetime: this.exerciseData.record_date + 'T00:00:00Z'
                };
                delete submitData.record_date; // 删除record_date字段

                let exerciseRecordId = null;

                if (this.isEditMode && this.editingRecordId) {
                    // 编辑模式：更新现有记录
                    await axios.put(`/api/exercise/${this.editingRecordId}/`, submitData);
                    this.successMessage = '运动记录更新成功！';
                    exerciseRecordId = this.editingRecordId;
                } else {
                    // 新增模式：创建新记录
                    const response = await axios.post('/api/exercise/', submitData);
                    this.successMessage = '运动记录保存成功！';
                    exerciseRecordId = response.data.id;
                }

                // 检查是否是当日记录，如果是则获取饮食推荐
                const recordDate = this.exerciseData.record_date;
                const today = new Date().toISOString().split('T')[0];

                if (recordDate === today && exerciseRecordId) {
                    await this.fetchDietRecommendations(exerciseRecordId);
                }

                // 重置表单和编辑状态
                this.resetForm();

                // 刷新历史记录
                await this.fetchExerciseHistory();

                // 清除成功提示
                setTimeout(() => {
                    this.successMessage = '';
                }, 3000);

            } catch (error) {
                console.error('保存运动记录失败：', error);
                if (error.response?.data?.detail) {
                    this.errorMessage = error.response.data.detail;
                } else {
                    this.errorMessage = '保存失败，请重试';
                }
            } finally {
                this.loading = false;
            }
        },

        async deleteRecord(recordId) {
            if (!confirm('确定要删除这条运动记录吗？')) return;

            try {
                await axios.delete(`/api/exercise/${recordId}/`);
                this.successMessage = '运动记录删除成功！';
                await this.fetchExerciseHistory();

                setTimeout(() => {
                    this.successMessage = '';
                }, 3000);

            } catch (error) {
                console.error('删除运动记录失败：', error);
                this.errorMessage = '删除失败，请重试';
            }
        },

        editRecord(record) {
            // 设置编辑模式
            this.isEditMode = true;
            this.editingRecordId = record.id;

            // 填充表单数据
            this.exerciseData = {
                exercise_type_cn: record.exercise_type_cn,
                record_date: this.formatDateForInput(record.record_datetime),
                duration_minutes: record.duration_minutes,
                intensity: record.intensity || 'moderate',
                notes: record.notes || ''
            };

            // 滚动到表单
            document.querySelector('.record-form-card').scrollIntoView({
                behavior: 'smooth'
            });
        },

        resetForm() {
            // 重置表单数据
            this.exerciseData = {
                exercise_type_cn: '',
                record_date: this.getCurrentDate(),
                duration_minutes: null,
                intensity: 'moderate',
                notes: ''
            };
            // 重置编辑状态
            this.isEditMode = false;
            this.editingRecordId = null;
        },

        cancelEdit() {
            this.resetForm();
        },

        setDefaultDate() {
            const today = new Date();
            this.exerciseData.record_date = today.toISOString().split('T')[0];
        },

        getCurrentDate() {
            return new Date().toISOString().split('T')[0];
        },

        formatDateForInput(dateString) {
            return new Date(dateString).toISOString().split('T')[0];
        },

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('zh-CN', {
                month: 'short',
                day: 'numeric'
            });
        },

        formatTime(dateString) {
            const date = new Date(dateString);
            return date.toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit'
            });
        },

        getWeekday(dateString) {
            const date = new Date(dateString);
            const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
            return `周${weekdays[date.getDay()]}`;
        },

        getIntensityText(intensity) {
            const map = { low: '低强度', moderate: '中等强度', high: '高强度' };
            return map[intensity] || '中等强度';
        },

        getIntensityClass(intensity) {
            if (intensity === 'high') return 'intensity-high';
            if (intensity === 'low') return 'intensity-low';
            return 'intensity-moderate';
        },

        // 历史记录管理相关方法
        showAllHistory() {
            this.showHistoryManager = true;
        },

        handleEditFromHistory(record) {
            // 填充表单数据进行编辑
            this.exerciseData = {
                exercise_type_cn: record.exercise_type_cn,
                record_date: this.formatDateForInput(record.record_datetime),
                duration_minutes: record.duration_minutes,
                intensity: record.intensity,
                notes: record.notes || ''
            };
            this.isEditMode = true;
            this.editingRecordId = record.id;
            // 滚动到表单顶部
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },

        handleRecordDeleted(recordId) {
            // 从本地历史记录中移除已删除的记录
            this.exerciseHistory = this.exerciseHistory.filter(record => record.id !== recordId);
            this.successMessage = '记录已删除';
            setTimeout(() => {
                this.successMessage = '';
            }, 3000);
        },

        handleError(message) {
            this.errorMessage = message;
            setTimeout(() => {
                this.errorMessage = '';
            }, 5000);
        },

        formatDateForInput(dateTimeString) {
            if (!dateTimeString) return '';
            const date = new Date(dateTimeString);
            return date.toISOString().split('T')[0];
        },

        async fetchDietRecommendations(exerciseRecordId) {
            this.loadingRecommendations = true;
            this.dietRecommendations = null;

            try {
                const response = await axios.get(`/api/exercise/${exerciseRecordId}/diet_recommendations/`);
                this.dietRecommendations = response.data;
                this.showDietRecommendations = true;
            } catch (error) {
                console.error('获取饮食推荐失败：', error);
                if (error.response?.status === 400) {
                    // 不是当天的记录，静默处理
                    console.log('运动记录不是当天的，无法获取饮食推荐');
                } else {
                    this.errorMessage = '获取饮食推荐失败，请稍后重试';
                }
            } finally {
                this.loadingRecommendations = false;
            }
        },

        closeDietRecommendations() {
            this.showDietRecommendations = false;
            this.dietRecommendations = null;
        }
    }
};
</script>

<style scoped>
.exercise-record-container {
    min-height: 100vh;
    background: #f5f7fa;
}

/* 头部样式 */
.report-header {
    background: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.report-header h1 {
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
    color: #27ae60; /* 绿色 - 运动相关 */
}

.back-btn {
    background: #27ae60;
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
    background: #229954;
}

.back-btn svg {
    width: 16px;
    height: 16px;
}

.main-content {
    max-width: 1000px;
    margin: 0 auto;
    padding: 30px 20px;
    display: grid;
    gap: 30px;
    grid-template-columns: 1fr 1fr;
}

.record-form-card {
    grid-column: 1 / -1;
    background: white;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.history-card,
.stats-card {
    background: white;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.history-header h2 {
    margin: 0;
}

.view-all-btn {
    background: #27ae60;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    gap: 6px;
}

.view-all-btn:hover {
    background: #229954;
}

.view-all-btn svg {
    width: 14px;
    height: 14px;
}

.record-form-card h2,
.history-card h2,
.stats-card h2 {
    color: #2c3e50;
    margin: 0 0 24px 0;
    font-size: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-icon {
    width: 20px;
    height: 20px;
    color: #27ae60;
}

.exercise-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    color: #555;
    font-weight: 600;
    margin-bottom: 8px;
    font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.3s;
    box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #27ae60;
    box-shadow: 0 0 0 2px rgba(39, 174, 96, 0.2);
}

.input-with-suggestions {
    position: relative;
    width: 100%;
}

.input-with-suggestions input {
    width: 100%;
    box-sizing: border-box;
}

.suggestions {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #ddd;
    border-top: none;
    border-radius: 0 0 6px 6px;
    max-height: 200px;
    overflow-y: auto;
    z-index: 10;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.suggestion-item {
    padding: 10px 12px;
    cursor: pointer;
    transition: background-color 0.2s;
    border-bottom: 1px solid #f0f0f0;
}

.suggestion-item:hover {
    background: #f5f5f5;
}

.suggestion-item:last-child {
    border-bottom: none;
}

.calories-display {
    background: #f3e5f5;
    padding: 16px;
    border-radius: 6px;
    text-align: center;
}

.calories-value {
    font-weight: bold;
    color: #27ae60;
    font-size: 18px;
}

.calories-display small {
    display: block;
    margin-top: 4px;
    color: #666;
}

.form-actions {
    display: flex;
    gap: 12px;
    align-items: center;
}

.submit-btn {
    background: #27ae60;
    color: white;
    border: none;
    padding: 14px 28px;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
    flex: 1;
}

.submit-btn:hover:not(:disabled) {
    background: #229954;
}

.submit-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.cancel-btn {
    padding: 14px 20px;
    background: #f5f5f5;
    color: #666;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.cancel-btn:hover {
    background: #e9e9e9;
    border-color: #ccc;
}

.loading,
.no-data {
    text-align: center;
    padding: 40px;
    color: #666;
}

.no-data svg {
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}

.history-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.history-item {
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    padding: 16px;
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 16px;
    align-items: center;
    transition: box-shadow 0.3s;
}

.history-item:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.record-date {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 60px;
}

.date-text {
    font-weight: bold;
    color: #2c3e50;
}

.weekday {
    font-size: 12px;
    color: #666;
}

.record-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.exercise-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.exercise-type {
    font-weight: bold;
    color: #2c3e50;
}

.intensity {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
}

.intensity-low {
    background: #e3f2fd;
    color: #1976d2;
}

.intensity-moderate {
    background: #fff3e0;
    color: #f57c00;
}

.intensity-high {
    background: #ffebee;
    color: #d32f2f;
}

.duration-calories {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
}

.duration {
    color: #27ae60;
    font-weight: bold;
}

.calories {
    color: #666;
}

.notes {
    font-size: 12px;
    color: #666;
    font-style: italic;
}

.record-actions {
    display: flex;
    gap: 8px;
}

.edit-btn,
.delete-btn {
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s;
}

.edit-btn {
    background: #e8f5e8;
    color: #27ae60;
}

.edit-btn:hover {
    background: #d4edd4;
}

.delete-btn {
    background: #ffebee;
    color: #f56c6c;
}

.delete-btn:hover {
    background: #ffcdd2;
}

.edit-btn svg,
.delete-btn svg {
    width: 16px;
    height: 16px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.stat-item {
    text-align: center;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
}

.stat-item h3 {
    margin: 0 0 12px 0;
    color: #666;
    font-size: 14px;
    font-weight: normal;
}

.stat-value {
    font-size: 24px;
    font-weight: bold;
    margin: 0;
    color: #2c3e50;
}

.error-message,
.success-message {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 6px;
    font-size: 14px;
    z-index: 1000;
    animation: slideIn 0.3s ease;
    display: flex;
    align-items: center;
    gap: 10px;
    background: #ffebee;
    color: #d32f2f;
    border: 1px solid #ffcdd2;
}

.error-message .close-btn,
.success-message .close-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    margin-left: 10px;
}

.error-message .close-btn svg,
.success-message .close-btn svg {
    width: 16px;
    height: 16px;
    color: #d32f2f;
}

.success-message {
    background: #e8f5e8;
    color: #388e3c;
    border: 1px solid #c8e6c9;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }

    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@media (max-width: 768px) {
    .main-content {
        grid-template-columns: 1fr;
        padding: 20px 15px;
    }

    .record-form-card,
    .history-card,
    .stats-card {
        padding: 20px 15px;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .history-item {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }
}

/* 饮食推荐模态框样式 */
.diet-recommendations-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.3s ease;
}

.modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
}

.modal-content {
    background: white;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    max-width: 600px;
    max-height: 80vh;
    position: relative;
    margin: 20px;
    width: 100%;
    animation: modalSlideIn 0.3s ease;
    display: flex;
    flex-direction: column;
    overflow: hidden; /* 防止内容溢出圆角 */
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 30px;
    border-bottom: 1px solid #f0f0f0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 16px 16px 0 0;
}

.modal-header h3 {
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 20px;
    font-weight: 600;
}

.recommendation-icon {
    font-size: 24px;
}

.modal-header .close-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s;
}

.modal-header .close-btn:hover {
    background: rgba(255, 255, 255, 0.3);
}

.modal-header .close-btn svg {
    width: 20px;
    height: 20px;
    color: white;
}

.modal-body {
    overflow-y: auto;
    max-height: calc(80vh - 80px); /* 减去头部高度 */
    padding: 0;
    /* 自定义滚动条样式 */
    scrollbar-width: thin;
    scrollbar-color: #d1d5db #f3f4f6;
}

.modal-body::-webkit-scrollbar {
    width: 8px;
}

.modal-body::-webkit-scrollbar-track {
    background: #f3f4f6;
    border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
    background: #9ca3af;
}

.loading-section {
    padding: 60px 30px;
    text-align: center;
    color: #666;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

.recommendations-content {
    padding: 30px;
}

.exercise-summary {
    background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 24px;
    border: 1px solid #e8ecff;
}

.exercise-summary h4 {
    margin: 0 0 16px 0;
    color: #2c3e50;
    font-size: 16px;
    font-weight: 600;
}

.summary-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 16px;
}

.stat-item {
    text-align: center;
    background: white;
    padding: 12px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-label {
    display: block;
    font-size: 12px;
    color: #666;
    margin-bottom: 4px;
}

.stat-value {
    display: block;
    font-size: 16px;
    font-weight: 600;
    color: #2c3e50;
}

.stat-value.recommend {
    color: #667eea;
    font-weight: 700;
}

.recommendations-sections {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.recommendation-category {
    background: #fafbfc;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #e8ecf0;
}

.recommendation-category h5 {
    margin: 0 0 16px 0;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
}

.category-icon {
    width: 18px;
    height: 18px;
    color: #667eea;
}

.recommendation-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.recommendation-item {
    background: white;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #e8ecf0;
    transition: box-shadow 0.3s;
}

.recommendation-item:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
}

.item-header {
    margin-bottom: 8px;
}

.item-name {
    font-weight: 600;
    color: #2c3e50;
    font-size: 14px;
}

.item-description {
    margin: 0 0 12px 0;
    color: #666;
    font-size: 13px;
    line-height: 1.4;
}

.item-examples {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.example-tag {
    background: #f0f4ff;
    color: #667eea;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 500;
    border: 1px solid #e8ecff;
}

.modal-actions {
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid #f0f0f0;
    display: flex;
    gap: 12px;
    justify-content: center;
}

.action-btn {
    padding: 12px 24px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s;
    min-width: 140px;
    justify-content: center;
}

.action-btn.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.action-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.action-btn.secondary {
    background: #f8f9fa;
    color: #666;
    border: 1px solid #e8ecf0;
}

.action-btn.secondary:hover {
    background: #e9ecef;
    color: #495057;
}

.action-icon {
    font-size: 16px;
}

@keyframes modalSlideIn {
    from {
        opacity: 0;
        transform: scale(0.9) translateY(-20px);
    }
    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .modal-content {
        margin: 10px;
        max-height: 90vh;
    }

    .modal-header {
        padding: 20px;
    }

    .recommendations-content {
        padding: 20px;
    }

    .summary-stats {
        grid-template-columns: repeat(2, 1fr);
    }

    .modal-actions {
        flex-direction: column;
    }

    .action-btn {
        width: 100%;
    }
}
</style>