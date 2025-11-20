<script setup lang="ts">
import { ref, watch } from 'vue'
import { getLogs, getTokens } from '@/services/logService.ts'

const showMenu = ref(false)
const totalTokens = ref(0)
const promptTokens = ref(0)
const completionTokens = ref(0)

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const downloadLogs = async () => {
  try {
    const logs = await getLogs()

    // Replace escaped newlines with actual line breaks
    let textContent = logs
    textContent = textContent.replace(/\\n/g, '\n')
    const blob = new Blob([textContent], { type: 'text/plain' })

    // Create a temporary download link
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `logs-${new Date().toISOString().split('T')[0]}.txt`

    // Trigger the download by simulating a click
    document.body.appendChild(link)
    link.click()

    // Clean up
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    showMenu.value = false
  } catch (error) {
    console.error('Failed to download logs:', error)
    alert('Failed to download logs. Please try again.')
  }
}

watch(showMenu, (newValue) => {
  if (newValue) {
    getTokens().then((tokenResponse) => {
      totalTokens.value = tokenResponse.total_tokens
      promptTokens.value = tokenResponse.api_calls[0].prompt_tokens
      completionTokens.value = tokenResponse.api_calls[0].completion_tokens
    })
  }
})
</script>

<template>
  <header class="main-header">
    <div class="header-text">Transformative Engine for Smart Testing</div>
    <div class="settings-container">
      <button class="settings-button" @click="toggleMenu">
        <span class="material-icons">settings</span>
      </button>
      <div v-if="showMenu" class="dropdown-menu">
        <button class="menu-item menu-button" @click="downloadLogs">
          <span class="material-icons">download</span> Download logs
        </button>
        <div class="menu-item menu-text">Total tokens {{ totalTokens }}</div>
        <div class="menu-item menu-text">Prompt tokens {{ promptTokens }}</div>
        <div class="menu-item menu-text">Completion tokens {{ completionTokens }}</div>
      </div>
    </div>
  </header>
</template>

<style>
.main-header {
  color: white;
  font-size: 20px;
  height: 50px;
  position: fixed;
  top: 0;
  left: 0;
  background-color: #218a91;
  width: calc(100% - 40px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.settings-container {
  position: relative;
}

.settings-button {
  border: none;
  background-color: #218a91;
  color: white;
  padding: 4px 8px;
  height: auto;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.settings-button:hover {
  background-color: #1a6e76;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  z-index: 1000;
  margin-top: 8px;
}

.menu-item {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.menu-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
  width: 100%;
  text-align: left;
  transition: background-color 0.2s;
}

.menu-button:hover {
  background-color: #f0f0f0;
}

.menu-text {
  color: #666;
  cursor: default;
}
</style>
