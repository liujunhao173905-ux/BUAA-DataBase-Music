<template>
    <div class="health-report">
        <!-- 头部导航 -->
        <header class="report-header">
            <h1>
                <svg viewBox="0 0 24 24" fill="currentColor" class="header-icon">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                </svg>
                健康报告
            </h1>
            <button @click="$router.push('/dashboard')" class="back-btn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.42-1.41L7.83 13H20v-2z"/>
                </svg>
                返回首页
            </button>
        </header>

        <!-- 报告生成控制面板 -->
        <div class="report-controls">
            <div class="control-section">
                <h3>选择报告类型</h3>
                <div class="report-type-buttons">
                    <button
                        v-for="tab in tabs"
                        :key="tab.key"
                        @click="activeTab = tab.key"
                        :class="['type-btn', { active: activeTab === tab.key }]"
                    >
                        <svg viewBox="0 0 24 24" fill="currentColor" class="type-icon">
                            <path v-if="tab.icon === 'chart-bar'" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                            <path v-else-if="tab.icon === 'chart-line'" d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
                            <path v-else-if="tab.icon === 'analytics'" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                        </svg>
                        <div class="type-info">
                            <span class="type-name">{{ tab.label }}</span>
                            <span class="type-desc">{{ getReportDescription(tab.key) }}</span>
                        </div>
                    </button>
                </div>
            </div>

            <!-- 时间范围选择 -->
            <div class="control-section">
                <h3>选择时间范围</h3>
                <div class="time-selection">
                    <!-- 周报时间选择 -->
                    <div v-if="activeTab === 'weekly'" class="week-selection">
                        <div class="week-options">
                            <button
                                v-for="(option, index) in weekOptions"
                                :key="index"
                                @click="selectedWeek = option.value"
                                :class="['week-option', { active: selectedWeek === option.value }]"
                            >
                                {{ option.label }}
                            </button>
                        </div>
                    </div>

                    <!-- 月报时间选择 -->
                    <div v-if="activeTab === 'monthly'" class="month-selection">
                        <div class="month-options">
                            <button
                                v-for="(option, index) in monthOptions"
                                :key="index"
                                @click="selectedMonth = option.value"
                                :class="['month-option', { active: selectedMonth === option.value }]"
                            >
                                {{ option.label }}
                            </button>
                        </div>
                    </div>

                    <!-- 综合分析时间选择 -->
                    <div v-if="activeTab === 'comprehensive'" class="period-selection">
                        <div class="period-options">
                            <button
                                v-for="(option, index) in periodOptions"
                                :key="index"
                                @click="selectedPeriod = option.value"
                                :class="['period-option', { active: selectedPeriod === option.value }]"
                            >
                                {{ option.label }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 生成报告按钮 -->
            <div class="generate-section">
                <button
                    @click="generateReport"
                    :disabled="loading || !canGenerate"
                    class="generate-btn"
                >
                    <svg v-if="loading" viewBox="0 0 24 24" class="spin">
                        <path fill="currentColor" d="M12,4a8,8 0 0,1 7.89,6.7 1.53,1.53 0 0,0 1.49,1.3 1.5,1.5 0 0,0 1.48-1.75 11,11 0 0,0-21.72,0 1.5,1.5 0 0,0 1.48,1.75 1.53,1.53 0 0,0 1.49-1.3A8,8 0 0,1 12,4Z"/>
                    </svg>
                    <span v-else>生成健康报告</span>
                </button>
                <p class="generate-tip">点击按钮生成选定时间范围的健康报告</p>
            </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-container">
            <div class="loading-spinner">
                <svg viewBox="0 0 24 24" class="spin">
                    <path fill="currentColor" d="M12,4a8,8 0 0,1 7.89,6.7 1.53,1.53 0 0,0 1.49,1.3 1.5,1.5 0 0,0 1.48-1.75 11,11 0 0,0-21.72,0 1.5,1.5 0 0,0 1.48,1.75 1.53,1.53 0 0,0 1.49-1.3A8,8 0 0,1 12,4Z"/>
                </svg>
            </div>
            <p>正在生成健康报告...</p>
        </div>

        <!-- 报告内容 -->
        <main v-else-if="currentReport" class="report-content">
            <!-- 周报 -->
            <div v-if="activeTab === 'weekly' && weeklyReport" class="report-section">
                <div class="report-header-section">
                    <h2>周健康报告</h2>
                    <div class="period-info">
                        <span>报告周期：{{ weeklyReport.period.start_date }} 至 {{ weeklyReport.period.end_date }}</span>
                        <div class="health-score">
                            <span class="score-label">健康评分</span>
                            <span :class="['score-value', getScoreClass(weeklyReport.overall_score)]">
                                {{ weeklyReport.overall_score }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- 数据概览卡片 -->
                <div class="overview-cards">
                    <div class="overview-card sleep-card">
                        <svg viewBox="0 0 24 24" fill="currentColor" class="card-icon">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                        </svg>
                        <div class="card-content">
                            <h3>睡眠质量</h3>
                            <div class="card-stats">
                                <span class="main-stat">{{ weeklyReport.sleep_analysis.summary.avg_hours_per_night }}小时</span>
                                <span class="sub-stat">平均每晚</span>
                            </div>
                            <div class="quality-indicator">
                                质量评分：{{ weeklyReport.sleep_analysis.summary.avg_quality }}/5
                            </div>
                        </div>
                    </div>

                    <div class="overview-card exercise-card">
                        <svg viewBox="0 0 24 24" fill="currentColor" class="card-icon">
                            <path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z"/>
                        </svg>
                        <div class="card-content">
                            <h3>运动情况</h3>
                            <div class="card-stats">
                                <span class="main-stat">{{ weeklyReport.exercise_analysis.summary.total_minutes }}分钟</span>
                                <span class="sub-stat">本周总计</span>
                            </div>
                            <div class="quality-indicator">
                                {{ weeklyReport.exercise_analysis.summary.total_sessions }}次运动
                            </div>
                        </div>
                    </div>

                    <div class="overview-card diet-card">
                        <svg viewBox="0 0 24 24" fill="currentColor" class="card-icon">
                            <path d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z"/>
                        </svg>
                        <div class="card-content">
                            <h3>饮食营养</h3>
                            <div class="card-stats">
                                <span class="main-stat">{{ Math.round(weeklyReport.diet_analysis.summary.avg_calories_per_day) }}</span>
                                <span class="sub-stat">日均卡路里</span>
                            </div>
                            <div class="quality-indicator">
                                {{ weeklyReport.diet_analysis.summary.total_meals }}餐记录
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 详细分析 -->
                <div class="analysis-sections">
                    <!-- 睡眠分析 -->
                    <div class="analysis-card">
                        <h3>睡眠详细分析</h3>
                        <div class="sleep-details">
                            <div v-if="weeklyReport.sleep_analysis.details.length === 0" class="no-data">
                                本周暂无睡眠记录
                            </div>
                            <div v-else class="sleep-records">
                                <div v-for="sleep in weeklyReport.sleep_analysis.details" :key="sleep.date" class="sleep-record">
                                    <span class="date">{{ formatDate(sleep.date) }}</span>
                                    <span class="duration">{{ sleep.duration }}小时</span>
                                    <span class="time-range">{{ sleep.sleep_time }} - {{ sleep.wake_time }}</span>
                                    <span :class="['quality', 'quality-' + sleep.quality]">
                                        {{ getQualityText(sleep.quality) }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 运动分析 -->
                    <div class="analysis-card">
                        <h3>运动类型分布</h3>
                        <div class="exercise-distribution">
                            <div v-if="Object.keys(weeklyReport.exercise_analysis.by_type).length === 0" class="no-data">
                                本周暂无运动记录
                            </div>
                            <div v-else class="exercise-types">
                                <div v-for="(data, type) in weeklyReport.exercise_analysis.by_type" :key="type" class="exercise-type">
                                    <div class="type-header">
                                        <span class="type-name">{{ type }}</span>
                                        <span class="type-count">{{ data.count }}次</span>
                                    </div>
                                    <div class="type-stats">
                                        <span>{{ data.total_minutes }}分钟</span>
                                        <span>{{ Math.round(data.total_calories) }}卡路里</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 饮食分析 -->
                    <div class="analysis-card">
                        <h3>营养成分分析</h3>
                        <div class="nutrition-breakdown">
                            <div class="nutrition-item">
                                <span class="nutrient-name">蛋白质</span>
                                <span class="nutrient-value">{{ Math.round(weeklyReport.diet_analysis.summary.total_protein) }}g</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrient-name">碳水化合物</span>
                                <span class="nutrient-value">{{ Math.round(weeklyReport.diet_analysis.summary.total_carbs) }}g</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrient-name">脂肪</span>
                                <span class="nutrient-value">{{ Math.round(weeklyReport.diet_analysis.summary.total_fat) }}g</span>
                            </div>
                            <div class="nutrition-item">
                                <span class="nutrient-name">纤维</span>
                                <span class="nutrient-value">{{ Math.round(weeklyReport.diet_analysis.summary.total_fiber) }}g</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 目标达成情况 -->
                <div v-if="weeklyReport.goal_progress.length > 0" class="goals-section">
                    <h3>目标达成情况</h3>
                    <div class="goals-list">
                        <div v-for="goal in weeklyReport.goal_progress" :key="goal.goal_type" class="goal-item">
                            <div class="goal-info">
                                <span class="goal-type">{{ goal.goal_type }}</span>
                                <span :class="['goal-status', { achieved: goal.achieved }]">
                                    {{ goal.achieved ? '已达成' : '未达成' }}
                                </span>
                            </div>
                            <div class="goal-progress">
                                <div class="progress-bar">
                                    <div
                                        class="progress-fill"
                                        :style="{ width: Math.min(goal.progress_percentage, 100) + '%' }"
                                        :class="{ achieved: goal.achieved }"
                                    ></div>
                                </div>
                                <span class="progress-text">
                                    {{ goal.current_value }} / {{ goal.target_value }} ({{ goal.progress_percentage }}%)
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 健康建议 -->
                <div v-if="weeklyReport.recommendations.length > 0" class="recommendations-section">
                    <h3>健康建议</h3>
                    <div class="recommendations-list">
                        <div v-for="(rec, index) in weeklyReport.recommendations" :key="index" class="recommendation-item">
                            <div :class="['priority-indicator', rec.priority]"></div>
                            <div class="recommendation-content">
                                <h4>{{ rec.title }}</h4>
                                <p>{{ rec.content }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 月报 -->
            <div v-if="activeTab === 'monthly' && monthlyReport" class="report-section">
                <div class="report-header-section">
                    <h2>月健康报告</h2>
                    <div class="period-info">
                        <span>报告月份：{{ monthlyReport.period.year }}年{{ monthlyReport.period.month }}月</span>
                        <div class="health-score">
                            <span class="score-label">健康评分</span>
                            <span :class="['score-value', getScoreClass(monthlyReport.health_score)]">
                                {{ monthlyReport.health_score }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- 月度概览 -->
                <div class="monthly-overview">
                    <div class="overview-card">
                        <h3>睡眠统计</h3>
                        <div class="monthly-stats">
                            <div class="stat-item">
                                <span class="stat-value">{{ monthlyReport.monthly_summary.sleep.avg_hours_per_night }}</span>
                                <span class="stat-label">平均睡眠时间(小时)</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-value">{{ monthlyReport.monthly_summary.sleep.consistency_rate }}%</span>
                                <span class="stat-label">记录一致性</span>
                            </div>
                        </div>
                    </div>

                    <div class="overview-card">
                        <h3>运动统计</h3>
                        <div class="monthly-stats">
                            <div class="stat-item">
                                <span class="stat-value">{{ monthlyReport.monthly_summary.exercise.total_minutes }}</span>
                                <span class="stat-label">总运动时间(分钟)</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-value">{{ monthlyReport.monthly_summary.exercise.total_sessions }}</span>
                                <span class="stat-label">运动次数</span>
                            </div>
                        </div>
                    </div>

                    <div class="overview-card">
                        <h3>饮食统计</h3>
                        <div class="monthly-stats">
                            <div class="stat-item">
                                <span class="stat-value">{{ Math.round(monthlyReport.monthly_summary.diet.avg_calories_per_day) }}</span>
                                <span class="stat-label">日均卡路里</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-value">{{ monthlyReport.monthly_summary.diet.total_meals }}</span>
                                <span class="stat-label">总餐数</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 周度趋势 -->
                <div class="weekly-breakdown">
                    <h3>周度数据趋势</h3>
                    <div class="weeks-container">
                        <div v-for="week in monthlyReport.weekly_breakdown" :key="week.week" class="week-card">
                            <div class="week-header">
                                <span class="week-number">第{{ week.week }}周</span>
                                <span class="week-period">{{ formatDate(week.start_date) }} - {{ formatDate(week.end_date) }}</span>
                            </div>
                            <div class="week-stats">
                                <div class="week-stat sleep-stat">
                                    <svg viewBox="0 0 24 24" fill="currentColor" class="stat-icon">
                                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                                    </svg>
                                    <span class="stat-text">{{ week.sleep_hours }}h</span>
                                </div>
                                <div class="week-stat exercise-stat">
                                    <svg viewBox="0 0 24 24" fill="currentColor" class="stat-icon">
                                        <path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z"/>
                                    </svg>
                                    <span class="stat-text">{{ week.exercise_minutes }}min</span>
                                </div>
                                <div class="week-stat diet-stat">
                                    <svg viewBox="0 0 24 24" fill="currentColor" class="stat-icon">
                                        <path d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z"/>
                                    </svg>
                                    <span class="stat-text">{{ Math.round(week.diet_calories) }}cal</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 趋势分析 -->
                <div v-if="monthlyReport.trends && monthlyReport.trends.message !== '数据不足，无法分析趋势'" class="trends-section">
                    <h3>趋势分析</h3>
                    <div class="trends-grid">
                        <div class="trend-item sleep-trend">
                            <span class="trend-label">睡眠趋势</span>
                            <span :class="['trend-value', monthlyReport.trends.sleep_trend]">
                                <svg viewBox="0 0 24 24" fill="currentColor" class="trend-icon">
                                    <path v-if="getTrendText(monthlyReport.trends.sleep_trend).icon === 'trending-up'" d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
                                    <path v-else-if="getTrendText(monthlyReport.trends.sleep_trend).icon === 'trending-down'" d="M16 18l2.29-2.29-4.88-4.88-4 4L2 7.41 3.41 6l6 6 4-4 6.3 6.29L22 12v6z"/>
                                    <path v-else d="M22 12l-4-4v3H3v2h15v3z"/>
                                </svg>
                                {{ getTrendText(monthlyReport.trends.sleep_trend).text }}
                            </span>
                        </div>
                        <div class="trend-item exercise-trend">
                            <span class="trend-label">运动趋势</span>
                            <span :class="['trend-value', monthlyReport.trends.exercise_trend]">
                                <svg viewBox="0 0 24 24" fill="currentColor" class="trend-icon">
                                    <path v-if="getTrendText(monthlyReport.trends.exercise_trend).icon === 'trending-up'" d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
                                    <path v-else-if="getTrendText(monthlyReport.trends.exercise_trend).icon === 'trending-down'" d="M16 18l2.29-2.29-4.88-4.88-4 4L2 7.41 3.41 6l6 6 4-4 6.3 6.29L22 12v6z"/>
                                    <path v-else d="M22 12l-4-4v3H3v2h15v3z"/>
                                </svg>
                                {{ getTrendText(monthlyReport.trends.exercise_trend).text }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 综合分析 -->
            <div v-if="activeTab === 'comprehensive' && comprehensiveReport" class="report-section">
                <div class="report-header-section">
                    <h2>综合健康分析</h2>
                    <div class="period-info">
                        <span>分析周期：{{ comprehensiveReport.period.analysis_period.replace('months', '个月').replace('year', '年') }}</span>
                        <div class="health-score">
                            <span class="score-label">综合评分</span>
                            <span :class="['score-value', getScoreClass(comprehensiveReport.overall_health_score)]">
                                {{ comprehensiveReport.overall_health_score }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- 长期趋势 -->
                <div class="long-term-trends">
                    <h3>长期趋势分析</h3>
                    <div class="trends-grid">
                        <div class="trend-card">
                            <h4>睡眠趋势</h4>
                            <span class="trend-status">{{ comprehensiveReport.trends.sleep_trend }}</span>
                        </div>
                        <div class="trend-card">
                            <h4>运动趋势</h4>
                            <span class="trend-status">{{ comprehensiveReport.trends.exercise_trend }}</span>
                        </div>
                        <div class="trend-card">
                            <h4>饮食趋势</h4>
                            <span class="trend-status">{{ comprehensiveReport.trends.diet_trend }}</span>
                        </div>
                        <div class="trend-card">
                            <h4>整体趋势</h4>
                            <span class="trend-status positive">{{ comprehensiveReport.trends.overall_trend }}</span>
                        </div>
                    </div>
                </div>

                <!-- 健康模式识别 -->
                <div class="health-patterns">
                    <h3>健康模式识别</h3>
                    <div class="patterns-grid">
                        <div class="pattern-category sleep-pattern">
                            <h4>睡眠模式</h4>
                            <ul>
                                <li v-for="pattern in comprehensiveReport.patterns.sleep_patterns" :key="pattern">
                                    {{ pattern }}
                                </li>
                            </ul>
                        </div>
                        <div class="pattern-category exercise-pattern">
                            <h4>运动模式</h4>
                            <ul>
                                <li v-for="pattern in comprehensiveReport.patterns.exercise_patterns" :key="pattern">
                                    {{ pattern }}
                                </li>
                            </ul>
                        </div>
                        <div class="pattern-category diet-pattern">
                            <h4>饮食模式</h4>
                            <ul>
                                <li v-for="pattern in comprehensiveReport.patterns.diet_patterns" :key="pattern">
                                    {{ pattern }}
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- 个性化建议 -->
                <div class="personalized-advice">
                    <h3>个性化建议</h3>
                    <div class="advice-list">
                        <div v-for="advice in comprehensiveReport.personalized_advice" :key="advice.category"
                             :class="['advice-item', getAdviceCategoryClass(advice.category)]">
                            <h4>{{ advice.category }}</h4>
                            <p>{{ advice.advice }}</p>
                        </div>
                    </div>
                </div>

                <!-- 成就系统 -->
                <div class="achievements-section">
                    <h3>健康成就</h3>
                    <div class="achievements-grid">
                        <div v-for="achievement in comprehensiveReport.achievements" :key="achievement.title"
                             :class="['achievement-item', { achieved: achievement.achieved }]">
                            <div class="achievement-icon">
                                <svg v-if="achievement.achieved" viewBox="0 0 24 24" fill="currentColor" class="achievement-svg">
                                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                                </svg>
                                <svg v-else viewBox="0 0 24 24" fill="currentColor" class="achievement-svg locked">
                                    <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                                </svg>
                            </div>
                            <div class="achievement-content">
                                <h4>{{ achievement.title }}</h4>
                                <p v-if="achievement.achieved">达成时间：{{ achievement.date }}</p>
                                <p v-else>尚未达成</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 改进计划 -->
                <div class="improvement-plan">
                    <h3>改进计划</h3>
                    <div class="plan-sections">
                        <div class="plan-section">
                            <h4>短期目标</h4>
                            <ul>
                                <li v-for="goal in comprehensiveReport.improvement_suggestions.short_term" :key="goal">
                                    {{ goal }}
                                </li>
                            </ul>
                        </div>
                        <div class="plan-section">
                            <h4>长期目标</h4>
                            <ul>
                                <li v-for="goal in comprehensiveReport.improvement_suggestions.long_term" :key="goal">
                                    {{ goal }}
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <!-- 无报告状态 -->
        <div v-else-if="!loading" class="no-report">
            <div class="no-report-content">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                </svg>
                <h3>请选择报告类型和时间范围</h3>
                <p>选择好后点击"生成健康报告"按钮查看您的健康报告</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'HealthReport',
    data() {
        return {
            activeTab: 'weekly',
            loading: false,
            tabs: [
                { key: 'weekly', label: '周报', icon: 'chart-bar' },
                { key: 'monthly', label: '月报', icon: 'chart-line' },
                { key: 'comprehensive', label: '综合分析', icon: 'analytics' }
            ],
            weeklyReport: null,
            monthlyReport: null,
            comprehensiveReport: null,
            // 新增选择项
            selectedWeek: null,
            selectedMonth: null,
            selectedPeriod: null,
            // 周选项
            weekOptions: [
                { label: '上一周', value: 'last-week', description: '查看上一周的健康数据' },
                { label: '上上周', value: 'last-2-week', description: '查看两周前的健康数据' },
                { label: '上上上周', value: 'last-3-week', description: '查看三周前的健康数据' }
            ],
            // 月选项
            monthOptions: [
                { label: '上个月', value: 'last-month', description: '查看上个月的健康数据' },
                { label: '上上个月', value: 'last-2-month', description: '查看两个月前的健康数据' },
                { label: '上上上个月', value: 'last-3-month', description: '查看三个月前的健康数据' }
            ],
            // 综合分析选项
            periodOptions: [
                { label: '最近3个月', value: '3months', description: '分析最近3个月的健康趋势' },
                { label: '最近6个月', value: '6months', description: '分析最近6个月的健康趋势' },
                { label: '最近1年', value: '1year', description: '分析最近1年的健康趋势' }
            ]
        };
    },
    computed: {
        // 当前报告
        currentReport() {
            if (this.activeTab === 'weekly') {
                return this.weeklyReport;
            } else if (this.activeTab === 'monthly') {
                return this.monthlyReport;
            } else if (this.activeTab === 'comprehensive') {
                return this.comprehensiveReport;
            }
            return null;
        },
        // 是否可以生成报告
        canGenerate() {
            if (this.activeTab === 'weekly') {
                return this.selectedWeek !== null;
            } else if (this.activeTab === 'monthly') {
                return this.selectedMonth !== null;
            } else if (this.activeTab === 'comprehensive') {
                return this.selectedPeriod !== null;
            }
            return false;
        }
    },
    mounted() {
        // 不再自动加载报告
    },
    watch: {
        activeTab() {
            // 切换标签时重置选择
            this.resetSelections();
        }
    },
    methods: {
        // 重置选择
        resetSelections() {
            this.selectedWeek = null;
            this.selectedMonth = null;
            this.selectedPeriod = null;

            // 清空报告数据
            if (this.activeTab === 'weekly') {
                this.weeklyReport = null;
            } else if (this.activeTab === 'monthly') {
                this.monthlyReport = null;
            } else if (this.activeTab === 'comprehensive') {
                this.comprehensiveReport = null;
            }
        },

        // 获取报告描述
        getReportDescription(type) {
            switch (type) {
                case 'weekly':
                    return '查看过去某一周的健康数据';
                case 'monthly':
                    return '查看过去某一个月的健康数据';
                case 'comprehensive':
                    return '查看长期健康趋势和分析';
                default:
                    return '';
            }
        },

        // 生成报告
        async generateReport() {
            this.loading = true;
            try {
                let url = '';
                let params = {};

                // 根据不同报告类型和选择设置参数
                if (this.activeTab === 'weekly') {
                    url = '/api/reports/weekly_report/';

                    // 计算日期范围
                    const today = new Date();
                    let startDate = new Date();

                    if (this.selectedWeek === 'last-week') {
                        // 上周
                        startDate.setDate(today.getDate() - 7 - today.getDay());
                    } else if (this.selectedWeek === 'last-2-week') {
                        // 上上周
                        startDate.setDate(today.getDate() - 14 - today.getDay());
                    } else if (this.selectedWeek === 'last-3-week') {
                        // 上上上周
                        startDate.setDate(today.getDate() - 21 - today.getDay());
                    }

                    const endDate = new Date(startDate);
                    endDate.setDate(startDate.getDate() + 6);

                    params = {
                        start_date: startDate.toISOString().split('T')[0],
                        end_date: endDate.toISOString().split('T')[0]
                    };

                } else if (this.activeTab === 'monthly') {
                    url = '/api/reports/monthly_report/';

                    const today = new Date();
                    let year = today.getFullYear();
                    let month = today.getMonth(); // 0-11

                    if (this.selectedMonth === 'last-month') {
                        // 上个月
                        month = month - 1;
                        if (month < 0) {
                            month = 11;
                            year--;
                        }
                    } else if (this.selectedMonth === 'last-2-month') {
                        // 上上个月
                        month = month - 2;
                        if (month < 0) {
                            month = 12 + month;
                            year--;
                        }
                    } else if (this.selectedMonth === 'last-3-month') {
                        // 上上上个月
                        month = month - 3;
                        if (month < 0) {
                            month = 12 + month;
                            year--;
                        }
                    }

                    params = {
                        year: year,
                        month: month + 1 // API需要1-12的月份
                    };

                } else if (this.activeTab === 'comprehensive') {
                    url = '/api/reports/comprehensive_analysis/';
                    params = { period: this.selectedPeriod };
                }

                // 发送请求
                if (url) {
                    const response = await axios.get(url, { params });

                    // 更新对应的报告数据
                    if (this.activeTab === 'weekly') {
                        this.weeklyReport = response.data;
                    } else if (this.activeTab === 'monthly') {
                        this.monthlyReport = response.data;
                    } else if (this.activeTab === 'comprehensive') {
                        this.comprehensiveReport = response.data;
                    }
                }
            } catch (error) {
                console.error('生成健康报告失败：', error);

                // 检查是否是数据不足的错误
                if (error.response && error.response.status === 400) {
                    const errorData = error.response.data;
                    if (errorData.error === '数据不足，无法生成健康报告') {
                        // 显示数据不足的详细信息
                        this.showInsufficientDataError(errorData);
                    } else {
                        // 其他400错误
                        this.showError(errorData.message || '请求参数错误');
                    }
                } else if (error.response && error.response.status === 500) {
                    this.showError('服务器内部错误，请稍后重试');
                } else if (error.request) {
                    this.showError('网络连接错误，请检查网络连接');
                } else {
                    this.showError('生成健康报告失败，请稍后重试');
                }

                // 清空对应报告数据
                if (this.activeTab === 'weekly') {
                    this.weeklyReport = null;
                } else if (this.activeTab === 'monthly') {
                    this.monthlyReport = null;
                } else if (this.activeTab === 'comprehensive') {
                    this.comprehensiveReport = null;
                }
            } finally {
                this.loading = false;
            }
        },

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('zh-CN', {
                month: 'short',
                day: 'numeric'
            });
        },

        getQualityText(quality) {
            const qualityMap = {
                1: '很差',
                2: '较差',
                3: '一般',
                4: '较好',
                5: '很好'
            };
            return qualityMap[quality] || '未知';
        },

        getScoreClass(score) {
            if (score >= 80) return 'excellent';
            if (score >= 60) return 'good';
            if (score >= 40) return 'fair';
            return 'poor';
        },

        getTrendText(trend) {
            const trendMap = {
                'improving': { text: '改善中', icon: 'trending-up' },
                'declining': { text: '下降中', icon: 'trending-down' },
                'stable': { text: '稳定', icon: 'trending-flat' }
            };
            return trendMap[trend] || { text: trend, icon: 'trending-flat' };
        },

        getAdviceCategoryClass(category) {
            if (category.includes('睡眠') || category.includes('Sleep')) {
                return 'advice-sleep';
            } else if (category.includes('运动') || category.includes('Exercise') || category.includes('健身')) {
                return 'advice-exercise';
            } else if (category.includes('饮食') || category.includes('Diet') || category.includes('营养')) {
                return 'advice-diet';
            }
            return '';
        },

        // 显示数据不足错误
        showInsufficientDataError(errorData) {
            const details = errorData.details;
            let message = errorData.message;

            if (details) {
                message += `\n\n📊 数据统计：`;
                message += `\n• 当前有效记录天数：${details.total_days_with_data}天`;
                message += `\n• 最少需要记录天数：${details.min_required_days}天`;
                message += `\n• 还需要记录：${details.min_required_days - details.total_days_with_data}天`;

                if (details.breakdown) {
                    message += `\n\n📝 记录明细：`;
                    if (details.breakdown.sleep_days !== undefined) {
                        message += `\n• 睡眠记录：${details.breakdown.sleep_days}天`;
                    }
                    if (details.breakdown.exercise_days !== undefined) {
                        message += `\n• 运动记录：${details.breakdown.exercise_days}天`;
                    }
                    if (details.breakdown.diet_days !== undefined) {
                        message += `\n• 饮食记录：${details.breakdown.diet_days}天`;
                    }
                }

                message += `\n\n💡 建议：请继续记录您的健康数据，积累足够的数据后再生成报告，这样可以获得更准确的分析结果。`;
            }

            this.showError(message, '数据不足');
        },

        // 通用错误显示方法
        showError(message, title = '错误') {
            // 如果有 Element Plus 的 ElMessageBox
            if (this.$alert) {
                this.$alert(message, title, {
                    confirmButtonText: '知道了',
                    type: 'warning',
                    showClose: false
                });
            }
            // 如果有 Element Plus 的 ElMessage
            else if (this.$message) {
                this.$message({
                    message: message,
                    type: 'warning',
                    duration: 5000,
                    showClose: true
                });
            }
            // 如果没有 UI 组件，使用浏览器原生 alert
            else {
                alert(`${title}：\n${message}`);
            }
        }
    }
};
</script>

<style scoped>
.health-report {
    min-height: 100vh;
    background: #f5f7fa;
    padding-bottom: 40px;
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
    color: #409eff;
}

.back-btn {
    background: #409eff;
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

/* 报告控制面板 */
.report-controls {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.control-section {
    padding: 20px;
    background: #f8f9fa;
    border-radius: 12px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.control-section h3 {
    margin: 0 0 16px 0;
    color: #2c3e50;
    font-size: 18px;
}

.report-type-buttons {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.type-btn {
    background: #e0e0e0;
    color: #333;
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    transition: all 0.3s;
    flex: 1;
    min-width: 200px;
}

.type-btn:hover {
    background: #d0d0d0;
}

.type-btn.active {
    background: #409eff;
    color: white !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.type-btn.active .type-icon {
    color: white;
}

.type-btn.active .type-info {
    color: white;
}

.type-btn.active .type-name {
    color: white !important;
}

.type-btn.active .type-desc {
    color: rgba(255, 255, 255, 0.8) !important;
}

.type-icon {
    width: 24px;
    height: 24px;
    color: #409eff;
}

.type-info {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
}

.type-name {
    font-weight: bold;
    font-size: 16px;
}

.type-desc {
    font-size: 12px;
    color: #666;
}

.time-selection {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.week-options, .month-options, .period-options {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.week-option, .month-option, .period-option {
    background: #e0e0e0;
    color: #333;
    border: none;
    padding: 8px 15px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}

.week-option:hover, .month-option:hover, .period-option:hover {
    background: #d0d0d0;
}

.week-option.active, .month-option.active, .period-option.active {
    background: #409eff;
    color: white;
}

.generate-section {
    text-align: center;
    padding: 20px;
}

.generate-btn {
    background: #409eff;
    color: white;
    border: none;
    padding: 14px 30px;
    border-radius: 12px;
    cursor: pointer;
    font-size: 18px;
    font-weight: bold;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    transition: background-color 0.3s;
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.generate-btn:hover:not(:disabled) {
    background: #337ecc;
}

.generate-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
    color: #888;
}

.generate-tip {
    margin-top: 10px;
    color: #666;
    font-size: 14px;
}

/* 加载状态 */
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 20px;
    color: #666;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    margin-bottom: 16px;
    color: #409eff;
}

.spin {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* 报告内容 */
.report-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 30px 20px;
}

.report-section {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* 报告头部 */
.report-header-section {
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
}

.report-header-section h2 {
    margin: 0 0 16px 0;
    color: #2c3e50;
    font-size: 28px;
}

.period-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #666;
}

.health-score {
    display: flex;
    align-items: center;
    gap: 12px;
}

.score-label {
    font-size: 14px;
}

.score-value {
    font-size: 32px;
    font-weight: bold;
    padding: 8px 16px;
    border-radius: 12px;
    background: #f0f9ff;
}

.score-value.excellent { color: #10b981; background: #ecfdf5; }
.score-value.good { color: #3b82f6; background: #eff6ff; }
.score-value.fair { color: #f59e0b; background: #fffbeb; }
.score-value.poor { color: #ef4444; background: #fef2f2; }

/* 概览卡片 */
.overview-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.overview-card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 20px;
}

.card-icon {
    width: 48px;
    height: 48px;
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #f8f9fa;
    color: #409eff;
}

.sleep-card .card-icon {
    background: rgba(155, 89, 182, 0.1);
    color: #9b59b6;
}
.exercise-card .card-icon {
    background: #e8f5e8;
    color: #27ae60;
}
.diet-card .card-icon {
    background: rgba(230, 126, 34, 0.1);
    color: #e67e22;
}

.card-content h3 {
    margin: 0 0 12px 0;
    color: #2c3e50;
    font-size: 18px;
}

.card-stats {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 8px;
}

.main-stat {
    font-size: 32px;
    font-weight: bold;
    color: #2c3e50;
}

.sub-stat {
    color: #666;
    font-size: 14px;
}

.quality-indicator {
    color: #666;
    font-size: 14px;
}

/* 分析卡片 */
.analysis-sections {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.analysis-card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.analysis-card h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
    font-size: 18px;
}

.no-data {
    text-align: center;
    color: #999;
    padding: 40px;
    font-style: italic;
}

/* 睡眠记录 */
.sleep-records {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.sleep-record {
    display: grid;
    grid-template-columns: 1fr 1fr 1.5fr 1fr;
    gap: 12px;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 8px;
    align-items: center;
}

.date {
    font-weight: 500;
    color: #2c3e50;
}

.duration {
    color: #409eff;
    font-weight: 500;
}

.time-range {
    color: #666;
    font-size: 14px;
}

.quality {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 12px;
    text-align: center;
}

.quality-1, .quality-2 { background: #fef2f2; color: #ef4444; }
.quality-3 { background: #fffbeb; color: #f59e0b; }
.quality-4, .quality-5 { background: #ecfdf5; color: #10b981; }

/* 运动分布 */
.exercise-types {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.exercise-type {
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
}

.type-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.type-name {
    font-weight: 500;
    color: #2c3e50;
}

.type-count {
    background: #409eff;
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
}

.type-stats {
    display: flex;
    gap: 16px;
    color: #666;
    font-size: 14px;
}

/* 营养成分 */
.nutrition-breakdown {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 16px;
}

.nutrition-item {
    text-align: center;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
}

.nutrient-name {
    display: block;
    color: #666;
    font-size: 14px;
    margin-bottom: 8px;
}

.nutrient-value {
    display: block;
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
}

/* 目标进度 */
.goals-section {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
}

.goals-section h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
}

.goals-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.goal-item {
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
}

.goal-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.goal-type {
    font-weight: 500;
    color: #2c3e50;
}

.goal-status {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    background: #fef2f2;
    color: #ef4444;
}

.goal-status.achieved {
    background: #ecfdf5;
    color: #10b981;
}

.progress-bar {
    height: 8px;
    background: #e1e8ed;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 8px;
}

.progress-fill {
    height: 100%;
    background: #409eff;
    transition: width 0.3s;
}

.progress-fill.achieved {
    background: #10b981;
}

.progress-text {
    color: #666;
    font-size: 14px;
}

/* 健康建议 */
.recommendations-section {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.recommendations-section h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
}

.recommendations-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.recommendation-item {
    display: flex;
    gap: 16px;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
}

.priority-indicator {
    width: 4px;
    border-radius: 2px;
    min-height: 40px;
}

.priority-indicator.high { background: #ef4444; }
.priority-indicator.medium { background: #f59e0b; }
.priority-indicator.low { background: #10b981; }

.recommendation-content h4 {
    margin: 0 0 8px 0;
    color: #2c3e50;
}

.recommendation-content p {
    margin: 0;
    color: #666;
    line-height: 1.5;
}

/* 月报特有样式 */
.monthly-overview {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.monthly-overview .overview-card {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
}

.monthly-overview .overview-card h3 {
    margin: 0;
    color: #2c3e50;
    text-align: center;
}

.monthly-stats {
    display: flex;
    justify-content: space-around;
}

.stat-item {
    text-align: center;
}

.stat-value {
    display: block;
    font-size: 28px;
    font-weight: bold;
    color: #409eff;
    margin-bottom: 4px;
}

.stat-label {
    font-size: 12px;
    color: #666;
}

/* 周度趋势 */
.weekly-breakdown {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
}

.weekly-breakdown h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
}

.weeks-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
}

.week-card {
    background: #f8f9fa;
    padding: 16px;
    border-radius: 8px;
}

.week-header {
    margin-bottom: 12px;
}

.week-number {
    font-weight: 500;
    color: #2c3e50;
}

.week-period {
    display: block;
    font-size: 12px;
    color: #666;
    margin-top: 4px;
}

.week-stats {
    display: flex;
    justify-content: space-between;
}

.week-stat {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 14px;
    color: #666;
}

.stat-icon {
    width: 16px;
    height: 16px;
}

.sleep-stat .stat-icon {
    color: #9b59b6;
}

.exercise-stat .stat-icon {
    color: #27ae60;
}

.diet-stat .stat-icon {
    color: #e67e22;
}

/* 趋势分析 */
.trends-section {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.trends-section h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
}

.trends-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}

.trend-item {
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
    text-align: center;
}

.trend-label {
    display: block;
    color: #666;
    font-size: 14px;
    margin-bottom: 8px;
}

.trend-value {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 500;
    padding: 8px 12px;
    border-radius: 8px;
}

.trend-icon {
    width: 16px;
    height: 16px;
}

.sleep-trend .trend-label {
    color: #9b59b6;
}

.exercise-trend .trend-label {
    color: #27ae60;
}

.trend-value.improving {
    background: #ecfdf5;
    color: #10b981;
}

.trend-value.declining {
    background: #fef2f2;
    color: #ef4444;
}

/* 综合分析特有样式 */
.long-term-trends {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
}

.long-term-trends h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
}

.trend-card {
    background: #f8f9fa;
    padding: 16px;
    border-radius: 8px;
    text-align: center;
}

.trend-card h4 {
    margin: 0 0 8px 0;
    color: #2c3e50;
}

.trend-status {
    color: #666;
    font-size: 14px;
}

.trend-status.positive {
    color: #10b981;
    font-weight: 500;
}

/* 健康模式 */
.health-patterns {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
}

.health-patterns h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
}

.patterns-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.pattern-category h4 {
    margin: 0 0 12px 0;
    color: #409eff;
}

.sleep-pattern h4 {
    color: #9b59b6;
}

.exercise-pattern h4 {
    color: #27ae60;
}

.diet-pattern h4 {
    color: #e67e22;
}

.pattern-category ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.pattern-category li {
    padding: 8px 0;
    color: #666;
    border-bottom: 1px solid #f0f0f0;
}

.pattern-category li:last-child {
    border-bottom: none;
}

/* 个性化建议 */
.personalized-advice {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
}

.personalized-advice h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
}

.advice-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.advice-item {
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
}

.advice-item h4 {
    margin: 0 0 8px 0;
    color: #409eff;
}

.advice-sleep h4 {
    color: #9b59b6;
}

.advice-exercise h4 {
    color: #27ae60;
}

.advice-diet h4 {
    color: #e67e22;
}

.advice-item p {
    margin: 0;
    color: #666;
    line-height: 1.5;
}

/* 成就系统 */
.achievements-section {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
}

.achievements-section h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
}

.achievements-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
}

.achievement-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    border-radius: 8px;
    border: 2px solid #e1e8ed;
}

.achievement-item.achieved {
    background: #ecfdf5;
    border-color: #10b981;
}

.achievement-icon {
    display: flex;
    align-items: center;
    justify-content: center;
}

.achievement-svg {
    width: 32px;
    height: 32px;
    color: #ffc107;
}

.achievement-svg.locked {
    color: #ccc;
}

.achievement-content h4 {
    margin: 0 0 4px 0;
    color: #2c3e50;
}

.achievement-content p {
    margin: 0;
    color: #666;
    font-size: 14px;
}

/* 改进计划 */
.improvement-plan {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 无报告状态 */
.no-report {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 20px;
    text-align: center;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin: 20px;
}

.no-report-content {
    max-width: 400px;
}

.no-report svg {
    width: 80px;
    height: 80px;
    color: #ccc;
    margin-bottom: 20px;
}

.no-report h3 {
    margin: 0 0 10px 0;
    color: #2c3e50;
    font-size: 20px;
}

.no-report p {
    margin: 0;
    color: #666;
    line-height: 1.5;
}

.improvement-plan h3 {
    margin: 0 0 20px 0;
    color: #2c3e50;
}

.plan-sections {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}

.plan-section h4 {
    margin: 0 0 16px 0;
    color: #409eff;
}

.plan-section ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.plan-section li {
    padding: 12px 16px;
    margin-bottom: 8px;
    background: #f8f9fa;
    border-radius: 8px;
    color: #666;
    position: relative;
    padding-left: 32px;
}

.plan-section li::before {
    content: '✓';
    position: absolute;
    left: 12px;
    color: #10b981;
    font-weight: bold;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .report-header {
        padding: 16px;
    }

    .report-header h1 {
        font-size: 20px;
    }

    .period-info {
        flex-direction: column;
        gap: 12px;
    }

    .overview-cards {
        grid-template-columns: 1fr;
    }

    .overview-card {
        flex-direction: column;
        text-align: center;
    }

    .analysis-sections {
        grid-template-columns: 1fr;
    }

    .sleep-record {
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }

    .weeks-container {
        grid-template-columns: 1fr;
    }

    .trends-grid,
    .patterns-grid,
    .achievements-grid,
    .plan-sections {
        grid-template-columns: 1fr;
    }
}
</style>
