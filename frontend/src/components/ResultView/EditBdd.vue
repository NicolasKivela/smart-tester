<script setup lang="ts">
import type { editable } from './types'
import { ref } from 'vue'

const props = defineProps<{
  visible: boolean
  scenario: editable
}>()

defineEmits(['close', 'save'])

const editable = ref(JSON.parse(JSON.stringify(props.scenario)))
const whenLineCount = ref(editable.value.when.split('\n').length || 1)
const thenLineCount = ref(editable.value.then.split('\n').length || 1)
const givenLineCount = ref(editable.value.given.split('\n').length || 1)
</script>

<template>
  <div v-if="visible" class="popup-overlay" data-testid="modify-bdd-popup-overlay">
    <div class="popup" data-testid="modify-bdd-popup">
      <div class="modal">
        <h2>Edit BDD Scenario</h2>

        <div class="input-grid">
          <div class="label">Feature:</div>
          <div><input v-model="editable.feature" class="input-field" /></div>
        </div>
        <div class="input-grid">
          <div class="label">Scenario:</div>
          <div><input v-model="editable.scenario" class="input-field" /></div>
        </div>
        <div class="input-grid">
          <div class="indented-label">Given</div>
          <div>
            <textarea v-model="editable.given" :rows="givenLineCount" class="input-field" />
          </div>
        </div>
        <div class="input-grid">
          <div class="indented-label">When</div>
          <div><textarea v-model="editable.when" :rows="whenLineCount" class="input-field" /></div>
        </div>
        <div class="input-grid">
          <div class="indented-label">Then</div>
          <div><textarea v-model="editable.then" :rows="thenLineCount" class="input-field" /></div>
        </div>
        <div class="actions">
          <button class="secondary" @click="$emit('close')">Cancel</button>
          <button class="primary" @click="$emit('save', editable)">Save</button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-overlay" @click.self="close"></div>
</template>

<style scoped>
/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
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
  max-width: 600px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  position: relative;
}
.input-field {
  width: 100%;
  margin: 5px 0;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.label {
  margin: 5px 0;
  padding: 5px;
}
.indented-label {
  margin: 5px 0 5px 20px;
  padding: 5px;
}
.input-grid {
  display: grid;
  grid-template-columns: 1fr 6fr;
  gap: 1rem;
}
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 15px;
}
</style>
