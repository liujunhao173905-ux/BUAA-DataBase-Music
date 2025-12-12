<template>
  <div class="my-bought-songs">
    <router-link to="/home" style="text-decoration: none; margin-right: 20px;">
      <h1 style="display: inline-block; margin: 0; color: #409eff; margin-bottom: 20px;">音乐平台</h1>
    </router-link>
    
    <el-card class="bought-songs-card">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-button type="default" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <h2>我的购买</h2>
          </div>
        </div>
      </template>
      
      <div class="song-card" v-loading="loading">
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
                @click="handleSongClick(scope.row)"
              >
                试听
              </el-button>
              <el-button
                type="success"
                size="small"
                @click="handleToggleStar(scope.row)"
              >
                {{ scope.row.is_starred ? '取消收藏' : '收藏' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <el-empty v-else description="暂无购买歌曲" />
    </div>
  </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/request'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const loading = ref(false)
const songs = ref<any[]>([])

const formatPrice = (price: any) => {
  const numPrice = Number(price)
  if (!price || isNaN(numPrice)) return '免费'
  return `¥${numPrice.toFixed(2)}`
}

const fetchBoughtSongs = async () => {
  loading.value = true
  try {
    const response = await request.get('/music/songs/bought/')
    songs.value = response
    
    // 为了提供更好的用户体验，获取已收藏状态
    await fetchStarredSongsStatus()
  } catch (error) {
    ElMessage.error('加载购买歌曲失败')
    console.error('Failed to fetch bought songs:', error)
  } finally {
    loading.value = false
  }
}

const fetchStarredSongsStatus = async () => {
  try {
    const response = await request.get('/music/songs/starred/')
    const starredSongs = response
    
    // 标记已收藏状态
    songs.value.forEach(song => {
      song.is_starred = starredSongs.some((s: any) => s.song_id === song.song_id)
    })
  } catch (error) {
    console.error('Failed to fetch starred status:', error)
    // 不影响主功能
  }
}

const handleSongClick = (song: any) => {
  router.push(`/songs/${song.song_id}`)
}

const handleToggleStar = async (song: any) => {
  try {
    if (song.is_starred) {
      // 取消收藏
      await request.delete(`/music/songs/${song.song_id}/unstar/`)
      song.is_starred = false
      ElMessage.success('取消收藏成功')
    } else {
      // 添加收藏
      await request.post(`/music/songs/${song.song_id}/star/`)
      song.is_starred = true
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试')
  }
}

const handleBack = () => {
  router.back()
}

onMounted(() => {
  fetchBoughtSongs()
})
</script>

<style scoped>
.my-bought-songs {
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