<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-6">📊 Admin Summary</h2>

    <!-- Revenue Chart -->
    <section class="mb-12">
      <h3 class="text-xl mb-2">Revenue per Parking Lot</h3>
      <Pie :data="revenueChartData" :options="chartOptions" />
    </section>

    <!-- Availability Chart -->
    <section>
      <h3 class="text-xl mb-2">Availability Overview</h3>
      <Bar :data="availabilityChartData" :options="chartOptions" />
    </section>
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
section {
  height: 400px;
}
</style>
