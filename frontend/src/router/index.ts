/**
 * 路由配置
 * 包含路由守卫和权限控制
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/home',
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/auth/Login.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/auth/Register.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/home',
      name: 'Home',
      component: () => import('@/views/Home.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/views/user/Profile.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/user/:id',
      name: 'UserDetail',
      component: () => import('@/views/user/UserDetail.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/songs',
      name: 'SongList',
      component: () => import('@/views/music/SongList.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/songs/:id',
      name: 'SongDetail',
      component: () => import('@/views/music/SongDetail.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/my/starred',
      name: 'MyStarredSongs',
      component: () => import('@/views/music/MyStarredSongs.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/my/bought',
      name: 'MyBoughtSongs',
      component: () => import('@/views/music/MyBoughtSongs.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && authStore.isAuthenticated) {
    // 已登录用户访问登录页，重定向到首页
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router

