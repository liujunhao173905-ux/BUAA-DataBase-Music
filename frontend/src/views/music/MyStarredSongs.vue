<template>
  <div class="my-starred-songs">
    <div style="margin-bottom: 20px;">
      <router-link to="/home" style="text-decoration: none; margin-right: 20px;">
        <h1 style="display: inline-block; margin: 0; color: #409eff;">音乐平台</h1>
      </router-link>
      <el-page-header content="我的收藏" @back="handleBack" />
    </div>
    
    <el-card class="song-card" v-loading="loading">
      <div v-if="songs.length > 0" class="song-list">
        <el-table
          :data="songs"
          style="width: 100%"
          border
        >
          <el-table-column prop="song_name" label="歌曲名称" width="200">
            <template #default="scope">
              <span class="song-name" @click="handleSongClick(scope.row)">{{ scope.row.song_name }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="song_singer_name" label="歌手" width="120"></el-table-column>
          <el-table-column prop="song_duration" label="时长" width="100"></el-table-column>
          <el-table-column prop="song_price" label="价格" width="100">
            <template #default="scope">
              {{ formatPrice(scope.row.song_price) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button
                type="primary"
                size="small"
                :disabled="scope.row.is_bought"
                @click="handleBuySong(scope.row)"
              >
                {{ scope.row.is_bought ? '已购买' : '购买' }}
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="handleRemoveStar(scope.row)"
              >
                取消收藏
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <el-empty v-else description="暂无收藏歌曲" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/request'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const loading = ref(false)
const songs = ref<any[]>([])

const formatPrice = (price: any) => {
  const numPrice = Number(price)
  if (!price || isNaN(numPrice)) return '免费'
  return `¥${numPrice.toFixed(2)}`
}

const fetchStarredSongs = async () => {
  loading.value = true
  try {
    const response = await request.get('/music/songs/starred/')
    songs.value = response
  } catch (error) {
    ElMessage.error('加载收藏歌曲失败')
    console.error('Failed to fetch starred songs:', error)
  } finally {
    loading.value = false
  }
}

const handleSongClick = (song: any) => {
  router.push(`/songs/${song.song_id}`)
}

const handleBuySong = async (song: any) => {
  try {
    await request.post(`/music/songs/${song.song_id}/buy/`)
    song.is_bought = true
    ElMessage.success('购买成功')
  } catch (error: any) {
    const errorMessage = error.response?.data?.error || '购买失败'
    ElMessage.error(errorMessage)
  }
}

const handleRemoveStar = async (song: any) => {
  try {
    await request.delete(`/music/songs/${song.song_id}/unstar/`)
    const index = songs.value.findIndex(s => s.song_id === song.song_id)
    if (index > -1) {
      songs.value.splice(index, 1)
    }
    ElMessage.success('取消收藏成功')
  } catch (error) {
    ElMessage.error('取消收藏失败')
  }
}

const handleBack = () => {
  router.back()
}

onMounted(() => {
  fetchStarredSongs()
})
</script>

<style scoped>
.my-starred-songs {
  padding: 24px;
}

.song-card {
  margin-top: 16px;
}

.song-name {
  cursor: pointer;
  color: #409EFF;
}

.song-name:hover {
  text-decoration: underline;
}
</style>