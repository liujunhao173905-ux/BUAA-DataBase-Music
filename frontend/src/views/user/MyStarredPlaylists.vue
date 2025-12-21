<template>
  <div class="my-starred-playlists">
    <el-card class="starred-card" :class="{ 'no-border': isEmbedded }" shadow="never">
      <template #header>
        <el-page-header v-if="!isEmbedded" @back="handleBack" content="我收藏的歌单" title="返回" />
      </template>

      <div class="starred-container" v-loading="loading">
        <el-row :gutter="20" v-if="playlists.length > 0">
          <el-col
            v-for="playlist in playlists"
            :key="playlist.playlist_id"
            :xs="12"
            :sm="8"
            :md="6"
            :lg="4"
          >
            <el-card 
              class="playlist-card" 
              hoverable 
              :body-style="{ padding: '20px' }"
              @click="handlePlaylistClick(playlist)"
            >
              <el-image
                :src="playlist.playlist_cover || ''"
                fit="cover"
                class="playlist-cover"
              >
                <template #error>
                  <div class="image-slot"><el-icon><Collection /></el-icon></div>
                </template>
              </el-image>
              <div class="playlist-info">
                <h3>{{ playlist.playlist_name }}</h3>
                <p>{{ playlist.song_count || 0 }}首</p>
              </div>
              <div class="playlist-actions">
                <el-button
                  type="danger"
                  size="small"
                  @click.stop="handleUnstar(playlist)"
                >
                  取消收藏
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-empty v-else description="您还没有收藏任何歌单" />
        
        <div class="pagination-container" v-if="playlists.length > 0 || total > 0">
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
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Collection } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyStarredPlaylists } from '@/api/user'
import { unstarPlaylist } from '@/api/music'
import type { Playlist } from '@/api/music'

const props = defineProps<{
  isEmbedded?: boolean
}>()

const router = useRouter()
const playlists = ref<Playlist[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const handleBack = () => {
  router.back()
}

const loadData = async () => {
  loading.value = true
  try {
    const res = await getMyStarredPlaylists(currentPage.value, pageSize.value)
    playlists.value = res.data.playlists
    total.value = res.data.total
  } catch (error) {
    console.error(error)
    ElMessage.error('加载收藏歌单失败')
  } finally {
    loading.value = false
  }
}

const handlePlaylistClick = (playlist: Playlist) => {
  router.push(`/playlists/${playlist.playlist_id}`)
}

const handleUnstar = (playlist: Playlist) => {
  ElMessageBox.confirm(
    '确定要取消收藏该歌单吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      await unstarPlaylist(playlist.playlist_id)
      ElMessage.success('取消收藏成功')
      // Refresh list to keep pagination correct
      if (playlists.value.length === 1 && currentPage.value > 1) {
        currentPage.value--
      }
      loadData()
    } catch (error) {
      ElMessage.error('取消收藏失败')
    }
  })
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  loadData()
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.my-starred-playlists {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.starred-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

.starred-card :deep(.el-card__header) {
  border-bottom: none;
}

.starred-card.no-border {
  border: none;
  background: transparent;
}

.playlist-card {
  margin-bottom: 20px;
  cursor: pointer;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
  background: rgba(255, 255, 255, 0.8);
  /* 注意：El-Card 的 padding 主要通过 body-style 控制，
     但这里定义基本样式不冲突 */
}

.playlist-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.playlist-cover {
  width: 100%;
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  font-size: 40px;
  color: #909399;
  border-radius: 8px; /* 稍微减小圆角以适应内部 padding */
  overflow: hidden;
}

.playlist-info {
  /* 这里原来的 padding: 10px 0; 可以保留，
     或者改为 margin-top: 10px 以获得更清晰的间距 */
  padding: 10px 0;
}

.playlist-info h3 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #303133;
}

.playlist-info p {
  margin: 4px 0 0;
  font-size: 12px;
  color: #909399;
}

.playlist-actions {
  margin-top: 5px; /* 稍微调整顶部间距 */
  text-align: right;
}

.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>