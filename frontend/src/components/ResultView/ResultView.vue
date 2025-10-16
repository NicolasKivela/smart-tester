<script setup lang="ts">
import BddView from '@/components/ResultView/BddView.vue'
import CodeView from '@/components/ResultView/CodeView.vue'
import { ref } from 'vue'

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
</script>

<template>
  <div class="column">
    <BddView :bdd-scenarios="bddScenarios" @update-tests="handleTests" />
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
