/**
 * 认证状态管理
 * 管理用户登录状态和权限
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, register, getUserProfile, type LoginData, type RegisterData, type UserInfo } from '@/api/user'
import { ElMessage } from 'element-plus'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref<string | null>(localStorage.getItem('token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))
  const user = ref<UserInfo | null>(null)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.user_type === 2)
  const isSinger = computed(() => user.value?.user_type === 1)
  const isNormalUser = computed(() => user.value?.user_type === 0)

  // 初始化用户信息
  const initUser = async () => {
    if (token.value) {
      try {
        const userInfo = await getUserProfile()
        user.value = userInfo
      } catch (error) {
        // token可能已过期，清除登录状态
        logout()
      }
    }
  }

  // 登录
  const loginAction = async (data: LoginData) => {
    try {
      const response = await login(data)
      token.value = response.tokens.access
      refreshToken.value = response.tokens.refresh
      user.value = response.user
      
      // 保存到localStorage
      localStorage.setItem('token', response.tokens.access)
      localStorage.setItem('refreshToken', response.tokens.refresh)
      
      ElMessage.success('登录成功')
      return response
    } catch (error: any) {
      ElMessage.error(error?.error || '登录失败')
      throw error
    }
  }

  // 注册
  const registerAction = async (data: RegisterData) => {
    try {
      const response = await register(data)
      token.value = response.tokens.access
      refreshToken.value = response.tokens.refresh
      user.value = response.user
      
      // 保存到localStorage
      localStorage.setItem('token', response.tokens.access)
      localStorage.setItem('refreshToken', response.tokens.refresh)
      
      ElMessage.success('注册成功')
      return response
    } catch (error: any) {
      ElMessage.error(error?.error || '注册失败')
      throw error
    }
  }

  // 登出
  const logout = () => {
    token.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }

  // 更新用户信息
  const updateUser = (userInfo: UserInfo) => {
    user.value = userInfo
  }

  // 初始化时加载用户信息
  if (token.value) {
    initUser()
  }

  return {
    token,
    refreshToken,
    user,
    isAuthenticated,
    isAdmin,
    isSinger,
    isNormalUser,
    loginAction,
    registerAction,
    logout,
    updateUser,
    initUser,
  }
})

