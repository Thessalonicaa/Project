
<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-950  flex items-center justify-center p-4">
    <!-- Main Container -->
    <div class="w-full max-w-7xl h-[85vh] bg-gray-900/80 backdrop-blur-xl rounded-3xl border border-gray-800/50 shadow-2xl flex overflow-hidden">
      
      <!-- Conversations List -->
      <div class="w-full md:w-80 bg-gray-900/50 border-r border-gray-700/50 flex flex-col">
        <!-- Header -->
        <div class="p-6 border-b border-gray-700/50 bg-gradient-to-r from-red-600/20 to-transparent">
          <h1 class="text-3xl font-extrabold text-red-500 mb-2">Messages</h1>
          <p class="text-gray-400 text-sm">Chat with buyers and sellers</p>
        </div>

        <!-- Search -->
        <div class="p-4 border-b border-gray-700/50">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search conversations..."
            class="w-full px-4 py-2 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all"
          />
        </div>

        <!-- Conversations -->
        <div class="flex-1 overflow-y-auto">
          <div
            v-for="conversation in filteredConversations"
            :key="conversation.id"
            @click="selectConversation(conversation)"
            :class="[
              'p-4 border-b border-gray-800 cursor-pointer transition-all duration-200 hover:bg-gray-800/50 group',
              selectedConversation?.id === conversation.id ? 'bg-red-600/20 border-l-4 border-l-red-500' : ''
            ]"
          >
            <!-- Profile + Name + Unread Badge -->
            <div class="flex items-center gap-3 mb-2">
              <div class="w-12 h-12 rounded-full bg-gradient-to-r from-red-600 to-red-500 flex items-center justify-center flex-shrink-0 text-lg font-bold shadow-lg group-hover:scale-110 transition-transform">
                {{ conversation.otherUser.charAt(0).toUpperCase() }}
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-white truncate">{{ conversation.otherUser }}</h3>
                <p class="text-xs text-gray-400">{{ conversation.accountType === 'seller' ? 'Seller' : 'User' }}</p>
              </div>
              <div v-if="conversation.unreadCount > 0" class="bg-red-600 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold shadow-lg animate-pulse">
                {{ conversation.unreadCount }}
              </div>
            </div>
            <!-- Last Message Preview -->
            <p class="text-sm text-gray-400 truncate">{{ conversation.lastMessage }}</p>
            <!-- Time -->
            <p class="text-xs text-gray-500 mt-1">{{ formatTime(conversation.lastMessageTime) }}</p>
          </div>

          <!-- Empty State -->
          <div v-if="conversations.length === 0" class="p-6 text-center mt-8">
            <i class="fas fa-inbox text-6xl text-gray-600 mb-4"></i>
            <p class="text-gray-400 font-medium">No conversations yet</p>
            <p class="text-gray-500 text-sm mt-1">Start chatting with sellers!</p>
          </div>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="flex-1 flex flex-col bg-gradient-to-b from-gray-950 to-gray-900">
        <div v-if="selectedConversation">
          <!-- Chat Header -->
          <div class="p-6 border-b border-gray-700/50 bg-gradient-to-r from-gray-900/50 to-transparent backdrop-blur-sm flex items-center justify-between">
            <NuxtLink
              :to="`/profile?user=${selectedConversation.otherUser}`"
              class="flex items-center gap-4 flex-1 group cursor-pointer"
            >
              <img 
                v-if="selectedConversation.profileImage"
                :src="selectedConversation.profileImage" 
                :alt="selectedConversation.otherUser"
                class="w-12 h-12 rounded-full object-cover shadow-lg group-hover:scale-110 transition-transform"
              />
              <div v-else class="w-12 h-12 rounded-full bg-gradient-to-r from-red-600 to-red-500 flex items-center justify-center text-lg font-bold shadow-lg group-hover:scale-110 transition-transform">
                {{ selectedConversation.otherUser.charAt(0).toUpperCase() }}
              </div>
              <div class="group-hover:text-red-400 transition-colors">
                <h2 class="text-xl font-bold text-white">{{ selectedConversation.otherUser }}</h2>
                <p class="text-sm text-gray-400">
                  {{ selectedConversation.accountType === 'seller' ? 'Seller Account' : 'User Account' }}
                </p>
              </div>
            </NuxtLink>
          </div>

          <!-- Messages -->
          <div class="flex-1 overflow-y-auto p-6 space-y-4">
            <div
              v-for="(message, index) in selectedConversation.messages"
              :key="index"
              :class="[
                'flex animate-message-slide',
                message.sender === currentUsername ? 'justify-end' : 'justify-start'
              ]"
            >
              <div
                :class="[
                  'max-w-xs lg:max-w-md px-5 py-3 rounded-2xl shadow-lg',
                  message.sender === currentUsername
                    ? 'bg-gradient-to-r from-red-600 to-red-700 text-white rounded-br-none'
                    : 'bg-gray-800 border border-gray-700 text-gray-100 rounded-bl-none'
                ]"
              >
                <p class="break-words">{{ message.text }}</p>
                <p class="text-xs mt-2 opacity-70">{{ formatTime(message.timestamp) }}</p>
              </div>
            </div>
            <div ref="messagesEnd"></div>
          </div>

          <!-- Message Input -->
          <div class="p-6 border-t border-gray-700/50 bg-gradient-to-t from-gray-950 to-transparent backdrop-blur-sm">
            <div class="flex items-center gap-3">
              <input
                v-model="newMessage"
                type="text"
                placeholder="Type your message..."
                class="flex-1 px-5 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all"
                @keyup.enter="sendMessage"
              />
              <button
                @click="sendMessage"
                class="px-6 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg"
              >
                <i class="fas fa-paper-plane mr-2"></i>Send
              </button>
            </div>
          </div>
        </div>

        <!-- No Conversation Selected -->
        <div v-else class="flex-1 flex items-center justify-center">
          <div class="text-center">
            <i class="fas fa-comments text-8xl text-gray-700 mb-4 opacity-50"></i>
            <p class="text-2xl font-bold text-gray-400">Select a conversation</p>
            <p class="text-gray-500 mt-2">Choose from your conversations to start chatting</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const currentUsername = ref('')
