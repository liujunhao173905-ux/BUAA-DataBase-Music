<template>
  <div class="out-container">
    <div class="home-container">
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索歌曲、歌手、歌单..."
          class="search-input"
          @keyup.enter="handleSearch"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <!-- Banner Section -->
      <div class="banner-section" v-if="!loadingSongs && songs.length > 0">
        <el-carousel :interval="4000" type="card" height="220px">
          <el-carousel-item v-for="item in bannerSongs" :key="item.song_id" @click="handleSongClick(item)">
            <div class="banner-item" :style="{ backgroundImage: `url(${item.song_cover})` }">
              <div class="banner-content">
                <h3>{{ item.song_name }}</h3>
                <p>{{ item.song_singer_name }}</p>
              </div>
              <div class="play-icon-overlay" @click.stop="handlePlay(item)">
                <el-icon><VideoPlay /></el-icon>
              </div>
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>

      <div class="section">
        <div class="section-header">
          <div class="title-with-icon">
            <el-icon class="section-icon" color="#F56C6C"><Headset /></el-icon>
            <h2>推荐歌曲</h2>
          </div>
          <span class="more" @click="$router.push('/songs')">更多 <el-icon><ArrowRight /></el-icon></span>
        </div>
        <div class="scroll-container" v-loading="loadingSongs">
          <div 
            v-for="song in songs.slice(0, 6)" 
            :key="song.song_id" 
            class="scroll-item song-item"
            @click="handleSongClick(song)"
          >
            <div class="image-wrapper">
              <el-image :src="song.song_cover" class="cover" fit="cover" lazy>
                <template #error>
                  <div class="image-placeholder"><el-icon><Headset /></el-icon></div>
                </template>
              </el-image>
              <div class="play-overlay" @click.stop="handlePlay(song)">
                <el-icon><VideoPlay /></el-icon>
              </div>
            </div>
            <div class="info">
              <div class="name text-ellipsis">{{ song.song_name }}</div>
              <div class="singer text-ellipsis">{{ song.song_singer_name }}</div>
            </div>
          </div>
          <el-empty v-if="!loadingSongs && songs.length === 0" description="暂无推荐" />
        </div>
      </div>

      <div class="section">
        <div class="section-header">
          <div class="title-with-icon">
            <el-icon class="section-icon" color="#67C23A"><Timer /></el-icon>
            <h2>最新发布</h2>
          </div>
          <span class="more" @click="$router.push('/songs')">更多 <el-icon><ArrowRight /></el-icon></span>
        </div>
        <div class="scroll-container" v-loading="loadingNewSongs">
          <div 
            v-for="song in newSongs.slice(0, 6)" 
            :key="song.song_id" 
            class="scroll-item song-item"
            @click="handleSongClick(song)"
          >
            <div class="image-wrapper">
              <el-image :src="song.song_cover" class="cover" fit="cover" lazy>
                <template #error>
                  <div class="image-placeholder"><el-icon><Headset /></el-icon></div>
                </template>
              </el-image>
              <div class="play-overlay" @click.stop="handlePlay(song)">
                <el-icon><VideoPlay /></el-icon>
              </div>
            </div>
            <div class="info">
              <div class="name text-ellipsis">{{ song.song_name }}</div>
              <div class="singer text-ellipsis">{{ song.song_singer_name }}</div>
            </div>
          </div>
          <el-empty v-if="!loadingNewSongs && newSongs.length === 0" description="暂无最新歌曲" />
        </div>
      </div>

      <div class="section">
        <div class="section-header">
          <div class="title-with-icon">
            <el-icon class="section-icon" color="#E6A23C"><Collection /></el-icon>
            <h2>推荐歌单</h2>
          </div>
          <span class="more" @click="$router.push('/songs?searchType=playlist')">更多 <el-icon><ArrowRight /></el-icon></span>
        </div>
        <div class="scroll-container" v-loading="loadingPlaylists">
          <div 
            v-for="playlist in playlists.slice(0, 6)" 
            :key="playlist.playlist_id" 
            class="scroll-item playlist-item"
            @click="handlePlaylistClick(playlist)"
          >
            <div class="image-wrapper">
              <el-image :src="playlist.playlist_cover" class="cover" fit="cover" lazy>
                <template #error>
                  <div class="image-placeholder"><el-icon><Collection /></el-icon></div>
                </template>
              </el-image>
              <div class="play-overlay">
                <el-icon><View /></el-icon>
              </div>
            </div>
            <div class="info">
              <div class="name text-ellipsis">{{ playlist.playlist_name }}</div>
              <div class="count text-ellipsis">{{ playlist.song_count || 0 }}首</div>
            </div>
          </div>
          <el-empty v-if="!loadingPlaylists && playlists.length === 0" description="暂无推荐" />
        </div>
      </div>

      <!-- 推荐歌手 Section -->
      <div class="section">
        <div class="section-header">
          <div class="title-with-icon">
            <el-icon class="section-icon" color="#409EFF"><Mic /></el-icon>
            <h2>热门歌手</h2>
          </div>
          <!-- <span class="more">更多 <el-icon><ArrowRight /></el-icon></span> -->
        </div>
        <div class="scroll-container" v-loading="loadingSingers">
          <div 
            v-for="singer in singers.slice(0, 6)" 
            :key="singer.user_id" 
            class="scroll-item singer-item"
            @click="handleSingerClick(singer)"
          >
            <div class="image-wrapper round">
              <el-image :src="singer.user_avatar" class="cover" fit="cover" lazy>
                <template #error>
                  <div class="image-placeholder"><el-icon><User /></el-icon></div>
                </template>
              </el-image>
            </div>
            <div class="info">
              <div class="name text-ellipsis">{{ singer.user_name }}</div>
              <div class="count text-ellipsis">粉丝: {{ singer.followers_count || 0 }}</div>
            </div>
          </div>
          <el-empty v-if="!loadingSingers && singers.length === 0" description="暂无推荐" />
        </div>
        <!-- <div class="pagination-wrapper" v-if="singerTotal > 0">
          <el-pagination
            v-model:current-page="singerPage"
            :page-size="singerPageSize"
            :total="singerTotal"
            layout="prev, pager, next"
            @current-change="handleSingerPageChange"
            background
            small
          />
        </div> -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, ArrowRight, Headset, Collection, VideoPlay, View, Mic, User, Timer } from '@element-plus/icons-vue'
