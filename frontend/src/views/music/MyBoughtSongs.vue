<template>
  <div class="my-bought-songs-container">
    <el-card class="my-bought-songs-card" :class="{ 'no-border': isEmbedded }">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;" v-if="!isEmbedded">
            <el-button type="default" @click="handleBack" circle>
              <el-icon><ArrowLeft /></el-icon>
            </el-button>
            <h2>我的购买</h2>
          </div>
          <div v-else></div> <!-- Spacer -->
          
          <el-button type="primary" round @click="handlePlayAll" :disabled="songs.length === 0">
            <el-icon class="el-icon--left"><VideoPlay /></el-icon> 播放全部
          </el-button>
        </div>
      </template>
      
      <div class="song-card" v-loading="loading">
        <div v-if="songs.length > 0" class="song-list">
          <el-table :data="songs" stripe style="width: 100%" @row-dblclick="handlePlay">
            <el-table-column type="index" width="50" />
            <el-table-column prop="song_name" label="歌曲名称" min-width="200">
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
            <el-table-column prop="song_singer_name" label="歌手" width="150" />
            <el-table-column prop="song_duration" label="时长" width="100">
               <template #default="scope">
                  {{ formatDuration(scope.row.song_duration) }}
               </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
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
import { getMyBoughtSongs, type Song } from '@/api/music'
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

const handleDownload = (song: Song) => {
  if (song.song_file) {
    window.open(song.song_file, '_blank')
  } else {
    ElMessage.warning('暂无下载链接')
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
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.my-bought-songs-card.no-border {
  border: none;
  box-shadow: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.song-info {
  display: flex;
  align-items: center;
}

.cover-wrapper {
  position: relative;
  width: 40px;
  height: 40px;
  margin-right: 10px;
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
}

.song-cover {
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.2s;
  color: white;
}

.song-info:hover .hover-play {
  opacity: 1;
}

.song-name {
  font-weight: 500;
  color: #303133;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