const currentUserId = ref('')
const selectedConversation = ref(null)
const newMessage = ref('')
const searchQuery = ref('')
const messagesEnd = ref(null)
const loading = ref(false)

const conversations = ref([])
const messagesByConversation = ref({})
const allSellers = ref([])

const filteredConversations = computed(() => {
  if (!searchQuery.value) return conversations.value
  return conversations.value.filter(conv =>
    conv.otherUser.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const filteredSellers = computed(() => {
  if (!searchQuery.value) return allSellers.value
  return allSellers.value.filter(seller =>
    seller.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    seller.business_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  
  return date.toLocaleDateString('th-TH', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Fetch all conversations
const fetchConversations = async () => {
  try {
    loading.value = true
    const response = await fetch(`http://localhost:5000/api/conversations/${currentUsername.value}`)
    const data = await response.json()

    if (data.success) {
      conversations.value = data.conversations.map(conv => ({
        id: conv._id,
        otherUser: conv.otherUser,
        otherUserId: conv.otherUserId,
        accountType: conv.accountType || 'buyer',
        lastMessage: conv.lastMessage || 'No messages yet',
        lastMessageTime: conv.lastMessageTime || new Date().toISOString(),
        unreadCount: conv.unreadCount || 0,
        messages: messagesByConversation[conv._id] || [],
        profileImage: conv.profileImage || null
      }))
    }
  } catch (error) {
    console.error('Error fetching conversations:', error)
  } finally {
    loading.value = false
  }
}

// Fetch all sellers
const fetchSellers = async () => {
  try {
    const response = await fetch(`http://localhost:5000/api/sellers`)
    const data = await response.json()

    if (data.success) {
      allSellers.value = data.sellers || []
    }
  } catch (error) {
    console.error('Error fetching sellers:', error)
  }
}

// Fetch messages for a specific conversation
const fetchMessages = async (conversationId) => {
  try {
    const response = await fetch(`http://localhost:5000/api/messages/${conversationId}`)
    const data = await response.json()

    if (data.success) {
      messagesByConversation[conversationId] = data.messages.map(msg => ({
        sender: msg.sender,
        text: msg.text,
        timestamp: msg.timestamp,
        _id: msg._id
      }))
      
      // Update selected conversation with messages
      if (selectedConversation.value && selectedConversation.value.id === conversationId) {
        selectedConversation.value.messages = messagesByConversation[conversationId]
      }
    }
  } catch (error) {
    console.error('Error fetching messages:', error)
  }
}

const selectConversation = async (conversation) => {
  selectedConversation.value = { ...conversation }
  
  // Fetch messages for this conversation
  await fetchMessages(conversation.id)
  
  // Mark as read
  try {
    await fetch(`http://localhost:5000/api/conversations/${conversation.id}/read`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    // Update unread count
    conversation.unreadCount = 0
  } catch (error) {
    console.error('Error marking conversation as read:', error)
  }
  
  await nextTick()
  scrollToBottom()
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !selectedConversation.value) return

  const messageText = newMessage.value
  newMessage.value = ''

  try {
    const response = await fetch(`http://localhost:5000/api/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        sender: currentUsername.value,
        senderId: currentUserId.value,
        recipientUsername: selectedConversation.value.otherUser,
        recipientId: selectedConversation.value.otherUserId,
        text: messageText,
        conversationId: selectedConversation.value.id
      })
    })

    const data = await response.json()

    if (data.success) {
      // Add message to UI immediately
      const message = {
        sender: currentUsername.value,
        text: messageText,
        timestamp: new Date().toISOString(),
        _id: data.messageId
      }
      
      if (!selectedConversation.value.messages) {
        selectedConversation.value.messages = []
      }
      selectedConversation.value.messages.push(message)
      
      // Update conversation
      const conv = conversations.value.find(c => c.id === selectedConversation.value.id)
      if (conv) {
        conv.lastMessage = messageText
        conv.lastMessageTime = message.timestamp
      }

      await nextTick()
      scrollToBottom()
    } else {
      alert('Failed to send message: ' + data.message)
      newMessage.value = messageText
    }
  } catch (error) {
    console.error('Error sending message:', error)
    alert('Error sending message')
    newMessage.value = messageText
  }
}

// Create or find conversation with seller
const createConversationWithSeller = async (sellerUsername) => {
  try {
    const response = await fetch(`http://localhost:5000/api/conversations/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: currentUsername.value,
        otherUsername: sellerUsername,
        accountType: 'seller'
      })
    })

    const data = await response.json()

    if (data.success) {
      // Fetch updated conversations
      await fetchConversations()
      
      // Find and select the new conversation
      const newConv = conversations.value.find(c => c.otherUser === sellerUsername)
      if (newConv) {
        await selectConversation(newConv)
      }
    }
  } catch (error) {
    console.error('Error creating conversation:', error)
  }
}

const scrollToBottom = () => {
  messagesEnd.value?.scrollIntoView({ behavior: 'smooth' })
}

// Poll for new messages every 3 seconds
const pollMessages = setInterval(() => {
  if (selectedConversation.value) {
    fetchMessages(selectedConversation.value.id)
  }
  fetchConversations()
}, 3000)

onMounted(async () => {
  currentUsername.value = localStorage.getItem('username') || 'User'
  currentUserId.value = localStorage.getItem('userId') || ''
  
  // Fetch conversations
  await fetchConversations()
  
  // Check if coming from car detail page with seller parameter
  let sellerParam = route.query.seller
  let carData = null
  
  // Check sessionStorage for car data and seller
  if (sessionStorage.getItem('contactSeller')) {
    sellerParam = sessionStorage.getItem('contactSeller')
    const carDataJson = sessionStorage.getItem('contactCarData')
    if (carDataJson) {
      try {
        carData = JSON.parse(carDataJson)
      } catch (error) {
        console.error('Error parsing car data:', error)
      }
    }
    // Clear sessionStorage after reading
    sessionStorage.removeItem('contactSeller')
    sessionStorage.removeItem('contactCarData')
  }
  
  if (sellerParam) {
    // Find or create conversation with this seller
    let conversation = conversations.value.find(c => c.otherUser === sellerParam)
    if (!conversation) {
      // Create new conversation
      await createConversationWithSeller(sellerParam)
      conversation = conversations.value.find(c => c.otherUser === sellerParam)
    }
    
    if (conversation) {
      await selectConversation(conversation)
      
      // If car data is provided, send automatic message
      if (carData) {
        // Build automatic message
        const autoMessage = `สวัสดีครับ/ค่ะ ต้องการสอบถามข้อมูลเกี่ยวกับสินค้านี้\n\n📍 ${carData.brand} ${carData.model}\n📅 ปี ${carData.year}\n💰 ฿${new Intl.NumberFormat('th-TH').format(carData.price)}`
        
        // Set the message in the input
        newMessage.value = autoMessage
        
        // Auto-send after a short delay
        await nextTick()
        setTimeout(() => {
          sendMessage()
        }, 500)
      }
    }
  }
})


// Cleanup polling interval
onBeforeUnmount(() => {
  clearInterval(pollMessages)
})

import { onBeforeUnmount } from 'vue'
</script>

<style scoped>
@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-message-slide {
  animation: messageSlide 0.3s ease-out;
}
</style>
