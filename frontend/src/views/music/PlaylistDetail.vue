<template>
  <div class="playlist-detail-page">
    <!-- Dynamic Background -->
    <div class="page-bg" v-if="playlist.playlist_cover" :style="{ backgroundImage: `url(${playlist.playlist_cover})` }"></div>
    <div class="page-bg-overlay"></div>

    <div class="content-wrapper">
      <el-card v-if="loading" shadow="never" class="glass-card">
        <el-skeleton :rows="6" animated />
      </el-card>
      
      <el-card v-else shadow="never" class="glass-card">
        <template #header>
          <el-page-header @back="handleBack" content="歌单详情" title="返回" />
        </template>
        <div class="playlist-header">
          <div class="cover-container">
            <el-image
              :src="playlist.playlist_cover || ''"
              fit="cover"
              class="playlist-cover"
            >
              <template #error>
                <div class="image-slot">暂无封面</div>
              </template>
            </el-image>
          </div>
          <div class="playlist-info">
            <h1 class="playlist-title">{{ playlist.playlist_name }}</h1>
            <div class="playlist-meta">
              <p class="playlist-creator">
                <el-icon><User /></el-icon> 创建者：{{ playlist.playlist_creator_name }}
              </p>
              <p class="playlist-date">
                <el-icon><Calendar /></el-icon> 创建时间：{{ formatDate(playlist.playlist_createtime) }}
              </p>
              <p class="playlist-songs-count">
                <el-icon><Headset /></el-icon> {{ playlist.song_count }}首歌曲
              </p>
            </div>
            
            <div class="playlist-intro-container" v-if="playlist.playlist_intro">
              <p class="playlist-intro">{{ playlist.playlist_intro }}</p>
            </div>

            <div class="playlist-actions">
              <el-button 
                type="primary" 
                class="play-all-btn"
                @click="handlePlayAll" 
                :disabled="songs.length === 0"
                round
              >
                  <el-icon><VideoPlay /></el-icon> 播放全部
              </el-button>
              <el-button 
                :loading="starLoading"
                @click="toggleStar"
                :type="isStarred ? 'warning' : 'default'"
                :plain="!isStarred"
                round
                class="star-btn"
              >
                <el-icon><StarFilled v-if="isStarred" /><Star v-else /></el-icon>
                {{ isStarred ? '已收藏' : '收藏歌单' }}
              </el-button>
            </div>
          </div>
        </div>
        
        <div class="playlist-songs">
          <h2>歌曲列表</h2>
          <el-table
            :data="songs"
            style="width: 100%"
            class="transparent-table"
            :row-class-name="tableRowClassName"
            @row-dblclick="handlePlaySong"
          >
            <el-table-column label="序号" type="index" width="60" align="center" />
            <el-table-column label="歌曲名称" min-width="200" align="center">
              <template #default="scope">
                <div class="song-info-cell" @click="handlePlaySong(scope.row)">
                  <div class="cover-wrapper">
                    <el-image 
                      v-if="scope.row.song_cover" 
                      :src="scope.row.song_cover" 
                      class="song-cover-mini" 
                      fit="cover" 
                    />
                    <div class="hover-play"><el-icon><VideoPlay /></el-icon></div>
                  </div>
                  <span class="song-name" :class="{ 'active': isPlaying(scope.row) }">{{ scope.row.song_name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="歌手" min-width="150" align="center">
              <template #default="scope">
                <span class="singer-name">{{ scope.row.song_singer_name }}</span>
              </template>
            </el-table-column>
            <el-table-column label="时长" width="100" align="center">
              <template #default="scope">
                <span class="duration">{{ formatDuration(scope.row.song_duration) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="价格" width="100" align="center">
              <template #default="scope">
                <span class="price">{{ formatPrice(scope.row.song_price) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right" align="center">
              <template #default="scope">
                <div class="action-buttons">
                  <el-button
                    type="primary"
                    link
                    @click.stop="handleDetail(scope.row)"
                  >
                    详情
                  </el-button>
                  <el-button 
                    type="primary" 
                    link 
                    @click.stop="handlePlaySong(scope.row)"
                  >
                    <el-icon><VideoPlay /></el-icon>
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
          
          <div v-if="songs.length === 0" class="empty-songs">
            <el-empty description="暂无歌曲" />
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, VideoPlay, Download, Star, StarFilled, User, Calendar, Headset } from '@element-plus/icons-vue'
import request from '@/api/request'
import { useAuthStore } from '@/stores/auth'
import { usePlayerStore } from '@/stores/player'
import type { Song } from '@/api/music'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const playerStore = usePlayerStore()

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
    const playlistId = String(route.params.id)
    const response = await request.get(`/playlists/${playlistId}/`)
    playlist.value = response
    songs.value = response.songs?.map((item: any) => item.song) || []
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
  if (authStore.user) {
    if (playlist.value.playlist_creator === authStore.user.user_id) {
      ElMessage.warning('不能收藏自己的歌单')
      return
    }
  }
  else {
    ElMessage.warning('用户不存在')
    return
  }
  
  starLoading.value = true
  try {
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
  const numPrice = Number(price)
  if (price === null || price === undefined || isNaN(numPrice)) {
    return '免费'
  }
  if (numPrice <= 0) {
    return '免费'
  }
  return `¥${numPrice.toFixed(2)}`
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const handleDetail = (song: Song) => {
  router.push(`/songs/${song.song_id}`)
}

const handleBack = () => {
  router.back()
}

const handlePlayAll = () => {
  if (songs.value.length === 0) {
    ElMessage.warning('歌单中暂无歌曲')
    return
  }
  playerStore.setPlaylist(songs.value)
  playerStore.playSong(songs.value[0])
}

const handlePlaySong = (song: any) => {
  playerStore.setPlaylist(songs.value)
  playerStore.playSong(song)
}

const isPlaying = (song: any) => {
  return playerStore.currentSong?.song_id === song.song_id
}

const tableRowClassName = ({ rowIndex }: { rowIndex: number }) => {
  return 'transparent-row'
}
</script>

<style scoped>
.playlist-detail-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
}

.page-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  filter: blur(60px) brightness(0.6);
  z-index: 0;
  transform: scale(1.1);
}

.page-bg-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.5));
  z-index: 1;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.75) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  overflow: hidden;
}

