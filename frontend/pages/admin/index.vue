<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-950 to-gray-900 text-white p-8">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-5xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent mb-2">
          <i class="fas fa-shield-alt mr-3"></i>Admin Dashboard
        </h1>
        <p class="text-gray-400 text-lg">Manage users, sellers, and car listings</p>
      </div>

      <div v-if="!isAdmin" class="text-center py-20">
        <div class="inline-block">
          <i class="fas fa-lock text-6xl text-red-500 mb-4"></i>
          <p class="text-gray-400 text-xl">You are not authorized to view this page.</p>
          <NuxtLink to="/" class="inline-block mt-6 px-6 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-all">
            Go Home
          </NuxtLink>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Data Users Card -->
        <NuxtLink 
          to="/admin/users" 
          class="group relative bg-gradient-to-br from-blue-600/20 to-blue-800/10 border border-blue-500/30 hover:border-blue-500/60 rounded-3xl p-8 transition-all transform hover:scale-105 duration-300 shadow-xl hover:shadow-2xl hover:shadow-blue-500/30 overflow-hidden cursor-pointer"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-blue-600/0 to-blue-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative z-10">
            <div class="text-5xl text-blue-500 mb-4">
              <i class="fas fa-users"></i>
            </div>
            <h2 class="text-2xl font-bold text-white mb-2">Data Users</h2>
            <p class="text-gray-400">View and manage user and seller accounts</p>
            <div class="mt-4 flex items-center text-blue-400 group-hover:translate-x-2 transition-transform">
              <span>Manage Users</span>
              <i class="fas fa-arrow-right ml-2"></i>
            </div>
          </div>
        </NuxtLink>

        <!-- Data Cars Card -->
        <NuxtLink 
          to="/admin/cars" 
          class="group relative bg-gradient-to-br from-red-600/20 to-red-800/10 border border-red-500/30 hover:border-red-500/60 rounded-3xl p-8 transition-all transform hover:scale-105 duration-300 shadow-xl hover:shadow-2xl hover:shadow-red-500/30 overflow-hidden cursor-pointer"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative z-10">
            <div class="text-5xl text-red-500 mb-4">
              <i class="fas fa-car"></i>
            </div>
            <h2 class="text-2xl font-bold text-white mb-2">Data Cars</h2>
            <p class="text-gray-400">View and manage car listings</p>
            <div class="mt-4 flex items-center text-red-400 group-hover:translate-x-2 transition-transform">
              <span>Manage Cars</span>
              <i class="fas fa-arrow-right ml-2"></i>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- Stats Section -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
        <div class="bg-gray-800/50 border border-gray-700 rounded-2xl p-6">
          <p class="text-gray-400 text-sm uppercase font-semibold mb-2">Total Users</p>
          <p class="text-4xl font-bold text-blue-400">{{ stats.users }}</p>
        </div>
        <div class="bg-gray-800/50 border border-gray-700 rounded-2xl p-6">
          <p class="text-gray-400 text-sm uppercase font-semibold mb-2">Total Cars</p>
          <p class="text-4xl font-bold text-red-400">{{ stats.cars }}</p>
        </div>
        <div class="bg-gray-800/50 border border-gray-700 rounded-2xl p-6">
          <p class="text-gray-400 text-sm uppercase font-semibold mb-2">Last Updated</p>
          <p class="text-lg font-bold text-green-400">{{ lastUpdate }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isAdmin = ref(false)
const stats = ref({ users: 0, cars: 0 })
const lastUpdate = ref('just now')

const fetchStats = async () => {
  try {
    const usersRes = await fetch('http://localhost:5000/api/admin/users')
    const carsRes = await fetch('http://localhost:5000/api/admin/cars')
    
    const usersData = await usersRes.json()
    const carsData = await carsRes.json()
    
    if (usersData.success) stats.value.users = usersData.users?.length || 0
    if (carsData.success) stats.value.cars = carsData.cars?.length || 0
    lastUpdate.value = new Date().toLocaleTimeString()
  } catch (e) { console.error(e) }
}

onMounted(() => {
  if (process.client) {
    const role = localStorage.getItem('role')
    isAdmin.value = role === 'admin' || localStorage.getItem('is_admin') === 'true'
    if (isAdmin.value) fetchStats()
  }
})
</script>

<style scoped>
/* Tailwind handles all styling */
</style>