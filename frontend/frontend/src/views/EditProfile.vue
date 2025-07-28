<template>
  <div class="container mt-5">
    <div class="clay-card p-4 mx-auto" style="max-width: 500px;">
      <h3 class="text-white mb-4">✏️ Edit Profile</h3>
      <form @submit.prevent="updateProfile" class="text-white">
        <div class="mb-3">
          <label class="form-label">Email:</label>
          <input v-model="email" class="form-control" type="email" disabled />
        </div>
        <div class="mb-3">
          <label class="form-label">Full Name:</label>
          <input v-model="full_name" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Address:</label>
          <input v-model="address" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Pincode:</label>
          <input v-model="pincode" class="form-control" />
        </div>
        <button class="btn btn-success w-100">Save</button>
      </form>
      <p v-if="message" class="mt-3 text-success">{{ message }}</p>
    </div>
  </div>
</template>



<script setup>
import { ref } from 'vue'

const token = localStorage.getItem('token')
const user = JSON.parse(localStorage.getItem('user') || '{}')

const email = ref(user.email)
const full_name = ref(user.full_name || '')
const address = ref(user.address || '')
const pincode = ref(user.pincode || '')
const message = ref('')

const updateProfile = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/user/update-profile', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        full_name: full_name.value,
        address: address.value,
        pincode: pincode.value
      })
    })

    const data = await res.json()
    // console.log("data:", data)
    if (res.ok) {
      message.value = '✅ Profile updated successfully!'
      localStorage.setItem('user', JSON.stringify({ 
        ...user, 
        full_name: full_name.value, 
        address: address.value, 
        pincode: pincode.value 
      }))
    } else {
      message.value = `❌ ${data.message || 'Failed to update profile'}`
    }
  } catch (error) {
    message.value = '❌ An error occurred while updating profile'
    console.error(error)
  }
}
</script>

<style scoped>
.clay-card {
  background: #2b2b2b;
  border-radius: 16px;
  box-shadow: 8px 8px 20px #1c1c1c, -8px -8px 20px #3c3c3c;
}
</style>
