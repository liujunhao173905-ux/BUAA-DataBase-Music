<template>
  <div class="health-management">
    <!-- 头部导航 -->
    <header class="hub-header">
      <h1>
        <svg viewBox="0 0 24 24" fill="currentColor" class="header-icon">
          <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
        </svg>
        健康管理
      </h1>
      <button @click="$router.push('/dashboard')" class="back-btn">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.42-1.41L7.83 13H20v-2z"/>
        </svg>
        返回首页
      </button>
    </header>

    <!-- 健康管理功能导航 -->
    <nav class="health-nav">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="handleTabClick(tab.key)"
        :class="['nav-btn', { active: activeTab === tab.key }]"
      >
        <svg viewBox="0 0 24 24" fill="currentColor" class="nav-icon">
          <path :d="tab.iconPath"/>
        </svg>
        {{ tab.label }}
        <span v-if="tab.badge && getBadgeCount(tab.key) > 0" class="nav-badge">
          {{ getBadgeCount(tab.key) }}
        </span>
      </button>
    </nav>

    <!-- 内容区域 -->
    <main class="hub-content">
      <!-- 健康报告 -->
      <div v-if="activeTab === 'report'" class="content-section">
        <div class="section-header">
          <h2>健康报告</h2>
        </div>

        <!-- 报告类型选择 -->
        <div class="report-controls">
          <div class="control-section">
            <h3>选择报告类型</h3>
            <div class="report-type-buttons">
              <button
                v-for="type in reportTypes"
                :key="type.key"
                @click="selectedReportType = type.key"
                :class="['type-btn', { active: selectedReportType === type.key }]"
              >
                <svg viewBox="0 0 24 24" fill="currentColor" class="type-icon">
                  <path :d="type.iconPath"/>
                </svg>
                <div class="type-info">
                  <span class="type-name">{{ type.label }}</span>
                  <span class="type-desc">{{ type.description }}</span>
                </div>
              </button>
            </div>
          </div>

          <!-- 时间范围选择 -->
          <div class="control-section">
            <h3>选择时间范围</h3>
            <div class="time-selection">
              <!-- 周报时间选择 -->
              <div v-if="selectedReportType === 'weekly'" class="week-selection">
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
              <div v-if="selectedReportType === 'monthly'" class="month-selection">
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
              <div v-if="selectedReportType === 'comprehensive'" class="period-selection">
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
              :disabled="generatingReport || !canGenerate"
              class="generate-btn"
            >
              <svg v-if="!generatingReport" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
              </svg>
              <div v-else class="loading-spinner small"></div>
              {{ generatingReport ? '生成中...' : '生成健康报告' }}
            </button>
          </div>
        </div>

        <!-- 报告内容显示区域 -->
        <div v-if="currentReport" class="health-overview">
          <div class="report-container">
            <!-- 报告头部信息 - 垂直排列 -->
            <div class="report-header">
              <h3 class="report-title">{{ getReportTitle() }}</h3>
              <div class="report-period">
                <span class="period-text">{{ getReportPeriod() }}</span>
              </div>
              <div class="report-score">
                <span class="score-label">健康评分</span>
                <span :class="['score-value', getScoreClass(getHealthScore())]">
                  {{ getHealthScore() }}
                </span>
              </div>
            </div>

            <!-- 报告详细内容 -->
            <div class="report-details">
              <!-- 周报详细内容 -->
              <div v-if="selectedReportType === 'weekly' && weeklyReport" class="weekly-report-content">
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
                <div v-if="weeklyReport.goal_progress && weeklyReport.goal_progress.length > 0" class="goals-section">
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
                <div v-if="weeklyReport.recommendations && weeklyReport.recommendations.length > 0" class="recommendations-section">
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

              <!-- 月报详细内容 -->
              <div v-if="selectedReportType === 'monthly' && monthlyReport" class="monthly-report-content">
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
                      <span :class="['trend-value', getTrendClass(monthlyReport.trends.sleep_trend)]">
                        <svg viewBox="0 0 24 24" fill="currentColor" class="trend-icon">
                          <path v-if="getTrendIcon(monthlyReport.trends.sleep_trend) === 'up'" d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
                          <path v-else-if="getTrendIcon(monthlyReport.trends.sleep_trend) === 'down'" d="M16 18l2.29-2.29-4.88-4.88-4 4L2 7.41 3.41 6l6 6 4-4 6.3 6.29L22 12v6z"/>
                          <path v-else d="M22 12l-4-4v3H3v2h15v3z"/>
                        </svg>
                        {{ getTrendText(monthlyReport.trends.sleep_trend) }}
                      </span>
                    </div>
                    <div class="trend-item exercise-trend">
                      <span class="trend-label">运动趋势</span>
                      <span :class="['trend-value', getTrendClass(monthlyReport.trends.exercise_trend)]">
                        <svg viewBox="0 0 24 24" fill="currentColor" class="trend-icon">
                          <path v-if="getTrendIcon(monthlyReport.trends.exercise_trend) === 'up'" d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
                          <path v-else-if="getTrendIcon(monthlyReport.trends.exercise_trend) === 'down'" d="M16 18l2.29-2.29-4.88-4.88-4 4L2 7.41 3.41 6l6 6 4-4 6.3 6.29L22 12v6z"/>
                          <path v-else d="M22 12l-4-4v3H3v2h15v3z"/>
                        </svg>
                        {{ getTrendText(monthlyReport.trends.exercise_trend) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 综合分析详细内容 -->
              <div v-if="selectedReportType === 'comprehensive' && comprehensiveReport" class="comprehensive-report-content">
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
                <div v-if="comprehensiveReport.achievements" class="achievements-section">
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
                        <p v-else>{{ achievement.progress || '尚未达成' }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 改进计划 -->
                <div v-if="comprehensiveReport.improvement_suggestions" class="improvement-plan">
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
            </div>
          </div>
        </div>

        <!-- 如果没有报告数据，显示简单提示信息 -->
        <div v-else-if="!insufficientDataError" class="no-report-simple">
          <div class="no-report-message">
            <svg viewBox="0 0 24 24" fill="currentColor" class="no-report-icon">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
            </svg>
            <h3>暂无健康报告</h3>
            <p>请选择报告类型和时间范围，然后生成健康报告</p>
          </div>
        </div>

        <!-- 数据不足错误提示 -->
        <div v-else class="insufficient-data-panel">
          <div class="insufficient-data-content">
            <!-- 头部信息 -->
            <div class="error-header">
              <svg viewBox="0 0 24 24" fill="currentColor" class="error-icon">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
              <div class="error-text">
                <h3>数据不足，无法生成报告</h3>
                <p>{{ insufficientDataError.message }}</p>
              </div>
            </div>

            <!-- 数据统计卡片 -->
            <div v-if="insufficientDataError.details" class="data-stats-cards">
              <div class="stat-card current-data">
                <div class="stat-header">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="stat-icon">
                    <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4 0h-2v6h2v-6zm2.5-9H19V1h-2v1H7V1H5v1H4.5C3.11 2 2 3.11 2 4.5v14C2 19.89 3.11 21 4.5 21h15c1.39 0 2.5-1.11 2.5-2.5v-14C22 3.11 20.89 2 19.5 2z"/>
                  </svg>
                  <span class="stat-title">当前数据</span>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ insufficientDataError.details.total_days_with_data }}</div>
                  <div class="stat-label">天有效记录</div>
                </div>
              </div>

              <div class="stat-card required-data">
                <div class="stat-header">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="stat-icon">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                  <span class="stat-title">至少需要</span>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ insufficientDataError.details.min_required_days }}</div>
                  <div class="stat-label">天最少记录</div>
                </div>
              </div>

              <div class="stat-card remaining-data">
                <div class="stat-header">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="stat-icon">
                    <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
                  </svg>
                  <span class="stat-title">还需记录</span>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ insufficientDataError.details.min_required_days - insufficientDataError.details.total_days_with_data }}</div>
                  <div class="stat-label">天额外记录</div>
                </div>
              </div>
            </div>

            <!-- 记录明细 -->
            <div v-if="hasRecordDetails" class="record-details">
              <h4>
                <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                  <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4 0h-2v6h2v-6zm2.5-9H19V1h-2v1H7V1H5v1H4.5C3.11 2 2 3.11 2 4.5v14C2 19.89 3.11 21 4.5 21h15c1.39 0 2.5-1.11 2.5-2.5v-14C22 3.11 20.89 2 19.5 2z"/>
                </svg>
                各类记录统计
              </h4>
              <div class="record-breakdown">
                <div v-if="insufficientDataError.details.sleep_days !== undefined" class="record-item sleep-record">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="record-icon">
                    <path d="M12 3c3.87 0 7 3.13 7 7 0 3.87-3.13 7-7 7s-7-3.13-7-7c0-3.87 3.13-7 7-7zM12 1C6.48 1 2 5.48 2 11s4.48 10 10 10 10-4.48 10-10S17.52 1 12 1zm0 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm-1-8h2v6h-2zm0-2h2v1h-2z"/>
                  </svg>
                  <span class="record-name">睡眠记录</span>
                  <span class="record-count">{{ insufficientDataError.details.sleep_days }}天</span>
                </div>

                <div v-if="insufficientDataError.details.exercise_days !== undefined" class="record-item exercise-record">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="record-icon">
                    <path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z"/>
                  </svg>
                  <span class="record-name">运动记录</span>
                  <span class="record-count">{{ insufficientDataError.details.exercise_days }}天</span>
                </div>

                <div v-if="insufficientDataError.details.diet_days !== undefined" class="record-item diet-record">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="record-icon">
                    <path d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z"/>
                  </svg>
                  <span class="record-name">饮食记录</span>
                  <span class="record-count">{{ insufficientDataError.details.diet_days }}天</span>
                </div>
              </div>
            </div>

            <!-- 建议和操作 -->
            <div class="suggestions-section">
              <h4>
                <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                数据收集建议
              </h4>
              <div class="suggestions-list">
                <div class="suggestion-item">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="suggestion-icon">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                  <span>继续记录日常健康数据，保持数据的连续性</span>
                </div>
                <div class="suggestion-item">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="suggestion-icon">
                    <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4 0h-2v6h2v-6z"/>
                  </svg>
                  <span>尽量每天记录睡眠、运动和饮食数据以获得准确分析</span>
                </div>
                <div class="suggestion-item">
                  <svg viewBox="0 0 24 24" fill="currentColor" class="suggestion-icon">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                  <span>数据积累越多，健康报告的分析结果越精准</span>
                </div>
              </div>
            </div>

            <!-- 快捷操作 -->
            <div class="quick-actions">
              <button @click="$router.push('/dashboard')" class="action-btn primary">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
                </svg>
                去记录健康数据
              </button>
              <button @click="dismissInsufficientDataError" class="action-btn secondary">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
                我知道了
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 健康预警 -->
      <div v-if="activeTab === 'alerts'" class="content-section">
        <div class="section-header">
          <h2>健康预警</h2>
          <div class="alerts-stats">
            <div class="stat-item danger" v-if="alertStats.active > 0">
              <span class="stat-number">{{ alertStats.active }}</span>
              <span class="stat-label">活跃预警</span>
            </div>
            <div class="stat-item success" v-if="alertStats.resolved > 0">
              <span class="stat-number">{{ alertStats.resolved }}</span>
              <span class="stat-label">已解决</span>
            </div>
            <div class="stat-item info" v-if="alertStats.total === 0">
              <span class="stat-label">暂无预警</span>
            </div>
          </div>
        </div>

        <!-- 预警列表 -->
        <div v-if="alerts.length > 0" class="alerts-list">
          <div 
            v-for="alert in alerts" 
            :key="alert.id"
            :class="['alert-card', alert.severity]"
          >
            <div class="alert-header">
              <div class="alert-icon">
                <svg v-if="alert.alert_type === 'sleep_insufficient'" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9.5 1.5L7.5 3.5l1 1 2-2z"/>
                  <path d="M20.5 3.5L18.5 1.5l-1 1 2 2z"/>
                  <path d="M12.5 6.5c-3.03 0-5.5 2.47-5.5 5.5s2.47 5.5 5.5 5.5 5.5-2.47 5.5-5.5-2.47-5.5-5.5-5.5zm0 9c-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"/>
                </svg>
                <svg v-else-if="alert.alert_type === 'exercise_insufficient'" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M13.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.8 8.5L6 10.5v5h2v7h3.5v-7h2.5v7H17v-7h2v-5l-3.8-2z"/>
                </svg>
              </div>
              <div class="alert-info">
                <h4 class="alert-title">{{ alert.title }}</h4>
                <span class="alert-type">{{ getAlertTypeDisplay(alert.alert_type) }}</span>
                <span class="alert-severity">{{ getSeverityDisplay(alert.severity) }}</span>
              </div>
              <div class="alert-actions">
                <button 
                  v-if="alert.is_active" 
                  @click="dismissAlert(alert.id)"
                  class="dismiss-btn"
                  title="忽略预警"
                >
                  ✕
                </button>
              </div>
            </div>
            <div class="alert-content">
              <p class="alert-message">{{ alert.message }}</p>
              <div class="alert-details">
                <span class="alert-value">当前值: {{ alert.current_value.toFixed(1) }}</span>
                <span class="alert-threshold">目标值: {{ alert.threshold_value }}</span>
                <span class="alert-days">持续{{ alert.trigger_days }}天</span>
              </div>
              <div v-if="alert.suggestions" class="alert-suggestions">
                <p><strong>建议：</strong></p>
                <p>{{ alert.suggestions }}</p>
              </div>
              <div class="alert-meta">
                <span class="alert-date">{{ formatDate(alert.created_at) }}</span>
                <span :class="['alert-status', alert.is_active ? 'active' : 'resolved']">
                  {{ alert.is_active ? '活跃' : '已解决' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="alerts.length === 0" class="no-data">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
          </svg>
          <h3>一切正常</h3>
          <p>目前没有需要关注的健康预警</p>
        </div>
      </div>

      <!-- 预警设置 -->
      <div v-if="activeTab === 'settings'" class="content-section">
        <div class="section-header">
          <h2>预警设置</h2>
          <p class="section-desc">配置您的健康预警参数，当健康指标异常时及时提醒</p>
        </div>

        <div class="settings-form">
          <!-- 睡眠预警设置 -->
          <div class="setting-group">
            <h3>睡眠预警</h3>
            <div class="setting-item">
              <label class="setting-label">
                <input type="checkbox" v-model="alertSettings.sleep_alert_enabled">
                <span class="setting-title">启用睡眠预警</span>
              </label>
              <p class="setting-desc">当连续多天睡眠不足时进行预警提醒</p>
            </div>

            <div v-if="alertSettings.sleep_alert_enabled" class="sub-settings">
              <div class="setting-item">
                <label class="setting-label">
                  <span class="setting-title">最少睡眠时间</span>
                  <div class="input-group">
                    <input
                      type="number"
                      v-model.number="alertSettings.min_sleep_hours"
                      min="4"
                      max="12"
                      step="0.5"
                      class="setting-input"
                    >
                    <span class="input-unit">小时</span>
                  </div>
                </label>
              </div>

              <div class="setting-item">
                <label class="setting-label">
                  <span class="setting-title">连续检查天数</span>
                  <div class="input-group">
                    <input
                      type="number"
                      v-model.number="alertSettings.sleep_check_days"
                      min="1"
                      max="7"
                      class="setting-input"
                    >
                    <span class="input-unit">天</span>
                  </div>
                </label>
                <p class="setting-desc">连续多少天睡眠不足时触发预警</p>
              </div>
            </div>
          </div>

          <!-- 运动预警设置 -->
          <div class="setting-group">
            <h3>运动预警</h3>
            <div class="setting-item">
              <label class="setting-label">
                <input type="checkbox" v-model="alertSettings.exercise_alert_enabled">
                <span class="setting-title">启用运动预警</span>
              </label>
              <p class="setting-desc">当连续多天运动不足时进行预警提醒</p>
            </div>

            <div v-if="alertSettings.exercise_alert_enabled" class="sub-settings">
              <div class="setting-item">
                <label class="setting-label">
                  <span class="setting-title">最少运动时间</span>
                  <div class="input-group">
                    <input
                      type="number"
                      v-model.number="alertSettings.min_exercise_minutes"
                      min="10"
                      max="180"
                      step="5"
                      class="setting-input"
                    >
                    <span class="input-unit">分钟</span>
                  </div>
                </label>
              </div>

              <div class="setting-item">
                <label class="setting-label">
                  <span class="setting-title">连续检查天数</span>
                  <div class="input-group">
                    <input
                      type="number"
                      v-model.number="alertSettings.exercise_check_days"
                      min="1"
                      max="7"
                      class="setting-input"
                    >
                    <span class="input-unit">天</span>
                  </div>
                </label>
                <p class="setting-desc">连续多少天运动不足时触发预警</p>
              </div>
            </div>
          </div>

          <!-- 通知设置 -->
          <div class="setting-group">
            <h3>通知设置</h3>
            <div class="setting-item">
              <label class="setting-label">
                <input type="checkbox" v-model="alertSettings.show_popup">
                <span class="setting-title">显示弹窗提醒</span>
              </label>
              <p class="setting-desc">有新预警时显示弹窗通知</p>
            </div>

            <div class="setting-item">
              <label class="setting-label">
                <input type="checkbox" v-model="alertSettings.show_badge">
                <span class="setting-title">显示徽章提醒</span>
              </label>
              <p class="setting-desc">在导航栏显示预警数量徽章</p>
            </div>
          </div>

          <div class="action-buttons">
            <button @click="saveAlertSettings" :disabled="saving" class="save-btn">
              <svg v-if="!saving" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z"/>
              </svg>
              <div v-else class="loading-spinner small"></div>
              {{ saving ? '保存中...' : '保存设置' }}
            </button>
          </div>
        </div>

        <!-- 成功消息 -->
        <div v-if="showSuccessMessage" class="message success-message">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
          </svg>
          设置已成功保存！
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HealthManagement',
  data() {
    return {
      activeTab: 'report',
      generatingReport: false,

      // 标签页配置
      tabs: [
        {
          key: 'report',
          label: '健康报告',
          iconPath: 'M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z',
          badge: false
        },
        {
          key: 'alerts',
          label: '健康预警',
          iconPath: 'M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z',
          badge: true
        },
        {
          key: 'settings',
          label: '预警设置',
          iconPath: 'M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z',
          badge: false
        }
      ],

      // 报告相关数据
      selectedReportType: 'weekly',
      selectedWeek: null,
      selectedMonth: null,
      selectedPeriod: null,

      reportTypes: [
        {
          key: 'weekly',
          label: '周报',
          description: '查看过去某一周的健康数据',
          iconPath: 'M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z'
        },
        {
          key: 'monthly',
          label: '月报',
          description: '查看过去某一个月的健康数据',
          iconPath: 'M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z'
        },
        {
          key: 'comprehensive',
          label: '综合分析',
          description: '查看长期健康趋势和分析',
          iconPath: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z'
        }
      ],

      weekOptions: [
        { label: '上一周', value: 'last-week' },
        { label: '上上周', value: 'last-2-week' },
        { label: '上上上周', value: 'last-3-week' }
      ],

      monthOptions: [
        { label: '上个月', value: 'last-month' },
        { label: '上上个月', value: 'last-2-month' },
        { label: '上上上个月', value: 'last-3-month' }
      ],

      periodOptions: [
        { label: '最近3个月', value: '3months' },
        { label: '最近6个月', value: '6months' },
        { label: '最近1年', value: '1year' }
      ],

      // 健康指标数据
      healthMetrics: {
        avgSleep: 7.5,
        avgExercise: 45,
        avgCalories: 1850,
        healthScore: 85,
        sleepTrend: 'positive',
        exerciseTrend: 'negative',
        dietTrend: 'stable',
        scoreTrend: 'positive'
      },

      // 报告数据
      weeklyReport: null,
      monthlyReport: null,
      comprehensiveReport: null,

      // 预警数据
      alerts: [],
      alertSettings: {
        sleep_alert_enabled: true,
        min_sleep_hours: 7.0,
        sleep_check_days: 3,
        exercise_alert_enabled: true,
        min_exercise_minutes: 30,
        exercise_check_days: 3,
        show_popup: true,
        show_badge: true
      },
      saving: false,
      showSuccessMessage: false,

      // 数据不足错误状态
      insufficientDataError: null
    }
  },

  computed: {
    alertStats() {
      return {
        total: this.alerts.length,
        active: this.alerts.filter(alert => alert.status === 'active').length,
        resolved: this.alerts.filter(alert => alert.status === 'resolved').length
      }
    },

    // 当前报告
    currentReport() {
      if (this.selectedReportType === 'weekly') {
        return this.weeklyReport;
      } else if (this.selectedReportType === 'monthly') {
        return this.monthlyReport;
      } else if (this.selectedReportType === 'comprehensive') {
        return this.comprehensiveReport;
      }
      return null;
    },

    canGenerate() {
      if (this.selectedReportType === 'weekly') {
        return this.selectedWeek !== null;
      } else if (this.selectedReportType === 'monthly') {
        return this.selectedMonth !== null;
      } else if (this.selectedReportType === 'comprehensive') {
        return this.selectedPeriod !== null;
      }
      return false;
    },

    // 检查是否有记录明细数据
    hasRecordDetails() {
      if (!this.insufficientDataError || !this.insufficientDataError.details) {
        return false;
      }
      const details = this.insufficientDataError.details;
      return details.sleep_days !== undefined ||
             details.exercise_days !== undefined ||
             details.diet_days !== undefined;
    }
  },

  async mounted() {
    await this.initData()
  },

  methods: {
    async initData() {
      await this.loadAlerts()
      await this.loadAlertSettings()
    },

    handleTabClick(tabKey) {
      this.activeTab = tabKey
    },

    getBadgeCount(tabKey) {
      if (tabKey === 'alerts') {
        return this.alertStats.active
      }
      return 0
    },

    // 获取报告标题
    getReportTitle() {
      const typeMap = {
        'weekly': '周健康报告',
        'monthly': '月健康报告',
        'comprehensive': '综合健康分析'
      };
      return typeMap[this.selectedReportType] || '健康报告';
    },

    // 获取报告周期
    getReportPeriod() {
      if (this.selectedReportType === 'weekly' && this.selectedWeek) {
        const periodMap = {
          'last-week': '上一周',
          'last-2-week': '上上周',
          'last-3-week': '上上上周'
        };
        return `报告周期：${periodMap[this.selectedWeek]}`;
      } else if (this.selectedReportType === 'monthly' && this.selectedMonth) {
        const periodMap = {
          'last-month': '上个月',
          'last-2-month': '上上个月',
          'last-3-month': '上上上个月'
        };
        return `报告月份：${periodMap[this.selectedMonth]}`;
      } else if (this.selectedReportType === 'comprehensive' && this.selectedPeriod) {
        const periodMap = {
          '3months': '最近3个月',
          '6months': '最近6个月',
          '1year': '最近1年'
        };
        return `分析周期：${periodMap[this.selectedPeriod]}`;
      }
      return '请选择时间范围';
    },

    // 获取健康评分
    getHealthScore() {
      if (this.selectedReportType === 'weekly' && this.weeklyReport) {
        return this.weeklyReport.overall_score;
      } else if (this.selectedReportType === 'monthly' && this.monthlyReport) {
        return this.monthlyReport.health_score;
      } else if (this.selectedReportType === 'comprehensive' && this.comprehensiveReport) {
        return this.comprehensiveReport.overall_health_score;
      }
      // 如果没有报告数据，返回基础健康评分
      return this.healthMetrics.healthScore || 75;
    },

    // 获取分数等级样式类
    getScoreClass(score) {
      if (score >= 80) return 'excellent';
      if (score >= 60) return 'good';
      if (score >= 40) return 'fair';
      return 'poor';
    },

      // 生成报告
      async generateReport() {
        this.generatingReport = true;
        // 清除之前的数据不足错误
        this.insufficientDataError = null;

        try {
          let url = '';
          let params = {};

          if (this.selectedReportType === 'weekly') {
            url = '/api/reports/weekly_report/';
            const today = new Date();
            let startDate = new Date();

            if (this.selectedWeek === 'last-week') {
              startDate.setDate(today.getDate() - 7 - today.getDay());
            } else if (this.selectedWeek === 'last-2-week') {
              startDate.setDate(today.getDate() - 14 - today.getDay());
            } else if (this.selectedWeek === 'last-3-week') {
              startDate.setDate(today.getDate() - 21 - today.getDay());
            }

            const endDate = new Date(startDate);
            endDate.setDate(startDate.getDate() + 6);

            params = {
              start_date: startDate.toISOString().split('T')[0],
              end_date: endDate.toISOString().split('T')[0]
            };
          } else if (this.selectedReportType === 'monthly') {
            url = '/api/reports/monthly_report/';
            const today = new Date();
            let year = today.getFullYear();
            let month = today.getMonth();

            if (this.selectedMonth === 'last-month') {
              month = month - 1;
              if (month < 0) {
                month = 11;
                year--;
              }
            } else if (this.selectedMonth === 'last-2-month') {
              month = month - 2;
              if (month < 0) {
                month = 12 + month;
                year--;
              }
            } else if (this.selectedMonth === 'last-3-month') {
              month = month - 3;
              if (month < 0) {
                month = 12 + month;
                year--;
              }
            }

            params = {
              year: year,
              month: month + 1
            };
          } else if (this.selectedReportType === 'comprehensive') {
            url = '/api/reports/comprehensive_analysis/';
            params = { period: this.selectedPeriod };
          }

          if (url) {
            const response = await axios.get(url, { params });

            if (this.selectedReportType === 'weekly') {
              this.weeklyReport = response.data;
            } else if (this.selectedReportType === 'monthly') {
              this.monthlyReport = response.data;
            } else if (this.selectedReportType === 'comprehensive') {
              this.comprehensiveReport = response.data;
            }
          }
          } catch (error) {
            console.error('生成健康报告失败：', error);
            this.showError(error);
          } finally {
            this.generatingReport = false;
          }
        },      // 日期格式化
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN', {
          month: 'short',
          day: 'numeric'
        });
      },

      // 获取睡眠质量文本
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

      // 获取趋势文本
      getTrendText(trend) {
        const trendMap = {
          'improving': '改善中',
          'declining': '下降中',
          'stable': '稳定'
        };
        return trendMap[trend] || trend;
      },

      // 获取趋势图标
      getTrendIcon(trend) {
        const iconMap = {
          'improving': 'up',
          'declining': 'down',
          'stable': 'flat'
        };
        return iconMap[trend] || 'flat';
      },

      // 获取趋势样式类
      getTrendClass(trend) {
        const classMap = {
          'improving': 'improving',
          'declining': 'declining',
          'stable': 'stable'
        };
        return classMap[trend] || 'stable';
      },

      // 获取建议分类样式类
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

      // 显示错误信息
      showError(error) {
        // 检查是否是数据不足的错误
        if (error.response && error.response.status === 400) {
          const errorData = error.response.data;
          if (errorData.error === '数据不足，无法生成健康报告') {
            // 设置数据不足错误状态，显示优化的错误面板
            this.insufficientDataError = errorData;
          } else {
            // 其他400错误
            this.showBasicError(errorData.message || '请求参数错误');
          }
        } else if (error.response && error.response.status === 500) {
          this.showBasicError('服务器内部错误，请稍后重试');
        } else if (error.request) {
          this.showBasicError('网络连接错误，请检查网络连接');
        } else {
          this.showBasicError('生成健康报告失败，请稍后重试');
        }
      },

      // 显示基本错误信息
      showBasicError(message) {
        alert(`错误：\n${message}`);
      },

      // 关闭数据不足错误提示
      dismissInsufficientDataError() {
        this.insufficientDataError = null;
      },    // 加载预警数据
    async loadAlerts() {
      try {
        const response = await axios.get('/api/alerts/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        })
        this.alerts = response.data
      } catch (error) {
        console.error('加载预警失败：', error)
      }
    },

    // 加载预警设置
    async loadAlertSettings() {
      try {
        const response = await axios.get('/api/alert-settings/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        })
        this.alertSettings = response.data
      } catch (error) {
        console.error('加载预警设置失败：', error)
      }
    },

    // 保存预警设置
    async saveAlertSettings() {
      this.saving = true
      try {
        await axios.post('/api/alert-settings/', this.alertSettings, {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        })
        this.showSuccessMessage = true
        setTimeout(() => {
          this.showSuccessMessage = false
        }, 3000)
      } catch (error) {
        console.error('保存预警设置失败：', error)
      } finally {
        this.saving = false
      }
    },

    // 获取预警类型显示名称
    getAlertTypeDisplay(type) {
      const typeMap = {
        'sleep_insufficient': '睡眠不足',
        'exercise_insufficient': '运动不足',
        'diet_unbalanced': '饮食不均衡'
      }
      return typeMap[type] || type
    },

    // 获取严重程度显示名称
    getSeverityDisplay(severity) {
      const severityMap = {
        'low': '轻微',
        'medium': '中等', 
        'high': '严重'
      }
      return severityMap[severity] || severity
    },

    // 忽略预警
    async dismissAlert(alertId) {
      try {
        await axios.patch(`/api/alerts/${alertId}/dismiss/`, {}, {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        })
        // 重新加载预警列表
        await this.loadAlerts()
      } catch (error) {
        console.error('忽略预警失败：', error)
      }
    }
  }
}
</script>

