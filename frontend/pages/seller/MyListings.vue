<template>
  <div class="mylistings-page min-h-screen bg-gray-950 text-white p-6 relative overflow-hidden">
    <!-- Beams Background -->
    <div class="beams-background">
      <Beams
        :beamWidth="3"
        :beamHeight="25"
        :beamNumber="10"
        lightColor="#ff3c03"
        :speed="1.2"
        :noiseIntensity="1.7"
        :scale="0.22"
        :rotation="10"
        :width="1920"
        :height="1080"
      />
    </div>

    <div class="max-w-6xl mx-auto relative z-10">
      <!-- Header -->
      <div class="text-center mb-8 animate-slide-down">
        <h1 class="text-4xl font-extrabold text-red-500 mb-2 drop-shadow-lg">
          <i class="fas fa-list mr-3"></i>My Car Listings
        </h1>
        <p class="text-gray-400">Manage Your Car Listings</p>
      </div>

      <!-- No Listings -->
      <div v-if="sellerCars.length === 0" class="text-center py-16 animate-fade-in">
        <i class="fas fa-inbox text-6xl text-gray-600 mb-4"></i>
        <p class="text-2xl text-gray-400 mb-6">No Cars Listed Yet</p>
        <button
          @click="handlePostCarClick"
          class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-xl transition-colors font-semibold"
        >
          <i class="fas fa-plus mr-2"></i>Post a Car for Sale
        </button>
      </div>

      <!-- Listings Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
        <div
          v-for="(car, index) in sellerCars"
          :key="car.id || car._id"
          :data-car-id="car.id || car._id"
          class="bg-gray-800/50 rounded-xl overflow-hidden border border-gray-700 hover:border-red-500 transition-all transform hover:-translate-y-2 duration-300 animate-form-item relative"
          :style="{ 'animation-delay': `${index * 0.1}s` }"
        >
          <!-- Image Container -->
          <div class="relative h-48 overflow-hidden group">
            <img
              :src="car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/300x200?text=No+Image'"
              :alt="car.model"
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
            />
            <!-- Sold Out Badge -->
            <div v-if="car.sold_out" class="absolute inset-0 bg-black/70 flex items-center justify-center">
              <span class="text-3xl font-bold text-red-500">SOLD OUT</span>
            </div>
            <!-- Sold Out Stripe -->
            <div v-if="car.sold_out" class="absolute inset-0 bg-gradient-to-br from-red-600 to-transparent opacity-40 transform -rotate-45 origin-center"></div>
          </div>

          <!-- Content -->
          <div class="p-4 space-y-3">
            <!-- Title -->
            <div>
              <h3 class="text-lg font-bold text-white">{{ car.brand }} {{ car.model }}</h3>
              <p class="text-sm text-gray-400">ปี {{ car.year }}</p>
            </div>

            <!-- Price -->
            <div class="flex justify-between items-center">
              <p v-if="!car.sold_out" class="text-red-500 font-bold text-lg">฿{{ formatPrice(car.price) }}</p>
              <p v-else class="text-red-500 font-bold text-lg line-through opacity-50">฿{{ formatPrice(car.price) }}</p>
              <span v-if="car.sold_out" class="px-3 py-1 bg-red-600 rounded-full text-xs font-semibold">
                Sold
              </span>
              <span v-else class="px-3 py-1 bg-green-600 rounded-full text-xs font-semibold">
                Active
              </span>
            </div>

            <!-- License Plate -->
            <p class="text-xs text-gray-500">License: {{ car.license_plate }}</p>

            <!-- Auto-delete Countdown -->
            <div v-if="car.sold_out" class="text-xs text-orange-400 bg-orange-500/20 rounded px-2 py-1 text-center">
              <i class="fas fa-hourglass-end mr-1"></i>Will be deleted in 3 minutes
            </div>

            <!-- Actions -->
            <div class="flex gap-2 pt-2">
              <NuxtLink
                :to="`/car/${car.id || car._id}`"
                class="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-sm font-semibold text-center"
              >
                <i class="fas fa-eye mr-1"></i>View
              </NuxtLink>

              <button
                v-if="!car.sold_out"
                @click="markAsSoldOut(car.id || car._id)"
                class="flex-1 px-3 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg transition-colors text-sm font-semibold"
              >
                <i class="fas fa-check mr-1"></i>Sold
              </button>

              <button
                v-else
                @click="markAsActive(car.id || car._id)"
                class="flex-1 px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors text-sm font-semibold"
              >
                <i class="fas fa-redo mr-1"></i>Active
              </button>

              <button
                @click="deleteListing(car.id || car._id)"
                class="flex-1 px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors text-sm font-semibold animate-pulse-subtle"
              >
                <i class="fas fa-trash mr-1"></i>Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete Confirm Modal -->
  <teleport to="body">
    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70">
        <div class="bg-gray-900 rounded-2xl p-8 max-w-sm w-full mx-4 animate-pop-in">
          <h2 class="text-2xl font-bold text-white mb-4">Delete Listing?</h2>
          <p class="text-gray-300 mb-6">Are you sure you want to delete this listing?</p>
          <div class="flex gap-3">
            <button
              @click="showDeleteModal = false"
              class="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
            >
              ยกเลิก
            </button>
            <button
              @click="confirmDelete"
              class="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors font-semibold"
            >
              ลบ
            </button>
          </div>
        </div>
      </div>
    </transition>
  </teleport>

  <!-- Success Modal -->
  <SuccessModal
    :show="showSuccessModal"
    :title="successMessage.title"
    :message="successMessage.message"
    icon="✅"
    :duration="3"
    @close="showSuccessModal = false"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Beams from '~/components/Beams.vue'