import { getRecommendSongs, getRecommendPlaylists, getSongs, type Song, type Playlist } from '@/api/music'
import { getSingers, type UserInfo } from '@/api/user'
import { usePlayerStore } from '@/stores/player'

const router = useRouter()
const playerStore = usePlayerStore()

const searchKeyword = ref('')
const songs = ref<Song[]>([])
const newSongs = ref<Song[]>([])
const playlists = ref<Playlist[]>([])
const singers = ref<UserInfo[]>([])
const loadingSongs = ref(false)
const loadingNewSongs = ref(false)
const loadingPlaylists = ref(false)
const loadingSingers = ref(false)
const singerPage = ref(1)
const singerTotal = ref(0)
const singerPageSize = 10

const bannerSongs = computed(() => songs.value.slice(0, 5))

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({ name: 'SongList', query: { search: searchKeyword.value } })
  }
}

const handleSongClick = (song: Song) => {
  router.push(`/songs/${song.song_id}`)
}

const handlePlay = (song: Song) => {
  playerStore.setPlaylist([song])
  playerStore.playSong(song)
}

const handlePlaylistClick = (playlist: Playlist) => {
  router.push(`/playlists/${playlist.playlist_id}`)
}

const handleSingerClick = (singer: UserInfo) => {
  router.push(`/user/${singer.user_id}`)
}

const loadSingersData = async () => {
  loadingSingers.value = true
  try {
    const res = await getSingers(singerPage.value, singerPageSize)
    singers.value = res.results || []
    singerTotal.value = res.count || 0
  } catch (error) {
    console.error('Failed to load singers', error)
  } finally {
    loadingSingers.value = false
  }
}

// const handleSingerPageChange = (page: number) => {
//   singerPage.value = page
//   loadSingersData()
// }

const loadData = async () => {
  loadingSongs.value = true
  try {
    songs.value = await getRecommendSongs()
  } catch (error) {
    console.error('Failed to load songs', error)
  } finally {
    loadingSongs.value = false
  }

  loadingNewSongs.value = true
  try {
    const res = await getSongs({ ordering: '-song_createtime', page_size: 10 })
    newSongs.value = res.results || []
  } catch (error) {
    console.error('Failed to load new songs', error)
  } finally {
    loadingNewSongs.value = false
  }

  loadingPlaylists.value = true
  try {
    const res = await getRecommendPlaylists()
    playlists.value = res.data.playlists
  } catch (error) {
    console.error('Failed to load playlists', error)
  } finally {
    loadingPlaylists.value = false
  }

  loadSingersData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.out-container {
  background-color: #f5f5f5;
}

.home-container {
  padding: 25px;
  padding-bottom: 80px;
  max-width: 1030px;
  background-color: #f5f5f5;
  min-height: 100vh;
  box-sizing: border-box;
  margin: 0 auto;
}

.search-bar {
  margin-bottom: 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #f5f5f5; /* Match page bg if needed, or white */
  padding: 10px 0;
  backdrop-filter: blur(10px);
}

.section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.title-with-icon {
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-icon {
  font-size: 20px;
}

.section-header h2 {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin: 0;
}

.more {
  font-size: 14px;
  color: #909399;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.scroll-container {
  display: flex;
  overflow-x: auto;
  gap: 24px;
  padding-bottom: 10px;
  scrollbar-width: none; /* Firefox */
}

.scroll-container::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

.scroll-item {
  flex: 0 0 140px;
  width: 140px;
  max-width: 140px;
  cursor: pointer;
  transition: transform 0.2s;
  overflow: hidden;
}

.scroll-item:hover {
  transform: translateY(-5px);
}

.image-wrapper {
  position: relative;
  width: 140px;
  height: 140px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.image-wrapper.round {
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.cover {
  width: 100%;
  height: 100%;
  transition: transform 0.3s;
}

.scroll-item:hover .cover {
  transform: scale(1.1);
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f2f5;
  color: #909399;
  font-size: 32px;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.play-overlay .el-icon {
  font-size: 32px;
  color: #fff;
}

.scroll-item:hover .play-overlay {
  opacity: 1;
}

.info .name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
  margin-bottom: 4px;
}

.info .singer, .info .count {
  font-size: 12px;
  color: #909399;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Banner Styles */
.banner-section {
  margin-bottom: 30px;
}

.banner-item {
  height: 100%;
  background-size: cover;
  background-position: center;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
}

.banner-content {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 20px;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  color: #fff;
}

.banner-content h3 {
  margin: 0 0 5px 0;
  font-size: 18px;
}

.banner-content p {
  margin: 0;
  font-size: 14px;
  opacity: 0.8;
}

.play-icon-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 48px;
  color: rgba(255,255,255,0.8);
  opacity: 0;
  transition: opacity 0.3s;
}

.banner-item:hover .play-icon-overlay {
  opacity: 1;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}
</style>
