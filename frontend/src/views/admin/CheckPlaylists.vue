<template>
  <div class="check-playlists">
    <div class="container">
      <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px;">
        <el-button type="default" @click="handleBack">
          <el-icon><ArrowLeft /></el-icon> 返回
        </el-button>
        <h2 class="page-title">歌单审核</h2>
      </div>
      
      <div class="filters">
        <select v-model="statusFilter" @change="loadPlaylists">
          <option value="">全部状态</option>
          <option value="0">待审核</option>
          <option value="1">已通过</option>
          <option value="2">已拒绝</option>
        </select>
        <button 
          class="btn btn-clear-all" 
          @click="showClearAllDialog"
        >
          批量清空已处理审核
        </button>
      </div>
      
      <div class="playlists-list">
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="playlists.length === 0" class="empty">暂无歌单审核记录</div>
        <div v-else class="playlist-items">
          <div 
            v-for="playlist in playlists" 
            :key="playlist.check_id" 
            class="playlist-item"
          >
            <div class="playlist-info">
              <div class="playlist-cover">
                <img :src="playlist.check_playlist_cover || '/default-playlist-cover.png'" alt="歌单封面">
              </div>
              <div class="playlist-details">
                <h3>{{ playlist.check_playlist_name }}</h3>
                <p class="creator">{{ playlist.check_playlist_detail.playlist_creator?.user_name || '未知创建者' }}</p>
                <p class="song-count">{{ playlist.check_playlist_detail.songs.length }}首歌曲</p>
                <p class="intro" v-if="playlist.check_playlist_intro">{{ playlist.check_playlist_intro }}</p>
              </div>
            </div>
            
            <div class="playlist-status">
              <span 
                class="status-tag"
                :class="getStatusClass(playlist.check_status)"
              >
                {{ playlist.check_status_display }}
              </span>
              <p class="submit-time">提交时间: {{ formatDate(playlist.check_submit_time) }}</p>
              <p v-if="playlist.check_admin_name" class="check-admin">审核人: {{ playlist.check_admin_name }}</p>
              <p v-if="playlist.check_modify_time" class="modify-time">审核时间: {{ formatDate(playlist.check_modify_time) }}</p>
            </div>
            
            <div class="playlist-actions">
              <button 
                v-if="playlist.check_status === 0" 
                class="btn btn-approve"
                @click="showApproveDialog(playlist)"
              >
                通过
              </button>
              <button 
                v-if="playlist.check_status === 0" 
                class="btn btn-reject"
                @click="showRejectDialog(playlist)"
              >
                拒绝
              </button>
              <button 
                class="btn" style="background-color: #ffc107; color: #333;"
                @click="showClearDialog(playlist)"
              >
                清空审核
              </button>
              <button 
                class="btn btn-detail"
                @click="viewPlaylistDetail(playlist.check_playlist_detail.playlist_id)"
              >
                查看详情
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 分页 -->
      <div v-if="total > 0" class="pagination">
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
    </div>
    
    <!-- 审核通过对话框 -->
    <div v-if="approveDialogVisible" class="dialog-overlay" @click="approveDialogVisible = false">
      <div class="dialog" @click.stop>
        <h3>审核通过</h3>
        <p>确定要通过 "{{ currentPlaylist?.check_playlist_name }}" 的审核吗？</p>
        <div class="dialog-actions">
          <button @click="approveDialogVisible = false">取消</button>
          <button class="btn-approve" @click="approvePlaylist">确定通过</button>
        </div>
      </div>
    </div>
    
    <!-- 审核拒绝对话框 -->
    <div v-if="rejectDialogVisible" class="dialog-overlay" @click="rejectDialogVisible = false">
      <div class="dialog" @click.stop>
        <h3>审核拒绝</h3>
        <p>请输入拒绝理由：</p>
        <textarea v-model="rejectComment" rows="4"></textarea>
        <div class="dialog-actions">
          <button @click="rejectDialogVisible = false">取消</button>
          <button class="btn-reject" @click="rejectPlaylist">确定拒绝</button>
        </div>
      </div>
    </div>
    
    <!-- 清空审核对话框 -->
    <div v-if="clearDialogVisible" class="dialog-overlay" @click="clearDialogVisible = false">
      <div class="dialog" @click.stop>
        <h3>清空审核</h3>
        <p>确定要将 "{{ currentPlaylist?.check_playlist_name }}" 的审核状态重置为待审核吗？</p>
        <div class="dialog-actions">
          <button @click="clearDialogVisible = false">取消</button>
          <button class="btn" style="background-color: #ffc107; color: #333;" @click="clearPlaylistAction">确定清空</button>
        </div>
      </div>
    </div>
    
    <!-- 批量清空审核对话框 -->
    <div v-if="clearAllDialogVisible" class="dialog-overlay" @click="clearAllDialogVisible = false">
      <div class="dialog" @click.stop>
        <h3>批量清空审核</h3>
        <p>确定要清空所有已通过或已拒绝的审核记录吗？此操作不可恢复。</p>
        <div class="dialog-actions">
          <button @click="clearAllDialogVisible = false">取消</button>
          <button class="btn btn-clear-all" @click="clearAllPlaylistsAction">确定清空</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useAuditStore } from '@/stores/audit'

