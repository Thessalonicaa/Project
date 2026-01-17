<template>
  <div class="min-h-screen bg-gray-950 flex items-center justify-center p-4 relative overflow-hidden">
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

    <!-- Main Container -->
    <div class="w-full max-w-7xl h-[85vh] bg-gradient-to-br from-gray-900/80 via-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl border border-gray-800/50 shadow-2xl flex overflow-hidden relative z-10 min-h-0">
      
      <!-- Conversations List -->
      <div class="w-full md:w-96 bg-gray-900/60 border-r border-gray-700/50 flex flex-col">
        <!-- Header -->
        <div class="p-8 border-b border-gray-700/50 bg-gradient-to-r from-red-600/30 via-red-600/10 to-transparent backdrop-blur-sm">
          <h1 class="text-4xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent mb-2">Messages</h1>
          <p class="text-gray-400 text-sm"> Chat with buyers and sellers</p>
        </div>

        <!-- Search -->
        <div class="p-4 border-b border-gray-700/50 bg-gray-900/40">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search conversations..."
            class="w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 hover:border-red-500/50 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all duration-300 shadow-lg"
          />
        </div>

        <!-- Conversations -->
        <div class="flex-1 overflow-y-auto hide-scrollbar">
          <div
            v-for="conversation in filteredConversations"
            :key="conversation.id"
            @click="selectConversation(conversation)"
            :class="[
              'p-4 border-b border-gray-800 cursor-pointer transition-all duration-200 hover:bg-red-600/10 group relative',
              selectedConversation?.id === conversation.id ? 'bg-gradient-to-r from-red-600/30 to-transparent border-l-4 border-l-red-500' : ''
            ]"
          >
            <!-- Profile + Name + Unread Badge -->
            <div class="flex items-center gap-3 mb-3">
              <div class="relative flex-shrink-0">
                <img 
                  v-if="conversation.profileImage"
                  :src="conversation.profileImage" 
                  :alt="conversation.otherUser"
                  class="w-14 h-14 rounded-full object-cover shadow-lg group-hover:scale-110 transition-transform duration-300"
                />
                <div v-else class="w-14 h-14 rounded-full bg-gradient-to-br from-red-600 to-orange-600 flex items-center justify-center text-lg font-bold shadow-lg group-hover:scale-110 transition-transform duration-300">
                  {{ conversation.otherUser.charAt(0).toUpperCase() }}
                </div>
                <div class="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-green-500 border-2 border-gray-900 shadow-lg"></div>
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="font-bold text-white truncate group-hover:text-red-400 transition-colors">{{ conversation.otherUser }}</h3>
                <p class="text-xs text-gray-400">{{ conversation.accountType === 'seller' ? ' Seller' : ' User' }}</p>
              </div>
              <div v-if="conversation.unreadCount > 0" class="bg-gradient-to-r from-red-600 to-red-700 rounded-full px-2.5 py-1 flex items-center justify-center text-xs font-bold shadow-lg animate-pulse">
                {{ conversation.unreadCount }}
              </div>
            </div>
            <!-- Last Message Preview -->
            <p class="text-sm text-gray-400 truncate ml-17">{{ conversation.lastMessage }}</p>
            <!-- Time -->
            <p class="text-xs text-gray-500 mt-2 ml-17">⏱️ {{ formatTime(conversation.lastMessageTime) || timeUpdateTrigger }}</p>
          </div>

          <!-- Empty State -->
          <div v-if="conversations.length === 0" class="p-8 text-center mt-12">
            <i class="fas fa-inbox text-7xl text-gray-700 mb-4 opacity-50"></i>
            <p class="text-gray-400 font-semibold text-lg">No conversations yet</p>
            <p class="text-gray-500 text-sm mt-2">Start chatting with sellers!</p>
          </div>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="flex-1 flex flex-col bg-gradient-to-b from-gray-950 to-gray-900 min-h-0">
        <div v-if="selectedConversation" class="flex-1 min-h-0 h-0 flex flex-col">
          <!-- Chat Header -->
          <div class="p-6 border-b border-gray-700/50 bg-gradient-to-r from-gray-900/80 to-transparent backdrop-blur-sm flex items-center justify-between shadow-lg">
            <NuxtLink
              :to="`/profile?user=${selectedConversation.otherUser}`"
              class="flex items-center gap-4 flex-1 group cursor-pointer"
            >
              <div class="relative">
                <img 
                  v-if="selectedConversation.profileImage"
                  :src="selectedConversation.profileImage" 
                  :alt="selectedConversation.otherUser"
                  class="w-14 h-14 rounded-full object-cover shadow-lg group-hover:scale-110 transition-transform duration-300"
                />
                <div v-else class="w-14 h-14 rounded-full bg-gradient-to-br from-red-600 to-orange-600 flex items-center justify-center text-xl font-bold shadow-lg group-hover:scale-110 transition-transform duration-300">
                  {{ selectedConversation.otherUser.charAt(0).toUpperCase() }}
                </div>
                <div class="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-green-500 border-2 border-gray-900 shadow-lg"></div>
              </div>
              <div class="group-hover:text-red-400 transition-colors">
                <h2 class="text-xl font-bold text-white">{{ selectedConversation.otherUser }}</h2>
                <p class="text-sm text-gray-400">
                  {{ selectedConversation.accountType === 'seller' ? ' Seller Account' : ' User Account' }}
                </p>
              </div>
            </NuxtLink>
            <i class="fas fa-ellipsis-v text-gray-400 text-lg cursor-pointer hover:text-red-500 transition-colors"></i>
          </div>

          <!-- Messages -->
          <div class="flex-1 overflow-y-auto p-6 space-y-4 hide-scrollbar bg-gradient-to-b from-gray-950/50 to-gray-900/50">
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
                  'max-w-xs lg:max-w-md px-5 py-3 rounded-2xl shadow-lg backdrop-blur-sm',
                  message.sender === currentUsername
                    ? 'bg-gradient-to-br from-red-600 to-red-700 text-white rounded-br-none border border-red-500/50'
                    : 'bg-gray-800 border border-gray-700 text-gray-100 rounded-bl-none hover:bg-gray-750 transition-colors'
                ]"
              >
                <p class="break-words leading-relaxed">{{ message.text }}</p>
                <p class="text-xs mt-2 opacity-70 flex items-center gap-1">
                  <i class="fas fa-clock text-xs"></i>
                  {{ formatTime(message.timestamp) || timeUpdateTrigger }}
                </p>
              </div>
            </div>
            <div ref="messagesEnd"></div>
          </div>

          <!-- Message Input -->
          <div class="p-6 border-t border-gray-700/50 bg-gradient-to-t from-gray-950 to-gray-900/50 backdrop-blur-sm">
            <div class="flex items-center gap-3">
              <input
                v-model="newMessage"
                type="text"
                placeholder="Type your message..."
                class="flex-1 px-5 py-3 rounded-xl bg-gray-800 border border-gray-700 hover:border-red-500/50 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all duration-300 shadow-lg"
                @keyup.enter="sendMessage"
              />
              <button
                @click="sendMessage"
                class="px-6 py-3 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-bold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-red-600/50 flex items-center gap-2"
              >
                <i class="fas fa-paper-plane"></i>
                <span class="hidden sm:inline">Send</span>
              </button>
            </div>
          </div>
        </div>

        <!-- No Conversation Selected -->
        <div v-else class="flex-1 flex items-center justify-center overflow-y-auto min-h-0">
          <div class="text-center">
            <i class="fas fa-comments text-9xl text-gray-700 mb-6 opacity-30 drop-shadow-lg"></i>
            <p class="text-3xl font-bold text-gray-400 mb-2">Select a conversation</p>
            <p class="text-gray-500 text-lg">Choose from your conversations to start chatting </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, nextTick, onBeforeUnmount } from 'vue'
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
const timeUpdateTrigger = ref(0) // Trigger for time updates

