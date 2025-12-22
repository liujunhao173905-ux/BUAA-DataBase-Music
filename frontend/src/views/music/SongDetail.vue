<template>
  <div class="song-detail-page">
    <!-- Dynamic Background -->
    <div class="page-bg" v-if="song" :style="{ backgroundImage: `url(${song.song_cover})` }"></div>
    <div class="page-bg-overlay"></div>

    <div class="content-wrapper">
      <el-card class="song-card" shadow="never" v-loading="loading">
        <template #header>
          <el-page-header @back="handleBack" content="歌曲详情" title="返回" />
        </template>
        <template v-if="song">
          <div class="song-header">
            <div class="cover-container">
              <div class="vinyl-record" :class="{ 'playing': isPlayingThisSong }">
                <div class="vinyl-inner"></div>
              </div>
              <el-image
                :src="song.song_cover || ''"
                fit="cover"
                class="song-cover"
                :class="{ 'playing': isPlayingThisSong }"
              >
                <template #error>
                  <div class="image-slot">暂无封面</div>
                </template>
              </el-image>
            </div>
            
            <div class="song-info">
              <h1 class="song-title">{{ song.song_name }}</h1>
              <div class="song-meta">
                <span class="singer"><el-icon><Microphone /></el-icon> {{ song.song_singer_name }}</span>
                <el-divider direction="vertical" />
                <span><el-icon><Timer /></el-icon> {{ songDurationText }}</span>
              </div>
              
              <div class="tags-row">
                 <el-tag effect="dark" type="warning" v-if="song.song_price > 0" class="price-tag">
                   ¥{{ Number(song.song_price).toFixed(2) }}
                 </el-tag>
                 <el-tag effect="plain" type="info" v-else class="price-tag">免费</el-tag>
                 
                 <div class="stats">
                    <span class="stat-item"><el-icon><Star /></el-icon> {{ song.star_count }} 收藏</span>
                    <span class="stat-item"><el-icon><Goods /></el-icon> {{ song.buy_count }} 购买</span>
                 </div>
              </div>

              <div class="action-buttons">
                <div v-if="song.song_status === 1" class="btn-group">
                  <el-button 
                    type="primary" 
                    size="large"
                    class="play-btn-large"
                    @click="handlePlay"
                    round
                  >
                    <el-icon class="btn-icon">
                      <VideoPlay/>
                    </el-icon>
                    {{ '立即播放' }}
                  </el-button>

                  <el-button
                    :type="song.is_starred ? 'warning' : 'default'"
                    :plain="!song.is_starred"
                    size="large"
                    :loading="starLoading"
                    @click="handleToggleStar"
                    circle
                    class="action-btn-circle"
                  >
                    <el-icon><StarFilled v-if="song.is_starred" /><Star v-else /></el-icon>
                  </el-button>

                  <el-button
                    :type="song.is_bought ? 'success' : 'danger'"
                    :plain="!song.is_bought"
                    size="large"
                    :disabled="song.is_bought"
                    :loading="buyLoading"
                    @click="openBuyDialog"
                    round
                  >
                     <el-icon style="margin-right: 4px"><Money /></el-icon>
                    {{ song.is_bought ? '已购买' : '购买歌曲' }}
                  </el-button>
                  
                  <el-button
                    type="info"
                    plain
                    size="large"
                    :loading="playlistLoading"
                    @click="openPlaylistDialog"
                    circle
                    class="action-btn-circle"
                  >
                    <el-icon><Plus /></el-icon>
                  </el-button>


                <!-- 购买确认弹窗 -->
                <el-dialog
                  v-model="buyDialogVisible"
                  title="确认购买"
                  width="400px"
                  :close-on-click-modal="false"
                >
                  <div v-loading="buyCheckLoading">
                    <p>歌曲：<strong>{{ song?.song_name }}</strong></p>
                    <p>价格：<strong style="color: #f56c6c;">{{ formatPrice(song?.song_price) }}</strong></p>
                    <p>您的余额：<strong>{{ formatPrice(userBalance) }}</strong></p>
                    <p v-if="!canAfford" style="color: #f56c6c; margin-top: 8px;">
                      余额不足，请先充值
                    </p>
                  </div>
                  <template #footer>
                    <el-button @click="buyDialogVisible = false">取消</el-button>
                    <el-button
                      type="primary"
                      :disabled="!canAfford"
                      :loading="buyLoading"
                      @click="confirmBuy"
                    >
                      确认购买
                    </el-button>
                  </template>
                </el-dialog>
              </div>
            </div>

            <!-- <audio
              v-if="song.song_file"
              class="audio-player"
              :src="song.song_file"
              controls
              preload="none"
            /> -->
          </div>
        </div>
      </template>
      <el-empty v-else-if="!loading" description="未找到歌曲" />
    </el-card>
  </div>
  </div>

  <el-dialog
    v-model="playlistDialogVisible"
    title="加入歌单"
    width="500px"
    @opened="fetchUserPlaylists"
  >
    <div v-loading="playlistLoading">
      <el-checkbox-group v-model="selectedPlaylistIds">
        <div v-for="p in userPlaylists" :key="p.playlist_id" class="playlist-item">
          <el-checkbox :label="p.playlist_id">{{ p.playlist_name }}</el-checkbox>
        </div>
      </el-checkbox-group>
    </div>
    <template #footer>
      <el-button @click="playlistDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="confirmJoinPlaylists">确认</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { VideoPlay, VideoPause } from '@element-plus/icons-vue'
