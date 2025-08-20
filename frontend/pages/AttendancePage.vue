<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const attendanceLogs = ref([])

const fetchLogs = async () => {
  const token = localStorage.getItem('token')
  try {
    const res = await axios.get('http://localhost:5000/api/attendance', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    attendanceLogs.value = res.data
  } catch (e) {
    console.error('Fetch attendance logs failed:', e)
  }
}

const markAttendance = async (type) => {
  const token = localStorage.getItem('token')
  try {
    await axios.post(
      'http://localhost:5000/api/attendance',
      { type }, // type: 'in' or 'out'
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
    fetchLogs()
  } catch (e) {
    console.error('Mark attendance failed:', e)
  }
}

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString('th-TH', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}

onMounted(fetchLogs)
</script>
