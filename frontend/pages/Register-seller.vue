<template>
  <div class="min-h-screen p-6 relative overflow-hidden">
    <div class="register-seller-page animate-fade-in">
      <!-- Beams Background -->
      <div class="beams-background">
        <Beams
          :beamWidth="3"
          :beamHeight="25"
          :beamNumber="20"
          lightColor="#ff3c03"
          :speed="2"
          :noiseIntensity="1.75"
          :scale="0.2"
          :rotation="30"
          :width="1920"
          :height="1080"
        />
      </div>

      <div class="flex justify-center items-center min-h-screen relative z-10">
        <div class="register-seller-card bg-gradient-to-br from-gray-900/90 via-gray-800/90 to-gray-900/90 backdrop-blur-xl p-8 rounded-2xl shadow-2xl w-[450px] text-black border border-gray-700/50">
          <h1 class="text-3xl font-bold mb-6 text-center text-white animate-fadeInDown">
            <span class="bg-gradient-to-r from-orange-500 via-red-500 to-orange-500 bg-clip-text text-transparent">
              Register as Seller
            </span>
          </h1>

          <form @submit.prevent="handleRegister" class="space-y-4">
            <div class="input-group">
              <input
                v-model="username"
                type="text"
                placeholder="Username"
                class="w-full p-3 border border-gray-600 bg-gray-700/50 text-gray-400 rounded-lg cursor-not-allowed"
                readonly
              />
            </div>

            <div class="input-group">
              <input
                v-model="email"
                type="email"
                placeholder="Email"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
                required
              />
            </div>

            <div class="input-group">
              <input
                v-model="shopName"
                type="text"
                placeholder="Shop Name"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
                required
              />
            </div>

            <div class="input-group">
              <input
                v-model="phone"
                type="text"
                placeholder="Phone Number"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              />
            </div>

            <div class="input-group">
              <textarea
                v-model="address"
                placeholder="Address"
                rows="3"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400 resize-none"
                required
              ></textarea>
            </div>

            <button
              type="submit"
              class="w-full p-3 rounded-lg bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-semibold shadow-lg hover:shadow-orange-500/50 transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              :disabled="!isFormValid"
            >
              Register as Seller
            </button>
          </form>

          <p class="text-center text-sm mt-6 text-gray-300">
            Already have an account?
            <NuxtLink to="/login" class="text-orange-500 hover:text-orange-400 font-semibold hover:underline transition-colors">
              Login
            </NuxtLink>
          </p>

          <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center bg-red-900/20 p-3 rounded-lg border border-red-500/30 animate-shake">
            {{ errorMsg }}
          </p>
        </div>
      </div>

      <!-- Success Modal -->
      <SuccessRegistrationModal
        :show="showSuccessModal"
        title="Seller Registration Successful"
        @redirect="redirectNow"
        @close="showSuccessModal = false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Beams from '~/components/Beams.vue'
import SuccessRegistrationModal from '~/components/SuccessRegistrationModal.vue'

const router = useRouter()
const username = ref('')
const email = ref('')
const shopName = ref('')
const phone = ref('')
const address = ref('')
const errorMsg = ref('')
const showSuccessModal = ref(false)

onMounted(() => {
  const storedUsername = localStorage.getItem('username')
  if (storedUsername) username.value = storedUsername

  window.addEventListener('keydown', handleEnter)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleEnter)
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
      errorMsg.value = 'Please fill in all fields correctly.'
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
    } else {
      errorMsg.value = response.data.message || 'Registration failed'
    }
  } catch (error) {
    console.error('Registration error:', error.response?.data)
    errorMsg.value =
      error.response?.data?.message ||
      'Error registering. Please try again.'
  }
}

const redirectNow = () => {
  // Clear all authentication data
  localStorage.removeItem('token')
  localStorage.removeItem('user_id')
  localStorage.removeItem('username')
  localStorage.removeItem('role')
  localStorage.removeItem('is_seller')
  localStorage.removeItem('is_admin')
  localStorage.removeItem('app_initialized')
  sessionStorage.removeItem('zavora_loader_shown')
  
  // Force redirect to login
  window.location.href = '/login'
}
</script>

<style scoped>
.register-seller-page {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.beams-background {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 0;
  opacity: 0.6;
}

.register-seller-card {
  animation: fadeInUp 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.input-group {
  animation: fadeInLeft 0.6s ease-out;
}

.input-group:nth-child(2) { animation-delay: 0.1s; }
.input-group:nth-child(3) { animation-delay: 0.2s; }
.input-group:nth-child(4) { animation-delay: 0.3s; }
.input-group:nth-child(5) { animation-delay: 0.4s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

@keyframes modalPop {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes checkPop {
  from {
    opacity: 0;
    transform: scale(0) rotate(-180deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.animate-fadeInDown {
  animation: fadeInDown 0.8s ease-out;
}

.animate-shake {
  animation: shake 0.5s ease-in-out;
}

.animate-fade-in {
  animation: fadeIn 1s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
