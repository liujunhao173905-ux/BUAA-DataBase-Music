<template>
  <div class="song-list-page">
    <el-card class="filter-card" shadow="never">
      <template #header>
        <el-page-header @back="handleBack" content="发现音乐" title="返回" />
      </template>
      <div class="filter-row">
        <el-input
          v-model="filters.search"
          :placeholder="getSearchPlaceholder()"
          clearable
          @keyup.enter="handleFilterSubmit"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select
          v-model="filters.searchType"
          placeholder="选择搜索类型"
          style="width: 150px"
        >
          <el-option label="歌曲" value="song" />
          <el-option label="歌单" value="playlist" />
          <el-option label="歌手" value="singer" />
        </el-select>
        <div v-if="filters.searchType === 'song'" class="price-filters">
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
        </div>
        <div class="filter-actions">
          <el-button type="primary" @click="handleFilterSubmit">搜索</el-button>
          <el-button @click="handleFilterReset">重置</el-button>
        </div>
      </div>
    </el-card>

    <el-skeleton v-if="loading" :rows="6" animated />

    <div v-else>
      <div v-if="songs.length" class="songs-grid">
        <el-card 
          v-for="item in songs"
          :key="getItemKey(item)"
          class="song-card" 
          :body-style="{ padding: '0px' }"
          @click="handleSongClick(item)"
        >
          <div class="cover-container">
            <el-image
              :src="getItemCover(item) || ''"
              fit="cover"
              class="song-cover"
            >
              <template #error>
                <div class="image-slot">暂无封面</div>
              </template>
            </el-image>
            <div 
              v-if="filters.searchType === 'song'" 
              class="play-overlay"
              @click.stop="handlePlay(item)"
            >
              <el-icon><VideoPlay /></el-icon>
            </div>
          </div>
          <div class="song-info">
            <h3>{{ getItemName(item) }}</h3>
            <p>{{ getItemCreator(item) }}</p>
            <span v-if="filters.searchType === 'song'" class="price">{{ formatPrice(getItemPrice(item)) }}</span>
            <span v-else-if="filters.searchType === 'playlist'" class="song-count">{{ item.song_count }}首歌曲</span>
            <span v-else-if="filters.searchType === 'singer'" class="tag">{{ item.user_type_display }}</span>
          </div>
        </el-card>
      </div>
      
      <el-empty v-else :description="`暂无${getSearchTypeText()}`" />

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
import { ArrowLeft, VideoPlay, Search } from '@element-plus/icons-vue'
import request from '@/api/request'
import { usePlayerStore } from '@/stores/player'

const route = useRoute()
const router = useRouter()
const playerStore = usePlayerStore()

const loading = ref(false)
const songs = ref<any[]>([])

const pagination = reactive({
  page: Number(route.query.page) || 1,
  pageSize: 12,
  total: 0,
})

const filters = reactive<{
  search: string
  searchType: string
  priceMin: number | null
  priceMax: number | null
}>({
  search: String(route.query.search || ''),
  searchType: String(route.query.searchType || 'song'),
  priceMin: route.query.price_min ? Number(route.query.price_min) : null,
  priceMax: route.query.price_max ? Number(route.query.price_max) : null,
})

const syncFiltersFromQuery = () => {
  filters.search = String(route.query.search || '')
  filters.searchType = String(route.query.searchType || 'song')
  filters.priceMin = route.query.price_min ? Number(route.query.price_min) : null
  filters.priceMax = route.query.price_max ? Number(route.query.price_max) : null
  pagination.page = Number(route.query.page) || 1
}

const fetchSongs = async (page = pagination.page) => {
  loading.value = true
  try {
    if (filters.searchType === 'song') {
      const params: Record<string, string | number> = {
        page,
        page_size: pagination.pageSize,
      }
      if (filters.search) params.search = filters.search
      if (filters.priceMin !== null) params.price_min = filters.priceMin
      if (filters.priceMax !== null) params.price_max = filters.priceMax

      const response = await request.get('/music/songs/', { params })
      const responseData = response as { results?: any[], count?: number }
      songs.value = responseData.results || []
      pagination.total = responseData.count || songs.value.length
    } else if (filters.searchType === 'playlist') {
      const params: Record<string, string | number> = {
        page,
        page_size: pagination.pageSize
      }
      if (filters.search) params.search = filters.search

      const response = await request.get('/playlists/', { params })
      const responseData = response as { data?: { playlists?: any[], total?: number } }
      songs.value = responseData.data?.playlists || []
      pagination.total = responseData.data?.total || 0
    } else if (filters.searchType === 'singer') {
      if (filters.search) {
        const params: Record<string, string | number> = {
          page,
          page_size: pagination.pageSize,
          search: filters.search
        }

        const response = await request.get('/users/singers/', { params })
        const responseData = response as { results?: any[], count?: number }
        songs.value = responseData.results || []
        pagination.total = responseData.count || songs.value.length
      } else {
        songs.value = []
        pagination.total = 0
      }
    }
    pagination.page = page
  } catch (error) {
    ElMessage.error(`加载${getSearchTypeText()}列表失败`)
  } finally {
    loading.value = false
  }
}

