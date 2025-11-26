<template>
  <div class="user-detail-container">
    <el-card v-if="user">
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
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { getUserDetail, followUser, unfollowUser } from '@/api/user'

const route = useRoute()
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
    // TODO: 检查是否已关注
  } catch (error) {
    ElMessage.error('加载用户信息失败')
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

