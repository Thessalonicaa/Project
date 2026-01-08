<template> 
  <div class="min-h-screen bg-gray-950 text-white transition-all duration-500">
   <!-- Car List -->
    <div class="space-y-8 p-6">
      <!-- First Row -->
      <div class="relative">
        <div class="absolute left-0 top-1/2 -translate-y-1/2 z-10">
          <button @click="scrollLeft('row1')" class="p-2 bg-red-600/80 rounded-r-lg hover:bg-red-700 transition-colors">
            <i class="fas fa-chevron-left text-2xl"></i>
          </button>
        </div>
        <div class="absolute right-0 top-1/2 -translate-y-1/2 z-10">
          <button @click="scrollRight('row1')" class="p-2 bg-red-600/80 rounded-l-lg hover:bg-red-700 transition-colors">
            <i class="fas fa-chevron-right text-2xl"></i>
          </button>
        </div>
        <div id="row1" class="flex overflow-x-auto hide-scrollbar gap-6 px-12 scroll-smooth">
          <NuxtLink
            v-for="car in cars.slice(0, Math.ceil(cars.length/2))"
            :key="car.id"
            :to="`/car/${car.id}`"
            class="car-card flex-shrink-0 w-[300px] bg-gradient-to-br from-gray-800/50 to-gray-900/50 p-4 rounded-2xl border border-gray-700  transition-all duration-300 hover:shadow-2xl hover:shadow-red-600/50 hover:-translate-y-2 transform"
          >
            <div class="relative mb-4 overflow-hidden rounded-xl group">
              <img :src="car.image" alt="" class="rounded-xl mb-0 w-full h-40 object-cover group-hover:scale-110 transition-transform duration-300" />
            </div>
            <h3 class="font-bold text-lg text-white mb-1">{{ car.name }}</h3>
            <p class="text-sm text-gray-400 mb-3">{{ car.brand }}</p>

            <!-- Extra info -->
            <div class="flex items-center justify-between text-sm text-gray-300 mb-4 p-2 bg-gray-700/30 rounded-lg">
              <span><i class="fas fa-cog text-red-500 mr-1"></i> {{ car.transmission }}</span>
              <span><i class="fas fa-gas-pump text-orange-500 mr-1"></i> {{ car.fuel }}</span>
            </div>

            <div class="flex items-center justify-between">
              <p class="text-2xl font-bold  text-red-500 ">฿{{ formatPrice(car.price) }}</p>
              <button class="px-4 py-2 rounded-lg bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white hover:shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-105 active:scale-95 font-semibold text-sm">
                View
              </button>
            </div>
          </NuxtLink>
        </div>
      </div>

      <!-- Second Row -->
      <div class="relative">
        <div class="absolute left-0 top-1/2 -translate-y-1/2 z-10">
          <button @click="scrollLeft('row2')" class="p-2 bg-red-600/80 rounded-r-lg hover:bg-red-700 transition-colors">
            <i class="fas fa-chevron-left text-2xl"></i>
          </button>
        </div>
        <div class="absolute right-0 top-1/2 -translate-y-1/2 z-10">
          <button @click="scrollRight('row2')" class="p-2 bg-red-600/80 rounded-l-lg hover:bg-red-700 transition-colors">
            <i class="fas fa-chevron-right text-2xl"></i>
          </button>
        </div>
        <div id="row2" class="flex overflow-x-auto hide-scrollbar gap-6 px-12 scroll-smooth">
          <NuxtLink
            v-for="car in cars.slice(Math.ceil(cars.length/2))"
            :key="car.id"
            :to="`/car/${car.id}`"
            class="car-card flex-shrink-0 w-[300px] bg-gradient-to-br from-gray-800/50 to-gray-900/50 p-4 rounded-2xl border border-gray-700  transition-all duration-300 hover:shadow-2xl hover:shadow-red-600/50 hover:-translate-y-2 transform"
          >
            <div class="relative mb-4 overflow-hidden rounded-xl group">
              <img :src="car.image" alt="" class="rounded-xl mb-0 w-full h-40 object-cover group-hover:scale-110 transition-transform duration-300" />
            </div>
            <h3 class="font-bold text-lg text-white mb-1">{{ car.name }}</h3>
            <p class="text-sm text-gray-400 mb-3">{{ car.brand }}</p>

            <!-- Extra info -->
            <div class="flex items-center justify-between text-sm text-gray-300 mb-4 p-2 bg-gray-700/30 rounded-lg">
              <span><i class="fas fa-cog text-red-500 mr-1"></i> {{ car.transmission }}</span>
              <span><i class="fas fa-gas-pump text-orange-500 mr-1"></i> {{ car.fuel }}</span>
            </div>

            <div class="flex items-center justify-between">
              <p class="text-2xl font-bold text-red-500">฿{{ formatPrice(car.price) }}</p>
              <button class="px-4 py-2 rounded-lg bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white hover:shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-105 active:scale-95 font-semibold text-sm">
                View
              </button>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>


    <!-- Compare Modal -->
    <div v-if="showCompare" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-4xl">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold">Compare Cars</h2>
          <button @click="showCompare = false" class="text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="grid grid-cols-3 gap-4">
          <!-- Compare cars content -->
        </div>
      </div>
    </div>

    <!-- Enhanced Brand Menu -->
     <div class="bg-gradient-to-r from-red-700/20 via-orange-600/10 to-red-700/20 py-8 px-6 border-y border-red-500/30 backdrop-blur-sm">
      <div class="max-w-7xl mx-auto">
        <div class="relative">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 z-10">
            <button @click="scrollLeft('brands')" class="p-3 bg-red-600/80 hover:bg-red-700 rounded-full transition-all transform hover:scale-110 active:scale-95 shadow-lg">
              <i class="fas fa-chevron-left text-white"></i>
            </button>
          </div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 z-10">
            <button @click="scrollRight('brands')" class="p-3 bg-red-600/80 hover:bg-red-700 rounded-full transition-all transform hover:scale-110 active:scale-95 shadow-lg">
              <i class="fas fa-chevron-right text-white"></i>
            </button>
          </div>
          <div id="brands" class="flex overflow-x-auto hide-scrollbar gap-4 px-12 scroll-smooth">
            <NuxtLink
              v-for="brand in brands"
              :key="brand"
              :to="`/brand/${brand.toLowerCase()}`"
              class="brand-button flex items-center gap-3 bg-gradient-to-r from-gray-800/50 to-gray-900/50 backdrop-blur-sm px-6 py-4 rounded-2xl hover:from-red-600/30 hover:to-orange-600/30 border border-gray-700 hover:border-red-500 transition-all duration-300 flex-shrink-0 transform hover:scale-110 shadow-lg hover:shadow-red-600/50"
            >
              <img 
                :src="`/images/brands/${brand.toLowerCase()}.png`" 
                :alt="`${brand} logo`" 
                class="w-8 h-8 object-contain drop-shadow-lg"
                @error="handleImageError"
              />
              <span class="whitespace-nowrap font-semibold text-white">{{ brand }}</span>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const isDark = ref(true)
