<template>
  <div class="create-playlist-container">
    <el-card class="create-playlist-card">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-button type="default" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <h2>编辑歌单</h2>
          </div>
        </div>
      </template>

      <el-form ref="formRef" :model="formData" label-width="80px" class="create-playlist-form">
        <el-form-item label="歌单名称" prop="playlist_name" :rules="[{ required: true, message: '请输入歌单名称', trigger: 'blur' }, { max: 128, message: '歌单名称不能超过128个字符', trigger: 'blur' }]">
          <el-input v-model="formData.playlist_name" placeholder="请输入歌单名称" />
        </el-form-item>

        <el-form-item label="歌单封面">
          <el-upload
            v-model:file-list="fileList"
            class="avatar-uploader"
            action=""
            :show-file-list="true"
            :before-upload="handleBeforeUpload"
            :auto-upload="false"
            :limit="1"
            :on-change="handleCoverChange"
            :on-remove="handleCoverRemove"
          >
            <el-button type="primary">选择封面</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持 JPG、PNG 格式，建议尺寸 300x300px
              </div>
            </template>
          </el-upload>
          <el-image v-if="currentCover" :src="currentCover" class="current-cover" fit="cover" />
        </el-form-item>

        <el-form-item label="歌单介绍">
          <el-input
            v-model="formData.playlist_intro"
            type="textarea"
            :rows="4"
            placeholder="请输入歌单介绍（可选）"
          />
        </el-form-item>

        <el-form-item label="批量删除">
          <el-collapse v-model="activeNames">
            <el-collapse-item title="从歌单歌曲中选择" name="1">
              <div v-if="allSongsLoading" class="loading-container">
                <el-skeleton :rows="3" animated />
              </div>
              <div v-else-if="allSongs.length === 0" class="empty-container">
                <el-empty description="歌单中暂无歌曲" />
              </div>
              <div v-else class="all-songs-container">
                <el-checkbox-group v-model="selectedSongs">
                  <div v-for="song in allSongs" :key="song.song_id" class="song-item">
                    <el-checkbox :label="song.song_id">
                      <div class="song-info">
                        <div class="song-name">{{ song.song_name }}</div>
                        <div class="song-singer">{{ song.song_singer_name }}</div>
                      </div>
                    </el-checkbox>
                  </div>
                </el-checkbox-group>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">保存修改</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElForm, ElFormItem, ElMessageBox } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getPlaylistDetail, updatePlaylist, addSongToPlaylist, removeSongFromPlaylist } from '@/api/music'
import request from '@/api/request'
import type { Playlist } from '@/api/music'

const router = useRouter()
const route = useRoute()
const formRef = ref<InstanceType<typeof ElForm> | null>(null)
const submitting = ref(false)
const fileList = ref<any[]>([])
const currentCover = ref<string | null>(null)

const originalData = reactive({
  playlist_name: '',
  playlist_intro: '',
})

const formData = reactive({
  playlist_name: '',
  playlist_intro: '',
  playlist_cover: null as File | null,
})

// 歌单歌曲相关
const allSongs = ref<any[]>([])
const allSongsLoading = ref(false)
const selectedSongs = ref<number[]>([])
const activeNames = ref(['1'])

// 获取歌单ID
const playlistId = ref<number>(Number(route.params.id))

const needsReview0 = ref(false)
const needsReview1 = ref(false)

// 处理封面上传前的验证
const handleBeforeUpload = (file: File) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('只支持 JPG/PNG 格式的图片')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }

  return true
}

// 处理封面文件变化
const handleCoverChange = (file: any, _fileList: any[]) => {
  if (file.raw) {
    formData.playlist_cover = file.raw
    needsReview0.value = true
  }
  return false
}

const handleCoverRemove = (file: any, _fileList: any[]) => {
  if (_fileList.length === 0) {
    formData.playlist_cover = null
    needsReview0.value = false
  }
  return false
}

