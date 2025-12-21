<template>
  <div class="admin-dashboard">
    <div class="container">
      <el-card shadow="hover" class="page-card">
        <template #header>
          <el-page-header @back="handleBack" content="管理员仪表板" title="返回" />
        </template>
      
        <div class="stats-cards">
        <div class="stat-card">
          <h3>待审核歌曲</h3>
          <p class="stat-number">{{ pendingSongs }}</p>
          <router-link to="/admin/check-songs?status=0" class="view-link">查看详情</router-link>
        </div>
        
        <div class="stat-card">
          <h3>待审核歌单</h3>
          <p class="stat-number">{{ pendingPlaylists }}</p>
          <router-link to="/admin/check-playlists?status=0" class="view-link">查看详情</router-link>
        </div>
        
        <div class="stat-card">
          <h3>待审核用户</h3>
          <p class="stat-number">{{ pendingUsers }}</p>
          <router-link to="/admin/check-users?status=0" class="view-link">查看详情</router-link>
        </div>
        
        <div class="stat-card">
          <h3>审核历史</h3>
          <p class="stat-number">{{ todayChecked }}</p>
          <router-link to="/admin/check-history" class="view-link">查看历史</router-link>
        </div>
      </div>
      
      <div class="admin-nav">
        <h3>审核管理</h3>
        <ul>
          <li><router-link to="/admin/check-songs">歌曲审核</router-link></li>
          <li><router-link to="/admin/check-playlists">歌单审核</router-link></li>
          <li><router-link to="/admin/check-users">用户审核</router-link></li>
          <li><router-link to="/admin/check-history">审核历史</router-link></li>
          <li><router-link to="/admin/check-login-logs">登录日志</router-link></li>
        </ul>
      </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useAuditStore } from '../../stores/audit'
import { getCheckSongs, getCheckPlaylists, getCheckUsers, CheckStatus } from '@/api/audit'

const authStore = useAuthStore()
const router = useRouter()

// 返回上一页
const handleBack = () => {
  router.back()
}
const auditStore = useAuditStore()

// 统计数据
const pendingSongs = ref(0)
const pendingPlaylists = ref(0)
const pendingUsers = ref(0)
const todayChecked = ref(0)

onMounted(async () => {
  // 检查权限
  if (authStore.user?.user_type !== 2) {
    router.push('/home')
    return
  }
  
  // 获取统计数据
  await loadStatistics()
})

const loadStatistics = async () => {
  try {
    // 使用auditStore获取实际的待审核统计数据
    const counts = await auditStore.fetchPendingCounts()
    pendingSongs.value = counts.songs
    pendingPlaylists.value = counts.playlists
    pendingUsers.value = counts.users
    // 获取审核历史数量
  const historyCounts = await Promise.all([
    getCheckSongs({ status: [CheckStatus.APPROVED, CheckStatus.REJECTED].join(',') }),
    getCheckPlaylists({ status: [CheckStatus.APPROVED, CheckStatus.REJECTED].join(',') }),
    getCheckUsers({ status: [CheckStatus.APPROVED, CheckStatus.REJECTED].join(',') })
  ])
  todayChecked.value = historyCounts.reduce((total, count) => total + count.count, 0)
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.page-title {
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card h3 {
  font-size: 16px;
  color: #666;
  margin-bottom: 10px;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 15px;
}

.view-link {
  display: inline-block;
  color: #3498db;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.view-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

.admin-nav {
  background: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.admin-nav h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
}

.admin-nav ul {
  list-style: none;
  padding: 0;
}

.admin-nav ul li {
  margin-bottom: 10px;
}

.admin-nav ul li a {
  display: block;
  padding: 12px 15px;
  color: #555;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.admin-nav ul li a:hover {
  background: #f5f7fa;
  color: #3498db;
}
</style>