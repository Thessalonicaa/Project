<template>
  <Nav
    class="bg-black/95 backdrop-blur-md text-white px-4 md:px-6 py-3 flex items-center shadow-lg transition-all duration-500 relative z-50"
  >
    <!-- หน้า login/register -->
    <template v-if="isAuthPage">
      <div class="w-full flex justify-center">
        <NuxtLink
          to="/login"
          class="font-extrabold text-2xl tracking-wide text-red-500 hover:scale-125 hover:text-red-400 transition-transform duration-300"
        >
          ZAVORA
        </NuxtLink>
      </div>
    </template>

    <!-- หน้าอื่น -->
    <template v-else>
      <div class="w-full flex justify-between items-center">
        <!-- โลโก้ -->
          <NuxtLink
          to="/"
          class="font-extrabold text-2xl tracking-widest text-transparent bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text hover:scale-110 transition-transform duration-300 drop-shadow-lg"
        >
          ZAVORA
        </NuxtLink>

        <!-- ส่วนขวา -->
        <div v-if="isLoggedIn" class="flex items-center space-x-6">
          <!-- Back Button -->
          

          <!-- ตะกร้าช้อปปิ้ง -->
          <NuxtLink 
            to="/cart" 
            class="relative flex items-center text-white hover:text-red-500 transition-all duration-300 transform hover:scale-110"
          >
            <i class="fas fa-shopping-cart text-xl"></i>
            <span v-if="cartCount > 0" class="absolute -top-3 -right-3 bg-red-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center font-bold animate-pulse">
              {{ cartCount }}
            </span>
          </NuxtLink>

          <!-- โปรไฟล์ -->
          <div class="relative">
            <NuxtLink to="/profile" class="flex items-center space-x-2 text-gray-300 hover:text-red-500">
              <div class="w-8 h-8 rounded-full bg-gray-800 border border-gray-700 flex items-center justify-center">
                <img v-if="profileImage" :src="profileImage" class="w-full h-full rounded-full object-cover" />
                <i v-else class="fas fa-user"></i>
              </div>
              <span class="hidden md:block">{{ username }}</span>
            </NuxtLink>
          </div>

          <!-- กล่องค้นหา -->
          <div class="relative group w-72">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search cars..."
              class="px-4 py-2 rounded-xl bg-gray-900 border border-gray-700 text-white w-full focus:outline-none focus:ring-2 focus:ring-red-500 transition-all duration-300 placeholder-gray-400 group-focus-within:ring-2 group-focus-within:ring-red-500 group-focus-within:border-red-500 group-focus-within:bg-gray-800 group-focus-within:scale-105"
              @input="searchCars"
              @keyup.enter="handleEnterSearch"
            />
            <!-- Search Icon Animation -->
            <i class="fas fa-search absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-red-500 group-focus-within:animate-pulse transition-colors duration-300 pointer-events-none"></i>
            
            <!-- ผลลัพธ์ค้นหา Real-time -->
            <transition name="search-fade">
              <div
                v-if="searchResults.length > 0 && searchQuery.trim()"
                class="absolute z-50 w-full mt-3 bg-gray-900/95 backdrop-blur-lg border border-red-500/50 rounded-xl shadow-2xl animate-search-slide-down max-h-96 overflow-y-auto"
              >
                <div class="p-2 sticky top-0 bg-gray-900/80 border-b border-gray-700">
                  <div class="text-xs text-gray-400 px-3 py-2 font-semibold">ผลลัพธ์ค้นหา ({{ searchResults.length }})</div>
                </div>
                <div
                  v-for="(car, index) in searchResults"
                  :key="car._id || car.id"
                  @click="selectCar(car)"
                  class="p-3 hover:bg-red-600/20 cursor-pointer flex items-center gap-3 transition-all transform hover:translate-x-2 rounded-lg hover:rounded-2xl animate-search-item hover:shadow-lg hover:shadow-red-600/30 mx-1"
                  :style="{ 'animation-delay': `${index * 0.05}s` }"
                >
                  <div class="relative flex-shrink-0">
                    <img 
                      :src="car.images?.[0] || 'https://via.placeholder.com/50x50'" 
                      class="w-16 h-12 object-cover rounded-lg hover:scale-110 transition-transform duration-300" 
                      @error="(e) => e.target.src = 'https://via.placeholder.com/50x50'"
                    />
                    <div class="absolute inset-0 rounded-lg bg-gradient-to-r from-red-600/0 to-red-600/20 opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="font-semibold text-white truncate group-hover:text-red-400 transition-colors">{{ car.brand }} {{ car.model }}</div>
                    <div class="text-xs text-gray-400">{{ car.year }} • ฿{{ formatPrice(car.price) }}</div>
                  </div>
                  <i class="fas fa-arrow-right text-red-500 text-xs flex-shrink-0 opacity-0 group-hover:opacity-100 transform group-hover:translate-x-1 transition-all duration-300"></i>
                </div>
              </div>
            </transition>

            <!-- No results message -->
            <transition name="search-fade">
              <div
                v-if="searchQuery.trim() && searchResults.length === 0"
                class="absolute z-50 w-full mt-3 bg-gray-900/95 backdrop-blur-lg border border-gray-700/50 rounded-xl shadow-lg p-6 text-center animate-search-slide-down"
              >
                <i class="fas fa-search text-gray-500 text-3xl mb-2"></i>
                <p class="text-gray-400 text-sm font-medium">ไม่พบรถที่ตรงกับการค้นหา</p>
              </div>
            </transition>
          </div>

          <!-- ปุ่มเมนู -->
          <div
            class="relative"
            @mouseenter="hovering = true"
            @mouseleave="hovering = false"
          >
            <button
              class="flex items-center gap-2 text-gray-300 hover:text-red-500 transition-all duration-300"
              @click="toggleMenu"
            >
              <i class="fas fa-bars text-lg"></i>
              Menu
            </button>

            <!-- พื้นหลังบังหน้าทั้งหน้า -->
            <transition name="fade">
              <div
                v-if="isMenuVisible"
                class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
                @click="closeMenu"
              ></div>
            </transition>

            <!-- Dropdown -->
            <transition name="fade-slide">
              <div
                v-if="isMenuVisible"
                class="absolute right-0 top-12 bg-gray-900/95 backdrop-blur-md border border-gray-700 rounded-2xl shadow-2xl p-4 w-56 flex flex-col space-y-2 animate-slideDown z-50"
              >
                <NuxtLink
                  to="/"
                  class="menu-item font-extrabold text-xl tracking-wide text-red-500 hover:scale-125 hover:text-red-400 transition-transform duration-300"
                  >
                  <i class="fas fa-home mr-2 text-red-500"></i> Home
                </NuxtLink>
                <NuxtLink to="/dashboard" class="menu-item">
                  <i class="fas fa-user mr-2 text-red-500"></i> My Profile
                </NuxtLink>
                <NuxtLink to="/orders" class="menu-item">
                  <i class="fas fa-receipt mr-2 text-red-500"></i> Orders
                </NuxtLink>
                <NuxtLink to="/messages" class="menu-item">
                  <i class="fas fa-comments mr-2 text-red-500"></i> Messages
                </NuxtLink>
                <NuxtLink to="/CarList" class="menu-item">
                  <i class="fas fa-car-side mr-2 text-red-500"></i> Cars
                </NuxtLink>
                <!-- Sell Your Car (button) -->
                <button @click="handleSellClick" class="menu-item flex items-center">
                  <i class="fas fa-plus-circle mr-2 text-red-500"></i>
                  Sell Your Car
                </button>

                <button @click="handleLogout" class="menu-item text-left">
                  <i class="fas fa-sign-out-alt mr-2 text-red-500"></i> Logout
                </button>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </template>
  </Nav>

  <!-- Teleport modal -->
  <teleport to="body">
    <div v-if="showNotSellerModal" class="fixed inset-0 z-[9999] flex items-center justify-center">
      <div class="absolute inset-0 bg-black/70" @click="closeNotSellerModal"></div>
      <div class="relative z-50 max-w-lg w-full mx-4 p-8 bg-gray-900 text-center rounded-lg animate-modal">
        <div class="text-white text-2xl font-bold">คุณไม่ได้เป็นผู้ขาย</div>
        <div class="text-sm text-gray-400 mt-3">คลิกที่ใดก็ได้บนหน้าจอนี้เพื่อไปที่ ลงทะเบียนเป็นผู้ขาย</div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useSmartBack } from '~/composables/useSmartBack'

