<template>
  <div class="mine-container">
    <!-- User Profile Section -->
    <el-card class="profile-card" shadow="hover" :body-style="{ padding: '20px' }" @click="$router.push('/profile')">
      <div class="profile-content">
        <el-avatar :size="64" :src="authStore.user?.user_avatar" class="avatar">
          {{ authStore.user?.user_name?.charAt(0)?.toUpperCase() }}
        </el-avatar>
        <div class="user-info">
          <h2 class="username">{{ authStore.user?.user_name || '未登录' }}</h2>
          <!-- <p class="phone">{{ authStore.user?.user_mobile || '点击登录/注册' }}</p> -->
          <div class="tags">
            <el-tag size="small" v-if="authStore.isSinger" type="success">歌手</el-tag>
            <el-tag size="small" v-if="authStore.isAdmin" type="warning">管理员</el-tag>
            <el-tag size="small" v-if="!authStore.isAuthenticated" type="info">游客</el-tag>
          </div>
        </div>
        <el-icon class="arrow-icon"><ArrowRight /></el-icon>
      </div>
    </el-card>

    <!-- Function Icons Section (Scrollable) -->
    <div class="function-scroll-container" v-if="authStore.isAuthenticated">
      <div class="function-item" @click="$router.push('/my/music')">
        <div class="icon-box heart">
          <el-icon>
            <StarFilled />
          </el-icon> 
        </div>
        <span>歌曲</span>
      </div>
      
      <div class="function-item" @click="$router.push('/my/following')">
        <div class="icon-box star">
          <el-icon><User /></el-icon>
        </div>
        <span>关注歌手</span>
      </div>

      <div class="function-item" @click="$router.push('/my/playlists-center')">
        <div class="icon-box book">
          <el-icon><Collection /></el-icon>
        </div>
        <span>歌单</span>
      </div>

      <div class="function-item" @click="$router.push('/my/bought')">
        <div class="icon-box coin">
          <el-icon><Money /></el-icon>
        </div>
        <span>我的购买</span>
      </div>

      <div class="function-item" @click="$router.push('/my/report')">
        <div class="icon-box chart">
          <el-icon><DataAnalysis /></el-icon>
        </div>
        <span>听歌报告</span>
      </div>

      <div class="function-item" v-if="authStore.isAdmin" @click="$router.push('/admin/dashboard')">
        <div class="icon-box tool">
          <el-icon><Tools /></el-icon>
        </div>
        <span>管理审核</span>
      </div>
    </div>
    
    <div class="login-hint" v-else>
      <el-empty description="请先登录查看更多功能">
        <el-button type="primary" @click="$router.push('/login')">去登录</el-button>
      </el-empty>
    </div>

    <!-- General Services Menu -->
    <div class="menu-list" v-if="authStore.isAuthenticated">
       <el-card class="menu-card" :body-style="{ padding: '0' }">
         <div class="menu-item" @click="handleSetting">
            <div class="menu-left">
               <el-icon class="menu-icon" color="#909399"><Setting /></el-icon>
               <span>设置</span>
            </div>
            <el-icon><ArrowRight /></el-icon>
         </div>
         <div class="menu-item" @click="handleHelp">
            <div class="menu-left">
               <el-icon class="menu-icon" color="#909399"><Service /></el-icon>
               <span>帮助与反馈</span>
            </div>
            <el-icon><ArrowRight /></el-icon>
         </div>
         <div class="menu-item" @click="handleAbout">
            <div class="menu-left">
               <el-icon class="menu-icon" color="#909399"><InfoFilled /></el-icon>
               <span>关于我们</span>
            </div>
            <el-icon><ArrowRight /></el-icon>
         </div>
         <div class="menu-item logout" @click="handleLogout">
            <div class="menu-left">
               <el-icon class="menu-icon" color="#F56C6C"><SwitchButton /></el-icon>
               <span style="color: #F56C6C;">退出登录</span>
            </div>
         </div>
       </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ArrowRight, StarFilled, User, Collection, Money, Tools, Setting, Service, InfoFilled, SwitchButton, DataAnalysis } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const authStore = useAuthStore()
const router = useRouter()

const handleSetting = () => {
  ElMessage.info('功能开发中')
}

const handleHelp = () => {
  ElMessage.info('功能开发中')
}

const handleAbout = () => {
  ElMessage.info('Music System v1.0.0')
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    authStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  }).catch(() => {})
}
</script>

<style scoped>
.mine-container {
  padding: 20px;
  padding-bottom: 80px; /* Space for bottom nav */
}

.profile-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s;
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.profile-card:active {
  transform: scale(0.98);
}

.profile-content {
  display: flex;
  align-items: center;
}

.avatar {
  margin-right: 16px;
  background-color: #409eff;
}

.user-info {
  flex: 1;
}

.username {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.phone {
  margin: 4px 0 8px;
  color: #909399;
  font-size: 14px;
}

.tags {
  display: flex;
  gap: 8px;
}

.arrow-icon {
  color: #c0c4cc;
}

/* Function Scroll Area */
.function-scroll-container {
  display: flex;
  overflow-x: auto;
  gap: 20px;
  padding: 10px 5px;
  margin-bottom: 20px;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
}

.function-scroll-container::-webkit-scrollbar {
  display: none; /* Chrome/Safari/Opera */
}

.function-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 70px;
  cursor: pointer;
}

.icon-box {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 8px;
  font-size: 24px;
  color: white;
  transition: transform 0.2s;
}

.function-item:active .icon-box {
  transform: scale(0.9);
}

.heart { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%); }
.star { background: linear-gradient(120deg, #f6d365 0%, #fda085 100%); }
.book { background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%); }
.coin { background: linear-gradient(120deg, #f093fb 0%, #f5576c 100%); }
.chart { background: linear-gradient(120deg, #a18cd1 0%, #fbc2eb 100%); }
.tool { background: linear-gradient(120deg, #4facfe 0%, #00f2fe 100%); }

.function-item span {
  font-size: 12px;
  color: #606266;
}

.menu-list {
  margin-top: 10px;
}

.menu-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid #f5f7fa;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:active {
  background-color: #f5f7fa;
}

.menu-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.menu-icon {
  font-size: 20px;
}

.menu-item span {
  font-size: 14px;
  color: #303133;
}

.logout {
  justify-content: center;
}

.logout .menu-left {
  justify-content: center;
}
</style>
