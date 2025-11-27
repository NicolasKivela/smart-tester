<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { BddScenario } from './types'
import { updateBddScenario, deleteBddScenario } from '@/services/resultsService.ts'

const props = defineProps({
  modelValue: {
    type: Object as () => BddScenario,
    required: true,
  },
})

const emit = defineEmits(['updateScenario', 'delete'])
const allowEdit = ref(false)
const bddScenario = ref(props.modelValue)

watch(
  () => props.modelValue,
  (newValue) => {
    bddScenario.value = newValue
  },
)

const saveEdited = () => {
  allowEdit.value = false

  updateBddScenario(bddScenario.value).then((response) => {
    if (response === 'success') {
      emit('updateScenario', bddScenario.value)
    } else {
      console.error('Failed to update BDD scenario: ', response)
    }
  })
}

const rows = computed(() => {
  return bddScenario.value.content ? bddScenario.value.content.split('\n').length : 4
})

const handleDelete = async () => {
  deleteBddScenario(bddScenario.value.feature_id, bddScenario.value.id).then((response) => {
    if (response === 'success') {
      emit('delete', bddScenario.value)
    } else {
      console.error('Failed to delete BDD scenario: ', response)
    }
  })
}
</script>

<template>
  <div class="bdd-card">
    <div class="bdd-text">
      <textarea
        v-if="allowEdit"
        v-model="bddScenario.content"
        cols="90"
        :rows="rows"
        data-testid="bdd-card-edit-textarea"
        @blur="saveEdited"
      ></textarea>
      <div v-else>
        <span data-testid="bdd-card-text">{{ bddScenario.content }}</span>
      </div>
    </div>
    <div class="actions">
      <button
        v-if="!allowEdit"
        class="round-button edit-button"
        data-testid="bdd-card-edit-btn"
        @click="allowEdit = true"
      >
        <span class="material-icons" style="font-size: 20px">edit</span>
      </button>
      <button
        v-else
        class="round-button save-button"
        data-testid="bdd-card-save-btn"
        @click="saveEdited"
      >
        <span class="material-icons" style="font-size: 20px">check</span>
      </button>
      <button
        class="round-button delete-button"
        data-testid="bdd-card-delete-btn"
        @click="handleDelete"
      >
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
