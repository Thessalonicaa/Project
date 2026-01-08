<template>
  <div class="min-h-screen bg-gray-950 text-white transition-all duration-500">
    <div class="max-w-5xl mx-auto p-6 space-y-10">
      <!-- Header -->
      <div class="text-center mb-12 animate-slide-down">
        <h1 class="text-6xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent mb-3 drop-shadow-lg">
          <i class="fas fa-tachometer-alt mr-3"></i>{{ accountType }} Dashboard
        </h1>
        <p class="text-gray-400 text-lg">Welcome  <span class="text-red-400 font-semibold">{{ username }}</span>
        </p>
      </div>

      <!-- Profile Card -->
      <div class="mb-12 bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50  transition-all duration-300 shadow-2xl animate-fade-in">
        <div class="flex flex-col md:flex-row items-center gap-8">
          <div class="relative flex-shrink-0">
            <div class="w-32 h-32 rounded-full bg-gradient-to-br from-red-600 to-orange-600 p-1 shadow-2xl">
              <div v-if="profileImage" class="w-full h-full rounded-full overflow-hidden bg-gray-800">
                <img :src="profileImage" class="w-full h-full object-cover" alt="Profile" />
              </div>
              <div v-else class="w-full h-full rounded-full bg-gray-800 flex items-center justify-center">
                <i class="fas fa-user text-white text-5xl"></i>
              </div>
            </div>
            <div 
              :class="[
                'absolute -bottom-1 -right-1 w-6 h-6 rounded-full border-4 border-gray-950 flex items-center justify-center shadow-lg',
                isOnline ? 'bg-green-500' : 'bg-gray-500'
              ]"
            >
              <i :class="['fas text-white font-bold', isOnline ? 'fa-check' : 'fa-circle text-xs']"></i>
            </div>
          </div>

          <div class="flex-1 text-center md:text-left space-y-4">
            <div>
              <h2 class="text-4xl font-extrabold text-white mb-1">{{ username }}</h2>
              <p class="text-lg text-red-400 font-semibold">{{ accountType }} Account</p>
            </div>
            <div class="grid grid-cols-3 gap-4">
              <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-3 text-center">
                <p class="text-gray-400 text-sm mb-1">Member Since</p>
                <p class="text-white font-bold">{{ memberSince }}</p>
              </div>
              <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-3 text-center">
                <p class="text-gray-400 text-sm mb-1">Last Activity</p>
                <p class="text-white font-bold">{{ lastActivity }}</p>
              </div>
              <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-3 text-center">
                <p class="text-gray-400 text-sm mb-1">Status</p>
                <p class="text-green-400 font-bold">
                  <i class="fas fa-circle text-green-500 mr-1"></i>Active
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div v-if="isSeller" class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8 animate-fade-in">
        <div class="group relative bg-gradient-to-br from-red-600/20 to-red-800/10 p-8 rounded-3xl border border-red-500/30 hover:border-red-500/60 transition-all transform hover:scale-105 duration-300 hover:shadow-2xl hover:shadow-red-500/30 shadow-xl cursor-pointer overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative flex items-center justify-between">
            <div class="z-10">
              <p class="text-red-200 text-sm uppercase font-semibold mb-2 tracking-wider">Cars Listed</p>
              <p class="text-5xl font-extrabold text-red-400 drop-shadow-lg">{{ stats.totalProducts }}</p>
              <p class="text-red-300 text-xs mt-2"><i class="fas fa-arrow-up mr-1"></i>Active vehicles</p>
            </div>
            <div class="text-7xl text-red-500/20 group-hover:text-red-500/40 transition-colors duration-300">
              <i class="fas fa-car"></i>
            </div>
          </div>
        </div>

        <div class="group relative bg-gradient-to-br from-blue-600/20 to-blue-800/10 p-8 rounded-3xl border border-blue-500/30 hover:border-blue-500/60 transition-all transform hover:scale-105 duration-300 hover:shadow-2xl hover:shadow-blue-500/30 shadow-xl cursor-pointer overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-blue-600/0 to-blue-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative flex items-center justify-between">
            <div class="z-10">
              <p class="text-blue-200 text-sm uppercase font-semibold mb-2 tracking-wider">Orders</p>
              <p class="text-5xl font-extrabold text-blue-400 drop-shadow-lg">{{ stats.totalOrders }}</p>
              <p class="text-blue-300 text-xs mt-2"><i class="fas fa-shopping-cart mr-1"></i>Total purchases</p>
            </div>
            <div class="text-7xl text-blue-500/20 group-hover:text-blue-500/40 transition-colors duration-300">
              <i class="fas fa-receipt"></i>
            </div>
          </div>
        </div>

        <div class="group relative bg-gradient-to-br from-green-600/20 to-green-800/10 p-8 rounded-3xl border border-green-500/30 hover:border-green-500/60 transition-all transform hover:scale-105 duration-300 hover:shadow-2xl hover:shadow-green-500/30 shadow-xl cursor-pointer overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-green-600/0 to-green-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative flex items-center justify-between">
            <div class="z-10">
              <p class="text-green-200 text-sm uppercase font-semibold mb-2 tracking-wider">Total Revenue</p>
              <p class="text-4xl font-extrabold text-green-400 drop-shadow-lg">฿{{ formatPrice(stats.totalRevenue) }}</p>
              <p class="text-green-300 text-xs mt-2"><i class="fas fa-wallet mr-1"></i>Earnings</p>
            </div>
            <div class="text-7xl text-green-500/20 group-hover:text-green-500/40 transition-colors duration-300">
              <i class="fas fa-money-bill-wave"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- My Cars -->
      <div class="bg-gray-800/40 backdrop-blur-sm p-8 rounded-2xl border border-gray-700/50 transition-all duration-300 animate-fade-in">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold flex items-center gap-3">
            <i class="fas fa-list text-red-500 text-2xl"></i>My Listings
          </h3>
          <div class="flex items-center gap-3">
            <NuxtLink to="/seller/MyListings" class="px-2 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-all duration-300 transform hover:scale-105 font-semibold flex items-center">
              <i class="fas fa-car"></i>List
            </NuxtLink>
            <NuxtLink to="/seller/PostCar" class="px-2 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-all duration-300 transform hover:scale-105 font-semibold flex items-center">
              <i class="fas fa-plus mr-2"></i>Post Car
            </NuxtLink>
          </div>
        </div>

        <div v-if="sellerCars.length === 0" class="text-center py-12">
          <i class="fas fa-inbox text-6xl text-gray-600 mb-4"></i>
          <p class="text-gray-400 text-lg">No cars listed yet</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <NuxtLink
            v-for="car in sellerCars"
            :key="car._id"
            :to="`/car/${car._id}`"
            class="bg-gray-800/50 rounded-xl overflow-hidden border border-gray-700  transition-all transform hover:-translate-y-2 duration-300 group"
          >
            <div class="relative h-32 overflow-hidden">
              <img
                :src="car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/300x200?text=No+Image'"
                :alt="car.model"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
              />
            </div>
            <div class="p-4">
              <h4 class="font-bold text-white">{{ car.brand }} {{ car.model }}</h4>
              <p class="text-sm text-gray-400">Year {{ car.year }}</p>
              <p class="text-red-500 font-bold mt-2 text-lg">฿{{ formatPrice(car.price) }}</p>
            </div>
          </NuxtLink>
        </div>
      </div>

      <!-- Chart -->
      <div class="bg-gray-800/40 backdrop-blur-sm p-8 rounded-2xl border border-gray-700/50 transition-all duration-300 animate-fade-in">
        <h3 class="text-2xl font-bold flex items-center gap-3 mb-6">
          <i class="fas fa-chart-line text-red-500 text-2xl"></i>Monthly Sales
        </h3>
        <p class="text-gray-400">Chart updates when orders are received</p>

        <div class="mt-8 flex items-end justify-around gap-4 h-48 bg-gray-900/50 rounded-lg p-6">
          <div class="flex flex-col items-center flex-1">
            <div class="w-12 bg-red-500/30 rounded-t h-24 hover:h-28 transition-all duration-300 hover:bg-red-500/50"></div>
            <p class="text-xs text-gray-400 mt-3">Jan</p>
          </div>
          <div class="flex flex-col items-center flex-1">
            <div class="w-12 bg-red-500/30 rounded-t h-16 hover:h-20 transition-all duration-300 hover:bg-red-500/50"></div>
            <p class="text-xs text-gray-400 mt-3">Feb</p>
          </div>
          <div class="flex flex-col items-center flex-1">
            <div class="w-12 bg-red-500/30 rounded-t h-32 hover:h-36 transition-all duration-300 hover:bg-red-500/50"></div>
            <p class="text-xs text-gray-400 mt-3">Mar</p>
          </div>
          <div class="flex flex-col items-center flex-1">
            <div class="w-12 bg-red-500/30 rounded-t h-20 hover:h-24 transition-all duration-300 hover:bg-red-500/50"></div>
            <p class="text-xs text-gray-400 mt-3">Apr</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const username = ref('')
