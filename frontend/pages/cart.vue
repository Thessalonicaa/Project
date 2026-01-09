// filepath: e:\ProjectFainal\frontend\pages\cart.vue
<template>
  <div class="min-h-screen bg-gray-950 text-white p-6">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center gap-4 mb-4">
       <button 
          @click="goBack"
          class="group relative inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br border-red-500/50 hover:border-red-400 hover:from-red-600/40 hover:to-red-700/40 transition-all duration-300 shadow-lg hover:shadow-red-500/30"
          title="Go back"
        >
          <i class="fas fa-arrow-left text-red-500 group-hover:text-red-400 group-hover:-translate-x-1 transition-all duration-300"></i>
        </button>
          
          <NuxtLink 
            to="/CarList" 
            class="inline-flex items-center gap-2 text-red-500 hover:text-red-400 font-semibold group transition-all duration-300"
          >
            <span class="relative overflow-hidden">
              <span class="absolute inset-0 flex items-center translate-x-full group-hover:translate-x-0 transition-transform duration-300 text-red-400">
                <i class="fas fa-arrow-right ml-2"></i> Browse More
              </span>
            </span>
          </NuxtLink>
        </div>
        <h1 class="text-4xl font-extrabold bg-gradient-to-r from-red-500 to-red-400 bg-clip-text text-transparent">
          Shopping Cart
        </h1>
      </div>

      <div v-if="cartItems.length === 0" class="text-center py-16">
        <i class="fas fa-shopping-cart text-8xl text-gray-700 mb-4 opacity-50"></i>
        <p class="text-2xl text-gray-400 mb-4">Your cart is empty</p>
        <NuxtLink to="/CarList" class="inline-block px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl transition-all">
          Continue Shopping
        </NuxtLink>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-gray-900/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50">
            <h2 class="text-2xl font-bold mb-6">Cart Items ({{ cartItems.length }})</h2>
            
            <div v-for="(item, index) in cartItems" :key="index" class="bg-gray-800/50 p-6 rounded-2xl border border-gray-700 mb-4">
              <div class="flex gap-6">
                <!-- Item Image -->
                <div class="w-32 h-32 flex-shrink-0 rounded-xl overflow-hidden">
                  <img 
                    :src="item.images && item.images.length > 0 ? item.images[0] : 'https://via.placeholder.com/200x200?text=No+Image'"
                    :alt="item.model"
                    class="w-full h-full object-cover"
                  />
                </div>

                <!-- Item Details -->
                <div class="flex-1">
                  <h3 class="text-xl font-bold text-white mb-2">{{ item.brand }} {{ item.model }}</h3>
                  <p class="text-gray-400 mb-2">Year: {{ item.year }}</p>
                  <p class="text-gray-400 mb-2">License: {{ item.license_plate }}</p>
                  <p class="text-2xl font-bold text-red-500">฿{{ formatPrice(item.price) }}</p>
                </div>

                <!-- Remove Button -->
                <button
                  @click="removeFromCart(index)"
                  class="text-red-500 hover:text-red-400 transition-colors"
                >
                  <i class="fas fa-trash text-2xl"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Checkout Sidebar -->
        <div class="space-y-6">
          <!-- Total Price -->
          <div class="bg-gradient-to-br from-red-600 via-red-700 to-red-900 rounded-3xl p-8 shadow-2xl shadow-red-600/50 border border-red-500/50">
            <p class="text-red-200 text-sm uppercase font-semibold mb-2">Total Price</p>
            <p class="text-5xl font-extrabold text-white mb-6 drop-shadow-lg">฿{{ formatPrice(totalPrice) }}</p>
            <div class="bg-red-500/20 rounded-lg p-3 border border-red-400/30">
              <p class="text-red-100 text-sm font-semibold">{{ cartItems.length }} car(s) in cart</p>
            </div>
          </div>

          <!-- Down Payment Section -->
          <div class="bg-gray-900/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50">
            <h3 class="text-xl font-bold mb-4">Down Payment</h3>
            
            <!-- Down Payment Input -->
            <div class="mb-6">
              <label class="text-gray-400 text-sm uppercase font-semibold mb-2 block">Down Payment Amount (฿)</label>
              <div class="flex items-center gap-2 mb-3">
                <span class="text-red-500 font-bold text-xl">฿</span>
                <input
                  v-model.number="downPayment"
                  type="number"
                  :min="Math.ceil(totalPrice * 0.1)"
                  :max="totalPrice"
                  class="flex-1 px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white text-lg focus:outline-none focus:ring-2 focus:ring-red-500 font-semibold"
                  placeholder="Enter amount"
                />
              </div>
              <p class="text-xs text-gray-500">Min: ฿{{ formatPrice(Math.ceil(totalPrice * 0.1)) }} | Max: ฿{{ formatPrice(totalPrice) }}</p>
              <p class="text-xs text-red-400 mt-1">Percentage: {{ ((downPayment / totalPrice) * 100).toFixed(1) }}%</p>
            </div>

            <!-- Down Payment Info -->
            <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 mb-6">
              <p class="text-gray-400 text-sm mb-2">Down Payment: <span class="text-white font-bold">฿{{ formatPrice(downPayment) }}</span></p>
              <p class="text-gray-400 text-sm">Remaining: <span class="text-red-400 font-bold">฿{{ formatPrice(totalPrice - downPayment) }}</span></p>
            </div>

            <!-- Installment Slider -->
            <div class="mb-6">
              <label class="text-gray-400 text-sm uppercase font-semibold mb-3 block">Payment Installments</label>
              <div class="flex items-center gap-4">
                <span class="text-white font-bold text-lg min-w-fit">{{ selectedInstallments }} months</span>
                <input
                  v-model.number="selectedInstallments"
                  type="range"
                  min="1"
                  max="60"
                  class="flex-1 h-2 rounded-lg appearance-none cursor-pointer installment-slider"
                  :style="{ '--slider-value': (selectedInstallments / 60) * 100 + '%' }"
                />
              </div>
              <p class="text-xs text-gray-500 mt-2">1 - 60 months</p>
            </div>

            <!-- Monthly Payment Display -->
            <div class="bg-gradient-to-r from-blue-600/20 to-blue-800/10 p-4 rounded-xl border border-blue-500/30 mb-6">
              <p class="text-gray-400 text-sm mb-1">Monthly Payment</p>
              <p class="text-2xl font-bold text-blue-400">฿{{ formatPrice(monthlyPayment) }}</p>
              <p class="text-xs text-gray-500 mt-2">{{ selectedInstallments }} months</p>
            </div>

            <!-- Checkout Button -->
            <button
              @click="openCheckoutModal"
              :disabled="downPayment < totalPrice * 0.1 || downPayment > totalPrice"
              class="w-full py-4 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg disabled:opacity-50"
            >
              <i class="fas fa-credit-card mr-2"></i>Proceed to Checkout
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Checkout Confirmation Modal -->
  <div v-if="showCheckoutModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-gray-900 rounded-3xl p-8 border border-gray-800/50 max-w-md w-full max-h-[90vh] overflow-y-auto">
      <!-- Close Button -->
      <button @click="showCheckoutModal = false" class="float-right text-gray-400 hover:text-white">
        <i class="fas fa-times text-2xl"></i>
      </button>

      <h2 class="text-3xl font-bold mb-6 text-white">Confirm Order</h2>

      <!-- Order Summary -->
      <div class="bg-gray-800/50 p-6 rounded-2xl border border-gray-700 mb-6 space-y-4">
        <div class="flex justify-between">
          <span class="text-gray-400">Total Price</span>
          <span class="text-white font-bold">฿{{ formatPrice(totalPrice) }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-400">Down Payment</span>
          <span class="text-green-400 font-bold">฿{{ formatPrice(downPayment) }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-400">Remaining Payment</span>
          <span class="text-red-400 font-bold">฿{{ formatPrice(totalPrice - downPayment) }}</span>
        </div>
        <div class="border-t border-gray-700 pt-4 flex justify-between">
          <span class="text-gray-300 font-semibold">Monthly Payment</span>
          <span class="text-blue-400 font-bold text-lg">฿{{ formatPrice(monthlyPayment) }}</span>
        </div>
        <p class="text-xs text-gray-500 text-center">For {{ selectedInstallments }} months</p>
      </div>

      <!-- Contact Seller Option -->
      <button
        @click="contactSellerBeforeCheckout"
        class="w-full py-4 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 mb-3 shadow-lg"
      >
        <i class="fas fa-comments mr-2"></i>Contact Seller First
      </button>

      <!-- Confirm Button -->
      <button
        @click="confirmCheckout"
        class="w-full py-4 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 shadow-lg"
      >
        <i class="fas fa-check mr-2"></i>Confirm & Pay
      </button>

      <!-- Cancel Button -->
      <button
        @click="showCheckoutModal = false"
        class="w-full py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-xl transition-all mt-3"
      >
        Cancel
      </button>
    </div>
  </div>

  <!-- Success Modal -->
  <SuccessModal
    :show="showSuccessModal"
    title="Order Created Successfully!"
    message="Your order has been created. Please proceed with payment."
    icon="✅"
    :duration="3"
    @close="handleSuccessClose"
  />
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const cartItems = ref([])
const downPayment = ref(0)
const selectedInstallments = ref(12)
const showCheckoutModal = ref(false)
const showSuccessModal = ref(false)
const currentUsername = ref('')
const currentUserId = ref('')

const formatPrice = (price) => {
  return new Intl.NumberFormat('th-TH').format(Math.round(price || 0))
}

const goBack = () => {
  router.back()
}

const totalPrice = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.price, 0)
})

