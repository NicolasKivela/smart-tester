<script setup lang="ts">
import { ref } from 'vue'
import MainHeader from '@/components/MainHeader.vue'
import InputView from '@/components/InputView/InputView.vue'
import ResultView from '@/components/ResultView/ResultView.vue'
import LoaderView from './components/LoaderView/LoaderView.vue'

const bddScenarios = ref([])
const chosenFeature = ref(Number)

// Loader states
const isLoading = ref(false)
const loadingMessage = ref('')

// Reset key for codeview
const resetKey = ref(0)

const handleBddScenarios = (scenarios) => {
  bddScenarios.value = scenarios
}
const handleFeatures = (feature_id) => {
  chosenFeature.value = feature_id
  console.log("THIS IS THE CHOSEN FEATURE ID",chosenFeature.value)
}
// Loader start/stop functions
const startLoader = (message: string) => {
  loadingMessage.value = message
  isLoading.value = true
}

const stopLoader = () => {
  isLoading.value = false
}

const resetCodeBlock = () => {
  resetKey.value++;
}
</script>

<template>
  <MainHeader />
  <div class="app">
    <InputView 
      @bdd-scenarios-updated="handleBddScenarios"
      @chosen-feature-updated="handleFeatures"
      @start-loader="startLoader"
      @stop-loader="stopLoader"
      @reset-code-block="resetCodeBlock"
    />
    <ResultView 
      :bdd-scenarios="bddScenarios"
      :feature-id="chosenFeature"
      :reset-value="resetKey"
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
