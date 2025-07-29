<template>
  <div class="container py-4">
    <h2 class="display-6 text-white mb-4 shadow-text">🛠️ Admin Dashboard</h2>

    <!-- Email Management Section -->
    <div class="clay-card mb-5 p-4">
      <h4 class="mb-3">📧 Email Management</h4>
      <div class="row g-3">
        <!-- Daily Reminders -->
        <div class="col-md-4">
          <div class="email-action-card">
            <div class="email-info mb-2">
              <h5>📅 Daily Reminders</h5>
              <p class="small text-muted">Send reminder emails to all users with active reservations</p>
            </div>
            <button 
              @click="sendDailyReminders" 
              :disabled="dailyLoading"
              class="btn btn-outline-warning w-100"
            >
              <span v-if="dailyLoading">🔄 Sending...</span>
              <span v-else>📤 Send Now</span>
            </button>
          </div>
        </div>

        <!-- Monthly Reports -->
        <div class="col-md-4">
          <div class="email-action-card">
            <div class="email-info mb-2">
              <h5>📊 Monthly Reports</h5>
              <p class="small text-muted">Send monthly activity reports to all users</p>
            </div>
            <button 
              @click="sendMonthlyReports" 
              :disabled="monthlyLoading"
              class="btn btn-outline-info w-100"
            >
              <span v-if="monthlyLoading">🔄 Processing...</span>
              <span v-else>📈 Generate Reports</span>
            </button>
          </div>
        </div>

        <!-- Test Email -->
        <div class="col-md-4">
          <div class="email-action-card">
            <div class="email-info mb-2">
              <h5>🧪 Test Email</h5>
              <p class="small text-muted">Send a test email to verify email system</p>
            </div>
            <button 
              @click="sendTestEmail" 
              :disabled="testLoading"
              class="btn btn-outline-success w-100"
            >
              <span v-if="testLoading">🔄 Testing...</span>
              <span v-else>✉️ Test Email</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Email Status Messages -->
      <div v-if="emailStatus" class="alert mt-3" :class="emailStatusClass">
        {{ emailStatus.message }}
      </div>

      <!-- Active Tasks -->
      <div v-if="activeTasks.length > 0" class="mt-3">
        <h6>⏳ Active Email Tasks</h6>
        <div class="row">
          <div v-for="task in activeTasks" :key="task.id" class="col-md-6 mb-2">
            <div class="task-item d-flex justify-content-between align-items-center p-2 bg-dark rounded">
              <span class="task-name">{{ task.name }}</span>
              <span class="badge" :class="getTaskStatusClass(task.status)">{{ task.status }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

   <!-- Create Lot - Simple & Better -->
<div class="clay-card mb-5 p-4">
  <h4 class="mb-3">🏢 Create New Parking Lot</h4>
  <form @submit.prevent="createLot">
    <div class="row g-3">
      <!-- Lot Name -->
      <div class="col-md-6">
        <label class="form-label text-light">Lot Name *</label>
        <input 
          v-model="newLotName" 
          type="text"
          class="form-control" 
          placeholder="e.g., Downtown Mall Parking"
          required
        />
      </div>

      <!-- Location -->
      <div class="col-md-6">
        <label class="form-label text-light">Location *</label>
        <input 
          v-model="newLotLocation" 
          type="text"
          class="form-control" 
          placeholder="e.g., 123 Main Street"
          required
        />
      </div>

      <!-- Price per Hour -->
      <div class="col-md-6">
        <label class="form-label text-light">Price per Hour (₹) *</label>
        <div class="input-group">
          <span class="input-group-text">₹</span>
          <input 
            v-model.number="newLotPrice" 
            type="number" 
            class="form-control" 
            placeholder="10"
            min="1"
            required
          />
          <span class="input-group-text">/hr</span>
        </div>
      </div>

      <!-- Number of Spots -->
      <div class="col-md-6">
        <label class="form-label text-light">Number of Parking Spots *</label>
        <div class="input-group">
          <input 
            v-model.number="newLotSpots" 
            type="number" 
            class="form-control" 
            placeholder="20"
            min="1"
            required
          />
          <span class="input-group-text">spots</span>
        </div>
      </div>

      <!-- Submit Button -->
      <div class="col-12 text-end">
        <button 
          type="submit" 
          :disabled="createLoading"
          class="btn btn-success"
        >
          <span v-if="createLoading">🔄 Creating...</span>
          <span v-else>✅ Create Lot</span>
        </button>
      </div>
    </div>
  </form>

  <!-- Success/Error Message -->
  <div v-if="createMessage" class="alert mt-3" :class="createMessage.includes('✅') ? 'alert-success' : 'alert-danger'">
    {{ createMessage }}
  </div>
</div>

    <!-- Users -->
    <div class="clay-card mb-5 p-4">
      <h4>👥 All Users</h4>
      <ul class="list-group mt-2">
        <li class="list-group-item bg-dark text-white" v-for="user in users" :key="user.id">
          {{ user.email }} <span class="badge bg-secondary ms-2">{{ user.role }}</span>
        </li>
      </ul>
    </div>

    <!-- Parking Lots -->
    <div class="clay-card mb-4 p-4">
      <h4>🏢 Parking Lots</h4>
      <ul class="list-group mt-2">
        <li class="list-group-item bg-dark text-white" v-for="lot in parkingLots" :key="lot.id">
          <strong>{{ lot.name }}</strong> — {{ lot.location }} (₹{{ lot.price }}/hr)
          <button class="btn btn-sm btn-primary float-end" @click="selectLot(lot)">+ Add Spot</button>
        </li>
      </ul>
    </div>

    <!-- Add Spot -->
    <div v-if="selectedLot" class="clay-card p-4">
      <h5>Add Spot to <span class="text-info">{{ selectedLot.name }}</span></h5>
      <button class="btn btn-purple mt-2" @click="addSpot">+ Add Spot</button>
      <p v-if="addMessage" class="mt-2 text-success">{{ addMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const users = ref([])
const parkingLots = ref([])
const selectedLot = ref(null)
const addMessage = ref('')

const newLotName = ref('')
const newLotLocation = ref('')
const newLotPrice = ref(10)
const newLotSpots = ref(0)

// Email management data
const dailyLoading = ref(false)
const monthlyLoading = ref(false)
const testLoading = ref(false)
const emailStatus = ref(null)
const activeTasks = ref([])

// Computed property for email status styling
const emailStatusClass = computed(() => {
  if (!emailStatus.value) return ''
  return {
    'alert-success': emailStatus.value.type === 'success',
    'alert-danger': emailStatus.value.type === 'error',
    'alert-info': emailStatus.value.type === 'info'
  }
})

const getTaskStatusClass = (status) => {
  switch (status) {
    case 'SUCCESS': return 'bg-success'
    case 'FAILURE': return 'bg-danger'
    case 'PENDING': return 'bg-warning'
    default: return 'bg-secondary'
  }
}

onMounted(() => {
  fetchUsers()
  fetchLots()
})

const fetchUsers = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/api/admin/users', {
    headers: { Authorization: `Bearer ${token}` }
  })
  users.value = await res.json()
}

