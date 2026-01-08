<template>
  <div>
    <!-- Loading Spinner -->
    <LoadingSpinner 
      :isLoading="loading" 
      loadingText="Loading brand cars..."
    />

    <div v-if="!loading" class="min-h-screen bg-gray-950 text-white">
      <div class="max-w-7xl mx-auto px-6 py-12">

        <!-- Back Button -->
        <button 
          @click="$router.back()"
          class="mb-8 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg transition-all flex items-center gap-2"
        >
          <i class="fas fa-arrow-left"></i> Back
        </button>

        <!-- Brand Header - Like Dashboard -->
        <div class="bg-gray-900/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 mb-12">
          <div class="flex flex-col md:flex-row items-center gap-8">
            <!-- Brand Logo -->
            <div class="relative">
              <div class="absolute inset-0 bg-gradient-to-r from-red-600 to-red-500 rounded-full blur-xl opacity-30"></div>
              <div class="relative w-32 h-32 bg-gray-800 rounded-full flex items-center justify-center border-4 border-red-500 shadow-2xl overflow-hidden">
                <img 
                  v-if="brandLogo" 
                  :src="brandLogo" 
                  :alt="selectedBrand" 
                  class="w-full h-full object-cover"
                />
                <i v-else class="fas fa-car text-5xl text-red-500"></i>
              </div>
            </div>

            <!-- Brand Info -->
            <div class="flex-1 text-center md:text-left">
              <h1 class="text-5xl font-extrabold bg-gradient-to-r from-red-500 to-red-400 bg-clip-text text-transparent mb-2">
                {{ selectedBrand }}
              </h1>
              <p class="text-xl text-gray-400 mb-4">Browse all available {{ selectedBrand }} cars</p>
              
              <!-- Stats -->
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-gray-800/50 p-3 rounded-lg border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Total Cars</p>
                  <p class="text-white font-bold text-2xl">{{ brandCars.length }}</p>
                </div>
                <div class="bg-gray-800/50 p-3 rounded-lg border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Price Range</p>
                  <p class="text-red-400 font-bold">฿{{ minPrice.toLocaleString('th-TH') }} - ฿{{ maxPrice.toLocaleString('th-TH') }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Filters Section -->
        <div class="mb-8 flex flex-wrap gap-4 animate-fade-in-up">
          <select
            v-model="selectedFuelType"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">All Fuel Types</option>
            <option value="Petrol">Petrol (น้ำมันแก๊ส)</option>
            <option value="Diesel">Diesel (น้ำมันดีเซล)</option>
            <option value="Hybrid">Hybrid (ไฮบริด)</option>
            <option value="Electric">Electric (รถไฟฟ้า)</option>
          </select>

          <select
            v-model="selectedTransmission"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">All Transmissions</option>
            <option value="Automatic">Automatic (อัตโนมัติ)</option>
            <option value="Manual">Manual (ธรรมชาติ)</option>
            <option value="Semi-Automatic">Semi-Automatic</option>
            <option value="CVT">CVT</option>
            <option value="e-CVT">e-CVT</option>
            <option value="DCT">DCT</option>
          </select>

          <select
            v-model="selectedCarType"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">All Car Types</option>
            <option value="Sedan">Sedan (ซีดาน)</option>
            <option value="SUV">SUV</option>
            <option value="Pickup">Pickup (พิคอัพ)</option>
            <option value="Van">Van (แวน)</option>
            <option value="Sports">Sports (สปอร์ต)</option>
          </select>

          <select
            v-model="priceRange"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">All Prices</option>
            <option value="0-50000">฿0 - ฿50,000</option>
            <option value="50000-100000">฿50,000 - ฿100,000</option>
            <option value="100000-500000">฿100,000 - ฿500,000</option>
            <option value="500000+">฿500,000+</option>
          </select>
        </div>

        <!-- Cars Grid - Like CarList -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in-up">
          <div v-if="filteredCars.length === 0" class="col-span-full text-center py-16">
            <i class="fas fa-search text-6xl text-gray-600 mb-4"></i>
            <p class="text-gray-400 text-xl">No {{ selectedBrand }} cars found</p>
          </div>

          <div
            v-for="(car, index) in filteredCars"
            :key="car.id"
            class="bg-gray-900/80 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 hover:scale-105 opacity-0 animate-fade-in-up border border-gray-800 hover:border-red-500/50 group"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <!-- Image -->
            <div class="relative h-48 overflow-hidden rounded-t-2xl">
              <img
                :src="car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/400x250?text=No+Image'"
                :alt="car.model"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              />
            </div>

            <!-- Content -->
            <div class="p-6">
              <!-- Title -->
              <h2 class="text-xl font-bold text-white mb-2">
                {{ car.brand }} {{ car.model }}
              </h2>

              <!-- Year & Type -->
              <div class="flex justify-between items-center mb-3 text-sm text-gray-400">
                <span><i class="fas fa-calendar mr-2"></i>{{ car.year }}</span>
                <span v-if="car.car_type" class="bg-red-500/20 px-2 py-1 rounded text-red-400">{{ car.car_type }}</span>
              </div>

              <!-- Fuel & Transmission -->
              <div v-if="car.fuel_type || car.transmission" class="flex gap-2 mb-3 flex-wrap">
                <span v-if="car.fuel_type" class="text-xs bg-blue-500/20 text-blue-400 px-2 py-1 rounded">
                  <i class="fas fa-gas-pump mr-1"></i>{{ car.fuel_type }}
                </span>
                <span v-if="car.transmission" class="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">
                  <i class="fas fa-cog mr-1"></i>{{ car.transmission }}
                </span>
              </div>

              <!-- Price -->
              <div class="flex items-baseline justify-between mb-4">
                <p class="text-3xl font-bold text-red-500">
                  ฿{{ car.price.toLocaleString('th-TH') }}
                </p>
                <span class="text-sm text-gray-400">Price</span>
              </div>

              <!-- Description -->
              <p class="text-gray-400 text-sm mb-4 line-clamp-2">{{ car.description }}</p>

              <!-- Button -->
              <NuxtLink
                :to="`/car/${car.id}`"
                class="w-full inline-block py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 duration-300 text-center shadow-lg"
              >
                <i class="fas fa-eye mr-2"></i>View Details
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import LoadingSpinner from '~/components/LoadingSpinner.vue'

const route = useRoute()
const selectedBrand = ref('')
const brandLogo = ref('')
const brandCars = ref([])
const loading = ref(true)

const selectedFuelType = ref('')
const selectedTransmission = ref('')
const selectedCarType = ref('')
const priceRange = ref('')

// Brand logos mapping - fallback to public images
const brandLogos = {
  'Toyota': '/images/brands/Toyota.png',
  'Honda': '/images/brands/Honda.png',
  'BMW': '/images/brands/BMW.png',
  'Mercedes': '/images/brands/Mercedes.png',
  'Audi': '/images/brands/Audi.png',
  'Ford': '/images/brands/Ford.png',
  'Chevrolet': '/images/brands/Chevrolet.png',
  'Nissan': '/images/brands/Nissan.png',
  'Mazda': '/images/brands/Mazda.png',
  'Mitsubishi': '/images/brands/Mitsubishi.png'
}

const fetchBrandCars = async () => {
  loading.value = true
  try {
    const brand = route.params.brand
    selectedBrand.value = brand

    // Fetch all cars
    const response = await fetch('http://localhost:5000/api/cars')
    const data = await response.json()

    if (data.success) {
      // Filter cars by brand
      const carsForBrand = data.cars.filter(car => car.brand === brand) || []
      brandCars.value = carsForBrand

      // Try to get brand image from first car's seller profile
      if (carsForBrand.length > 0) {
        const firstCar = carsForBrand[0]
        try {
          const sellerRes = await fetch(
            `http://localhost:5000/api/get-profile?username=${firstCar.seller_username}`
          )
          const sellerData = await sellerRes.json()
          
          // Use seller's profile image if available, otherwise use fallback
          if (sellerData.success && sellerData.profileImageUrl) {
            brandLogo.value = sellerData.profileImageUrl
          } else {
            brandLogo.value = brandLogos[brand] || ''
          }
        } catch (error) {
          // Fallback to public brand image
          console.log('Using fallback brand logo')
          brandLogo.value = brandLogos[brand] || ''
        }
      } else {
        brandLogo.value = brandLogos[brand] || ''
      }
    }
  } catch (error) {
    console.error('Error fetching cars:', error)
  } finally {
    loading.value = false
  }
}

const minPrice = computed(() => {
  if (filteredCars.value.length === 0) return 0
  return Math.min(...filteredCars.value.map(c => c.price))
})

const maxPrice = computed(() => {
  if (filteredCars.value.length === 0) return 0
  return Math.max(...filteredCars.value.map(c => c.price))
})

const filteredCars = computed(() => {
  return brandCars.value.filter(car => {
    if (selectedFuelType.value && car.fuel_type !== selectedFuelType.value) return false
    if (selectedTransmission.value && car.transmission !== selectedTransmission.value) return false
    if (selectedCarType.value && car.car_type !== selectedCarType.value) return false

    if (priceRange.value) {
      const [min, max] = priceRange.value.split('-').map(Number)
      if (max) {
        if (car.price < min || car.price > max) return false
      } else {
        if (car.price < min) return false
      }
    }

    return true
  })
})

onMounted(() => {
  fetchBrandCars()
})
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in 0.8s ease-out forwards;
}
</style>
