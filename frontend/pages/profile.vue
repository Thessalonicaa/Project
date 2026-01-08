<template>
  <div class="min-h-screen bg-gray-950 text-white p-6">
    <div class="max-w-5xl mx-auto">
      
      <!-- Profile Header -->
      <div class="bg-gray-900/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 mb-8  transition-all duration-300">
        <div class="flex flex-col md:flex-row items-center gap-8">
          <!-- Avatar with gradient border -->
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-r from-red-600 to-red-500 rounded-full blur-xl opacity-30 group-hover:opacity-50 transition-opacity"></div>
            <div class="relative w-32 h-32">
              <img 
                v-if="profileImageUrl" 
                :src="profileImageUrl" 
                alt="Profile" 
                class="w-32 h-32 object-cover rounded-full border-4 border-red-500 shadow-2xl"
              />
              <div v-else class="w-32 h-32 bg-gradient-to-br from-red-600 to-red-700 rounded-full flex items-center justify-center border-4 border-red-500 shadow-2xl">
                <i class="fas fa-user text-6xl text-white"></i>
              </div>

              <!-- Upload button overlay -->
              <label 
                v-if="isOwnProfile"
                for="file-upload" 
                class="absolute bottom-2 right-2 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 p-3 rounded-full cursor-pointer transition-all transform hover:scale-110 shadow-lg"
              >
                <i class="fas fa-camera text-white text-lg"></i>
              </label>
              <input id="file-upload" type="file" class="hidden" @change="onFileSelected" accept="image/*" />
            </div>
          </div>

          <!-- User Info -->
          <div class="flex-1 text-center md:text-left">
            <h1 class="text-4xl font-extrabold bg-gradient-to-r from-red-500 to-red-400 bg-clip-text text-transparent mb-2">
              {{ viewingUsername }}
            </h1>
            <p class="text-xl text-gray-400 mb-4">
              {{ isSeller ? 'Seller Account' : 'User Account' }}
            </p>
            <!-- Back button when viewing others -->
            <button 
              v-if="!isOwnProfile"
              @click="router.back()"
              class="px-6 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-red-400 rounded-lg transition-all duration-300 transform hover:scale-105"
            >
             
            </button>
          </div>

          <!-- Quick Stats -->
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 text-center">
              <p class="text-gray-400 text-sm mb-1">Member Since</p>
              <p class="text-white font-bold">{{ memberSince }}</p>
            </div>
            <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 text-center">
              <p class="text-gray-400 text-sm mb-1">Cars Listed</p>
              <p class="text-red-400 font-bold text-2xl">{{ stats.totalProducts }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Grid -->
      <div class="grid md:grid-cols-2 gap-8">

        <!-- Left Section -->
        <div class="space-y-6">
          <!-- Account Information -->
          <div class="bg-gray-900/80 backdrop-blur-xl p-8 rounded-3xl border border-gray-800/50  ">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
              Account Information
            </h2>
            <div class="space-y-4">
              <div class="border-b border-gray-700 pb-4">
                <p class="text-gray-500 text-sm uppercase font-semibold">Username</p>
                <p class="text-white font-bold text-lg">{{ viewingUsername }}</p>
              </div>
              <div class="border-b border-gray-700 pb-4">
                <p class="text-gray-500 text-sm uppercase font-semibold">Account Type</p>
                <p class="text-red-400 font-bold text-lg">{{ isSeller ? 'Seller' : 'User' }}</p>
              </div>
              <div>
                <p class="text-gray-500 text-sm uppercase font-semibold">Member Since</p>
                <p class="text-white font-bold text-lg">{{ memberSince }}</p>
              </div>
            </div>
          </div>

          <!-- Seller Information -->
          <div v-if="isSeller" class="bg-gray-900/80 backdrop-blur-xl p-8 rounded-3xl border border-gray-800/50  ">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
              Business Information
            </h2>
            <div class="space-y-4">
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                <p class="text-gray-500 text-sm uppercase font-semibold mb-1">Business Name</p>
                <p class="text-white font-bold">{{ businessName || 'Not Set' }}</p>
              </div>
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                <p class="text-gray-500 text-sm uppercase font-semibold mb-1">Email</p>
                <p class="text-white font-bold break-all">{{ sellerEmail || 'Not Set' }}</p>
              </div>
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                <p class="text-gray-500 text-sm uppercase font-semibold mb-1">Phone Number</p>
                <p class="text-white font-bold">{{ phoneNumber || 'Not Set' }}</p>
              </div>
              <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                <p class="text-gray-500 text-sm uppercase font-semibold mb-1">Address</p> 
                <p class="text-white font-bold">{{ contactInfo || 'Not Set' }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Section -->
        <div class="space-y-6">
          <!-- Activity Section -->
          <div class="bg-gray-900/80 backdrop-blur-xl p-8 rounded-3xl border border-gray-800/50">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
              Activity
            </h2>
            <div v-if="isSeller" class="grid grid-cols-1 sm:grid-cols-2 gap-6 animate-fade-in">
              <div class="group relative bg-gradient-to-br from-red-600/20 to-red-800/10 p-8 rounded-3xl border border-red-500/30 hover:border-red-500/60 transition-all transform hover:scale-105 duration-300 hover:shadow-2xl hover:shadow-red-500/30 shadow-xl cursor-pointer overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-r from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div class="relative flex items-center justify-between">
                  <div class="z-10">
                    <p class="text-red-200 text-sm uppercase font-semibold mb-2 tracking-wider">Cars Listed</p>
                    <p class="text-3xl font-extrabold text-red-400 drop-shadow-lg">{{ stats.totalProducts }}</p>
                    <p class="text-red-300 text-xs mt-2"><i class="fas fa-arrow-up mr-1"></i></p>
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
                    <p class="text-blue-200 text-sm uppercase font-semibold mb-2 tracking-wider">Last Active</p>
                    <p class="text-3xl font-extrabold text-blue-400 drop-shadow-lg">Today</p>
                    <p class="text-blue-300 text-xs mt-2"><i class="fas fa-calendar-check mr-1"></i></p>
                  </div>
                  <div class="text-7xl text-blue-500/20 group-hover:text-blue-500/40 transition-colors duration-300">
                    <i class="fas fa-clock"></i>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="grid grid-cols-2 gap-4">
              <div class="bg-gradient-to-br from-red-600/20 to-red-800/10 p-6 rounded-xl border border-red-500/30 text-center">
                <i class="fas fa-car text-3xl text-red-500 mb-2"></i>
                <p class="text-gray-400 text-sm">Cars Listed</p>
                <p class="text-3xl font-bold text-red-400">{{ stats.totalProducts }}</p>
              </div>
              <div class="bg-gradient-to-br from-blue-600/20 to-blue-800/10 p-6 rounded-xl border border-blue-500/30 text-center">
                <i class="fas fa-clock text-3xl text-blue-400 mb-2"></i>
                <p class="text-gray-400 text-sm">Last Active</p>
                <p class="text-lg font-bold text-blue-400">Today</p>
              </div>
            </div>
          </div>

          <!-- Actions Section -->
          <div class="bg-gray-900/80 backdrop-blur-xl p-8 rounded-3xl border border-gray-800/50  transition-all duration-300">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
              Actions
            </h2>
            <div class="space-y-3">
              <button 
                v-if="isOwnProfile"
                @click="saveProfile"
                class="w-full py-3 px-6 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 duration-300 shadow-lg flex items-center justify-center gap-2"
              >
                <i class="fas fa-save"></i>
                Save Changes
              </button>
              <NuxtLink 
                v-if="isOwnProfile"
                to="/dashboard"
                class="w-full py-3 px-6 bg-gray-800 hover:bg-gray-700 text-white font-bold rounded-xl transition-all transform hover:scale-105 duration-300 shadow-lg flex items-center justify-center gap-2"
              >
                <i class="fas fa-arrow-right"></i>
                Back to Dashboard
              </NuxtLink>
            </div>
          </div>
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
