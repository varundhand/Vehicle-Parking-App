<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-6">📈 My Parking Summary</h2>

    <section v-if="chartData">
      <Bar :data="chartData" :options="chartOptions" />
    </section>
    <p v-else>No data available</p>
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
