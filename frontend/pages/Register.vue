<template>
  <div class="flex justify-center items-center min-h-screen bg-black">
 <div class="bg-gradient-to-r from-gray-800 to-gray-600 p-6 rounded shadow w-80 text-white hover:scale-105 transform transition duration-300
">

      <h1 class="text-xl font-bold mb-4 text-center">Register</h1>

      <input
        v-model="username"
        placeholder="Username"
        class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300
"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300
"
      />

      <input
        v-model="confirmPassword"
        type="password"
        placeholder="Confirm Password"
        class="mb-4 p-2 border w-full rounded hover:scale-105 transform transition duration-300
"
      />

      <button
        @click="handleRegister"
        class="bg-black text-white p-2 w-full rounded hover:bg-gray-800 hover:scale-105 transform transition duration-300
"

      >
        Register
      </button>
        <p class="text-center text-sm mt-3">
  Already have an account?
  <router-link to="/login" class="text-blue-500 hover:underline">Login</router-link>
</p>

      <p v-if="errorMsg" class="text-red-500 text-sm mt-3 text-center">
        {{ errorMsg }}
      </p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleRegister = async () => {
  errorMsg.value = ''

  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match.'
    return
  }

  try {
    await axios.post('http://localhost:5000/api/register', {
      username: username.value,
      password: password.value
    })

    // หลังจาก register สำเร็จ ไปหน้า login
    router.push('/login')
  } catch (err) {
    errorMsg.value =
      err.response?.data?.msg || 'Registration failed. Please try again.'
  }
}
</script>
