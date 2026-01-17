<template>
  <div class="min-h-screen bg-gray-950 text-white transition-all duration-500">
    <div class="beams-background">
      <Beams
        :beamWidth="3"
        :beamHeight="25"
        :beamNumber="20"
        lightColor="#ff3c03"
        :speed="2"
        :noiseIntensity="1.75"
        :scale="0.2"
        :rotation="30"
        :width="1920"
        :height="1080"
      />
    </div>
    <div class="max-w-6xl mx-auto p-6 space-y-10 relative z-10">
      <!-- Header -->
      <div class="text-center mb-12 animate-slide-down">
        <div class="mb-4">
          <span class="inline-block px-4 py-2 bg-red-600/20 border border-red-500/50 rounded-full text-red-400 text-sm font-bold uppercase tracking-wider">
            Welcome Back
          </span>
        </div>
        <h1 class="text-6xl md:text-7xl font-extrabold bg-gradient-to-r from-red-500 via-orange-500 to-red-500 bg-clip-text text-transparent mb-3 drop-shadow-lg">
          {{ accountType }} Dashboard
        </h1>
        <p class="text-gray-400 text-lg">
          Welcome <span class="text-red-400 font-bold">{{ username }}</span>
        </p>
      </div>

      <!-- Profile Card with Enhanced Styling -->
      <div class="mb-12 bg-gradient-to-br from-gray-900/80 via-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-10 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-2xl animate-fade-in">
        <NuxtLink to="/profile" class="block cursor-pointer group">
          <div class="flex flex-col lg:flex-row items-center gap-10">
            <div class="relative flex-shrink-0">
              <div class="absolute inset-0 bg-gradient-to-r from-red-600 to-orange-600 rounded-full blur-2xl opacity-40 group-hover:opacity-60 transition-opacity duration-300"></div>
              <div class="relative w-40 h-40 rounded-full bg-gradient-to-br from-red-600 to-orange-600 p-1 shadow-2xl group-hover:shadow-red-600/50 transition-all duration-300 group-hover:scale-110 transform">
                <div v-if="profileImage" class="w-full h-full rounded-full overflow-hidden bg-gray-800">
                  <img :src="profileImage" class="w-full h-full object-cover" alt="Profile" />
                </div>
                <div v-else class="w-full h-full rounded-full bg-gray-800 flex items-center justify-center">
                  <i class="fas fa-user text-white text-6xl"></i>
                </div>
              </div>
              <div 
                :class="[
                  'absolute -bottom-2 -right-2 w-8 h-8 rounded-full border-4 border-gray-950 flex items-center justify-center shadow-lg text-lg',
                  isOnline ? 'bg-green-500' : 'bg-gray-500'
                ]"
              >
                <i :class="['fas text-white font-bold', isOnline ? 'fa-check text-sm' : 'fa-circle text-xs']"></i>
              </div>
            </div>

            <div class="flex-1 text-center lg:text-left space-y-6 group-hover:scale-105 transition-transform duration-300">
              <div>
                <h2 class="text-5xl font-extrabold text-white mb-2 group-hover:text-red-400 transition-colors">{{ username }}</h2>
                <p class="text-xl text-red-400 font-semibold flex items-center gap-2 justify-center lg:justify-start">
                  <i :class="[isSeller ? 'fas fa-store text-red-500' : 'fas fa-user text-blue-500']"></i>
                  {{ isSeller ? ' Seller Account' : ' User Account' }}
                </p>
              </div>
              <div class="grid grid-cols-3 gap-4">
                <div class="bg-gradient-to-br from-red-600/20 to-red-700/10 p-4 rounded-2xl border border-red-500/30 text-center hover:border-red-500/60 transition-all duration-300 group-hover:bg-red-600/30">
                  <p class="text-red-200 text-xs uppercase font-bold tracking-wider mb-1">Member Since</p>
                  <p class="text-white font-bold text-lg">{{ memberSince }}</p>
                </div>
                <div class="bg-gradient-to-br from-blue-600/20 to-blue-700/10 p-4 rounded-2xl border border-blue-500/30 text-center hover:border-blue-500/60 transition-all duration-300 group-hover:bg-blue-600/30">
                  <p class="text-blue-200 text-xs uppercase font-bold tracking-wider mb-1">Last Activity</p>
                  <p class="text-white font-bold text-lg">{{ lastActivity }}</p>
                </div>
                <div class="bg-gradient-to-br from-green-600/20 to-green-700/10 p-4 rounded-2xl border border-green-500/30 text-center hover:border-green-500/60 transition-all duration-300 group-hover:bg-green-600/30">
                  <p class="text-green-200 text-xs uppercase font-bold tracking-wider mb-1">Status</p>
                  <p class="text-green-400 font-bold text-lg">
                    <i class="fas fa-circle text-green-500 mr-1"></i>Active
                  </p>
                </div>
              </div>
            </div>

            <!-- Click to View Profile Indicator -->
            <div class="absolute top-6 right-6 bg-red-600/90 px-4 py-2 rounded-full text-sm font-bold text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 backdrop-blur-sm">
              <i class="fas fa-arrow-right mr-2"></i>View Profile
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- Stats Cards - Enhanced -->
      <div v-if="isSeller" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 animate-fade-in">
        <div class="group relative bg-gradient-to-br from-red-600/20 to-red-800/10 p-8 rounded-3xl border border-red-500/30 hover:border-red-500/60 transition-all transform hover:scale-105 duration-300 hover:shadow-2xl hover:shadow-red-500/30 shadow-xl cursor-pointer overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative flex items-center justify-between">
            <div class="z-10">
              <p class="text-red-200 text-xs uppercase font-bold mb-2 tracking-widest">Cars Listed</p>
              <p class="text-5xl font-extrabold text-red-400 drop-shadow-lg">{{ stats.totalProducts }}</p>
              <p class="text-red-300 text-xs mt-3 font-semibold"><i class="fas fa-arrow-up mr-1"></i>Active vehicles</p>
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
              <p class="text-blue-200 text-xs uppercase font-bold mb-2 tracking-widest">Orders</p>
              <p class="text-5xl font-extrabold text-blue-400 drop-shadow-lg">{{ stats.totalOrders }}</p>
              <p class="text-blue-300 text-xs mt-3 font-semibold"><i class="fas fa-shopping-cart mr-1"></i>Total purchases</p>
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
              <p class="text-green-200 text-xs uppercase font-bold mb-2 tracking-widest">Total Revenue</p>
              <p class="text-4xl font-extrabold text-green-400 drop-shadow-lg">฿{{ formatPrice(stats.totalRevenue) }}</p>
              <p class="text-green-300 text-xs mt-3 font-semibold"><i class="fas fa-wallet mr-1"></i>Earnings</p>
            </div>
            <div class="text-7xl text-green-500/20 group-hover:text-green-500/40 transition-colors duration-300">
              <i class="fas fa-money-bill-wave"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- My Cars Section -->
      <div class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl p-10 rounded-3xl border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-2xl animate-fade-in">
        <div class="flex flex-col md:flex-row items-center justify-between mb-8 gap-4">
          <h3 class="text-3xl font-bold flex items-center gap-3 text-white">
            <i class="fas fa-list text-red-500 text-3xl"></i>My Listings
          </h3>
          <div class="flex items-center gap-3 flex-wrap justify-center md:justify-end">
            <NuxtLink to="/seller/MyListings" class="px-4 py-3 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white rounded-xl transition-all duration-300 transform hover:scale-105 font-bold flex items-center gap-2 shadow-lg">
              <i class="fas fa-list-ul"></i>All Listings
            </NuxtLink>
            <!-- Post Car Button - Check role -->
            <NuxtLink 
              v-if="isSeller"
              to="/seller/PostCar" 
              class="px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white rounded-xl transition-all duration-300 transform hover:scale-105 font-bold flex items-center gap-2 shadow-lg hover:shadow-red-600/50"
            >
              <i class="fas fa-plus"></i>Post Car
            </NuxtLink>
            <button 
              v-else
              @click="redirectToRegisterSeller"
              class="px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white rounded-xl transition-all duration-300 transform hover:scale-105 font-bold flex items-center gap-2 shadow-lg hover:shadow-red-600/50"
            >
              <i class="fas fa-plus"></i>Post Car
            </button>
          </div>
        </div>

        <div v-if="sellerCars.length === 0" class="text-center py-20">
          <i class="fas fa-inbox text-8xl text-gray-600 mb-6 opacity-40"></i>
          <p class="text-gray-400 text-2xl font-bold mb-2">No cars listed yet</p>
          <p class="text-gray-500 text-base mb-8">Start selling your vehicles today!</p>
          
          <!-- Register as Seller Button (Show only if not a seller) -->
          <div v-if="!isSeller" class="flex flex-col items-center gap-4">
            <NuxtLink 
              to="/Register-seller" 
              class="group relative inline-flex items-center justify-center px-8 py-4   to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-red-600/50 overflow-hidden"
            >
              <span class="relative z-10 flex items-center gap-2">
                <i class="fas fa-crown"></i>
                Register as Seller
                <i class="fas fa-arrow-right ml-2 group-hover:translate-x-1 transition-transform"></i>
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-red-700 to-red-800 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </NuxtLink>
            <p class="text-gray-500 text-xs">Unlock the ability to list and sell vehicles</p>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <NuxtLink
            v-for="car in sellerCars"
            :key="car._id"
            :to="`/car/${car._id}`"
            class="bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl overflow-hidden border border-gray-700 hover:border-red-500/50 transition-all transform hover:-translate-y-3 duration-300 group shadow-lg hover:shadow-2xl hover:shadow-red-500/20"
          >
            <div class="relative h-40 overflow-hidden bg-gray-900">
              <img
                :src="car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/300x200?text=No+Image'"
                :alt="car.model"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
              />
              <div class="absolute top-3 right-3 bg-red-600/80 px-3 py-1 rounded-full text-xs font-bold text-white backdrop-blur-sm">
                {{ car.year }}
              </div>
            </div>
            <div class="p-5">
              <h4 class="font-bold text-white text-lg group-hover:text-red-400 transition-colors mb-1">{{ car.brand }} {{ car.model }}</h4>
              <p class="text-sm text-gray-400 mb-3">
                <i class="fas fa-tachometer-alt text-red-500 mr-1"></i>
                {{ car.mileage ? formatMileage(car.mileage) + ' km' : 'N/A' }}
              </p>
              <p class="text-lg font-bold text-red-400">
                <i class="fas fa-tag mr-1"></i>฿{{ formatPrice(car.price) }}
              </p>
            </div>
          </NuxtLink>
        </div>
      </div>

      <!-- Chart -->
      <div class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl p-10 rounded-3xl border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-2xl animate-fade-in">
        <h3 class="text-3xl font-bold flex items-center gap-3 mb-8 text-white">
          <i class="fas fa-chart-line text-red-500 text-3xl"></i>Monthly Sales
        </h3>
        <p class="text-gray-400 text-sm mb-8">Chart updates when orders are received</p>

        <div class="mt-8 flex items-end justify-around gap-4 h-64 bg-gray-900/50 rounded-2xl p-8 border border-gray-800">
          <div class="flex flex-col items-center flex-1">
            <div class="w-16 bg-gradient-to-t from-red-500 to-red-600 rounded-t-lg h-32 hover:h-40 transition-all duration-300 hover:shadow-lg hover:shadow-red-500/50 cursor-pointer group relative">
              <span class="absolute -top-8 left-1/2 transform -translate-x-1/2 text-red-400 font-bold opacity-0 group-hover:opacity-100 transition-opacity">12</span>
            </div>
            <p class="text-xs text-gray-400 mt-4 font-semibold">Jan</p>
          </div>
          <div class="flex flex-col items-center flex-1">
            <div class="w-16 bg-gradient-to-t from-red-500 to-red-600 rounded-t-lg h-24 hover:h-32 transition-all duration-300 hover:shadow-lg hover:shadow-red-500/50 cursor-pointer group relative">
              <span class="absolute -top-8 left-1/2 transform -translate-x-1/2 text-red-400 font-bold opacity-0 group-hover:opacity-100 transition-opacity">8</span>
            </div>
            <p class="text-xs text-gray-400 mt-4 font-semibold">Feb</p>
          </div>
          <div class="flex flex-col items-center flex-1">
            <div class="w-16 bg-gradient-to-t from-red-500 to-red-600 rounded-t-lg h-48 hover:h-56 transition-all duration-300 hover:shadow-lg hover:shadow-red-500/50 cursor-pointer group relative">
              <span class="absolute -top-8 left-1/2 transform -translate-x-1/2 text-red-400 font-bold opacity-0 group-hover:opacity-100 transition-opacity">18</span>
            </div>
            <p class="text-xs text-gray-400 mt-4 font-semibold">Mar</p>
          </div>
          <div class="flex flex-col items-center flex-1">
            <div class="w-16 bg-gradient-to-t from-red-500 to-red-600 rounded-t-lg h-32 hover:h-40 transition-all duration-300 hover:shadow-lg hover:shadow-red-500/50 cursor-pointer group relative">
              <span class="absolute -top-8 left-1/2 transform -translate-x-1/2 text-red-400 font-bold opacity-0 group-hover:opacity-100 transition-opacity">14</span>
            </div>
            <p class="text-xs text-gray-400 mt-4 font-semibold">Apr</p>
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
    const is_seller_value = localStorage.getItem('is_seller')
    const role_value = localStorage.getItem('role')
    
    // Check both is_seller and role
    isSeller.value = is_seller_value === 'true' || role_value === 'seller'
    accountType.value = isSeller.value ? 'Seller' : 'User'
    isOnline.value = true

    console.log('Dashboard - Username:', username.value)
    console.log('Dashboard - Is Seller:', isSeller.value)
    console.log('Dashboard - Role:', role_value)

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

    // Fetch seller cars if user is seller
    if (isSeller.value && username.value) {
      try {
        console.log('Fetching cars for seller:', username.value)
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:5000/api/seller-info/${username.value}`)
        const sellerData = await response.json()
        console.log('Seller info response:', sellerData)

        if (sellerData.success && sellerData.seller) {
          const sellerId = sellerData.seller.id
          
          // Now fetch cars for this seller
          const carsResponse = await fetch(`http://localhost:5000/api/cars?seller_id=${sellerId}`)
          const carsData = await carsResponse.json()
          console.log('Cars response:', carsData)

          if (carsData.success && carsData.cars) {
            sellerCars.value = carsData.cars
            stats.value.totalProducts = carsData.cars.length
            console.log('Cars loaded:', sellerCars.value.length)
          }
        }
      } catch (error) {
        console.error('Error fetching seller cars:', error)
      }
    }

    // Monitor online status
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

const formatMileage = (mileage) => {
  if (!mileage) return '0'
  return mileage.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

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

const redirectToRegisterSeller = () => {
  window.location.href = '/Register-seller'
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