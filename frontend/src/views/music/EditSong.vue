<template>
  <div class="upload-song-container">
    <el-card class="upload-song-card">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-button type="default" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <h2>编辑歌曲</h2>
          </div>
        </div>
      </template>

      <el-form ref="formRef" :model="formData" label-width="100px" class="upload-song-form">
        <el-form-item label="歌曲名称" prop="song_name" :rules="[{ required: true, message: '请输入歌曲名称', trigger: 'blur' }, { max: 128, message: '歌曲名称不能超过128个字符', trigger: 'blur' }]">
          <el-input v-model="formData.song_name" placeholder="请输入歌曲名称" />
        </el-form-item>

        <el-form-item label="歌曲文件">
          <el-upload
            v-model:file-list="songFileList"
            class="file-uploader"
            action=""
            :show-file-list="true"
            :before-upload="handleSongBeforeUpload"
            :auto-upload="false"
            :limit="1"
            :on-change="handleSongChange"
          >
            <el-button type="primary">重新上传歌曲</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持 MP3、WAV、OGG 格式，大小不超过 50MB
              </div>
            </template>
          </el-upload>
          <!-- <div v-if="currentSongName" class="current-file-info">
            当前歌曲：{{ currentSongName }}
          </div> -->
        </el-form-item>

        <el-form-item label="歌曲封面">
          <el-upload
            v-model:file-list="coverFileList"
            class="avatar-uploader"
            action=""
            :show-file-list="true"
            :before-upload="handleCoverBeforeUpload"
            :auto-upload="false"
            :limit="1"
            :on-change="handleCoverChange"
          >
            <el-button type="primary">重新上传封面</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持 JPG、PNG 格式，建议尺寸 300x300px
              </div>
            </template>
          </el-upload>
          <!-- <el-image v-if="currentCover" :src="currentCover" class="current-cover" fit="cover" /> -->
        </el-form-item>

        <!-- <el-form-item label="歌曲时长" prop="song_duration" :rules="[{ required: true, message: '请输入歌曲时长', trigger: 'blur' }, { type: 'number', min: 1, message: '歌曲时长必须大于0秒', trigger: 'blur' }]">
          <el-input-number v-model="formData.song_duration" :min="1" placeholder="请输入歌曲时长（秒）" style="width: 100%;" />
        </el-form-item> -->

        <el-form-item label="歌曲价格" prop="song_price" :rules="[{ type: 'number', min: 0, message: '歌曲价格不能为负数', trigger: 'blur' }]">
          <el-input-number v-model="formData.song_price" :min="0" :precision="2" :step="0.1" placeholder="请输入歌曲价格（元）" style="width: 100%;" />
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
import { ElMessage, ElForm } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getSongDetail, updateSong } from '@/api/music'
import type { Song } from '@/api/music'

const router = useRouter()
const route = useRoute()
const formRef = ref<InstanceType<typeof ElForm> | null>(null)
const submitting = ref(false)
const songFileList = ref<any[]>([])
const coverFileList = ref<any[]>([])
const currentCover = ref<string | null>(null)
const currentSongName = ref<string | null>(null)
  const duration = ref<number>(0)

const formData = reactive({
  song_name: '',
  song_file: null as File | null,
  song_cover: null as File | null,
  song_duration: 0,
  song_price: 0.00,
})

// 获取歌曲ID
const songId = ref<number>(Number(route.params.id))

async function getAudioDuration(file: File): Promise<number> {
  return new Promise((resolve, reject) => {
    const audio = new Audio()
    const url   = URL.createObjectURL(file)

    audio.addEventListener('loadedmetadata', () => {
      resolve(Math.round(audio.duration)) // 仅秒数
      URL.revokeObjectURL(url)
    })
    audio.addEventListener('error', () => {
      URL.revokeObjectURL(url)
      reject(new Error('无法读取音频时长'))
    })

    audio.src = url
    audio.load()
  })
}

// 处理歌曲文件上传前的验证
const handleSongBeforeUpload = (file: File) => {
  const isValidType = ['audio/mpeg', 'audio/wav', 'audio/ogg'].includes(file.type)
  const isLt50M = file.size / 1024 / 1024 < 50

  if (!isValidType) {
    ElMessage.error('只支持 MP3、WAV、OGG 格式的音频文件')
    return false
  }
  if (!isLt50M) {
    ElMessage.error('歌曲文件大小不能超过 50MB')
    return false
  }

  return true
}

// 处理歌曲文件变化
const handleSongChange = (file: any, _fileList: any[]) => {
  if (file.raw) {
    formData.song_file = file.raw
  }
  return false
}

// 处理封面上传前的验证
const handleCoverBeforeUpload = (file: File) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('只支持 JPG、PNG 格式的图片')
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
    formData.song_cover = file.raw
  }
  return false
}

// 获取歌曲详情
const fetchSongDetail = async () => {
  try {
    const song = await getSongDetail(songId.value)
    formData.song_name = song.song_name
    formData.song_duration = song.song_duration
    formData.song_price = song.song_price
    if (song.song_cover) {
      currentCover.value = song.song_cover
    }
    currentSongName.value = song.song_name
  } catch (error) {
    ElMessage.error('加载歌曲详情失败')
    console.error('Failed to fetch song detail:', error)
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    const formDataToSend = new FormData()
    formDataToSend.append('song_name', formData.song_name)
    if (formData.song_file) {
      formDataToSend.append('song_file', formData.song_file)
    }
    if (formData.song_cover) {
      formDataToSend.append('song_cover', formData.song_cover)
    }
    // formDataToSend.append('song_duration', formData.song_duration.toString())
    if (formData.song_file) {
      try {
        duration.value = await getAudioDuration(formData.song_file)
      } catch (e) {
        duration.value = 0
      }
      formDataToSend.append('song_duration', duration.value.toString())
    }
    formDataToSend.append('song_price', formData.song_price.toString())

    await updateSong(songId.value, formDataToSend)
    ElMessage.success('歌曲修改成功！歌曲将在审核通过后更新')
    router.push('/my/songs')
  } catch (error) {
    ElMessage.error('歌曲修改失败，请重试')
    console.error('修改歌曲失败:', error)
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
  formRef.value?.resetFields()
  songFileList.value = []
  coverFileList.value = []
  formData.song_file = null
  formData.song_cover = null
  fetchSongDetail()
}

// 组件挂载时获取歌曲详情
onMounted(() => {
  fetchSongDetail()
})
</script>

<style scoped>
.upload-song-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.upload-song-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-song-form {
  margin-top: 20px;
}

.file-uploader,
.avatar-uploader {
  margin-bottom: 20px;
}

.current-cover {
  width: 100px;
  height: 100px;
  border-radius: 4px;
  margin-top: 10px;
}

.current-file-info {
  margin-top: 10px;
  font-size: 14px;
  color: #606266;
}
</style>