import request from '@/api/request'
import { useAuthStore } from '@/stores/auth'
import { usePlayerStore } from '@/stores/player'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const playerStore = usePlayerStore()

const song = ref<any | null>(null)
const loading = ref(false)
const starLoading = ref(false)
const buyLoading = ref(false)

/* ----- 购买确认弹窗相关 ----- */
const buyDialogVisible = ref(false)
const buyCheckLoading = ref(false)   // 查询余额时的 loading
const userBalance = ref(0)           // 用户余额（单位：元）

const playlistDialogVisible = ref(false)
const userPlaylists = ref<any[]>([])
const playlistLoading = ref(false)
const selectedPlaylistIds = ref<number[]>([])   // 当前弹窗内选中项

const initialPlaylistIds = ref<number[]>([])   // 弹窗打开时已含歌曲的列表（用于 diff）

// 打开弹窗 + 加载用户歌单 + 默认选中含当前歌曲的列表
const openPlaylistDialog = () => {
  playlistDialogVisible.value = true
  selectedPlaylistIds.value = []
  initialPlaylistIds.value = []
}

const fetchUserPlaylists = async () => {
  playlistLoading.value = true
  try {
    const res = await request.get('/playlists/my_playlists/')
    userPlaylists.value = res.data.playlists
    // 并行检查每个歌单是否已含当前歌曲
    const checks = await Promise.all(
      userPlaylists.value.map(async p => {
        return request.get(`/playlists/${p.playlist_id}/check_song/?song_id=${song.value.song_id}`)
          .then(r => ({ id: p.playlist_id, in: r.is_in_playlist }))
      })
    )
    checks.filter(i => i.in).forEach(i => initialPlaylistIds.value.push(i.id))
    selectedPlaylistIds.value = [...initialPlaylistIds.value]   // 默认勾选
  } catch (e) {
    ElMessage.error('加载歌单失败')
    console.error('加载歌单失败：', e)
  } finally {
    playlistLoading.value = false
  }
}

// 确认：只发送变化量（新增/删除）
const confirmJoinPlaylists = async () => {
  const init = new Set(initialPlaylistIds.value)
  const curr = new Set(selectedPlaylistIds.value)

  const toAdd = [...curr].filter(id => !init.has(id))   // 新增
  const toDel = [...init].filter(id => !curr.has(id))   // 删除

  try {
    await Promise.all([
      ...toAdd.map(id => request.post(`/playlists/${id}/add_song/`, { song_id: song.value.song_id })),
      ...toDel.map(id => request.delete(`/playlists/${id}/remove_song/`, { data: { song_id: song.value.song_id } }))
    ])
    ElMessage.success('操作成功')
    playlistDialogVisible.value = false
  } catch (e) {
    ElMessage.error('操作失败，请稍后重试')
  }
}

const songDurationText = computed(() => {
  const total = song.value?.song_duration
  if (!total || total <= 0) return '未知'
  const m = Math.floor(total / 60)
  const s = Math.floor(total % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
})

const canAfford = computed(() => {
  return Number(userBalance.value) >= Number(song.value?.song_price || 0)
})

/* 打开弹窗 + 拉取余额 */
const openBuyDialog = async () => {
  if (!song.value) return
  buyDialogVisible.value = true
  buyCheckLoading.value = true
  try {
    const data = await request.get('/users/profile/')
    userBalance.value = Number(data.user_balance || 0)
  } catch (e) {
    ElMessage.error('获取余额失败')
    userBalance.value = 0
  } finally {
    buyCheckLoading.value = false
  }
}

/* 弹窗里点“确认购买”才真正走购买逻辑 */
const confirmBuy = async () => {
  buyLoading.value = true
  try {
    const cost = Number(song.value.song_price)
    // 1. 先调用购买接口
    await request.post(`/music/songs/${song.value.song_id}/buy/`)

    // 2. 本地状态更新
    song.value.is_bought = true
    song.value.buy_count = (song.value.buy_count || 0) + 1
    userBalance.value = Math.max(0, userBalance.value - cost)   // 本地先减
    ElMessage.success('购买成功')

    // 3. 把扣完后的余额同步给后端（partial 更新）
    await request.put('/users/profile/', { user_balance: userBalance.value.toFixed(2) })

    buyDialogVisible.value = false
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || e?.response?.data?.user_balance?.[0] || '购买失败')
  } finally {
    buyLoading.value = false
  }
}

