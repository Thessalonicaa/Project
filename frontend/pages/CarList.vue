<template>
  <div class="carlist-page min-h-screen bg-gray-950 p-8 text-gray-100 relative overflow-hidden">
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

    <div class="max-w-7xl mx-auto relative z-10">
      <!-- Header -->
      <div class="mb-12 animate-fade-in">
        <h1 class="text-5xl font-extrabold text-white mb-3 tracking-wide">
          Available Cars
        </h1>
        <p class="text-gray-400 text-lg">Browse and find your perfect vehicle</p>
      </div>

      <!-- Filters -->
      <div class="mb-8 flex flex-wrap gap-4 animate-fade-in-up">
        <select
          v-model="selectedVehicleType"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">All Vehicle Types</option>
          <option value="Car">Car </option>
          <option value="Motorcycle">Motorcycle </option>
          <option value="Bike">Bike </option>
        </select>

        <select
          v-model="selectedBrand"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">All Brands</option>
          <option v-for="brand in brands" :key="brand" :value="brand">
            {{ brand }}
          </option>
        </select>

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
            <option value="Automatic">Automatic</option>
            <option value="Semi-Automatic">Semi-Automatic</option>
            <option value="Manual">Manual</option>
            <option value="CVT">CVT</option>
            <option value="e-CVT">e-CVT</option>
            <option value="DCT">DCT</option>
        </select>

        <select
          v-model="selectedCarType"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">All Car Types</option>
          <option value="Sedan">Sedan </option>
          <option value="SUV">SUV</option>
          <option value="Pickup">Pickup </option>
          <option value="Van">Van </option>
          <option value="Sports">Sports </option>
          <option value="MPV">MPV</option>
          <option value="Convertible">Convertible</option>
          <option value="Coupe">Coupe</option>
          <option value="Hatchback">Hatchback</option>
          <option value="Roadster">Roadster</option>
        </select>

        <!-- Dynamic Filter: MPV Size -->
        <select
          v-if="selectedCarType === 'MPV'"
          v-model="selectedMpvSize"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">All MPV Sizes</option>
          <option value="Compact">Compact MPV</option>
          <option value="Mid-Size">Mid-Size MPV</option>
          <option value="Full-Size">Full-Size MPV</option>
        </select>

        <!-- Dynamic Filter: Convertible Options -->
        <select
          v-if="selectedCarType === 'Convertible'"
          v-model="selectedConvertibleTop"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">All Top Types</option>
          <option value="Soft Top">Soft Top</option>
          <option value="Retractable Hard Top">Retractable Hard Top</option>
        </select>

        <!-- Dynamic Filter: Van Type -->
        <select
          v-if="selectedCarType === 'Van'"
          v-model="selectedVanType"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">All Van Types</option>
          <option value="Cargo Van">Cargo Van</option>
          <option value="Minivan">Minivan</option>
        </select>

        <!-- Dynamic Filter: SUV Seats -->
        <select
          v-if="selectedCarType === 'SUV'"
          v-model="selectedSuvSeats"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">All Seat Capacities</option>
          <option value="2 Seats">2 Seats</option>
          <option value="4 Seats">4 Seats</option>
        </select>

        <!-- Dynamic Filter: Pickup Cab -->
        <select
          v-if="selectedCarType === 'Pickup'"
          v-model="selectedPickupCab"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">All Cab Types</option>
          <option value="Single Cab">Single Cab – 2 Seats</option>
          <option value="Extra Cab">Extra Cab – 2 Seats</option>
          <option value="Double Cab">Double Cab – 4 Seats</option>
        </select>

        <!-- Color Filter -->
        <select
          v-model="selectedColor"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">All Colors</option>
          <option v-for="color in colors" :key="color" :value="color">
            {{ color }}
          </option>
        </select>

        <!-- Engine Size Filter -->
        <select
          v-model="selectedEngineSize"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">All Engine Sizes</option>
          <option v-for="engine in engineSizes" :key="engine" :value="engine">
            {{ engine }}
          </option>
        </select>
      </div>

      <!-- Car Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in-up">
        <div v-if="loading" class="col-span-full text-center py-16">
          <div class="inline-flex flex-col items-center">
            <div class="w-12 h-12 border-4 border-red-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p class="text-gray-400 text-lg">Loading cars...</p>
          </div>
        </div>

        <div
          v-for="(car, index) in filteredCars"
          :key="car.id || car._id"
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

            <!-- Year -->
            <p class="text-sm text-gray-400 mb-3">
              <i class="fas fa-calendar mr-2"></i>Year: {{ car.year }}
            </p>

            <!-- Price -->
            <div class="flex items-baseline justify-between mb-4">
              <p class="text-3xl font-bold text-red-500">
                ฿{{ car.price.toLocaleString('th-TH') }}
              </p>
              <span class="text-sm text-gray-400">Total</span>
            </div>

            <!-- Description -->
            <p class="text-gray-400 text-sm mb-4 line-clamp-2">{{ car.description }}</p>

            <!-- Additional Info -->
            <div class="grid grid-cols-2 gap-2 mb-4 text-xs text-gray-400">
              <div v-if="car.mileage" class="flex items-center">
                <i class="fas fa-tachometer-alt text-red-500 mr-1"></i>
                <span>{{ formatMileage(car.mileage) }} km</span>
              </div>
              <div v-if="car.fuel_type" class="flex items-center">
                <i class="fas fa-gas-pump text-orange-500 mr-1"></i>
                <span>{{ car.fuel_type }}</span>
              </div>
              <div v-if="car.transmission" class="flex items-center">
                <i class="fas fa-cog text-blue-500 mr-1"></i>
                <span>{{ car.transmission }}</span>
              </div>
              <div v-if="car.gas_system" class="flex items-center">
                <i class="fas fa-water text-cyan-500 mr-1"></i>
                <span>{{ car.gas_system }}</span>
              </div>
              <div v-if="car.color" class="flex items-center">
                <i class="fas fa-palette text-pink-500 mr-1"></i>
                <span>{{ car.color }}</span>
              </div>
              <div v-if="car.engine_size" class="flex items-center">
                <i class="fas fa-cube text-purple-500 mr-1"></i>
                <span>{{ car.engine_size }}</span>
              </div>
            </div>

            <!-- Button -->
            <NuxtLink
              :to="`/car/${car.id || car._id}`"
              class="w-full inline-block py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 duration-300 text-center shadow-lg"
            >
              <i class="fas fa-eye mr-2"></i>View Details
            </NuxtLink>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredCars.length === 0 && !loading" class="col-span-full text-center py-16">
          <i class="fas fa-search text-6xl text-gray-600 mb-4"></i>
          <p class="text-gray-400 text-xl">No cars found matching your criteria</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import Beams from "~/components/Beams.vue"

