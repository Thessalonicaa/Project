<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-950 p-8 text-gray-100">
    <div class="max-w-7xl mx-auto">
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
          <option value="Automatic">Automatic </option>
          <option value="Manual">Manual </option>
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

            <!-- Button -->
            <NuxtLink
              :to="`/car/${car.id}`"
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

const selectedBrand = ref("");
const priceRange = ref("");
const selectedFuelType = ref("");
const selectedTransmission = ref("");
const selectedCarType = ref("");
const cars = ref([]);
const loading = ref(true);
const route = useRoute();

const fetchCars = async () => {
  loading.value = true;
  try {
    const response = await fetch("http://localhost:5000/api/cars");
    const data = await response.json();

    if (data.success) {
      cars.value = data.cars || [];
    }
  } catch (error) {
    console.error("Error fetching cars:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await fetchCars();
});

watch(
  () => route.path,
  async () => {
    await fetchCars();
  },
  { immediate: false }
);

const brands = computed(() => [...new Set(cars.value.map((car) => car.brand))]);

const filteredCars = computed(() => {
  return cars.value.filter((car) => {
    if (selectedBrand.value && car.brand !== selectedBrand.value) return false;

    if (selectedFuelType.value && car.fuel_type !== selectedFuelType.value) return false;

    if (selectedTransmission.value && car.transmission !== selectedTransmission.value) return false;

    if (selectedCarType.value && car.car_type !== selectedCarType.value) return false;

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
/* Fade-in animations */
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
.animate-fade-in {
  animation: fade-in 1s ease-out forwards;
}
.animate-fade-in-up {
  animation: fade-in 0.8s ease-out forwards;
}
</style>
