<template>
    <div class="dashboard">
        <!-- 顶部导航栏 -->
        <header class="header">
            <div class="header-content">
                <h1>健康管理系统</h1>
                <div class="header-right">
                    <div class="current-time">
                        <span class="time-display">{{ currentTime }}</span>
                        <span class="date-display">{{ currentDate }}</span>
                    </div>
                    <div class="user-info">
                        <span>欢迎，{{ username }}</span>
                        <!-- 收件箱徽章 -->
                        <div class="inbox-badge" @click="showInbox" :class="{ 'has-unread': inboxUnreadCount > 0 }">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path d="M20 4H4C2.9 4 2.01 4.9 2.01 6L2 18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V6C22 4.9 21.1 4 20 4ZM20 8L12 13L4 8V6L12 11L20 6V8Z"/>
                            </svg>
                            <span v-if="inboxUnreadCount > 0" class="badge-count">{{ inboxUnreadCount }}</span>
                        </div>
                        <!-- 用户下拉菜单 -->
                        <div class="user-dropdown" @mouseenter="showUserMenu = true" @mouseleave="handleDropdownLeave">
                            <div class="user-trigger">
                                <div class="user-avatar">
                                    {{ username.charAt(0).toUpperCase() }}
                                </div>
                                <svg viewBox="0 0 24 24" fill="currentColor" class="dropdown-arrow" :class="{ 'rotated': showUserMenu }">
                                    <path d="M7 10l5 5 5-5z"/>
                                </svg>
                            </div>
                            <div class="user-menu" v-show="showUserMenu" @mouseenter="cancelHideMenu" @mouseleave="handleMenuLeave">
                                <div class="menu-header">
                                    <div class="menu-avatar">
                                        {{ username.charAt(0).toUpperCase() }}
                                    </div>
                                    <div class="menu-user-info">
                                        <span class="menu-username">{{ username }}</span>
                                        <span class="menu-welcome">健康管理中心</span>
                                    </div>
                                </div>
                                <div class="menu-divider"></div>
                                <ul class="menu-items">
                                    <li class="menu-item" @click="$router.push('/profile')">
                                        <svg viewBox="0 0 24 24" fill="currentColor" class="menu-icon">
                                            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                                        </svg>
                                        <span>个人信息</span>
                                    </li>
                                    <li class="menu-item" @click="$router.push('/my-activity')">
                                        <svg viewBox="0 0 24 24" fill="currentColor" class="menu-icon">
                                            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                                        </svg>
                                        <span>我的健康动态</span>
                                    </li>
                                    <li class="menu-item logout-item" @click="handleLogout">
                                        <svg viewBox="0 0 24 24" fill="currentColor" class="menu-icon">
                                            <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.59L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
                                        </svg>
                                        <span>退出登录</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </header>

        <!-- 主要内容区域 -->
        <main class="main-content">
            <!-- 数据概览卡片 -->
            <section class="overview-section">
                <h2>今日数据概览</h2>
                <div class="overview-cards">
                    <div class="card sleep-card">
                        <div class="card-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" />
                            </svg>
                        </div>
                        <div class="card-content">
                            <h3>睡眠时间</h3>
                            <p class="card-value">{{ todaySleep }}</p>
                            <span class="card-unit">小时</span>
                        </div>
                    </div>

                    <div class="card exercise-card">
                        <div class="card-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z" />
                            </svg>
                        </div>
                        <div class="card-content">
                            <h3>运动时间</h3>
                            <p class="card-value">{{ todayExercise }}</p>
                            <span class="card-unit">分钟</span>
                        </div>
                    </div>

                    <div class="card diet-card">
                        <div class="card-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z" />
                            </svg>
                        </div>
                        <div class="card-content">
                            <h3>摄入热量</h3>
                            <p class="card-value">{{ todayCalories }}</p>
                            <span class="card-unit">卡路里</span>
                        </div>
                    </div>

                    <div class="card weight-card">
                        <div class="card-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M12 3c3.87 0 7 3.13 7 7 0 3.87-3.13 7-7 7s-7-3.13-7-7c0-3.87 3.13-7 7-7zM12 1C6.48 1 2 5.48 2 11s4.48 10 10 10 10-4.48 10-10S17.52 1 12 1zm0 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" />
                            </svg>
                        </div>
                        <div class="card-content">
                            <h3>当前体重</h3>
                            <p class="card-value">{{ currentWeight }}</p>
                            <span class="card-unit">kg</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 快捷操作区域 -->
            <section class="actions-section">
                <h2>快捷操作</h2>
                <div class="quick-actions">
                    <button @click="$router.push('/sleep')" class="action-btn sleep-btn">
                        <span class="btn-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" />
                            </svg>
                        </span>
                        记录睡眠
                    </button>
                    <button @click="$router.push('/exercise')" class="action-btn exercise-btn">
                        <span class="btn-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z" />
                            </svg>
                        </span>
                        记录运动
                    </button>
                    <button @click="$router.push('/diet')" class="action-btn diet-btn">
                        <span class="btn-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z" />
                            </svg>
                        </span>
                        记录饮食
                    </button>
                    <button @click="$router.push('/social')" class="action-btn social-hub-btn">
                        <span class="btn-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M12 12.75c1.63 0 3.07.39 4.24.9 1.08.48 1.76 1.56 1.76 2.73V18H6v-1.61c0-1.18.68-2.26 1.76-2.74 1.17-.51 2.61-.9 4.24-.9zM4 13c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm1.13 1.1c-.37-.06-.74-.1-1.13-.1C2.48 14 0 14.81 0 16.25V18h4.5v-1.61c0-.83.23-1.61.63-2.29zM20 13c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm-.63 1.1c.4.68.63 1.46.63 2.29V18H24v-1.75C24 14.81 21.52 14 20 14c-.39 0-.76.04-1.13.1zM12 6c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3z" />
                            </svg>
                        </span>
                        社交管理
                    </button>
                    <button @click="$router.push('/health-management')" class="action-btn health-management-btn">
                        <span class="btn-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                            </svg>
                        </span>
                        健康管理
                    </button>
                </div>
            </section>

            <!-- 最近记录和健康目标 -->
            <section class="bottom-section">
                <div class="recent-section">
                    <h2>最近记录</h2>
                    <div class="recent-tabs">
                        <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key"
                            :class="['tab-btn', { active: activeTab === tab.key }]">
                            {{ tab.label }}
                        </button>
                    </div>

                    <div class="recent-content">
                        <!-- 滚动提示 -->
                        <div v-if="shouldShowScrollHint" class="scroll-hint">
                            <svg viewBox="0 0 24 24" fill="currentColor" class="scroll-icon">
                                <path d="M7.41 8.84L12 13.42L16.59 8.84L18 10.25L12 16.25L6 10.25L7.41 8.84Z"/>
                            </svg>
                            <span>{{ currentRecords.length }}条记录，可滚动查看</span>
                        </div>

                        <!-- 睡眠记录 -->
                        <div v-if="activeTab === 'sleep'" class="records-list">
                            <div v-if="recentSleep.length === 0" class="no-data">
                                暂无睡眠记录
                            </div>
                            <div v-else>
                                <div v-for="record in recentSleep" :key="record.id" class="record-item">
                                    <span class="record-date">{{ formatDate(record.sleep_time) }}</span>
                                    <span class="record-detail">
                                        {{ formatTime(record.sleep_time) }} - {{ formatTime(record.wake_time) }}
                                        ({{ calculateDuration(record.sleep_time, record.wake_time) }})
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 运动记录 -->
                        <div v-if="activeTab === 'exercise'" class="records-list">
                            <div v-if="recentExercise.length === 0" class="no-data">
                                暂无运动记录
                            </div>
                            <div v-else>
                                <div v-for="record in recentExercise" :key="record.id" class="record-item">
                                    <span class="record-date">{{ formatDate(record.record_datetime) }}</span>
                                    <span class="record-detail">
                                        {{ record.exercise_type_cn }} - {{ record.duration_minutes }}分钟
                                        ({{ Math.round(record.calories_burned) }}卡路里)
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- 饮食记录 -->
                        <div v-if="activeTab === 'diet'" class="records-list">
                            <div v-if="recentDiet.length === 0" class="no-data">
                                暂无饮食记录
                            </div>
                            <div v-else>
                                <div v-for="record in recentDiet" :key="record.id" class="record-item">
                                    <span class="record-date">{{ formatDate(record.record_date) }}</span>
                                    <span class="record-detail">
                                        {{ record.food_name }} - {{ Math.round(record.calories) }}卡路里
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 个人健康目标 -->
                <div class="goals-section">
                    <h2>健康目标</h2>
                    <!-- 占位div，保持与最近记录的高度对齐 -->
                    <div class="goals-header">
                        <div class="goals-status">
                            <span v-if="activeGoals.length > 0" class="goals-count active">
                                {{ activeGoals.length }}个进行中
                            </span>
                            <span v-if="completedGoals.length > 0" class="goals-count completed">
                                {{ completedGoals.length }}个已完成
                            </span>
                            <span v-if="activeGoals.length === 0 && completedGoals.length === 0" class="goals-count">
                                暂无目标
                            </span>
                        </div>
                    </div>
                    <div class="goals-content">
                        <div v-if="healthGoals.length === 0" class="no-goals">
                            <svg viewBox="0 0 24 24" fill="currentColor" class="no-goals-icon">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                            </svg>
                            <p>暂无健康目标</p>
                            <button @click="showGoalEditor = true" class="create-goal-btn">
                                设置目标
                            </button>
                        </div>
                        <div v-else class="goals-list">
                            <div v-for="goal in displayGoals" :key="goal.id" :class="['goal-item', { 'completed-goal': isGoalCompleted(goal) }]">
                                <div class="goal-header">
                                    <span class="goal-type">{{ getGoalTypeName(goal.goal_type) }}</span>
                                    <span :class="['goal-period', { 'completed-period': isGoalCompleted(goal) }]">
                                        {{ isGoalCompleted(goal) ? '已完成' : formatDateRange(goal.start_date, goal.end_date) }}
                                    </span>
                                </div>
                                <div class="goal-progress">
                                    <div class="progress-info">
                                        <span class="progress-text">
                                            {{ getCachedProgress(goal) }} / {{ goal.target_value }}{{ getGoalUnit(goal.goal_type) }}
                                        </span>
                                        <span
                                            :class="['progress-percentage', {
                                                'completed': isGoalCompleted(goal),
                                                'over-achieved': isGoalOverAchieved(goal)
                                            }]"
                                        >
                                            {{ getProgressPercentage(goal) }}%
                                            <span v-if="isGoalCompleted(goal)" class="completion-badge">
                                                {{ isGoalOverAchieved(goal) ? '🎉' : '✅' }}
                                            </span>
                                        </span>
                                    </div>
                                    <div class="progress-bar">
                                        <div
                                            :class="['progress-fill', {
                                                'completed': isGoalCompleted(goal),
                                                'over-achieved': isGoalOverAchieved(goal)
                                            }]"
                                            :style="{ width: getProgressBarPercentage(goal) + '%' }"
                                        ></div>
                                    </div>
                                    <div v-if="isGoalCompleted(goal)" class="completion-message">
                                        <span v-if="isGoalOverAchieved(goal)" class="over-achieved-text">
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="achievement-icon">
                                                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                                            </svg>
                                            超额完成！比目标多{{ getProgressPercentage(goal) - 100 }}%
                                        </span>
                                        <span v-else class="completed-text">
                                            <svg viewBox="0 0 24 24" fill="currentColor" class="achievement-icon">
                                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                            </svg>
                                            目标达成！
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="goals-actions">
                                <button @click="showGoalEditor = true" class="edit-goals-btn">
                                    <svg viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                                    </svg>
                                    管理目标
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 健康目标编辑器弹窗 -->
            <HealthGoalEditor
                :visible="showGoalEditor"
                @close="showGoalEditor = false"
                @goal-updated="refreshGoals"
            />

            <!-- 健康预警弹窗 -->
            <HealthAlertModal
                :visible="showAlertModal"
                :alert="currentAlert || {}"
                @close="showAlertModal = false"
                @alert-handled="handleAlertAction"
            />

            <!-- 收件箱面板 -->
            <InboxPanel
                :visible="showInboxPanel"
                @close="closeInboxPanel"
                @unread-count-changed="handleUnreadCountChanged"
            />
        </main>
    </div>
