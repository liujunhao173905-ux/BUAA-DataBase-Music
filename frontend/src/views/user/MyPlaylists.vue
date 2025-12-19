<template>
  <div class="my-playlists-container">
    <el-card class="my-playlists-card">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-button type="default" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <h2>我的歌单</h2>
          </div>
          <el-button type="primary" @click="handleCreatePlaylist">创建歌单</el-button>
        </div>
      </template>

      <el-table :data="playlists" stripe style="width: 100%">
        <!-- <el-table-column prop="playlist_id" label="歌单ID" width="100" /> -->
        <el-table-column prop="playlist_name" label="歌单名称" min-width="200">
          <template #default="scope">
            <div class="playlist-info">
              <el-image v-if="scope.row.playlist_cover" :src="scope.row.playlist_cover" class="playlist-cover" fit="cover" />
              <span>{{ scope.row.playlist_name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="playlist_intro" label="歌单介绍" min-width="300" />
        <el-table-column prop="playlist_createtime" label="创建时间" width="200">
          <template #default="scope">
            {{ formatDate(scope.row.playlist_createtime) }}
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'warning'">
              {{ scope.row.is_active ? '已公开' : '待审核' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleView(scope.row)">详情</el-button>
            <el-button type="success" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
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
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getMyPlaylists, deletePlaylist } from '@/api/music'
import type { Playlist } from '@/api/music'

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

.playlist-cover {
  width: 40px;
  height: 40px;
  margin-right: 10px;
  border-radius: 4px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
