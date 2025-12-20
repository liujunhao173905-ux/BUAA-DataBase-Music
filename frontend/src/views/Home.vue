<template>
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
      <el-carousel :interval="4000" type="card" height="150px">
        <el-carousel-item v-for="item in bannerSongs" :key="item.song_id" @click="handleSongClick(item)">
          <div class="banner-item" :style="{ backgroundImage: `url(${item.song_cover})` }">
            <div class="banner-content">
              <h3>{{ item.song_name }}</h3>
              <p>{{ item.song_singer_name }}</p>
            </div>
            <div class="play-icon-overlay">
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
          v-for="song in songs" 
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
            <div class="play-overlay">
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
          <el-icon class="section-icon" color="#E6A23C"><Collection /></el-icon>
          <h2>推荐歌单</h2>
        </div>
        <span class="more" @click="$router.push('/songs?searchType=playlist')">更多 <el-icon><ArrowRight /></el-icon></span>
      </div>
      <div class="scroll-container" v-loading="loadingPlaylists">
         <div 
          v-for="playlist in playlists" 
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, ArrowRight, Headset, Collection, VideoPlay, View } from '@element-plus/icons-vue'
import { getRecommendSongs, getRecommendPlaylists, type Song, type Playlist } from '@/api/music'
import { usePlayerStore } from '@/stores/player'

const router = useRouter()
const playerStore = usePlayerStore()

const searchKeyword = ref('')
const songs = ref<Song[]>([])
const playlists = ref<Playlist[]>([])
const loadingSongs = ref(false)
const loadingPlaylists = ref(false)

const bannerSongs = computed(() => songs.value.slice(0, 5))

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({ name: 'SongList', query: { search: searchKeyword.value } })
  }
}

const handleSongClick = (song: Song) => {
  playerStore.setPlaylist([song])
  playerStore.playSong(song)
}

const handlePlaylistClick = (playlist: Playlist) => {
  router.push(`/playlists/${playlist.playlist_id}`)
}

const loadData = async () => {
  loadingSongs.value = true
  try {
    songs.value = await getRecommendSongs()
  } catch (error) {
    console.error('Failed to load songs', error)
    // ElMessage.error('加载推荐歌曲失败')
  } finally {
    loadingSongs.value = false
  }

  loadingPlaylists.value = true
  try {
    const res = await getRecommendPlaylists()
    playlists.value = res.data.playlists
  } catch (error) {
    console.error('Failed to load playlists', error)
    // ElMessage.error('加载推荐歌单失败')
  } finally {
    loadingPlaylists.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.home-container {
  padding: 20px;
  padding-bottom: 80px;
}

.search-bar {
  margin-bottom: 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #f5f5f5;
  padding: 10px 0;
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
  gap: 16px;
  padding-bottom: 10px;
  scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.scroll-item {
  flex: 0 0 120px;
  cursor: pointer;
}

.cover {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  margin-bottom: 8px;
  background-color: #e0e0e0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-placeholder {
  color: #909399;
  font-size: 24px;
}

.info {
  width: 100%;
}

.name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.singer, .count {
  font-size: 12px;
  color: #909399;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.banner-section {
  margin-bottom: 24px;
}

.banner-item {
  height: 100%;
  background-size: cover;
  background-position: center;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
}

.banner-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
}

.banner-content {
  position: absolute;
  bottom: 20px;
  left: 20px;
  color: white;
  z-index: 2;
}

.banner-content h3 {
  margin: 0 0 4px;
  font-size: 18px;
}

.banner-content p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.play-icon-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 40px;
  color: white;
  opacity: 0;
  transition: opacity 0.3s;
  z-index: 2;
}

.banner-item:hover .play-icon-overlay {
  opacity: 1;
}

.title-with-icon {
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-icon {
  font-size: 20px;
}

.image-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 8px;
  border-radius: 8px;
  overflow: hidden;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: white;
  font-size: 24px;
}

.scroll-item:hover .play-overlay {
  opacity: 1;
}
</style>
