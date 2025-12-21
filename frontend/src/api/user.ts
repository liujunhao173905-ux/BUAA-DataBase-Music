/**
 * 用户相关API
 */
import request from './request'
import { Playlist } from './music'

export interface LoginData {
  user_name: string
  password: string
}

export interface RegisterData {
  user_name: string
  user_mobile?: string
  password: string
  password_confirm: string
  user_type?: number
}

export interface UserInfo {
  user_id: number
  user_name: string
  user_mobile?: string
  user_avatar?: string
  user_createtime: string
  user_type: number
  user_type_display: string
  date_joined: string
  followers_count?: number
  following_count?: number
  user_gender?: 0 | 1 | 2
  user_birth_date?: string
  user_age?: number
  user_balance?: number
}

export interface LoginResponse {
  message: string
  user: UserInfo
  tokens: {
    access: string
    refresh: string
  }
}

// 用户登录
export const login = (data: LoginData) => {
  return request.post<LoginResponse>('/users/login/', data) as unknown as LoginResponse
}

// 用户注册
export const register = (data: RegisterData) => {
  return request.post<LoginResponse>('/users/register/', data) as unknown as LoginResponse
}

// 获取当前用户资料
export const getUserProfile = () => {
  return request.get<UserInfo>('/users/profile/') as unknown as UserInfo
}

// 更新用户资料
export const updateUserProfile = (formData: FormData) => {
  return request.put<UserInfo>('/users/profile/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }) as unknown as UserInfo
}

// 获取指定用户资料
export const getUserDetail = (user_id: number) => {
  return request.get<UserInfo>(`/users/${user_id}/`)
}

// 获取歌手列表
export const getSingers = (page: number = 1, pageSize: number = 10) => {
  return request.get<{ count: number; results: UserInfo[] }>('/users/singers/', { 
    params: { 
      page,
      page_size: pageSize
    } 
  })
}

// 关注用户
export const followUser = (user_id: number) => {
  return request.post(`/users/${user_id}/follow/`)
}

// 取消关注
export const unfollowUser = (user_id: number) => {
  return request.delete(`/users/${user_id}/follow/`)
}

// 获取粉丝列表
export const getFollowers = (user_id: number) => {
  return request.get(`/users/${user_id}/followers/`)
}

// 获取关注列表
export const getFollowing = (user_id: number) => {
  return request.get(`/users/${user_id}/following/`)
}

// 获取我关注的歌手
export const getMyFollowingSingers = (page: number = 1, pageSize: number = 10) => {
  return request.get<{ count: number; results: any[] }>(`/users/me/following/`, { params: { page, page_size: pageSize } })
}

// 获取我收藏的歌单
export const getMyStarredPlaylists = (page: number = 1, pageSize: number = 10) => {
  return request.get<{ count: number; results: Playlist[] }>(`/playlists/my_starred/`, { params: { page, page_size: pageSize } })
    .then(response => {
      // Check if response has results (pagination) or is array
      if (Array.isArray(response)) {
        return {
          data: {
            playlists: response,
            total: response.length
          }
        }
      }
      return {
        data: {
          playlists: (response as any).results || [],
          total: (response as any).count || 0
        }
      }
    })
}

// 取消收藏歌单（从music.ts导入，保持一致）
// export const unstarPlaylist = async (playlistId: number) => {
//   return request({
//     url: `/playlists/${playlistId}/unstar/`,
//     method: 'POST'
//   })
// }