const monthlyPayment = computed(() => {
  const remaining = totalPrice.value - downPayment.value
  if (remaining <= 0) return 0
  return Math.ceil(remaining / selectedInstallments.value)
})

const loadCart = () => {
  const username = localStorage.getItem('username')
  const cartKey = `cart_${username}`
  const saved = localStorage.getItem(cartKey)
  if (saved) {
    cartItems.value = JSON.parse(saved)
  }
}

const removeFromCart = (index) => {
  cartItems.value.splice(index, 1)
  const username = localStorage.getItem('username')
  const cartKey = `cart_${username}`
  localStorage.setItem(cartKey, JSON.stringify(cartItems.value))
}

const saveCheckoutSettings = () => {
  const username = localStorage.getItem('username')
  const settingsKey = `checkout_settings_${username}`
  localStorage.setItem(settingsKey, JSON.stringify({
    downPayment: downPayment.value,
    selectedInstallments: selectedInstallments.value,
    timestamp: new Date().getTime()
  }))
}

const loadCheckoutSettings = () => {
  const username = localStorage.getItem('username')
  const settingsKey = `checkout_settings_${username}`
  const saved = localStorage.getItem(settingsKey)
  
  if (saved) {
    try {
      const settings = JSON.parse(saved)
      downPayment.value = settings.downPayment || 0
      selectedInstallments.value = settings.selectedInstallments || 12
    } catch (error) {
      console.error('Error loading checkout settings:', error)
    }
  }
}

