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

const routes = [
  // auth
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },

  // Admin routes
  { path: '/admin', component: AdminDashboard },
  { path: '/admin/users', component: Users },
  { path: '/admin/search', component: Search },
  { path: '/admin/summary', component: AdminSummary },
  { path: '/admin/profile', component: EditProfile },

  // User routes
  { path: '/user', component: UserDashboard },
  { path: '/user/summary', component: UserSummary },
  { path: '/user/profile', component: EditProfile },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