</template>

<script>
import axios from 'axios';
import HealthGoalEditor from '../components/HealthGoalEditor.vue';
import HealthAlertModal from '../components/HealthAlertModal.vue';
import InboxPanel from '../components/InboxPanel.vue';

export default {
    name: 'Dashboard',
    components: {
        HealthGoalEditor,
        HealthAlertModal,
        InboxPanel
    },
    data() {
        return {
            username: '',
            currentTime: '',
            currentDate: '',
            todaySleep: 0,
            todayExercise: 0,
            todayCalories: 0,
            currentWeight: 0,
            activeTab: 'sleep',
            tabs: [
                { key: 'sleep', label: '睡眠记录' },
                { key: 'exercise', label: '运动记录' },
                { key: 'diet', label: '饮食记录' }
            ],
            recentSleep: [],
            recentExercise: [],
            recentDiet: [],
            loading: false,
            timeInterval: null,
            // 健康目标相关数据
            healthGoals: [],
            showGoalEditor: false,
            // 缓存目标进度数据
            goalProgress: {},
            // 健康预警相关数据
            healthAlerts: [],
            currentAlert: null,
            showAlertModal: false,
            alertCheckInterval: null,
            // 收件箱相关数据
            showInboxPanel: false,
            inboxUnreadCount: 0,
            // 用户下拉菜单
            showUserMenu: false,
            menuHideTimer: null,
            // 健康管理下拉菜单
            showHealthMenu: false,
            healthMenuHideTimer: null
        };
    },
    computed: {
        // 当前活动标签页的记录数据
        currentRecords() {
            if (this.activeTab === 'sleep') return this.recentSleep;
            if (this.activeTab === 'exercise') return this.recentExercise;
            if (this.activeTab === 'diet') return this.recentDiet;
            return [];
        },
        // 是否需要显示滚动提示
        shouldShowScrollHint() {
            return this.currentRecords.length > 4;
        }
    },
    async mounted() {
        this.updateTime();
        this.timeInterval = setInterval(this.updateTime, 1000);
        await this.initDashboard();
    },
    beforeUnmount() {
        if (this.timeInterval) {
            clearInterval(this.timeInterval);
        }
        if (this.alertCheckInterval) {
            clearInterval(this.alertCheckInterval);
        }
        if (this.menuHideTimer) {
            clearTimeout(this.menuHideTimer);
        }
    },
    methods: {
        updateTime() {
            const now = new Date();
            this.currentTime = now.toLocaleTimeString('zh-CN', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            this.currentDate = now.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                weekday: 'long'
            });
        },

        async initDashboard() {
            this.loading = true;
            try {
                // 获取用户信息
                await this.fetchUserInfo();
                // 获取今日数据概览
                await this.fetchTodayData();
                // 获取最近记录
                await this.fetchRecentRecords();
                // 获取健康目标
                await this.fetchHealthGoals();
                // 检查健康预警
                await this.checkHealthAlerts();
                // 设置定时检查预警
                this.startAlertChecking();
                // 加载收件箱未读数量
                await this.loadInboxUnreadCount();
            } catch (error) {
                console.error('Dashboard初始化失败：', error);
            } finally {
                this.loading = false;
            }
        },

        async fetchUserInfo() {
            try {
                // 首先尝试从localStorage获取用户名
                const storedUsername = localStorage.getItem('username');
                if (storedUsername) {
                    this.username = storedUsername;
                    return;
                }

                // 如果没有存储的用户名，尝试调用API获取
                const response = await axios.get('/api/profile/my_profile/');
                this.username = response.data.user?.username || '用户';
            } catch (error) {
                console.error('获取用户信息失败：', error);
                // 设置默认值
                this.username = '用户';
            }
        },

        // 修复退出登录功能
        async handleLogout() {
            if (confirm('确定要退出登录吗？')) {
                try {
                    // 调用后端登出API
                    await axios.post('/api/logout/post/');
                } catch (error) {
                    // 即使后端登出失败，前端也要清理token
                    console.log('后端登出失败，但继续前端登出');
                } finally {
                    // 清除本地存储的token和用户信息
                    localStorage.removeItem('token');
                    localStorage.removeItem('username');

                    // 清除axios默认headers
                    delete axios.defaults.headers.common['Authorization'];

                    // 跳转到登录页面
                    this.$router.push('/login');
                }
            }
        },

        async fetchTodayData() {
            try {
                // 获取今日睡眠数据
                const sleepResponse = await axios.get('/api/sleep/today/');
                this.todaySleep = sleepResponse.data.total_hours || 0;

                // 获取今日运动数据
                const exerciseResponse = await axios.get('/api/exercise/today/');
                this.todayExercise = exerciseResponse.data.total_minutes || 0;

                // 获取今日饮食数据
                const dietResponse = await axios.get('/api/diet/today/');
                this.todayCalories = dietResponse.data.total_calories || 0;

                // 获取最新体重
                const weightResponse = await axios.get('/api/profile/weight/latest/');
                this.currentWeight = weightResponse.data.weight || 0;

            } catch (error) {
                console.error('获取今日数据失败：', error);
                // 设置默认值，避免显示错误
                this.todaySleep = this.todaySleep || 0;
                this.todayExercise = this.todayExercise || 0;
                this.todayCalories = this.todayCalories || 0;
                this.currentWeight = this.currentWeight || 0;
            }
        },

        async fetchRecentRecords() {
            try {
                // 获取最近的睡眠记录
                const sleepResponse = await axios.get('/api/sleep/recent/');
                this.recentSleep = sleepResponse.data.slice(0, 7) || [];

                // 获取最近的运动记录
                const exerciseResponse = await axios.get('/api/exercise/recent/');
                this.recentExercise = exerciseResponse.data.slice(0, 7) || [];

                // 获取最近的饮食记录
                const dietResponse = await axios.get('/api/diet/recent/');
                this.recentDiet = dietResponse.data.slice(0, 7) || [];

            } catch (error) {
                console.error('获取最近记录失败：', error);
                // 设置空数组避免显示错误
                this.recentSleep = [];
                this.recentExercise = [];
                this.recentDiet = [];
            }
        },

        // 退出登录功能
        async handleLogout() {
            if (confirm('确定要退出登录吗？')) {
                try {
                    // 调用后端登出API（如果有的话）
                    await axios.post('/api/logout/');
                } catch (error) {
                    // 即使后端登出失败，前端也要清理token
                    console.log('后端登出失败，但继续前端登出');
                } finally {
                    // 清除本地存储的token和用户信息
                    localStorage.removeItem('token');
                    localStorage.removeItem('username');

                    // 清除axios默认headers
                    delete axios.defaults.headers.common['Authorization'];

                    // 跳转到登录页面
                    this.$router.push('/login');
                }
            }
        },

        // 格式化日期显示
        formatDate(dateString) {
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

        formatTime(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit'
            });
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

        // === 健康目标相关方法 ===
        async fetchHealthGoals() {
            try {
                const response = await axios.get('/api/goals/');
                this.healthGoals = response.data;
                // 获取所有目标的进度数据
                await this.refreshGoalProgress();
            } catch (error) {
                console.error('获取健康目标失败：', error);
                this.healthGoals = [];
            }
        },

        async refreshGoalProgress() {
            // 清空旧的进度数据
            this.goalProgress = {};

            // 为每个目标获取进度
            for (const goal of this.healthGoals) {
                try {
                    const progress = await this.getCurrentProgress(goal);
                    this.goalProgress[goal.id] = progress;
                } catch (error) {
                    console.error(`获取目标${goal.id}进度失败：`, error);
                    this.goalProgress[goal.id] = 0;
                }
            }
        },

        async refreshGoals() {
            await this.fetchHealthGoals();
        },

        // 获取缓存的目标进度
        getCachedProgress(goal) {
            return this.goalProgress[goal.id] || 0;
        },

        getGoalTypeName(goalType) {
            const typeMap = {
                'sleep': '睡眠目标',
                'exercise': '运动目标',
                'diet': '饮食目标'
            };
            return typeMap[goalType] || goalType;
        },

        getGoalUnit(goalType) {
            const unitMap = {
                'sleep': '小时',
                'exercise': '分钟',
                'diet': '卡路里'
            };
            return unitMap[goalType] || '';
        },

        formatDateRange(startDate, endDate) {
            const start = new Date(startDate);
            const end = new Date(endDate);
            const now = new Date();

            if (start <= now && now <= end) {
                return '进行中';
            } else if (now < start) {
                return '未开始';
            } else {
                return '已结束';
            }
        },

        async getCurrentProgress(goal) {
            const goalType = goal.goal_type;
            const startDate = goal.start_date;
            const endDate = goal.end_date;

            try {
                if (goalType === 'sleep') {
                    const response = await axios.get(`/api/sleep/period_summary/`, {
                        params: { start_date: startDate, end_date: endDate }
                    });
                    return response.data.total_hours || 0;
                } else if (goalType === 'exercise') {
                    const response = await axios.get(`/api/exercise/period_summary/`, {
                        params: { start_date: startDate, end_date: endDate }
                    });
                    return response.data.total_minutes || 0;
                } else if (goalType === 'diet') {
                    const response = await axios.get(`/api/diet/period_summary/`, {
                        params: { start_date: startDate, end_date: endDate }
                    });
                    return response.data.total_calories || 0;
                }
            } catch (error) {
                console.error(`获取${goalType}期间数据失败：`, error);
                // 如果API不存在，回退到今日数据
                if (goalType === 'sleep') {
                    return this.todaySleep || 0;
                } else if (goalType === 'exercise') {
                    return this.todayExercise || 0;
                } else if (goalType === 'diet') {
                    return this.todayCalories || 0;
                }
            }
            return 0;
        },

        getProgressPercentage(goal) {
            const current = this.getCachedProgress(goal);
            const target = goal.target_value;
            return Math.round((current / target) * 100);
        },

        getProgressBarPercentage(goal) {
            const percentage = this.getProgressPercentage(goal);
            return Math.min(percentage, 100); // 进度条最多显示100%
        },

        isGoalCompleted(goal) {
            return this.getProgressPercentage(goal) >= 100;
        },

        isGoalOverAchieved(goal) {
            return this.getProgressPercentage(goal) > 100;
        },

        // === 健康预警相关方法 ===
        async checkHealthAlerts() {
            try {
                // 检查并生成新的预警
                const checkResponse = await axios.post('/api/alerts/check_alerts/');

                // 获取所有未读预警
                const unreadResponse = await axios.get('/api/alerts/unread/');
                this.healthAlerts = unreadResponse.data;

                // 如果有新的预警，显示第一个
                if (checkResponse.data.new_alerts && checkResponse.data.new_alerts.length > 0) {
                    this.showNextAlert();
                }
            } catch (error) {
                console.error('检查健康预警失败：', error);
            }
        },

        startAlertChecking() {
            // 每30分钟检查一次预警
            this.alertCheckInterval = setInterval(() => {
                this.checkHealthAlerts();
            }, 30 * 60 * 1000);
        },

        showNextAlert() {
            const unreadAlerts = this.healthAlerts.filter(alert => !alert.is_read && alert.is_active);
            if (unreadAlerts.length > 0) {
                this.currentAlert = unreadAlerts[0];
                this.showAlertModal = true;
            }
        },

        async handleAlertAction(data) {
            const { action, alertId } = data;

            // 从本地数组中移除或更新预警
            if (action === 'dismiss') {
                this.healthAlerts = this.healthAlerts.filter(alert => alert.id !== alertId);
            } else if (action === 'read') {
                const alert = this.healthAlerts.find(alert => alert.id === alertId);
                if (alert) {
                    alert.is_read = true;
                }
            }

            // 如果还有未读预警，显示下一个
            setTimeout(() => {
                this.showNextAlert();
            }, 1000);
        },

        // === 收件箱相关方法 ===
        async loadInboxUnreadCount() {
            try {
                const response = await axios.get('/api/inbox/unread_count/');
                this.inboxUnreadCount = response.data.unread_count;
            } catch (error) {
                console.error('获取收件箱未读数量失败：', error);
            }
        },

        showInbox() {
            this.showInboxPanel = true;
        },

        closeInboxPanel() {
            this.showInboxPanel = false;
        },

        handleUnreadCountChanged(newCount) {
            this.inboxUnreadCount = newCount;
        },

        // 用户菜单控制方法
        handleDropdownLeave() {
            this.menuHideTimer = setTimeout(() => {
                this.showUserMenu = false;
            }, 300); // 300ms延迟
        },

        handleMenuLeave() {
            this.menuHideTimer = setTimeout(() => {
                this.showUserMenu = false;
            }, 300); // 300ms延迟
        },

        cancelHideMenu() {
            if (this.menuHideTimer) {
                clearTimeout(this.menuHideTimer);
                this.menuHideTimer = null;
            }
        },

        // 健康菜单控制方法
        handleHealthMenuLeave() {
            this.healthMenuHideTimer = setTimeout(() => {
                this.showHealthMenu = false;
            }, 300); // 300ms延迟
        },

        cancelHealthMenuHide() {
            if (this.healthMenuHideTimer) {
                clearTimeout(this.healthMenuHideTimer);
                this.healthMenuHideTimer = null;
            }
        }
    },

    computed: {
        // 正在进行中的目标（活跃且未完成100%）
        activeGoals() {
            return this.healthGoals.filter(goal =>
                goal.is_active && this.getProgressPercentage(goal) < 100
            );
        },

        // 已完成的目标（活跃且完成100%）
        completedGoals() {
            return this.healthGoals.filter(goal =>
                goal.is_active && this.getProgressPercentage(goal) >= 100
            );
        },

        // 所有显示的目标（进行中优先，然后是已完成）
        displayGoals() {
            return [...this.activeGoals, ...this.completedGoals];
        }
    }
};
</script>

