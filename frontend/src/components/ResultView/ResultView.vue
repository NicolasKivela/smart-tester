<script setup lang="ts">
import BddView from '@/components/ResultView/BddView.vue'
import CodeView from '@/components/ResultView/CodeView.vue'
import { ref } from 'vue'

// Emits for loader functionality
const emit = defineEmits(['start-loader', 'stop-loader'])

defineProps({
  bddScenarios: {
    type: Array,
    required: true,
  },
})

const testScripts = ref([])

const handleTests = (tests) => {
  for (const key in tests) {
    testScripts.value.push(tests[key].content)
  }
}

// To pass loader events in BddView.vue to App.vue
const loaderStart = (message: string) =>{
  emit('start-loader', message)
}
const loaderStop = (message: string) =>{
  emit('stop-loader')
}

</script>

<template>
  <div class="column">
    <BddView
      :bdd-scenarios="bddScenarios"
      @update-tests="handleTests"
      @start-tests-loader="loaderStart"
      @stop-tests-loader="loaderStop"
    />
    <CodeView :scripts="testScripts" />
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
