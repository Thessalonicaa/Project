<template>
  <div class="flex justify-center items-center min-h-screen bg-black">
    <div
      class="bg-gradient-to-r from-gray-800 to-gray-600 p-6 rounded shadow-lg w-96 text-black hover:scale-105 transform transition duration-300"
    >
      <h1 class="text-xl font-bold mb-4 text-center text-white">
        Register as Seller
      </h1>

      <!-- ✅ เมื่อกด Enter จะเรียก handleRegister -->
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <input
            v-model="username"
            type="text"
            placeholder="Username"
            class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
            readonly
          />
        </div>

        <div>
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
            required
          />
        </div>

        <div>
          <input
            v-model="shopName"
            type="text"
            placeholder="Shop Name"
            class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
            required
          />
        </div>

        <div>
          <input
            v-model="phone"
            type="text"
            placeholder="Phone Number"
            class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
          />
        </div>

        <!-- ✅ Address Field -->
        <div>
          <textarea
            v-model="address"
            placeholder="Address"
            rows="3"
            class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
            required
          ></textarea>
        </div>

        <button
          type="submit"
          class="bg-black text-white p-2 w-full rounded hover:bg-gray-800 hover:scale-105 transform transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!isFormValid"
        >
          Register as Seller
        </button>
      </form>

      <p class="text-center text-sm mt-3 text-white">
        Already have an account?
        <NuxtLink to="/login" class="text-blue-500 hover:underline">
          Login
        </NuxtLink>
      </p>

      <p v-if="errorMsg" class="text-red-500 text-sm mt-3 text-center">
        {{ errorMsg }}
      </p>
    </div>
  </div>

  <!-- ✅ Fullscreen Success Modal -->
  <template v-if="showSuccessModal">
    <div
      class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 backdrop-blur-sm"
      @click="redirectNow"
    >
      <div
        @click.stop
        class="bg-gray-900 p-6 rounded-lg text-center max-w-md w-full mx-4 animate-fadeIn"
      >
        <h3 class="text-white text-xl font-bold mb-2">
          ลงทะเบียนผู้ขายสำเร็จ
        </h3>
        <p class="text-gray-300 mb-4">
          ระบบจะพาไปหน้าเข้าสู่ระบบในอีก {{ countdown }} วินาที
        </p>
      </div>
    </div>
  </template>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const username = ref('')
const email = ref('')
const shopName = ref('')
const phone = ref('')
const address = ref('')
const errorMsg = ref('')
const showSuccessModal = ref(false)
const countdown = ref(5)
let countdownInterval = null
let redirectTimeout = null

// ✅ ดึง username จาก localStorage
onMounted(() => {
  const storedUsername = localStorage.getItem('username')
  if (storedUsername) username.value = storedUsername

  // ✅ รองรับการกด Enter เพื่อ Register
  window.addEventListener('keydown', handleEnter)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleEnter)
  clearInterval(countdownInterval)
  clearTimeout(redirectTimeout)
})

const handleEnter = (e) => {
  if (e.key === 'Enter') {
    handleRegister()
  }
}

const isFormValid = computed(() => {
  return username.value && email.value && shopName.value && address.value
})

const handleRegister = async () => {
  try {
    if (!isFormValid.value) {
      errorMsg.value = 'กรุณากรอกข้อมูลให้ครบทุกช่อง'
      return
    }

    const token = localStorage.getItem('token')
    if (!token) {
      errorMsg.value = 'You must be logged in to register as a seller.'
      return
    }

    const response = await axios.post(
      'http://localhost:5000/api/register/seller',
      {
        email: email.value,
        business_name: shopName.value,
        contact_info: address.value,
        phonenumber: phone.value,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (response.status === 201) {
      showSuccessModal.value = true
      countdown.value = 5

      countdownInterval = setInterval(() => {
        countdown.value = Math.max(0, countdown.value - 1)
      }, 1000)

      redirectTimeout = setTimeout(() => {
        router.push('/login')
      }, 5000)
    } else {
      errorMsg.value = response.data.message || 'ลงทะเบียนไม่สำเร็จ'
    }
  } catch (error) {
    console.error('Registration error:', error.response?.data)
    errorMsg.value =
      error.response?.data?.message ||
      'มีข้อผิดพลาดในการลงทะเบียน กรุณาลองใหม่อีกครั้ง'
  }
}

const redirectNow = () => {
  clearInterval(countdownInterval)
  clearTimeout(redirectTimeout)
  router.push('/login')
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}
</style>