<style scoped>
.dashboard {
    min-height: 100vh;
    background: #f5f7fa;
}

/* 头部样式 */
.header {
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 64px;
}

.header h1 {
    color: #2c3e50;
    margin: 0;
    font-size: 24px;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 20px;
}

.current-time {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    color: #2c3e50;
}

.time-display {
    font-size: 18px;
    font-weight: bold;
    color: #409eff;
}

.date-display {
    font-size: 12px;
    color: #666;
    margin-top: 2px;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 15px;
}

.user-info span {
    color: #555;
    font-size: 14px;
}

.inbox-badge {
    position: relative;
    background: #f5f7fa;
    color: #666;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s;
    border: 1px solid #e1e8ed;
}

.inbox-badge:hover {
    background: #e8f4fd;
    border-color: #409eff;
    color: #409eff;
}

.inbox-badge.has-unread {
    background: linear-gradient(135deg, #409eff, #337ecc);
    color: white;
    border-color: #409eff;
}

.inbox-badge.has-unread:hover {
    background: linear-gradient(135deg, #337ecc, #2b66a3);
    transform: scale(1.05);
}

.inbox-badge svg {
    width: 16px;
    height: 16px;
}

.badge-count {
    position: absolute;
    top: -6px;
    right: -6px;
    background: #ff4757;
    color: white;
    font-size: 9px;
    font-weight: bold;
    padding: 1px 5px;
    border-radius: 8px;
    min-width: 14px;
    text-align: center;
    line-height: 1.3;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.inbox-badge.has-unread .badge-count {
    background: #ff4757;
    color: white;
}

.profile-btn {
    background: #409eff;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: background-color 0.3s;
}

.profile-btn svg {
    width: 16px;
    height: 16px;
}

.profile-btn:hover {
    background: #337ecc;
}

/* 用户下拉菜单样式 */
.user-dropdown {
    position: relative;
    display: flex;
    align-items: center;
}

.user-trigger {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: #f8f9fa;
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.user-trigger:hover {
    background: #e9ecef;
    border-color: #409eff;
    box-shadow: 0 2px 8px rgba(64, 158, 255, 0.15);
}

.user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    color: #495057;
    border: 2px solid #dee2e6;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 13px;
    transition: all 0.3s ease;
}

.user-trigger:hover .user-avatar {
    background: linear-gradient(135deg, #409eff, #5a6fd8);
    color: white;
    border-color: #409eff;
}

.dropdown-arrow {
    width: 16px;
    height: 16px;
    color: #666;
    transition: transform 0.3s ease;
}

.dropdown-arrow.rotated {
    transform: rotate(180deg);
}

.user-menu {
    position: absolute;
    top: 100%;
    right: 0;
    z-index: 1000;
    background: white;
    border: 1px solid #e1e8ed;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    min-width: 280px;
    margin-top: 8px; /* 增加一些间距便于鼠标移动 */
    padding: 0;
    overflow: hidden;
    animation: fadeInDown 0.3s ease;
}

/* 在菜单和触发器之间添加一个不可见的连接区域 */
.user-menu::before {
    content: '';
    position: absolute;
    top: -12px; /* 增加缓冲区域 */
    left: 0;
    right: 0;
    height: 12px;
    background: transparent;
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.menu-header {
    padding: 20px;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    color: #495057;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid #dee2e6;
}

.menu-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #409eff, #667eea);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 18px;
    box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.menu-user-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.menu-username {
    font-size: 16px;
    font-weight: 600;
    color: #2c3e50;
}

.menu-welcome {
    font-size: 12px;
    opacity: 0.7;
    color: #6c757d;
}

.menu-divider {
    height: 1px;
    background: #e1e8ed;
    margin: 0;
    display: none; /* 不再需要，因为header已有边框 */
}

.menu-items {
    list-style: none;
    padding: 8px 0;
    margin: 0;
}

.menu-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    cursor: pointer;
    transition: background-color 0.2s;
    color: #2c3e50;
}

.menu-item:hover {
    background: #f8f9fa;
}

.menu-item.logout-item {
    color: #f56c6c;
}

.menu-item.logout-item:hover {
    background: rgba(245, 108, 108, 0.1);
}

.menu-icon {
    width: 18px;
    height: 18px;
    color: #666;
}

.menu-item.logout-item .menu-icon {
    color: #f56c6c;
}

.menu-item span {
    font-size: 14px;
    font-weight: 500;
}

.logout-btn {
    background: #f56c6c;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
    display: none; /* 隐藏原来的退出按钮，已整合到下拉菜单 */
}

.logout-btn:hover {
    background: #f04747;
}

/* 健康管理下拉菜单样式 */
.health-management-btn {
    position: relative;
    background: white;
    border: 2px solid #e1e8ed;
    padding: 20px;
    border-radius: 12px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    font-size: 16px;
    color: #2c3e50;
    transition: all 0.3s;
}

.health-trigger {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    position: relative;
}

.btn-text {
    font-weight: 500;
}

.dropdown-arrow {
    width: 16px;
    height: 16px;
    transition: transform 0.3s ease;
}

.dropdown-arrow.rotated {
    transform: rotate(180deg);
}

.health-menu {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border: 1px solid #e1e8ed;
    min-width: 200px;
    z-index: 1000;
    overflow: hidden;
    margin-top: 8px;
}

.health-menu::before {
    content: '';
    position: absolute;
    top: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 8px solid white;
}

.health-menu-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    cursor: pointer;
    transition: background-color 0.2s;
    color: #2c3e50;
    border-bottom: 1px solid #f8f9fa;
}

.health-menu-item:last-child {
    border-bottom: none;
}

.health-menu-item:hover {
    background: #f8f9fa;
}

.health-menu-item .menu-icon {
    width: 18px;
    height: 18px;
    color: #666;
}

.health-menu-item span {
    font-size: 14px;
    font-weight: 500;
}

/* 主要内容样式 */
.main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 30px 20px;
}

.overview-section,
.actions-section,
.bottom-section {
    margin-bottom: 40px;
}

.overview-section h2,
.actions-section h2,
.recent-section h2,
.goals-section h2 {
    color: #2c3e50;
    margin-bottom: 20px;
    font-size: 20px;
}

/* 底部布局 - 最近记录和健康目标 */
.bottom-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
}

.recent-section,
.goals-section {
    margin-bottom: 0;
}

/* 概览卡片样式 */
.overview-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 16px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
}

