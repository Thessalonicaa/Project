// filepath: e:\ProjectFainal\frontend\pages\orders.vue
<template>
  <div class="min-h-screen bg-gray-950 text-white p-6">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8 animate-slide-down">
        <h1 class="text-4xl font-extrabold text-red-500 mb-2 drop-shadow-lg">
          <i class="fas fa-receipt mr-3"></i>My Orders
        </h1>
        <p class="text-gray-400">ดูประวัติการซื้อขายของคุณ</p>
      </div>

      <!-- Tabs -->
      <div class="flex gap-4 mb-8 border-b border-gray-700">
        <button
          @click="activeTab = 'purchases'"
          :class="[
            'pb-3 px-4 font-semibold transition-colors',
            activeTab === 'purchases'
              ? 'text-red-500 border-b-2 border-red-500'
              : 'text-gray-400 hover:text-gray-300'
          ]"
        >
          <i class="fas fa-shopping-bag mr-2"></i>My Purchases
        </button>
        <button
          v-if="isSeller"
          @click="activeTab = 'sales'"
          :class="[
            'pb-3 px-4 font-semibold transition-colors',
            activeTab === 'sales'
              ? 'text-red-500 border-b-2 border-red-500'
              : 'text-gray-400 hover:text-gray-300'
          ]"
        >
          <i class="fas fa-store mr-2"></i>My Sales
        </button>
      </div>

      <!-- Purchases Tab -->
      <div v-if="activeTab === 'purchases'" class="space-y-4 animate-fade-in">
        <div v-if="purchases.length === 0" class="text-center py-12">
          <i class="fas fa-inbox text-6xl text-gray-600 mb-4"></i>
          <p class="text-gray-400">ยังไม่มีการซื้อสินค้า</p>
        </div>

        <!-- Purchases Table -->
        <div v-else class="overflow-x-auto bg-gray-800/50 rounded-xl border border-gray-700">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-700 bg-gray-800">
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">รถ</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ปี</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ราคา</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ผู้ขาย</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">วันที่ซื้อ</th>
                <th class="px-6 py-4 text-center text-sm font-semibold text-gray-300">สถานะ</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(order, index) in purchases" 
                :key="order.id"
                class="border-b border-gray-700 hover:bg-gray-700/50 transition-colors animate-form-item"
                :style="{ 'animation-delay': `${index * 0.05}s` }"
              >
                <!-- Car Image & Name -->
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <img 
                      :src="order.car.images?.[0]" 
                      :alt="order.car.model"
                      class="w-12 h-12 object-cover rounded"
                    />
                    <div>
                      <p class="font-semibold text-white">{{ order.car.brand }} {{ order.car.model }}</p>
                      <p class="text-xs text-gray-400">License: {{ order.car.license_plate }}</p>
                    </div>
                  </div>
                </td>
                <!-- Year -->
                <td class="px-6 py-4 text-white">{{ order.car.year }}</td>
                <!-- Price -->
                <td class="px-6 py-4 text-red-500 font-bold">฿{{ formatPrice(order.car.price) }}</td>
                <!-- Seller -->
                <td class="px-6 py-4">
                  <NuxtLink
                    :to="`/profile?user=${order.seller.username}`"
                    class="flex items-center gap-2 text-red-500 hover:text-red-400 transition-colors"
                  >
                    <i class="fas fa-store text-sm"></i>
                    <span>{{ order.seller.username }}</span>
                  </NuxtLink>
                  <p class="text-xs text-gray-400">{{ order.seller.businessName }}</p>
                </td>
                <!-- Date -->
                <td class="px-6 py-4 text-gray-300 text-sm">{{ formatDate(order.purchaseDate) }}</td>
                <!-- Status -->
                <td class="px-6 py-4 text-center">
                  <span class="px-3 py-1 bg-green-600/20 border border-green-600 text-green-400 rounded-full text-xs font-semibold">
                    <i class="fas fa-check-circle mr-1"></i>ซื้อแล้ว
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Sales Tab (Seller Only) -->
      <div v-if="activeTab === 'sales' && isSeller" class="space-y-4 animate-fade-in">
        <div v-if="sales.length === 0" class="text-center py-12">
          <i class="fas fa-inbox text-6xl text-gray-600 mb-4"></i>
          <p class="text-gray-400">ยังไม่มีการขายสินค้า</p>
        </div>

        <!-- Sales Table -->
        <div v-else class="overflow-x-auto bg-gray-800/50 rounded-xl border border-gray-700">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-700 bg-gray-800">
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">รถ</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ปี</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ราคา</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ผู้ซื้อ</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">วันที่ขาย</th>
                <th class="px-6 py-4 text-center text-sm font-semibold text-gray-300">สถานะ</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(order, index) in sales" 
                :key="order.id"
                class="border-b border-gray-700 hover:bg-gray-700/50 transition-colors animate-form-item"
                :style="{ 'animation-delay': `${index * 0.05}s` }"
              >
                <!-- Car Image & Name -->
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <img 
                      :src="order.car.images?.[0]" 
                      :alt="order.car.model"
                      class="w-12 h-12 object-cover rounded"
                    />
                    <div>
                      <p class="font-semibold text-white">{{ order.car.brand }} {{ order.car.model }}</p>
                      <p class="text-xs text-gray-400">License: {{ order.car.license_plate }}</p>
                    </div>
                  </div>
                </td>
                <!-- Year -->
                <td class="px-6 py-4 text-white">{{ order.car.year }}</td>
                <!-- Price -->
                <td class="px-6 py-4 text-green-500 font-bold">฿{{ formatPrice(order.car.price) }}</td>
                <!-- Buyer -->
                <td class="px-6 py-4">
                  <NuxtLink
                    :to="`/profile?user=${order.buyer.username}`"
                    class="flex items-center gap-2 text-blue-500 hover:text-blue-400 transition-colors"
                  >
                    <i class="fas fa-user text-sm"></i>
                    <span>{{ order.buyer.username }}</span>
                  </NuxtLink>
                </td>
                <!-- Date -->
                <td class="px-6 py-4 text-gray-300 text-sm">{{ formatDate(order.saleDate) }}</td>
                <!-- Status -->
                <td class="px-6 py-4 text-center">
                  <span class="px-3 py-1 bg-green-600/20 border border-green-600 text-green-400 rounded-full text-xs font-semibold">
                    <i class="fas fa-check-circle mr-1"></i>ขายแล้ว
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const activeTab = ref('purchases')
const purchases = ref([])
const sales = ref([])
const username = ref('')

const isSeller = computed(() => {
  if (!process.client) return false
  return localStorage.getItem('is_seller') === 'true'
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('th-TH').format(price)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('th-TH', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  if (process.client) {
    username.value = localStorage.getItem('username') || ''
    fetchOrders()
  }
})

const fetchOrders = async () => {
  try {
    // Fetch purchases
    const purchasesRes = await fetch(`http://localhost:5000/api/orders/purchases?username=${username.value}`)
    const purchasesData = await purchasesRes.json()
    if (purchasesData.success) {
      purchases.value = purchasesData.orders
    }

    // Fetch sales if seller
    if (isSeller.value) {
      const salesRes = await fetch(`http://localhost:5000/api/orders/sales?username=${username.value}`)
      const salesData = await salesRes.json()
      if (salesData.success) {
        sales.value = salesData.orders
      }
    }
  } catch (error) {
    console.error('Error fetching orders:', error)
  }
}
</script>

<style scoped>
.animate-slide-down {
  animation: slideDown 0.6s ease-out;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

.animate-form-item {
  animation: formItem 0.5s ease-out forwards;
  opacity: 0;
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
</style>
