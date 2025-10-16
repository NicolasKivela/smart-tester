<script setup lang="ts">
import { ref, watch } from 'vue'
import type { BddScenario } from './types'

const props = defineProps({
  modelValue: {
    type: Object as () => BddScenario,
    required: true,
  },
})

const emit = defineEmits(['updateScenario', 'delete'])

const bddScenario = ref(props.modelValue)
const bddScenarioString = ref()

watch(
  () => props.modelValue,
  (newValue) => {
    bddScenario.value = newValue
  },
)

const saveEdited = () => {
  editable.value = false
  emit('updateScenario', bddScenario.value)
}

const editable = ref(false)
const rows = ref(
  2 +
    bddScenario.value.given.length +
    bddScenario.value.when.length +
    bddScenario.value.then.length,
)
</script>

<template>
  <div class="bdd-card">
    <div class="bdd-text">
      <textarea
        v-if="editable"
        :v-model="bddScenarioString"
        cols="50"
        :rows="rows"
        @blur="saveEdited"
      ></textarea>
      <div v-else>
        <span>Feature: {{ bddScenario.feature }}<br /></span>
        <span>Scenario: {{ bddScenario.scenario }}<br /></span>
        <div style="margin-left: 20px">
          <span>Given {{ bddScenario.given[0] }}<br /></span>
          <span v-for="(given, index) in bddScenario.given.slice(1)" :key="index"
            >And {{ given }}<br
          /></span>
          <span>When {{ bddScenario.when[0] }}<br /></span>
          <span v-for="(when, index) in bddScenario.when.slice(1)" :key="index"
            >And {{ when }}<br
          /></span>
          <span>Then {{ bddScenario.then[0] }}<br /></span>
          <span v-for="(then, index) in bddScenario.then.slice(1)" :key="index"
            >And {{ then }}<br
          /></span>
        </div>
      </div>
    </div>
    <!-- <div class="actions">
      <button v-if="!editable" class="round-button edit-button" @click="editable = true">
        <span class="material-icons" style="font-size: 20px">edit</span>
      </button>
      <button v-else class="round-button save-button" @click="saveEdited">
        <span class="material-icons" style="font-size: 20px">check</span>
      </button>
      <button class="round-button delete-button" @click="emit('delete')">
        <span class="material-icons" style="font-size: 20px">close</span>
      </button>
    </div> -->
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