.card-icon svg {
    width: 24px;
    height: 24px;
    color: #666;
}

.sleep-card .card-icon {
    background: rgba(155, 89, 182, 0.1);
}

.sleep-card .card-icon svg {
    color: #9b59b6;
}

.exercise-card .card-icon {
    background: rgba(39, 174, 96, 0.1);
}

.exercise-card .card-icon svg {
    color: #27ae60;
}

.diet-card .card-icon {
    background: rgba(230, 126, 34, 0.1);
}

.diet-card .card-icon svg {
    color: #e67e22;
}

.weight-card .card-icon {
    background: rgba(32, 178, 170, 0.1);
}

.weight-card .card-icon svg {
    color: #20b2aa;
}

.card-content h3 {
    margin: 0 0 8px 0;
    color: #666;
    font-size: 14px;
    font-weight: normal;
}

.card-value {
    font-size: 28px;
    font-weight: bold;
    margin: 0;
    color: #2c3e50;
}

.card-unit {
    color: #999;
    font-size: 12px;
}

/* 快捷操作样式 */
.quick-actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}

.action-btn {
    background: white;
    border: 2px solid #e1e8ed;
    padding: 20px;
    border-radius: 12px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    font-size: 16px;
    color: #2c3e50;
    transition: all 0.3s;
}

