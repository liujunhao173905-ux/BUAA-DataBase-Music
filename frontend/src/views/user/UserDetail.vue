<template>
  <div class="user-detail-page">
    <!-- Dynamic Background -->
    <div class="page-bg" v-if="user"></div>
    <div class="page-bg-overlay"></div>

    <div class="content-wrapper">
      <el-card v-if="user" class="glass-card" :body-style="{ padding: '0' }" shadow="never">
        <template #header>
          <el-page-header 
            @back="handleBack" 
            :content="user.user_type_display === '歌手' ? '歌手详情' : '用户详情'" 
            title="返回" 
          />
        </template>
        
        <!-- 用户头部信息 -->
        <div class="user-profile-header">
          <div class="user-bg-pattern"></div>
          <div class="user-main-info">
            <div class="avatar-wrapper">
              <el-avatar :size="120" :src="user.user_avatar" class="user-avatar">
                {{ user.user_name?.charAt(0)?.toUpperCase() }}
              </el-avatar>
            </div>
            
            <div class="info-content">
              <div class="name-row">
                <h1 class="user-name">{{ user.user_name }}</h1>
                <el-tag :type="getUserTypeTag(user.user_type)" effect="dark" size="small" class="role-tag">
                  {{ user.user_type_display }}
                </el-tag>
                <el-icon v-if="user.user_gender === 1" class="gender-icon male"><Male /></el-icon>
                <el-icon v-if="user.user_gender === 2" class="gender-icon female"><Female /></el-icon>
              </div>
              
              <div class="stats-row">
                <div class="stat-item">
                  <span class="count">{{ user.followers_count || 0 }}</span>
                  <span class="label">粉丝</span>
                </div>
                <el-divider direction="vertical" />
                <div class="stat-item">
                  <span class="count">{{ user.following_count || 0 }}</span>
                  <span class="label">关注</span>
                </div>
                <el-divider direction="vertical" />
                <div class="stat-item">
                  <span class="label">加入时间: {{ formatDate(user.date_joined) }}</span>
                </div>
              </div>

              <div class="action-row">
                <el-button
                  v-if="authStore.isAuthenticated && authStore.user?.user_id !== user.user_id"
                  :type="isFollowing ? 'default' : 'primary'"
                  :icon="isFollowing ? Check : Plus"
                  round
                  @click="handleFollow"
                  class="action-btn"
                >
                  {{ isFollowing ? '已关注' : '关注' }}
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 内容标签页 -->
        <div class="user-content-tabs">
          <el-tabs v-model="activeTab" class="custom-tabs">
            <el-tab-pane label="创建的歌单" name="playlists">
              <div class="tab-pane-content" v-loading="loadingPlaylists">
                <div v-if="playlists.length > 0" class="playlist-grid">
                  <div 
                    v-for="playlist in playlists" 
                    :key="playlist.playlist_id" 
                    class="playlist-item"
                    @click="router.push(`/playlists/${playlist.playlist_id}`)"
                  >
                    <div class="playlist-cover-wrapper">
                      <el-image :src="playlist.playlist_cover" fit="cover" class="playlist-cover">
                        <template #error>
                          <div class="image-slot"><el-icon><Collection /></el-icon></div>
                        </template>
                      </el-image>
                      <div class="play-count">
                        <el-icon><Headset /></el-icon> {{ playlist.song_count }}首
                      </div>
                      <div class="hover-overlay">
                         <el-icon><VideoPlay /></el-icon>
                      </div>
                    </div>
                    <div class="playlist-info">
                      <div class="playlist-name" :title="playlist.playlist_name">{{ playlist.playlist_name }}</div>
                      <div class="playlist-date">{{ formatDate(playlist.playlist_createtime) }}</div>
                    </div>
                  </div>
                </div>
                <el-empty v-else description="暂无公开歌单" />
              </div>
            </el-tab-pane>

            <el-tab-pane v-if="user.user_type === 1" label="发布的歌曲" name="songs">
              <div class="tab-pane-content" v-loading="loadingSongs">
                <div v-if="songs.length > 0" class="section-actions" style="margin-bottom: 20px;">
                  <el-button type="primary" :icon="VideoPlay" round @click="handlePlayAll">播放全部</el-button>
                </div>
                <el-table 
                  v-if="songs.length > 0" 
                  :data="songs" 
                  class="transparent-table"
                  :row-class-name="tableRowClassName"
                  style="width: 100%" 
                  @row-dblclick="handlePlaySong"
                >
                  <el-table-column type="index" width="60" align="center" />
                  <el-table-column prop="song_name" label="歌曲" min-width="200">
                    <template #default="scope">
                      <div class="song-name-cell">
                         <div class="mini-cover-wrapper">
                            <el-image :src="scope.row.song_cover" class="mini-cover" fit="cover" />
                         </div>
                        <span class="name" :class="{ 'active': isPlaying(scope.row) }">{{ scope.row.song_name }}</span>
                        <el-tag v-if="scope.row.song_price > 0" size="small" type="warning" effect="plain" class="vip-tag">VIP</el-tag>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="song_duration" label="时长" width="100">
                    <template #default="scope">
                      <span class="duration">{{ formatDuration(scope.row.song_duration) }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="150" align="right">
                    <template #default="scope">
                      <el-button circle size="small" :icon="VideoPlay" @click.stop="handlePlaySong(scope.row)" class="action-btn-mini" />
                      <el-button circle size="small" :icon="Star" @click.stop="handleStarSong(scope.row)" class="action-btn-mini" />
                    </template>
                  </el-table-column>
                </el-table>
                <el-empty v-else description="暂无发布歌曲" />
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Check, Male, Female, Collection, Headset, VideoPlay, Star } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { usePlayerStore } from '@/stores/player'
import { getUserDetail, followUser, unfollowUser } from '@/api/user'
import { getPlaylists, getSongs, starSong } from '@/api/music'
import type { Playlist, Song } from '@/api/music'
import request from '@/api/request'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const playerStore = usePlayerStore()

