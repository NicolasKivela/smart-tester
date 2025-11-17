<script setup lang="ts">
import BddView from '@/components/ResultView/BddView.vue'
import CodeView from '@/components/ResultView/CodeView.vue'
import { ref } from 'vue'

// Emits for loader functionality
const emit = defineEmits(['start-loader', 'stop-loader'])

const props = defineProps({
  bddScenarios: {
    type: Array,
    required: true,
  },
  featureId: {
    type: Number,
    required: true,
  },
  resetValue: Number,
})
console.log('feature id in resultview', props.featureId)
const testScripts = ref('')

const handleTests = (tests) => {
  console.log(tests)
  testScripts.value = tests
}

// To pass loader events in BddView.vue to App.vue
const loaderStart = (message: string) => {
  emit('start-loader', message)
}
const loaderStop = (message: string) => {
  emit('stop-loader')
}
</script>

<template>
  <div class="column">
    <BddView
      :bdd-scenarios="bddScenarios"
      :feature-id="featureId"
      @update-tests="handleTests"
      @start-tests-loader="loaderStart"
      @stop-tests-loader="loaderStop"
    />
    <CodeView :scripts="testScripts" :reset-value="resetValue" />
  </div>
</template>

<style>
.column {
  display: flex;
  gap: 1rem;
}

.column > * {
  flex: 1;
}
</style>
