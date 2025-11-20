<script setup lang="ts">
import BddCard from '@/components/ResultView/BddCard.vue'
import { watch, ref, computed } from 'vue'
import type { BddScenario } from './types'
import { createTests } from '@/services/resultsService.ts'

const props = defineProps<{
  bddScenarios: BddScenario[]
  featureId: number
}>()

const emit = defineEmits(['updateTests', 'start-tests-loader', 'stop-tests-loader'])

const mutatedBddScenarios = ref<BddScenario[]>(props.bddScenarios)

// Function to check if the "Generate tests" -button should be activated
const disabledButton = computed(() => {
  return !props.featureId || props.bddScenarios.length === 0
})

const generateTests = async () => {
  // Start loader
  emit('start-tests-loader', 'Generating tests, please wait...')

  const result = await createTests(props.featureId)

  console.log('test scripts', result)
  emit('updateTests', result)

  // Stop loader
  emit('stop-tests-loader')
}

//TODO: Handle adding new scenarios
// const addEmptyScenario = () => {
//   mutatedBddScenarios.value.push({
//     feature: 'New Feature',
//     scenario: 'New Scenario',
//     given: [''],
//     when: [''],
//     then: [''],
//   })
// }

watch(
  () => props.bddScenarios,
  (newValue) => {
    mutatedBddScenarios.value = newValue
  },
)
</script>

<template>
  <div class="bdd-view">
    <div class="column">
      <h3 class="title">BDD Scenarios</h3>
      <button class="primary" @click="generateTests" :disabled="disabledButton">
        Generate Tests
      </button>
    </div>
    <div class="scrollable-section">
      <ul
        v-for="(bddScenario, index) in mutatedBddScenarios"
        :key="index"
        style="list-style: none; padding-left: 0; margin-left: 0"
      >
        <BddCard
          :modelValue="bddScenario"
          @update-scenario="(value) => (mutatedBddScenarios[index] = value)"
          @delete="mutatedBddScenarios.splice(index, 1)"
        />
      </ul>
      <!-- <button class="primary add-button" @click="addEmptyScenario">
      <span class="material-icons" style="font-size: 20px">add</span> Add New Scenario
    </button> -->
    </div>
  </div>
</template>

<style scoped>
.bdd-view {
  border: 2px solid #ccc;
  padding: 1rem;
  border-radius: 4px;
  height: calc(100vh - 275px);
  display: flex;
  flex-direction: column;
}
.scrollable-section {
  flex: 1;
  overflow-y: auto;
}
.column {
  display: flex;
  gap: 1rem;
}
.title {
  flex: 8;
  justify-self: start;
  align-self: center;
  margin-top: 0.5rem;
}
button {
  flex: 2;
}
.add-button {
  display: flex;
  align-items: center;
}
button.primary:disabled {
  cursor: not-allowed !important;
  background: #cccccc;
  color: #666666;
}
</style>
