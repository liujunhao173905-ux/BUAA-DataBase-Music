<template>
  <div class="my-starred-songs-container">
    <el-card class="starred-songs-card" :class="{ 'no-border': isEmbedded }">
      <template #header>
        <el-page-header v-if="!isEmbedded" @back="handleBack" content="我的收藏" title="返回">
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
          <el-table :data="songs" stripe style="width: 100%" @row-dblclick="handleSongClick">
            <el-table-column type="index" width="50" />
            <el-table-column prop="song_name" label="歌曲名称" min-width="200">
              <template #default="scope">
                <div class="song-info" @click="handleSongClick(scope.row)" style="cursor: pointer;">
                  <div class="cover-wrapper">
                    <el-image v-if="scope.row.song_cover" :src="scope.row.song_cover" class="song-cover" fit="cover" />
                    <div class="hover-play"><el-icon><VideoPlay /></el-icon></div>
                  </div>
                  <span class="song-name">{{ scope.row.song_name }}</span>
                  <el-tag size="small" type="danger" v-if="scope.row.song_price > 0 && !scope.row.is_bought" effect="plain" style="margin-left: 8px">VIP</el-tag>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="song_singer_name" label="歌手" width="150" />
            <el-table-column prop="song_duration" label="时长" width="100">
               <template #default="scope">
                  {{ formatDuration(scope.row.song_duration) }}
               </template>
            </el-table-column>
            <el-table-column prop="song_price" label="价格" width="100">
              <template #default="scope">
                {{ formatPrice(scope.row.song_price) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="220" fixed="right">
              <template #default="scope">
                <el-button
                  type="primary"
                  size="small"
                  @click.stop="handleDetail(scope.row)"
                  plain>详情</el-button>
                <el-button
                  type="primary"
                  size="small"
                  :disabled="scope.row.is_bought"
                  @click.stop="handleBuySong(scope.row)"
                  :icon="ShoppingCart"
                  plain
                >
                  {{ scope.row.is_bought ? '已购买' : '购买' }}
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  @click.stop="handleRemoveStar(scope.row)"
                  :icon="Delete"
                  circle
                >
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
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
        </div>
        
        <el-empty v-else description="暂无收藏歌曲" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, VideoPlay, ShoppingCart, Delete } from '@element-plus/icons-vue'
import { getMyStarredSongs, unstarSong, buySong, type Song } from '@/api/music'
import { usePlayerStore } from '@/stores/player'

const props = defineProps<{
  isEmbedded?: boolean
}>()

const router = useRouter()
const playerStore = usePlayerStore()

const songs = ref<Song[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

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

const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const fetchStarredSongs = async () => {
  loading.value = true
  try {
    const response = await getMyStarredSongs(currentPage.value, pageSize.value)
    songs.value = response.data.songs
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('加载收藏歌曲失败')
    console.error('Failed to fetch starred songs:', error)
  } finally {
    loading.value = false
  }
}

// 查看歌曲详情
const handleDetail = (song: Song) => {
  router.push(`/songs/${song.song_id}`)
}

const handleSongClick = (song: Song) => {
  playerStore.setPlaylist(songs.value)
  playerStore.playSong(song)
}

const handlePlayAll = () => {
  if (songs.value.length > 0) {
    playerStore.setPlaylist(songs.value)
    playerStore.playSong(songs.value[0])
  }
}

const handleBuySong = async (song: Song) => {
  try {
    await buySong(song.song_id)
    song.is_bought = true
    ElMessage.success('购买成功')
  } catch (error: any) {
    const errorMessage = error.response?.data?.error || '购买失败'
    ElMessage.error(errorMessage)
  }
}

const handleRemoveStar = async (song: Song) => {
  try {
    await unstarSong(song.song_id)
    ElMessage.success('取消收藏成功')
    // Refresh list to keep pagination correct
    if (songs.value.length === 1 && currentPage.value > 1) {
      currentPage.value--
    }
    fetchStarredSongs()
  } catch (error) {
    ElMessage.error('取消收藏失败')
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchStarredSongs()
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
  fetchStarredSongs()
}

const handleBack = () => {
  router.back()
}

onMounted(() => {
  fetchStarredSongs()
})
</script>

<style scoped>
.my-starred-songs-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.starred-songs-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

.starred-songs-card.no-border {
  border: none;
  box-shadow: none;
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
