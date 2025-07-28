import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import UserDashboard from '../views/UserDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserSummary from '../views/UserSummary.vue'
import AdminSummary from '../views/AdminSummary.vue'
import Search from '../views/Search.vue'
import Users from '../views/Users.vue'
import EditProfile from '../views/EditProfile.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
  // Auth
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },

  // Admin routes
  { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/users', component: Users, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/search', component: Search, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/summary', component: AdminSummary, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/profile', component: EditProfile, meta: { requiresAuth: true, role: 'admin' } },

  // User routes
  { path: '/user', component: UserDashboard, meta: { requiresAuth: true, role: 'user' } },
  { path: '/user/summary', component: UserSummary, meta: { requiresAuth: true, role: 'user' } },
  { path: '/user/profile', component: EditProfile, meta: { requiresAuth: true, role: 'user' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ Navigation Guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  if (to.meta.requiresAuth) {
    if (!token) {
      return next('/login')
    }

    if (to.meta.role && to.meta.role !== user.role) {
      return next('/login') // redirect unauthorized access
    }
  }

  next()
})

export default router