<style scoped>
/* 主容器 */
.health-management {
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
  font-weight: 600;
}

.header-icon {
  width: 28px;
  height: 28px;
  color: #20b2aa;
}

.back-btn {
  background: #20b2aa;
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
  background: #1a9d96;
}

.back-btn svg {
  width: 16px;
  height: 16px;
}

/* 导航样式 */
.health-nav {
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
  color: #20b2aa;
  background: #f8f9fa;
}

.nav-btn.active {
  color: #20b2aa;
  border-bottom-color: #20b2aa;
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
  margin-bottom: 24px;
}

.section-header h2 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 24px;
}

.section-desc {
  margin: 0;
  color: #6c757d;
  font-size: 14px;
}

/* 健康概览样式 */
.health-overview {
  margin-bottom: 20px;
}

.health-overview .overview-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.report-container {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 24px;
  display: block; /* 确保垂直布局 */
}

.card-header {
  margin-bottom: 24px;
}

.report-header {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.report-title {
  margin: 0;
  color: #2c3e50;
  font-size: 20px;
  font-weight: 600;
}

.report-period {
  margin: 0;
}

.period-text {
  color: #666;
  font-size: 14px;
}

.report-score {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.card-header h3 {
  margin: 0 0 12px 0;
  color: #2c3e50;
  font-size: 20px;
}

.period-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #666;
  margin-bottom: 20px;
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
  font-size: 28px;
  font-weight: bold;
  padding: 6px 12px;
  border-radius: 8px;
  background: #f0f9ff;
}

.score-value.excellent { color: #10b981; background: #ecfdf5; }
.score-value.good { color: #3b82f6; background: #eff6ff; }
.score-value.fair { color: #f59e0b; background: #fffbeb; }
.score-value.poor { color: #ef4444; background: #fef2f2; }

/* 数据不足错误面板 */
.insufficient-data-panel {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 24px;
  margin-top: 20px;
  border: 1px solid #e9ecef;
}

.insufficient-data-content {
  max-width: 800px;
  margin: 0 auto;
}

.error-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 32px;
  padding: 20px;
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
}

.error-icon {
  width: 32px;
  height: 32px;
  color: #856404;
  flex-shrink: 0;
  margin-top: 4px;
}

.error-text h3 {
  margin: 0 0 8px 0;
  color: #856404;
  font-size: 18px;
  font-weight: 600;
}

.error-text p {
  margin: 0;
  color: #856404;
  line-height: 1.5;
}

/* 数据统计卡片 */
.data-stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 2px solid #e9ecef;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card.current-data {
  border-color: #3498db;
}

.stat-card.required-data {
  border-color: #e74c3c;
}

.stat-card.remaining-data {
  border-color: #f39c12;
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 16px;
}

.stat-icon {
  width: 20px;
  height: 20px;
}

.current-data .stat-icon {
  color: #3498db;
}

.required-data .stat-icon {
  color: #e74c3c;
}

.remaining-data .stat-icon {
  color: #f39c12;
}

.stat-title {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.stat-content {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 4px;
}

.current-data .stat-number {
  color: #3498db;
}

.required-data .stat-number {
  color: #e74c3c;
}

.remaining-data .stat-number {
  color: #f39c12;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

/* 记录明细 */
.record-details {
  background: white;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 32px;
  border: 1px solid #e9ecef;
}

.record-details h4 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.record-details .section-icon {
  width: 20px;
  height: 20px;
  color: #20b2aa;
}

.record-breakdown {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.record-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #ddd;
}

.record-item.sleep-record {
  border-left-color: #9b59b6;
}

.record-item.exercise-record {
  border-left-color: #27ae60;
}

.record-item.diet-record {
  border-left-color: #e67e22;
}

.record-icon {
  width: 20px;
  height: 20px;
}

.sleep-record .record-icon {
  color: #9b59b6;
}

.exercise-record .record-icon {
  color: #27ae60;
}

.diet-record .record-icon {
  color: #e67e22;
}

.record-name {
  flex: 1;
  font-weight: 500;
  color: #2c3e50;
}

.record-count {
  font-weight: bold;
  color: #666;
}

/* 建议部分 */
.suggestions-section {
  background: white;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 32px;
  border: 1px solid #e9ecef;
}

.suggestions-section h4 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.suggestions-section .section-icon {
  width: 20px;
  height: 20px;
  color: #20b2aa;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #f0f9ff;
  border-radius: 8px;
  border-left: 4px solid #20b2aa;
}

.suggestion-icon {
  width: 20px;
  height: 20px;
  color: #20b2aa;
  margin-top: 2px;
  flex-shrink: 0;
}

.suggestion-item span {
  color: #2c3e50;
  line-height: 1.5;
}

/* 快捷操作 */
.quick-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-decoration: none;
}

.action-btn.primary {
  background: #20b2aa;
  color: white;
}

.action-btn.primary:hover {
  background: #1a9d96;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(32, 178, 170, 0.3);
}

.action-btn.secondary {
  background: #f8f9fa;
  color: #666;
  border: 1px solid #e9ecef;
}

.action-btn.secondary:hover {
  background: #e9ecef;
  color: #2c3e50;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .data-stats-cards {
    grid-template-columns: 1fr;
  }

  .record-breakdown {
    grid-template-columns: 1fr;
  }

  .quick-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .error-header {
    flex-direction: column;
    text-align: center;
  }
}

/* 无报告状态 */
.no-report-content {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.no-report-simple {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 20px;
}

.no-report-message {
  max-width: 400px;
  margin: 0 auto;
}

.no-report-icon {
  width: 64px;
  height: 64px;
  color: #ccc;
  margin-bottom: 16px;
}

.no-report-message h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 18px;
}

.no-report-message p {
  margin: 0 0 8px 0;
  line-height: 1.5;
}

.score-tip {
  margin-top: 16px !important;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.current-score {
  font-weight: bold;
  color: #20b2aa;
  font-size: 18px;
}

/* 报告控制 */
.report-controls {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
}

.control-section {
  margin-bottom: 24px;
}

.control-section:last-child {
  margin-bottom: 0;
}

.control-section h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 16px;
}

.report-type-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.type-btn {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s;
}

.type-btn:hover {
  border-color: #20b2aa;
}

.type-btn.active {
  border-color: #20b2aa;
  background: #f0f9ff;
}

.type-icon {
  width: 20px;
  height: 20px;
  color: #20b2aa;
}

.type-info {
  flex: 1;
}

.type-name {
  display: block;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.type-desc {
  display: block;
  font-size: 12px;
  color: #6c757d;
}

.time-selection {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.week-options, .month-options, .period-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.week-option, .month-option, .period-option {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.week-option:hover, .month-option:hover, .period-option:hover {
  border-color: #20b2aa;
  color: #20b2aa;
}

.week-option.active, .month-option.active, .period-option.active {
  background: #20b2aa;
  border-color: #20b2aa;
  color: white;
}

.generate-section {
  text-align: center;
  margin-top: 24px;
}

.generate-btn {
  background: #20b2aa;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.generate-btn:hover:not(:disabled) {
  background: #1a9d96;
}

.generate-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.generate-btn svg {
  width: 16px;
  height: 16px;
}

/* 加载动画 */
.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-spinner.small {
  width: 12px;
  height: 12px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 预警统计 */
.alerts-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  padding: 8px 12px;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
}

.stat-item.danger {
  background: #fef2f2;
  color: #dc2626;
}

.stat-item.success {
  background: #ecfdf5;
  color: #059669;
}

.stat-item.info {
  background: #eff6ff;
  color: #2563eb;
}

.stat-number {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
}

/* 预警列表 */
.alerts-list {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.alert-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border-left: 4px solid;
}

.alert-card.high {
  border-left-color: #dc2626;
}

.alert-card.medium {
  border-left-color: #f59e0b;
}

.alert-card.low {
  border-left-color: #10b981;
}

.alert-header {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.alert-icon {
  width: 24px;
  height: 24px;
  margin-right: 12px;
  color: #6b7280;
}

.alert-info {
  flex: 1;
}

.alert-title {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.alert-type {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  background: #e5e7eb;
  color: #4b5563;
  margin-right: 8px;
}

.alert-severity {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.alert-card.high .alert-severity {
  background: #fef2f2;
  color: #dc2626;
}

.alert-card.medium .alert-severity {
  background: #fffbeb;
  color: #f59e0b;
}

.alert-card.low .alert-severity {
  background: #ecfdf5;
  color: #10b981;
}

.alert-actions {
  display: flex;
  gap: 8px;
}

.dismiss-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.dismiss-btn:hover {
  background: #e5e7eb;
  color: #374151;
}

.alert-content {
  padding: 20px;
}

.alert-message {
  margin: 0 0 12px 0;
  color: #374151;
  line-height: 1.5;
}

.alert-details {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.alert-value,
.alert-threshold,
.alert-days {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.alert-value {
  background: #fef2f2;
  color: #dc2626;
}

.alert-threshold {
  background: #f0f9ff;
  color: #0369a1;
}

.alert-days {
  background: #fefce8;
  color: #ca8a04;
}

.alert-suggestions {
  background: #f8fafc;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.alert-suggestions p {
  margin: 0;
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
}

.alert-suggestions p:first-child {
  margin-bottom: 4px;
  font-weight: 500;
}

.alert-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #6b7280;
}

.alert-date {
  font-weight: 500;
}

.alert-status {
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.alert-status.active {
  background: #fef2f2;
  color: #dc2626;
}

.alert-status.resolved {
  background: #ecfdf5;
  color: #059669;
}

/* 无数据状态 */
.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.no-data svg {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  color: #ccc;
}

.no-data h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.no-data p {
  margin: 0;
}

/* 设置表单 */
.settings-form {
  max-width: 800px;
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.setting-group {
  margin-bottom: 32px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #20b2aa;
}

.setting-group:last-child {
  margin-bottom: 0;
}

.setting-group h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.setting-item {
  margin-bottom: 16px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-label {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  width: 100%;
}

.setting-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin-top: 2px;
  accent-color: #20b2aa;
}

.setting-title {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 500;
  flex: 1;
}

.setting-desc {
  margin: 8px 0 0 30px;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

.sub-settings {
  margin-left: 30px;
  margin-top: 16px;
  padding: 16px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e1e8ed;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  min-width: 120px;
}

.setting-input {
  width: 80px;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  text-align: center;
}

.setting-input:focus {
  outline: none;
  border-color: #20b2aa;
  box-shadow: 0 0 0 2px rgba(32, 178, 170, 0.2);
}

.input-unit {
  color: #666;
  font-size: 14px;
  white-space: nowrap;
}

.action-buttons {
  margin-top: 32px;
}

.save-btn {
  background: #20b2aa;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: background-color 0.3s;
}

.save-btn:hover:not(:disabled) {
  background: #1a9d96;
}

.save-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.save-btn svg {
  width: 16px;
  height: 16px;
}

/* 成功消息 */
.message {
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-message {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #bbf7d0;
}

.success-message svg {
  width: 16px;
  height: 16px;
}

/* 报告详情 */
.report-details {
  margin-top: 24px;
}

.weekly-report-content,
.monthly-report-content,
.comprehensive-report-content {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 概览卡片 */
.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.overview-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
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
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
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
  margin-bottom: 30px;
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
  margin-bottom: 30px;
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
  justify-content: center;
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

.trend-value.stable {
  background: #f0f9ff;
  color: #3b82f6;
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
  margin-bottom: 30px;
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
  .hub-header {
    padding: 16px;
  }

  .hub-header h1 {
    font-size: 20px;
  }

  .health-nav {
    padding: 0 10px;
    overflow-x: auto;
  }

  .nav-btn {
    padding: 12px 16px;
    font-size: 14px;
    white-space: nowrap;
  }

  .hub-content {
    padding: 16px;
  }

  .content-section {
    padding: 16px;
  }

  .report-type-buttons {
    grid-template-columns: 1fr;
  }

  .week-options, .month-options, .period-options {
    flex-direction: column;
  }

  .alerts-stats {
    flex-direction: column;
  }

  .overview-cards {
    grid-template-columns: 1fr;
  }

  .analysis-sections {
    grid-template-columns: 1fr;
  }

  .sleep-record {
    grid-template-columns: 1fr;
    gap: 4px;
  }

  .monthly-overview {
    grid-template-columns: 1fr;
  }

  .weeks-container {
    grid-template-columns: 1fr;
  }

  .week-stats {
    flex-direction: column;
    gap: 8px;
  }

  .trends-grid {
    grid-template-columns: 1fr;
  }

  .patterns-grid {
    grid-template-columns: 1fr;
  }

  .achievements-grid {
    grid-template-columns: 1fr;
  }

  .plan-sections {
    grid-template-columns: 1fr;
  }

  .settings-form {
    max-width: 100%;
    padding: 16px;
  }

  .setting-group {
    padding: 16px;
  }

  .setting-label {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .input-group {
    margin-left: 0;
    margin-top: 8px;
  }

  .sub-settings {
    margin-left: 0;
    margin-top: 12px;
    padding: 12px;
  }

  .setting-desc {
    margin-left: 0;
    margin-top: 4px;
  }
}
</style>
