export default defineNuxtConfig({
  css: ['~/assets/css/main.css'],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },

  nitro: {
    compatibilityDate: '2025-08-22'
  },

  // เพิ่มการตั้งค่า pages
  pages: true,

  // เพิ่ม modules ที่จำเป็น
  modules: [
    '@nuxtjs/tailwindcss'
  ],

  // กำหนดค่า build
  build: {
    transpile: ['vue-router']
  }
})