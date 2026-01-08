// filepath: e:\ProjectFainal\frontend\pages\cart.vue
<template>
  <div class="min-h-screen bg-gray-950 text-white p-6">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-red-500 mb-2">My Cart</h1>
        <p class="text-gray-400">คุณมี {{ cartItems.length }} คันในรถเข้า</p>
      </div>

      <div v-if="cartItems.length === 0" class="text-center py-16">
        <i class="fas fa-shopping-cart text-6xl text-gray-600 mb-4"></i>
        <p class="text-2xl text-gray-400 mb-6">ตะกร้าของคุณว่างเปล่า</p>
        <NuxtLink 
          to="/CarList"
          class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-xl transition-colors"
        >
          ไปเลือกรถ →
        </NuxtLink>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2 space-y-4">
          <div
            v-for="(item, index) in cartItems"
            :key="item.id"
            class="bg-gray-800/50 p-6 rounded-xl border border-gray-700 hover:border-red-500 transition-all"
          >
            <div class="flex gap-6">
              <!-- Image -->
              <img
                :src="item.images && item.images.length > 0 ? item.images[0] : 'https://via.placeholder.com/200x150?text=No+Image'"
                :alt="item.model"
                class="w-32 h-24 object-cover rounded-lg"
              />

              <!-- Details -->
              <div class="flex-1">
                <h3 class="text-xl font-bold text-white">{{ item.brand }} {{ item.model }}</h3>
                <p class="text-gray-400 text-sm">ปี {{ item.year }}</p>
                <p class="text-red-500 font-bold text-lg mt-2">฿{{ formatPrice(item.price) }}</p>
              </div>

              <!-- Remove Button -->
              <button
                @click="removeFromCart(index)"
                class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors h-fit"
              >
                <i class="fas fa-trash mr-2"></i>Remove
              </button>
            </div>
          </div>
        </div>

        <!-- Summary -->
        <div class="bg-gray-800/50 p-6 rounded-xl border border-gray-700 h-fit sticky top-20">
          <h2 class="text-2xl font-bold text-red-500 mb-6">สรุปการสั่งซื้อ</h2>

          <div class="space-y-4 mb-6">
            <div class="flex justify-between text-gray-300">
              <span>จำนวนรถ:</span>
              <span>{{ cartItems.length }} คัน</span>
            </div>
            <div class="flex justify-between text-gray-300">
              <span>ราคารวม:</span>
              <span class="text-2xl font-bold text-red-500">฿{{ formatPrice(totalPrice) }}</span>
            </div>
          </div>

          <button
            @click="checkout"
            class="w-full px-6 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105"
          >
            <i class="fas fa-credit-card mr-2"></i>ชำระเงิน
          </button>

          <NuxtLink
            to="/CarList"
            class="block w-full mt-3 px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-bold rounded-xl transition-all text-center"
          >
            <i class="fas fa-shopping-bag mr-2"></i>ซื้อเพิ่มเติม
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>

  <!-- Success Modal -->
  <SuccessModal
    :show="showSuccessModal"
    title="สั่งซื้อสำเร็จ!"
    :message="`ราคารวม: ฿${formatPrice(totalPrice)}`"
    icon="🎉"
    :duration="5"
    @close="handleSuccessClose"
  />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const cartItems = ref([])
const showSuccessModal = ref(false)

onMounted(() => {
  // โหลด cart จาก localStorage (แยกตามชื่อ username)
  const username = localStorage.getItem('username')
  const cartKey = `cart_${username}`
  const saved = localStorage.getItem(cartKey)
  if (saved) {
    cartItems.value = JSON.parse(saved)
  }
})

const totalPrice = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.price, 0)
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('th-TH').format(price)
}

const removeFromCart = (index) => {
  cartItems.value.splice(index, 1)
  const username = localStorage.getItem('username')
  const cartKey = `cart_${username}`
  localStorage.setItem(cartKey, JSON.stringify(cartItems.value))
}

const checkout = () => {
  showSuccessModal.value = true
  
  // ล้าง cart หลังจากแสดง modal
  setTimeout(() => {
    cartItems.value = []
    const username = localStorage.getItem('username')
    const cartKey = `cart_${username}`
    localStorage.removeItem(cartKey)
    
    // ไปหน้าอื่นหลังจากเสร็จสิ้น
    setTimeout(() => {
      router.push('/CarList')
    }, 1000)
  }, 5000)
}

const handleSuccessClose = () => {
  showSuccessModal.value = false
}
</script>

<style scoped>
/* animations */
</style>