const router = useRouter()
const route = useRoute()

const searchQuery = ref('')
const searchResults = ref([])
const hovering = ref(false)
const clicked = ref(false)
const username = ref('')
const profileImage = ref('')
const showNotSellerModal = ref(false)
const cartCount = ref(0)

const { goBack } = useSmartBack()

const isSeller = computed(() => {
  if (!process.client) return false
  const role = localStorage.getItem('role')
  const isSellerFlag = localStorage.getItem('is_seller')
  return role === 'seller' || isSellerFlag === 'true' || isSellerFlag === '1'
})

onMounted(() => {
  if (process.client) {
    username.value = localStorage.getItem('username') || ''
    loadProfileImage()
    updateCartCount()
    
    // Watch for cart changes every 500ms
    const cartWatchInterval = setInterval(() => {
      updateCartCount()
    }, 500)
    
    // Poll for profile image updates every 2 seconds
    const profileWatchInterval = setInterval(() => {
      loadProfileImage()
    }, 2000)
    
    // Listen to storage changes from other tabs
    window.addEventListener('storage', (e) => {
      if (e.key && e.key.startsWith('cart_')) {
        updateCartCount()
      }
    })
    
    // Cleanup intervals on unmount
    return () => {
      clearInterval(cartWatchInterval)
      clearInterval(profileWatchInterval)
    }
  }
})

