<template>
  <div class="my-songs-container">
    <el-card class="my-songs-card" :class="{ 'no-border': isEmbedded }" shadow="never">
      <template #header>
        <el-page-header v-if="!isEmbedded" @back="handleBack" content="我的歌曲" title="返回">
          <template #extra>
            <div class="actions">
             <el-dropdown @command="handleExport">
               <el-button>
                 导出 <el-icon class="el-icon--right"><ArrowDown /></el-icon>
               </el-button>
               <template #dropdown>
                 <el-dropdown-menu>
                   <el-dropdown-item command="excel">导出 Excel</el-dropdown-item>
                   <el-dropdown-item command="xml">导出 XML</el-dropdown-item>
                 </el-dropdown-menu>
               </template>
             </el-dropdown>
             
             <el-upload
               class="upload-demo"
               action="#"
               :show-file-list="false"
               :before-upload="handleImport"
               style="display: inline-block; margin-left: 10px;"
             >
               <el-button>导入 Excel/XML</el-button>
             </el-upload>

             <el-button style="margin-left: 10px;" @click="showExternalDialog = true">
               从外部导入
             </el-button>

             <el-button type="primary" @click="handleUploadSong" style="margin-left: 10px;">上传歌曲</el-button>
           </div>
          </template>
        </el-page-header>
        <div v-else class="card-header" style="display: flex; justify-content: flex-end;">
           <div class="actions">
             <el-dropdown @command="handleExport">
               <el-button>
                 导出 <el-icon class="el-icon--right"><ArrowDown /></el-icon>
               </el-button>
               <template #dropdown>
                 <el-dropdown-menu>
                   <el-dropdown-item command="excel">导出 Excel</el-dropdown-item>
                   <el-dropdown-item command="xml">导出 XML</el-dropdown-item>
                 </el-dropdown-menu>
               </template>
             </el-dropdown>
             
             <el-upload
               class="upload-demo"
               action="#"
               :show-file-list="false"
               :before-upload="handleImport"
               style="display: inline-block; margin-left: 10px;"
             >
               <el-button>导入 Excel/XML</el-button>
             </el-upload>

             <el-button style="margin-left: 10px;" @click="showExternalDialog = true">
               从外部导入
             </el-button>

             <el-button type="primary" @click="handleUploadSong" style="margin-left: 10px;">上传歌曲</el-button>
           </div>
        </div>
      </template>

      <!-- 外部导入对话框 -->
      <el-dialog v-model="showExternalDialog" title="从外部API导入" width="600px">
         <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <el-input v-model="externalKeyword" placeholder="输入歌名或歌手" @keyup.enter="handleExternalSearch" />
            <el-button type="primary" @click="handleExternalSearch" :loading="externalLoading">搜索</el-button>
         </div>
         
         <el-table :data="externalResults" v-loading="externalLoading" height="300" style="width: 100%">
            <el-table-column property="name" label="歌名" />
            <el-table-column property="singer" label="歌手" />
            <el-table-column label="操作" width="100">
               <template #default="scope">
                  <el-button type="success" size="small" @click="importExternal(scope.row)">导入</el-button>
               </template>
            </el-table-column>
         </el-table>
      </el-dialog>

      <el-table :data="songs" stripe style="width: 100%" @selection-change="handleSelectionChange" @row-dblclick="handlePlay">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="song_name" label="歌曲名称" min-width="200">
          <template #default="scope">
            <div class="song-info" @click="handlePlay(scope.row)" style="cursor: pointer;">
              <div class="cover-wrapper">
                <el-image v-if="scope.row.song_cover" :src="scope.row.song_cover" class="song-cover" fit="cover" />
                <div class="hover-play"><el-icon><VideoPlay /></el-icon></div>
              </div>
              <span class="song-name">{{ scope.row.song_name }}</span>
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
            {{ formatPrice(scope.row.song_price) }}
          </template>
        </el-table-column>
        <el-table-column prop="song_createtime" label="上传时间" width="200">
          <template #default="scope">
            {{ formatDate(scope.row.song_createtime) }}
          </template>
        </el-table-column>
        <el-table-column prop="song_status" label="状态" width="120">
          <template #default="scope">
            <el-tag
              :type=statusColor(scope.row.song_status)>
              {{ statusText(scope.row.song_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click.stop="handleDetail(scope.row)"
              plain>详情</el-button>

            <el-button
              v-if="scope.row.song_status === 1 || scope.row.song_status === 2"
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
              :icon="Delete" circle></el-button>
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
import { ArrowDown, Delete, VideoPlay } from '@element-plus/icons-vue'
import { getMySongs, deleteSong, exportSongs, importSongs, searchExternalSongs, importExternalSong } from '@/api/music'
import type { Song } from '@/api/music'
import { usePlayerStore } from '@/stores/player'

const props = defineProps<{
  isEmbedded?: boolean
}>()

const router = useRouter()
const playerStore = usePlayerStore()

const songs = ref<Song[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)
const multipleSelection = ref<Song[]>([])

// 外部导入相关
const showExternalDialog = ref(false)
const externalKeyword = ref('')
const externalResults = ref<any[]>([])
const externalLoading = ref(false)

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

const handleSelectionChange = (val: Song[]) => {
  multipleSelection.value = val
}

const handleExport = async (command: string) => {
  try {
    const ids = multipleSelection.value.map(s => s.song_id)
    if (ids.length === 0) {
        ElMessage.warning('请选择要导出的歌曲')
        return
    }
    const res: any = await exportSongs(command as 'excel' | 'xml', ids)
    // 后端应该返回下载链接或文件流
    // 如果是文件流，需要处理下载
    if (res && res.url) {
        window.open(res.url, '_blank')
    } else {
        ElMessage.success('导出任务已开始')
    }
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleImport = async (file: any) => { 
  try {
    const res: any = await importSongs(file)
    ElMessage.success(res.message || '导入成功')
    fetchSongs()
  } catch (error: any) {
    // 错误已经在 request.ts 中处理了，但这里可能需要显示特定信息
    // 如果是 400 错误，request.ts 会显示 error message
    // 这里我们只是阻止默认上传行为
  }
  return false // 阻止自动上传
}

const handleExternalSearch = async () => {
  if (!externalKeyword.value) return
  externalLoading.value = true
  try {
    const res = await searchExternalSongs(externalKeyword.value)
    externalResults.value = res
  } catch (error) {
    // Error handled in interceptor
  } finally {
    externalLoading.value = false
  }
}

const importExternal = async (item: any) => {
  try {
    await importExternalSong(item)
    ElMessage.success('导入成功')
    fetchSongs()
    showExternalDialog.value = false
  } catch (error) {
    // Error handled
  }
}

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

// 播放歌曲
const handlePlay = (song: Song) => {
  playerStore.setPlaylist(songs.value)
  playerStore.playSong(song)
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
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

.my-songs-card.no-border {
  border: none;
  box-shadow: none;
  background: transparent;
}

:deep(.el-table) {
  background-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(255, 255, 255, 0.5);
  --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.5);
}

:deep(.el-table th.el-table__cell) {
  background-color: rgba(255, 255, 255, 0.5);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.song-info {
  display: flex;
  align-items: center;
  padding: 4px 0;
  transition: transform 0.2s;
}

.song-info:hover {
  transform: translateX(4px);
}

.cover-wrapper {
  position: relative;
  width: 48px;
  height: 48px;
  margin-right: 16px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.song-cover {
  width: 100%;
  height: 100%;
  display: block;
  transition: transform 0.3s;
}

.cover-wrapper:hover .song-cover {
  transform: scale(1.1);
}

.hover-play {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: #fff;
  font-size: 24px;
}

.cover-wrapper:hover .hover-play {
  opacity: 1;
}

.song-name {
  font-weight: 600;
  color: #303133;
  font-size: 15px;
}

.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>