const router = useRouter()
const sellerCars = ref([])
const showDeleteModal = ref(false)
const showSuccessModal = ref(false)
const deletingCarId = ref(null)
const successMessage = ref({ title: '', message: '' })
const autoDeleteTimers = ref({}) // Track auto-delete timers

const formatPrice = (price) => {
  return new Intl.NumberFormat('th-TH').format(price)
}

const handlePostCarClick = () => {
  const isSeller = localStorage.getItem('is_seller')
  const role = localStorage.getItem('role')
  
  // Check if user is seller
  if (isSeller !== 'true' && role !== 'seller') {
    // Not a seller, redirect to Register Seller page
    router.push('/Register-seller')
  } else {
    // Already a seller, go to PostCar
    router.push('/seller/PostCar')
  }
}

onMounted(async () => {
  await fetchSellerCars()
})


const fetchSellerCars = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.log('No token found')
      sellerCars.value = []
      return
    }

    console.log('Fetching seller cars with token...')
    
    // Get cars for current logged-in seller
    const response = await fetch('http://localhost:5000/api/cars/my-listings', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()
    console.log('Cars response:', data)

    if (data.success && Array.isArray(data.cars)) {
      sellerCars.value = data.cars
      console.log('Cars loaded:', sellerCars.value.length)
    } else {
      console.log('No cars found')
      sellerCars.value = []
    }
  } catch (error) {
    console.error('Error fetching seller cars:', error)
    sellerCars.value = []
  }
}

const markAsSoldOut = async (carId) => {
  try {
    const response = await fetch(`http://localhost:5000/api/cars/${carId}/sold`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ sold_out: true })
    })

    if (response.ok) {
      const car = sellerCars.value.find(c => (c.id || c._id) === carId)
      if (car) {
        car.sold_out = true
        
        // Show sold out animation
        showSoldOutAnimation(carId)
        
        successMessage.value = {
          title: 'Marked as Sold Out',
          message: 'This car has been marked as sold out'
        }
        showSuccessModal.value = true
        
        // Auto-delete after 3 minutes (180000ms)
        setTimeout(async () => {
          try {
            const deleteResponse = await fetch(`http://localhost:5000/api/cars/${carId}`, {
              method: 'DELETE',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
              }
            })
            
            if (deleteResponse.ok) {
              sellerCars.value = sellerCars.value.filter(c => (c.id || c._id) !== carId)
            }
          } catch (error) {
            console.error('Error auto-deleting car:', error)
          }
        }, 180000) // 3 minutes
      }
    }
  } catch (error) {
    console.error('Error marking as sold out:', error)
  }
}