const fetchLots = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/api/admin/parking-lots', {
    headers: { Authorization: `Bearer ${token}` }
  })
  parkingLots.value = await res.json()
}

const selectLot = (lot) => {
  selectedLot.value = lot
  addMessage.value = ''
}

const addSpot = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/api/admin/parking-spots', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ lot_id: selectedLot.value.id, count: 1 })
  })
  const data = await res.json()
  addMessage.value = res.ok ? '✅ Spot added successfully!' : `❌ ${data.message}`
}

const createLot = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch('http://127.0.0.1:5000/api/admin/parking-lots', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: newLotName.value,
      location: newLotLocation.value,
      price: newLotPrice.value,
      spots: newLotSpots.value
    })
  })

  const data = await res.json()
  if (res.ok) {
    alert('✅ Parking lot created')
    fetchLots()
    newLotName.value = ''
    newLotLocation.value = ''
    newLotPrice.value = 10
  } else {
    alert(`❌ ${data.message || 'Failed to create lot'}`)
  }
}

// Email Management Functions
const sendDailyReminders = async () => {
  dailyLoading.value = true
  emailStatus.value = null
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://127.0.0.1:5000/api/user/test-daily-reminders', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    
    if (response.ok) {
      emailStatus.value = {
        type: 'success',
        message: '✅ Daily reminders initiated! Users with active reservations will receive emails.'
      }
      addActiveTask(data.task_id, 'Daily Reminders')
    } else {
      emailStatus.value = {
        type: 'error',
        message: `❌ Failed: ${data.error || 'Unknown error'}`
      }
    }
  } catch (error) {
    emailStatus.value = {
      type: 'error',
      message: `❌ Network error: ${error.message}`
    }
  } finally {
    dailyLoading.value = false
  }
}

