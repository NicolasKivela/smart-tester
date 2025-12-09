<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'
import hljs from 'highlight.js/lib/core'
import 'highlight.js/styles/github-dark.css'
import hljsDefineRobot from 'highlightjs-robot'
import {resetDatabase} from '@/services/requirementService.ts'
hljsDefineRobot(hljs)

const props = defineProps<{ scripts: string; resetValue: number }>()
const codeRef = ref<HTMLElement | null>(null)

// Try parsing the JSON
const parseJSON = (original: string) => {
  if (!original) return ''
  try {
    const parsed = JSON.parse(original)
    if (parsed.test_script) return parsed.test_script
  } catch {}
  return original
}

// Render & highlight the generated code
const highlightCode = async () => {
  if (!codeRef.value) return
  console.log('code view ', props.scripts)
  // Parse the JSON
  let code = parseJSON(props.scripts)

  // Convert all literal "\n" into real line breaks
  code = code.replace(/\\n/g, '\n')

  // Insert code into <code> block
  codeRef.value.textContent = code

  // Delete any previous highlights
  delete (codeRef.value as HTMLElement).dataset.highlighted

  // Highlight the code
  hljs.highlightAll()

  // Highlight 'xpath...]' sections
  await nextTick()
  const html = codeRef.value.innerHTML
  codeRef.value.innerHTML = html.replace(
    /(xpath\s*=\s*[^\]]*\])/gi,
    '<span class="xpath-highlight">$1</span>',
  )
}

// Reset the codeblock if a new feature is selected
const resetCodeBlock = () => {
  if (!codeRef.value) return

  // Delete any previous highlights
  delete (codeRef.value as HTMLElement).dataset.highlighted

  // Clear the current code content
  codeRef.value.textContent = ''
}

// Reset the whole session, refreshes the page
const resetSession = async () => {
  await resetDatabase()
  window.location.reload()
}

// Watch props.scripts for changes
onMounted(highlightCode)
watch(() => props.scripts, highlightCode)

// Watch props.resetValue for reset
watch(
  () => props.resetValue,
  () => {
    resetCodeBlock()
  },
)

// Copy full script to clipboard
const copyToClipboard = () => {
  // Parse the JSON
  let code = parseJSON(props.scripts)

  // Convert all literal "\n" into real line breaks
  code = code.replace(/\\n/g, '\n')

  navigator.clipboard
    .writeText(code)
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
      <button class="secondary" data-testid="code-view-copy-btn" @click="copyToClipboard">
        Copy
      </button>
      <button class="primary" data-testid="code-view-reset-session-btn" @click="resetSession">
        Reset Session
      </button>
    </div>
    <pre class="code-block">
      <code ref="codeRef" data-testid="code-view-code-text" class="language-robot"></code>
    </pre>
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
  background-color: #0d1117;
  flex: 1;
  border-radius: 4px;
  overflow-y: auto;
  white-space: pre-wrap;
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

.code-block :deep(.xpath-highlight) {
  color: #ee82ee;
  font-weight: bold;
}
</style>
