<template>
  <div class="song-list-page">
    <el-card class="filter-card">
      <div class="filter-row">
        <el-button type="default" @click="handleBack" style="margin-right: 10px;">
          <el-icon><ArrowLeft /></el-icon> 返回
        </el-button>
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
      <el-row v-if="songs.length" :gutter="20">
        <el-col
          v-for="item in songs"
          :key="getItemKey(item)"
          :xs="12"
          :sm="8"
          :md="6"
          :lg="4"
        >
          <el-card class="song-card" @click="handleSongClick(item)">
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
        </el-col>
      </el-row>

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
      // 搜索歌曲
      const params: Record<string, string | number> = {
        page,
        page_size: pagination.pageSize,
      }
      if (filters.search) params.search = filters.search
      if (filters.priceMin !== null) params.price_min = filters.priceMin
      if (filters.priceMax !== null) params.price_max = filters.priceMax

      const response = await request.get('/music/songs/', { params })
      // 使用类型断言来处理API响应
      const responseData = response as { results?: any[], count?: number }
      // 直接使用后端返回的数据格式
      songs.value = responseData.results || []
      pagination.total = responseData.count || songs.value.length
    } else if (filters.searchType === 'playlist') {
      // 搜索歌单 - 仅在有搜索关键词时才请求
      if (filters.search) {
        const params: Record<string, string | number> = {
          page,
          page_size: pagination.pageSize,
          search: filters.search
        }

        const response = await request.get('/playlists/', { params })
        // 使用类型断言来处理API响应
        const responseData = response as { data?: { playlists?: any[], total?: number } }
        // 直接使用后端返回的数据格式
        songs.value = responseData.data?.playlists || []
        pagination.total = responseData.data?.total || songs.value.length
      } else {
        // 没有搜索关键词时，不显示歌单
        songs.value = []
        pagination.total = 0
      }
    } else if (filters.searchType === 'singer') {
      // 搜索歌手 - 仅在有搜索关键词时才请求
      if (filters.search) {
        const params: Record<string, string | number> = {
          page,
          page_size: pagination.pageSize,
          search: filters.search
        }

        const response = await request.get('/users/singers/', { params })
        // 使用类型断言来处理API响应
        const responseData = response as { results?: any[], count?: number }
        // 直接使用后端返回的数据格式
        songs.value = responseData.results || []
        pagination.total = responseData.count || songs.value.length
      } else {
        // 没有搜索关键词时，不显示歌手
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
  router.back()
}

const handlePlay = (item: any) => {
  if (item.song_id) {
    playerStore.setPlaylist(songs.value)
    playerStore.playSong(item)
  }
}

const handleSongClick = (item: any) => {
  if (filters.searchType === 'song') {
    // Go to detail
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
  // 检查price是否为有效数字
  const priceNum = Number(price)
  if (!price || isNaN(priceNum)) return '免费'
  return `¥${priceNum.toFixed(2)}`
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

const getItemId = (item: any) => {
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

// 监听搜索类型变化，确保切换标签时重新加载数据
watch(
  () => filters.searchType,
  (newType, oldType) => {
    // 只有当搜索类型真正变化时才重新加载数据
    if (newType !== oldType) {
      // 重置页码到第一页
      pagination.page = 1
      // 如果有搜索关键词，重新搜索对应类型的数据
      fetchSongs(1)
      // 更新路由参数，保持搜索状态同步
      const query = { ...route.query, searchType: newType, page: '1' }
      router.push({ name: 'SongList', query })
    }
  }
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

.price-filters {
  display: flex;
  gap: 12px;
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

.cover-container {
  position: relative;
  width: 100%;
  height: 200px;
}

.song-cover {
  width: 100%;
  height: 100%;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: white;
  font-size: 40px;
  backdrop-filter: blur(2px);
}

.song-card:hover .play-overlay {
  opacity: 1;
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

.song-count {
  color: #409eff;
}

.tag {
  color: #67c23a;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>



