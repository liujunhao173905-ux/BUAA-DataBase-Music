<template>
  <div class="health-alert-settings">
    <!-- 头部导航 -->
    <header class="hub-header">
      <h1>
        <svg viewBox="0 0 24 24" fill="currentColor" class="header-icon">
          <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
        </svg>
        健康预警设置
      </h1>
      <div class="header-actions">
        <button @click="resetToDefaults" class="action-btn">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.65,6.35C16.2,4.9 14.21,4 12,4c-4.42,0 -7.99,3.58 -7.99,8s3.57,8 7.99,8c3.73,0 6.84,-2.55 7.73,-6h-2.08c-0.82,2.33 -3.04,4 -5.65,4 -3.31,0 -6,-2.69 -6,-6s2.69,-6 6,-6c1.66,0 3.14,0.69 4.22,1.78L13,11h7V4L17.65,6.35z"/>
          </svg>
          恢复默认
        </button>
        <button @click="$router.push('/health-alerts')" class="action-btn primary">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
          </svg>
          查看预警
        </button>
        <button @click="$router.push('/dashboard')" class="back-btn">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.42-1.41L7.83 13H20v-2z"/>
          </svg>
          返回首页
        </button>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="hub-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-section">
        <div class="loading-spinner"></div>
        <p>加载设置中...</p>
      </div>

      <!-- 设置表单 -->
      <div v-else class="content-section">
        <form @submit.prevent="saveSettings" class="settings-form">

          <!-- 睡眠预警设置 -->
          <div class="settings-card">
            <div class="card-header">
              <h2 class="card-title">
                <svg class="card-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
                睡眠预警
              </h2>
              <div class="card-description">
                监测您的睡眠时间，确保充足休息
              </div>
            </div>

            <div class="card-body">
              <div class="setting-toggle">
                <label class="toggle-switch">
                  <input
                    type="checkbox"
                    v-model="settings.sleep_alerts_enabled"
                    class="toggle-input"
                  >
                  <span class="toggle-slider"></span>
                  <span class="toggle-label">启用睡眠预警</span>
                </label>
              </div>

              <div v-if="settings.sleep_alerts_enabled" class="setting-options">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">最少睡眠时间 (小时)</label>
                    <input
                      type="number"
                      v-model.number="settings.min_sleep_hours"
                      min="1"
                      max="12"
                      step="0.5"
                      class="form-input"
                    >
                    <div class="form-hint">低于此时间将触发预警</div>
                  </div>
                  <div class="form-group">
                    <label class="form-label">最多睡眠时间 (小时)</label>
                    <input
                      type="number"
                      v-model.number="settings.max_sleep_hours"
                      min="6"
                      max="15"
                      step="0.5"
                      class="form-input"
                    >
                    <div class="form-hint">高于此时间将触发预警</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 运动预警设置 -->
          <div class="settings-card">
            <div class="card-header">
              <h2 class="card-title">
                <svg class="card-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3.1 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1.2-.6-1.9-.6s-1.3.2-1.8.7L7.9 7.7c-.4.4-.7.9-.7 1.5 0 .6.2 1.1.7 1.5L11 13.8V20h2v-7.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z"/>
                </svg>
                运动预警
              </h2>
              <div class="card-description">
                提醒您保持规律运动，维持健康体魄
              </div>
            </div>

            <div class="card-body">
              <div class="setting-toggle">
                <label class="toggle-switch">
                  <input
                    type="checkbox"
                    v-model="settings.exercise_alerts_enabled"
                    class="toggle-input"
                  >
                  <span class="toggle-slider"></span>
                  <span class="toggle-label">启用运动预警</span>
                </label>
              </div>

              <div v-if="settings.exercise_alerts_enabled" class="setting-options">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">每日最少运动时间 (分钟)</label>
                    <input
                      type="number"
                      v-model.number="settings.min_exercise_minutes"
                      min="0"
                      max="300"
                      class="form-input"
                    >
                    <div class="form-hint">未达到将触发预警</div>
                  </div>
                  <div class="form-group">
                    <label class="form-label">每周最少运动天数</label>
                    <input
                      type="number"
                      v-model.number="settings.exercise_days_per_week"
                      min="1"
                      max="7"
                      class="form-input"
                    >
                    <div class="form-hint">低于此天数将触发预警</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 饮食预警设置 -->
          <div class="settings-card">
            <div class="card-header">
              <h2 class="card-title">
                <svg class="card-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z"/>
                </svg>
                饮食预警
              </h2>
              <div class="card-description">
                监控饮食习惯，维持营养平衡
              </div>
            </div>

            <div class="card-body">
              <div class="setting-toggle">
                <label class="toggle-switch">
                  <input
                    type="checkbox"
                    v-model="settings.diet_alerts_enabled"
                    class="toggle-input"
                  >
                  <span class="toggle-slider"></span>
                  <span class="toggle-label">启用饮食预警</span>
                </label>
              </div>

              <div v-if="settings.diet_alerts_enabled" class="setting-options">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">每日最大卡路里摄入</label>
                    <input
                      type="number"
                      v-model.number="settings.max_calories_per_day"
                      min="800"
                      max="5000"
                      class="form-input"
                    >
                    <div class="form-hint">超出将触发预警</div>
                  </div>
                  <div class="form-group">
                    <label class="form-label">每日最少用餐次数</label>
                    <input
                      type="number"
                      v-model.number="settings.min_meals_per_day"
                      min="1"
                      max="6"
                      class="form-input"
                    >
                    <div class="form-hint">低于此次数将触发预警</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 通知设置 -->
          <div class="settings-card">
            <div class="card-header">
              <h2 class="card-title">
                <svg class="card-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
                </svg>
                通知设置
              </h2>
              <div class="card-description">
                配置预警通知的方式和时间
              </div>
            </div>

            <div class="card-body">
              <div class="setting-toggle">
                <label class="toggle-switch">
                  <input
                    type="checkbox"
                    v-model="settings.notifications_enabled"
                    class="toggle-input"
                  >
                  <span class="toggle-slider"></span>
                  <span class="toggle-label">启用推送通知</span>
                </label>
              </div>

              <div v-if="settings.notifications_enabled" class="setting-options">
                <div class="form-group">
                  <label class="form-label">每日通知时间</label>
                  <input
                    type="time"
                    v-model="settings.notification_time"
                    class="form-input time-input"
                  >
                  <div class="form-hint">系统将在此时间检查并发送预警</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="action-section">
            <button type="submit" class="save-btn" :disabled="saving">
              <svg v-if="!saving" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z"/>
              </svg>
              <div v-else class="loading-spinner small"></div>
              {{ saving ? '保存中...' : '保存设置' }}
            </button>
          </div>
        </form>
      </div>

      <!-- 成功消息 -->
      <div v-if="showSuccessMessage" class="message success-message">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
        </svg>
        设置已成功保存！
      </div>

      <!-- 错误消息 -->
      <div v-if="errorMessage" class="message error-message">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        {{ errorMessage }}
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HealthAlertSettings',
  data() {
    return {
      loading: true,
      saving: false,
      showSuccessMessage: false,
      errorMessage: '',
      settings: {
        sleep_alerts_enabled: true,
        min_sleep_hours: 6,
        max_sleep_hours: 9,
        exercise_alerts_enabled: true,
        min_exercise_minutes: 30,
        exercise_days_per_week: 3,
        diet_alerts_enabled: true,
        max_calories_per_day: 2000,
        min_meals_per_day: 3,
        notifications_enabled: true,
        notification_time: '20:00'
      }
    }
  },

  async mounted() {
    await this.loadSettings()
  },

  methods: {
    async loadSettings() {
      try {
        this.loading = true
        this.errorMessage = ''

        const token = localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/health-alert-settings/`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )

        if (response.data) {
          this.settings = { ...this.settings, ...response.data }
        }
      } catch (error) {
        console.error('加载设置失败:', error)
        if (error.response?.status === 401) {
          localStorage.removeItem('token')
          this.$router.push('/login')
        } else if (error.response?.status === 404) {
          // 首次使用，使用默认设置
          console.log('使用默认设置')
        } else {
          this.errorMessage = '加载设置失败，请稍后重试'
        }
      } finally {
        this.loading = false
      }
    },

    async saveSettings() {
      try {
        this.saving = true
        this.errorMessage = ''
        this.showSuccessMessage = false

        const token = localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        await axios.post(
          `${process.env.VUE_APP_API_URL}/health-alert-settings/`,
          this.settings,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )

        this.showSuccessMessage = true
        setTimeout(() => {
          this.showSuccessMessage = false
        }, 3000)

      } catch (error) {
        console.error('保存设置失败:', error)
        if (error.response?.status === 401) {
          localStorage.removeItem('token')
          this.$router.push('/login')
        } else {
          this.errorMessage = error.response?.data?.error || '保存设置失败，请稍后重试'
        }
      } finally {
        this.saving = false
      }
    },

    resetToDefaults() {
      this.settings = {
        sleep_alerts_enabled: true,
        min_sleep_hours: 6,
        max_sleep_hours: 9,
        exercise_alerts_enabled: true,
        min_exercise_minutes: 30,
        exercise_days_per_week: 3,
        diet_alerts_enabled: true,
        max_calories_per_day: 2000,
        min_meals_per_day: 3,
        notifications_enabled: true,
        notification_time: '20:00'
      }
    }
  }
}
</script>

<style scoped>
.health-alert-settings {
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

.action-btn svg {
  width: 16px;
  height: 16px;
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

/* 加载状态 */
.loading-section {
  background: white;
  border-radius: 12px;
  padding: 60px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
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

/* 设置卡片 */
.settings-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  margin-bottom: 24px;
  overflow: hidden;
}

.settings-card:last-child {
  margin-bottom: 0;
}

.card-header {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafbfc;
}

.card-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-icon {
  width: 20px;
  height: 20px;
  color: #3498db;
}

.card-description {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.card-body {
  padding: 20px;
}

/* 开关控件 */
.setting-toggle {
  margin-bottom: 20px;
}

.toggle-switch {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
}

.toggle-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: relative;
  width: 48px;
  height: 26px;
  background-color: #ccc;
  border-radius: 26px;
  transition: 0.3s;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

.toggle-input:checked + .toggle-slider {
  background-color: #3498db;
}

.toggle-input:checked + .toggle-slider:before {
  transform: translateX(22px);
}

.toggle-label {
  font-weight: 500;
  color: #2c3e50;
  margin: 0;
  font-size: 16px;
}

/* 设置选项 */
.setting-options {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.form-group {
  margin-bottom: 0;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-hint {
  margin-top: 4px;
  color: #666;
  font-size: 12px;
}

.time-input {
  max-width: 200px;
}

/* 操作按钮 */
.action-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  margin-top: 24px;
}

.save-btn {
  padding: 12px 32px;
  background: #3498db;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-width: 140px;
  justify-content: center;
}

.save-btn:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-1px);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.save-btn svg {
  width: 18px;
  height: 18px;
}

/* 小加载器 */
.loading-spinner.small {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 消息样式 */
.message {
  background: white;
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  animation: slideIn 0.3s ease-out;
}

.message svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.success-message {
  border-left: 4px solid #27ae60;
  color: #27ae60;
}

.error-message {
  border-left: 4px solid #e74c3c;
  color: #e74c3c;
}

/* 动画 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .health-alert-settings {
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

  .form-row {
    grid-template-columns: 1fr;
  }

  .card-header {
    padding: 16px;
  }

  .card-body {
    padding: 16px;
  }

  .setting-options {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .hub-header h1 {
    font-size: 20px;
  }

  .card-title {
    font-size: 16px;
  }

  .action-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style>
