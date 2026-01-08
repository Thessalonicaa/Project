<template>
  <div class="flex justify-center items-center min-h-screen bg-black">
    <div
      class="bg-gradient-to-r from-gray-800 to-gray-600 p-6 rounded shadow w-80 text-black hover:scale-105 transform transition duration-300"
    >
      <h1 class="text-xl font-bold mb-4 text-center text-white">Login</h1>

      <form @submit.prevent="handleLogin">
        <input
          v-model="username"
          type="text"
          placeholder="Username"
          class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
          required
          @keyup.enter="handleLogin"
        />

        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="mb-4 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
          required
          @keyup.enter="handleLogin"
        />

        <button
          type="submit"
          class="bg-black text-white p-2 w-full rounded hover:bg-gray-800 hover:scale-105 transform transition duration-300"
        >
          Login
        </button>
      </form>

      <p class="text-center text-sm mt-3 text-white">
        Don't have an account?
        <router-link to="/register" class="text-blue-500 hover:underline">
          Register
        </router-link>
      </p>

      <p v-if="error" class="text-red-500 text-sm mt-3 text-center">
        {{ error }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      localStorage.setItem('token', data.token)
      localStorage.setItem('user_id', data.user_id)
      localStorage.setItem('username', data.username)
      localStorage.setItem('role', data.role)
      localStorage.setItem('is_seller', data.is_seller)

      if (data.is_seller) {
        router.push('/seller/PostCar')
      } else {
        router.push('/dashboard')
      }
    } else {
      console.log('Error response:', data) // For debugging
      if (data.error.includes('ชื่อผู้ใช้') && data.error.includes('รหัสผ่าน')) {
        error.value = 'ชื่อผู้ใช้และรหัสผ่านไม่ถูกต้อง'
      } else if (data.error.includes('ชื่อผู้ใช้')) {
        error.value = 'ชื่อผู้ใช้ไม่ถูกต้อง'
      } else if (data.error.includes('รหัสผ่าน')) {
        error.value = 'รหัสผ่านไม่ถูกต้อง'
      } else {
        error.value = data.error || 'เกิดข้อผิดพลาดในการเข้าสู่ระบบ'
      }
    }
  } catch (err) {
    error.value = 'เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์'
    console.error('Login error:', err)
  }
}
</script>