const user = ref<any>(null)
const isFollowing = ref(false)
const activeTab = ref('playlists')

const playlists = ref<Playlist[]>([])
const loadingPlaylists = ref(false)

const songs = ref<Song[]>([])
const loadingSongs = ref(false)

onMounted(async () => {
  const userId = parseInt(route.params.id as string)
  if (userId) {
    await loadUserDetail(userId)
    loadPlaylists(userId)
    // 如果是歌手，加载歌曲
    if (user.value?.user_type === 1) {
      loadSongs(userId)
    }
  }
})

// 监听路由变化，重新加载数据
watch(() => route.params.id, async (newId) => {
  if (newId) {
    const userId = parseInt(newId as string)
    await loadUserDetail(userId)
    loadPlaylists(userId)
    if (user.value?.user_type === 1) {
      loadSongs(userId)
    }
  }
})

const loadUserDetail = async (userId: number) => {
  try {
    user.value = await getUserDetail(userId)
    // 检查是否已关注
    if (authStore.isAuthenticated && authStore.user?.user_id !== userId) {
      checkFollowStatus(userId)
    }
  } catch (error) {
    ElMessage.error('加载用户信息失败')
  }
}

const loadPlaylists = async (userId: number) => {
  loadingPlaylists.value = true
  try {
    const res = await getPlaylists({ creator_id: userId })
    playlists.value = res.results || []
  } catch (error) {
    console.error('Failed to load playlists', error)
  } finally {
    loadingPlaylists.value = false
  }
}

const loadSongs = async (userId: number) => {
  loadingSongs.value = true
  try {
    const res = await getSongs({ singer_id: userId })
    songs.value = res.results || []
  } catch (error) {
    console.error('Failed to load songs', error)
  } finally {
    loadingSongs.value = false
  }
}

const checkFollowStatus = async (userId: number) => {
  try {
    const response = await request.get(`/users/${userId}/follow/`)
    isFollowing.value = response.is_following
  } catch (error) {
    console.error('检查关注状态失败:', error)
  }
}

const getUserTypeTag = (type: number) => {
  const tags = ['', 'success', 'danger', 'warning']
  return tags[type] || ''
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString()
}

const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const handleFollow = async () => {
  if (!user.value) return
  
  try {
    if (isFollowing.value) {
      await unfollowUser(user.value.user_id)
      ElMessage.success('取消关注成功')
    } else {
      await followUser(user.value.user_id)
      ElMessage.success('关注成功')
    }
    isFollowing.value = !isFollowing.value
    // 更新粉丝数
    user.value.followers_count += isFollowing.value ? 1 : -1
  } catch (error: any) {
    ElMessage.error(error?.error || '操作失败')
  }
}

const handleBack = () => {
  router.back()
}

const handlePlaySong = (song: Song) => {
  playerStore.playSong(song)
}

const handlePlayAll = () => {
  if (songs.value.length === 0) return
  playerStore.setPlaylist(songs.value)
  playerStore.playSong(songs.value[0])
}

