<template>
  <div class="home-container">
    <el-container>
      <el-header>
        <div class="header-content">
          <router-link to="/home" style="text-decoration: none;">
            <h1 style="margin: 0; color: #409eff;">音乐平台</h1>
          </router-link>
          <div class="header-actions">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索歌曲、歌手、歌单..."
              class="search-input"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button v-if="!authStore.isAuthenticated" @click="$router.push('/login')">
              登录
            </el-button>
            <el-dropdown v-else>
              <span class="user-info">
                <el-avatar :size="32" :src="authStore.user?.user_avatar" />
                <span>{{ authStore.user?.user_name }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="$router.push('/profile')">个人资料</el-dropdown-item>
                  <el-dropdown-item @click="$router.push('/my/starred')">我的收藏</el-dropdown-item>
                  <el-dropdown-item @click="$router.push('/my/bought')">我的购买</el-dropdown-item>
                  <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <div class="main-content">
          <h2>推荐歌曲</h2>
          <el-row :gutter="20">
            <el-col
              v-for="song in songs"
              :key="song.song_id"
              :xs="12"
              :sm="8"
              :md="6"
              :lg="4"
            >
              <el-card class="song-card" @click="handleSongClick(song)">
                <el-image
                  :src="song.song_cover || ''"
                  fit="cover"
                  class="song-cover"
                >
                  <template #error>
                    <div class="image-slot">暂无封面</div>
                  </template>
                </el-image>
                <div class="song-info">
                  <h3>{{ song.song_name }}</h3>
                  <p>{{ song.song_singer_name }}</p>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import request from '@/api/request'

const router = useRouter()
const authStore = useAuthStore()

const searchKeyword = ref('')
const songs = ref<any[]>([])

onMounted(async () => {
  await loadSongs()
})

const loadSongs = async () => {
  try {
    const response = await request.get('/music/songs/', {
      params: {
        page: 1,
        page_size: 12
      }
    })
    songs.value = response.results || response
  } catch (error) {
    ElMessage.error('加载歌曲失败')
  }
}

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({
      name: 'SongList',
      query: { search: searchKeyword.value }
    })
  }
}

const handleSongClick = (song: any) => {
  router.push(`/songs/${song.song_id}`)
}

const handleLogout = () => {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  color: #409eff;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-input {
  width: 300px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}

.song-card {
  cursor: pointer;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.song-card:hover {
  transform: translateY(-5px);
}

.song-cover {
  width: 100%;
  height: 200px;
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f5f5f5;
  color: #909399;
}

.song-info {
  padding: 10px 0;
}

.song-info h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-info p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}
</style>

