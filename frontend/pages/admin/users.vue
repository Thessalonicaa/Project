<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-950 to-gray-900 text-white p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-4xl font-extrabold bg-gradient-to-r from-blue-500 to-blue-400 bg-clip-text text-transparent">
            <i class="fas fa-users mr-3"></i>Users & Sellers Management
          </h1>
          <p class="text-gray-400 mt-2">View, edit, and manage user accounts</p>
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
            placeholder="Search by username or email..." 
            class="flex-1 px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white focus:border-blue-500 focus:outline-none transition-all"
          />
          <button @click="fetchAll" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-all flex items-center gap-2 font-semibold">
            <i class="fas fa-sync"></i>Refresh
          </button>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto bg-gray-900/50 rounded-2xl border border-gray-700 shadow-xl">
          <table class="min-w-full text-left text-sm">
            <thead class="bg-gradient-to-r from-gray-800 to-gray-900 border-b border-gray-700">
              <tr>
                <th class="px-6 py-4 font-semibold text-gray-300">Username</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Role</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Created Date</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in filtered" :key="u._id" class="border-t border-gray-800 hover:bg-gray-800/50 transition-colors">
                <td class="px-6 py-4 font-semibold">{{ u.username }}</td>
                <td class="px-6 py-4">
                  <span :class="[
                    'px-3 py-1 rounded-full text-xs font-bold',
                    u.role === 'admin' ? 'bg-red-600/30 text-red-300' : u.role === 'seller' ? 'bg-blue-600/30 text-blue-300' : 'bg-gray-600/30 text-gray-300'
                  ]">
                    {{ u.role || 'user' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-gray-400">{{ formatDate(u.created_at) }}</td>
                <td class="px-6 py-4 flex gap-2">
                  <button @click="openEdit(u)" class="px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-all text-sm font-semibold flex items-center gap-1">
                    <i class="fas fa-edit"></i>Edit
                  </button>
                  <button @click="confirmDelete(u)" class="px-3 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-all text-sm font-semibold flex items-center gap-1">
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
      <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 w-full max-w-md border border-gray-700 shadow-2xl animate-scale-in">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-white">Edit User Account</h3>
          <button @click="closeEdit" class="text-gray-400 hover:text-white text-2xl">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Username</label>
            <input v-model="editForm.username" class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Role</label>
            <select v-model="editForm.role" class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all">
              <option value="user">User</option>
              <option value="seller">Seller</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Email</label>
            <input v-model="editForm.email" type="email" class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Address</label>
            <input v-model="editForm.address" class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Phone Number</label>
            <input v-model="editForm.phonenumber" class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
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
        
        <h3 class="text-2xl font-bold text-white text-center mb-2">Delete Account?</h3>
        <p class="text-gray-400 text-center mb-6">
          Are you sure you want to delete <span class="font-semibold text-white">{{ deleteTarget?.username }}</span>? This action cannot be undone.
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

    <!-- Notification Toast -->
    <transition name="slide-down">
      <div 
        v-if="notification.show"
        :class="[
          'fixed top-6 left-1/2 transform -translate-x-1/2 z-[100] px-8 py-4 rounded-2xl border shadow-2xl flex items-center gap-3 animate-slide-down',
          notification.type === 'success' 
            ? 'bg-gradient-to-r from-green-600 to-green-700 border-green-500/50 text-white' 
            : 'bg-gradient-to-r from-red-600 to-red-700 border-red-500/50 text-white'
        ]"
      >
        <i :class="[
          'text-2xl',
          notification.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'
        ]"></i>
        <span class="font-semibold text-lg">{{ notification.message }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const isAdmin = ref(false)
const users = ref([])
const filter = ref('')
const editing = ref(false)
const editForm = ref({})
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)
const notification = ref({ show: false, message: '', type: 'success' })

const fetchAll = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/admin/users')
    const data = await res.json()
    if (data.success) users.value = data.users || []
  } catch (e) { console.error(e) }
}

const filtered = computed(() => {
  if (!filter.value) return users.value
  return users.value.filter(u => 
    (u.username || '').toLowerCase().includes(filter.value.toLowerCase())
  )
})

const formatDate = (d) => d ? new Date(d).toLocaleDateString('th-TH') : '-'

const openEdit = (u) => { editForm.value = { ...u }; editing.value = true }
const closeEdit = () => { editing.value = false; editForm.value = {} }

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

const saveEdit = async () => {
  try {
    const res = await fetch(`http://localhost:5000/api/admin/users/${editForm.value._id}`, {
      method: 'PUT', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify(editForm.value)
    })
    const data = await res.json()
    if (data.success) { 
      fetchAll()
      closeEdit()
      showNotification('✅ User updated successfully!', 'success')
    } else {
      showNotification('❌ ' + (data.message || 'Error updating user'), 'error')
    }
  } catch (e) { 
    console.error(e)
    showNotification('❌ Error updating user', 'error')
  }
}

const confirmDelete = (u) => { deleteTarget.value = u; showDeleteConfirm.value = true }
const closeDeleteConfirm = () => { showDeleteConfirm.value = false; deleteTarget.value = null }

const performDelete = async () => {
  try {
    const res = await fetch(`http://localhost:5000/api/admin/users/${deleteTarget.value._id}`, { method: 'DELETE' })
    const data = await res.json()
    if (data.success) { 
      fetchAll()
      closeDeleteConfirm()
      showNotification('✅ User deleted successfully!', 'success')
    } else {
      showNotification('❌ ' + (data.message || 'Error deleting user'), 'error')
    }
  } catch (e) { 
    console.error(e)
    showNotification('❌ Error deleting user', 'error')
  }
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

@keyframes slideDown {
  from { 
    opacity: 0; 
    transform: translate(-50%, -30px); 
  }
  to { 
    opacity: 1; 
    transform: translate(-50%, 0); 
  }
}

@keyframes slideUp {
  from { 
    opacity: 1; 
    transform: translate(-50%, 0); 
  }
  to { 
    opacity: 0; 
    transform: translate(-50%, -30px); 
  }
}

.animate-scale-in { animation: scaleIn 0.3s ease-out; }
.animate-slide-down { animation: slideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }

.slide-down-enter-active { animation: slideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.slide-down-leave-active { animation: slideUp 0.3s ease-in; }
</style>