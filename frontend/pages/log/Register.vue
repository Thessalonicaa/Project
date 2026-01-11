<!-- pages/Register.vue -->
<template>
  <div class="flex justify-center items-center min-h-screen bg-black">
    <div
      class="bg-gradient-to-r from-gray-800 to-gray-600 p-6 rounded shadow w-80 text-black hover:scale-105 transform transition duration-300"
    >
      <h1 class="text-xl font-bold mb-4 text-center text-white">Register</h1>

      <form @submit.prevent="handleRegister">
        <input
          v-model="username"
          placeholder="Username"
          class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
        />
        <input
          v-model="confirmPassword"
          type="password"
          placeholder="Confirm Password"
          class="mb-4 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
        />
        <button
          type="submit"
          class="bg-black text-white p-2 w-full rounded hover:bg-gray-800 hover:scale-105 transform transition duration-300"
        >
          Register
        </button>
      </form>

      <p class="text-center text-sm mt-3 text-white">
        Already have an account?
        <router-link to="/login" class="text-blue-400 hover:underline">
          Login
        </router-link>
      </p>

      <p v-if="errorMsg" class="text-red-500 text-sm mt-3 text-center">
        {{ errorMsg }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleRegister = async () => {
  if (!username.value || !password.value) {
    errorMsg.value = 'Please fill all fields'
    return
  }
  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match'
    return
  }

  try {
    const response = await axios.post('http://localhost:5000/api/register', {
      username: username.value,
      password: password.value,
      role: 'user'  // เปลี่ยนจาก buyer เป็น user
    })

    // ถ้าสำเร็จ (backend คืน status 201 หรือ msg) ให้ไปหน้า login ทันที
    if (response.status === 201 || response.data?.msg || response.data?.success) {
      router.push('/login')
      return
    } else {
      errorMsg.value = response.data.message || 'มีข้อผิดพลาดในการลงทะเบียน กรุณาลองใหม่อีกครั้งในภายหลัง'
    }
  } catch (error) {
    console.error('Registration error:', error.response?.data)
    errorMsg.value = error.response?.data?.message || 'มีชื่อซ้ำในระบบ กรุณาลองใหม่อีกครั้ง'
  }
}
</script>
