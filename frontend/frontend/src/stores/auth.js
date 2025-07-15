import { defineStore } from 'pinia'
// Pinia is a state management system used globally in an application.

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  actions: {
    setToken(token) {
    //   this.token = token
      console.log("token in setToken", token)
      localStorage.setItem('token', token)
    },
    setUser(user) {
      this.user = user
      console.log("user in setuser", user)
      localStorage.setItem('user', JSON.stringify(user))
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.clear()
    }
  }
})
