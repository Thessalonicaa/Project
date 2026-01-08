<template>
  <div 
    class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50"
    @click="handleClick"
  >
    <div class="text-center p-8 transform transition-all duration-500 scale-110">
      <div class="text-red-500 text-6xl mb-4">
        <i class="fas fa-exclamation-circle"></i>
      </div>
      <h2 class="text-white text-2xl font-bold mb-4">{{ title }}</h2>
      <p class="text-gray-300 mb-6">{{ message }}</p>
      <p class="text-gray-400 text-sm animate-pulse">คลิกที่ใดก็ได้เพื่อกลับ</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  title: {
    type: String,
    default: 'ไม่สามารถเข้าถึงได้'
  },
  message: {
    type: String,
    default: 'คุณไม่มีสิทธิ์เข้าถึงหน้านี้ กรุณาลงทะเบียนเป็นผู้ขายก่อน'
  },
  redirectTo: {
    type: String,
    default: '/dashboard'
  }
})

const router = useRouter()

const handleClick = () => {
  router.push(props.redirectTo)
}
</script>