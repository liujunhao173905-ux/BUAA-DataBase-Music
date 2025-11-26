/**
 * 用户相关API
 */
import request from './request'

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
}

export interface LoginResponse {
  message: string
  user: UserInfo
  tokens: {
    access: string
    refresh: string
  }
}

// 用户注册
export const register = (data: RegisterData) => {
  return request.post<LoginResponse>('/users/register/', data)
}

// 用户登录
export const login = (data: LoginData) => {
  return request.post<LoginResponse>('/users/login/', data)
}

// 获取当前用户资料
export const getUserProfile = () => {
  return request.get<UserInfo>('/users/profile/')
}

// 更新用户资料
export const updateUserProfile = (data: Partial<UserInfo>) => {
  return request.put<UserInfo>('/users/profile/', data)
}

// 获取指定用户资料
export const getUserDetail = (user_id: number) => {
  return request.get<UserInfo>(`/users/${user_id}/`)
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

