<template>
  <div class="container py-4">
    <div class="clay-card p-4 mb-5">
      <h2 class="mb-3 text-white">📊 Revenue by Parking Lot</h2>
      <div style="height: 350px;">
        <Pie :data="revenueChartData" :options="chartOptions" />
      </div>
    </div>

    <div class="clay-card p-4">
      <h2 class="mb-3 text-white">📦 Spot Availability Overview</h2>
      <div style="height: 400px;">
        <Bar :data="availabilityChartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Pie, Bar } from 'vue-chartjs'
// import {Pie} from vue-ChartJS
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  ArcElement, BarElement,
  CategoryScale, LinearScale
} from 'chart.js'

// Register chart components
ChartJS.register(Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale)

const token = localStorage.getItem('token')

const revenueChartData = ref({ labels: [], datasets: [] })
const availabilityChartData = ref({ labels: [], datasets: [] })

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
}

const fetchRevenue = async () => {
  const res = await fetch('http://127.0.0.1:5000/api/admin/summary/revenue', {
    headers: { Authorization: `Bearer ${token}` }
  })
  const data = await res.json()

  revenueChartData.value = {
    labels: data.map(d => d.lot),
    datasets: [{
      label: 'Revenue',
      backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
      data: data.map(d => d.revenue)
    }]
  }
}

const fetchAvailability = async () => {
  const res = await fetch('http://127.0.0.1:5000/api/admin/summary/availability', {
    headers: { Authorization: `Bearer ${token}` }
  })
  const data = await res.json()

  availabilityChartData.value = {
    labels: data.map(d => d.lot),
    datasets: [
      {
        label: 'Available',
        backgroundColor: '#10b981',
        data: data.map(d => d.available)
      },
      {
        label: 'Occupied',
        backgroundColor: '#ef4444',
        data: data.map(d => d.occupied)
      }
    ]
  }
}

onMounted(() => {
  fetchRevenue()
  fetchAvailability()
})
</script>

<style scoped>
.clay-card {
  background: #2b2b2b;
  border-radius: 16px;
  box-shadow: 8px 8px 20px #1c1c1c, -8px -8px 20px #3c3c3c;
  color: white;
}
</style>