// Watch route changes to update cart count
watch(() => route.path, () => {
  updateCartCount()
})

// Fetch profile image from API
const loadProfileImage = async () => {
  try {
    const currentUsername = localStorage.getItem('username')
    if (!currentUsername) return

    const response = await fetch(
      `http://localhost:5000/api/get-profile?username=${currentUsername}`
    )
    const data = await response.json()

    if (data.success && data.profileImageUrl) {
      profileImage.value = data.profileImageUrl
      // Also save to localStorage for faster access
      localStorage.setItem('profileImage', data.profileImageUrl)
    }
  } catch (error) {
    console.error('Error loading profile image:', error)
  }
}

const isLoggedIn = computed(() => !!localStorage.getItem('token'))
const isAuthPage = computed(() =>
  ['/login', '/register', '/register-seller'].includes(route.path)
)

const isMenuVisible = computed(() => hovering.value || clicked.value)

const toggleMenu = () => {
  clicked.value = !clicked.value
}

const closeMenu = () => {
  clicked.value = false
  hovering.value = false
}

const updateCartCount = () => {
  if (!process.client) return
  
  const currentUsername = localStorage.getItem('username')
  if (!currentUsername) {
    cartCount.value = 0
    return
  }
  
  const cartKey = `cart_${currentUsername}`
  const cart = localStorage.getItem(cartKey)
  
  try {
    cartCount.value = cart ? JSON.parse(cart).length : 0
  } catch (error) {
    console.error('Error parsing cart:', error)
    cartCount.value = 0
  }
}

const searchCars = async () => {
  if (!searchQuery.value || searchQuery.value.length < 1) {
    searchResults.value = []
    return
  }
  try {
    const response = await axios.get(
      `http://localhost:5000/api/cars/search?q=${searchQuery.value}`
    )
    if (response.data && Array.isArray(response.data)) {
      searchResults.value = response.data.slice(0, 8) // Limit to 8 results
    } else {
      searchResults.value = []
    }
  } catch (error) {
    console.error('Search failed:', error)
    searchResults.value = []
  }
}

const selectCar = (car) => {
  router.push(`/car/${car._id}`)
  searchQuery.value = ''
  searchResults.value = []
  closeMenu()
}

const handleEnterSearch = () => {
  if (searchResults.value.length > 0) selectCar(searchResults.value[0])
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
  closeMenu()
}

const handleSellClick = (e) => {
  if (isSeller.value) {
    router.push('/seller/PostCar')
    closeMenu()
  } else {
    showNotSellerModal.value = true
  }
}

const closeNotSellerModal = () => {
  showNotSellerModal.value = false
  closeMenu()
  router.push('/dashboard')
}

const handleBackClick = () => {
  goBack()
}

const formatPrice = (price) => {
  if (!price) return 'N/A'
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}
</script>

<style scoped>
/* เมนู hover */
.menu-item {
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  color: rgb(209, 213, 219);
  transition: all 0.3s;
  display: flex;
  align-items: center;
}

.menu-item:hover {
  background-color: rgb(220, 38, 38);
  color: white;
}

/* Fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Slide */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.25s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* keyframes */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-15px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
.animate-slideDown {
  animation: slideDown 0.30s ease-out;
}

/* Modal animation */
.animate-modal {
  animation: popIn 0.35s ease-out;
}

@keyframes popIn {
  0% { opacity: 0; transform: translateY(-12px) scale(0.98); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}

/* Search animations */
.animate-search-slide-down {
  animation: searchSlideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.animate-search-item {
  animation: searchItemSlide 0.4s ease-out forwards;
  opacity: 0;
}

@keyframes searchSlideDown {
  from {
    opacity: 0;
    transform: translateY(-15px) scaleY(0.95);
    filter: blur(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0) scaleY(1);
    filter: blur(0);
  }
}

@keyframes searchItemSlide {
  from {
    opacity: 0;
    transform: translateX(-15px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

.search-fade-enter-active,
.search-fade-leave-active {
  transition: all 0.25s ease;
}

.search-fade-enter-from,
.search-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px) scaleY(0.95);
  filter: blur(4px);
}
</style>
