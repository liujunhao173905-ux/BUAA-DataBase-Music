<template>
  <div class="layout-container">
    <div class="main-content" :class="{ 'has-player': playerStore.currentSong }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>

    <GlobalPlayer />

    <div class="bottom-nav">
      <router-link to="/home" class="nav-item" :class="{ active: $route.path.startsWith('/home') }">
        <el-icon><HomeFilled /></el-icon>
        <span>首页</span>
      </router-link>
      <router-link to="/mine" class="nav-item" :class="{ active: $route.path.startsWith('/mine') }">
        <el-icon><UserFilled /></el-icon>
        <span>我的</span>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { HomeFilled, UserFilled } from '@element-plus/icons-vue'
import GlobalPlayer from '@/components/GlobalPlayer.vue'
import { usePlayerStore } from '@/stores/player'

const playerStore = usePlayerStore()
</script>

<style scoped>
.layout-container {
  flex-direction: column;
  height: 100vh;
  background-color: transparent;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 60px; /* Space for bottom nav */
}

.main-content.has-player {
  padding-bottom: 120px; /* Space for bottom nav + player */
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 1000;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: #909399;
  font-size: 12px;
  width: 50%;
  height: 100%;
  transition: color 0.3s;
}

.nav-item .el-icon {
  font-size: 24px;
  margin-bottom: 4px;
}

.nav-item.active {
  color: #409eff;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
