<script setup lang="ts">
import MainHeader from '@/components/mainHeader.vue'
import InputView from '@/components/InputView/InputView.vue'
import ResultView from '@/components/ResultView/ResultView.vue'
</script>

<template>
  <MainHeader />
  <div class="app">
    <InputView />
    <ResultView />
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
