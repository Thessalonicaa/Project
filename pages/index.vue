<script setup>
// Get formatPrice from plugin
const { $formatPrice } = useNuxtApp()

// Define a test price value
const price = ref(100)
</script>

<template>
  <div>
    {{ $formatPrice(price) }}
  </div>
</template>