.action-btn:hover {
    border-color: #409eff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.profile-btn:hover {
    border-color: #409eff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.sleep-btn:hover {
    border-color: #9b59b6;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(155, 89, 182, 0.2);
}

.exercise-btn:hover {
    border-color: #27ae60;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(39, 174, 96, 0.2);
}

.diet-btn:hover {
    border-color: #e67e22;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(230, 126, 34, 0.2);
}

.social-hub-btn:hover {
    border-color: #409eff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.health-report-btn:hover {
    border-color: #409eff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.health-alerts-btn:hover {
    border-color: #f56c6c;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(245, 108, 108, 0.2);
}

.health-management-btn:hover {
    border-color: #17a2b8;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(23, 162, 184, 0.2);
}

.sleep-btn .btn-icon svg {
    color: #9b59b6; /* 紫色 - 睡眠相关 */
}

.exercise-btn .btn-icon svg {
    color: #27ae60; /* 绿色 - 运动相关 */
}

.diet-btn .btn-icon svg {
    color: #e67e22; /* 橙色 - 饮食相关 */
}

.social-hub-btn .btn-icon svg {
    color: #409eff; /* 蓝色 - 社交相关 */
}

.health-report-btn .btn-icon svg {
    color: #409eff;
}

.health-alerts-btn .btn-icon svg {
    color: #f56c6c;
}

