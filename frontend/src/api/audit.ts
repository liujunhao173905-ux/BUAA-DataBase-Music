/**
 * 审核系统API
 * 管理歌曲、歌单、用户的审核相关操作
 */
import request from './request'

// 审核状态枚举
export enum CheckStatus {
  PENDING = 0,
  APPROVED = 1,
  REJECTED = 2
}

// 审核类型
export type CheckType = 'song' | 'playlist' | 'user'

// 歌曲审核日志接口
export interface CheckSongLog {
  check_id: number
  check_song: number
  check_song_name: string
  check_song_detail: any
  check_submit_time: string
  check_modify_time: string | null
  check_status: CheckStatus
  check_status_display: string
  check_admin: number | null
  check_admin_name: string | null
  check_comment: string | null
  check_snapshoot_data: any
}

// 歌单审核日志接口
export interface CheckPlaylistLog {
  check_id: number
  check_playlist: number
  check_playlist_name: string
  check_playlist_detail: any
  check_submit_time: string
  check_modify_time: string | null
  check_status: CheckStatus
  check_status_display: string
  check_admin: number | null
  check_admin_name: string | null
  check_comment: string | null
  check_snapshoot_data: any
}

// 用户审核日志接口
export interface CheckUserLog {
  check_id: number
  check_user: number
  check_user_name: string
  check_user_phone: string
  check_user_email: string | null
  check_user_gender: string | null
  check_user_birth: string | null
  check_user_type: number
  check_submit_time: string
  check_modify_time: string | null
  check_status: CheckStatus
  check_status_display: string
  check_admin: number | null
  check_admin_name: string | null
  check_comment: string | null
  check_snapshoot_data: any
}

// 登录日志接口
export interface LoginLog {
  log_id: number
  log_user: number
  log_user_name: string
  log_user_type: number
  log_user_type_display: string
  log_time: string
}

// 审核日志分页响应
export interface CheckLogPaginationResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// 审核操作参数
export interface AuditActionParams {
  checkId: number
  comment?: string
}

// 获取歌曲审核列表
export const getCheckSongs = (params?: any) => {
  return request.get<CheckLogPaginationResponse<CheckSongLog>>('/audit/songs/', { params }) as unknown as CheckLogPaginationResponse<CheckSongLog>
}

// 审核歌曲（通过）
export const approveSong = (params: AuditActionParams) => {
  return request.post<CheckSongLog>(`/audit/songs/${params.checkId}/approve/`, params) as unknown as CheckSongLog
}

// 审核歌曲（拒绝）
export const rejectSong = (params: AuditActionParams) => {
  return request.post<CheckSongLog>(`/audit/songs/${params.checkId}/reject/`, params) as unknown as CheckSongLog
}

// 获取歌单审核列表
export const getCheckPlaylists = (params?: any) => {
  return request.get<CheckLogPaginationResponse<CheckPlaylistLog>>('/audit/playlists/', { params }) as unknown as CheckLogPaginationResponse<CheckPlaylistLog>
}

// 审核歌单（通过）
export const approvePlaylist = (params: AuditActionParams) => {
  return request.post<CheckPlaylistLog>(`/audit/playlists/${params.checkId}/approve/`, params) as unknown as CheckPlaylistLog
}

// 审核歌单（拒绝）
export const rejectPlaylist = (params: AuditActionParams) => {
  return request.post<CheckPlaylistLog>(`/audit/playlists/${params.checkId}/reject/`, params) as unknown as CheckPlaylistLog
}

// 获取用户审核列表
export const getCheckUsers = (params?: any) => {
  return request.get<CheckLogPaginationResponse<CheckUserLog>>('/audit/users/', { params }) as unknown as CheckLogPaginationResponse<CheckUserLog>
}

// 审核用户（通过）
export const approveUser = (params: AuditActionParams) => {
  return request.post<CheckUserLog>(`/audit/users/${params.checkId}/approve/`, params) as unknown as CheckUserLog
}

// 审核用户（拒绝）
export const rejectUser = (params: AuditActionParams) => {
  return request.post<CheckUserLog>(`/audit/users/${params.checkId}/reject/`, params) as unknown as CheckUserLog
}

// 清空歌曲审核
export const clearSong = (params: AuditActionParams) => {
  return request.post<CheckSongLog>(`/audit/songs/${params.checkId}/clear/`, params) as unknown as CheckSongLog
}

// 清空歌单审核
export const clearPlaylist = (params: AuditActionParams) => {
  return request.post<CheckPlaylistLog>(`/audit/playlists/${params.checkId}/clear/`, params) as unknown as CheckPlaylistLog
}

// 清空用户审核
export const clearUser = (params: AuditActionParams) => {
  return request.post<CheckUserLog>(`/audit/users/${params.checkId}/clear/`, params) as unknown as CheckUserLog
}

// 批量清空歌曲审核记录
export const clearAllSongs = () => {
  return request.post<{ message: string; deleted_count: number }>('/audit/songs/clear_all/') as unknown as { message: string; deleted_count: number }
}

// 批量清空歌单审核记录
export const clearAllPlaylists = () => {
  return request.post<{ message: string; deleted_count: number }>('/audit/playlists/clear_all/') as unknown as { message: string; deleted_count: number }
}

// 批量清空用户审核记录
export const clearAllUsers = () => {
  return request.post<{ message: string; deleted_count: number }>('/audit/users/clear_all/') as unknown as { message: string; deleted_count: number }
}

// 获取登录日志列表
export const getLoginLogs = (params?: any) => {
  return request.get<CheckLogPaginationResponse<LoginLog>>('/users/logs/login-logs/', { params }) as unknown as CheckLogPaginationResponse<LoginLog>
}