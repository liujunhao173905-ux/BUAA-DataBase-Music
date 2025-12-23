<template>
  <div class="following-container">
    <el-card class="following-card" shadow="never">
      <template #header>
        <el-page-header @back="handleBack" content="关注歌手" title="返回" />
      </template>

      <div class="singer-list" v-loading="loading">
        <el-table :data="singers" stripe style="width: 100%" @row-click="handleSingerClickRow">
          <el-table-column type="index" width="50" align="center" />
          
          <el-table-column label="歌手" min-width="200">
            <template #default="scope">
              <div class="singer-info" @click.stop="handleSingerClick(scope.row.user_id)" style="cursor: pointer;">
                <div class="cover-wrapper">
                  <el-image v-if="scope.row.user_avatar" :src="scope.row.user_avatar" class="singer-avatar" fit="cover" />
                  <div v-else class="avatar-placeholder">{{ scope.row.user_name?.charAt(0)?.toUpperCase() }}</div>
                </div>
                <span class="singer-name">{{ scope.row.user_name }}</span>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="user_type_display" label="身份" width="150" align="center">
            <template #default="scope">
              <el-tag size="small" type="success">{{ scope.row.user_type_display || '歌手' }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column label="关注时间" width="180" align="center">
             <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
             </template>
          </el-table-column>

          <el-table-column label="操作" width="150" fixed="right" align="center">
            <template #default="scope">
              <el-button 
                type="primary" 
                plain 
                size="small" 
                @click.stop="handleUnfollow(scope.row)"
              >
                已关注
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-empty v-if="!loading && singers.length === 0" description="暂无关注的歌手" />
      </div>

      <div class="pagination-container" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMyFollowingSingers, unfollowUser } from '@/api/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const singers = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchSingers = async () => {
  loading.value = true
  try {
    const res = await getMyFollowingSingers(currentPage.value, pageSize.value)
    if (res && res.results) {
        singers.value = res.results
        total.value = res.count || 0
    } else {
        singers.value = []
        total.value = 0
    }
  } catch (error) {
    console.error('Failed to fetch singers:', error)
    ElMessage.error('获取关注列表失败')
  } finally {
    loading.value = false
  }
}

const handleBack = () => {
  router.push('/mine')
}

const handleSingerClick = (id: number) => {
  router.push(`/user/${id}`)
}

const handleSingerClickRow = (row: any) => {
  handleSingerClick(row.user_id)
}

const handleUnfollow = async (singer: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消关注 ${singer.user_name} 吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await unfollowUser(singer.user_id)
    ElMessage.success('已取消关注')
    fetchSingers() // Refresh list
  } catch (error: any) {
    if (error !== 'cancel') {
        ElMessage.error('操作失败')
    }
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchSingers()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  fetchSingers()
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return isNaN(date.getTime()) ? '-' : date.toLocaleDateString()
}

onMounted(() => {
  fetchSingers()
})
</script>

<style scoped>
.following-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.following-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

:deep(.el-table) {
  background-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(255, 255, 255, 0.5);
  --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.5);
}

:deep(.el-table th.el-table__cell) {
  background-color: rgba(255, 255, 255, 0.5);
}

.singer-info {
  display: flex;
  align-items: center;
  padding: 4px 0;
  transition: transform 0.2s;
}

.singer-info:hover {
  transform: translateX(4px);
}

.cover-wrapper {
  position: relative;
  width: 48px;
  height: 48px;
  margin-right: 16px;
  border-radius: 50%; /* Circle for avatar */
  overflow: hidden;
  flex-shrink: 0;
  border: 2px solid rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(245, 247, 250, 0.5);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.singer-avatar {
  width: 100%;
  height: 100%;
  display: block;
  transition: transform 0.3s;
}

.cover-wrapper:hover .singer-avatar {
  transform: scale(1.1);
}

.avatar-placeholder {
  color: #909399;
  font-weight: bold;
  font-size: 18px;
}

.singer-name {
  font-weight: 600;
  color: #303133;
  font-size: 15px;
}

.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>
