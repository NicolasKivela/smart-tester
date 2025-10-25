<script setup lang="ts">
import { ref } from 'vue'
import MainHeader from '@/components/MainHeader.vue'
import InputView from '@/components/InputView/InputView.vue'
import ResultView from '@/components/ResultView/ResultView.vue'
import LoaderView from './components/LoaderView/LoaderView.vue'

const bddScenarios = ref([])

// Loader states
const isLoading = ref(false)
const loadingMessage = ref('')

const handleBddScenarios = (scenarios) => {
  bddScenarios.value = scenarios
}

// Loader start/stop functions
const startLoader = (message: string) => {
  loadingMessage.value = message
  isLoading.value = true
}

const stopLoader = () => {
  isLoading.value = false
}
</script>

<template>
  <MainHeader />
  <div class="app">
    <InputView 
      @bdd-scenarios-updated="handleBddScenarios"
      @start-loader="startLoader"
      @stop-loader="stopLoader"
    />
    <ResultView 
      :bdd-scenarios="bddScenarios"
      @start-loader="startLoader"
      @stop-loader="stopLoader"
    />
    <LoaderView :visible="isLoading" :message="loadingMessage" />
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
