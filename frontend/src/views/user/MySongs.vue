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
             
             <!-- 隐藏的文件夹输入框 -->
             <input
               type="file"
               ref="folderInput"
               style="display: none"
               webkitdirectory
               directory
               multiple
               @change="handleFolderImport"
             />

             <el-button @click="triggerFolderImport" style="margin-left: 10px;">
               批量导入
             </el-button>
             
             <el-button @click="showImportInstructions = true" style="margin-left: 10px;" type="info" plain>
               导入说明
             </el-button>

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
             
             <!-- 隐藏的文件夹输入框 -->
             <input
               type="file"
               ref="folderInput"
               style="display: none"
               webkitdirectory
               directory
               multiple
               @change="handleFolderImport"
             />

             <el-button @click="triggerFolderImport" style="margin-left: 10px;">
               批量导入
             </el-button>
             
             <el-button @click="showImportInstructions = true" style="margin-left: 10px;" type="info" plain>
               导入说明
             </el-button>

             <el-button style="margin-left: 10px;" @click="showExternalDialog = true">
               从外部导入
             </el-button>

             <el-button type="primary" @click="handleUploadSong" style="margin-left: 10px;">上传歌曲</el-button>
           </div>
        </div>
      </template>

      <div v-if="songs.length > 0" class="song-list">
        <div class="table-wrapper">
          <el-table :data="songs" stripe style="width: 100%; height: 100%" @selection-change="handleSelectionChange" @row-dblclick="handlePlay">
            <el-table-column type="selection" width="55" />
            <el-table-column prop="song_name" label="歌曲名称" min-width="200" align="center">
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
            <el-table-column prop="song_duration" label="时长" width="100" align="center">
              <template #default="scope">
                {{ formatDuration(scope.row.song_duration) }}
              </template>
            </el-table-column>
            <el-table-column prop="song_price" label="价格" width="100" align="center">
              <template #default="scope">
                {{ formatPrice(scope.row.song_price) }}
              </template>
            </el-table-column>
            <el-table-column prop="song_createtime" label="上传时间" width="200" align="center">
              <template #default="scope">
                {{ formatDate(scope.row.song_createtime) }}
              </template>
            </el-table-column>
            <el-table-column prop="song_status" label="状态" width="120" align="center">
              <template #default="scope">
                <el-tag
                  :type="statusColor(scope.row.song_status)">
                  {{ statusText(scope.row.song_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="250" fixed="right" align="center">
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
      </div>
      
      <el-empty v-else description="暂无歌曲" style="flex: 1; display: flex; justify-content: center; align-items: center;" />

    </el-card>

    <el-dialog v-model="showImportInstructions" title="批量导入说明" width="600px">
      <div class="import-instructions">
        <p>请选择一个包含以下内容的文件夹：</p>
        <ol>
          <li>
            <strong>歌曲详情文件</strong>：必须命名为 <code>歌曲详情.xlsx</code> 或 <code>歌曲详情.xml</code>。
          </li>
          <li>
            <strong>资源文件</strong>：歌曲的音频文件（mp3/flac等）和封面图片（jpg/png等）。
          </li>
        </ol>
        <p><strong>表格/XML 格式要求：</strong></p>
        <ul>
          <li><code>song_name</code> / <code>歌曲名称</code>：歌曲标题（必填）</li>
          <li><code>song_singer_name</code> / <code>歌手</code>：歌手名称（可选）</li>
          <li><code>song_price</code> / <code>价格</code>：价格（可选，默认为0）</li>
          <li><code>song_file</code> / <code>录音文件</code>：音频文件名（包含扩展名）。若为空或未找到文件，系统将自动使用占位文件并提示。</li>
          <li><code>song_cover</code> / <code>封面文件</code>：封面文件名（包含扩展名）。若为空或未找到文件，系统将自动使用占位图片并提示。</li>
        </ul>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="showImportInstructions = false">知道了</el-button>
        </span>
      </template>
    </el-dialog>

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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowDown, Delete, VideoPlay } from '@element-plus/icons-vue'
import { getMySongs, deleteSong, exportSongs, importSongs, searchExternalSongs, importExternalSong, uploadSong } from '@/api/music'
import type { Song } from '@/api/music'
import { usePlayerStore } from '@/stores/player'
import * as XLSX from 'xlsx'

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

// 批量导入相关
const folderInput = ref<HTMLInputElement | null>(null)
const showImportInstructions = ref(false)

const triggerFolderImport = async () => {
  try {
    // 尝试使用现代 API
    if ('showDirectoryPicker' in window) {
      try {
        const handle = await (window as any).showDirectoryPicker()
        const files: File[] = []
        
        // 递归遍历函数
        async function scanEntry(entry: any) {
           if (entry.kind === 'file') {
              const file = await entry.getFile()
              files.push(file)
           } else if (entry.kind === 'directory') {
              for await (const child of entry.values()) {
                 await scanEntry(child)
              }
           }
        }
        
        await scanEntry(handle)
        processFiles(files)
      } catch (err) {
        if ((err as Error).name === 'AbortError') return // 用户取消
        console.error(err)
        ElMessage.error('无法打开文件夹选择器')
      }
    } else {
      // 降级方案
      folderInput.value?.click()
    }
  } catch (err) {
    console.error(err)
    folderInput.value?.click()
  }
}

const handleFolderImport = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files) {
    processFiles(Array.from(files))
    target.value = '' // 清空 input
  }
}

