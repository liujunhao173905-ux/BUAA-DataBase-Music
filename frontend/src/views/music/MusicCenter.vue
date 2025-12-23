<template>
  <div class="center-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <el-page-header @back="handleBack" content="歌曲中心" title="返回" />
      </template>
    
      <el-tabs v-model="activeTab" class="custom-tabs">
        <el-tab-pane label="收藏歌曲" name="starred">
          <div class="tab-content">
            <MyStarredSongs :is-embedded="true" />
          </div>
        </el-tab-pane>
        
        <el-tab-pane v-if="authStore.isSinger" label="我的歌曲" name="my_songs">
          <div class="tab-content">
             <MySongs :is-embedded="true" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import MyStarredSongs from './MyStarredSongs.vue'
import MySongs from '@/views/user/MySongs.vue'

const router = useRouter()
const authStore = useAuthStore()
const activeTab = ref('starred')

const handleBack = () => {
  router.push('/mine')
}
</script>

<style scoped>
/* 1. 最外层容器：固定高度为视口高度，且不可滚动 */
.center-container {
  padding: 40px;
  max-width: 1400px;
  height: 100vh; /* 强制占满屏幕 */
  box-sizing: border-box;
  display: flex; /* 启用 Flex 布局 */
  flex-direction: column;
  overflow: hidden; /* 防止外层出现滚动条 */
  margin: 0 auto; 
  width: 100%;
}

/* 2. 卡片主体：自动占据剩余空间 */
.page-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
  
  flex: 1; /* 关键：撑满 center-container 的剩余高度 */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止卡片被撑大 */
}

/* 3. 穿透修改 Element Plus 卡片内部结构 */
:deep(.el-card__body) {
  flex: 1; /* 撑满卡片剩余空间 */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止内容溢出 */
  padding: 0 20px 20px 20px; /* 调整内边距，根据需要 */
}

/* 4. Tabs 组件：撑满卡片 body */
.custom-tabs {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
}

/* 5. 穿透修改 Tabs 内容区：撑满 Tabs */
:deep(.el-tabs__content) {
  flex: 1;
  overflow: hidden; /* 关键：滚动条应该出现在更里层的组件里，而不是这里 */
  padding: 15px 0 0 0; /* 给 Tab 内容一点顶部间距 */
}

/* 6. Tab Pane 和内部容器：撑满高度 */
:deep(.el-tab-pane), .tab-content {
  height: 100%;
  width: 100%;
}
</style>