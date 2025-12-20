<template>
  <div class="global-player" v-if="playerStore.currentSong">
    <div class="player-content">
      <div class="song-info" @click="toDetail">
        <el-image :src="playerStore.currentSong.song_cover" class="mini-cover" fit="cover">
          <template #error>
            <div class="image-slot">
              <el-icon><Headset /></el-icon>
            </div>
          </template>
        </el-image>
        <div class="text-info">
          <div class="song-name">{{ playerStore.currentSong.song_name }}</div>
          <div class="singer-name">{{ playerStore.currentSong.song_singer_name }}</div>
        </div>
      </div>
      
      <div class="controls">
        <el-icon class="control-icon" @click="playerStore.playPrev"><ArrowLeft /></el-icon>
        <el-icon class="control-icon play-btn" @click="playerStore.togglePlay">
          <VideoPause v-if="playerStore.isPlaying" />
          <VideoPlay v-else />
        </el-icon>
        <el-icon class="control-icon" @click="playerStore.playNext"><ArrowRight /></el-icon>
      </div>

      <div class="progress-bar">
        <el-slider 
          v-model="currentTime" 
          :max="playerStore.duration" 
          :show-tooltip="false" 
          @change="handleSeek" 
          @input="onStartDrag" 
          size="small"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { usePlayerStore } from '@/stores/player'
import { Headset, ArrowLeft, ArrowRight, VideoPlay, VideoPause } from '@element-plus/icons-vue'

const router = useRouter()
const playerStore = usePlayerStore()

const currentTime = ref(0)
const isDragging = ref(false)

watch(() => playerStore.currentTime, (val) => {
  if (!isDragging.value) {
    currentTime.value = val
  }
})

const onStartDrag = () => {
  isDragging.value = true
}

const handleSeek = (val: number) => {
  playerStore.seek(val)
  // 延迟一小会儿释放锁定，防止进度回弹闪烁
  setTimeout(() => {
    isDragging.value = false
  }, 100)
}

const toDetail = () => {
  if (playerStore.currentSong) {
    router.push(`/songs/${playerStore.currentSong.song_id}`)
  }
}
</script>

<style scoped>
.global-player {
  position: fixed;
  bottom: 60px; /* Above bottom nav */
  left: 0;
  width: 100%;
  height: 60px;
  background: white;
  border-top: 1px solid #eee;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  z-index: 999;
  padding: 0 16px;
}

.player-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  position: relative;
}

.song-info {
  display: flex;
  align-items: center;
  flex: 1;
  overflow: hidden;
  cursor: pointer;
}

.mini-cover {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  margin-right: 10px;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-info {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.song-name {
  font-size: 14px;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.singer-name {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.control-icon {
  font-size: 24px;
  color: #606266;
  cursor: pointer;
}

.play-btn {
  font-size: 32px;
  color: #409eff;
}

.progress-bar {
  position: absolute;
  top: -12px;
  left: 0;
  width: 100%;
}

:deep(.el-slider__button-wrapper) {
  display: none;
}

:deep(.el-slider__bar) {
  background-color: #409eff;
}
</style>
