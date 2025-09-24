<script setup lang="ts">
import { ref } from "vue";

// Initialize inputs 
const file = ref<File | null>(null);
const url = ref("");
const username = ref("");
const password = ref("");

// Handle file input
const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  // Ensure that a file was selected.
  if (target.files?.[0]) {
    file.value = target.files[0];
  }
};

// TODO: make the button send the file forward to create BDDs.
const generateBDD = () => {

};

// Reset input button triggers this to reset of inputs.
const resetInputs = () => {
  file.value = null;
  url.value = "";
  username.value = "";
  password.value = "";
};
</script>

<template>
  <!-- Inpuview -->  
  <div class="inputview">
    
    <!-- File input -->
    <div class="titles">
      <span>Add requirements file</span>
      <input type="file" @change="handleFileUpload" />
    </div>

    <!-- URL input -->
    <div class="titles">
      <span>URL</span>
      <input type="text" v-model="url" placeholder="URL" class="url-input" />
    </div>

    <!-- Username input -->
    <div class="titles">
      <span>Username</span>
      <input type="text" v-model="username" placeholder="Username" class="text-input"/>
    </div>

    <!-- Password input -->
    <div class="titles">
      <span>Password</span>
      <input type="password" v-model="password" placeholder="Password" class="text-input" />
    </div>

    <!-- Buttons -->
    <div class="buttons">
      <button class="primary" @click="generateBDD">Generate BDD scenarios</button>
      <button class="secondary" @click="resetInputs">Reset Inputs</button>
    </div>
  </div>
</template>

<style scoped>

/* Input field properties */
.inputview {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  font-family: monospace;
  gap: 20px;
  margin-bottom: 20px;
  background: #d0e7ea;
  border: 1px solid #aaa;
  border-radius: 6px;
  padding: 15px;
  box-sizing: border-box;
  align-items: baseline;
}

.url-input{
    min-width: 250px;
    padding: 8px;
    border: 1px solid #bbb;
    border-radius: 4px;
}

.text-input {
  background: #ffffffff;
  padding: 8px;
  border: 1px solid #bbb;
  border-radius: 4px;
}

/* Title properties */
.titles {
  display: flex;
  flex-direction: column;
}

.titles span {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 4px;
}

/* Button properties */
.buttons {
  display: flex;
  gap: 10px;
  margin-left: auto;
  align-self: center;
}

button {
  padding: 8px 14px;
  border: 1px solid #aaa;
  border-radius: 4px;
  cursor: pointer;
}

button.primary {
  background: #1b7b7f;
  color: white;
}

button.secondary {
  background: #218a9138;
  color: black;
}
</style>
