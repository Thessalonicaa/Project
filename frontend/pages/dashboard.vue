<template>
  <div class="min-h-screen bg-gradient-to-br from-sky-100 to-white p-6">
    <div class="max-w-3xl mx-auto bg-white rounded-2xl shadow-lg p-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">ระบบลงเวลา</h1>

    <div class="flex gap-2 mb-6">
    <input
      v-model="title"
      placeholder="กรอกชื่อพนักงาน..."
      class="flex-1 px-4 py-2 border rounded-xl shadow-sm
             transition-colors duration-300
             bg-white focus:bg-sky-100
             text-gray-800 focus:outline-none focus:ring-2 focus:ring-sky-300"
             />
        <button
          @click="createNote"
          class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-xl shadow-md transition hover:scale-105 transform transition duration-300
"
        >
          ลงเวลา
        </button>
      </div>

      <div v-if="notes.length === 0" class="text-center text-gray-500 italic">
        ยังไม่มีการลงเวลา
      </div>

      <div class="space-y-4">
        <NoteCard
          v-for="note in notes"
          :key="note.id"
          :note="note"
          @delete="deleteNote"
          @checkout="handleCheckout"
        />
      </div>
    </div>
  </div>
</template>



<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const title = ref('')
const notes = ref([])

const fetchNotes = async () => {
  const token = localStorage.getItem('token')
  const res = await axios.get('http://localhost:5000/api/notes', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  notes.value = res.data
}

const createNote = async () => {
  const token = localStorage.getItem('token')
  const currentTime = new Date().toLocaleString() // เช่น "25/6/2025, 09:12:34"

  try {
    await axios.post('http://localhost:5000/api/notes', {
      title: title.value,
      content: currentTime
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    title.value = ''
    fetchNotes()
  } catch (e) {
    console.error('Create note failed:', e)
  }
}

const deleteNote = async (id) => {
  const token = localStorage.getItem('token')
  await axios.delete(`http://localhost:5000/api/notes/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  fetchNotes()
}

async function handleCheckout({ id, checkout }) {
  const token = localStorage.getItem('token')
  try {
    await axios.patch(`http://localhost:5000/api/notes/${id}/checkout`, {
      checkout
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    // ✅ อัปเดตเฉพาะโน้ตนั้น
    const note = notes.value.find(n => n.id === id)
    if (note) {
      note.checkout = checkout
    }
  } catch (e) {
    console.error('Checkout update failed:', e)
  }
}

onMounted(fetchNotes)
</script>
