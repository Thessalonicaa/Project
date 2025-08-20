<template>
  <div class="bg-gradient-to-r from-sky-100 to-blue-100 p-4 rounded-xl shadow-md transition-transform hover:scale-[1.01]">
    <div class="flex justify-between items-start">
      <div>
        <h2 class="font-semibold text-lg text-gray-800 mb-2">{{ note.title }}</h2>

        <p class="text-sm text-gray-700">
          🟢 เวลาเข้า: {{ formatDate(note.created_at) }}
        </p>

        <p class="text-sm text-gray-700" v-if="localNote.checkout">
          🔴 เวลาออก: {{ formatDate(localNote.checkout) }}
        </p>

        <p v-else class="text-sm text-yellow-600 italic">ยังไม่ลงเวลาออก</p>
      </div>

      <div class="text-right">
        <button
          @click="markCheckout"
          class="bg-red-500 hover:bg-red-600 text-white text-sm px-3 py-1 rounded mb-1"
          title="ลงเวลาออก"
          v-if="!localNote.checkout"
        >
          ลงเวลาออก
        </button>

        <p v-if="showConfirmation" class="text-green-600 text-sm">✅ ลงเวลาออกแล้ว</p>

        <button
          @click="$emit('delete', localNote.id)"
          class="text-red-500 text-sm hover:text-red-700 hover:underline transition mt-1 block"
          title="ลบรายการนี้"
        >
          ลบ
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({ note: Object })
const emit = defineEmits(['delete', 'checkout'])

const localNote = reactive({
  ...props.note,
  checkout: localStorage.getItem(`checkout_${props.note.id}`) || props.note.checkout
})

watch(() => props.note, (newValue) => {
  Object.assign(localNote, {
    ...newValue,
    checkout: localStorage.getItem(`checkout_${newValue.id}`) || newValue.checkout
  })
}, { deep: true })
const showConfirmation = ref(false)

function formatDate(dateStr) {
  const d = new Date(dateStr)
  return (
    d.getFullYear() + '-' +
    String(d.getMonth() + 1).padStart(2, '0') + '-' +
    String(d.getDate()).padStart(2, '0') + ' ' +
    String(d.getHours()).padStart(2, '0') + ':' +
    String(d.getMinutes()).padStart(2, '0') + ':' +
    String(d.getSeconds()).padStart(2, '0')
  )
}

function markCheckout() {
  // สร้างเวลาปัจจุบัน
  const now = new Date()
  // อัพเดตค่า checkout ใน localNote
  localNote.checkout = now.toISOString()
  // เก็บค่า checkout ใน localStorage
  localStorage.setItem(`checkout_${localNote.id}`, now.toISOString())
  // ส่ง ID และเวลา checkout ให้ backend
  emit('checkout', {
    id: localNote.id,
    checkout: now.toISOString()
  })

  showConfirmation.value = true
  setTimeout(() => {
    showConfirmation.value = false
  }, 3000)
}

function handleDelete() {
  localStorage.removeItem(`checkout_${localNote.id}`)
  emit('delete', localNote.id)
}

</script> 
