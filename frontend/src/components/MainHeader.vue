<script setup lang="ts">
import { getLogs } from '@/services/logService.ts'

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
  } catch (error) {
    console.error('Failed to download logs:', error)
    alert('Failed to download logs. Please try again.')
  }
}
</script>

<template>
  <header class="main-header">
    <div class="header-text">Transformative Engine for Smart Testing</div>
    <button class="settings-button" @click="downloadLogs" style="font-size: 14px">
      <span class="material-icons">settings</span> Download logs
    </button>
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

.settings-button {
  border: none;
  background-color: #218a91;
  color: white;
  padding: 4px 8px;
  height: auto;
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>
