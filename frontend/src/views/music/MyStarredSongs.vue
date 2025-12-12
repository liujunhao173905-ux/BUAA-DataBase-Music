<template>
  <div class="my-starred-songs">
    <router-link to="/home" style="text-decoration: none; margin-right: 20px;">
      <h1 style="display: inline-block; margin: 0; color: #409eff; margin-bottom: 20px;">音乐平台</h1>
    </router-link>
    
    <el-card class="starred-songs-card">
      <template #header>
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-button type="default" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <h2>我的收藏与关注</h2>
          </div>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="收藏歌曲" name="songs">
        <div class="song-card" v-loading="songsLoading">
          <div v-if="songs.length > 0" class="song-list">
            <el-table
              :data="songs"
              style="width: 100%"
              border
            >
              <el-table-column prop="song_name" label="歌曲名称" width="200">
                <template #default="scope">
                  <span class="song-name" @click="handleSongClick(scope.row)">{{ scope.row.song_name }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="song_singer_name" label="歌手" width="120"></el-table-column>
              <el-table-column prop="song_duration" label="时长" width="100"></el-table-column>
              <el-table-column prop="song_price" label="价格" width="100">
                <template #default="scope">
                  {{ formatPrice(scope.row.song_price) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button
                    type="primary"
                    size="small"
                    :disabled="scope.row.is_bought"
                    @click="handleBuySong(scope.row)"
                  >
                    {{ scope.row.is_bought ? '已购买' : '购买' }}
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    @click="handleRemoveStar(scope.row)"
                  >
                    取消收藏
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          
          <el-empty v-else description="暂无收藏歌曲" />
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="关注歌手" name="following">
        <el-card class="following-card" v-loading="followingLoading">
          <div v-if="followingList.length === 0" class="empty-container">
            <el-empty description="您还没有关注任何歌手" />
          </div>
          <div v-else class="following-container">
            <el-row :gutter="20">
              <el-col
                v-for="singer in followingList"
                :key="singer.user_id"
                :xs="12"
                :sm="8"
                :md="6"
                :lg="4"
              >
                <el-card class="singer-card" hoverable>
                  <el-image
                    :src="singer.user_avatar || ''"
                    fit="cover"
                    class="singer-avatar"
                  >
                    <template #error>
                      <div class="image-slot">
                        <User />
                      </div>
                    </template>
                  </el-image>
                  <div class="singer-info">
                    <h3>{{ singer.user_name }}</h3>
                    <p>歌手</p>
                  </div>
                  <div class="singer-actions">
                    <el-button
                      type="danger"
                      size="small"
                      @click="handleUnfollow(singer)"
                    >
                      取消关注
                    </el-button>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="收藏歌单" name="starred">
        <el-card class="starred-card" v-loading="starredLoading">
          <div v-if="starredList.length === 0" class="empty-container">
            <el-empty description="您还没有收藏任何歌单" />
          </div>
          <div v-else class="starred-container">
            <el-row :gutter="20">
              <el-col
                v-for="playlist in starredList"
                :key="playlist.playlist_id"
                :xs="12"
                :sm="8"
                :md="6"
                :lg="4"
              >
                <el-card class="playlist-card" hoverable @click="handlePlaylistClick(playlist)">
                  <el-image
                    :src="playlist.playlist_cover || ''"
                    fit="cover"
                    class="playlist-cover"
                  >
                    <template #error>
                      <div class="image-slot">暂无封面</div>
                    </template>
                  </el-image>
                  <div class="playlist-info">
                    <h3>{{ playlist.playlist_name }}</h3>
                    <p>{{ playlist.playlist_description || '暂无描述' }}</p>
                  </div>
                  <div class="playlist-actions">
                    <el-button
                      type="danger"
                      size="small"
                      @click.stop="handleUnstar(playlist)"
                    >
                      取消收藏
                    </el-button>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="starredCurrentPage"
                v-model:page-size="starredPageSize"
                :page-sizes="[10, 20, 50]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="starredTotal"
                @size-change="handleStarredSizeChange"
                @current-change="handleStarredCurrentChange"
              />
            </div>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User, ArrowLeft } from '@element-plus/icons-vue'
import request from '@/api/request'
import { useRouter } from 'vue-router'
import { getMyFollowingSingers, unfollowUser, getMyStarredPlaylists } from '@/api/user'
import { unstarPlaylist } from '@/api/music'
const router = useRouter()

// 收藏歌曲相关
const songsLoading = ref(false)
const songs = ref<any[]>([])

// 关注歌手相关
const followingLoading = ref(false)
const followingList = ref<any[]>([])

// 收藏歌单相关
const starredLoading = ref(false)
const starredList = ref<any[]>([])
const starredCurrentPage = ref(1)
const starredPageSize = ref(10)
const starredTotal = ref(0)

// 标签页
const activeTab = ref('songs')

const formatPrice = (price: any) => {
  const numPrice = Number(price)
  if (!price || isNaN(numPrice)) return '免费'
  return `¥${numPrice.toFixed(2)}`
}

// 加载收藏歌曲
const fetchStarredSongs = async () => {
  songsLoading.value = true
  try {
    const response = await request.get('/music/songs/starred/')
    songs.value = response
  } catch (error) {
    ElMessage.error('加载收藏歌曲失败')
    console.error('Failed to fetch starred songs:', error)
  } finally {
    songsLoading.value = false
  }
}

// 加载关注歌手
const fetchFollowingSingers = async () => {
  followingLoading.value = true
  try {
    const response = await getMyFollowingSingers()
    // 检查响应是否包含results属性
    followingList.value = response.results || response
  } catch (error) {
    ElMessage.error('加载关注歌手失败')
    console.error('Failed to fetch following singers:', error)
  } finally {
    followingLoading.value = false
  }
}

// 加载收藏歌单
const fetchStarredPlaylists = async (page = 1, pageSize = 10) => {
  starredLoading.value = true
  try {
    const response = await getMyStarredPlaylists(page, pageSize)
    starredList.value = response.data.playlists
    starredTotal.value = response.data.total
  } catch (error) {
    ElMessage.error('加载收藏歌单失败')
    console.error('Failed to fetch starred playlists:', error)
  } finally {
    starredLoading.value = false
  }
}

// 处理歌曲点击
const handleSongClick = (song: any) => {
  router.push(`/songs/${song.song_id}`)
}

// 处理歌单点击
const handlePlaylistClick = (playlist: any) => {
  router.push(`/playlists/${playlist.playlist_id}`)
}

// 处理购买歌曲
const handleBuySong = async (song: any) => {
  try {
    await request.post(`/music/songs/${song.song_id}/buy/`)
    song.is_bought = true
    ElMessage.success('购买成功')
  } catch (error: any) {
    const errorMessage = error.response?.data?.error || '购买失败'
    ElMessage.error(errorMessage)
  }
}

// 处理取消收藏歌曲
const handleRemoveStar = async (song: any) => {
  try {
    await request.delete(`/music/songs/${song.song_id}/unstar/`)
    const index = songs.value.findIndex(s => s.song_id === song.song_id)
    if (index > -1) {
      songs.value.splice(index, 1)
    }
    ElMessage.success('取消收藏成功')
  } catch (error) {
    ElMessage.error('取消收藏失败')
  }
}

// 处理取消关注歌手
const handleUnfollow = async (singer: any) => {
  try {
    await unfollowUser(singer.user_id)
    const index = followingList.value.findIndex(s => s.user_id === singer.user_id)
    if (index > -1) {
      followingList.value.splice(index, 1)
    }
    ElMessage.success('已取消关注')
  } catch (error) {
    ElMessage.error('取消关注失败')
    console.error('Failed to unfollow singer:', error)
  }
}

// 处理取消收藏歌单
const handleUnstar = async (playlist: any) => {
  try {
    await unstarPlaylist(playlist.playlist_id)
    const index = starredList.value.findIndex(p => p.playlist_id === playlist.playlist_id)
    if (index > -1) {
      starredList.value.splice(index, 1)
      starredTotal.value--
    }
    ElMessage.success('已取消收藏歌单')
  } catch (error) {
    ElMessage.error('取消收藏歌单失败')
    console.error('Failed to unstar playlist:', error)
  }
}

// 处理关注歌手分页
// const handleFollowingPageChange = (page: number) => {
//   console.log('Following page changed:', page)
// }

// 处理收藏歌单分页
const handleStarredSizeChange = (size: number) => {
  starredPageSize.value = size
  fetchStarredPlaylists(1, size)
}

const handleStarredCurrentChange = (page: number) => {
  starredCurrentPage.value = page
  fetchStarredPlaylists(page, starredPageSize.value)
}

// 处理标签页切换
const handleTabChange = (tab: string) => {
  if (tab === 'following' && followingList.value.length === 0) {
    fetchFollowingSingers()
  }
  if (tab === 'starred' && starredList.value.length === 0) {
    fetchStarredPlaylists()
  }
}

// 返回
const handleBack = () => {
  router.back()
}

// 初始化加载
onMounted(() => {
  fetchStarredSongs()
  fetchFollowingSingers()
  fetchStarredPlaylists()
})
</script>

<style scoped>
.my-starred-songs {
  padding: 24px;
}

.song-card,
.following-card,
.starred-card {
  margin-top: 16px;
}

.song-name {
  cursor: pointer;
  color: #409EFF;
}

.song-name:hover {
  text-decoration: underline;
}

/* 关注歌手样式 */
.following-container {
  padding: 10px 0;
}

.singer-card {
  margin-bottom: 20px;
  height: 280px;
  display: flex;
  flex-direction: column;
}

.singer-avatar {
  width: 100%;
  height: 180px;
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f5f5f5;
  color: #909399;
  font-size: 36px;
}

.singer-info {
  text-align: center;
  padding: 10px 0;
  flex: 1;
}

.singer-info h3 {
  margin: 5px 0;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.singer-info p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.singer-actions {
  text-align: center;
  padding: 10px;
}

/* 收藏歌单样式 */
.starred-container {
  padding: 10px 0;
}

.playlist-card {
  margin-bottom: 20px;
  height: 300px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.playlist-cover {
  width: 100%;
  height: 180px;
}

.playlist-info {
  padding: 10px 0;
  flex: 1;
  overflow: hidden;
}

.playlist-info h3 {
  margin: 5px 0;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.playlist-info p {
  margin: 0;
  font-size: 14px;
  color: #909399;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
}

.playlist-actions {
  text-align: center;
  padding: 10px;
}

/* 空状态样式 */
.empty-container {
  text-align: center;
  padding: 50px 0;
}

/* 分页样式 */
.pagination-container {
  margin-top: 20px;
  text-align: center;
}
</style>