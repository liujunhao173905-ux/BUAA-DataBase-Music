<template>
  <div class="health-alerts">
    <!-- 头部导航 -->
    <header class="hub-header">
      <h1>
        <svg viewBox="0 0 24 24" fill="currentColor" class="header-icon">
          <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
        </svg>
        健康预警
      </h1>
      <div class="header-actions">
        <button @click="refreshAlerts" class="action-btn" :disabled="loading">
          <svg :class="{ 'fa-spin': loading }" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.65,6.35C16.2,4.9 14.21,4 12,4c-4.42,0 -7.99,3.58 -7.99,8s3.57,8 7.99,8c3.73,0 6.84,-2.55 7.73,-6h-2.08c-0.82,2.33 -3.04,4 -5.65,4 -3.31,0 -6,-2.69 -6,-6s2.69,-6 6,-6c1.66,0 3.14,0.69 4.22,1.78L13,11h7V4L17.65,6.35z"/>
          </svg>
          刷新
        </button>
        <button @click="$router.push('/health-alert-settings')" class="action-btn primary">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
          </svg>
          预警设置
        </button>
        <button @click="$router.push('/dashboard')" class="back-btn">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.42-1.41L7.83 13H20v-2z"/>
          </svg>
          返回首页
        </button>
      </div>
    </header>

    <!-- 健康预警功能导航 -->
    <nav class="health-nav">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
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
      <!-- 预警列表 -->
      <div v-if="activeTab === 'alerts'" class="content-section">
        <!-- 统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card danger">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-number">{{ stats.active }}</span>
              <span class="stat-label">活跃预警</span>
            </div>
          </div>
          <div class="stat-card success">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-number">{{ stats.resolved }}</span>
              <span class="stat-label">已解决</span>
            </div>
          </div>
          <div class="stat-card warning">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-number">{{ stats.thisWeek }}</span>
              <span class="stat-label">本周新增</span>
            </div>
          </div>
          <div class="stat-card info">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-number">{{ stats.total }}</span>
              <span class="stat-label">总计</span>
            </div>
          </div>
        </div>

        <!-- 筛选器 -->
        <div class="filter-section">
          <h3>筛选条件</h3>
          <div class="filter-grid">
            <select v-model="filters.alertType" class="filter-select">
              <option value="">全部类型</option>
              <option value="sleep">睡眠预警</option>
              <option value="exercise">运动预警</option>
              <option value="diet">饮食预警</option>
            </select>
            <select v-model="filters.severity" class="filter-select">
              <option value="">全部程度</option>
              <option value="low">轻微</option>
              <option value="medium">中等</option>
              <option value="high">严重</option>
            </select>
            <select v-model="filters.status" class="filter-select">
              <option value="">全部状态</option>
              <option value="active">活跃</option>
              <option value="resolved">已解决</option>
              <option value="dismissed">已忽略</option>
            </select>
            <select v-model="filters.dateRange" class="filter-select">
              <option value="today">今天</option>
              <option value="week">本周</option>
              <option value="month">本月</option>
              <option value="all">全部</option>
            </select>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-section">
          <div class="loading-spinner"></div>
          <p>加载预警信息...</p>
        </div>

        <!-- 预警列表 -->
        <div v-else-if="paginatedAlerts.length > 0" class="alerts-list">
          <div
            v-for="alert in paginatedAlerts"
            :key="alert.id"
            class="alert-item"
          >
            <div class="alert-header">
              <div class="alert-badges">
                <span class="badge" :class="getAlertTypeClass(alert.alert_type)">
                  {{ getAlertTypeName(alert.alert_type) }}
                </span>
                <span class="badge" :class="getSeverityClass(alert.severity)">
                  {{ getSeverityName(alert.severity) }}
                </span>
                <span class="badge" :class="getStatusClass(alert.status)">
                  {{ getStatusName(alert.status) }}
                </span>
              </div>
              <div class="alert-actions">
                <button
                  v-if="alert.status === 'active'"
                  @click="resolveAlert(alert.id)"
                  :disabled="updatingAlert === alert.id"
                  class="action-btn accept-btn"
                >
                  {{ updatingAlert === alert.id ? '处理中...' : '已解决' }}
                </button>
                <button
                  v-if="alert.status === 'active'"
                  @click="dismissAlert(alert.id)"
                  :disabled="updatingAlert === alert.id"
                  class="action-btn reject-btn"
                >
                  {{ updatingAlert === alert.id ? '处理中...' : '忽略' }}
                </button>
                <button
                  @click="viewDetails(alert)"
                  class="action-btn view-btn"
                >
                  详情
                </button>
              </div>
            </div>

            <h4 class="alert-title">{{ alert.title }}</h4>
            <p class="alert-message">{{ alert.message }}</p>

            <div class="alert-metadata">
              <span class="metadata-item">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                </svg>
                触发时间: {{ formatDate(alert.triggered_at) }}
              </span>
              <span v-if="alert.resolved_at" class="metadata-item">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                </svg>
                解决时间: {{ formatDate(alert.resolved_at) }}
              </span>
            </div>

            <!-- 相关数据 -->
            <div v-if="alert.related_data" class="related-data">
              <span
                v-for="(value, key) in alert.related_data"
                :key="key"
                class="data-badge"
              >
                {{ key }}: {{ value }}
              </span>
            </div>
          </div>

          <!-- 分页 -->
          <div v-if="totalPages > 1" class="pagination-section">
            <button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="page-btn"
            >
              上一页
            </button>

            <button
              v-for="page in pageNumbers"
              :key="page"
              @click="changePage(page)"
              :class="['page-btn', { active: page === currentPage }]"
            >
              {{ page }}
            </button>

            <button
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="page-btn"
            >
              下一页
            </button>
          </div>
        </div>

        <!-- 无数据状态 -->
        <div v-else class="no-data">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
          </svg>
          <h3>暂无健康预警</h3>
          <p>系统会根据您的健康数据自动监测并生成预警信息</p>
          <button @click="$router.push('/health-alert-settings')" class="primary-btn">
            配置预警设置
          </button>
        </div>

        <!-- 错误消息 -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>

      <!-- 预警设置快捷入口 -->
      <div v-if="activeTab === 'settings'" class="content-section">
        <div class="settings-overview">
          <h2>预警设置</h2>
          <p>管理您的健康预警参数和通知偏好</p>
          <button @click="$router.push('/health-alert-settings')" class="primary-btn">
            进入设置
          </button>
        </div>
      </div>
    </main>

    <!-- 详情模态框 -->
    <div v-if="showDetailModal" class="modal-overlay" @click="closeDetailModal">
      <div class="modal-dialog" @click.stop>
        <div class="modal-header">
          <h3>预警详情</h3>
          <button @click="closeDetailModal" class="close-btn">&times;</button>
        </div>

        <div class="modal-body" v-if="selectedAlert">
          <div class="detail-grid">
            <div class="detail-item">
              <label>预警类型</label>
              <span>{{ getAlertTypeName(selectedAlert.alert_type) }}</span>
            </div>
            <div class="detail-item">
              <label>严重程度</label>
              <span>{{ getSeverityName(selectedAlert.severity) }}</span>
            </div>
            <div class="detail-item">
              <label>状态</label>
              <span>{{ getStatusName(selectedAlert.status) }}</span>
            </div>
            <div class="detail-item">
              <label>触发时间</label>
              <span>{{ formatDate(selectedAlert.triggered_at) }}</span>
            </div>
          </div>

          <div class="detail-item full">
            <label>标题</label>
            <span>{{ selectedAlert.title }}</span>
          </div>

          <div class="detail-item full">
            <label>详细消息</label>
            <p>{{ selectedAlert.message }}</p>
          </div>

          <div v-if="selectedAlert.related_data" class="detail-item full">
            <label>相关数据</label>
            <div class="related-data">
              <span
                v-for="(value, key) in selectedAlert.related_data"
                :key="key"
                class="data-badge"
              >
                {{ key }}: {{ value }}
              </span>
            </div>
          </div>

          <div v-if="selectedAlert.resolved_at" class="detail-item full">
            <label>解决时间</label>
            <span>{{ formatDate(selectedAlert.resolved_at) }}</span>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeDetailModal" class="secondary-btn">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HealthAlerts',
  data() {
    return {
      loading: false,
      alerts: [],
      filteredAlerts: [],
      errorMessage: '',

      // 分页
      currentPage: 1,
      itemsPerPage: 10,

      // 筛选器
      filters: {
        alertType: '',
        severity: '',
        status: '',
        dateRange: 'all'
      },

      // 模态框
      showDetailModal: false,
      selectedAlert: null,

      // 更新状态
      updatingAlert: null,

      // 统计数据
      stats: {
        active: 0,
        resolved: 0,
        thisWeek: 0,
        total: 0
      },

      // 导航标签
      activeTab: 'alerts',
      tabs: [
        {
          key: 'alerts',
          label: '预警列表',
          iconPath: 'M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z',
          badge: true
        },
        {
          key: 'settings',
          label: '设置',
          iconPath: 'M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z',
          badge: false
        }
      ]
    }
  },

  computed: {
    paginatedAlerts() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredAlerts.slice(start, end)
    },

    totalPages() {
      return Math.ceil(this.filteredAlerts.length / this.itemsPerPage)
    },

    pageNumbers() {
      const pages = []
      const total = this.totalPages
      const current = this.currentPage

      if (total <= 7) {
        for (let i = 1; i <= total; i++) {
          pages.push(i)
        }
      } else {
        if (current <= 4) {
          for (let i = 1; i <= 5; i++) {
            pages.push(i)
          }
          pages.push('...')
          pages.push(total)
        } else if (current >= total - 3) {
          pages.push(1)
          pages.push('...')
          for (let i = total - 4; i <= total; i++) {
            pages.push(i)
          }
        } else {
          pages.push(1)
          pages.push('...')
          for (let i = current - 1; i <= current + 1; i++) {
            pages.push(i)
          }
          pages.push('...')
          pages.push(total)
        }
      }

      return pages
    }
  },

  watch: {
    filters: {
      handler() {
        this.applyFilters()
      },
      deep: true
    }
  },

  async mounted() {
    await this.fetchAlerts()
  },

  methods: {
    async fetchAlerts() {
      this.loading = true
      this.errorMessage = ''

      try {
        const token = localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const response = await axios.get(
          `/api/alerts/`,
          {
            headers: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )

        this.alerts = response.data.results || response.data || []
        this.applyFilters()
        this.updateStats()

      } catch (error) {
        console.error('获取健康预警失败:', error)
        if (error.response?.status === 401) {
          localStorage.removeItem('token')
          this.$router.push('/login')
        } else {
          this.errorMessage = '获取健康预警失败，请稍后重试'
        }
      } finally {
        this.loading = false
      }
    },

    async refreshAlerts() {
      await this.fetchAlerts()
    },

    applyFilters() {
      let filtered = [...this.alerts]

      if (this.filters.alertType) {
        filtered = filtered.filter(alert => alert.alert_type === this.filters.alertType)
      }

      if (this.filters.severity) {
        filtered = filtered.filter(alert => alert.severity === this.filters.severity)
      }

      if (this.filters.status) {
        filtered = filtered.filter(alert => alert.status === this.filters.status)
      }

      if (this.filters.dateRange !== 'all') {
        const now = new Date()
        let cutoffDate

        switch (this.filters.dateRange) {
          case 'today':
            cutoffDate = new Date(now.getFullYear(), now.getMonth(), now.getDate())
            break
          case 'week':
            cutoffDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
            break
          case 'month':
            cutoffDate = new Date(now.getFullYear(), now.getMonth(), 1)
            break
        }

        filtered = filtered.filter(alert => {
          const alertDate = new Date(alert.triggered_at)
          return alertDate >= cutoffDate
        })
      }

      this.filteredAlerts = filtered
      this.currentPage = 1
    },

    async resolveAlert(alertId) {
      await this.updateAlertStatus(alertId, 'resolved')
    },

    async dismissAlert(alertId) {
      await this.updateAlertStatus(alertId, 'dismissed')
    },

    async updateAlertStatus(alertId, status) {
      this.updatingAlert = alertId

      try {
        const token = localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        await axios.patch(
          `/api/alerts/${alertId}/`,
          { status: status },
          {
            headers: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )

        // 更新本地数据
        const alert = this.alerts.find(a => a.id === alertId)
        if (alert) {
          alert.status = status
          if (status === 'resolved') {
            alert.resolved_at = new Date().toISOString()
          }
        }

        this.updateStats()

      } catch (error) {
        console.error('更新预警状态失败:', error)
        if (error.response?.status === 401) {
          localStorage.removeItem('token')
          this.$router.push('/login')
        } else {
          this.errorMessage = '更新预警状态失败，请稍后重试'
        }
      } finally {
        this.updatingAlert = null
      }
    },

    viewDetails(alert) {
      this.selectedAlert = alert
      this.showDetailModal = true
    },

    closeDetailModal() {
      this.showDetailModal = false
      this.selectedAlert = null
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },

    updateStats() {
      this.stats = {
        active: this.alerts.filter(a => a.status === 'active').length,
        resolved: this.alerts.filter(a => a.status === 'resolved').length,
        thisWeek: this.alerts.filter(a => {
          const alertDate = new Date(a.triggered_at)
          const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
          return alertDate >= weekAgo
        }).length,
        total: this.alerts.length
      }
    },

    getBadgeCount(tabKey) {
      if (tabKey === 'alerts') {
        return this.stats.active
      }
      return 0
    },

    getAlertTypeClass(type) {
      return type
    },

    getAlertTypeName(type) {
      const types = {
        'sleep': '睡眠',
        'exercise': '运动',
        'diet': '饮食'
      }
      return types[type] || type
    },

    getSeverityClass(severity) {
      return severity
    },

    getSeverityName(severity) {
      const severities = {
        'low': '轻微',
        'medium': '中等',
        'high': '严重'
      }
      return severities[severity] || severity
    },

    getStatusClass(status) {
      return status
    },

    getStatusName(status) {
      const statuses = {
        'active': '活跃',
        'resolved': '已解决',
        'dismissed': '已忽略'
      }
      return statuses[status] || status
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.health-alerts {
  background-color: #f5f7fa;
  min-height: 100vh;
  padding: 20px;
}

/* 头部样式 */
.hub-header {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hub-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 28px;
  height: 28px;
  color: #3498db;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.action-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  white-space: nowrap;
}

.action-btn:hover {
  background: #f8f9fa;
  border-color: #bbb;
}

.action-btn.primary {
  background: #3498db;
  border-color: #3498db;
  color: white;
}

.action-btn.primary:hover {
  background: #2980b9;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.fa-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.back-btn {
  padding: 8px 12px;
  border: 1px solid #e74c3c;
  border-radius: 8px;
  background: white;
  color: #e74c3c;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.back-btn:hover {
  background: #e74c3c;
  color: white;
}

/* 导航标签 */
.health-nav {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 12px;
}

.nav-btn {
  padding: 12px 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #f8f9fa;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  white-space: nowrap;
}

.nav-btn:hover {
  background: #e9ecef;
  border-color: #ccc;
}

.nav-btn.active {
  background: #3498db;
  border-color: #3498db;
  color: white;
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.nav-badge {
  background: #e74c3c;
  color: white;
  border-radius: 12px;
  padding: 2px 8px;
  font-size: 12px;
  margin-left: 4px;
}

/* 主内容区域 */
.hub-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.content-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
  border-left: 4px solid #3498db;
}

.stat-card.danger {
  border-left-color: #e74c3c;
}

.stat-card.success {
  border-left-color: #27ae60;
}

.stat-card.warning {
  border-left-color: #f39c12;
}

.stat-card.info {
  border-left-color: #3498db;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
}

.stat-card.danger .stat-icon {
  background: #fee;
  color: #e74c3c;
}

.stat-card.success .stat-icon {
  background: #efe;
  color: #27ae60;
}

.stat-card.warning .stat-icon {
  background: #ffc;
  color: #f39c12;
}

.stat-card.info .stat-icon {
  background: #eef;
  color: #3498db;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  display: block;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

/* 筛选器 */
.filter-section {
  margin-bottom: 24px;
}

.filter-section h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.filter-select {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  color: #333;
  font-size: 14px;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

/* 加载状态 */
.loading-section {
  text-align: center;
  padding: 40px;
  color: #666;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

/* 预警列表 */
.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.alert-item {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s ease;
}

.alert-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #3498db;
}

.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 16px;
}

.alert-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.badge {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.badge.sleep { background: #e3f2fd; color: #1976d2; }
.badge.exercise { background: #f3e5f5; color: #7b1fa2; }
.badge.diet { background: #e8f5e8; color: #388e3c; }
.badge.low { background: #fff3e0; color: #f57c00; }
.badge.medium { background: #ffe0b2; color: #ef6c00; }
.badge.high { background: #ffebee; color: #d32f2f; }
.badge.active { background: #ffebee; color: #d32f2f; }
.badge.resolved { background: #e8f5e8; color: #388e3c; }
.badge.dismissed { background: #f5f5f5; color: #757575; }

.alert-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.accept-btn {
  background: #27ae60;
  border-color: #27ae60;
  color: white;
}

.accept-btn:hover {
  background: #219a52;
}

.reject-btn {
  background: #e74c3c;
  border-color: #e74c3c;
  color: white;
}

.reject-btn:hover {
  background: #c0392b;
}

.view-btn {
  background: #3498db;
  border-color: #3498db;
  color: white;
}

.view-btn:hover {
  background: #2980b9;
}

.alert-title {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
}

.alert-message {
  margin: 0 0 16px 0;
  color: #555;
  line-height: 1.5;
}

.alert-metadata {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.metadata-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
  font-size: 14px;
}

.metadata-item svg {
  width: 16px;
  height: 16px;
}

.related-data {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.data-badge {
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 4px 8px;
  font-size: 12px;
  color: #666;
}

/* 分页 */
.pagination-section {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e0e0e0;
}

.page-btn {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover {
  background: #f8f9fa;
  border-color: #bbb;
}

.page-btn.active {
  background: #3498db;
  border-color: #3498db;
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 无数据状态 */
.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.no-data svg {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.no-data h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 20px;
}

.no-data p {
  margin: 0 0 24px 0;
  color: #666;
}

.primary-btn {
  padding: 12px 24px;
  background: #3498db;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.2s ease;
}

.primary-btn:hover {
  background: #2980b9;
}

/* 错误消息 */
.error-message {
  background: #ffebee;
  border: 1px solid #e57373;
  border-radius: 8px;
  padding: 16px;
  color: #d32f2f;
  margin-top: 16px;
}

/* 设置快捷入口 */
.settings-overview {
  text-align: center;
  padding: 40px;
}

.settings-overview h2 {
  margin: 0 0 12px 0;
  color: #2c3e50;
  font-size: 24px;
}

.settings-overview p {
  margin: 0 0 24px 0;
  color: #666;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-dialog {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s ease;
}

.close-btn:hover {
  background: #f0f0f0;
}

.modal-body {
  padding: 20px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item.full {
  grid-column: 1 / -1;
}

.detail-item label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 14px;
}

.detail-item span {
  color: #666;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.secondary-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.secondary-btn:hover {
  background: #f8f9fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .health-alerts {
    padding: 16px;
  }

  .hub-header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .header-actions {
    flex-wrap: wrap;
    justify-content: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }

  .health-nav {
    flex-wrap: wrap;
  }

  .alert-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .alert-actions {
    justify-content: flex-end;
  }

  .modal-dialog {
    margin: 10px;
    max-height: 90vh;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
