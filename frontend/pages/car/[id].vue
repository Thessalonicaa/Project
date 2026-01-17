<template>
  <div class="min-h-screen bg-gray-950 text-white p-6 relative overflow-hidden">
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

    <div class="max-w-7xl mx-auto">
      <!-- Back Button with Animation -->
      <div class="mb-8 flex items-center gap-4">
        <button 
          @click="goBack"
          class="group relative inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br border-red-500/50 hover:border-red-400 hover:from-red-600/40 hover:to-red-700/40 transition-all duration-300 shadow-lg hover:shadow-red-500/30"
          title="Go back"
        >
          <i class="fas fa-arrow-left text-red-500 group-hover:text-red-400 group-hover:-translate-x-1 transition-all duration-300"></i>
        </button>
        
        <NuxtLink 
          to="/CarList" 
          class="inline-flex items-center gap-2 text-red-500 hover:text-red-400 font-semibold group transition-all duration-300"
        >
          <span class="relative overflow-hidden">
            
            <span class="absolute inset-0 flex items-center translate-x-full group-hover:translate-x-0 transition-transform duration-300 text-red-400">
              <i class="fas fa-arrow-right ml-2"></i> Browse More
            </span>
          </span>
        </NuxtLink>
      </div>

      <div v-if="loading" class="text-center py-16">
        <div class="inline-flex flex-col items-center">
          <div class="w-12 h-12 border-4 border-red-500 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p class="text-gray-400 text-lg">Loading car details...</p>
        </div>
      </div>

      <div v-else-if="car" class="space-y-8">
        <!-- Sold Out Banner -->
        <div v-if="car.sold_out" class="bg-gradient-to-r from-red-600/30 to-red-800/30 border border-red-500/50 rounded-2xl p-6 text-center backdrop-blur-sm animate-pulse">
          <p class="text-red-400 font-bold text-xl">
            <i class="fas fa-times-circle mr-3"></i>This Car is SOLD OUT
          </p>
        </div>

        <!-- Main Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <!-- Left Section - Images (3 cols) -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Main Image with Badge -->
            <div class="relative bg-gradient-to-br from-gray-900 to-gray-950 backdrop-blur-sm rounded-3xl overflow-hidden border border-gray-800/50 hover:border-red-500/50 transition-all duration-300 group shadow-2xl">
              <img
                :src="car.images && car.images.length > 0 ? car.images[selectedImageIndex] : 'https://via.placeholder.com/800x500?text=No+Image'"
                :alt="car.model"
                class="w-full h-96 object-cover group-hover:scale-110 transition-transform duration-700"
              />
              
              <!-- Image Counter Badge -->
              <div class="absolute top-6 right-6 bg-black/60 backdrop-blur-md px-4 py-2 rounded-full text-white text-sm font-semibold border border-white/20 hover:bg-black/80 transition-all">
                <i class="fas fa-images mr-2"></i>{{ selectedImageIndex + 1 }} / {{ car.images?.length || 1 }}
              </div>

              <!-- Sold Badge -->
              <div v-if="car.sold_out" class="absolute top-6 left-6 bg-red-600/90 backdrop-blur-md px-4 py-2 rounded-full text-white text-sm font-bold border border-red-400/20">
                <i class="fas fa-check-circle mr-2"></i>SOLD
              </div>

              <!-- Arrow Navigation Buttons -->
              <button
                v-if="car.images && car.images.length > 1"
                @click="previousImage"
                class="absolute left-4 top-1/2 transform -translate-y-1/2 bg-black/50 hover:bg-black/80 text-white rounded-full w-12 h-12 flex items-center justify-center transition-all duration-300 opacity-0 group-hover:opacity-100 hover:scale-110 z-10"
              >
                <i class="fas fa-chevron-left text-xl"></i>
              </button>

              <button
                v-if="car.images && car.images.length > 1"
                @click="nextImage"
                class="absolute right-4 top-1/2 transform -translate-y-1/2 bg-black/50 hover:bg-black/80 text-white rounded-full w-12 h-12 flex items-center justify-center transition-all duration-300 opacity-0 group-hover:opacity-100 hover:scale-110 z-10"
              >
                <i class="fas fa-chevron-right text-xl"></i>
              </button>

              <!-- Image Indicators Dots -->
              <div v-if="car.images && car.images.length > 1" class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2 z-10">
                <button
                  v-for="(image, index) in car.images"
                  :key="index"
                  @click="selectedImageIndex = index"
                  :class="[
                    'w-2 h-2 rounded-full transition-all duration-300',
                    selectedImageIndex === index ? 'bg-red-500 w-8' : 'bg-white/50 hover:bg-white/80'
                  ]"
                  :title="`Image ${index + 1}`"
                />
              </div>
            </div>

            <!-- Car Header with Gradient -->
            <div class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h1 class="text-5xl font-extrabold bg-gradient-to-r from-red-500 via-red-400 to-orange-400 bg-clip-text text-transparent mb-2">
                    {{ car.brand }}
                  </h1>
                  <p class="text-3xl font-bold text-gray-200">{{ car.model }}</p>
                </div>
              </div>
              
              <!-- Key Details Grid -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-700">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-red-600/20 rounded-lg flex items-center justify-center">
                    <i class="fas fa-calendar text-red-500"></i>
                  </div>
                  <div>
                    <p class="text-gray-400 text-xs uppercase">Year</p>
                    <p class="text-white font-bold">{{ car.year }}</p>
                  </div>
                </div>
                
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-blue-600/20 rounded-lg flex items-center justify-center">
                    <i class="fas fa-id-card text-blue-500"></i>
                  </div>
                  <div>
                    <p class="text-gray-400 text-xs uppercase">License</p>
                    <p class="text-white font-mono font-bold">{{ car.license_plate }}</p>
                  </div>
                </div>

                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-green-600/20 rounded-lg flex items-center justify-center">
                    <i class="fas fa-gas-pump text-green-500"></i>
                  </div>
                  <div>
                    <p class="text-gray-400 text-xs uppercase">Fuel</p>
                    <p class="text-white font-bold">{{ car.fuel_type || 'N/A' }}</p>
                  </div>
                </div>

                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-purple-600/20 rounded-lg flex items-center justify-center">
                    <i class="fas fa-cog text-purple-500"></i>
                  </div>
                  <div>
                    <p class="text-gray-400 text-xs uppercase">Trans</p>
                    <p class="text-white font-bold text-sm">{{ car.transmission || 'N/A' }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Car Specs Card -->
            <div class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
              <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
                <div class="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                  <i class="fas fa-list text-white"></i>
                </div>
                Specifications
              </h2>
              
              <div class="grid grid-cols-2 gap-4 space-y-2">
            
                <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Car Type</p>
                  <p class="text-white font-bold">{{ car.car_type || 'N/A' }}</p>
                </div>
                <!-- Row 3 -->
                <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Engine Size</p>
                  <p class="text-white font-bold">{{ car.engine_size || 'N/A' }}</p>
                </div>
                <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Gas System</p>
                  <p class="text-white font-bold">{{ car.gas_system || 'None' }}</p>
                </div>

                <!-- Row 4 -->
                <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Mileage</p>
                  <p class="text-white font-bold">{{ car.mileage ? formatMileage(car.mileage) + ' km' : 'N/A' }}</p>
                </div>
                <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Color</p>
                  <p class="text-white font-bold">{{ car.color || 'N/A' }}</p>
                </div>

                <!-- Row 5 - Dynamic Fields -->
                <div v-if="car.car_type === 'MPV' && car.mpv_size" class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">MPV Size</p>
                  <p class="text-white font-bold">{{ car.mpv_size }}</p>
                </div>
                <div v-if="car.car_type === 'Convertible' && car.convertible_top" class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Top Type</p>
                  <p class="text-white font-bold">{{ car.convertible_top }}</p>
                </div>
                <div v-if="car.car_type === 'Convertible' && car.convertible_seats" class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Seats</p>
                  <p class="text-white font-bold">{{ car.convertible_seats }}</p>
                </div>
                <div v-if="car.car_type === 'Van' && car.van_type" class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Van Type</p>
                  <p class="text-white font-bold">{{ car.van_type }}</p>
                </div>
                <div v-if="car.car_type === 'SUV' && car.suv_seats" class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Seat Capacity</p>
                  <p class="text-white font-bold">{{ car.suv_seats }}</p>
                </div>
                <div v-if="car.car_type === 'Pickup' && car.pickup_cab" class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Cab Type</p>
                  <p class="text-white font-bold">{{ car.pickup_cab }}</p>
                </div>
                <div v-if="car.car_type === 'Pickup' && car.pickup_body_type" class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Body Type</p>
                  <p class="text-white font-bold">{{ car.pickup_body_type }}</p>
                </div>

                <!-- Row 6 -->
                <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                  <p class="text-gray-400 text-sm mb-1">Condition</p>
                  <p class="text-white font-bold">{{ car.sold_out ? 'Sold' : 'Available' }}</p>
                </div>
              </div>
            </div>

            <!-- Description -->
            <div class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
              <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
                <div class="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                  <i class="fas fa-align-left text-white"></i>
                </div>
                Description
              </h2>
              <p class="text-gray-300 leading-relaxed text-lg">{{ car.description || 'No description provided' }}</p>
            </div>

            <!-- Gallery -->
            <div v-if="car.images && car.images.length > 1" class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
              <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
                <div class="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                  <i class="fas fa-images text-white"></i>
                </div>
                Gallery
              </h2>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div
                  v-for="(image, index) in car.images.slice(1)"
                  :key="index"
                  @click="selectedImageIndex = index + 1"
                  class="relative group cursor-pointer"
                >
                  <img
                    :src="image"
                    :alt="`Car image ${index + 2}`"
                    class="w-full h-32 object-cover rounded-xl hover:scale-110 transition-transform duration-300"
                    :class="{
                      'ring-4 ring-red-500 shadow-lg shadow-red-500/50': selectedImageIndex === index + 1,
                      'ring-2 ring-gray-700': selectedImageIndex !== index + 1
                    }"
                  />
                  <div v-if="selectedImageIndex === index + 1" class="absolute inset-0 rounded-xl bg-gradient-to-t from-red-600/50 to-transparent flex items-center justify-center">
                    <i class="fas fa-check-circle text-white text-3xl drop-shadow-lg"></i>
                  </div>
                  <div class="absolute inset-0 rounded-xl bg-black/0 group-hover:bg-black/20 transition-all duration-300"></div>
                </div>
              </div>
            </div>

            <!-- Video Section (if available) -->
            <div v-if="car.video_url" class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl animate-fade-in">
              <h2 class="text-2xl font-bold mb-6 flex items-center gap-3">
                <div class="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                  <i class="fas fa-video text-white"></i>
                </div>
                Video Walkthrough
              </h2>
              <div class="relative w-full aspect-video rounded-2xl overflow-hidden border border-gray-700 group hover:border-red-500/50 transition-all">
                <video
                  :src="car.video_url"
                  class="w-full h-full object-cover"
                  controls
                  poster="https://via.placeholder.com/800x450?text=Car+Video"
                ></video>
                <div class="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                  <i class="fas fa-play text-white text-6xl opacity-70"></i>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Section - Sidebar (1 col) -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Price Card - Premium Style -->
            <div class="bg-gradient-to-br from-red-600 via-red-700 to-red-900 rounded-3xl p-8 shadow-2xl shadow-red-600/50 border border-red-500/50 hover:border-red-400 transition-all transform hover:scale-105 duration-300">
              <p class="text-red-200 text-sm uppercase font-semibold mb-2 tracking-widest">Price</p>
              <p class="text-6xl font-extrabold text-white mb-4 drop-shadow-lg">฿{{ formatPrice(car.price) }}</p>
              <div class="bg-red-500/20 rounded-lg p-3 border border-red-400/30">
                <p class="text-red-100 text-sm font-semibold">Ready to negotiate</p>
              </div>
            </div>

            <!-- Seller Info Card with SellerProfileHover -->
            <SellerProfileHover
              :username="car.seller.username"
              :business-name="car.seller.business_name"
              :phone-number="car.seller.phonenumber"
              :email="car.seller.email"
              :profile-image="sellerProfileImage"
              :last-activity="lastActivity"
              :cars-listed="carsListed"
            >
              <template #default>
                <div class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl border border-gray-800/50 hover:border-red-500/50 transition-all duration-300 overflow-hidden group shadow-xl">
                  <!-- Top gradient bar -->
                  <div class="h-1 bg-gradient-to-r from-red-600 via-red-500 to-orange-500"></div>

                  <div class="p-6">
                    <h2 class="text-2xl font-bold mb-6 text-white flex items-center gap-3">
                      <div class="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                        <i class="fas fa-store text-white"></i>
                      </div>
                      Seller Info
                    </h2>

                    <!-- Seller Profile Link -->
                    <NuxtLink
                      :to="`/profile?user=${car.seller.username}`"
                      class="flex items-center gap-4 p-4 rounded-xl hover:bg-gray-800/50 transition-all group/profile mb-4"
                    >
                      <!-- Avatar -->
                      <div class="flex-shrink-0 relative">
                        <img v-if="sellerProfileImage" :src="sellerProfileImage" :alt="car.seller.username" class="w-16 h-16 rounded-full border-3 border-red-500 group-hover/profile:scale-110 transition-transform shadow-lg object-cover" />
                        <div v-else class="w-16 h-16 rounded-full bg-gradient-to-br from-red-600 to-red-700 flex items-center justify-center border-3 border-red-500 group-hover/profile:scale-110 transition-transform shadow-lg">
                          <i class="fas fa-store text-white text-2xl"></i>
                        </div>
                        <div :class="[
                          'absolute -bottom-1 -right-1 rounded-full w-5 h-5 flex items-center justify-center text-xs text-white border-2 border-gray-900',
                          isOnline ? 'bg-green-500' : 'bg-gray-500'
                        ]">
                          <i :class="['fas', isOnline ? 'fa-check' : 'fa-circle text-xs']"></i>
                        </div>
                      </div>

                      <!-- Info -->
                      <div class="flex-1 min-w-0">
                        <p class="text-gray-400 text-xs uppercase font-semibold">Shop</p>
                        <h3 class="text-white font-bold text-lg truncate group-hover/profile:text-red-400 transition-colors">{{ car.seller.business_name }}</h3>
                        <p class="text-red-500 text-sm font-semibold">@{{ car.seller.username }}</p>
                      </div>

                      <i class="fas fa-arrow-right text-red-500 group-hover/profile:translate-x-1 transition-transform"></i>
                    </NuxtLink>

                    <!-- Seller Details -->
                    <div class="space-y-3 pt-4 border-t border-gray-700">
                      <div class="flex items-start gap-3 bg-gray-800/30 p-3 rounded-lg">
                        <i class="fas fa-envelope text-red-500 w-5 mt-1"></i>
                        <div class="min-w-0 flex-1">
                          <p class="text-gray-400 text-xs">Email</p>
                          <p class="text-white text-sm font-medium break-all">{{ car.seller.email }}</p>
                        </div>
                      </div>

                      <div class="flex items-start gap-3 bg-gray-800/30 p-3 rounded-lg">
                        <i class="fas fa-phone text-green-500 w-5 mt-1"></i>
                        <div class="min-w-0 flex-1">
                          <p class="text-gray-400 text-xs">Phone</p>
                          <p class="text-white text-sm font-medium">{{ car.seller.phonenumber }}</p>
                        </div>
                      </div>

                      <div class="flex items-start gap-3 bg-gray-800/30 p-3 rounded-lg">
                        <i class="fas fa-map-marker-alt text-blue-500 w-5 mt-1"></i>
                        <div class="min-w-0 flex-1">
                          <p class="text-gray-400 text-xs">Address</p>
                          <p class="text-white text-sm font-medium break-words">{{ car.seller.contact_info || 'Not specified' }}</p>
                        </div>
                      </div>

                      <div class="flex items-center gap-3 bg-red-600/10 border border-red-500/30 p-3 rounded-lg">
                        <i class="fas fa-car text-red-500 w-5"></i>
                        <div class="min-w-0 flex-1">
                          <p class="text-gray-400 text-xs">Cars Listed</p>
                          <p class="text-white text-sm font-bold">{{ carsListed }} cars available</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
            </SellerProfileHover>

            <!-- Action Buttons -->
            <div class="space-y-3 sticky top-6">
              <!-- Contact Seller Button -->
              <button 
                @click="contactSeller"
                :disabled="car.sold_out"
                class="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold py-4 px-6 rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-red-500/50 flex items-center justify-center gap-2 text-lg disabled:opacity-50"
              >
                <i class="fas fa-comments"></i>Contact Seller
              </button>

              <!-- Add to Cart Button -->
              <button 
                id="cartBtn"
                @click="addToCart"
                :disabled="car.sold_out"
                class="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold py-4 px-6 rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-blue-500/50 flex items-center justify-center gap-2 text-lg disabled:opacity-50"
              >
                <i class="fas fa-shopping-cart"></i>{{ car.sold_out ? 'Sold Out' : 'Add to Cart' }}
              </button>
            </div>

            <!-- Stats Card -->
            <div class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-6 border border-gray-800/50 shadow-xl">
              <h3 class="font-bold text-white mb-4">Quick Info</h3>
              <div class="space-y-3 text-sm">
                <div class="flex justify-between items-center py-2 border-b border-gray-700">
                  <span class="text-gray-400">Status</span>
                  <span class="font-bold" :class="car.sold_out ? 'text-red-500' : 'text-green-500'">
                    {{ car.sold_out ? 'Sold Out' : 'Available' }}
                  </span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-gray-700">
                  <span class="text-gray-400">Listed</span>
                  <span class="text-white font-bold">{{ formatDate(car.created_at) }}</span>
                </div>
                <div class="flex justify-between items-center py-2">
                  <span class="text-gray-400">Views</span>
                  <span class="text-white font-bold">
                    <i class="fas fa-eye text-red-500 mr-1"></i>{{ car.views || 0 }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-16">
        <i class="fas fa-exclamation-circle text-6xl text-gray-600 mb-4"></i>
        <p class="text-gray-400 text-xl">Car not found</p>
      </div>
    </div>
  </div>

  <!-- Success Modal -->
  <SuccessModal
    :show="showSuccessModal"
    title="เพิ่มรถเข้าตะกร้าสำเร็จ"
    message="รถคันนี้ถูกเพิ่มเข้าตะกร้าเรียบร้อยแล้ว"
    icon="✅"
    :duration="5"
    @close="handleSuccessClose"
  />

  <!-- Duplicate Warning Modal -->
  <SuccessModal
    :show="showDuplicateWarning"
    title="⚠️ รถคันนี้อยู่ในตะกร้าแล้ว"
    message="กรุณาตรวจสอบตะกร้าของคุณก่อน"
    icon="⚠️"
    :duration="4"
    @close="showDuplicateWarning = false"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SellerProfileHover from '~/components/SellerProfileHover.vue'

const route = useRoute()
const router = useRouter()
const car = ref(null)
const loading = ref(true)
const showSuccessModal = ref(false)
const showDuplicateWarning = ref(false)
const sellerProfileImage = ref('')
const lastActivity = ref('')
const carsListed = ref(0)
const selectedImageIndex = ref(0)
const isOnline = ref(true)
let autoSlideInterval = null

const nextImage = () => {
  if (car.value && car.value.images && car.value.images.length > 0) {
    selectedImageIndex.value = (selectedImageIndex.value + 1) % car.value.images.length
    resetAutoSlide()
  }
}

const previousImage = () => {
  if (car.value && car.value.images && car.value.images.length > 0) {
    selectedImageIndex.value = (selectedImageIndex.value - 1 + car.value.images.length) % car.value.images.length
    resetAutoSlide()
  }
}

const startAutoSlide = () => {
  if (car.value && car.value.images && car.value.images.length > 1) {
    autoSlideInterval = setInterval(() => {
      selectedImageIndex.value = (selectedImageIndex.value + 1) % car.value.images.length
    }, 5000) // Change image every 5 seconds
  }
}

const resetAutoSlide = () => {
  if (autoSlideInterval) {
    clearInterval(autoSlideInterval)
  }
  startAutoSlide()
}

const incrementViewCount = async () => {
  try {
    const response = await fetch(`http://localhost:5000/api/cars/${route.params.id}/view`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    const data = await response.json()
    
    if (data.success && car.value) {
      car.value.views = data.views || (car.value.views || 0) + 1
      console.log('Views updated to:', car.value.views)
    }
  } catch (error) {
    console.error('Error incrementing views:', error)
  }
}

const goBack = () => {
  router.back()
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('th-TH').format(price)
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('th-TH', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatMileage = (mileage) => {
  if (!mileage) return '0'
  return mileage.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const handleSuccessClose = () => {
  showSuccessModal.value = false
}

const contactSeller = () => {
  if (!car.value?.seller) {
    alert('Seller information not available')
    return
  }
  
  // Store car data in sessionStorage instead of URL params
  const carData = {
    id: car.value.id,
    brand: car.value.brand,
    model: car.value.model,
    year: car.value.year,
    price: car.value.price,
    image: car.value.images && car.value.images.length > 0 ? car.value.images[0] : ''
  }
  
  sessionStorage.setItem('contactCarData', JSON.stringify(carData))
  sessionStorage.setItem('contactSeller', car.value.seller.username)
  
  // Navigate to messages page
  router.push(`/messages`)
}

const addToCart = () => {
  if (!car.value) return

  // ตรวจสอบถ้าขายแล้ว
  if (car.value.sold_out) {
    alert('⚠️ สินค้านี้ขายหมดแล้ว')
    return
  }

  // ดึง cart จาก localStorage (แยกตามชื่อ username)
  const username = localStorage.getItem('username')
  const cartKey = `cart_${username}`
  let cart = []
  const saved = localStorage.getItem(cartKey)
  if (saved) {
    cart = JSON.parse(saved)
  }

  // ตรวจสอบรถซ้ำ
  const exists = cart.find(item => item.id === car.value.id)
  if (exists) {
    // แสดง animation สำหรับเตือน
    const cartBtn = document.getElementById('cartBtn')
    if (cartBtn) {
      cartBtn.classList.add('animate-duplicate-warning')
      setTimeout(() => cartBtn.classList.remove('animate-duplicate-warning'), 800)
    }
    showDuplicateWarning.value = true
    return
  }

  // เพิ่มรถเข้าตะกร้า
  cart.push({
    id: car.value.id,
    brand: car.value.brand,
    model: car.value.model,
    year: car.value.year,
    price: car.value.price,
    images: car.value.images,
    license_plate: car.value.license_plate
  })

  localStorage.setItem(cartKey, JSON.stringify(cart))
  
  // Show sold out animation
  showBuyNotification()
  
  // แสดง animation
  const cartBtn = document.getElementById('cartBtn')
  if (cartBtn) {
    cartBtn.classList.add('animate-cart-success')
    setTimeout(() => cartBtn.classList.remove('animate-cart-success'), 600)
  }
  
  // แสดง success modal แทน alert
  showSuccessModal.value = true
}

const showBuyNotification = () => {
  // Create sold out notification
  const notification = document.createElement('div')
  notification.className = 'buy-notification'
  notification.innerHTML = `
    <div class="buy-text">
      <i class="fas fa-shopping-bag"></i> ADDED TO CART
    </div>
  `
  
  document.body.appendChild(notification)
  
  // Remove after animation
  setTimeout(() => {
    notification.remove()
  }, 2000)
}

onMounted(async () => {
  try {
    const response = await fetch(`http://localhost:5000/api/cars/${route.params.id}`)
    const data = await response.json()
    
    if (data.success) {
      car.value = data.car
      console.log('Car data:', car.value)
      console.log('Engine size:', car.value.engine_size)
      console.log('Color:', car.value.color)
      
      // Start auto-sliding images
      startAutoSlide()
      
      // Increment view count
      incrementViewCount()
      
      if (car.value.seller && car.value.seller.username) {
        try {
          const profileRes = await fetch(
            `http://localhost:5000/api/get-profile?username=${car.value.seller.username}`
          )
          const profileData = await profileRes.json()
          if (profileData.profileImageUrl) {
            sellerProfileImage.value = profileData.profileImageUrl
          }
          if (profileData.lastActivity) {
            lastActivity.value = profileData.lastActivity
          }
          
          // Fetch seller's cars count using seller-info endpoint
          const sellerInfoRes = await fetch(
            `http://localhost:5000/api/seller-info/${car.value.seller.username}`
          )
          const sellerInfoData = await sellerInfoRes.json()
          
          if (sellerInfoData.success && sellerInfoData.seller) {
            const sellerId = sellerInfoData.seller.id
            const carsRes = await fetch(
              `http://localhost:5000/api/cars?seller_id=${sellerId}`
            )
            const carsData = await carsRes.json()
            if (carsData.success) {
              carsListed.value = carsData.cars.length
            }
          }
        } catch (error) {
          console.error('Error fetching seller profile:', error)
        }
      }
    }
  } catch (error) {
    console.error('Error fetching car details:', error)
  } finally {
    loading.value = false
  }

  // ติดตามสถานะออนไลน์
  const handleOnline = () => {
    isOnline.value = true
  }
  const handleOffline = () => {
    isOnline.value = false
  }

  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)

  return () => {
    window.removeEventListener('online', handleOnline)
    window.removeEventListener('offline', handleOffline)
  }
})
</script>

<style scoped>
@keyframes cartSuccess {
  0% {
    transform: scale(1);
    background: linear-gradient(to right, #dc2626, #b91c1c);
  }
  50% {
    transform: scale(1.05);
    background: linear-gradient(to right, #22c55e, #16a34a);
  }
  100% {
    transform: scale(1);
    background: linear-gradient(to right, #dc2626, #b91c1c);
  }
}

@keyframes duplicateWarning {
  0% {
    transform: translateX(0) scale(1);
    background: linear-gradient(to right, #dc2626, #b91c1c);
  }
  25% {
    transform: translateX(-10px) scale(1.02);
    background: linear-gradient(to right, #f97316, #ea580c);
  }
  50% {
    transform: translateX(10px) scale(1.02);
    background: linear-gradient(to right, #f97316, #ea580c);
  }
  75% {
    transform: translateX(-10px) scale(1.02);
    background: linear-gradient(to right, #f97316, #ea580c);
  }
  100% {
    transform: translateX(0) scale(1);
    background: linear-gradient(to right, #dc2626, #b91c1c);
  }
}

@keyframes popInHover {
  0% {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-cart-success {
  animation: cartSuccess 0.6s ease-in-out;
}

.animate-duplicate-warning {
  animation: duplicateWarning 0.8s ease-in-out;
}

.animate-pop-in-hover {
  animation: popInHover 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.buy-notification {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 50;
  animation: buyPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.buy-text {
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  color: white;
  padding: 20px 40px;
  border-radius: 12px;
  font-size: 24px;
  font-weight: bold;
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.5);
  border: 2px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 12px;
}

.buy-text i {
  font-size: 28px;
  animation: bagSwing 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes buyPop {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.5) rotateZ(-10deg);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.1) rotateZ(5deg);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1) rotateZ(0deg);
  }
}

@keyframes bagSwing {
  0% {
    transform: scale(0) rotateZ(-45deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.2) rotateZ(10deg);
  }
  100% {
    transform: scale(1) rotateZ(0deg);
    opacity: 1;
  }
  
}
</style>
