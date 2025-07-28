<script setup>
import Navbar from './components/Navbar.vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

// ✅ This makes it reactive on route change
const hideNavbar = computed(() => ['login', 'register'].includes(route.name))
</script>

<template>
  <div class="app-wrapper">
    <div class="background-gif"></div>
    <div class="foreground-container">
      <Navbar v-if="!hideNavbar" />
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.app-wrapper {
  position: relative;
  min-height: 100vh;
  overflow-x: hidden;
  /* background-color: #111; Fallback */
}

/* Background GIF layer */
.background-gif {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 0;
  width: 100%;
  height: 100%;
  background-image: url('/Users/varundhand/Desktop/IITM/mad 2 final project /vehicle_parking_app_24dp2000034/frontend/frontend/src/assets/iitm-bg.gif');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.55;
  filter: blur(2px);
  pointer-events: none;
}

/* Foreground layout above background */
.foreground-container {
  position: relative;
  z-index: 1;
  padding: 1rem;
  color: #e0e0e0;
  font-family: 'Segoe UI', sans-serif;
}

</style>
