<template>
  <div class="center-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <el-page-header @back="$router.back()" content="歌单中心" title="返回" />
      </template>
    
      <el-tabs v-model="activeTab" class="custom-tabs">
        <el-tab-pane label="收藏歌单" name="starred">
          <MyStarredPlaylists :is-embedded="true" />
        </el-tab-pane>
        
        <el-tab-pane label="我的歌单" name="my_playlists">
          <MyPlaylists :is-embedded="true" />
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MyStarredPlaylists from './MyStarredPlaylists.vue'
import MyPlaylists from './MyPlaylists.vue'

const activeTab = ref('starred')
</script>

<style scoped>
.center-container {
  padding: 20px;
  min-height: 100vh;
}

.page-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

.header {
  margin-bottom: 20px;
}
</style>
