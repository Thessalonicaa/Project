<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-sky-100 to-white">
    <div class="bg-gradient-to-r from-teal-300 to-sky-400 p-6 rounded shadow w-80 text-white hover:scale-105 transform transition duration-300">
      <form @submit.prevent="handleLogin"> <!-- เพิ่ม form -->
        <h1 class="text-xl font-bold mb-4 text-center">Login</h1>

        <input
          v-model="username"
          placeholder="Username"
          class="mb-3 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
        />

        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="mb-4 p-2 border w-full rounded hover:scale-105 transform transition duration-300"
        />

        <button
          type="submit"
          class="bg-sky-200 text-white p-2 w-full rounded hover:bg-sky-300 hover:scale-105 transform transition duration-300"
        >
          Login
        </button>
      </form>

      <p class="text-center text-sm mt-3">
        Don't have an account?
        <router-link to="/register" class="text-blue-500 hover:underline">Register</router-link>
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
const errorMsg = ref('')
const router = useRouter()

const handleLogin = async () => {
  errorMsg.value = ''
  try {
    const res = await axios.post('http://localhost:5000/api/login', {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('token', res.data.access_token)
    router.push('/dashboard')
  } catch (err) {
    errorMsg.value =
      err.response?.data?.msg || 'Login failed. Please try again.'
  }
}
</script>