const fetchSongDetail = async () => {
  const songId = route.params.id
  if (!songId) return

  loading.value = true
  try {
    const data = await request.get(`/music/songs/${songId}/`)
    song.value = data
  } catch (error) {
    ElMessage.error('加载歌曲详情失败')
  } finally {
    loading.value = false
  }
}

// const fetchPlaylists = async () => {
//   playListsLoading.value = true
//   try {
//     const response = await request.get('/music/songs/bought/')
//     playLists.value = response
//   } catch (error) {
//     ElMessage.error('加载歌单列表失败')
//     console.error('Failed to fetch playlists:', error)
//   } finally {
//     playListsLoading.value = false
//   }
// }

const isPlayingThisSong = computed(() => {
  return playerStore.currentSong?.song_id === song.value?.song_id && playerStore.isPlaying
})

const handlePlay = () => {
  if (song.value) {
    playerStore.setPlaylist([song.value])
    playerStore.playSong(song.value)
  }
}

const ensureLoggedIn = () => {
  if (authStore.isAuthenticated) return true
  ElMessage.warning('请先登录后再操作')
  router.push({ name: 'Login', query: { redirect: route.fullPath } })
  return false
}

const handleToggleStar = async () => {
  if (!song.value || !ensureLoggedIn()) return
  starLoading.value = true
  try {
    if (song.value.is_starred) {
      await request.delete(`/music/songs/${song.value.song_id}/unstar/`)
      song.value.is_starred = false
      song.value.star_count = Math.max(0, (song.value.star_count || 1) - 1)
      ElMessage.success('已取消收藏')
    } else {
      await request.post(`/music/songs/${song.value.song_id}/star/`)
      song.value.is_starred = true
      song.value.star_count = (song.value.star_count || 0) + 1
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试')
  } finally {
    starLoading.value = false
  }
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

const handleBack = () => {
  router.back()
}

watch(
  () => route.params.id,
  () => fetchSongDetail(),
  { immediate: true }
)
</script>

<style scoped>
.song-detail-page {
  position: relative;
  min-height: 100vh;
  padding: 40px 24px;
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
  background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.6));
  z-index: 1;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  max-width: 1000px;
  margin: 0 auto;
}

.song-card {
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 24px;
  overflow: visible;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.song-header {
  display: flex;
  gap: 60px;
  padding: 20px;
  align-items: center;
}

.cover-container {
  position: relative;
  width: 260px;
  height: 260px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.vinyl-record {
  position: absolute;
  top: 0;
  right: -40px;
  width: 240px;
  height: 240px;
  background: #111;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.5s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.vinyl-record.playing {
  animation: spin 8s linear infinite;
}

.vinyl-inner {
  width: 80px;
  height: 80px;
  background: #333;
  border-radius: 50%;
  border: 2px solid #555;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.song-cover {
  position: relative;
  width: 260px;
  height: 260px;
  border-radius: 12px;
  box-shadow: 0 12px 24px rgba(0,0,0,0.2);
  z-index: 2;
  transition: transform 0.3s;
}

.song-cover:hover {
  transform: scale(1.02);
}

.song-info {
  flex: 1;
  min-width: 300px;
}

.song-title {
  font-size: 36px;
  font-weight: 800;
  color: #1a1a1a;
  margin: 0 0 16px 0;
  line-height: 1.2;
}

.song-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #606266;
  font-size: 16px;
  margin-bottom: 24px;
}

.singer {
  color: #409eff;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

.tags-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
}

.price-tag {
  font-size: 16px;
  padding: 8px 16px;
  height: auto;
}

.stats {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 14px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.action-buttons {
  margin-top: 20px;
}

.btn-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.play-btn-large {
  padding: 12px 32px;
  font-weight: 600;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}

.play-btn-large:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.5);
}

.action-btn-circle {
  font-size: 18px;
}

.image-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: #f5f7fa;
  color: #909399;
}

/* Responsive */
@media (max-width: 768px) {
  .song-header {
    flex-direction: column;
    text-align: center;
    gap: 30px;
  }
  
  .vinyl-record {
    display: none; /* Hide vinyl on mobile to save space */
  }
  
  .song-meta, .tags-row, .btn-group {
    justify-content: center;
  }
  
  .song-title {
    font-size: 28px;
  }
}
</style>


