<template>
  <v-app>
    <AppBar />

    <v-main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>

    <BottomNav />
  </v-app>
</template>

<script setup lang="ts">
import AppBar from '@/components/layout/AppBar.vue'
import BottomNav from '@/components/layout/BottomNav.vue'
</script>

<style>
.main-content {
  padding-bottom: 70px;
  /* Space for bottom navigation on mobile */
  min-height: 100vh;
  background: linear-gradient(180deg, #0A1628 0%, #001E40 100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Custom scrollbar for dark theme */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #0A1628;
}

::-webkit-scrollbar-thumb {
  background: #243652;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #2d4563;
}
</style>