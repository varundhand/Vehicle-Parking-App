<template>
  <div>
    <h2>Welcome, {{ user?.email || 'User' }}!</h2>

    <section>
      <h3>Available Parking Lots</h3>
      <ul>
        <li v-for="lot in parkingLots" :key="lot.id">
          {{ lot.name }} - {{ lot.location }}
        </li>
      </ul>
    </section>

    <button @click="logout">Logout</button>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { onMounted, ref, watchEffect } from 'vue'

const auth = useAuthStore()
const router = useRouter()
const user = auth.user

const parkingLots = ref([])

const fetchParkingLots = async () => {
  try {
    // console.log(auth)
    console.log('This is what I need',localStorage.getItem('token'))
    
    const token = localStorage.getItem('token')
    const res = await fetch('http://127.0.0.1:5000/api/user/parking-lots', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    parkingLots.value = await res.json()
    console.log('✅ Parking lots fetched for user:', parkingLots.value)
  } catch (err) {
    console.error('❌ Failed to fetch parking lots', err)
  }
}

// ✅ Automatically fetch lots when token becomes available
// watchEffect(() => {
//   if (auth.token) {
//     fetchParkingLots()
//   }
// })

onMounted(() => {
  if (!auth.token) {
    auth.token = localStorage.getItem('token')
  }
  fetchParkingLots()
})


const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