const authStore = useAuthStore()
const router = useRouter()

// 返回上一页
const handleBack = () => {
  router.back()
}
const auditStore = useAuditStore()

// 歌单列表
const playlists = ref<any[]>([])
const loading = ref(false)
const statusFilter = ref('')

// 分页
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框
const approveDialogVisible = ref(false)
const rejectDialogVisible = ref(false)
const clearDialogVisible = ref(false)
const clearAllDialogVisible = ref(false)
const currentPlaylist = ref<any>(null)
const rejectComment = ref('')

onMounted(async () => {
  // 检查权限
  if (authStore.user?.user_type !== 2) {
    router.push('/home')
    return
  }
  
  await loadPlaylists()
})

const loadPlaylists = async () => {
  loading.value = true
  try {
    // 调用审核API获取歌单审核列表
    const params = {
      status: statusFilter.value || undefined,
      page: page.value,
      page_size: pageSize.value
    }
    const response = await auditStore.fetchCheckPlaylists(params)
    playlists.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('加载歌单审核列表失败:', error)
  } finally {
    loading.value = false
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

const showApproveDialog = (playlist: any) => {
  currentPlaylist.value = playlist
  approveDialogVisible.value = true
}

const showRejectDialog = (playlist: any) => {
  currentPlaylist.value = playlist
  rejectComment.value = ''
  rejectDialogVisible.value = true
}

const showClearDialog = (playlist: any) => {
  currentPlaylist.value = playlist
  clearDialogVisible.value = true
}

const approvePlaylist = async () => {
  if (!currentPlaylist.value) return
  
  try {
    await auditStore.approvePlaylistAction({ checkId: currentPlaylist.value.check_id })
    await loadPlaylists()
    approveDialogVisible.value = false
  } catch (error) {
    console.error('审核通过失败:', error)
  }
}

const rejectPlaylist = async () => {
  if (!currentPlaylist.value) return
  
  try {
    await auditStore.rejectPlaylistAction({ checkId: currentPlaylist.value.check_id, comment: rejectComment.value })
    await loadPlaylists()
    rejectDialogVisible.value = false
  } catch (error) {
    console.error('审核拒绝失败:', error)
  }
}

const clearPlaylistAction = async () => {
  if (!currentPlaylist.value) return
  
  try {
    await auditStore.clearPlaylistAction({ checkId: currentPlaylist.value.check_id })
    await loadPlaylists()
    clearDialogVisible.value = false
  } catch (error) {
    console.error('清空审核失败:', error)
  }
}

const showClearAllDialog = () => {
  clearAllDialogVisible.value = true
}

const clearAllPlaylistsAction = async () => {
  try {
    await auditStore.clearAllPlaylistsAction()
    await loadPlaylists()
    clearAllDialogVisible.value = false
  } catch (error) {
    console.error('批量清空审核失败:', error)
  }
}

const viewPlaylistDetail = (playlistId: number) => {
  // 这里假设歌单详情页路由为 /playlists/:id
  router.push(`/playlists/${playlistId}`)
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
    loadPlaylists()
  }
}

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
    loadPlaylists()
  }
}

const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value)
})
</script>

<style scoped>
.check-playlists {
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

.btn-clear-all {
  background: #ffc107;
  color: #333;
}

.btn-clear-all:hover {
  background: #e0a800;
}

.playlists-list {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.loading, .empty {
  text-align: center;
  padding: 50px;
  color: #666;
}

.playlist-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.playlist-item {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.3s;
}

.playlist-item:hover {
  background-color: #f9f9f9;
}

.playlist-info {
  display: flex;
  align-items: flex-start;
  flex: 1;
  gap: 15px;
}

.playlist-cover img {
  width: 100px;
  height: 100px;
  border-radius: 4px;
  object-fit: cover;
}

.playlist-details h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
  color: #333;
}

.creator, .song-count {
  margin: 3px 0;
  font-size: 14px;
  color: #666;
}

.intro {
  margin: 10px 0 0 0;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  max-width: 500px;
}

.playlist-status {
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

.submit-time, .check-admin, .modify-time {
  margin: 5px 0;
  font-size: 12px;
  color: #999;
}

.playlist-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.btn-approve {
  background: #28a745;
  color: white;
}

.btn-approve:hover {
  background: #218838;
}

.btn-reject {
  background: #dc3545;
  color: white;
}

.btn-reject:hover {
  background: #c82333;
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

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background: white;
  padding: 25px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.dialog h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}

.dialog p {
  margin-bottom: 20px;
  color: #666;
}

.dialog textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 20px;
  font-size: 14px;
  resize: vertical;
  min-height: 100px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.dialog-actions button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}
</style>