const isSeller = ref(false)
const accountType = ref('User')
const sellerCars = ref([])
const profileImage = ref('')
const isOnline = ref(true)

const memberSince = ref('10/12/2025')
const lastActivity = ref(new Date().toLocaleDateString())
const stats = ref({
  totalProducts: 0,
  totalOrders: 0,
  totalRevenue: 0,
  monthlySales: [],
  lastUpdate: ''
})

const fetchDashboardData = async () => {
  try {
    const usernameLocal = localStorage.getItem('username')
    if (!usernameLocal) return

    const response = await fetch(`http://localhost:5000/api/cars/seller/${usernameLocal}`)
    const data = await response.json()

    if (data.success) {
      stats.value.totalProducts = data.cars?.length || 0
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

onMounted(async () => {
  if (process.client) {
    username.value = localStorage.getItem('username') || ''
    isSeller.value = localStorage.getItem('is_seller') === 'true'
    accountType.value = isSeller.value ? 'Seller' : 'User'
    isOnline.value = true

     try {
      const response = await fetch(`http://localhost:5000/api/get-profile?username=${username.value}`)
      const data = await response.json()
      if (data.success && data.profileImageUrl) {
        profileImage.value = data.profileImageUrl
        localStorage.setItem('profileImage', data.profileImageUrl)
      }
    } catch (error) {
      console.error('Error fetching profile image:', error)
      const saved = localStorage.getItem('profileImage')
      if (saved) {
        profileImage.value = saved
      }
    }

    if (isSeller.value) {
      try {
        const response = await fetch(`http://localhost:5000/api/cars/seller/${username.value}`)
        const data = await response.json()

        if (data.success) {
          sellerCars.value = data.cars
          stats.value.totalProducts = data.cars.length
        }
      } catch (error) {
        console.error('Error fetching seller cars:', error)
      }
    }

    // ติดตามสถานะออนไลน์
    const handleOnline = () => {
      isOnline.value = true
    }
    const handleOffline = () => {
      isOnline.value = false
    }

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }
})

watch(() => route.path, fetchDashboardData, { immediate: true })

const formatPrice = (price) => price?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') || 0

const lastUpdateDisplay = computed(() =>
  stats.value.lastUpdate
    ? new Date(stats.value.lastUpdate).toLocaleString('th-TH', {
        dateStyle: 'medium',
        timeStyle: 'short'
      })
    : new Date().toLocaleString('th-TH', {
        dateStyle: 'medium',
        timeStyle: 'short'
      })
)

const logout = () => {
  localStorage.clear()
  window.location.href = '/login'
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root {
  font-family: 'Inter', sans-serif;
}
.animate-fadeIn {
  animation: fadeIn 0.6s ease-out;
}
.animate-slideUp {
  animation: slideUp 0.7s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>