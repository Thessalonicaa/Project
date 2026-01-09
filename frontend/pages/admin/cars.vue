<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-950 to-gray-900 text-white p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-4xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
            <i class="fas fa-car mr-3"></i>Car Listings Management
          </h1>
          <p class="text-gray-400 mt-2">View, edit, and manage car listings from MongoDB</p>
        </div>
        <NuxtLink to="/admin" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-all flex items-center gap-2">
          <i class="fas fa-arrow-left"></i>Back to Dashboard
        </NuxtLink>
      </div>

      <div v-if="!isAdmin" class="text-center py-20">
        <p class="text-gray-400">Unauthorized</p>
        <NuxtLink to="/" class="text-red-400 mt-4 inline-block">Go Home</NuxtLink>
      </div>

      <div v-else>
        <!-- Search Bar -->
        <div class="mb-6 flex gap-4">
          <input 
            v-model="filter" 
            placeholder="Search by brand, model, or license plate..." 
            class="flex-1 px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white focus:border-red-500 focus:outline-none transition-all"
          />
          <button @click="fetchAll" class="px-6 py-3 bg-red-600 hover:bg-red-700 rounded-lg transition-all flex items-center gap-2 font-semibold">
            <i class="fas fa-sync"></i>Refresh
          </button>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto bg-gray-900/50 rounded-2xl border border-gray-700 shadow-xl">
          <table class="min-w-full text-left text-sm">
            <thead class="bg-gradient-to-r from-gray-800 to-gray-900 border-b border-gray-700">
              <tr>
                <th class="px-6 py-4 font-semibold text-gray-300">Brand/Model</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Year</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Price</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Seller</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Status</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in filtered" :key="c._id" class="border-t border-gray-800 hover:bg-gray-800/50 transition-colors">
                <td class="px-6 py-4 font-semibold">{{ c.brand }} {{ c.model }}</td>
                <td class="px-6 py-4">{{ c.year }}</td>
                <td class="px-6 py-4 text-red-400 font-bold">฿{{ formatPrice(c.price) }}</td>
                <td class="px-6 py-4 text-gray-400">{{ c.seller?.username || '-' }}</td>
                <td class="px-6 py-4">
                  <span :class="[
                    'px-3 py-1 rounded-full text-xs font-bold',
                    c.sold_out ? 'bg-red-600/30 text-red-300' : 'bg-green-600/30 text-green-300'
                  ]">
                    {{ c.sold_out ? 'Sold Out' : 'Available' }}
                  </span>
                </td>
                <td class="px-6 py-4 flex gap-2">
                  <button @click="openEdit(c)" class="px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-all text-sm font-semibold flex items-center gap-1">
                    <i class="fas fa-edit"></i>Edit
                  </button>
                  <button @click="confirmDelete(c)" class="px-3 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-all text-sm font-semibold flex items-center gap-1">
                    <i class="fas fa-trash"></i>Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editing" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 w-full max-w-2xl border border-gray-700 shadow-2xl animate-scale-in max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6 sticky top-0">
          <h3 class="text-2xl font-bold text-white">Edit Car Listing</h3>
          <button @click="closeEdit" class="text-gray-400 hover:text-white text-2xl">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Brand</label>
              <input v-model="editForm.brand" placeholder="Brand" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Model</label>
              <input v-model="editForm.model" placeholder="Model" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Year</label>
              <input v-model.number="editForm.year" type="number" placeholder="Year" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Price (฿)</label>
              <input v-model.number="editForm.price" type="number" placeholder="Price" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Description</label>
            <textarea v-model="editForm.description" placeholder="Description" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" rows="3"></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">License Plate</label>
              <input v-model="editForm.license_plate" placeholder="License Plate" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Status</label>
              <select v-model="editForm.sold_out" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all">
                <option :value="false">Available</option>
                <option :value="true">Sold Out</option>
              </select>
            </div>
          </div>
        </div>

        <div class="mt-6 flex gap-3">
          <button @click="saveEdit" class="flex-1 px-4 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 rounded-lg text-white font-bold transition-all transform hover:scale-105 flex items-center justify-center gap-2">
            <i class="fas fa-save"></i>Save Changes
          </button>
          <button @click="closeEdit" class="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-white font-semibold transition-all">
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 w-full max-w-md border border-red-500/50 shadow-2xl animate-scale-in">
        <div class="flex items-center justify-center w-12 h-12 rounded-full bg-red-600/20 mx-auto mb-4">
          <i class="fas fa-exclamation text-2xl text-red-500"></i>
        </div>
        
        <h3 class="text-2xl font-bold text-white text-center mb-2">Delete Car Listing?</h3>
        <p class="text-gray-400 text-center mb-6">
          Are you sure you want to delete <span class="font-semibold text-white">{{ deleteTarget?.brand }} {{ deleteTarget?.model }}</span>? This action cannot be undone.
        </p>

        <div class="flex gap-3">
          <button @click="performDelete" class="flex-1 px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 rounded-lg text-white font-bold transition-all transform hover:scale-105">
            Yes, Delete
          </button>
          <button @click="closeDeleteConfirm" class="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-white font-semibold transition-all">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const isAdmin = ref(false)
const cars = ref([])
const filter = ref('')
const editing = ref(false)
const editForm = ref({})
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)

const fetchAll = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/admin/cars')
    const data = await res.json()
    if (data.success) cars.value = data.cars || []
  } catch (e) { console.error(e) }
}

const filtered = computed(() => {
  if (!filter.value) return cars.value
  const q = filter.value.toLowerCase()
  return cars.value.filter(c => 
    (c.brand || '').toLowerCase().includes(q) || 
    (c.model || '').toLowerCase().includes(q) || 
    (c.license_plate || '').toLowerCase().includes(q)
  )
})

const formatPrice = (p) => p?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') || 0

const openEdit = (c) => { editForm.value = { ...c }; editing.value = true }
const closeEdit = () => { editing.value = false; editForm.value = {} }

const saveEdit = async () => {
  try {
    const res = await fetch(`http://localhost:5000/api/admin/cars/${editForm.value._id}`, { 
      method: 'PUT', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify(editForm.value) 
    })
    const data = await res.json()
    if (data.success) { fetchAll(); closeEdit(); alert('✅ Car updated successfully!') }
  } catch (e) { console.error(e); alert('❌ Error updating car') }
}

const confirmDelete = (c) => { deleteTarget.value = c; showDeleteConfirm.value = true }
const closeDeleteConfirm = () => { showDeleteConfirm.value = false; deleteTarget.value = null }

const performDelete = async () => {
  try {
    const res = await fetch(`http://localhost:5000/api/admin/cars/${deleteTarget.value._id}`, { method: 'DELETE' })
    const data = await res.json()
    if (data.success) { fetchAll(); closeDeleteConfirm(); alert('✅ Car deleted successfully!') }
  } catch (e) { console.error(e); alert('❌ Error deleting car') }
}

onMounted(() => {
  if (process.client) {
    const role = localStorage.getItem('role')
    isAdmin.value = role === 'admin' || localStorage.getItem('is_admin') === 'true'
    if (!isAdmin.value) return
    fetchAll()
  }
})
</script>

<style scoped>
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
.animate-scale-in { animation: scaleIn 0.3s ease-out; }
</style>