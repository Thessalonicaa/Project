<template>
  <div class="min-h-screen bg-gray-950 text-white p-6">
    <div class="max-w-2xl mx-auto">
      <!-- Header with Animation -->
      <div class="text-center mb-8 animate-slide-down">
        <h1 class="text-5xl font-extrabold bg-gradient-to-r from-red-500 to-red-400 bg-clip-text text-transparent mb-2 drop-shadow-lg">
          <i class="fas fa-car-side mr-3"></i>Post Your Car
        </h1>
        <p class="text-gray-400 text-lg">ลงทะเบียนรถของคุณเพื่อขาย</p>
      </div>

      <!-- Seller Info Card -->
      <div class="bg-gradient-to-r from-red-600/20 to-red-800/20 border border-red-500/30 rounded-2xl p-6 mb-8 animate-fade-in backdrop-blur-sm">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-gradient-to-r from-red-600 to-red-700 rounded-full flex items-center justify-center shadow-lg">
            <i class="fas fa-user text-white text-lg"></i>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Seller:</p>
            <p class="text-white font-bold text-lg">{{ sellerName }}</p>
          </div>
        </div>
      </div>

      <!-- Form Container -->
      <form @submit.prevent="handleSubmit" class="bg-gray-900/80 border border-gray-800 rounded-2xl p-8 backdrop-blur-sm space-y-6 animate-slide-up">
        
        <!-- Car Brand -->
        <div class="form-group animate-form-item" style="animation-delay: 0.1s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-tag text-red-500 mr-2"></i>Brand
          </label>
          <input
            v-model="carData.brand"
            type="text"
            placeholder="e.g., Toyota, Honda, BMW"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            required
          />
        </div>

        <!-- Car Model -->
        <div class="form-group animate-form-item" style="animation-delay: 0.2s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-edit text-red-500 mr-2"></i>Model
          </label>
          <input
            v-model="carData.model"
            type="text"
            placeholder="e.g., Camry, Civic, X5"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            required
          />
        </div>

        <!-- Year and Price Row -->
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group animate-form-item" style="animation-delay: 0.3s">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-calendar text-red-500 mr-2"></i>Year
            </label>
            <input
              v-model="carData.year"
              type="number"
              placeholder="2023"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
              required
            />
          </div>

          <div class="form-group animate-form-item" style="animation-delay: 0.4s">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-dollar-sign text-red-500 mr-2"></i>Price (฿)
            </label>
            <input
              v-model="carData.price"
              type="number"
              placeholder="100000"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
              required
            />
          </div>
        </div>

        <!-- Fuel Type -->
        <div class="form-group animate-form-item" style="animation-delay: 0.45s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-gas-pump text-red-500 mr-2"></i>Fuel Type
          </label>
          <select
            v-model="carData.fuelType"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            required
          >
            <option value="">Select Fuel Type</option>
            <option value="Petrol">Petrol </option>
            <option value="Diesel">Diesel </option>
            <option value="Hybrid">Hybrid </option>
            <option value="Electric">Electric </option> 
          </select>
        </div>

        <!-- Transmission -->
        <div class="form-group animate-form-item" style="animation-delay: 0.5s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-cog text-red-500 mr-2"></i>Transmission
          </label>
          <select
            v-model="carData.transmission"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            required
          >
            <option value="">Select Transmission</option>
            <option value="Automatic">Automatic</option>
            <option value="Semi-Automatic">Semi-Automatic</option>
            <option value="Manual">Manual</option>
            <option value="CVT">CVT</option>
            <option value="e-CVT">e-CVT</option>
            <option value="DCT">DCT</option>
          </select>
        </div>

        <!-- Car Type -->
        <div class="form-group animate-form-item" style="animation-delay: 0.55s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-car-side text-red-500 mr-2"></i>Car Type
          </label>
          <select
            v-model="carData.carType"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            required
          >
            <option value="">Select Car Type</option>
            <option value="Sedan">Sedan </option>
            <option value="SUV">SUV</option>
            <option value="Pickup">Pickup </option>
            <option value="Van">Van </option>
            <option value="Sports">Sports </option>
          </select>
        </div>

        <!-- License Plate -->
        <div class="form-group animate-form-item" style="animation-delay: 0.5s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-id-card text-red-500 mr-2"></i>License Plate
          </label>
          <input
            v-model="carData.licensePlate"
            type="text"
            placeholder="ABC 1234"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
          />
        </div>

        <!-- Description -->
        <div class="form-group animate-form-item" style="animation-delay: 0.6s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-align-left text-red-500 mr-2"></i>Description
          </label>
          <textarea
            v-model="carData.description"
            placeholder="Describe your car in detail..."
            rows="4"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all resize-none"
          ></textarea>
        </div>

        <!-- Image Upload -->
        <div class="form-group animate-form-item" style="animation-delay: 0.7s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-image text-red-500 mr-2"></i>Upload Images
          </label>
          <label class="flex items-center justify-center w-full px-4 py-6 border-2 border-dashed border-gray-700 rounded-xl cursor-pointer hover:border-red-500 hover:bg-gray-800/50 transition-all group">
            <div class="text-center">
              <i class="fas fa-cloud-upload-alt text-3xl text-gray-500 group-hover:text-red-500 transition-colors mb-2"></i>
              <p class="text-gray-300">Click to upload images</p>
              <p class="text-gray-500 text-sm">PNG, JPG up to 10MB</p>
            </div>
            <input
              type="file"
              multiple
              accept="image/*"
              class="hidden"
              @change="onFilesSelected"
            />
          </label>
        </div>

        <!-- Image Previews -->
        <div v-if="previewImages.length > 0" class="form-group animate-form-item" style="animation-delay: 0.8s">
          <p class="text-gray-300 font-semibold mb-3">Preview Images ({{ previewImages.length }})</p>
          <div class="grid grid-cols-3 gap-3">
            <div
              v-for="(image, index) in previewImages"
              :key="index"
              class="relative group"
            >
              <img :src="image" :alt="`Preview ${index}`" class="w-full h-24 object-cover rounded-lg border border-gray-700 group-hover:border-red-500 transition-all" />
              <button
                type="button"
                @click="removeImage(index)"
                class="absolute top-1 right-1 bg-red-600 hover:bg-red-700 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <i class="fas fa-times text-sm"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold py-3 px-6 rounded-xl transition-all transform hover:scale-105 duration-200 submitBtn animate-form-item shadow-lg"
          id="submitBtn"
          style="animation-delay: 0.9s"
        >
          <i class="fas fa-upload mr-2"></i>Post Car Listing
        </button>
      </form>
    </div>
  </div>

  <!-- Success Modal -->
  <SuccessModal
    :show="showSuccessModal"
    title="โพสต์รถสำเร็จ!"
    message="รถของคุณถูกลงทะเบียนเรียบร้อยแล้ว"
    icon="✅"
    :duration="3"
    @close="handleSuccessClose"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const carData = ref({
  brand: '',
  model: '',
  year: new Date().getFullYear(),
  price: '',
  licensePlate: '',
  description: '',
  fuelType: '',
  transmission: '',
  carType: ''
})