const processFiles = async (files: File[]) => {
  if (!files || files.length === 0) {
    ElMessageBox.alert('所选文件夹为空或未检测到文件，请检查文件夹内容。', '提示', {
      confirmButtonText: '确定',
      type: 'warning'
    })
    return
  }

  // 1. 寻找元数据文件
  let metadataFile: File | null = null
  const resourceFiles = new Map<string, File>()

  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    if (file.name === '歌曲详情.xlsx' || file.name === '歌曲详情.xls' || file.name === '歌曲详情.xml') {
      metadataFile = file
    } else {
      resourceFiles.set(file.name, file)
    }
  }

  if (!metadataFile) {
    ElMessageBox.alert('在所选文件夹中未找到“歌曲详情”文件（.xlsx, .xls 或 .xml），请检查文件夹内容。', '提示', {
      confirmButtonText: '确定',
      type: 'warning'
    })
    return
  }

  try {
    loading.value = true
    let songEntries: any[] = []

    // 2. 解析元数据
    if (metadataFile.name.endsWith('.xml')) {
      const text = await metadataFile.text()
      const parser = new DOMParser()
      const xmlDoc = parser.parseFromString(text, 'text/xml')
      const items = xmlDoc.getElementsByTagName('item') // 假设 XML 结构为 <root><item>...</item></root>
      // 如果没有 item 标签，尝试 row 或者 song
      const rows = items.length > 0 ? items : (xmlDoc.getElementsByTagName('row').length > 0 ? xmlDoc.getElementsByTagName('row') : xmlDoc.getElementsByTagName('song'))
      
      for (let i = 0; i < rows.length; i++) {
        const row = rows[i]
        const entry: any = {}
        for (let j = 0; j < row.children.length; j++) {
          const child = row.children[j]
          entry[child.tagName] = child.textContent
        }
        songEntries.push(entry)
      }
    } else {
      // Excel
      const arrayBuffer = await metadataFile.arrayBuffer()
      const workbook = XLSX.read(arrayBuffer, { type: 'array' })
      const firstSheetName = workbook.SheetNames[0]
      const worksheet = workbook.Sheets[firstSheetName]
      songEntries = XLSX.utils.sheet_to_json(worksheet)
    }

    if (songEntries.length === 0) {
      ElMessage.warning('歌曲详情文件为空')
      return
    }

    let successCount = 0
    let warningMessages: string[] = []

    // 3. 遍历并上传
    for (const entry of songEntries) {
      // 字段映射兼容
      const name = entry['song_name'] || entry['歌曲名称']
      const singer = entry['song_singer_name'] || entry['歌手']
      const price = entry['song_price'] || entry['价格']
      const fileName = entry['song_file'] || entry['录音文件']
      const coverName = entry['song_cover'] || entry['封面文件']

      if (!name) {
        warningMessages.push(`跳过：缺少歌曲名称`)
        continue
      }

      const formData = new FormData()
      formData.append('song_name', name)
      if (singer) formData.append('song_singer_name', singer)
      formData.append('song_price', price || '0')

      // 处理音频文件
      if (fileName && resourceFiles.has(fileName)) {
        formData.append('song_file', resourceFiles.get(fileName)!)
      } else {
        // 占位逻辑
        const placeholderBlob = new Blob(['Placeholder Audio'], { type: 'audio/mp3' })
        const placeholderFile = new File([placeholderBlob], 'placeholder.mp3', { type: 'audio/mp3' })
        formData.append('song_file', placeholderFile)
        warningMessages.push(`歌曲 "${name}"：未找到音频文件 "${fileName || '空'}"，已使用占位文件。`)
      }

      // 处理封面文件
      if (coverName && resourceFiles.has(coverName)) {
        formData.append('song_cover', resourceFiles.get(coverName)!)
      } else {
         // 占位逻辑
        const placeholderBlob = new Blob(['Placeholder Image'], { type: 'image/jpeg' })
        const placeholderFile = new File([placeholderBlob], 'placeholder.jpg', { type: 'image/jpeg' })
        formData.append('song_cover', placeholderFile)
        warningMessages.push(`歌曲 "${name}"：未找到封面文件 "${coverName || '空'}"，已使用占位图片。`)
      }

      try {
        await uploadSong(formData)
        successCount++
      } catch (err) {
        warningMessages.push(`歌曲 "${name}" 上传失败`)
        console.error(err)
      }
    }

    // 4. 结果反馈
    if (successCount > 0) {
      ElMessage.success(`成功导入 ${successCount} 首歌曲`)
      fetchSongs()
    }

    if (warningMessages.length > 0) {
      // 延迟一点显示警告，防止被成功消息覆盖
      setTimeout(() => {
        const msg = warningMessages.length > 5 
          ? `导入完成，但有 ${warningMessages.length} 个警告（前5个）：\n${warningMessages.slice(0, 5).join('\n')}...` 
          : `导入警告：\n${warningMessages.join('\n')}`
        
        ElMessageBox.alert(msg, '导入报告', {
          confirmButtonText: '确定',
          type: 'warning',
          customStyle: { whiteSpace: 'pre-line' }
        })
      }, 500)
    }

  } catch (error) {
    console.error('导入处理出错:', error)
    ElMessage.error('导入处理出错，请检查文件格式')
  } finally {
    loading.value = false
  }
}

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

    const isExcel = command === 'excel'
    const extension = isExcel ? 'xlsx' : 'xml'
    const mimeType = isExcel 
      ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
      : 'application/xml'

    const blob = new Blob([res], { type: mimeType })

    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `music_export.${extension}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')

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
    // 错误处理
  }
  return false 
}

const handleExternalSearch = async () => {
  if (!externalKeyword.value) return
  externalLoading.value = true
  try {
    const res = await searchExternalSongs(externalKeyword.value)
    externalResults.value = res
  } catch (error) {
    // Error handled
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

const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchSongs()
}

const handleCurrentChange = (current: number) => {
  currentPage.value = current
  fetchSongs()
}

const handleBack = () => {
  router.back()
}

onMounted(() => {
  fetchSongs()
})
</script>

<style scoped>
/* 1. 容器：高度 100%，Flex 列布局 */
.my-songs-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

/* 2. 卡片：占满剩余空间，Flex 列布局，防止溢出 */
.my-songs-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
  
  flex: 1; 
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.my-songs-card.no-border {
  border: none;
  background: transparent;
}

/* 3. 卡片 Body：穿透修改，Flex 列布局，限制溢出 */
:deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0 20px 20px 20px;
}

/* 4. 歌曲列表容器 */
.song-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 5. 表格包装器：占据剩余空间，隐藏溢出 */
.table-wrapper {
  flex: 1;
  overflow: hidden;
}

/* 样式微调：表格透明背景 */
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
  padding-bottom: 0;
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

/* 6. 分页栏：固定底部，不被压缩 */
.pagination-container {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}
</style>