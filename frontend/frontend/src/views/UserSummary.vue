<template>
  <div class="user-summary p-4">
    <div class="clay-card">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="text-light fs-4 fw-bold mb-0">📈 My Parking Summary</h2>
        <button 
          @click="exportData" 
          :disabled="exportLoading"
          class="btn btn-outline-info btn-sm"
        >
          <span v-if="exportLoading">🔄 Exporting...</span>
          <span v-else>📄 Export CSV</span>
        </button>
      </div>
      
      <!-- Export Status -->
      <div v-if="exportStatus" class="alert alert-sm mb-3" :class="exportStatusClass">
        {{ exportStatus.message }}
      </div>
      
      <!-- Chart Section -->
      <section v-if="chartData">
        <Bar :data="chartData" :options="chartOptions" />
      </section>
      <p v-else>No data available</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
} from 'chart.js'

// Register components
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const token = localStorage.getItem('token')
const chartData = ref(null)
const exportLoading = ref(false)
const exportStatus = ref(null)
const taskId = ref(null)

// Computed property for export status styling
const exportStatusClass = computed(() => {
  if (!exportStatus.value) return ''
  return {
    'alert-success': exportStatus.value.type === 'success',
    'alert-danger': exportStatus.value.type === 'error',
    'alert-info': exportStatus.value.type === 'info'
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Reservations by Location' }
  }
}

const fetchUserHistory = async () => {
  const res = await fetch('http://127.0.0.1:5000/api/user/reservations/history', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  const data = await res.json()
  if (Array.isArray(data)) {
    const locationCounts = {}
    data.forEach(entry => {
      const loc = entry.location || 'Unknown'
      locationCounts[loc] = (locationCounts[loc] || 0) + 1
    })
    const labels = Object.keys(locationCounts)
    const counts = Object.values(locationCounts)
    chartData.value = {
      labels,
      datasets: [
        {
          label: 'Total Reservations',
          backgroundColor: '#3b82f6',
          data: counts
        }
      ]
    }
  }
}

// Export functionality
const exportData = async () => {
  exportLoading.value = true
  exportStatus.value = null
  
  try {
    const response = await fetch('http://127.0.0.1:5000/api/user/export-csv', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    
    if (response.ok) {
      taskId.value = data.task_id
      exportStatus.value = {
        type: 'success',
        message: `✅ CSV export initiated! Check your email in a few minutes.`
      }
      
      // Check status after 5 seconds
      setTimeout(() => checkExportStatus(), 5000)
    } else {
      exportStatus.value = {
        type: 'error',
        message: `❌ Export failed: ${data.error || 'Unknown error'}`
      }
    }
  } catch (error) {
    exportStatus.value = {
      type: 'error',
      message: `❌ Network error: ${error.message}`
    }
  } finally {
    exportLoading.value = false
  }
}

const checkExportStatus = async () => {
  if (!taskId.value) return
  
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/user/email-status/${taskId.value}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    const data = await response.json()
    
    if (data.state === 'SUCCESS') {
      exportStatus.value = {
        type: 'success',
        message: '✅ CSV export completed! Check your email inbox.'
      }
    } else if (data.state === 'FAILURE') {
      exportStatus.value = {
        type: 'error',
        message: `❌ Export failed: ${data.error}`
      }
    } else {
      exportStatus.value = {
        type: 'info',
        message: '⏳ Export in progress...'
      }
      // Check again in 3 seconds
      setTimeout(() => checkExportStatus(), 3000)
    }
  } catch (error) {
    console.error('Error checking export status:', error)
  }
}

onMounted(() => {
  fetchUserHistory()
})
</script>

<style scoped>
.clay-card {
  background: #2b2b3c;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 10px 10px 20px #1c1c2b, -10px -10px 20px #3a3a4a;
}

section {
  height: 400px;
}

.alert-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
</style>