// 获取歌单详情
const fetchPlaylistDetail = async () => {
  try {
    const playlist = await getPlaylistDetail(playlistId.value)
    formData.playlist_name = playlist.playlist_name
    originalData.playlist_name = playlist.playlist_name
    formData.playlist_intro = playlist.playlist_intro || ''
    originalData.playlist_intro = playlist.playlist_intro || ''
    if (playlist.playlist_cover) {
      currentCover.value = playlist.playlist_cover
    }
  } catch (error) {
    ElMessage.error('加载歌单详情失败')
    console.error('Failed to fetch playlist detail:', error)
  }
}

// 获取用户收藏的歌曲
// const fetchStarredSongs = async () => {
//   starredSongsLoading.value = true
//   try {
//     const response = await request.get('/music/songs/starred/')
//     starredSongs.value = response
//   } catch (error) {
//     ElMessage.error('加载收藏歌曲失败')
//     console.error('Failed to fetch starred songs:', error)
//   } finally {
//     starredSongsLoading.value = false
//   }
// }

// 获取歌单中的全部歌曲
const fetchAllSongs = async () => {
  allSongsLoading.value = true
  try {
    const response = await request.get(`/playlists/${playlistId.value}/get_songs`)
    allSongs.value = response
  } catch (error) {
    ElMessage.error('加载歌单歌曲失败')
    console.error('Failed to fetch all songs:', error)
  } finally {
    allSongsLoading.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    const formDataToSend = new FormData()
    formDataToSend.append('playlist_name', formData.playlist_name)
    if (formData.playlist_intro) {
      formDataToSend.append('playlist_intro', formData.playlist_intro)
    }
    if (formData.playlist_cover) {
      formDataToSend.append('playlist_cover', formData.playlist_cover)
    }
    
    if (formData.playlist_name !== originalData.playlist_name || formData.playlist_intro !== originalData.playlist_intro) {
      needsReview1.value = true
    }
    else {
      needsReview1.value = false
    }

    // console.log('debug: ', formData.playlist_cover, needsReview0, needsReview1)

    if (needsReview0.value || needsReview1.value) {
      // 弹出提示框
      await ElMessageBox.confirm('歌单信息有变更，需要重新审核。确认提交吗？', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '返回继续修改',
        type: 'warning',
      })
    }

    if (needsReview0.value || needsReview1.value) {
      // 更新歌单
      await updatePlaylist(playlistId.value, formDataToSend as any)
    }
    
    // 添加选中的歌曲到歌单
    if (selectedSongs.value.length > 0) {
      // 使用 Promise.all 并行添加歌曲
      await Promise.all(
        selectedSongs.value.map(songId => removeSongFromPlaylist(playlistId.value, songId))
      )
    }
    
    ElMessage.success('歌单修改成功！')
    router.push('/my/playlists')
  } catch (error) {
    ElMessage.error('歌单修改失败，请重试')
    console.error('修改歌单失败:', error)
  } finally {
    submitting.value = false
  }
}

// 返回上一页
const handleBack = () => {
  router.back()
}

// 重置表单
const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  fileList.value = []
  formData.playlist_cover = null
  selectedSongs.value = []
  fetchPlaylistDetail()
}

// 组件挂载时获取歌单详情和收藏歌曲
onMounted(() => {
  fetchPlaylistDetail()
  // fetchStarredSongs()
  fetchAllSongs()
})
</script>

<style scoped>
.create-playlist-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.create-playlist-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.create-playlist-form {
  margin-top: 20px;
}

.avatar-uploader {
  margin-bottom: 20px;
}

.current-cover {
  width: 100px;
  height: 100px;
  border-radius: 4px;
  margin-top: 10px;
}

/* .starred-songs-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 10px;
} */

.all-songs-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 10px;
}

.song-item {
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.song-item:hover {
  background-color: #f5f7fa;
}

.song-item:last-child {
  border-bottom: none;
}

.song-info {
  margin-left: 10px;
  display: inline-block;
}

.song-name {
  font-weight: 500;
  color: #303133;
}

.song-singer {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.loading-container {
  padding: 20px;
}

.empty-container {
  padding: 30px 0;
}
</style>