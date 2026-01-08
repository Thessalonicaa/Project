// Create file: e:\ProjectFainal\backend\models\Conversation.js
const mongoose = require('mongoose')

const conversationSchema = new mongoose.Schema({
  userOne: {
    type: String,
    required: true
  },
  userOneId: {
    type: String
  },
  userOneType: {
    type: String,
    enum: ['buyer', 'seller'],
    default: 'buyer'
  },
  userTwo: {
    type: String,
    required: true
  },
  userTwoId: {
    type: String
  },
  userTwoType: {
    type: String,
    enum: ['buyer', 'seller'],
    default: 'seller'
  },
  lastMessage: {
    type: String,
    default: ''
  },
  lastMessageAt: {
    type: Date,
    default: Date.now
  },
  unreadCountOne: {
    type: Number,
    default: 0
  },
  unreadCountTwo: {
    type: Number,
    default: 0
  }
}, {
  timestamps: true
})

module.exports = mongoose.model('Conversation', conversationSchema)