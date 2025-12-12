/**
 * 审核系统状态管理
 * 管理歌曲、歌单、用户的审核相关状态和操作
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  getCheckSongs,
  getCheckPlaylists,
  getCheckUsers,
  approveSong,
  rejectSong,
  clearSong,
  clearAllSongs,
  approvePlaylist,
  rejectPlaylist,
  clearPlaylist,
  clearAllPlaylists,
  approveUser,
  rejectUser,
  clearUser,
  clearAllUsers,
  CheckPlaylistLog,
  CheckUserLog,
  AuditActionParams,
  CheckStatus
} from '@/api/audit'

// 定义审核日志项的基本接口
interface CheckLogItem {
  check_id: number
}

export const useAuditStore = defineStore('audit', () => {
  // 状态
  // 注意：checkSongs 存储的是完整的分页响应对象，而不仅仅是结果数组
  const checkSongs = ref<any>({ results: [], count: 0 })
  const checkPlaylists = ref<CheckPlaylistLog[]>([])
  const checkUsers = ref<CheckUserLog[]>([])
  const pendingCount = ref({
    songs: 0,
    playlists: 0,
    users: 0
  })

  // 获取歌曲审核列表
  const fetchCheckSongs = async (params?: any) => {
    try {
      const response = await getCheckSongs(params)
      // 存储完整的分页响应对象，包括count、next、previous等属性
      const validResponse = response || { results: [], count: 0 }
      checkSongs.value = validResponse
      return validResponse
    } catch (error) {
      ElMessage.error('获取歌曲审核列表失败')
      // 出错时确保本地状态有默认的分页响应结构
      const defaultResponse = { results: [], count: 0 }
      checkSongs.value = defaultResponse
      throw error
    }
  }

  // 获取歌单审核列表
  const fetchCheckPlaylists = async (params?: any) => {
    try {
      const response = await getCheckPlaylists(params)
      checkPlaylists.value = response.results
      return response
    } catch (error) {
      ElMessage.error('获取歌单审核列表失败')
      throw error
    }
  }

  // 获取用户审核列表
  const fetchCheckUsers = async (params?: any) => {
    try {
      const response = await getCheckUsers(params)
      checkUsers.value = response.results
      return response
    } catch (error) {
      ElMessage.error('获取用户审核列表失败')
      throw error
    }
  }

  // 审核歌曲（通过）
  const approveSongAction = async (params: AuditActionParams) => {
    try {
      const response = await approveSong(params)
      ElMessage.success('歌曲审核通过')
      // 更新本地列表中的状态
      const index = checkSongs.value.results.findIndex((item: CheckLogItem) => item.check_id === params.checkId)
      if (index !== -1) {
        checkSongs.value.results[index] = response
      }
      return response
    } catch (error) {
      ElMessage.error('歌曲审核通过失败')
      throw error
    }
  }

  // 审核歌曲（拒绝）
  const rejectSongAction = async (params: AuditActionParams) => {
    try {
      const response = await rejectSong(params)
      ElMessage.success('歌曲审核拒绝')
      // 更新本地列表中的状态
      const index = checkSongs.value.results.findIndex((item: CheckLogItem) => item.check_id === params.checkId)
      if (index !== -1) {
        checkSongs.value.results[index] = response
      }
      return response
    } catch (error) {
      ElMessage.error('歌曲审核拒绝失败')
      throw error
    }
  }

  // 审核歌单（通过）
  const approvePlaylistAction = async (params: AuditActionParams) => {
    try {
      const response = await approvePlaylist(params)
      ElMessage.success('歌单审核通过')
      // 更新本地列表中的状态
      const index = checkPlaylists.value.findIndex(item => item.check_id === params.checkId)
      if (index !== -1) {
        checkPlaylists.value[index] = response
      }
      return response
    } catch (error) {
      ElMessage.error('歌单审核通过失败')
      throw error
    }
  }

  // 审核歌单（拒绝）
  const rejectPlaylistAction = async (params: AuditActionParams) => {
    try {
      const response = await rejectPlaylist(params)
      ElMessage.success('歌单审核拒绝')
      // 更新本地列表中的状态
      const index = checkPlaylists.value.findIndex(item => item.check_id === params.checkId)
      if (index !== -1) {
        checkPlaylists.value[index] = response
      }
      return response
    } catch (error) {
      ElMessage.error('歌单审核拒绝失败')
      throw error
    }
  }

  // 审核用户（通过）
  const approveUserAction = async (params: AuditActionParams) => {
    try {
      const response = await approveUser(params)
      ElMessage.success('用户审核通过')
      // 更新本地列表中的状态
      const index = checkUsers.value.findIndex(item => item.check_id === params.checkId)
      if (index !== -1) {
        checkUsers.value[index] = response
      }
      return response
    } catch (error) {
      ElMessage.error('用户审核通过失败')
      throw error
    }
  }

  // 审核用户（拒绝）
  const rejectUserAction = async (params: AuditActionParams) => {
    try {
      const response = await rejectUser(params)
      ElMessage.success('用户审核拒绝')
      // 更新本地列表中的状态
      const index = checkUsers.value.findIndex(item => item.check_id === params.checkId)
      if (index !== -1) {
        checkUsers.value[index] = response
      }
      return response
    } catch (error) {
      ElMessage.error('用户审核拒绝失败')
      throw error
    }
  }
  
  // 清空歌曲审核
  const clearSongAction = async (params: AuditActionParams) => {
    try {
      const response = await clearSong(params)
      ElMessage.success('歌曲审核已清空')
      // 更新本地列表中的状态
      const index = checkSongs.value.results.findIndex((item: CheckLogItem) => item.check_id === params.checkId)
      if (index !== -1) {
        checkSongs.value.results[index] = response
      }
      return response
    } catch (error) {
      ElMessage.error('清空歌曲审核失败')
      throw error
    }
  }
  
  // 清空歌单审核
  const clearPlaylistAction = async (params: AuditActionParams) => {
    try {
      const response = await clearPlaylist(params)
      ElMessage.success('歌单审核已清空')
      // 更新本地列表中的状态
      const index = checkPlaylists.value.findIndex(item => item.check_id === params.checkId)
      if (index !== -1) {
        checkPlaylists.value[index] = response
      }
      return response
    } catch (error) {
      ElMessage.error('清空歌单审核失败')
      throw error
    }
  }
  
  // 清空用户审核
  const clearUserAction = async (params: AuditActionParams) => {
    try {
      const response = await clearUser(params)
      ElMessage.success('用户审核已清空')
      // 更新本地列表中的状态
      const index = checkUsers.value.findIndex(item => item.check_id === params.checkId)
      if (index !== -1) {
        checkUsers.value[index] = response
      }
      return response
    } catch (error) {
      ElMessage.error('清空用户审核失败')
      throw error
    }
  }
  
  // 批量清空歌曲审核记录
  const clearAllSongsAction = async () => {
    try {
      const response = await clearAllSongs()
      ElMessage.success(response.message)
      // 重新加载歌曲审核列表
      await fetchCheckSongs()
      return response
    } catch (error) {
      ElMessage.error('批量清空歌曲审核记录失败')
      throw error
    }
  }
  
  // 批量清空歌单审核记录
  const clearAllPlaylistsAction = async () => {
    try {
      const response = await clearAllPlaylists()
      ElMessage.success(response.message)
      // 重新加载歌单审核列表
      await fetchCheckPlaylists()
      return response
    } catch (error) {
      ElMessage.error('批量清空歌单审核记录失败')
      throw error
    }
  }
  
  // 批量清空用户审核记录
  const clearAllUsersAction = async () => {
    try {
      const response = await clearAllUsers()
      ElMessage.success(response.message)
      // 重新加载用户审核列表
      await fetchCheckUsers()
      return response
    } catch (error) {
      ElMessage.error('批量清空用户审核记录失败')
      throw error
    }
  }

  // 获取待审核统计
  const fetchPendingCounts = async () => {
    try {
      const [songsRes, playlistsRes, usersRes] = await Promise.all([
        getCheckSongs({ status: CheckStatus.PENDING }),
        getCheckPlaylists({ status: CheckStatus.PENDING }),
        getCheckUsers({ status: CheckStatus.PENDING })
      ])
      
      pendingCount.value = {
        songs: songsRes.count,
        playlists: playlistsRes.count,
        users: usersRes.count
      }
      
      return pendingCount.value
    } catch (error) {
      ElMessage.error('获取待审核统计失败')
      throw error
    }
  }



  return {
    checkSongs,
    checkPlaylists,
    checkUsers,
    pendingCount,
    fetchCheckSongs,
    fetchCheckPlaylists,
    fetchCheckUsers,
    approveSongAction,
    rejectSongAction,
    clearSongAction,
    clearAllSongsAction,
    approvePlaylistAction,
    rejectPlaylistAction,
    clearPlaylistAction,
    clearAllPlaylistsAction,
    approveUserAction,
    rejectUserAction,
    clearUserAction,
    clearAllUsersAction,
    fetchPendingCounts
  }
})