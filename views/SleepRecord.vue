<template>
    <div class="sleep-record-container">
        <header class="report-header">
            <h1>
                <svg viewBox="0 0 24 24" fill="currentColor" class="header-icon">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
                睡眠记录
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
                            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" />
                    </svg>
                    记录今日睡眠
                </h2>

                <form @submit.prevent="submitSleep" class="sleep-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label>入睡时间</label>
                            <input v-model="sleepData.sleep_time" type="datetime-local" required
                                :max="getCurrentDateTime()" />
                        </div>
                        <div class="form-group">
                            <label>起床时间</label>
                            <input v-model="sleepData.wake_time" type="datetime-local" required
                                :min="sleepData.sleep_time" :max="getCurrentDateTime()" />
                        </div>
                    </div>

                    <div class="duration-display" v-if="sleepDuration">
                        <p>睡眠时长：<span class="duration-value">{{ sleepDuration }}</span></p>
                    </div>

                    <div class="form-group">
                        <label>睡眠质量</label>
                        <div class="quality-selector">
                            <button v-for="quality in qualityOptions" :key="quality.value" type="button"
                                @click="sleepData.quality = quality.value"
                                :class="['quality-btn', { active: sleepData.quality === quality.value }]"
                                :data-value="quality.value">
                                <span class="quality-icon">
                                    <svg viewBox="0 0 24 24" fill="currentColor">
                                        <path :d="quality.iconPath" />
                                    </svg>
                                </span>
                                <span>{{ quality.label }}</span>
                            </button>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>睡眠备注（可选）</label>
                        <textarea v-model="sleepData.notes" placeholder="记录睡眠感受、梦境或影响睡眠的因素..." rows="3"></textarea>
                    </div>

                    <div class="form-actions">
                        <button v-if="isEditMode" type="button" @click="cancelEdit" class="cancel-btn">
                            取消编辑
                        </button>
                        <button type="submit" :disabled="loading" class="submit-btn">
                            {{ loading ? '保存中...' : (isEditMode ? '更新睡眠记录' : '保存睡眠记录') }}
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
                        最近睡眠记录
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

                <div v-else-if="sleepHistory.length === 0" class="no-data">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path
                            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" />
                    </svg>
                    <p>暂无睡眠记录</p>
                </div>

                <div v-else class="history-list">
                    <div v-for="record in sleepHistory" :key="record.id" class="history-item">
                        <div class="record-date">
                            <span class="date-text">{{ formatDate(record.sleep_time) }}</span>
                            <span class="weekday">{{ getWeekday(record.sleep_time) }}</span>
                        </div>

                        <div class="record-details">
                            <div class="time-info">
                                <span class="sleep-time">{{ formatTime(record.sleep_time) }}</span>
                                <span class="separator">→</span>
                                <span class="wake-time">{{ formatTime(record.wake_time) }}</span>
                            </div>
                            <div class="duration-info">
                                <span class="duration">{{ calculateDuration(record.sleep_time, record.wake_time)
                                    }}</span>
                                <span class="quality" :class="getQualityClass(record.quality)">
                                    {{ getQualityText(record.quality) }}
                                </span>
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

            <!-- 睡眠统计 -->
            <div class="stats-card">
                <h2>
                    <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                        <path
                            d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" />
                    </svg>
                    本周睡眠统计
                </h2>

                <div class="stats-grid">
                    <div class="stat-item">
                        <h3>平均睡眠时长</h3>
                        <p class="stat-value">{{ weeklyStats.averageDuration }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>总睡眠时间</h3>
                        <p class="stat-value">{{ weeklyStats.totalDuration }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>记录天数</h3>
                        <p class="stat-value">{{ weeklyStats.recordDays }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>睡眠质量</h3>
                        <p class="stat-value">{{ weeklyStats.averageQuality }}</p>
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
            recordType="sleep"
            @close="showHistoryManager = false"
            @edit="handleEditFromHistory"
            @deleted="handleRecordDeleted"
            @error="handleError"
        />
    </div>
</template>

<script>
import axios from 'axios';
import HistoryManager from '../components/HistoryManager.vue';

export default {
    name: 'SleepRecord',
    components: {
        HistoryManager
    },
    data() {
        return {
            sleepData: {
                sleep_time: '',
                wake_time: '',
                quality: 3,
                notes: ''
            },
            sleepHistory: [],
            loading: false,
            errorMessage: '',
            successMessage: '',
            // 编辑模式状态管理
            isEditMode: false,
            editingRecordId: null,
            qualityOptions: [
                {
                    value: 1,
                    label: '很差',
                    iconPath: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1.5 6c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm2.5 0c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm-4 7h6c0 1.66-1.34 3-3 3s-3-1.34-3-3z' // 难过表情 - 睡眠质量很差
                },
                {
                    value: 2,
                    label: '较差',
                    iconPath: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1.5 6c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm2.5 0c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm-3 6h4v1c0 1.1-.9 2-2 2s-2-.9-2-2v-1z' // 疲惫表情 - 睡眠质量较差
                },
                {
                    value: 3,
                    label: '一般',
                    iconPath: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1.5 6c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm2.5 0c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm-3 6h6v1H9v-1z' // 平静表情 - 睡眠质量一般
                },
                {
                    value: 4,
                    label: '较好',
                    iconPath: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1.5 6c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm2.5 0c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm-4 7c0-1.66 1.34-3 3-3s3 1.34 3 3H8z' // 满意微笑 - 睡眠质量较好
                },
                {
                    value: 5,
                    label: '很好',
                    iconPath: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1.5 6c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm2.5 0c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5zm-5.5 7c0-2.76 2.24-5 5-5s5 2.24 5 5H7z' // 开心大笑 - 睡眠质量很好
                }
            ],
            showHistoryManager: false
        };
    },
    computed: {
        sleepDuration() {
            if (!this.sleepData.sleep_time || !this.sleepData.wake_time) return '';

            const sleepTime = new Date(this.sleepData.sleep_time);
            const wakeTime = new Date(this.sleepData.wake_time);

            if (wakeTime <= sleepTime) return '';

            const duration = (wakeTime - sleepTime) / (1000 * 60 * 60);
            return `${duration.toFixed(1)} 小时`;
        },

        weeklyStats() {
            if (this.sleepHistory.length === 0) {
                return {
                    averageDuration: '0小时',
                    totalDuration: '0小时',
                    recordDays: '0天',
                    averageQuality: '无数据'
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
            const weeklyRecords = this.sleepHistory.filter(record => {
                const recordDate = new Date(record.sleep_time);
                return recordDate >= weekStart && recordDate <= weekEnd;
            });

            if (weeklyRecords.length === 0) {
                return {
                    averageDuration: '0小时',
                    totalDuration: '0小时',
                    recordDays: '0天',
                    averageQuality: '无数据'
                };
            }

            // 计算每条记录的小时数
            const totalHours = weeklyRecords.reduce((sum, record) => {
                if (!record.sleep_time || !record.wake_time) return sum;

                const sleepTime = new Date(record.sleep_time);
                const wakeTime = new Date(record.wake_time);
                const hours = (wakeTime - sleepTime) / (1000 * 60 * 60);

                return sum + (hours > 0 ? hours : 0);
            }, 0);

            const avgHours = totalHours / weeklyRecords.length;
            const avgQuality = weeklyRecords.reduce((sum, record) => sum + (record.quality || 3), 0) / weeklyRecords.length;

            return {
                averageDuration: `${avgHours.toFixed(1)}小时`,
                totalDuration: `${totalHours.toFixed(1)}小时`,
                recordDays: `${weeklyRecords.length}天`,
                averageQuality: this.getQualityText(Math.round(avgQuality))
            };
        }
    },
    async mounted() {
        await this.fetchSleepHistory();
        this.setDefaultTimes();
    },
    methods: {
        async fetchSleepHistory() {
            try {
                const response = await axios.get('/api/sleep/recent/');
                this.sleepHistory = response.data.slice(0, 7);
            } catch (error) {
                console.error('获取睡眠记录失败：', error);
                this.sleepHistory = [];
            }
        },

        async submitSleep() {
            if (!this.sleepData.sleep_time || !this.sleepData.wake_time) {
                this.errorMessage = '请填写完整的睡眠时间';
                return;
            }

            const sleepTime = new Date(this.sleepData.sleep_time);
            const wakeTime = new Date(this.sleepData.wake_time);

            if (wakeTime <= sleepTime) {
                this.errorMessage = '起床时间必须晚于入睡时间';
                return;
            }

            this.loading = true;
            this.errorMessage = '';

            try {
                if (this.isEditMode && this.editingRecordId) {
                    // 编辑模式：更新现有记录
                    await axios.put(`/api/sleep/${this.editingRecordId}/`, this.sleepData);
                    this.successMessage = '睡眠记录更新成功！';
                } else {
                    // 新增模式：创建新记录
                    await axios.post('/api/sleep/', this.sleepData);
                    this.successMessage = '睡眠记录保存成功！';
                }

                // 重置表单和编辑状态
                this.resetForm();

                // 刷新历史记录
                await this.fetchSleepHistory();

                // 清除成功提示
                setTimeout(() => {
                    this.successMessage = '';
                }, 3000);

            } catch (error) {
                console.error('保存睡眠记录失败：', error);
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
            if (!confirm('确定要删除这条睡眠记录吗？')) return;

            try {
                await axios.delete(`/api/sleep/${recordId}/`);
                this.successMessage = '睡眠记录删除成功！';
                await this.fetchSleepHistory();

                setTimeout(() => {
                    this.successMessage = '';
                }, 3000);

            } catch (error) {
                console.error('删除睡眠记录失败：', error);
                this.errorMessage = '删除失败，请重试';
            }
        },

        editRecord(record) {
            // 设置编辑模式
            this.isEditMode = true;
            this.editingRecordId = record.id;

            // 填充表单数据
            this.sleepData = {
                sleep_time: this.formatDateTimeForInput(record.sleep_time),
                wake_time: this.formatDateTimeForInput(record.wake_time),
                quality: record.quality,
                notes: record.notes || ''
            };

            // 滚动到表单
            document.querySelector('.record-form-card').scrollIntoView({
                behavior: 'smooth'
            });
        },

        resetForm() {
            // 重置表单数据
            this.sleepData = {
                sleep_time: '',
                wake_time: '',
                quality: 3,
                notes: ''
            };
            // 重置编辑状态
            this.isEditMode = false;
            this.editingRecordId = null;
            // 设置默认时间
            this.setDefaultTimes();
        },

        cancelEdit() {
            this.resetForm();
        },

        setDefaultTimes() {
            const now = new Date();
            const yesterday = new Date(now);
            yesterday.setDate(yesterday.getDate() - 1);

            // 默认入睡时间：昨晚23:00
            yesterday.setHours(23, 0, 0, 0);
            this.sleepData.sleep_time = this.formatDateTimeForInput(yesterday.toISOString());

            // 默认起床时间：今早7:00
            now.setHours(7, 0, 0, 0);
            this.sleepData.wake_time = this.formatDateTimeForInput(now.toISOString());
        },

        getCurrentDateTime() {
            const now = new Date();
            // 获取本地时间并格式化为 datetime-local 格式
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');

            return `${year}-${month}-${day}T${hours}:${minutes}`;
        },

        formatDateTimeForInput(dateString) {
            const date = new Date(dateString);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');

            return `${year}-${month}-${day}T${hours}:${minutes}`;
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

        formatDuration(hours) {
            // 确保 hours 是一个有效的数字
            const numHours = parseFloat(hours);
            if (isNaN(numHours) || numHours < 0) {
                return '0.0小时';
            }
            return `${numHours.toFixed(1)}小时`;
        },

        calculateDuration(sleepTime, wakeTime) {
            if (!sleepTime || !wakeTime) {
                return '0.0小时';
            }

            const sleep = new Date(sleepTime);
            const wake = new Date(wakeTime);

            if (wake <= sleep) {
                return '0.0小时';
            }

            const hours = (wake - sleep) / (1000 * 60 * 60);
            return `${hours.toFixed(1)}小时`;
        },

        getWeekday(dateString) {
            const date = new Date(dateString);
            const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
            return `周${weekdays[date.getDay()]}`;
        },

        getQualityText(quality) {
            const option = this.qualityOptions.find(opt => opt.value === quality);
            return option ? option.label : '未知';
        },

        getQualityClass(quality) {
            if (quality >= 4) return 'quality-good';
            if (quality >= 3) return 'quality-normal';
            return 'quality-poor';
        },

        // 历史记录管理相关方法
        showAllHistory() {
            this.showHistoryManager = true;
        },

        handleEditFromHistory(record) {
            // 填充表单数据进行编辑
            this.sleepData = {
                sleep_time: this.formatDateTimeForInput(record.sleep_time),
                wake_time: this.formatDateTimeForInput(record.wake_time),
                quality: record.quality,
                notes: record.notes || ''
            };
            this.isEditMode = true;
            this.editingRecordId = record.id;
            // 滚动到表单顶部
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },

        handleRecordDeleted(recordId) {
            // 从本地历史记录中移除已删除的记录
            this.sleepHistory = this.sleepHistory.filter(record => record.id !== recordId);
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

        formatDateTimeForInput(dateTimeString) {
            if (!dateTimeString) return '';
            const date = new Date(dateTimeString);
            // 格式化为 datetime-local 输入框需要的格式
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            return `${year}-${month}-${day}T${hours}:${minutes}`;
        }
    }
};
</script>

<style scoped>
.sleep-record-container {
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
    color: #9b59b6; /* 紫色 - 睡眠相关 */
}

.back-btn {
    background: #9b59b6;
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
    background: #8e44ad;
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
    background: #9b59b6;
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
    background: #8e44ad;
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
    color: #9b59b6;
}

.sleep-form {
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
.form-group textarea {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.3s;
}

/* 确保datetime-local输入框显示正确的时间选择器 */
.form-group input[type="datetime-local"] {
    padding: 12px;
    font-family: inherit;
    cursor: pointer;
    /* 保持原生外观和功能 */
}

.form-group input[type="datetime-local"]::-webkit-calendar-picker-indicator {
    cursor: pointer;
    /* 确保日历图标可点击 */
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #9b59b6;
    box-shadow: 0 0 0 2px rgba(155, 89, 182, 0.2);
}

.duration-display {
    background: #f8f9fa;
    padding: 16px;
    border-radius: 6px;
    text-align: center;
}

.duration-value {
    font-weight: bold;
    color: #9b59b6;
    font-size: 18px;
}

.quality-selector {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.quality-btn {
    flex: 1;
    min-width: 80px;
    padding: 12px 8px;
    border: 2px solid #e1e8ed;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    font-size: 12px;
}

.quality-btn:hover {
    border-color: #9b59b6;
}

.quality-btn.active {
    border-color: #9b59b6;
    background: #e8f3ff;
    color: #9b59b6;
}

.quality-icon {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.quality-icon svg {
    width: 100%;
    height: 100%;
}

/* 为不同睡眠质量等级添加对应的颜色 */
.quality-btn[data-value="1"] .quality-icon svg {
    color: #f56c6c; /* 很差 - 红色 */
}

.quality-btn[data-value="2"] .quality-icon svg {
    color: #e6a23c; /* 较差 - 橙色 */
}

.quality-btn[data-value="3"] .quality-icon svg {
    color: #909399; /* 一般 - 灰色 */
}

.quality-btn[data-value="4"] .quality-icon svg {
    color: #67c23a; /* 较好 - 绿色 */
}

.quality-btn[data-value="5"] .quality-icon svg {
    color: #9b59b6; /* 很好 - 紫色 */
}

.quality-btn.active[data-value="1"] {
    border-color: #f56c6c;
    background: rgba(245, 108, 108, 0.1);
    color: #f56c6c;
}

.quality-btn.active[data-value="2"] {
    border-color: #e6a23c;
    background: rgba(230, 162, 60, 0.1);
    color: #e6a23c;
}

.quality-btn.active[data-value="3"] {
    border-color: #909399;
    background: rgba(144, 147, 153, 0.1);
    color: #909399;
}

.quality-btn.active[data-value="4"] {
    border-color: #67c23a;
    background: rgba(103, 194, 58, 0.1);
    color: #67c23a;
}

.quality-btn.active[data-value="5"] {
    border-color: #9b59b6;
    background: rgba(155, 89, 182, 0.1);
    color: #9b59b6;
}

.form-actions {
    display: flex;
    gap: 12px;
    align-items: center;
}

.submit-btn {
    background: #9b59b6;
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
    background: #8e44ad;
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

.time-info {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
}

.separator {
    color: #999;
}

.duration-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.duration {
    font-weight: bold;
    color: #409eff;
}

.quality {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
}

.quality-good {
    background: #e8f5e8;
    color: #388e3c;
}

.quality-normal {
    background: #fff3e0;
    color: #f57c00;
}

.quality-poor {
    background: #ffebee;
    color: #d32f2f;
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
}

.error-message {
    background: #ffebee;
    color: #d32f2f;
    border: 1px solid #ffcdd2;
}

.success-message {
    background: #e8f5e8;
    color: #388e3c;
    border: 1px solid #c8e6c9;
}

.close-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    margin-left: 10px;
}

.close-btn svg {
    width: 16px;
    height: 16px;
    color: #666;
}

.close-btn:hover svg {
    color: #333;
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

    .quality-selector {
        grid-template-columns: repeat(3, 1fr);
    }

    .history-item {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }
}
</style>