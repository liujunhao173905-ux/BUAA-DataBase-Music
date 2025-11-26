<template>
  <div class="song-list-page">
    <el-card class="filter-card">
      <div class="filter-row">
        <el-input
          v-model="filters.search"
          placeholder="搜索歌曲或歌手"
          clearable
          @keyup.enter="handleFilterSubmit"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-input-number
          v-model="filters.priceMin"
          :min="0"
          :max="filters.priceMax ?? undefined"
          :controls="false"
          placeholder="最低价格"
        />
        <el-input-number
          v-model="filters.priceMax"
          :min="filters.priceMin ?? 0"
          :controls="false"
          placeholder="最高价格"
        />
        <div class="filter-actions">
          <el-button type="primary" @click="handleFilterSubmit">搜索</el-button>
          <el-button @click="handleFilterReset">重置</el-button>
        </div>
      </div>
    </el-card>

    <el-skeleton v-if="loading" :rows="6" animated />

    <div v-else>
      <el-row v-if="songs.length" :gutter="20">
        <el-col
          v-for="song in songs"
          :key="song.song_id"
          :xs="12"
          :sm="8"
          :md="6"
          :lg="4"
        >
          <el-card class="song-card" @click="handleSongClick(song.song_id)">
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
              <h3>{{ song.song_name }}</h3>
              <p>{{ song.song_singer_name }}</p>
              <span class="price">{{ formatPrice(song.song_price) }}</span>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-empty v-else description="暂无歌曲" />

      <div
        v-if="songs.length && pagination.total > pagination.pageSize"
        class="pagination-wrapper"
      >
        <el-pagination
          :total="pagination.total"
          :current-page="pagination.page"
          :page-size="pagination.pageSize"
          layout="prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import request from '@/api/request'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const songs = ref<any[]>([])

const pagination = reactive({
  page: Number(route.query.page) || 1,
  pageSize: 12,
  total: 0,
})

const filters = reactive<{
  search: string
  priceMin: number | null
  priceMax: number | null
}>({
  search: String(route.query.search || ''),
  priceMin: route.query.price_min ? Number(route.query.price_min) : null,
  priceMax: route.query.price_max ? Number(route.query.price_max) : null,
})

const syncFiltersFromQuery = () => {
  filters.search = String(route.query.search || '')
  filters.priceMin = route.query.price_min ? Number(route.query.price_min) : null
  filters.priceMax = route.query.price_max ? Number(route.query.price_max) : null
  pagination.page = Number(route.query.page) || 1
}

const fetchSongs = async (page = pagination.page) => {
  loading.value = true
  try {
    const params: Record<string, string | number> = {
      page,
      page_size: pagination.pageSize,
    }
    if (filters.search) params.search = filters.search
    if (filters.priceMin !== null) params.price_min = filters.priceMin
    if (filters.priceMax !== null) params.price_max = filters.priceMax

    const response = await request.get('/music/songs/', { params })
    if (Array.isArray(response)) {
      songs.value = response
      pagination.total = response.length
    } else {
      songs.value = response.results || []
      pagination.total = response.count || songs.value.length
    }
    pagination.page = page
  } catch (error) {
    ElMessage.error('加载歌曲列表失败')
  } finally {
    loading.value = false
  }
}

const handleFilterSubmit = () => {
  const query: Record<string, string> = {}
  if (filters.search) query.search = filters.search
  if (filters.priceMin !== null) query.price_min = String(filters.priceMin)
  if (filters.priceMax !== null) query.price_max = String(filters.priceMax)
  query.page = '1'
  router.push({ name: 'SongList', query })
}

const handleFilterReset = () => {
  filters.search = ''
  filters.priceMin = null
  filters.priceMax = null
  router.push({ name: 'SongList' })
}

const handlePageChange = (page: number) => {
  const query = { ...route.query, page: String(page) }
  router.push({ name: 'SongList', query })
}

const handleSongClick = (songId: number) => {
  router.push({ name: 'SongDetail', params: { id: String(songId) } })
}

const formatPrice = (price: number) => {
  if (!price) return '免费'
  return `¥${price.toFixed(2)}`
}

watch(
  () => route.query,
  () => {
    syncFiltersFromQuery()
    fetchSongs(pagination.page)
  },
  { immediate: true }
)
</script>

<style scoped>
.song-list-page {
  padding: 24px;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.filter-actions {
  display: flex;
  gap: 10px;
}

.song-card {
  cursor: pointer;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.song-card:hover {
  transform: translateY(-4px);
}

.song-cover {
  width: 100%;
  height: 200px;
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
  padding: 12px 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.song-info h3 {
  margin: 0;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-info p {
  margin: 0;
  color: #909399;
}

.price {
  color: #f56c6c;
  font-weight: bold;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>


