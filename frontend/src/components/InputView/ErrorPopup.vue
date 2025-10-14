<script setup lang="ts">
defineProps<{
  visible: boolean;
  message: string;
}>();

// Call for parent in case of an event
defineEmits(["close"]);
</script>

<template>
  <div v-if="visible" class="popup-overlay" data-testid="error-popup-overlay">
    <div class="popup" data-testid="error-popup">
      <!-- Close button (X) -->
      <button 
        class="close-btn"
        @click="$emit('close')"
        data-testid="error-popup-close-btn">
        &times;
      </button>

      <!-- Error message -->
      <p class="instruction-text error-instruction" data-testid="error-popup-message">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<style scoped>

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.popup {
  font-family: 'Inter', sans-serif;
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
  position: relative;
  text-align: center;
}

.instruction-text {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
}

.error-instruction {
  color: #cc0000be;
  font-weight: 600;
}

/* Close 'X' Button Style */
.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: #999;
  padding: 5px 10px;
  cursor: pointer;
}
.close-btn:hover {
  color: #333;
}
</style>