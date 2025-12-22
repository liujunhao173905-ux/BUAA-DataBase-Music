<template>
  <div class="check-history">
    <div class="container">
      <el-card shadow="hover" class="page-card">
        <template #header>
          <el-page-header @back="handleBack" content="审核历史" title="返回" />
        </template>
      
        <div class="filters">
          <select v-model="typeFilter" @change="loadHistory">
            <option value="">全部类型</option>
            <option value="song">歌曲审核</option>
            <option value="playlist">歌单审核</option>
            <option value="user">用户审核</option>
          </select>
          
          <select v-model="statusFilter" @change="loadHistory">
            <option value="">全部状态</option>
            <option value="0">待审核</option>
            <option value="1">已通过</option>
            <option value="2">已拒绝</option>
          </select>
        </div>
      
        <div class="history-list-container">
          <div v-if="loading" class="loading">加载中...</div>
          <div v-else-if="history.length === 0" class="empty">暂无审核历史记录</div>
          <div v-else class="history-items">
          <div 
            v-for="record in history" 
            :key="record.check_id" 
            class="history-item"
          >
            <div class="record-info">
              <span class="record-type-tag">{{ getRecordTypeText(record) }}</span>
              <h3>{{ getRecordName(record) }}</h3>
              <p class="submitter">{{ getSubmitter(record) }}</p>
            </div>
            
            <div class="record-status">
              <span 
                class="status-tag"
                :class="getStatusClass(record.check_status)"
              >
                {{ record.check_status_display }}
              </span>
              <p class="submit-time">提交时间: {{ formatDate(record.check_submit_time) }}</p>
              <p v-if="record.check_modify_time" class="modify-time">审核时间: {{ formatDate(record.check_modify_time) }}</p>
            </div>
            
            <div class="record-details">
              <p class="admin" v-if="record.check_admin_name">审核人: {{ record.check_admin_name }}</p>
              <p class="comment" v-if="record.check_comment">{{ record.check_comment }}</p>
            </div>
            
            <div class="record-actions">
              <button 
                class="btn btn-detail"
                @click="viewRecordDetail(record)"
              >
                查看详情
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 分页 -->
        <div class="pagination">
          <button 
            @click="prevPage" 
            :disabled="page <= 1"
          >
            上一页
          </button>
          <span>{{ page }} / {{ totalPages }}</span>
          <button 
            @click="nextPage" 
            :disabled="page >= totalPages"
          >
            下一页
          </button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useAuditStore } from '@/stores/audit'
// import { ArrowLeft } from '@element-plus/icons-vue' // 不再需要

const authStore = useAuthStore()
const router = useRouter()

// 返回上一页
const handleBack = () => {
  router.back()
}
const auditStore = useAuditStore()

// 历史记录列表
const history = ref<any[]>([])
const loading = ref(false)
const typeFilter = ref('')
const statusFilter = ref('')

// 分页
const page = ref(1)
const pageSize = ref(15)
const total = ref(0)

onMounted(async () => {
  // 检查权限
  if (authStore.user?.user_type !== 2) {
    router.push('/home')
    return
  }
  
  await loadHistory()
})

const loadHistory = async () => {
  loading.value = true
  try {
    // 调用审核API获取历史记录
    const params = {
      type: typeFilter.value || undefined,
      status: statusFilter.value || undefined,
      page: page.value,
      page_size: pageSize.value
    }
    
    // 由于审核历史记录可能来自不同的API，这里暂时合并三个API的结果
    const [songHistory, playlistHistory, userHistory] = await Promise.all([
      auditStore.fetchCheckSongs(params),
      auditStore.fetchCheckPlaylists(params),
      auditStore.fetchCheckUsers(params)
    ])
    
    // 标记记录类型
    const songRecords = songHistory.results.map((record: any) => ({ ...record, type: 'song' }))
    const playlistRecords = playlistHistory.results.map((record: any) => ({ ...record, type: 'playlist' }))
    const userRecords = userHistory.results.map((record: any) => ({ ...record, type: 'user' }))
    
    // 合并并按提交时间排序
    history.value = [...songRecords, ...playlistRecords, ...userRecords]
      .sort((a, b) => new Date(b.check_submit_time).getTime() - new Date(a.check_submit_time).getTime())
    
    // 计算总记录数
    total.value = songHistory.count + playlistHistory.count + userHistory.count
  } catch (error) {
    console.error('加载审核历史失败:', error)
  } finally {
    loading.value = false
  }
}

const getRecordTypeText = (record: any) => {
  switch (record.type) {
    case 'song': return '歌曲审核'
    case 'playlist': return '歌单审核'
    case 'user': return '用户审核'
    default: return '未知类型'
  }
}

const getRecordName = (record: any) => {
  switch (record.type) {
    case 'song': return record.check_song_name
    case 'playlist': return record.check_playlist_name
    case 'user': return record.check_user_name
    default: return '未知名称'
  }
}

const getSubmitter = (record: any) => {
  switch (record.type) {
    case 'song': return `提交者: ${record.check_song_detail.song_singer_name || '未知'}`
    case 'playlist': return `提交者: ${record.check_playlist_detail.playlist_creator_name || '未知'}`
    case 'user': return `申请人: ${record.check_user_name}`
    default: return ''
  }
}

const getStatusClass = (status: number) => {
  switch (status) {
    case 0: return 'status-pending'
    case 1: return 'status-approved'
    case 2: return 'status-rejected'
    default: return ''
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const viewRecordDetail = (record: any) => {
  switch (record.type) {
    case 'song':
      router.push(`/songs/${record.check_song}`)
      break
    case 'playlist':
      router.push(`/playlists/${record.check_playlist}`)
      break
    case 'user':
      router.push(`/user/${record.check_user}`)
      break
  }
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
    loadHistory()
  }
}

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
    loadHistory()
  }
}

const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value)
})
</script>

<style scoped>
.check-history {
  padding: 20px;
}

.page-title {
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
}

.filters {
  margin-bottom: 20px;
}

.filters {
  display: flex;
  gap: 15px;
  align-items: center;
}

.filters select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

/*
.history-list {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}
*/

.loading, .empty {
  text-align: center;
  padding: 50px;
  color: #666;
}

.history-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.3s;
}

.history-item:hover {
  background-color: #f9f9f9;
}

.record-info {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.record-type-tag {
  display: inline-block;
  padding: 3px 8px;
  background: #3498db;
  color: white;
  border-radius: 10px;
  font-size: 12px;
  font-weight: bold;
  width: fit-content;
}

.record-info h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.submitter {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.record-status {
  flex: 1;
  text-align: center;
  margin: 0 20px;
  min-width: 120px;
}

.status-tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-approved {
  background: #d4edda;
  color: #155724;
}

.status-rejected {
  background: #f8d7da;
  color: #721c24;
}

.submit-time, .modify-time {
  margin: 5px 0;
  font-size: 12px;
  color: #999;
}

.record-details {
  flex: 1;
  min-width: 200px;
}

.admin, .comment {
  margin: 5px 0;
  font-size: 14px;
  color: #666;
}

.comment {
  font-style: italic;
}

.record-actions {
  align-self: center;
}

.btn {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.btn-detail {
  background: #6c757d;
  color: white;
}

.btn-detail:hover {
  background: #5a6268;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 15px;
}

.pagination button {
  padding: 8px 15px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>