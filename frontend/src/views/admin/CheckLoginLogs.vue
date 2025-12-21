<template>
  <div class="check-login-logs">
    <div class="container">
      <el-card shadow="hover" class="page-card">
        <template #header>
          <el-page-header @back="handleBack" content="登录日志" title="返回" />
        </template>

        <!-- 登录日志列表 -->
        <div v-loading="loading" class="logs-list-container">
        <div v-if="logs.length === 0" class="empty-state">
          暂无登录日志
        </div>
        
        <div v-else class="log-items">
          <div v-for="log in logs" :key="log.log_id" class="log-item">
            <div class="log-info">
              <h3>{{ log.log_user_name }}</h3>
              <p class="user-type">用户类型: {{ log.log_user_type_display }}</p>
            </div>
            
            <div class="log-status">
              <p class="log-time">登录时间: {{ log.log_time }}</p>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination" v-if="total > 0">
          <button 
            :disabled="page === 1" 
            @click="prevPage"
            class="page-btn"
          >
            上一页
          </button>
          <span class="page-info">{{ page }} / {{ totalPages }}</span>
          <button 
            :disabled="page === totalPages" 
            @click="nextPage"
            class="page-btn"
          >
            下一页
          </button>
        </div>
      </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useAuditStore } from '../../stores/audit'

const authStore = useAuthStore()
const router = useRouter()

// 返回上一页
const handleBack = () => {
  router.back()
}
const auditStore = useAuditStore()

// 日志列表
const logs = ref<any[]>([])
const loading = ref(false)

// 分页
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

onMounted(async () => {
  // 检查权限
  if (authStore.user?.user_type !== 2) {
    router.push('/home')
    return
  }
  
  await loadLogs()
})

const loadLogs = async () => {
  loading.value = true
  try {
    console.log('开始加载登录日志列表...')
    const params = {
      page: page.value,
      page_size: pageSize.value
    }
    const response = await auditStore.fetchLoginLogs(params)
    logs.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('加载登录日志列表失败:', error)
  } finally {
    loading.value = false
  }
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
    loadLogs()
  }
}

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
    loadLogs()
  }
}

const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value) || 1
})
</script>

<style scoped>
.check-login-logs {
  padding: 20px;
}

.page-title {
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
}

.logs-list {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  min-height: 400px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 16px;
}

.log-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s;
}

.log-item:hover {
  background-color: #f9f9f9;
}

.log-item:last-child {
  border-bottom: none;
}

.log-info h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
}

.user-type {
  color: #666;
  font-size: 14px;
  margin: 5px 0 0;
}

.log-status {
  text-align: right;
}

.log-time {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  gap: 20px;
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  border-color: #3498db;
  color: #3498db;
}

.page-btn:disabled {
  background: #f5f5f5;
  color: #ccc;
  cursor: not-allowed;
}

.page-info {
  color: #666;
}
</style>