const selectedBrand = ref("");
const priceRange = ref("");
const selectedFuelType = ref("");
const selectedTransmission = ref("");
const selectedCarType = ref("");
const selectedMpvSize = ref("");
const selectedConvertibleTop = ref("");
const selectedVanType = ref("");
const selectedSuvSeats = ref("");
const selectedPickupCab = ref("");
const selectedColor = ref("");
const selectedEngineSize = ref("");
const selectedVehicleType = ref("");
const cars = ref([]);
const loading = ref(true);
const route = useRoute();

const fetchCars = async () => {
  loading.value = true;
  try {
    console.log('Fetching cars from API...');
    const response = await fetch('http://localhost:5000/api/cars');
    console.log('Response status:', response.status);
    
    const data = await response.json();
    console.log('Cars data:', data);
    console.log('Engine sizes in data:', data.cars?.map(c => c.engine_size).filter(e => e));

    if (data.success) {
      cars.value = data.cars || [];
      console.log('Cars loaded:', cars.value.length);
      console.log('Unique engine sizes:', [...new Set(cars.value.map(c => c.engine_size).filter(e => e))]);
    } else {
      console.log('API returned success: false');
      cars.value = [];
    }
  } catch (error) {
    console.error('Error fetching cars:', error);
    cars.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  console.log('CarList mounted - fetching cars');
  await fetchCars();
  // Refetch cars every 10 seconds to stay updated
  setInterval(fetchCars, 10000);
});

watch(
  () => route.path,
  async () => {
    console.log('Route changed - refetching cars');
    await fetchCars();
  },
  { immediate: false }
);

const brands = computed(() => [...new Set(cars.value.map((car) => car.brand))]);

const colors = computed(() => {
  const uniqueColors = [...new Set(cars.value
    .map((car) => car.color)
    .filter((color) => color && color.trim() !== '')
  )];
  return uniqueColors.sort();
});

const engineSizes = computed(() => {
  const uniqueEngineSizes = [...new Set(cars.value
    .map((car) => car.engine_size)
    .filter((engine) => engine && engine.trim() !== '')
  )];
  return uniqueEngineSizes.sort();
});

const formatMileage = (mileage) => {
  if (!mileage) return '0'
  return mileage.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const filteredCars = computed(() => {
  return cars.value.filter((car) => {
    // Vehicle Type filter
    if (selectedVehicleType.value && car.vehicle_type !== selectedVehicleType.value) return false;

    if (selectedBrand.value && car.brand !== selectedBrand.value) return false;

    if (selectedFuelType.value && car.fuel_type !== selectedFuelType.value) return false;

    if (selectedTransmission.value && car.transmission !== selectedTransmission.value) return false;

    if (selectedCarType.value && car.car_type !== selectedCarType.value) return false;

    // Dynamic filter: MPV Size
    if (selectedMpvSize.value && car.mpv_size !== selectedMpvSize.value) return false;

    // Dynamic filter: Convertible Top
    if (selectedConvertibleTop.value && car.convertible_top !== selectedConvertibleTop.value) return false;

    // Dynamic filter: Van Type
    if (selectedVanType.value && car.van_type !== selectedVanType.value) return false;

    // Dynamic filter: SUV Seats
    if (selectedSuvSeats.value && car.suv_seats !== selectedSuvSeats.value) return false;

    // Dynamic filter: Pickup Cab
    if (selectedPickupCab.value && car.pickup_cab !== selectedPickupCab.value) return false;

    // Color filter (exact match)
    if (selectedColor.value && car.color !== selectedColor.value) return false;

    // Engine Size filter (exact match)
    if (selectedEngineSize.value && car.engine_size !== selectedEngineSize.value) return false;

    // Price range filter
    if (priceRange.value) {
      const [min, max] = priceRange.value.split("-").map(Number);
      if (max) {
        if (car.price < min || car.price > max) return false;
      } else {
        if (car.price < min) return false;
      }
    }

    return true;
  });
});
</script>

<style scoped>
.carlist-page {
  position: relative;
}

/* Fade-in animations */
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
.animate-fade-in {
  animation: fade-in 1s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
.animate-fade-in-up {
  animation: fade-in 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

/* Card hover effect enhancement */
.group:hover {
  box-shadow: 0 0 30px rgba(239, 68, 68, 0.2);
}
</style>
