<template>
  <div class="min-h-screen bg-gray-950 text-white p-6 relative overflow-hidden">
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
    <div class="max-w-6xl mx-auto relative z-10">
      
      <!-- Profile Header -->
      <div class="bg-gradient-to-r from-gray-900/80 via-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-10 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 mb-8 shadow-2xl">
        <div class="flex flex-col md:flex-row items-center gap-10">
          <!-- Avatar with enhanced styling -->
          <div class="relative group flex-shrink-0">
            <div class="absolute inset-0 bg-gradient-to-r from-red-600 to-orange-600 rounded-full blur-2xl opacity-40 group-hover:opacity-60 transition-opacity duration-300"></div>
            <div class="relative w-40 h-40">
              <img 
                v-if="profileImageUrl" 
                :src="profileImageUrl" 
                alt="Profile" 
                class="w-40 h-40 object-cover rounded-full border-4 border-red-500 shadow-2xl group-hover:scale-110 transition-transform duration-300"
              />
              <div v-else class="w-40 h-40 bg-gradient-to-br from-red-600 to-orange-600 rounded-full flex items-center justify-center border-4 border-red-500 shadow-2xl group-hover:scale-110 transition-transform duration-300">
                <i class="fas fa-user text-7xl text-white"></i>
              </div>

              <!-- Upload button overlay -->
              <label 
                v-if="isOwnProfile"
                for="file-upload" 
                class="absolute bottom-2 right-2 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 p-4 rounded-full cursor-pointer transition-all transform hover:scale-125 shadow-lg border-2 border-red-500/50"
              >
                <i class="fas fa-camera text-white text-xl"></i>
              </label>
              <input id="file-upload" type="file" class="hidden" @change="onFileSelected" accept="image/*" />
            </div>
          </div>

          <!-- User Info -->
          <div class="flex-1 text-center md:text-left">
            <h1 class="text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-red-500 via-orange-500 to-red-500 bg-clip-text text-transparent mb-3 drop-shadow-lg">
              {{ viewingUsername }}
            </h1>
            <p class="text-xl text-gray-300 mb-6 flex items-center gap-2 justify-center md:justify-start">
              <i :class="[isSeller ? 'fas fa-store text-red-500' : 'fas fa-user text-blue-500']"></i>
              {{ isSeller ? ' Seller Account' : ' User Account' }}
            </p>
            <p class="text-gray-400 text-sm mb-6">Member since {{ memberSince }}</p>
          </div>

          <!-- Quick Stats -->
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-gradient-to-br from-red-600/20 to-red-700/10 p-6 rounded-2xl border border-red-500/30 hover:border-red-500/60 transition-all text-center hover:scale-105 transform duration-300">
              <p class="text-red-200 text-xs uppercase font-bold tracking-wider mb-2">Cars Listed</p>
              <p class="text-red-400 font-extrabold text-4xl drop-shadow-lg">{{ stats.totalProducts }}</p>
            </div>
            <div class="bg-gradient-to-br from-blue-600/20 to-blue-700/10 p-6 rounded-2xl border border-blue-500/30 hover:border-blue-500/60 transition-all text-center hover:scale-105 transform duration-300">
              <p class="text-blue-200 text-xs uppercase font-bold tracking-wider mb-2">Last Active</p>
              <p class="text-blue-400 font-extrabold text-2xl drop-shadow-lg">Today</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Grid -->
      <div class="grid lg:grid-cols-3 gap-8">

        <!-- Left Section - Account Info -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Account Information -->
          <div class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl p-8 rounded-2xl border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-3 text-white">
              <i class="fas fa-user-circle text-red-500 text-2xl"></i>
              Account Info
            </h2>
            <div class="space-y-5">
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-red-500/50 transition-all">
                <p class="text-gray-400 text-xs uppercase font-bold tracking-wider mb-2">Username</p>
                <p class="text-white font-bold text-lg">{{ viewingUsername }}</p>
              </div>
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-red-500/50 transition-all">
                <p class="text-gray-400 text-xs uppercase font-bold tracking-wider mb-2">Account Type</p>
                <p :class="['font-bold text-lg', isSeller ? 'text-red-400' : 'text-blue-400']">
                  {{ isSeller ? ' Seller' : ' User' }}
                </p>
              </div>
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-red-500/50 transition-all">
                <p class="text-gray-400 text-xs uppercase font-bold tracking-wider mb-2">Member Since</p>
                <p class="text-white font-bold text-lg">{{ memberSince }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Middle Section - Business Info / Activity -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Seller Information -->
          <div v-if="isSeller" class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl p-8 rounded-2xl border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-3 text-white">
              <i class="fas fa-briefcase text-red-500 text-2xl"></i>
              Business Info
            </h2>
            <div class="space-y-4">
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                <p class="text-gray-400 text-xs uppercase font-bold tracking-wider mb-2">Business Name</p>
                <p class="text-white font-bold text-sm">{{ businessName || 'Not Set' }}</p>
              </div>
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                <p class="text-gray-400 text-xs uppercase font-bold tracking-wider mb-2">Email</p>
                <p class="text-white font-bold text-sm break-all">{{ sellerEmail || 'Not Set' }}</p>
              </div>
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                <p class="text-gray-400 text-xs uppercase font-bold tracking-wider mb-2">Phone</p>
                <p class="text-white font-bold text-sm">{{ phoneNumber || 'Not Set' }}</p>
              </div>
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                <p class="text-gray-400 text-xs uppercase font-bold tracking-wider mb-2">Address</p> 
                <p class="text-white font-bold text-sm">{{ contactInfo || 'Not Set' }}</p>
              </div>
            </div>
          </div>

          <!-- Activity Section for Non-Sellers -->
          <div v-else class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl p-8 rounded-2xl border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-3 text-white">
              <i class="fas fa-chart-bar text-blue-500 text-2xl"></i>
              Stats
            </h2>
            <div class="space-y-4">
              <div class="bg-gradient-to-br from-red-600/20 to-red-700/10 p-6 rounded-xl border border-red-500/30 hover:border-red-500/60 transition-all">
                <p class="text-red-200 text-xs uppercase font-bold tracking-wider mb-2">Cars Listed</p>
                <p class="text-red-400 font-extrabold text-3xl">{{ stats.totalProducts }}</p>
              </div>
              <div class="bg-gradient-to-br from-blue-600/20 to-blue-700/10 p-6 rounded-xl border border-blue-500/30 hover:border-blue-500/60 transition-all">
                <p class="text-blue-200 text-xs uppercase font-bold tracking-wider mb-2">Member Since</p>
                <p class="text-blue-400 font-bold text-sm">{{ memberSince }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Section - Activity Stats -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Activity Section -->
          <div class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl p-8 rounded-2xl border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-3 text-white">
              <i class="fas fa-activity text-green-500 text-2xl"></i>
              Activity
            </h2>
            <div v-if="isSeller" class="space-y-4 animate-fade-in">
              <div class="group relative bg-gradient-to-br from-red-600/20 to-red-800/10 p-6 rounded-2xl border border-red-500/30 hover:border-red-500/60 transition-all transform hover:scale-105 duration-300 hover:shadow-2xl hover:shadow-red-500/30 shadow-lg overflow-hidden cursor-pointer">
                <div class="absolute inset-0 bg-gradient-to-r from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div class="relative flex items-center justify-between">
                  <div class="z-10">
                    <p class="text-red-200 text-xs uppercase font-bold tracking-wider mb-2">Listings</p>
                    <p class="text-4xl font-extrabold text-red-400 drop-shadow-lg">{{ stats.totalProducts }}</p>
                  </div>
                  <div class="text-6xl text-red-500/20 group-hover:text-red-500/40 transition-colors duration-300">
                    <i class="fas fa-car"></i>
                  </div>
                </div>
              </div>

              <div class="group relative bg-gradient-to-br from-blue-600/20 to-blue-800/10 p-6 rounded-2xl border border-blue-500/30 hover:border-blue-500/60 transition-all transform hover:scale-105 duration-300 hover:shadow-2xl hover:shadow-blue-500/30 shadow-lg overflow-hidden cursor-pointer">
                <div class="absolute inset-0 bg-gradient-to-r from-blue-600/0 to-blue-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div class="relative flex items-center justify-between">
                  <div class="z-10">
                    <p class="text-blue-200 text-xs uppercase font-bold tracking-wider mb-2">Last Active</p>
                    <p class="text-3xl font-extrabold text-blue-400 drop-shadow-lg">Today</p>
                  </div>
                  <div class="text-6xl text-blue-500/20 group-hover:text-blue-500/40 transition-colors duration-300">
                    <i class="fas fa-clock"></i>
                  </div>
                </div>
              </div>

              <!-- Contact Seller Button (for non-owner buyers) -->
              <NuxtLink 
                v-if="!isOwnProfile"
                to="/messages"
                @click="initiateChatWithSeller"
                class="block w-full py-4 px-6 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 duration-300 shadow-lg hover:shadow-red-600/50 text-center"
              >
                <i class="fas fa-comments mr-2"></i>
                Contact Seller
              </NuxtLink>
            </div>
            <div v-else class="space-y-4">
              <div class="bg-gradient-to-br from-green-600/20 to-green-800/10 p-6 rounded-xl border border-green-500/30 text-center hover:scale-105 transition-transform duration-300">
                <i class="fas fa-check-circle text-3xl text-green-500 mb-3"></i>
                <p class="text-green-400 text-sm uppercase font-bold">Account Status</p>
                <p class="text-2xl font-bold text-green-400 mt-2">Active</p>
              </div>
              <div class="bg-gradient-to-br from-purple-600/20 to-purple-800/10 p-6 rounded-xl border border-purple-500/30 text-center hover:scale-105 transition-transform duration-300">
                <i class="fas fa-clock text-3xl text-purple-400 mb-3"></i>
                <p class="text-purple-400 text-sm uppercase font-bold">Last Active</p>
                <p class="text-lg font-bold text-purple-400 mt-2">Today</p>
              </div>
            </div>
          </div>

          <!-- Actions Section (only show for own profile) -->
          <div v-if="isOwnProfile" class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl p-8 rounded-2xl border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-3 text-white">
              <i class="fas fa-cogs text-yellow-500 text-2xl"></i>
              Actions
            </h2>
            <div class="space-y-3">
              <button 
                @click="saveProfile"
                class="w-full py-3 px-6 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 duration-300 shadow-lg hover:shadow-green-600/50 flex items-center justify-center gap-2"
              >
                <i class="fas fa-save"></i>
                Save Changes
              </button>
              <NuxtLink 
                to="/dashboard"
                class="w-full py-3 px-6 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 duration-300 shadow-lg hover:shadow-blue-600/50 flex items-center justify-center gap-2"
              >
                <i class="fas fa-arrow-right"></i>
                Back to Dashboard
              </NuxtLink>
            </div>
          </div>
        </div>

      </div>

      <!-- Seller's Cars Section (shown to buyers viewing seller profile) -->
      <div v-if="isSeller && !isOwnProfile" class="mt-12">
        <div class="mb-8">
          <h2 class="text-4xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent mb-2 drop-shadow-lg flex items-center gap-3">
            <i class="fas fa-car text-red-500"></i>
            Cars for Sale by {{ viewingUsername }}
          </h2>
          <p class="text-gray-400 text-lg">Browse the available vehicles from this seller</p>
        </div>

        <!-- Cars Grid -->
        <div v-if="sellerCars.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <NuxtLink
            v-for="car in sellerCars"
            :key="car._id"
            :to="`/car/${car._id}`"
            class="car-card flex-shrink-0 bg-gradient-to-br from-gray-900/80 via-gray-800/50 to-gray-950/80 backdrop-blur-xl p-6 rounded-2xl border border-gray-700/50 hover:border-red-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-red-600/30 hover:-translate-y-3 transform group overflow-hidden relative"
          >
            <!-- Gradient Overlay on Hover -->
            <div class="absolute inset-0 bg-gradient-to-t from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

            <!-- Image Container -->
            <div class="relative mb-6 overflow-hidden rounded-xl group/image">
              <img 
                :src="car.images?.[0] || 'https://via.placeholder.com/300x200?text=No+Image'" 
                alt="car" 
                class="rounded-xl w-full h-48 object-cover group-hover/image:scale-110 transition-transform duration-500 shadow-xl" 
              />
              <!-- Badge -->
              <div class="absolute top-4 right-4 bg-gradient-to-r from-red-600 to-orange-600 px-4 py-2 rounded-full text-xs font-bold text-white shadow-lg">
                <i class="fas fa-check-circle mr-1"></i>Available
              </div>
              <!-- Year Badge -->
              <div class="absolute top-4 left-4 bg-gray-900/80 backdrop-blur-sm px-4 py-2 rounded-full text-xs font-bold text-gray-200 border border-gray-700">
                {{ car.year }}
              </div>
            </div>

            <!-- Content -->
            <div class="relative z-10 space-y-4">
              <!-- Title -->
              <div>
                <h3 class="font-extrabold text-xl text-white mb-1 group-hover:text-red-400 transition-colors">{{ car.brand }} {{ car.model }}</h3>
                <p class="text-sm text-gray-400 font-semibold">{{ car.body_type || 'N/A' }}</p>
              </div>

              <!-- Specs -->
              <div class="grid grid-cols-2 gap-3">
                <div class="bg-gray-800/50 border border-gray-700/50 p-3 rounded-xl hover:border-red-500/50 transition-all duration-300">
                  <p class="text-gray-400 text-xs uppercase font-bold mb-1">Transmission</p>
                  <p class="text-white font-semibold flex items-center gap-2">
                    <i class="fas fa-cog text-red-500"></i>
                    {{ car.transmission || 'N/A' }}
                  </p>
                </div>
                <div class="bg-gray-800/50 border border-gray-700/50 p-3 rounded-xl hover:border-orange-500/50 transition-all duration-300">
                  <p class="text-gray-400 text-xs uppercase font-bold mb-1">Fuel</p>
                  <p class="text-white font-semibold flex items-center gap-2">
                    <i class="fas fa-gas-pump text-orange-500"></i>
                    {{ car.fuel_type || 'N/A' }}
                  </p>
                </div>
              </div>

              <!-- Price & Button -->
              <div class="flex items-center justify-between pt-4 border-t border-gray-700/50">
                <div>
                  <p class="text-gray-400 text-xs uppercase font-bold mb-1">Price</p>
                  <p class="text-3xl font-extrabold text-red-500 drop-shadow-lg">฿{{ formatPrice(car.price) }}</p>
                </div>
                <button class="px-6 py-3 rounded-xl bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-bold hover:shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-110 active:scale-95 shadow-lg flex items-center gap-2">
                  <i class="fas fa-eye"></i>
                  View
                </button>
              </div>
            </div>
          </NuxtLink>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-16 bg-gradient-to-br from-gray-900/50 to-gray-950/50 rounded-2xl border border-gray-800/50">
          <i class="fas fa-inbox text-6xl text-gray-600 mb-4 opacity-50"></i>
          <p class="text-gray-400 font-semibold text-lg">No cars listed yet</p>
          <p class="text-gray-500 text-sm mt-2">This seller hasn't posted any vehicles</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Success Modal for Profile Image Update -->
  <SuccessModal
    :show="showProfileImageModal"
    title="โปรไฟล์อัปเดตสำเร็จ!"
    message="รูปโปรไฟล์ของคุณถูกบันทึกเรียบร้อยแล้ว"
    icon="✅"
    :duration="5"
    @close="handleProfileImageClose"
  />
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// Data
const currentUsername = ref(localStorage.getItem('username') || '')
const viewingUsername = ref('')
const isSeller = ref(localStorage.getItem('is_seller') === 'true')
const isOwnProfile = ref(true)
const businessName = ref('')
const sellerEmail = ref('')
const phoneNumber = ref('')
const contactInfo = ref('')
const carsListed = ref(0)
const memberSince = ref(new Date().toLocaleDateString())
const lastActivity = ref(new Date().toLocaleDateString())

// Profile image
const profileImageUrl = ref('')
const selectedFile = ref(null)
const showProfileImageModal = ref(false)

// Stats
const stats = ref({
  totalProducts: 0
})

// Seller's cars
const sellerCars = ref([])

// Methods
const onFileSelected = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    profileImageUrl.value = URL.createObjectURL(file)
  }
}

