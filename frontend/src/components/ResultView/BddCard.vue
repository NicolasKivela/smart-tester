<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const bddScenario = ref(props.modelValue)

watch(
  () => props.modelValue,
  (newValue) => {
    bddScenario.value = newValue
  },
)

const saveEdited = () => {
  editable.value = false
  updateValue()
}

const updateValue = () => {
  emit('update:modelValue', bddScenario.value)
}

const editable = ref(false)
const rows = ref(bddScenario.value.split('\n').length)
</script>

<template>
  <div class="bdd-card">
    <div class="bdd-text">
      <textarea
        v-if="editable"
        v-model="bddScenario"
        cols="50"
        :rows="rows"
        @blur="saveEdited"
      ></textarea>
      <span v-else> {{ bddScenario }}</span>
    </div>
    <div class="actions">
      <button v-if="!editable" class="round-button edit-button" @click="editable = true">
        <span class="material-icons" style="font-size: 20px">edit</span>
      </button>
      <button v-else class="round-button save-button" @click="saveEdited">
        <span class="material-icons" style="font-size: 20px">check</span>
      </button>
      <button class="round-button delete-button">
        <span class="material-icons" style="font-size: 20px">close</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.bdd-card {
  border: 2px solid #ccc;
  padding: 1rem;
  border-radius: 4px;
  font-size: 12px;
  display: flex;
  gap: 1rem;
  white-space: pre;
}
.actions {
  flex: 1;
  align-self: center;
}
.bdd-text {
  flex: 10;
}
.edit-button {
  margin-bottom: 16px;
}
.save-button {
  margin-bottom: 16px;
  background-color: green;
}
.delete-button {
  background-color: red;
}
</style>
