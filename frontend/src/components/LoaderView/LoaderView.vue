<script setup lang="ts">

defineProps<{
  visible: boolean
  message: string
}>();
</script>

<template>
  <div v-if="visible" class="loaderView" data-testid="loaderView">
    <div class="spinner"></div>
    <p>{{ message }}</p>
  </div>
</template>

<style scoped>
.loaderView {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  font-family: 'Inter', sans-serif;
  color: #1b7b7f;
  font-weight: 600;
  font-size: 20px;
}

/* Spinner properties */
.spinner {
  border: 5px solid #f3f3f3;
  border-top: 5px solid #1b7b7f;
  border-radius: 50%;
  width: 100px;
  height: 100px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>