.health-management-btn .btn-icon svg {
    color: #17a2b8;
}

.social-report-btn .btn-icon svg {
    color: #409eff;
}

.btn-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-icon svg {
    width: 24px;
    height: 24px;
    color: #409eff;
}



/* 最近记录样式 */
.recent-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
    height: 44px; /* 固定高度，确保对齐 */
    align-items: center;
}

.tab-btn {
    padding: 10px 20px;
    background: white;
    border: 1px solid #e1e8ed;
    border-radius: 6px;
    cursor: pointer;
    color: #666;
    transition: all 0.3s;
}

.tab-btn.active {
    background: #409eff;
    color: white;
    border-color: #409eff;
}

.tab-btn:hover:not(.active) {
    background: #f5f7fa;
}

.recent-content {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    min-height: 200px; /* 减小最小高度 */
}

.scroll-hint {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px 12px;
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 6px;
    color: #6c757d;
    font-size: 12px;
    margin-bottom: 12px;
}

.scroll-icon {
    width: 14px;
    height: 14px;
    animation: scrollBounce 2s ease-in-out infinite;
}

@keyframes scrollBounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(2px);
    }
    60% {
        transform: translateY(1px);
    }
}

/* 健康目标头部样式 */
.goals-header {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin-bottom: 20px;
    height: 44px; /* 与 recent-tabs 相同高度 */
}

