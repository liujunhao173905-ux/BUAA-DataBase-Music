<template>
  <div class="center-container">
    <div class="header">
      <el-page-header @back="$router.back()" content="歌曲中心" />
    </div>
    
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
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import MyStarredSongs from './MyStarredSongs.vue'
import MySongs from '@/views/user/MySongs.vue'

const authStore = useAuthStore()
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

.actions {
  margin-bottom: 15px;
  display: flex;
  justify-content: flex-end;
}
</style>
