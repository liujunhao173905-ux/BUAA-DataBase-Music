<template>
  <div class="my-songs-container">
    <el-card class="my-songs-card">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-button type="default" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <h2>我的歌曲</h2>
          </div>
          <el-button type="primary" @click="handleUploadSong">上传歌曲</el-button>
        </div>
      </template>

      <el-table :data="songs" stripe style="width: 100%">
        <el-table-column prop="song_id" label="歌曲ID" width="100" />
        <el-table-column prop="song_name" label="歌曲名称" min-width="200">
          <template #default="scope">
            <div class="song-info">
              <el-image v-if="scope.row.song_cover" :src="scope.row.song_cover" class="song-cover" fit="cover" />
              <span>{{ scope.row.song_name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="song_duration" label="时长" width="100">
          <template #default="scope">
            {{ formatDuration(scope.row.song_duration) }}
          </template>
        </el-table-column>
        <el-table-column prop="song_price" label="价格" width="100">
          <template #default="scope">
            ¥{{ scope.row.song_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="song_createtime" label="上传时间" width="200">
          <template #default="scope">
            {{ formatDate(scope.row.song_createtime) }}
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
            <el-button type="primary" size="small" @click="handleDetail(scope.row)">详情</el-button>
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
import { getMySongs, deleteSong } from '@/api/music'
import type { Song } from '@/api/music'

const router = useRouter()
const songs = ref<Song[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 格式化时长
const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 获取我的歌曲列表
const fetchSongs = async () => {
  try {
    loading.value = true
    const response = await getMySongs(currentPage.value, pageSize.value)
    songs.value = response.data.songs
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('获取歌曲列表失败')
    console.error('获取歌曲列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 上传歌曲
const handleUploadSong = () => {
  router.push('/music/upload-song')
}

// 查看歌曲详情
const handleDetail = (song: Song) => {
  router.push(`/songs/${song.song_id}`)
}

// 编辑歌曲
const handleEdit = (song: Song) => {
  router.push(`/music/edit-song/${song.song_id}`)
}

// 删除歌曲
const handleDelete = async (song: Song) => {
  try {
    await ElMessageBox.confirm('确定要删除该歌曲吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })

    // 调用删除歌曲的API
    await deleteSong(song.song_id)
    ElMessage.success('歌曲删除成功')
    fetchSongs()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('歌曲删除失败')
      console.error('删除歌曲失败:', error)
    }
  }
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchSongs()
}

// 当前页码变化
const handleCurrentChange = (current: number) => {
  currentPage.value = current
  fetchSongs()
}

// 返回上一页
const handleBack = () => {
  router.back()
}

// 组件挂载时获取歌曲列表
onMounted(() => {
  fetchSongs()
})
</script>

<style scoped>
.my-songs-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.my-songs-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.song-info {
  display: flex;
  align-items: center;
}

.song-cover {
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
