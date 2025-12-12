<template>
  <div class="playlist-detail-page">
    <el-card v-if="loading" shadow="never">
      <el-skeleton :rows="6" animated />
    </el-card>
    
    <el-card v-else shadow="never" class="playlist-card">
      <div class="playlist-header">
        <el-image
          :src="playlist.playlist_cover || ''"
          fit="cover"
          class="playlist-cover"
        >
          <template #error>
            <div class="image-slot">暂无封面</div>
          </template>
        </el-image>
        <div class="playlist-info">
          <el-button type="default" @click="handleBack" style="margin-bottom: 10px;">
            <el-icon><ArrowLeft /></el-icon> 返回
          </el-button>
          <h1>{{ playlist.playlist_name }}</h1>
          <p class="playlist-creator">创建者：{{ playlist.playlist_creator_name }}</p>
          <p class="playlist-songs-count">{{ playlist.song_count }}首歌曲</p>
          <p class="playlist-date">创建时间：{{ formatDate(playlist.playlist_createtime) }}</p>
          <div class="playlist-intro-container">
            <h3>歌单介绍</h3>
            <p class="playlist-intro">{{ playlist.playlist_intro || '暂无介绍' }}</p>
          </div>
          <div class="playlist-actions">
            <el-button 
              :loading="starLoading"
              @click="toggleStar"
              :type="isStarred ? 'primary' : 'default'"
              style="margin-right: 10px;"
            >
              {{ isStarred ? '取消收藏' : '收藏歌单' }}
            </el-button>
            <el-button type="success" @click="handlePlayAll" :disabled="songs.length === 0">
                <el-icon><VideoPlay /></el-icon> 播放全部
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="playlist-songs">
        <h2>歌单歌曲</h2>
        <el-table
          :data="songs"
          style="width: 100%"
          border
        >
          <el-table-column label="序号" type="index" width="80" />
          <el-table-column label="歌曲名称" min-width="200">
            <template #default="scope">
              <span @click="handleSongClick(scope.row.song_id)">{{ scope.row.song_name }}</span>
            </template>
          </el-table-column>
          <el-table-column label="歌手" min-width="150">
            <template #default="scope">
              <span>{{ scope.row.song_singer_name }}</span>
            </template>
          </el-table-column>
          <el-table-column label="时长" width="100">
            <template #default="scope">
              <span>{{ formatDuration(scope.row.song_duration) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="价格" width="100">
            <template #default="scope">
              <span class="price">{{ formatPrice(scope.row.song_price) }}</span>
            </template>
          </el-table-column>
        </el-table>
        
        <div v-if="songs.length === 0" class="empty-songs">
          <el-empty description="暂无歌曲" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, VideoPlay } from '@element-plus/icons-vue'
import request from '@/api/request'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const playlist = ref<any>({ song_count: 0 })
const songs = ref<any[]>([])
const isStarred = ref(false)
const starLoading = ref(false)

onMounted(async () => {
  await loadPlaylistDetail()
})

const loadPlaylistDetail = async () => {
  loading.value = true
  try {
    // 确保playlistId是字符串类型
    const playlistId = String(route.params.id)
    const response = await request.get(`/playlists/${playlistId}/`)
    playlist.value = response
    // 后端返回的歌曲列表字段名是'songs'，每个元素都有'song'属性包含实际歌曲信息
    songs.value = response.songs?.map((item: any) => item.song) || []
    // 检查是否已收藏
    if (authStore.isAuthenticated) {
      checkStarStatus(playlistId)
    }
  } catch (error) {
    ElMessage.error('加载歌单详情失败')
    console.error('Failed to load playlist detail:', error)
  } finally {
    loading.value = false
  }
}

const checkStarStatus = async (playlistId: string) => {
  try {
    const response = await request.get(`/playlists/${playlistId}/check-star/`)
    isStarred.value = response.is_starred
  } catch (error) {
    console.error('Failed to check star status:', error)
  }
}

const toggleStar = async () => {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  starLoading.value = true
  try {
    // 确保playlistId是字符串类型
    const playlistId = String(route.params.id)
    if (isStarred.value) {
      await request.delete(`/playlists/${playlistId}/unstar/`)
      ElMessage.success('取消收藏成功')
    } else {
      await request.post(`/playlists/${playlistId}/star/`)
      ElMessage.success('收藏成功')
    }
    isStarred.value = !isStarred.value
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试')
  } finally {
    starLoading.value = false
  }
}

const handleSongClick = (songId: number) => {
  router.push({ name: 'SongDetail', params: { id: String(songId) } })
}

const formatDuration = (duration: any) => {
  const minutes = Math.floor(duration / 60)
  const seconds = Math.floor(duration % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

const formatPrice = (price: any) => {
  // 检查price是否为有效数字
  const priceNum = Number(price)
  if (!price || isNaN(priceNum)) return '免费'
  return `¥${priceNum.toFixed(2)}`
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

const handleBack = () => {
  // 检查路由历史记录，如果上一个页面是我的歌单页，则直接返回
  const fromPath = sessionStorage.getItem('fromPath')
  if (fromPath === '/my/playlists') {
    sessionStorage.removeItem('fromPath')
    router.push('/my/playlists')
  } else {
    router.back()
  }
}

const handlePlayAll = () => {
  if (songs.value.length === 0) {
    ElMessage.warning('歌单中暂无歌曲')
    return
  }
  // 这里可以添加播放全部歌曲的逻辑
  ElMessage.success(`开始播放${playlist.value.playlist_name}中的全部歌曲`)
  // 例如：调用音乐播放器组件播放所有歌曲
  console.log('播放全部歌曲:', songs.value)
}
</script>

<style scoped>
.playlist-detail-page {
  padding: 24px;
}

.playlist-card {
  margin-bottom: 20px;
}

.playlist-header {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.playlist-cover {
  width: 200px;
  height: 200px;
  border-radius: 8px;
}

.image-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  color: #909399;
}

.playlist-info {
  flex: 1;
}

.playlist-info h1 {
  font-size: 28px;
  margin-bottom: 10px;
}

.playlist-creator {
  color: #909399;
  margin-bottom: 5px;
}

.playlist-songs-count {
  color: #909399;
  margin-bottom: 5px;
}

.playlist-date {
  color: #909399;
  margin-bottom: 15px;
}

.playlist-intro-container {
  margin: 15px 0;
}

.playlist-intro-container h3 {
  font-size: 16px;
  margin-bottom: 8px;
  color: #303133;
}

.playlist-intro {
  line-height: 1.6;
  color: #606266;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.playlist-actions {
  margin-top: 20px;
}

.playlist-songs {
  margin-top: 30px;
}

.playlist-songs h2 {
  font-size: 20px;
  margin-bottom: 15px;
}

.empty-songs {
  margin-top: 50px;
}

.price {
  color: #f56c6c;
  font-weight: bold;
}
</style>