const openCheckoutModal = () => {
  if (downPayment.value < totalPrice.value * 0.1 || downPayment.value > totalPrice.value) {
    alert('❌ Down payment must be between 10% - 100% of total price')
    return
  }
  showCheckoutModal.value = true
}

const contactSellerBeforeCheckout = async () => {
  if (cartItems.value.length === 0) {
    alert('No items in cart')
    return
  }

  try {
    // Get seller username from the first car
    const firstCarId = cartItems.value[0].id
    const carResponse = await fetch(`http://localhost:5000/api/cars/${firstCarId}`)
    const carData = await carResponse.json()
    
    if (!carData.success || !carData.car || !carData.car.seller) {
      alert('Error: Could not find seller information')
      return
    }

    const sellerUsername = carData.car.seller.username || carData.car.seller
    
    let message = `สวัสดีครับ/ค่ะ ต้องการสอบถามข้อมูลเกี่ยวกับการดาวน์รถเหล่านี้\n\n`
    
    cartItems.value.forEach((item, idx) => {
      message += `${idx + 1}. 📍 ${item.brand} ${item.model}\n`
      message += `   📅 ปี ${item.year}\n`
      message += `   💰 ฿${formatPrice(item.price)}\n`
      if (idx < cartItems.value.length - 1) message += '\n'
    })

    message += `\n\n💳 ข้อมูลการชำระเงิน:\n`
    message += `📊 ราคารวม: ฿${formatPrice(totalPrice.value)}\n`
    message += `💵 เงินดาวน์: ฿${formatPrice(downPayment.value)}\n`
    message += `📅 จำนวนงวด: ${selectedInstallments.value} เดือน\n`
    message += `💰 ค่างวดต่อเดือน: ฿${formatPrice(monthlyPayment.value)}`

    const cartsData = {
      items: cartItems.value,
      downPayment: downPayment.value,
      installments: selectedInstallments.value,
      totalPrice: totalPrice.value,
      monthlyPayment: monthlyPayment.value
    }
    
    sessionStorage.setItem('contactCarData', JSON.stringify(cartsData))
    sessionStorage.setItem('contactSellerMessage', message)
    sessionStorage.setItem('contactSeller', sellerUsername)
    sessionStorage.setItem('isFromCart', 'true')
    
    showCheckoutModal.value = false
    
    await new Promise(resolve => setTimeout(resolve, 100))
    router.push(`/messages?seller=${sellerUsername}`)
  } catch (error) {
    console.error('Error:', error)
    alert('Error: ' + error.message)
  }
}

