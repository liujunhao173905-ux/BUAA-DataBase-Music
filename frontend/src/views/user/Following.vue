<template>
  <div class="following-container">
    <div class="header">
      <el-page-header @back="$router.back()" content="关注歌手" />
    </div>

    <div class="singer-list" v-loading="loading">
      <div v-for="singer in singers" :key="singer.user_id" class="singer-item" @click="handleSingerClick(singer.user_id)">
        <el-avatar :size="50" :src="singer.user_avatar" class="avatar">
          {{ singer.user_name?.charAt(0)?.toUpperCase() }}
        </el-avatar>
        <div class="info">
          <div class="name">{{ singer.user_name }}</div>
          <div class="desc">{{ singer.user_type_display || '歌手' }}</div>
        </div>
        <el-button 
          type="primary" 
          plain 
          size="small" 
          @click.stop="handleUnfollow(singer)"
        >
          已关注
        </el-button>
      </div>
      <el-empty v-if="!loading && singers.length === 0" description="暂无关注的歌手" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMyFollowingSingers, unfollowUser, type UserInfo } from '@/api/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const singers = ref<UserInfo[]>([])
const loading = ref(false)

const fetchSingers = async () => {
  loading.value = true
  try {
    const res = await getMyFollowingSingers()
    // Assuming the API returns a standard pagination result or list
    // Adjust based on actual API response structure if needed.
    // Based on user.ts, it returns { count: number; results: any[] }
    if (res && (res as any).results) {
        singers.value = (res as any).results
    } else if (Array.isArray(res)) {
        singers.value = res
    }
  } catch (error) {
    console.error('Failed to fetch singers:', error)
    ElMessage.error('获取关注列表失败')
  } finally {
    loading.value = false
  }
}

const handleSingerClick = (id: number) => {
  router.push(`/user/${id}`)
}

const handleUnfollow = async (singer: UserInfo) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消关注 ${singer.user_name} 吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await unfollowUser(singer.user_id)
    ElMessage.success('已取消关注')
    fetchSingers() // Refresh list
  } catch (error: any) {
    if (error !== 'cancel') {
        ElMessage.error('操作失败')
    }
  }
}

onMounted(() => {
  fetchSingers()
})
</script>

<style scoped>
.following-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.header {
  margin-bottom: 20px;
}

.singer-list {
  background: white;
  border-radius: 8px;
  padding: 10px;
}

.singer-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.singer-item:last-child {
  border-bottom: none;
}

.singer-item:hover {
  background-color: #f9f9f9;
}

.avatar {
  margin-right: 15px;
}

.info {
  flex: 1;
}

.name {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.desc {
  font-size: 12px;
  color: #909399;
}
</style>
