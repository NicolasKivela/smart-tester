<script setup lang="ts">
import { ref } from 'vue'
import MainHeader from '@/components/MainHeader.vue'
import InputView from '@/components/InputView/InputView.vue'
import ResultView from '@/components/ResultView/ResultView.vue'

const bddScenarios = ref([])

const handleBddScenarios = (scenarios) => {
  bddScenarios.value = scenarios
}
</script>

<template>
  <MainHeader />
  <div class="app">
    <InputView @bdd-scenarios-updated="handleBddScenarios" />
    <ResultView :bdd-scenarios="bddScenarios" />
  </div>
</template>

<style scoped>
.app {
  margin-top: 50px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}
</style>
