<template>
  <teleport to="body">
    <transition name="fade">
      <div v-if="show" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70" @click="handleClose">
        <div 
          class="relative bg-gray-900 rounded-2xl p-8 max-w-md w-full mx-4 animate-pop-in"
          @click.stop
        >
          <!-- Success Icon with Animation -->
          <div class="flex justify-center mb-6">
            <div class="animate-success-icon text-6xl">
              {{ icon }}
            </div>
          </div>

          <!-- Title -->
          <h2 class="text-2xl font-bold text-white text-center mb-2">
            {{ title }}
          </h2>

          <!-- Message -->
          <p class="text-gray-300 text-center mb-6">
            {{ message }}
          </p>

          <!-- Progress Bar -->
          <div class="w-full bg-gray-700 rounded-full h-1 overflow-hidden mb-4">
            <div 
              class="bg-red-500 h-full animate-countdown"
              :style="{ '--countdown-duration': `${duration}s` }"
            ></div>
          </div>

          <!-- Auto close text -->
          <p class="text-gray-500 text-sm text-center">
            ปิดอัตโนมัติใน {{ remainingTime }} วินาที
          </p>

          <!-- Close Button -->
          <button
            @click="handleClose"
            class="mt-6 w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition-colors"
          >
            ปิด
          </button>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  show: Boolean,
  title: String,
  message: String,
  icon: {
    type: String,
    default: '✅'
  },
  duration: {
    type: Number,
    default: 5
  }
})

const emit = defineEmits(['close'])
const remainingTime = ref(props.duration)

watch(() => props.show, (newVal) => {
  if (newVal) {
    remainingTime.value = props.duration
    const interval = setInterval(() => {
      remainingTime.value--
      if (remainingTime.value <= 0) {
        clearInterval(interval)
        emit('close')
      }
    }, 1000)
  }
})

const handleClose = () => {
  emit('close')
}
</script>

<style scoped>
@keyframes popIn {
  0% {
    opacity: 0;
    transform: scale(0.5) translateY(-50px);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes successIcon {
  0% {
    transform: scale(0) rotate(0deg);
  }
  50% {
    transform: scale(1.2) rotate(10deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
  }
}

@keyframes countdown {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

.animate-pop-in {
  animation: popIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.animate-success-icon {
  animation: successIcon 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.animate-countdown {
  animation: countdown var(--countdown-duration, 5s) linear forwards;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
