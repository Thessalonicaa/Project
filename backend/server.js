const express = require('express')
const http = require('http')
const cors = require('cors')
const mongoose = require('mongoose')
require('dotenv').config()
const { initializeSocket } = require('./socket')

// Create Express app
const app = express()

// Middleware
app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// MongoDB Connection (FIXED – removed deprecated options)
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/zavora')
  .then(() => console.log('✅ MongoDB connected'))
  .catch(err => console.log('❌ MongoDB error:', err))

// Routes
const messagesRouter = require('./routes/messages')
const sellersRouter = require('./routes/sellers')

app.use('/api', messagesRouter)
app.use('/api', sellersRouter)

// Create HTTP server
const server = http.createServer(app)

// Initialize Socket.IO
initializeSocket(server)

// Server listen
const PORT = process.env.PORT || 5000
server.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`)
})
