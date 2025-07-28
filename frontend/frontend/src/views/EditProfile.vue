<template>
  <div class="p-6 max-w-md mx-auto">
    <h2 class="text-xl font-bold mb-4">Edit Profile</h2>
    <form @submit.prevent="updateProfile">
      <div class="mb-3">
        <label>Email:</label>
        <input v-model="email" class="input" type="email" disabled />
      </div>
      <div class="mb-3">
        <label>Full Name:</label>
        <input v-model="full_name" class="input" />
      </div>
      <div class="mb-3">
        <label>Address:</label>
        <input v-model="address" class="input" />
      </div>
      <div class="mb-3">
        <label>Pincode:</label>
        <input v-model="pincode" class="input" />
      </div>
      <button class="btn btn-blue" type="submit">Save</button>
    </form>
    <p v-if="message" class="mt-4 text-green-600">{{ message }}</p>
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
.input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
}
.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
}
.btn-blue {
  background-color: #3b82f6;
  color: white;
}
</style>