const handleFilterSubmit = () => {
  const query: Record<string, string> = {}
  if (filters.search) query.search = filters.search
  query.searchType = filters.searchType
  if (filters.searchType === 'song' && filters.priceMin !== null) query.price_min = String(filters.priceMin)
  if (filters.searchType === 'song' && filters.priceMax !== null) query.price_max = String(filters.priceMax)
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

const handleBack = () => {
  router.push('/home')
}

const handlePlay = (item: any) => {
  if (item.song_id) {
    playerStore.setPlaylist(songs.value)
    playerStore.playSong(item)
  }
}

const handleSongClick = (item: any) => {
  if (filters.searchType === 'song') {
    if (item.song_id) {
      router.push({ name: 'SongDetail', params: { id: String(item.song_id) } })
    }
  } else if (filters.searchType === 'playlist') {
    const id = item.playlist_id
    if (id) {
      router.push({ name: 'PlaylistDetail', params: { id: String(id) } })
    }
  } else if (filters.searchType === 'singer') {
    const id = item.user_id
    if (id) {
      router.push({ name: 'UserDetail', params: { id: String(id) } })
    }
  }
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

const getSearchPlaceholder = () => {
  if (filters.searchType === 'song') return '搜索歌曲'
  if (filters.searchType === 'playlist') return '搜索歌单'
  if (filters.searchType === 'singer') return '搜索歌手'
  return '搜索内容'
}

const getSearchTypeText = () => {
  if (filters.searchType === 'song') return '歌曲'
  if (filters.searchType === 'playlist') return '歌单'
  if (filters.searchType === 'singer') return '歌手'
  return '内容'
}

const getItemKey = (item: any) => {
  if (filters.searchType === 'song') return item.song_id
  if (filters.searchType === 'playlist') return item.playlist_id
  if (filters.searchType === 'singer') return item.user_id
  return null
}

const getItemCover = (item: any) => {
  if (filters.searchType === 'song') return item.song_cover
  if (filters.searchType === 'playlist') return item.playlist_cover
  if (filters.searchType === 'singer') return item.user_avatar
  return null
}

const getItemName = (item: any) => {
  if (filters.searchType === 'song') return item.song_name
  if (filters.searchType === 'playlist') return item.playlist_name
  if (filters.searchType === 'singer') return item.user_name
  return ''
}

const getItemCreator = (item: any) => {
  if (filters.searchType === 'song') return item.song_singer_name
  if (filters.searchType === 'playlist') return item.playlist_creator_name
  if (filters.searchType === 'singer') return `粉丝: ${item.followers_count}`
  return ''
}

const getItemPrice = (item: any) => {
  if (filters.searchType === 'song') return item.song_price
  return null
}

watch(
  () => route.query,
  () => {
    syncFiltersFromQuery()
    fetchSongs(pagination.page)
  },
  { immediate: true }
)

watch(
  () => filters.searchType,
  (newType, oldType) => {
    if (newType !== oldType) {
      pagination.page = 1
      fetchSongs(1)
      const query = { ...route.query, searchType: newType, page: '1' }
      router.push({ name: 'SongList', query })
    }
  }
)
</script>

<style scoped>
.song-list-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.filter-card {
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.price-filters {
  display: flex;
  gap: 12px;
}

.filter-actions {
  display: flex;
  gap: 10px;
}

/* 核心布局：Grid */
.songs-grid {
  display: grid;
  /* 220px 是卡片的最小宽度。
    如果一行能放得下更多，它会自动计算数量。
    1fr 表示剩余空间会被卡片平分，实现两端对齐。
  */
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 30px; /* 卡片之间的间距 */
  justify-content: space-between;
}

/* 卡片样式 */
.song-card {
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  
  /* 宽度设为 100% 以填满 Grid 分配的单元格 */
  width: 100%;
}

.song-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

/* 封面容器：实现 1:1 正方形比例 */
.cover-container {
  position: relative;
  width: 100%;
  padding-top: 100%; /* 宽高比 1:1 */
  height: 0;         /* 高度由 padding 撑开 */
}

/* 封面图片：绝对定位以适应容器 */
.song-cover {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* 播放遮罩 */
.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: white;
  font-size: 48px;
  backdrop-filter: blur(2px);
}

.song-card:hover .play-overlay {
  opacity: 1;
}

/* 图片加载失败占位 */
.image-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  color: #909399;
  position: absolute;
  top: 0;
  left: 0;
}

.song-info {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.song-info h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #303133;
}

.song-info p {
  margin: 0;
  color: #909399;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.price {
  color: #f56c6c;
  font-weight: bold;
}

.song-count {
  color: #409eff;
  font-size: 13px;
}

.tag {
  display: inline-block;
  background-color: #f0f9eb;
  color: #67c23a;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  max-width: fit-content;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 40px;
  margin-bottom: 20px;
}
</style>