const handleStarSong = async (song: Song) => {
  try {
    await starSong(song.song_id)
    ElMessage.success('收藏成功')
  } catch (error) {
    ElMessage.error('收藏失败')
  }
}

const isPlaying = (song: any) => {
  return playerStore.currentSong?.song_id === song.song_id
}

const tableRowClassName = ({  }: { rowIndex: number }) => {
  return 'transparent-row'
}
</script>

<style scoped>
.user-detail-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
}

.page-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
  z-index: 0;
  filter: blur(100px);
  opacity: 0.5;
}

.page-bg-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255,255,255,0.4);
  z-index: 1;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.75) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  overflow: hidden;
}

:deep(.el-card__header) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 15px 20px;
  background: rgba(255,255,255,0.3);
}

.user-profile-header {
  position: relative;
  background-color: rgba(255,255,255,0.2);
  padding-bottom: 30px;
}

.user-bg-pattern {
  height: 160px;
  background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
  border-radius: 0 0 20px 20px;
  opacity: 0.8;
}

.user-main-info {
  display: flex;
  padding: 0 40px;
  margin-top: -60px;
  position: relative;
  z-index: 1;
}

.avatar-wrapper {
  margin-right: 30px;
  border: 4px solid #fff;
  border-radius: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  background: #fff;
  flex-shrink: 0;
}

.info-content {
  flex: 1;
  padding-top: 70px;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.user-name {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  margin: 0;
}

.gender-icon {
  font-size: 18px;
}
.gender-icon.male { color: #409EFF; }
.gender-icon.female { color: #F56C6C; }

.stats-row {
  display: flex;
  align-items: center;
  gap: 20px;
  color: #606266;
  font-size: 14px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.stat-item .count {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.user-content-tabs {
  padding: 0 20px 20px;
}

/* Custom Tabs */
:deep(.el-tabs__nav-wrap::after) {
  height: 1px;
  background-color: rgba(0,0,0,0.05);
}
:deep(.el-tabs__item) {
  font-size: 16px;
  color: #606266;
}
:deep(.el-tabs__item.is-active) {
  color: #409eff;
  font-weight: 600;
}

.playlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 25px;
  padding: 20px 0;
}

.playlist-item {
  cursor: pointer;
  transition: all 0.3s;
  background: rgba(255,255,255,0.4);
  border-radius: 12px;
  padding: 10px;
  border: 1px solid rgba(255,255,255,0.2);
}

.playlist-item:hover {
  transform: translateY(-5px);
  background: rgba(255,255,255,0.6);
  box-shadow: 0 8px 20px rgba(0,0,0,0.05);
}

.playlist-cover-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 10px;
}

.playlist-cover {
  width: 100%;
  height: 100%;
  transition: transform 0.5s;
}

.playlist-item:hover .playlist-cover {
  transform: scale(1.05);
}

.play-count {
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(0,0,0,0.5);
  color: #fff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 3px;
}

.hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: #fff;
  font-size: 32px;
}

.playlist-item:hover .hover-overlay {
  opacity: 1;
}

.playlist-info {
  padding: 0 5px;
}

.playlist-name {
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.playlist-date {
  font-size: 12px;
  color: #909399;
}

/* Transparent Table Styles */
:deep(.el-table) {
  background-color: transparent !important;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(255, 255, 255, 0.3);
  --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.5) !important;
}

:deep(.el-table th), :deep(.el-table tr) {
  background-color: transparent !important;
}

:deep(.el-table td.el-table__cell), :deep(.el-table th.el-table__cell.is-leaf) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.song-name-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mini-cover-wrapper {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  overflow: hidden;
}

.mini-cover {
  width: 100%;
  height: 100%;
}

.name {
  font-weight: 500;
}
.name.active {
  color: #409eff;
  font-weight: 600;
}

.vip-tag {
  margin-left: 5px;
}

.duration {
  color: #909399;
}

.action-btn-mini {
  background: transparent;
  border: 1px solid #dcdfe6;
}
.action-btn-mini:hover {
  background: #ecf5ff;
  border-color: #c6e2ff;
  color: #409eff;
}

@media (max-width: 768px) {
  .user-main-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 0 20px;
    margin-top: -40px;
  }
  
  .avatar-wrapper {
    margin-right: 0;
    margin-bottom: 15px;
  }
  
  .info-content {
    padding-top: 0;
    width: 100%;
  }
  
  .name-row {
    justify-content: center;
  }
  
  .stats-row {
    justify-content: center;
  }
  
  .action-row {
    display: flex;
    justify-content: center;
    margin-top: 15px;
  }
}
</style>
