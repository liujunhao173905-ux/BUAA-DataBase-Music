<template>
  <div class="user-detail-container">
    <el-card v-if="user">
      <template #header>
        <div style="display: flex; align-items: center; gap: 16px;">
          <el-button type="default" @click="handleBack">
            <el-icon><ArrowLeft /></el-icon> 返回
          </el-button>
          <h2 style="margin: 0;">{{ user.user_type_display === '歌手' ? '歌手详情' : '用户详情' }}</h2>
        </div>
      </template>
      <div class="user-header">
        <el-avatar :size="100" :src="user.user_avatar" />
        <div class="user-info">
          <h2>{{ user.user_name }}</h2>
          <el-tag :type="getUserTypeTag(user.user_type)">
            {{ user.user_type_display }}
          </el-tag>
          <p>粉丝: {{ user.followers_count }} | 关注: {{ user.following_count }}</p>
        </div>
        <el-button
          v-if="authStore.isAuthenticated && authStore.user?.user_id !== user.user_id"
          type="primary"
          @click="handleFollow"
        >
          {{ isFollowing ? '取消关注' : '关注' }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Plus, Check } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { getUserDetail, followUser, unfollowUser } from '@/api/user'
import request from '@/api/request'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const user = ref<any>(null)
const isFollowing = ref(false)

onMounted(async () => {
  const userId = parseInt(route.params.id as string)
  await loadUserDetail(userId)
})

const loadUserDetail = async (userId: number) => {
  try {
    user.value = await getUserDetail(userId)
    // 检查是否已关注
    if (authStore.isAuthenticated && authStore.user?.user_id !== userId) {
      checkFollowStatus(userId)
    }
  } catch (error) {
    ElMessage.error('加载用户信息失败')
  }
}

const checkFollowStatus = async (userId: number) => {
  try {
    const response = await request.get(`/users/${userId}/follow/`)
    isFollowing.value = response.is_following
  } catch (error) {
    console.error('检查关注状态失败:', error)
  }
}

const getUserTypeTag = (type: number) => {
  const tags = ['', 'success', 'danger']
  return tags[type] || ''
}

const handleFollow = async () => {
  if (!user.value) return
  
  try {
    if (isFollowing.value) {
      await unfollowUser(user.value.user_id)
      ElMessage.success('取消关注成功')
    } else {
      await followUser(user.value.user_id)
      ElMessage.success('关注成功')
    }
    isFollowing.value = !isFollowing.value
  } catch (error: any) {
    ElMessage.error(error?.error || '操作失败')
  }
}

const handleBack = () => {
  router.back()
}
</script>

<style scoped>
.user-detail-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.user-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  flex: 1;
}

.user-info h2 {
  margin: 0 0 10px 0;
}
</style>

