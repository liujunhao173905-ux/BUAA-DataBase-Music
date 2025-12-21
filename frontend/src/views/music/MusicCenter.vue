<template>
  <div class="center-container">
    <el-card shadow="hover" class="page-card">
      <template #header>
        <el-page-header @back="$router.back()" content="歌曲中心" title="返回" />
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
import { useAuthStore } from '@/stores/auth'
import MyStarredSongs from './MyStarredSongs.vue'
import MySongs from '@/views/user/MySongs.vue'

const authStore = useAuthStore()
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

.actions {
  margin-bottom: 15px;
  display: flex;
  justify-content: flex-end;
}
</style>