const becomeSeller = () => {
  router.push('/register-seller')
}

const saveProfile = async () => {
  try {
    if (!selectedFile.value && !profileImageUrl.value) {
      alert('No changes to save')
      return
    }

    const token = localStorage.getItem('token')
    if (!token) {
      alert('You must be logged in')
      return
    }

    // If file selected, convert to base64
    let imageData = profileImageUrl.value
    if (selectedFile.value) {
      const reader = new FileReader()
      await new Promise((resolve) => {
        reader.onload = (e) => {
          imageData = e.target.result
          resolve()
        }
        reader.readAsDataURL(selectedFile.value)
      })
    }

    // Send to backend
    const response = await fetch('http://localhost:5000/api/update-profile-image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        profileImage: imageData
      })
    })

    const data = await response.json()
    if (response.ok && data.success) {
      // Save to localStorage for persistence
      localStorage.setItem('profileImage', imageData)
      selectedFile.value = null
      // Show success modal instead of alert
      showProfileImageModal.value = true
    } else {
      alert('❌ Error updating profile: ' + (data.message || 'Unknown error'))
    }
  } catch (err) {
    console.error(err)
    alert('Server error, please try again.')
  }
}

const handleProfileImageClose = () => {
  showProfileImageModal.value = false
}

// Format price function
const formatPrice = (price) => {
  if (!price) return 'N/A'
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

// Create a function to handle mounted data fetching
const onMountedFetch = async () => {
  const userParam = route.query.user

  if (userParam && userParam !== currentUsername.value) {
    // View other user's profile
    viewingUsername.value = userParam
    isOwnProfile.value = false
    isSeller.value = false

    try {
      // Fetch profile image
      const profileRes = await fetch(
        `http://localhost:5000/api/get-profile?username=${viewingUsername.value}`
      )
      const profileData = await profileRes.json()
      if (profileData.success && profileData.profileImageUrl) {
        profileImageUrl.value = profileData.profileImageUrl
      }

      const sellerRes = await fetch(
        `http://localhost:5000/api/seller-info/${viewingUsername.value}`
      )
      const sellerData = await sellerRes.json()

      if (sellerData.success && sellerData.seller) {
        isSeller.value = true
        businessName.value = sellerData.seller.business_name || ''
        sellerEmail.value = sellerData.seller.email || ''
        phoneNumber.value = sellerData.seller.phonenumber || ''
        contactInfo.value = sellerData.seller.contact_info || ''

        const carsResponse = await fetch(
          `http://localhost:5000/api/cars/seller/${viewingUsername.value}`
        )
        const carsData = await carsResponse.json()
        if (carsData.success) {
          carsListed.value = carsData.cars.length
          sellerCars.value = carsData.cars
          stats.value.totalProducts = carsData.cars.length
        }
      }
    } catch (error) {
      console.error('Error fetching seller info:', error)
    }
  } else {
    // View own profile
    viewingUsername.value = currentUsername.value
    isOwnProfile.value = true

    try {
      const res = await fetch(
        `http://localhost:5000/api/get-profile?username=${currentUsername.value}`
      )
      const data = await res.json()

      if (data.success) {
        profileImageUrl.value = data.profileImageUrl || ''
        memberSince.value = data.memberSince || new Date().toLocaleDateString()
        lastActivity.value = data.lastActivity || new Date().toLocaleDateString()
      }

      if (isSeller.value) {
        try {
          const sellerRes = await fetch(
            `http://localhost:5000/api/seller-info/${currentUsername.value}`
          )
          const sellerData = await sellerRes.json()

          if (sellerData.success && sellerData.seller) {
            businessName.value = sellerData.seller.business_name || ''
            sellerEmail.value = sellerData.seller.email || ''
            phoneNumber.value = sellerData.seller.phonenumber || ''
            contactInfo.value = sellerData.seller.contact_info || ''

            const carsResponse = await fetch(
              `http://localhost:5000/api/cars/seller/${currentUsername.value}`
            )
            const carsData = await carsResponse.json()
            if (carsData.success) {
              carsListed.value = carsData.cars.length
              stats.value.totalProducts = carsData.cars.length
            }
          }
        } catch (error) {
          console.error('Error fetching seller info:', error)
        }
      }
    } catch (error) {
      console.error('Error fetching profile:', error)
    }
  }
}

onMounted(() => {
  onMountedFetch()
})

watch(() => route.query.user, async (newUser) => {
  // Refetch when user parameter changes
  await onMountedFetch()
}, { immediate: false })
</script>

<style scoped>
input[type="file"] {
  display: none;
}
</style>