.goals-status {
    display: flex;
    align-items: center;
}

.goals-count {
    padding: 10px 16px;
    background: #f8f9fa;
    border: 1px solid #e1e8ed;
    border-radius: 6px;
    color: #666;
    font-size: 14px;
    margin-right: 8px;
}

.goals-count:last-child {
    margin-right: 0;
}

.goals-count.active {
    background: rgba(64, 158, 255, 0.1);
    border-color: rgba(64, 158, 255, 0.3);
    color: #409eff;
}

.goals-count.completed {
    background: rgba(103, 194, 58, 0.1);
    border-color: rgba(103, 194, 58, 0.3);
    color: #67c23a;
}

.goals-content {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    min-height: 200px; /* 与 recent-content 相同的最小高度 */
    display: flex;
    flex-direction: column;
}

.records-list {
    max-height: 200px;
    overflow-y: auto;
    /* 优化滚动条样式 */
    scrollbar-width: thin;
    scrollbar-color: #ddd #f5f5f5;
}

/* Webkit 浏览器的滚动条样式 */
.records-list::-webkit-scrollbar {
    width: 6px;
}

.records-list::-webkit-scrollbar-track {
    background: #f5f5f5;
    border-radius: 3px;
}

.records-list::-webkit-scrollbar-thumb {
    background: #ddd;
    border-radius: 3px;
}

.records-list::-webkit-scrollbar-thumb:hover {
    background: #bbb;
}

.record-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #f0f0f0;
}

.record-item:last-child {
    border-bottom: none;
}

.record-date {
    color: #999;
    font-size: 14px;
    min-width: 80px;
}

.record-detail {
    color: #2c3e50;
    flex: 1;
    text-align: right;
}