const searchQuery = ref('')
const showCompare = ref(false)
const showWishlist = ref(false)
const compareList = ref([])
const wishlist = ref([])
const cars = ref([])
const brands = ref(['Toyota', 'Honda', 'Nissan', 'Mazda', 'BMW', 'Mercedes', 'Audi', 'Ford', 'Chevrolet', 'Mitsubishi'])
const loading = ref(true)

// Fetch cars from backend
onMounted(async () => {
  try {
    const response = await fetch('http://localhost:5000/api/cars')
    const data = await response.json()
    
    if (data.success) {
      cars.value = data.cars.map(car => ({
        id: car.id,
        name: `${car.brand} ${car.model}`,
        brand: car.brand,
        model: car.model,
        year: car.year,
        price: car.price,
        image: car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/300x200?text=No+Image',
        transmission: 'Automatic',
        fuel: 'Petrol'
      }))
    }
  } catch (error) {
    console.error('Error fetching cars:', error)
  } finally {
    loading.value = false
  }
})

// Format price function
const formatPrice = (price) => {
  if (!price) return 'N/A'
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

// Handle missing brand images
const handleImageError = (e) => {
  e.target.src = '/images/brands/'
}

// Dark mode toggle
const toggleDarkMode = () => {
  isDark.value = !isDark.value
}

// Search functionality
const searchSuggestions = computed(() => {
  if (!searchQuery.value) return []
  return cars.value.filter(car => 
    car.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    car.brand.toLowerCase().includes(searchQuery.value.toLowerCase())
  ).slice(0, 5)
})

const filteredCars = computed(() => {
  if (!searchQuery.value) return cars.value
  return cars.value.filter(car => 
    car.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    car.brand.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Wishlist & Compare functions
const toggleWishlist = (car) => {
  const index = wishlist.value.findIndex(item => item.id === car.id)
  if (index === -1) {
    wishlist.value.push(car)
  } else {
    wishlist.value.splice(index, 1)
  }
}

const toggleCompare = (car) => {
  if (compareList.value.length >= 3 && !isInCompare(car.id)) {
    alert('You can compare up to 3 cars')
    return
  }
  const index = compareList.value.findIndex(item => item.id === car.id)
  if (index === -1) {
    compareList.value.push(car)
  } else {
    compareList.value.splice(index, 1)
  }
}

const isInWishlist = (id) => wishlist.value.some(car => car.id === id)
const isInCompare = (id) => compareList.value.some(car => car.id === id)

// Scroll functions
const scrollLeft = (elementId) => {
  const element = document.getElementById(elementId)
  element.scrollBy({ left: -300, behavior: 'smooth' })
}

const scrollRight = (elementId) => {
  const element = document.getElementById(elementId)
  element.scrollBy({ left: 300, behavior: 'smooth' })
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  font-family: 'Inter', sans-serif;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.car-card {
  @apply rounded-xl shadow-lg backdrop-blur-sm transition-all duration-500;
  animation: fadeIn 0.5s ease-out;
}

.car-card:hover {
  @apply shadow-xl transform -translate-y-1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.brand-button {
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
