<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-button type="default" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <span>个人资料</span>
          </div>
        </div>
      </template>
      
      <div v-if="user" class="profile-content">
        <!-- 内容标签页 -->
        <el-tabs v-model="activeTab" class="profile-tabs">
          <el-tab-pane label="个人资料" name="profile">
            <div class="avatar-section">
              <el-avatar
                :size="120"
                :src="user.user_avatar || ''"
                class="user-avatar"
                @error="handleAvatarError"
              >
                <el-icon><User /></el-icon>
              </el-avatar>
              <el-upload
                class="avatar-uploader"
                action="/api/users/profile/"
                :method="'PUT'"
                :show-file-list="false"
                :before-upload="beforeUpload"
                :on-success="handleAvatarSuccess"
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
  user_mobile: '',
})

const validateMobile = (_rule: any, value: any, callback: any) => {
  if (value && !/^1[3-9]\d{9}$/.test(value)) {
    callback(new Error('请输入正确的手机号'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  user_mobile: [
    { validator: validateMobile, trigger: 'blur' },
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

const handleAvatarSuccess = (response: any, file: any) => {
  // 处理响应数据，确保用户信息格式正确
  const userInfo = response.user || response
  authStore.updateUser(userInfo)
  ElMessage.success('头像更新成功')
}

const handleUpdate = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const user = await updateUserProfile(form)
        if (user) {
          authStore.updateUser(user)
          ElMessage.success('更新成功')
        }
      } catch (error) {
        // 错误已在request拦截器中处理
      } finally {
        loading.value = false
      }
    }
  })
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