:deep(.el-card__header) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 15px 20px;
}

.playlist-header {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
  padding: 20px;
}

.cover-container {
  flex-shrink: 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  overflow: hidden;
}

.playlist-cover {
  width: 240px;
  height: 240px;
  display: block;
}

.playlist-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.playlist-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 15px 0;
  color: #303133;
}

.playlist-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  color: #606266;
  font-size: 14px;
}

.playlist-meta p {
  display: flex;
  align-items: center;
  gap: 5px;
  margin: 0;
}

.playlist-intro-container {
  background: rgba(255, 255, 255, 0.4);
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 25px;
  flex: 1;
}

.playlist-intro {
  line-height: 1.6;
  color: #606266;
  font-size: 14px;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.playlist-actions {
  display: flex;
  gap: 15px;
}

.play-all-btn {
  padding: 12px 30px;
  font-size: 16px;
}

.playlist-songs {
  padding: 0 20px;
}

.playlist-songs h2 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #303133;
  padding-left: 10px;
  border-left: 4px solid #409eff;
}

/* Transparent Table Styles */
:deep(.el-table) {
  background-color: transparent !important;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(255, 255, 255, 0.3);
  --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.5) !important;
}

:deep(.el-table th), :deep(.el-table tr) {
  background-color: transparent !important;
}

:deep(.el-table td.el-table__cell), :deep(.el-table th.el-table__cell.is-leaf) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.song-info-cell {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px 0;
}

.cover-wrapper {
  position: relative;
  width: 44px;
  height: 44px;
  margin-right: 15px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.song-cover-mini {
  width: 100%;
  height: 100%;
  display: block;
}

.hover-play {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.2s;
  color: white;
  font-size: 20px;
}

.song-info-cell:hover .hover-play {
  opacity: 1;
}

.song-name {
  font-weight: 500;
  color: #303133;
  font-size: 15px;
}

.song-name.active {
  color: #409eff;
  font-weight: 600;
}

.singer-name, .duration {
  color: #606266;
}

.price {
  color: #f56c6c;
  font-weight: 600;
}

.empty-songs {
  padding: 40px 0;
}

@media (max-width: 768px) {
  .playlist-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 20px;
  }
  
  .playlist-cover {
    width: 180px;
    height: 180px;
  }
  
  .playlist-meta {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .playlist-actions {
    justify-content: center;
  }
  
  .content-wrapper {
    padding: 20px 10px;
  }
}
</style>
