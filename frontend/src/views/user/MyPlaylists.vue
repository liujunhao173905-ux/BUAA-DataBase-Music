<template>
  <div class="my-playlists-container">
    <el-card class="my-playlists-card" :class="{ 'no-border': isEmbedded }">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;" v-if="!isEmbedded">
            <el-button type="default" @click="handleBack" circle>
              <el-icon><ArrowLeft /></el-icon>
            </el-button>
            <h2>我的歌单</h2>
          </div>
          <div v-else></div>
          <el-button type="primary" @click="handleCreatePlaylist" :icon="Plus" round>创建歌单</el-button>
        </div>
      </template>

      <div class="song-card" v-loading="loading">
        <div v-if="playlists.length > 0" class="song-list">
          <el-table :data="playlists" stripe style="width: 100%" @row-dblclick="handleView">
            <!-- <el-table-column prop="playlist_id" label="歌单ID" width="100" /> -->
            <el-table-column prop="playlist_name" label="歌单名称" min-width="200">
              <template #default="scope">
                <div class="playlist-info" @click="handleView(scope.row)" style="cursor: pointer;">
                  <div class="cover-wrapper">
                    <el-image v-if="scope.row.playlist_cover" :src="scope.row.playlist_cover" class="playlist-cover" fit="cover" />
                    <div class="hover-play"><el-icon><View /></el-icon></div>
                  </div>
                  <span class="playlist-name">{{ scope.row.playlist_name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="playlist_intro" label="歌单介绍" min-width="300">
               <template #default="scope">
                  <div class="text-ellipsis" :title="scope.row.playlist_intro">{{ scope.row.playlist_intro || '-' }}</div>
               </template>
            </el-table-column>
            <el-table-column prop="playlist_createtime" label="创建时间" width="180">
              <template #default="scope">
                {{ formatDate(scope.row.playlist_createtime) }}
              </template>
            </el-table-column>
            <el-table-column prop="playlist_status" label="状态" width="120">
              <template #default="scope">
                <el-tag
                  :type=statusColor(scope.row.playlist_status)>
                  {{ statusText(scope.row.playlist_status) }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="250" fixed="right">
              <template #default="scope">
                <el-button
                  type="primary"
                  size="small"
                  @click.stop="handleView(scope.row)"
                  plain>详情</el-button>

                <el-button
                  v-if="scope.row.playlist_status === 1 || scope.row.playlist_status === 2"
                  type="success"
                  size="small"
                  @click.stop="handleEdit(scope.row)"
                  plain>编辑</el-button>

                <!-- 其余状态显示「已锁定」或禁用 -->
                <el-button
                  v-else
                  type="info"
                  size="small"
                  disabled
                  plain>编辑</el-button>

                <el-button
                  type="danger"
                  size="small"
                  @click.stop="handleDelete(scope.row)"
                  :icon="Delete" circle />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Plus, View, Edit, Delete } from '@element-plus/icons-vue'
import { getMyPlaylists, deletePlaylist } from '@/api/music'
import type { Playlist } from '@/api/music'

const props = defineProps<{
  isEmbedded?: boolean
}>()

const router = useRouter()
const playlists = ref<Playlist[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return isNaN(date.getTime()) ? '- Invalid Date -' : date.toLocaleString()
}

const statusColor = (st: number) => {
  switch (st) {
    case 0: return 'warning'
    case 1: return 'success'
    case 2: return 'danger'
    case 3: return 'danger'
    default: return 'default'
  }
}

/* 0 待审核  1 通过  2 未通过  3 锁定 */
const statusText = (st: number) => {
  switch (st) {
    case 0: return '审核中'
    case 1: return '已上架'
    case 2: return '未过审'
    case 3: return '已锁定'
    default: return '未知'
  }
}

// 获取我的歌单列表
const fetchPlaylists = async () => {
  try {
    loading.value = true
    const response = await getMyPlaylists(currentPage.value, pageSize.value)
    playlists.value = response.data.playlists
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('获取歌单列表失败')
    console.error('获取歌单列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 创建歌单
const handleCreatePlaylist = () => {
  router.push('/music/create-playlist')
}

// 查看歌单详情
const handleView = (playlist: Playlist) => {
  // 存储当前路径，以便返回时使用
  sessionStorage.setItem('fromPath', '/my/playlists')
  router.push(`/playlists/${playlist.playlist_id}`)
}

// 编辑歌单
const handleEdit = (playlist: Playlist) => {
  router.push(`/music/edit-playlist/${playlist.playlist_id}`)
}

// 删除歌单
const handleDelete = async (playlist: Playlist) => {
  try {
    await ElMessageBox.confirm('确定要删除该歌单吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })

    // 调用删除歌单的API
    await deletePlaylist(playlist.playlist_id)
    ElMessage.success('歌单删除成功')
    fetchPlaylists()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('歌单删除失败')
      console.error('删除歌单失败:', error)
    }
  }
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchPlaylists()
}

// 当前页码变化
const handleCurrentChange = (current: number) => {
  currentPage.value = current
  fetchPlaylists()
}

// 返回上一页
const handleBack = () => {
  router.back()
}

// 组件挂载时获取歌单列表
onMounted(() => {
  fetchPlaylists()
})
</script>

<style scoped>
.my-playlists-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.my-playlists-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.playlist-info {
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

.playlist-cover {
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

.playlist-info:hover .hover-play {
  opacity: 1;
}

.playlist-name {
  font-weight: 500;
  color: #303133;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.no-border {
  border: none;
  box-shadow: none;
}

.embedded-actions {
  margin-bottom: 15px;
  display: flex;
  justify-content: flex-end;
}
</style>
