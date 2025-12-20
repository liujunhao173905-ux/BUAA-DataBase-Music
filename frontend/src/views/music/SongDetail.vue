<template>
  <div class="song-detail-page">
    <el-card class="song-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-button type="default" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <h2>歌曲详情</h2>
          </div>
        </div>
      </template>
      <template v-if="song">
        <div class="song-content">
          <el-image
            :src="song.song_cover || ''"
            fit="cover"
            class="song-cover"
          >
            <template #error>
              <div class="image-slot">暂无封面</div>
            </template>
          </el-image>
          <div class="song-info">
            <h2>{{ song.song_name }}</h2>
            <p class="singer">歌手：{{ song.song_singer_name }}</p>
            <p>时长：{{ songDurationText }}</p>
            <p>价格：{{ formatPrice(song.song_price) }}</p>
            <p>收藏：{{ song.star_count }} 次 · 购买：{{ song.buy_count }} 次</p>

            <div class="action-buttons">
              <div v-if="song.song_status === 1">
                <el-button 
                  type="primary" 
                  size="large"
                  @click="handlePlay"
                >
                  <el-icon style="margin-right: 4px">
                    <VideoPause v-if="isPlayingThisSong" />
                    <VideoPlay v-else />
                  </el-icon>
                  {{ isPlayingThisSong ? '暂停播放' : '立即播放' }}
                </el-button>

                <el-button
                  type="warning"
                  :loading="starLoading"
                  @click="handleToggleStar"
                >
                  {{ song.is_starred ? '取消收藏' : '收藏歌曲' }}
                </el-button>
                <el-button
                  type="primary"
                  :disabled="song.is_bought"
                  :loading="buyLoading"
                  @click="openBuyDialog"
                >
                  {{ song.is_bought ? '已购买' : buyButtonText }}
                </el-button>
                <el-button
                  type="info"
                  :loading="playlistLoading"
                  @click="openPlaylistDialog"
                >
                  {{ '加入歌单' }}
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
import { ArrowLeft, VideoPlay, VideoPause } from '@element-plus/icons-vue'
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

const playLists = ref<any[]>([])
const playListsLoading = ref(false)

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

const buyButtonText = computed(() => {
  if (!song.value) return '购买'
  const price = Number(song.value.song_price)
  return !isNaN(price) && price > 0 ? `购买 - ¥${price.toFixed(2)}` : '购买'
})

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

const handleBuySong = async () => {
  if (!song.value || song.value.is_bought || !ensureLoggedIn()) return
  buyLoading.value = true
  try {
    await request.post(`/music/songs/${song.value.song_id}/buy/`)
    song.value.is_bought = true
    song.value.buy_count = (song.value.buy_count || 0) + 1
    ElMessage.success('购买成功')
  } catch (error) {
    ElMessage.error('购买失败，请稍后再试')
  } finally {
    buyLoading.value = false
  }
}

const formatPrice = (price: any) => {
  const numPrice = Number(price)
  if (!price || isNaN(numPrice)) return '免费'
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
  padding: 24px;
}

.song-card {
  margin-top: 16px;
}

.song-content {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.song-cover {
  width: 320px;
  height: 320px;
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

.song-info {
  flex: 1;
  min-width: 280px;
}

.song-info h2 {
  margin: 0 0 10px 0;
}

.singer {
  font-weight: bold;
}

.action-buttons {
  margin: 20px 0;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.audio-player {
  width: 100%;
  margin-top: 20px;
}

.playlist-item {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}
.playlist-item:last-child {
  border-bottom: none;
}
</style>


