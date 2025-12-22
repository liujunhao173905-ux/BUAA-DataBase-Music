<template>
  <div class="my-bought-songs-container">
    <el-card class="my-bought-songs-card" :class="{ 'no-border': isEmbedded }">
      <template #header>
        <el-page-header v-if="!isEmbedded" @back="handleBack" content="我的购买" title="返回">
          <template #extra>
            <el-button type="primary" round @click="handlePlayAll" :disabled="songs.length === 0">
              <el-icon class="el-icon--left"><VideoPlay /></el-icon> 播放全部
            </el-button>
          </template>
        </el-page-header>
        <div v-else class="card-header" style="display: flex; justify-content: flex-end;">
          <el-button type="primary" round @click="handlePlayAll" :disabled="songs.length === 0">
            <el-icon class="el-icon--left"><VideoPlay /></el-icon> 播放全部
          </el-button>
        </div>
      </template>
      
      <div class="song-card" v-loading="loading">
        <div v-if="songs.length > 0" class="song-list">
          <el-table :data="songs" stripe style="width: 100%" @row-dblclick="handlePlay">
            <el-table-column type="index" width="50" />
            <el-table-column prop="song_name" label="歌曲名称" min-width="200" align="center">
              <template #default="scope">
                <div class="song-info" @click="handlePlay(scope.row)" style="cursor: pointer;">
                  <div class="cover-wrapper">
                    <el-image v-if="scope.row.song_cover" :src="scope.row.song_cover" class="song-cover" fit="cover" />
                    <div class="hover-play"><el-icon><VideoPlay /></el-icon></div>
                  </div>
                  <span class="song-name">{{ scope.row.song_name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="song_singer_name" label="歌手" width="150" align="center" />
            <el-table-column prop="song_duration" label="时长" width="100" align="center">
               <template #default="scope">
                  {{ formatDuration(scope.row.song_duration) }}
               </template>
            </el-table-column>
            <el-table-column label="当前价格" width="110" align="center">
              <template #default="scope">
                {{ formatPrice(scope.row.song_price) }}
              </template>
            </el-table-column>
            <el-table-column label="购买价格" width="110" align="center">
              <template #default="scope">
                {{ formatPrice(scope.row.bought_price) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right" align="center">
              <template #default="scope">
                <el-button type="primary" size="small" @click.stop="handlePlay(scope.row)" :icon="VideoPlay" plain>播放</el-button>
                <el-button type="success" size="small" @click.stop="handleDownload(scope.row)" :icon="Download" plain>下载</el-button>
              </template>
            </el-table-column>
          </el-table>

        </div>
      </div>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, VideoPlay, Download } from '@element-plus/icons-vue'
import { downloadSong, getMyBoughtSongs, type Song } from '@/api/music'
import { usePlayerStore } from '@/stores/player'

const props = defineProps<{
  isEmbedded?: boolean
}>()

const router = useRouter()
const playerStore = usePlayerStore()

const songs = ref<Song[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const fetchSongs = async () => {
  try {
    loading.value = true
    const response = await getMyBoughtSongs(currentPage.value, pageSize.value)
    songs.value = response.data.songs
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('获取已购买歌曲失败')
    console.error('获取已购买歌曲失败:', error)
  } finally {
    loading.value = false
  }
}

const handlePlay = (song: Song) => {
  playerStore.setPlaylist(songs.value)
  playerStore.playSong(song)
}

const handlePlayAll = () => {
  if (songs.value.length > 0) {
    playerStore.setPlaylist(songs.value)
    playerStore.playSong(songs.value[0])
  }
}

const handleDownload = async (song: Song) => {
  try {
    const res = await downloadSong(song)
    // res is Blob
    const blob = new Blob([res as any], { 
      type: 'mp3'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${song.song_name}.mp3`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('下载成功')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchSongs()
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
  fetchSongs()
}

const handleBack = () => {
  router.back()
}

const formatPrice = (price: any) => {
  const numPrice = Number(price)
  console.log('price: ', numPrice)
  if (price === null || price === undefined || isNaN(numPrice)) {
    return '免费'
  }
  if (numPrice <= 0) {
    return '免费'
  }
  return `¥${numPrice.toFixed(2)}`
}

onMounted(() => {
  fetchSongs()
})
</script>

<style scoped>
.my-bought-songs-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.my-bought-songs-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

.my-bought-songs-card.no-border {
  border: none;
  background: transparent;
}

:deep(.el-table) {
  background-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(255, 255, 255, 0.5);
  --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.5);
}

:deep(.el-table th.el-table__cell) {
  background-color: rgba(255, 255, 255, 0.5);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.song-info {
  display: flex;
  align-items: center;
  padding: 4px 0;
  transition: transform 0.2s;
}

.song-info:hover {
  transform: translateX(4px);
}

.cover-wrapper {
  position: relative;
  width: 48px;
  height: 48px;
  margin-right: 16px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.song-cover {
  width: 100%;
  height: 100%;
  display: block;
  transition: transform 0.3s;
}

.cover-wrapper:hover .song-cover {
  transform: scale(1.1);
}

.hover-play {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: #fff;
  font-size: 24px;
}

.cover-wrapper:hover .hover-play {
  opacity: 1;
}

.song-name {
  font-weight: 600;
  color: #303133;
  font-size: 15px;
}

.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>
