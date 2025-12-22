<template>
  <div class="profile-container">
    <el-card class="profile-card" shadow="never">
      <template #header>
        <el-page-header @back="handleBack" content="个人资料" title="返回" />
      </template>
      
      <div v-if="user" class="profile-content">
        <!-- 内容标签页 -->
        <el-tabs v-model="activeTab" class="profile-tabs">
          <el-tab-pane label="个人资料" name="profile">
            <div class="avatar-section">
              <el-avatar
                :size="120"
                :src="avatarPreview"
                class="user-avatar"
                @error="handleAvatarError"
              >
                <el-icon><User /></el-icon>
              </el-avatar>
              <el-upload
                class="avatar-uploader"
                action=""
                :show-file-list="false"
                :before-upload="beforeUpload"
                :auto-upload="false"
                :limit="1"
                :on-change="handleAvatarChange"
                :headers="uploadHeaders"
              >
                <el-button type="primary" size="small">更换头像</el-button>
              </el-upload>
            </div>
            
            <el-form
              ref="formRef"
              :model="form"
              :rules="rules"
              label-width="100px"
              class="profile-form"
            >
              <el-form-item label="用户名">
                <el-input v-model="user.user_name" disabled />
              </el-form-item>
              
              <el-form-item label="用户类型">
                <el-tag :type="getUserTypeTag(user.user_type)">
                  {{ user.user_type_display }}
                </el-tag>
              </el-form-item>
              
              <el-form-item label="手机号" prop="user_mobile">
                <el-input
                  v-model="form.user_mobile"
                  placeholder="请输入手机号"
                  prefix-icon="Phone"
                />
              </el-form-item>

              <el-form-item label="性别" prop="user_gender">
                <el-select v-model="form.user_gender" placeholder="请选择性别">
                  <el-option label="保密" :value="0" />
                  <el-option label="男" :value="1" />
                  <el-option label="女" :value="2" />
                </el-select>
              </el-form-item>

              <el-form-item label="出生日期" prop="user_birth_date">
                <el-date-picker
                  v-model="form.user_birth_date"
                  type="date"
                  placeholder="选择日期"
                  :max="maxDate"
                />
              </el-form-item>

              <el-form-item label="年龄" prop="user_age">
                <el-input :model-value="computedAge" disabled />
              </el-form-item>

              <el-form-item label="账户余额" prop="user_balance">
                <el-input :model-value="`¥${user.user_balance || 0}`" disabled />
              </el-form-item>
              
              <el-form-item label="注册时间">
                <span>{{ formatDate(user.user_createtime) }}</span>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleUpdate" :loading="loading">
                  保存修改
                </el-button>
                <el-button @click="handleLogout">退出登录</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { User, ArrowLeft } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
// 导入API
import { updateUserProfile } from '@/api/user'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const user = computed(() => authStore.user)

const form = reactive({
  user_avatar: null as File | null,
  user_mobile: user.value?.user_mobile,
  user_gender: user.value?.user_gender,
  user_birth_date: user.value?.user_birth_date ? new Date(user.value.user_birth_date as string) : null as Date | null,
})

const maxDate = computed(() => new Date())

const computedAge = computed(() => {
  if (!form.user_birth_date) return ''
  const today = new Date()
  const birth = new Date(form.user_birth_date)
  let age = today.getFullYear() - birth.getFullYear()
  const m = today.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--
  return age.toString()
})

const avatarPreview = ref<string>(user.value?.user_avatar || '')  // 初始用后端头像

const validateMobile = (_rule: any, value: any, callback: any) => {
  if (value && !/^1[3-9]\d{9}$/.test(value)) {
    callback(new Error('请输入正确的手机号'))
  } else {
    callback()
  }
}

const validateBirth = (_rule: any, value: Date | null, callback: any) => {
  if (!value) return callback()                 // 允许空（可选）
  if (value > new Date()) {
    return callback(new Error('出生日期不能晚于当前日期'))
  }
  callback()
}

const rules: FormRules = {
  user_mobile: [
    { validator: validateMobile, trigger: 'blur' },
  ],
  user_birth_date: [
    { validator: validateBirth, trigger: 'blur' },
  ],
}

const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${authStore.token}`,
}))

// 处理头像加载失败
const handleAvatarError = () => {
  ElMessage.warning('头像加载失败，显示默认头像')
}

// 当前激活的标签页
const activeTab = ref('profile')

onMounted(() => {
  if (user.value) {
    form.user_mobile = user.value.user_mobile || ''
  }
})

const getUserTypeTag = (type: number) => {
  const tags = ['', 'success', 'danger']
  return tags[type] || ''
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 处理歌曲文件变化
const handleAvatarChange = (file: any, _fileList: any[]) => {
  if (file.raw) {
    form.user_avatar = file.raw
    avatarPreview.value = URL.createObjectURL(file.raw)
    ElMessage.success('头像上传成功')
  }
  return false
}

const handleUpdate = async () => {
  if (!formRef.value) return
  const valid = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  try {
    const formDataToSend = new FormData()
    if (form.user_mobile) {
      formDataToSend.append('user_mobile', form.user_mobile)
    }
    if (form.user_avatar) {
      formDataToSend.append('user_avatar', form.user_avatar)
    }
    if (form.user_gender) {
      formDataToSend.append('user_gender', form.user_gender.toString())
    }
    if (form.user_birth_date) {
      formDataToSend.append('user_birth_date', form.user_birth_date.toLocaleDateString('en-CA').split('T')[0])
    }
    const user = await updateUserProfile(formDataToSend)
    authStore.updateUser(user)
    await authStore.initUser()
    if (!authStore.isAuthenticated) {
      ElMessage.error('登录状态已失效，请重新登录')
      router.replace('/login')
      return
    }
    ElMessage.success('更新成功！')
  } finally {
    setTimeout(() => {
      loading.value = false
      router.replace('/mine')
    }, 50)
  }
}

// 返回上一页
const handleBack = () => {
  router.back()
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    authStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }).catch(() => {})
}
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.profile-card {
  min-height: 500px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.profile-content {
  padding: 20px 0;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.user-avatar {
  margin-bottom: 15px;
  border: 4px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.profile-form {
  max-width: 600px;
  margin: 0 auto;
}

/* 标签页样式 */
.profile-tabs {
  margin-top: 20px;
}


@media (max-width: 768px) {
  .profile-container {
    padding: 0 10px;
  }
}
</style>

