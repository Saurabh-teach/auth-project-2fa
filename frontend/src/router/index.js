import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'   // relative path - working fix

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/2fa-setup',
    component: () => import('../views/Setup2FA.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router