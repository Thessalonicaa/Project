<template>
  <div>
    <!-- Loading Spinner -->
    <LoadingSpinner 
      :isLoading="loading" 
      loadingText="Loading brand cars..."
    />

    <div v-if="!loading" class="brandcars-page min-h-screen bg-gray-950 text-white relative overflow-hidden p-8">
    <!-- Beams Background -->
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

    <div class="max-w-7xl mx-auto relative z-10">

        <!-- Back Button -->
        <div class="mb-8 animate-slide-down">
          <button 
            @click="$router.back()"
            class="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg transition-all flex items-center gap-2 font-semibold"
          >
            <i class="fas fa-arrow-left"></i> Back to Cars
          </button>
        </div>

        <!-- Brand Header - Enhanced -->
        <div class="mb-12 animate-slide-down">
          <div class="bg-gradient-to-r from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-10 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-2xl">
            <div class="flex flex-col lg:flex-row items-center gap-10">
              <!-- Brand Logo Circle -->
              <div class="relative flex-shrink-0">
                <div class="absolute inset-0 bg-gradient-to-r from-red-600 to-orange-600 rounded-full blur-2xl opacity-40"></div>
                <div class="relative w-40 h-40 bg-gradient-to-br from-gray-800 to-gray-900 rounded-full flex items-center justify-center border-4 border-red-500 shadow-2xl overflow-hidden group hover:border-red-400 transition-all transform hover:scale-110 duration-300">
                  <img 
                    v-if="brandLogo" 
                    :src="brandLogo" 
                    :alt="selectedBrand" 
                    class="w-full h-full object-cover"
                  />
                  <i v-else class="fas fa-car text-6xl text-red-500 group-hover:text-red-400 transition-colors"></i>
                </div>
              </div>

              <!-- Brand Info -->
              <div class="flex-1">
                <h1 class="text-6xl font-extrabold bg-gradient-to-r from-red-500 via-red-400 to-orange-400 bg-clip-text text-transparent mb-3 drop-shadow-lg">
                  {{ selectedBrand }}
                </h1>
                <p class="text-xl text-gray-300 mb-6">Explore all available {{ selectedBrand }} vehicles in our inventory</p>
                
                <!-- Stats Grid -->
                <div class="grid grid-cols-3 gap-4">
                  <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-red-500/50 transition-all">
                    <p class="text-gray-400 text-sm mb-1 uppercase font-semibold">Total Cars</p>
                    <p class="text-white font-bold text-3xl">{{ brandCars.length }}</p>
                  </div>
                  <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-red-500/50 transition-all">
                    <p class="text-gray-400 text-sm mb-1 uppercase font-semibold">Min Price</p>
                    <p class="text-green-400 font-bold text-lg">฿{{ minPrice.toLocaleString('th-TH') }}</p>
                  </div>
                  <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-red-500/50 transition-all">
                    <p class="text-gray-400 text-sm mb-1 uppercase font-semibold">Max Price</p>
                    <p class="text-red-400 font-bold text-lg">฿{{ maxPrice.toLocaleString('th-TH') }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Header -->
        <div class="mb-8 animate-fade-in">
          <h2 class="text-3xl font-bold text-white mb-2">Browse Vehicles</h2>
          <p class="text-gray-400">Filter and find your perfect {{ selectedBrand }} vehicle</p>
        </div>

        <!-- Filters Section - Like CarList -->
        <div class="mb-8 flex flex-wrap gap-4 animate-fade-in-up">
          <select
            v-model="selectedFuelType"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">All Fuel Types</option>
            <option value="Petrol">Petrol </option>
            <option value="Diesel">Diesel </option>
            <option value="Hybrid">Hybrid </option>
            <option value="Electric">Electric </option>
          </select>

          <select
            v-model="selectedTransmission"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">All Transmissions</option>
            <option value="Automatic">Automatic </option>
            <option value="Manual">Manual </option>
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
            <option value="Sedan">Sedan</option>
            <option value="SUV">SUV</option>
            <option value="Pickup">Pickup </option>
            <option value="Van">Van </option>
            <option value="Sports">Sports </option>
            <option value="MPV">MPV</option>
            <option value="Convertible">Convertible</option>
            <option value="Coupe">Coupe</option>
            <option value="Hatchback">Hatchback</option>
          </select>

          <select
            v-model="priceRange"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">All Prices</option>
            <option value="0-500000">฿0 - ฿500,000</option>
            <option value="500000-1000000">฿500,000 - ฿1,000,000</option>
            <option value="1000000-2000000">฿1,000,000 - ฿2,000,000</option>
            <option value="2000000+">฿2,000,000+</option>
          </select>

          <select
            v-model="selectedColor"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">All Colors</option>
            <option v-for="color in uniqueColors" :key="color" :value="color">
              {{ color }}
            </option>
          </select>
        </div>

        <!-- Cars Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in-up">
          <div v-if="filteredCars.length === 0" class="col-span-full text-center py-16">
            <i class="fas fa-search text-6xl text-gray-600 mb-4"></i>
            <p class="text-gray-400 text-xl">No {{ selectedBrand }} cars found matching your criteria</p>
          </div>

          <div
            v-for="(car, index) in filteredCars"
            :key="car.id || car._id"
            class="bg-gray-900/80 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 hover:scale-105 opacity-0 animate-fade-in-up border border-gray-800 hover:border-red-500/50 group"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <!-- Image -->
            <div class="relative h-48 overflow-hidden rounded-t-2xl group/image">
              <img
                :src="car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/400x250?text=No+Image'"
                :alt="car.model"
                class="w-full h-full object-cover group-hover/image:scale-110 transition-transform duration-500"
              />
              <!-- Status Badge -->
              <div class="absolute top-4 right-4 bg-green-600 px-3 py-1 rounded-full text-xs font-bold text-white">
                <i class="fas fa-check-circle mr-1"></i>Available
              </div>
            </div>

            <!-- Content -->
            <div class="p-6">
              <!-- Title -->
              <h2 class="text-xl font-bold text-white mb-2 group-hover:text-red-400 transition-colors">
                {{ car.brand }} {{ car.model }}
              </h2>

              <!-- Year & Type -->
              <div class="flex justify-between items-center mb-3 text-sm text-gray-400">
                <span><i class="fas fa-calendar mr-2 text-red-500"></i>{{ car.year }}</span>
                <span v-if="car.car_type" class="bg-red-500/20 px-3 py-1 rounded-lg text-red-400 font-semibold text-xs">{{ car.car_type }}</span>
              </div>

              <!-- Fuel & Transmission -->
              <div v-if="car.fuel_type || car.transmission" class="flex gap-2 mb-4 flex-wrap">
                <span v-if="car.fuel_type" class="text-xs bg-blue-500/20 text-blue-400 px-3 py-1 rounded-lg font-semibold">
                  <i class="fas fa-gas-pump mr-1"></i>{{ car.fuel_type }}
                </span>
                <span v-if="car.transmission" class="text-xs bg-green-500/20 text-green-400 px-3 py-1 rounded-lg font-semibold">
                  <i class="fas fa-cog mr-1"></i>{{ car.transmission }}
                </span>
              </div>

              <!-- Additional Info -->
              <div class="grid grid-cols-2 gap-2 mb-4 text-xs text-gray-400">
                <div v-if="car.mileage" class="flex items-center">
                  <i class="fas fa-tachometer-alt text-red-500 mr-1"></i>
                  <span>{{ formatMileage(car.mileage) }} km</span>
                </div>
                <div v-if="car.color" class="flex items-center">
                  <i class="fas fa-palette text-pink-500 mr-1"></i>
                  <span>{{ car.color }}</span>
                </div>
              </div>

              <!-- Price -->
              <div class="flex items-baseline justify-between mb-4 pb-4 border-b border-gray-700">
                <p class="text-3xl font-bold text-red-500">
                  ฿{{ car.price.toLocaleString('th-TH') }}
                </p>
                <span class="text-xs text-gray-400">Est. Price</span>
              </div>

              <!-- Description -->
              <p class="text-gray-400 text-sm mb-4 line-clamp-2">{{ car.description }}</p>

              <!-- Button -->
              <NuxtLink
                :to="`/car/${car.id || car._id}`"
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
import Beams from '~/components/Beams.vue'

const route = useRoute()
const selectedBrand = ref('')
const brandLogo = ref('')
const brandCars = ref([])
const loading = ref(true)

const selectedFuelType = ref('')
const selectedTransmission = ref('')
const selectedCarType = ref('')
const priceRange = ref('')
const selectedColor = ref('')

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
    const brandParam = route.params.id
    // Capitalize first letter of each word
    const brand = brandParam
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join('-')
    
    selectedBrand.value = brand

    // Fetch all cars
    const response = await fetch('http://localhost:5000/api/cars')
    const data = await response.json()

    console.log('All cars from API:', data.cars?.length)
    console.log('Looking for brand:', brand)

    if (data.success) {
      // Filter cars by brand (case-insensitive for safety)
      const carsForBrand = data.cars.filter(car => {
        console.log('Comparing:', car.brand, '===', brand, '→', car.brand === brand)
        return car.brand === brand
      }) || []
      
      console.log('Cars found for brand:', carsForBrand.length)
      brandCars.value = carsForBrand

      // Set brand logo
      if (carsForBrand.length > 0) {
        // Try to use first car's image as brand representative
        brandLogo.value = carsForBrand[0].images?.[0] || ''
        
        // If no image, try to get from seller profile
        if (!brandLogo.value && carsForBrand[0].seller?.username) {
          try {
            const sellerRes = await fetch(
              `http://localhost:5000/api/get-profile?username=${carsForBrand[0].seller.username}`
            )
            const sellerData = await sellerRes.json()
            
            if (sellerData.success && sellerData.profileImageUrl) {
              brandLogo.value = sellerData.profileImageUrl
            }
          } catch (error) {
            console.log('Could not fetch seller profile:', error)
          }
        }
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

const uniqueColors = computed(() => {
  const colors = [...new Set(brandCars.value
    .map((car) => car.color)
    .filter((color) => color && color.trim() !== '')
  )]
  return colors.sort()
})

const formatMileage = (mileage) => {
  if (!mileage) return '0'
  return mileage.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const filteredCars = computed(() => {
  return brandCars.value.filter(car => {
    if (selectedFuelType.value && car.fuel_type !== selectedFuelType.value) return false
    if (selectedTransmission.value && car.transmission !== selectedTransmission.value) return false
    if (selectedCarType.value && car.car_type !== selectedCarType.value) return false
    if (selectedColor.value && car.color !== selectedColor.value) return false

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
.brandcars-page {
  position: relative;
}

.beams-background {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 0;
  opacity: 0.3;
  pointer-events: none;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-down {
  animation: fade-in 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.animate-fade-in-up {
  animation: fade-in 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.bg-gray-900\/80 {
  animation: fade-in 1s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
</style>