.no-data {
    text-align: center;
    color: #999;
    padding: 40px;
    font-style: italic;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .header-content {
        padding: 0 15px;
    }

    .header h1 {
        font-size: 20px;
    }

    .header-right {
        gap: 10px;
    }

    .current-time {
        display: none;
        /* 在小屏幕上隐藏时间显示 */
    }

    .user-info span {
        display: none; /* 隐藏欢迎文字 */
    }

    .user-trigger {
        padding: 6px 8px;
    }

    .user-avatar {
        width: 28px;
        height: 28px;
        font-size: 12px;
    }

    .user-trigger:hover .user-avatar {
        background: linear-gradient(135deg, #409eff, #5a6fd8);
        color: white;
        border-color: #409eff;
    }

    .user-menu {
        min-width: 240px;
        right: -20px; /* 调整位置避免超出屏幕 */
    }

    .menu-header {
        padding: 16px;
    }

    .menu-avatar {
        width: 40px;
        height: 40px;
        font-size: 16px;
    }

    .menu-username {
        font-size: 14px;
    }

    .menu-welcome {
        font-size: 11px;
    }

    .menu-item {
        padding: 10px 16px;
    }

    .profile-btn {
        padding: 6px 8px;
        font-size: 12px;
    }

    .profile-btn svg {
        width: 14px;
        height: 14px;
    }

    .main-content {
        padding: 20px 15px;
    }

    .overview-cards {
        grid-template-columns: 1fr;
    }

    .quick-actions {
        grid-template-columns: repeat(2, 1fr);
    }

    .record-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }

    .record-detail {
        text-align: left;
    }

    .bottom-section {
        grid-template-columns: 1fr;
        gap: 20px;
    }
}

/* 健康目标样式 */
.no-goals {
    text-align: center;
    padding: 20px 0;
    color: #666;
}

.no-goals-icon {
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    color: #409eff;
}

.no-goals p {
    margin-bottom: 20px;
    font-size: 16px;
}

.create-goal-btn,
.edit-goals-btn {
    background: #409eff;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 auto;
}

.create-goal-btn:hover,
.edit-goals-btn:hover {
    background: #367ddd;
}

.goals-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.goal-item {
    padding: 16px;
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    background: #f8f9fa;
    transition: background-color 0.3s;
}

.goal-item:hover {
    background: #e9ecef;
}

.goal-item.completed-goal {
    background: rgba(103, 194, 58, 0.05);
    border-color: rgba(103, 194, 58, 0.2);
}

.goal-item.completed-goal:hover {
    background: rgba(103, 194, 58, 0.1);
}

.goal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.goal-type {
    font-weight: 600;
    color: #2c3e50;
    font-size: 16px;
}

.goal-period {
    font-size: 12px;
    color: #666;
    background: #e1e8ed;
    padding: 4px 8px;
    border-radius: 4px;
}

.goal-period.completed-period {
    background: rgba(103, 194, 58, 0.2);
    color: #67c23a;
    font-weight: 600;
}

.goal-progress {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.progress-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.progress-text {
    font-size: 14px;
    color: #555;
}

.progress-percentage {
    font-weight: 600;
    color: #409eff;
    font-size: 14px;
}

.progress-bar {
    height: 8px;
    background: #e1e8ed;
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #409eff, #67c23a);
    border-radius: 4px;
    transition: width 0.3s ease;
}

.progress-fill.completed {
    background: linear-gradient(90deg, #67c23a, #85ce61);
    box-shadow: 0 0 8px rgba(103, 194, 58, 0.3);
}

.progress-fill.over-achieved {
    background: linear-gradient(90deg, #f56c6c, #ff9500);
    box-shadow: 0 0 12px rgba(255, 149, 0, 0.4);
    animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
    0%, 100% {
        box-shadow: 0 0 12px rgba(255, 149, 0, 0.4);
    }
    50% {
        box-shadow: 0 0 20px rgba(255, 149, 0, 0.6);
    }
}

.progress-percentage.completed {
    color: #67c23a;
    font-weight: bold;
}

.progress-percentage.over-achieved {
    color: #ff9500;
    font-weight: bold;
}

.completion-badge {
    margin-left: 6px;
    animation: bounce 1s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-3px);
    }
    60% {
        transform: translateY(-2px);
    }
}

.completion-message {
    margin-top: 8px;
    text-align: center;
    font-size: 12px;
    font-weight: 600;
}

.completed-text {
    color: #67c23a;
    padding: 4px 8px;
    background: rgba(103, 194, 58, 0.1);
    border-radius: 12px;
    border: 1px solid rgba(103, 194, 58, 0.3);
}

.over-achieved-text {
    color: #ff9500;
    padding: 4px 8px;
    background: rgba(255, 149, 0, 0.1);
    border-radius: 12px;
    border: 1px solid rgba(255, 149, 0, 0.3);
    animation: celebration-glow 2s infinite;
    display: flex;
    align-items: center;
    gap: 6px;
    justify-content: center;
}

.completed-text {
    display: flex;
    align-items: center;
    gap: 6px;
    justify-content: center;
}

.achievement-icon {
    width: 16px;
    height: 16px;
}

@keyframes celebration-glow {
    0%, 100% {
        background: rgba(255, 149, 0, 0.1);
        border-color: rgba(255, 149, 0, 0.3);
    }
    50% {
        background: rgba(255, 149, 0, 0.2);
        border-color: rgba(255, 149, 0, 0.5);
    }
}

.goals-actions {
    margin-top: 16px;
    text-align: center;
}

.edit-goals-btn svg {
    width: 16px;
    height: 16px;
}
</style>