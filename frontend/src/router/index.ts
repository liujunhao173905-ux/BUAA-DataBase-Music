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
      path: '/playlists/:id',
      name: 'PlaylistDetail',
      component: () => import('@/views/music/PlaylistDetail.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      component: () => import('@/views/Layout.vue'),
      redirect: '/home',
      children: [
        {
          path: 'home',
          name: 'Home',
          component: () => import('@/views/Home.vue'),
        },
        {
          path: 'mine',
          name: 'Mine',
          component: () => import('@/views/Mine.vue'),
        }
      ]
    },
    {
      path: '/my/music',
      name: 'MusicCenter',
      component: () => import('@/views/music/MusicCenter.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/my/playlists-center',
      name: 'PlaylistCenter',
      component: () => import('@/views/user/PlaylistCenter.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/my/following',
      name: 'Following',
      component: () => import('@/views/user/Following.vue'),
      meta: { requiresAuth: true },
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
    // 新增歌单和歌曲相关路由
    {
      path: '/my/playlists',
      name: 'MyPlaylists',
      component: () => import('@/views/user/MyPlaylists.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/my/songs',
      name: 'MySongs',
      component: () => import('@/views/user/MySongs.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/playlists',
      name: 'PlaylistList',
      component: () => import('@/views/music/SongList.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/music/create-playlist',
      name: 'CreatePlaylist',
      component: () => import('@/views/music/CreatePlaylist.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/music/edit-playlist/:id',
      name: 'EditPlaylist',
      component: () => import('@/views/music/EditPlaylist.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/music/upload-song',
      name: 'UploadSong',
      component: () => import('@/views/music/UploadSong.vue'),
      meta: { requiresAuth: true, requiresSinger: true },
    },
    {
      path: '/music/edit-song/:id',
      name: 'EditSong',
      component: () => import('@/views/music/EditSong.vue'),
      meta: { requiresAuth: true, requiresSinger: true },
    },
    // 管理员审核页面
    {
      path: '/admin/dashboard',
      name: 'AdminDashboard',
      component: () => import('@/views/admin/Dashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/admin/check-songs',
      name: 'CheckSongs',
      component: () => import('@/views/admin/CheckSongs.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/admin/check-playlists',
      name: 'CheckPlaylists',
      component: () => import('@/views/admin/CheckPlaylists.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/admin/check-users',
      name: 'CheckUsers',
      component: () => import('@/views/admin/CheckUsers.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/admin/check-history',
      name: 'CheckHistory',
      component: () => import('@/views/admin/CheckHistory.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
  ],
})

// 路由守卫
router.beforeEach((to, _, next) => {
  const authStore = useAuthStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && authStore.isAuthenticated) {
    // 已登录用户访问登录页，重定向到首页
    next({ name: 'Home' })
  } else if (to.meta.requiresAdmin && authStore.user?.user_type !== 2) {
    // 检查是否需要管理员权限
    next({ name: 'Home' })
  } else if (to.meta.requiresSinger && authStore.user?.user_type !== 1) {
    // 检查是否需要歌手权限
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router