const confirmCheckout = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: currentUsername.value,
        items: cartItems.value,
        totalPrice: totalPrice.value,
        downPayment: downPayment.value,
        remainingPayment: totalPrice.value - downPayment.value,
        installments: selectedInstallments.value,
        monthlyPayment: monthlyPayment.value,
        status: 'pending'
      })
    })

    const data = await response.json()

    if (data.success) {
      showCheckoutModal.value = false
      showSuccessModal.value = true
      
      const username = localStorage.getItem('username')
      const cartKey = `cart_${username}`
      localStorage.removeItem(cartKey)
      cartItems.value = []
    } else {
      alert('❌ Error creating order: ' + data.message)
    }
  } catch (error) {
    console.error('Error:', error)
    alert('Server error, please try again')
  }
}

const handleSuccessClose = () => {
  showSuccessModal.value = false
  router.push('/orders')
}

onMounted(() => {
  currentUsername.value = localStorage.getItem('username') || ''
  currentUserId.value = localStorage.getItem('userId') || ''
  loadCart()
  loadCheckoutSettings()
  
  if (totalPrice.value > 0 && downPayment.value === 0) {
    downPayment.value = Math.ceil(totalPrice.value * 0.2)
  }
})

// Watch for route changes from messages
watch(() => route.query.from, (newVal) => {
  if (newVal === 'messages') {
    loadCart()
  }
}, { immediate: true })

// Save checkout settings when they change
watch([downPayment, selectedInstallments], () => {
  saveCheckoutSettings()
}, { deep: true })
</script>

<style scoped>
input[type="range"] {
  appearance: none;
  width: 100%;
  height: 8px;
  border-radius: 5px;
  outline: none;
}

/* Installment slider with gradient fill */
.installment-slider {
  background: linear-gradient(to right, #dc2626 0%, #dc2626 var(--slider-value, 0%), #374151 var(--slider-value, 0%), #374151 100%);
}

.installment-slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #dc2626;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
  transition: all 0.2s;
}

.installment-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 20px rgba(220, 38, 38, 0.8);
}

.installment-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #dc2626;
  cursor: pointer;
  border: none;
  box-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
  transition: all 0.2s;
}

.installment-slider::-moz-range-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 20px rgba(220, 38, 38, 0.8);
}

.installment-slider::-moz-range-track {
  background: transparent;
  border: none;
}
</style>
