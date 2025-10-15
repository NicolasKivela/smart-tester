<script setup lang="ts">
const props = defineProps<{
  scripts: object
}>()

const copyToClipboard = () => {
  navigator.clipboard
    .writeText(props.scripts.toString())
    .then(() => {
      console.log('Code copied to clipboard')
    })
    .catch((err) => {
      console.error('Failed to copy code: ', err)
    })
}
</script>

<template>
  <div class="code-view">
    <div class="column">
      <h3 class="title">Generated Code</h3>
      <!--<button class="secondary">Download .zip</button>-->
      <button class="secondary" @click="copyToClipboard">Copy</button>
      <button class="primary">Reset Session</button>
    </div>
    <div class="code-block">
      <p v-for="(script, index) of scripts" :key="index">{{ script }}</p>
    </div>
  </div>
</template>

<style scoped>
.code-view {
  border: 2px solid #ccc;
  padding: 1rem;
  border-radius: 4px;
  height: calc(100vh - 275px);
  display: flex;
  flex-direction: column;
}
.code-block {
  background-color: black;
  color: white;
  height: 400px;
  border-radius: 4px;
  padding-left: 1rem;
  padding-right: 1rem;
  flex: 1;
  overflow-y: auto;
}
.column {
  display: flex;
  gap: 1rem;
}
.title {
  flex: 6;
  justify-self: start;
  align-self: center;
  margin-top: 0.5rem;
}
button {
  flex: 2;
}
</style>
