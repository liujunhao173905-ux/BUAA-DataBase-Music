<template>
  <div class="check-users">
    <div class="container">
      <el-card shadow="hover" class="page-card">
        <template #header>
          <el-page-header @back="handleBack" content="用户审核" title="返回" />
        </template>
      
        <div class="filters">
          <select v-model="statusFilter" @change="loadUsers">
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
      
        <div class="users-list-container">
          <div v-if="loading" class="loading">加载中...</div>
          <div v-else-if="users.length === 0" class="empty">暂无用户审核记录</div>
          <div v-else class="user-items">
          <div 
            v-for="user in users" 
            :key="user.check_id" 
            class="user-item"
          >
            <div class="user-info">
              <div class="user-avatar">
                <img :src="user.check_user_avatar || '/default-avatar.png'" alt="用户头像">
              </div>
              <div class="user-details">
                <h3>{{ user.check_user_name }}</h3>
                <p class="user-type">{{ getUserTypeText(user.check_user_type) }}</p>
                <p class="mobile" v-if="user.check_user_mobile">{{ user.check_user_mobile }}</p>
                <p class="email" v-if="user.check_user_detail.email">{{ user.check_user_detail.email }}</p>
              </div>
            </div>
            
            <div class="user-status">
              <span 
                class="status-tag"
                :class="getStatusClass(user.check_status)"
              >
                {{ user.check_status_display }}
              </span>
              <p class="submit-time">提交时间: {{ formatDate(user.check_submit_time) }}</p>
              <p v-if="user.check_admin_name" class="check-admin">审核人: {{ user.check_admin_name }}</p>
              <p v-if="user.check_modify_time" class="modify-time">审核时间: {{ formatDate(user.check_modify_time) }}</p>
            </div>
            
            <div class="user-actions">
              <button 
                v-if="user.check_status === 0" 
                class="btn btn-approve"
                @click="showApproveDialog(user)"
              >
                通过
              </button>
              <button 
                v-if="user.check_status === 0" 
                class="btn btn-reject"
                @click="showRejectDialog(user)"
              >
                拒绝
              </button>
              <button 
                class="btn" style="background-color: #ffc107; color: #333;"
                @click="showClearDialog(user)"
              >
                清空审核
              </button>
              <button 
                class="btn btn-detail"
                @click="viewUserDetail(user.check_user_detail.user_id)"
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
    
    <!-- 审核通过对话框 -->
    <div v-if="approveDialogVisible" class="dialog-overlay" @click="approveDialogVisible = false">
      <div class="dialog" @click.stop>
        <h3>审核通过</h3>
        <p>确定要通过 "{{ currentUser?.check_user_name }}" 的歌手注册申请吗？</p>
        <div class="dialog-actions">
          <button @click="approveDialogVisible = false">取消</button>
          <button class="btn-approve" @click="approveUser">确定通过</button>
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
          <button class="btn-reject" @click="rejectUser">确定拒绝</button>
        </div>
      </div>
    </div>
    
    <!-- 清空审核对话框 -->
    <div v-if="clearDialogVisible" class="dialog-overlay" @click="clearDialogVisible = false">
      <div class="dialog" @click.stop>
        <h3>清空审核</h3>
        <p>确定要将用户 "{{ currentUser?.check_user_detail.nickname }}" 的审核状态重置为待审核吗？</p>
        <div class="dialog-actions">
          <button @click="clearDialogVisible = false">取消</button>
          <button class="btn" style="background-color: #ffc107; color: #333;" @click="clearUserAction">确定清空</button>
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
          <button class="btn btn-clear-all" @click="clearAllUsersAction">确定清空</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useAuditStore } from '../../stores/audit'
import { ArrowLeft } from '@element-plus/icons-vue'

const authStore = useAuthStore()
const router = useRouter()
const auditStore = useAuditStore()

// 返回上一页
const handleBack = () => {
  router.back()
}

// 用户列表
const users = ref<any[]>([])
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
const currentUser = ref<any>(null)
const rejectComment = ref('')

onMounted(async () => {
  // 检查权限
  if (authStore.user?.user_type !== 2) {
    router.push('/home')
    return
  }
  
  await loadUsers()
})

const loadUsers = async () => {
  loading.value = true
  try {
    // 调用审核API获取用户审核列表
    const params = {
      status: statusFilter.value || undefined,
      page: page.value,
      page_size: pageSize.value
    }
    const response = await auditStore.fetchCheckUsers(params)
    users.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('加载用户审核列表失败:', error)
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

const getUserTypeText = (type: number) => {
  switch (type) {
    case 0: return '普通用户'
    case 1: return '歌手'
    case 2: return '管理员'
    default: return '未知类型'
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const showApproveDialog = (user: any) => {
  currentUser.value = user
  approveDialogVisible.value = true
}

const showRejectDialog = (user: any) => {
  currentUser.value = user
  rejectComment.value = ''
  rejectDialogVisible.value = true
}

const showClearDialog = (user: any) => {
  currentUser.value = user
  clearDialogVisible.value = true
}

const approveUser = async () => {
  if (!currentUser.value) return
  
  try {
    await auditStore.approveUserAction({
      checkId: currentUser.value.check_id
    })
    await loadUsers()
    approveDialogVisible.value = false
  } catch (error) {
    console.error('审核通过失败:', error)
  }
}

const rejectUser = async () => {
  if (!currentUser.value) return
  
  try {
    await auditStore.rejectUserAction({
      checkId: currentUser.value.check_id,
      comment: rejectComment.value
    })
    await loadUsers()
    rejectDialogVisible.value = false
  } catch (error) {
    console.error('审核拒绝失败:', error)
  }
}

const clearUserAction = async () => {
  if (!currentUser.value) return
  
  try {
    await auditStore.clearUserAction({ checkId: currentUser.value.check_id })
    await loadUsers()
    clearDialogVisible.value = false
  } catch (error) {
    console.error('清空审核失败:', error)
  }
}

const showClearAllDialog = () => {
  clearAllDialogVisible.value = true
}

const clearAllUsersAction = async () => {
  try {
    await auditStore.clearAllUsersAction()
    await loadUsers()
    clearAllDialogVisible.value = false
  } catch (error) {
    console.error('批量清空审核失败:', error)
  }
}

const viewUserDetail = (userId: number) => {
  router.push(`/user/${userId}`)
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
    loadUsers()
  }
}

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
    loadUsers()
  }
}

const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value)
})


</script>

<style scoped>
.check-users {
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

/*
.users-list {
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

.user-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.3s;
}

.user-item:hover {
  background-color: #f9f9f9;
}

.user-info {
  display: flex;
  align-items: center;
  flex: 1;
  gap: 15px;
}

.user-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
  color: #333;
}

.user-type, .mobile, .email {
  margin: 3px 0;
  font-size: 14px;
  color: #666;
}

.user-status {
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

.user-actions {
  display: flex;
  gap: 10px;
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