const showSoldOutAnimation = (carId) => {
  // Find the card element
  const cardElement = document.querySelector(`[data-car-id="${carId}"]`)
  if (!cardElement) return
  
  // Create sold out notification
  const notification = document.createElement('div')
  notification.className = 'sold-out-notification'
  notification.innerHTML = `
    <div class="sold-out-text">
      <i class="fas fa-check-circle"></i> SOLD OUT
    </div>
  `
  
  cardElement.appendChild(notification)
  
  // Remove after animation
  setTimeout(() => {
    notification.remove()
  }, 2000)
}

const markAsActive = async (carId) => {
  try {
    const response = await fetch(`http://localhost:5000/api/cars/${carId}/sold`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ sold_out: false })
    })

    if (response.ok) {
      const car = sellerCars.value.find(c => (c.id || c._id) === carId)
      if (car) {
        car.sold_out = false
        
        successMessage.value = {
          title: 'Reactivated',
          message: 'This car has been reactivated for sale'
        }
        showSuccessModal.value = true
      }
    } else {
      const errorData = await response.json()
      alert('❌ Error: ' + (errorData.message || 'Failed to update status'))
    }
  } catch (error) {
    console.error('Error marking as active:', error)
    alert('❌ Error: ' + error.message)
  }
}

const deleteListing = (carId) => {
  deletingCarId.value = carId
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    const token = localStorage.getItem('token')
    
    if (!token) {
      alert('❌ No authentication token found')
      return
    }

    const response = await fetch(`http://localhost:5000/api/cars/${deletingCarId.value}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })

    const data = await response.json()

    if (response.ok && data.success) {
      sellerCars.value = sellerCars.value.filter(car => (car.id || car._id) !== deletingCarId.value)
      showDeleteModal.value = false
      deletingCarId.value = null
      
      successMessage.value = {
        title: 'Deleted Successfully',
        message: 'This listing has been deleted'
      }
      showSuccessModal.value = true
    } else {
      alert('❌ Error: ' + (data.message || 'Failed to delete car'))
    }
  } catch (error) {
    console.error('Error deleting car:', error)
    alert('❌ Error deleting listing: ' + error.message)
  }
}
</script>

<style scoped>
.mylistings-page {
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

.animate-slide-down {
  animation: slideDown 0.6s ease-out both;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out both;
}

.animate-form-item {
  animation: formItem 0.5s ease-out forwards both;
  opacity: 0;
}

.animate-pulse-subtle {
  animation: pulseSoft 2s ease-in-out infinite;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes formItem {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulseSoft {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

@keyframes popIn {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-pop-in {
  animation: popIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.sold-out-notification {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 50;
  animation: soldOutPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.sold-out-text {
  background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
  color: white;
  padding: 20px 40px;
  border-radius: 12px;
  font-size: 24px;
  font-weight: bold;
  box-shadow: 0 20px 60px rgba(220, 38, 38, 0.5);
  border: 2px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 12px;
}

.sold-out-text i {
  font-size: 28px;
  animation: checkmark 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes soldOutPop {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.5) rotateZ(-10deg);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.1) rotateZ(5deg);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1) rotateZ(0deg);
  }
}

@keyframes checkmark {
  0% {
    transform: scale(0) rotateZ(-45deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.2) rotateZ(10deg);
  }
  100% {
    transform: scale(1) rotateZ(0deg);
    opacity: 1;
  }
}
</style>