const sendMonthlyReports = async () => {
  monthlyLoading.value = true
  emailStatus.value = null
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://127.0.0.1:5000/api/user/test-all-monthly-reports', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    
    if (response.ok) {
      emailStatus.value = {
        type: 'success',
        message: '✅ Monthly reports generation started! All users will receive their reports.'
      }
      addActiveTask(data.task_id, 'Monthly Reports')
    } else {
      emailStatus.value = {
        type: 'error',
        message: `❌ Failed: ${data.error || 'Unknown error'}`
      }
    }
  } catch (error) {
    emailStatus.value = {
      type: 'error',
      message: `❌ Network error: ${error.message}`
    }
  } finally {
    monthlyLoading.value = false
  }
}

const sendTestEmail = async () => {
  testLoading.value = true
  emailStatus.value = null
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://127.0.0.1:5000/api/user/test-email', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    
    if (response.ok) {
      emailStatus.value = {
        type: 'success',
        message: '✅ Test email sent! Check your inbox.'
      }
    } else {
      emailStatus.value = {
        type: 'error',
        message: `❌ Failed: ${data.error || 'Unknown error'}`
      }
    }
  } catch (error) {
    emailStatus.value = {
      type: 'error',
      message: `❌ Network error: ${error.message}`
    }
  } finally {
    testLoading.value = false
  }
}

const addActiveTask = (taskId, taskName) => {
  const task = {
    id: taskId,
    name: taskName,
    status: 'PENDING'
  }
  activeTasks.value.push(task)
  
  // Monitor task status
  monitorTask(taskId)
}

const monitorTask = async (taskId) => {
  const checkStatus = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`http://127.0.0.1:5000/api/user/email-status/${taskId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      const data = await response.json()
      
      // Update task status
      const taskIndex = activeTasks.value.findIndex(t => t.id === taskId)
      if (taskIndex !== -1) {
        activeTasks.value[taskIndex].status = data.state
        
        // Remove completed tasks after 10 seconds
        if (data.state === 'SUCCESS' || data.state === 'FAILURE') {
          setTimeout(() => {
            const index = activeTasks.value.findIndex(t => t.id === taskId)
            if (index !== -1) {
              activeTasks.value.splice(index, 1)
            }
          }, 10000)
        } else {
          // Check again in 3 seconds
          setTimeout(checkStatus, 3000)
        }
      }
    } catch (error) {
      console.error('Error monitoring task:', error)
    }
  }
  
  // creating a ew parking lot js
  const createLoading = ref(false)
const createMessage = ref('')

// Replace your existing createLot function with this:
const createLot = async () => {
  createLoading.value = true
  createMessage.value = ''
  
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://127.0.0.1:5000/api/admin/parking-lots', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: newLotName.value,
        location: newLotLocation.value,
        price: newLotPrice.value,
        spots: newLotSpots.value
      })
    })

    const data = await res.json()
    if (res.ok) {
      createMessage.value = `✅ "${newLotName.value}" created with ${newLotSpots.value} spots!`
      fetchLots() // Refresh the list
      
      // Clear form
      newLotName.value = ''
      newLotLocation.value = ''
      newLotPrice.value = 10
      newLotSpots.value = 0
    } else {
      createMessage.value = `❌ ${data.message || 'Failed to create lot'}`
    }
  } catch (error) {
    createMessage.value = `❌ Error: ${error.message}`
  } finally {
    createLoading.value = false
  }
}

  // Start monitoring after 2 seconds
  setTimeout(checkStatus, 2000)
}
</script>

<style scoped>
.clay-card {
  background: #2b2b2b;
  border-radius: 16px;
  box-shadow: 8px 8px 20px #1c1c1c, -8px -8px 20px #3c3c3c;
  color: white;
}

.email-action-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 1rem;
  height: 100%;
}

.email-info h5 {
  color: #fff;
  margin-bottom: 0.5rem;
}

.task-item {
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-purple {
  background-color: #7c3aed;
  color: white;
}

.shadow-text {
  text-shadow: 2px 2px 5px #000;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.input-group-text {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: #fff;
}
</style>