const previewImages = ref([])
const sellerName = ref('')
const showSuccessModal = ref(false)

onMounted(() => {
  if (process.client) {
    sellerName.value = localStorage.getItem('username') || 'Seller'
  }
})

const onFilesSelected = (event) => {
  const files = event.target.files
  if (files) {
    Array.from(files).forEach((file) => {
      const reader = new FileReader()
      reader.onload = (e) => {
        previewImages.value.push(e.target.result)
      }
      reader.readAsDataURL(file)
    })
  }
}

const removeImage = (index) => {
  previewImages.value.splice(index, 1)
}

const handleSuccessClose = () => {
  showSuccessModal.value = false
  router.push('/dashboard')
}

const handleSubmit = async () => {
  try {
    // Validate required fields
    if (!carData.value.brand || !carData.value.model || !carData.value.year || !carData.value.price) {
      alert('Please fill in all required fields')
      return
    }

    const token = localStorage.getItem('token')
    if (!token) {
      alert('You must be logged in to post a car')
      return
    }

    // Show loading animation
    const submitBtn = document.getElementById('submitBtn')
    if (submitBtn) {
      submitBtn.classList.add('animate-post-loading')
      submitBtn.disabled = true
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Posting...'
    }

    // Create payload with car data
    const payload = {
      brand: carData.value.brand,
      model: carData.value.model,
      year: parseInt(carData.value.year),
      licensePlate: carData.value.licensePlate,
      description: carData.value.description,
      price: parseFloat(carData.value.price),
      fuel_type: carData.value.fuelType,
      transmission: carData.value.transmission,
      car_type: carData.value.carType,
      images: previewImages.value
    }

    // Send to backend
    const response = await fetch('http://localhost:5000/api/cars', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    })

    const data = await response.json()
    
    if (response.ok && data.success) {
      // Show success animation
      if (submitBtn) {
        submitBtn.classList.remove('animate-post-loading')
        submitBtn.classList.add('animate-post-success')
        submitBtn.innerHTML = '<i class="fas fa-check mr-2"></i>Posted Successfully!'
      }

      setTimeout(() => {
        showSuccessModal.value = true
      }, 500)
    } else {
      if (submitBtn) {
        submitBtn.classList.remove('animate-post-loading')
        submitBtn.disabled = false
        submitBtn.innerHTML = '<i class="fas fa-upload mr-2"></i>Post Car Listing'
      }
      alert('Error: ' + (data.message || data.error || 'Failed to post car'))
    }

  } catch (error) {
    console.error('Error posting car:', error)
    const submitBtn = document.getElementById('submitBtn')
    if (submitBtn) {
      submitBtn.classList.remove('animate-post-loading')
      submitBtn.disabled = false
      submitBtn.innerHTML = '<i class="fas fa-upload mr-2"></i>Post Car Listing'
    }
    alert('Failed to post car: ' + error.message)
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

.animate-slide-down {
  animation: slideDown 0.6s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.6s ease-out;
}

.animate-form-item {
  animation: formItem 0.5s ease-out forwards;
  opacity: 0;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
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

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

@keyframes postLoading {
  0% {
    background: linear-gradient(to right, #dc2626, #b91c1c);
  }
  50% {
    background: linear-gradient(to right, #f97316, #ea580c);
  }
  100% {
    background: linear-gradient(to right, #dc2626, #b91c1c);
  }
}

@keyframes postSuccess {
  0% {
    background: #dc2626;
    transform: scale(1);
  }
  50% {
    background: #22c55e;
    transform: scale(1.05);
  }
  100% {
    background: #22c55e;
    transform: scale(1);
  }
}

.animate-post-loading {
  animation: postLoading 0.6s ease-in-out infinite;
}

.animate-post-success {
  animation: postSuccess 1s ease-in-out forwards;
  background-color: #22c55e !important;
}
</style>
