<script setup lang="ts">
import MainHeader from '@/components/mainHeader.vue'
import InputView from '@/components/InputView/InputView.vue'
import ResultView from '@/components/ResultView/ResultView.vue'
</script>

<template>
  <div class="app">
    <MainHeader />
    <InputView />
    <ResultView />
  </div>
</template>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
}
</style>
