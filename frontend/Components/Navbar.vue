<template>
  <nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
      <!-- Logo -->
      <NuxtLink to="/" class="flex items-center gap-2 font-bold text-xl text-white hover:text-red-500 transition-colors">
        <i class="fas fa-car text-red-500"></i>
        CarHub
      </NuxtLink>

      <!-- Navigation Links -->
      <div class="hidden md:flex items-center gap-8">
        <NuxtLink to="/CarList" class="text-gray-400 hover:text-white transition-colors">
          <i class="fas fa-list mr-2"></i>Browse Cars
        </NuxtLink>
        <NuxtLink to="/messages" class="text-gray-400 hover:text-white transition-colors">
          <i class="fas fa-comments mr-2"></i>Messages
        </NuxtLink>
      </div>

      <!-- Right Side - User Menu -->
      <div class="flex items-center gap-4">
        <!-- Cart Icon -->
        <NuxtLink to="/cart" class="relative text-gray-400 hover:text-white transition-colors">
          <i class="fas fa-shopping-cart text-xl"></i>
          <span class="absolute -top-2 -right-2 bg-red-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">{{ cartCount }}</span>
        </NuxtLink>

        <!-- Admin Link (if admin) -->
        <NuxtLink v-if="isAdmin" to="/admin" class="text-gray-400 hover:text-red-500 transition-colors">
          <i class="fas fa-shield-alt text-lg"></i>
        </NuxtLink>

        <!-- User Menu -->
        <div class="relative">
          <button @click="toggleMenu" class="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-red-600 to-red-500 flex items-center justify-center text-white text-sm font-bold">
              {{ username.charAt(0).toUpperCase() }}
            </div>
            <i class="fas fa-chevron-down text-xs"></i>
          </button>

          <!-- Dropdown Menu -->
          <div v-if="showMenu" class="absolute right-0 mt-2 w-48 bg-gray-800 border border-gray-700 rounded-lg shadow-xl overflow-hidden">
            <NuxtLink to="/dashboard" class="block px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors">
              <i class="fas fa-user mr-2"></i>Dashboard
            </NuxtLink>
            <NuxtLink to="/profile" class="block px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors">
              <i class="fas fa-cog mr-2"></i>Profile
            </NuxtLink>
            <button @click="logout" class="w-full text-left px-4 py-3 text-red-400 hover:bg-gray-700 transition-colors border-t border-gray-700">
              <i class="fas fa-sign-out-alt mr-2"></i>Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('User')
const isAdmin = ref(false)
const showMenu = ref(false)
const cartCount = ref(0)

const toggleMenu = () => { showMenu.value = !showMenu.value }

const logout = () => {
  localStorage.clear()
  router.push('/login')
}

onMounted(() => {
  if (process.client) {
    username.value = localStorage.getItem('username') || 'User'
    const role = localStorage.getItem('role')
    isAdmin.value = role === 'admin' || localStorage.getItem('is_admin') === 'true'
    
    // Update cart count on mount
    const currentUsername = localStorage.getItem('username')
    if (currentUsername) {
      const cartKey = `cart_${currentUsername}`
      const cart = localStorage.getItem(cartKey)
      
      try {
        cartCount.value = cart ? JSON.parse(cart).length : 0
      } catch (error) {
        console.error('Error parsing cart:', error)
        cartCount.value = 0
      }
    }
  }
})
</script>

<style scoped>
/* Tailwind handles styling */
</style>
