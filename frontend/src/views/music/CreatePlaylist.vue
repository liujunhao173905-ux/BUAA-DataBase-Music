<template>
  <div class="create-playlist-container">
    <el-card class="create-playlist-card">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-button type="default" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <h2>创建歌单</h2>
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
          >
            <el-button type="primary">选择封面</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持 JPG、PNG 格式，建议尺寸 300x300px
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item label="歌单介绍">
          <el-input
            v-model="formData.playlist_intro"
            type="textarea"
            :rows="4"
            placeholder="请输入歌单介绍（可选）"
          />
        </el-form-item>

        <el-form-item label="添加歌曲">
          <el-collapse v-model="activeNames">
            <el-collapse-item title="从收藏歌曲中选择" name="1">
              <div v-if="starredSongsLoading" class="loading-container">
                <el-skeleton :rows="3" animated />
              </div>
              <div v-else-if="starredSongs.length === 0" class="empty-container">
                <el-empty description="暂无收藏歌曲" />
              </div>
              <div v-else class="starred-songs-container">
                <el-checkbox-group v-model="selectedSongs">
                  <div v-for="song in starredSongs" :key="song.song_id" class="song-item">
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
          <el-button type="primary" @click="handleSubmit" :loading="submitting">创建歌单</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElForm, ElFormItem } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { createPlaylist, addSongToPlaylist } from '@/api/music'
import request from '@/api/request'

const router = useRouter()
const formRef = ref<InstanceType<typeof ElForm> | null>(null)
const submitting = ref(false)
const fileList = ref<any[]>([])

const formData = reactive({
  playlist_name: '',
  playlist_intro: '',
  playlist_cover: null as File | null,
})

// 收藏歌曲相关
const starredSongs = ref<any[]>([])
const starredSongsLoading = ref(false)
const selectedSongs = ref<number[]>([])
const activeNames = ref(['1'])

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
  }
  return false
}



// 获取用户收藏的歌曲
const fetchStarredSongs = async () => {
  starredSongsLoading.value = true
  try {
    const response = await request.get('/music/songs/starred/')
    starredSongs.value = response
  } catch (error) {
    ElMessage.error('加载收藏歌曲失败')
    console.error('Failed to fetch starred songs:', error)
  } finally {
    starredSongsLoading.value = false
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

    // 创建歌单
    const playlist = await createPlaylist(formDataToSend as any)
    
    // 添加选中的歌曲到歌单
    if (selectedSongs.value.length > 0) {
      // 使用 Promise.all 并行添加歌曲
      await Promise.all(
        selectedSongs.value.map(songId => addSongToPlaylist(playlist.playlist_id, songId))
      )
    }
    
    ElMessage.success('歌单创建成功！歌单将在审核通过后公开')
    router.push('/my/playlists')
  } catch (error) {
    ElMessage.error('歌单创建失败，请重试')
    console.error('创建歌单失败:', error)
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
}

// 组件挂载时获取收藏歌曲
onMounted(() => {
  fetchStarredSongs()
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

.starred-songs-container {
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
