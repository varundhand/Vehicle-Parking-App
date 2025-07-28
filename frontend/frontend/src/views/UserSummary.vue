<template>
  <div class="user-summary p-4">
    <div class="clay-card">
      <h2 class="text-light fs-4 fw-bold mb-4">📈 My Parking Summary</h2>
      <section v-if="chartData">
        <Bar :data="chartData" :options="chartOptions" />
      </section>
      <p v-else>No data available</p>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
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

onMounted(() => {
  fetchUserHistory()
})
</script>

<style scoped>
section {
  height: 400px;
}
</style>


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
</style>
