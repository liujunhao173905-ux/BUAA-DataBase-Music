<template>
  <div class="song-detail-page">
    <el-page-header content="歌曲详情" @back="handleBack" />

    <el-card class="song-card" v-loading="loading">
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
            <p>时长：{{ song.song_duration || '未知' }}</p>
            <p>价格：{{ formatPrice(song.song_price) }}</p>
            <p>收藏：{{ song.star_count }} 次 · 购买：{{ song.buy_count }} 次</p>

            <div class="action-buttons">
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
                @click="handleBuySong"
              >
                {{ song.is_bought ? '已购买' : buyButtonText }}
              </el-button>
            </div>

            <audio
              v-if="song.song_file"
              class="audio-player"
              :src="song.song_file"
              controls
              preload="none"
            />
          </div>
        </div>
      </template>
      <el-empty v-else-if="!loading" description="未找到歌曲" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/api/request'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const song = ref<any | null>(null)
const loading = ref(false)
const starLoading = ref(false)
const buyLoading = ref(false)

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
</style>