const goBack = () => {
  router.back()
}

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
  if (!timestamp) return 'now'
  
  const date = new Date(timestamp)
  const now = new Date()
  
  // ถ้า timestamp ไม่ถูกต้อง ให้แสดง 'just now'
  if (isNaN(date.getTime())) return 'just now'
  
  const diffMs = now.getTime() - date.getTime()
  const diffSecs = Math.floor(diffMs / 1000)
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  // ถ้าเพิ่งเกิน 10 วินาที = "just now"
  if (diffSecs < 10) return 'just now'
  if (diffMins < 1) return `${diffSecs}s ago`
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  
  // แสดงวันที่เต็ม
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
  newMessage.value = '' // Clear immediately

  try {
    console.log('Sending message:', {
      sender: currentUsername.value,
      recipient: selectedConversation.value.otherUser,
      conversationId: selectedConversation.value.id,
      text: messageText
    })

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
    console.log('Send message response status:', response.status)
    console.log('Send message response data:', data)

    // Check if response is OK (regardless of data.success)
    if (response.ok) {
      // Add message to UI
      const message = {
        sender: currentUsername.value,
        text: messageText,
        timestamp: new Date().toISOString(),
        _id: data.messageId || data.id || Date.now().toString()
      }
      
      if (!selectedConversation.value.messages) {
        selectedConversation.value.messages = []
      }
      selectedConversation.value.messages.push(message)
      
      // Update conversation last message
      const conv = conversations.value.find(c => c.id === selectedConversation.value.id)
      if (conv) {
        conv.lastMessage = messageText
        conv.lastMessageTime = message.timestamp
      }

      await nextTick()
      scrollToBottom()
      console.log('Message sent successfully')
    } else {
      // Response NOT OK - restore message
      console.error('Failed to send message - HTTP error:', response.status, data)
      newMessage.value = messageText
    }
  } catch (error) {
    console.error('Error sending message - Network error:', error)
    newMessage.value = messageText // Restore on error
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

// Update time display every 30 seconds
const updateTimeDisplay = setInterval(() => {
  timeUpdateTrigger.value += 1
}, 30000)

onMounted(async () => {
  currentUsername.value = localStorage.getItem('username') || 'User'
  currentUserId.value = localStorage.getItem('userId') || ''
  
  // Fetch conversations
  await fetchConversations()
  
  // Check if coming from cart checkout
  let sellerParam = null
  let autoMessage = null
  
  // Priority 1: Check sessionStorage from cart
  if (sessionStorage.getItem('isFromCart') === 'true') {
    sellerParam = sessionStorage.getItem('contactSeller')
    autoMessage = sessionStorage.getItem('contactSellerMessage')
    console.log('From Cart - Seller:', sellerParam, 'Message:', autoMessage)
    
    // Clear sessionStorage
    sessionStorage.removeItem('isFromCart')
    sessionStorage.removeItem('contactSeller')
    sessionStorage.removeItem('contactSellerMessage')
    sessionStorage.removeItem('contactCarData')
  }
  // Priority 2: Check URL parameter
  else if (route.query.seller) {
    sellerParam = route.query.seller
  }
  
  // Priority 3: Check sessionStorage from car detail page
  if (!sellerParam && sessionStorage.getItem('contactSeller')) {
    sellerParam = sessionStorage.getItem('contactSeller')
    const carDataJson = sessionStorage.getItem('contactCarData')
    if (carDataJson) {
      try {
        const carData = JSON.parse(carDataJson)
        if (carData.brand && carData.model) {
          autoMessage = `สวัสดีครับ/ค่ะ ต้องการสอบถามข้อมูลเกี่ยวกับสินค้านี้\n\n📍 ${carData.brand} ${carData.model}\n📅 ปี ${carData.year}\n💰 ฿${new Intl.NumberFormat('th-TH').format(carData.price)}`
        }
      } catch (error) {
        console.error('Error parsing car data:', error)
      }
    }
    // Clear sessionStorage after reading
    sessionStorage.removeItem('contactSeller')
    sessionStorage.removeItem('contactCarData')
    sessionStorage.removeItem('contactSellerMessage')
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
      
      // Send auto message if exists
      if (autoMessage) {
        newMessage.value = autoMessage
        await nextTick()
        setTimeout(() => {
          sendMessage()
        }, 300)
      }
    }
  }
})


// Cleanup polling interval
onBeforeUnmount(() => {
  clearInterval(pollMessages)
  clearInterval(updateTimeDisplay)
})
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

/* Hide scrollbar but allow scrolling */
.hide-scrollbar {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE 10+ */
}
.hide-scrollbar::-webkit-scrollbar {
  display: none; /* Chrome/Safari/Webkit */
}

/* Beams Background */
.beams-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}
</style>
