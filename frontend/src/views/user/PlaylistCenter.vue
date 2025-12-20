<template>
  <div class="center-container">
    <div class="header">
      <el-page-header @back="$router.back()" content="歌单中心" />
    </div>
    
    <el-tabs v-model="activeTab" class="custom-tabs">
      <el-tab-pane label="收藏歌单" name="starred">
        <MyStarredPlaylists :is-embedded="true" />
      </el-tab-pane>
      
      <el-tab-pane label="我的歌单" name="my_playlists">
        <MyPlaylists :is-embedded="true" />
      </el-tab-pane>
    </el-tabs>
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
  background-color: #fff;
  min-height: 100vh;
}

.header {
  margin-bottom: 20px;
}
</style>
