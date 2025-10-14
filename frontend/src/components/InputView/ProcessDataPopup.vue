<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
  visible: boolean;
  options: { id: number; name: string }[];
}>();

// Call for parent in case of an event
defineEmits(["close", "continue"]);

// Selected option for implementing BDD:s
const selectedOption = ref<number | null>(null);

// Reset the selectedOption when opening the popup
watch(
  () => props.visible,
  (newVal) => {
    if (newVal) {
      selectedOption.value = null; // Reset immediately when popup opens
    }
  }
);

</script>

<template>
    <!-- Process data popup -->
  <div v-if="visible" class="popup-overlay" data-testid="process-popup-overlay">
    <div class="popup" data-testid="processdata-popup">

      <!-- Close button (X) in top right -->
      <button 
        class="close-btn"
        @click="$emit('close')"
        data-testid="processdata-popup-close-btn">
        &times;</button>
      
      <h2 data-testid="processdata-popup-title">Requirements have been processed</h2>
        <!-- Instruction text -->
        <p class="instruction-text" data-testid="processdata-popup-instruction-text">
          Choose the feature you want to continue making BDD scenarios and tests for.
        </p>

      <!-- Radio Buttons -->
      <div class="radio-group" data-testid="popup-radio-group">
        <label 
          v-for="option in props.options"
          :key="option.id"
          class="radio-label"
          :data-testid="`popup-radio-${option.name.replace(/\s+/g, '-').toLowerCase()}`">

          <input 
            type="radio"
            :value="option.id"
            v-model="selectedOption"
            :data-testid="`radio-input-${option.id}`" />
          {{ option.name }}
        </label>
      </div>

      <!-- Action Buttons -->
      <div class="popup-buttons">
        <button 
          class="secondary cancel-btn"
          @click="$emit('close')"
          data-testid="processdata-popup-cancel-btn">
          Cancel
        </button>

        <button 
          class="primary continue-btn"
          @click="$emit('continue', selectedOption)"
          :disabled="!selectedOption"
          data-testid="processdata-popup-continue-btn">
          Continue
        </button>
      </div>
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
  text-align: left;
}

.popup h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 10px;
  line-height: 1.2;
}

.instruction-text {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
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

/* Radio Button Group Styling */
.radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 30px;
}

.radio-label {
  display: flex;
  align-items: center;
  font-size: 1rem;
  cursor: pointer;
}

.radio-label input[type="radio"] {
  /* Default radio button appearance */
  margin-right: 10px;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* Popup Action Buttons */
.popup-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 15px;
  border-top: 1px solid #eee;
  margin-left: -30px;
  margin-right: -30px;
  margin-bottom: -30px;
  padding-right: 30px;
  padding-bottom: 30px;
  background: #f7f7f7;
  border-radius: 0 0 8px 8px;
}

.popup-buttons button {
  padding: 10px 20px;
}

button.primary:disabled {
    cursor: not-allowed !important;
    background: #cccccc;
    color: #666666;
}
</style>