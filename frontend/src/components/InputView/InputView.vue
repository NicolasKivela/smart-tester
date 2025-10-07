<script setup lang="ts">
import { ref } from "vue";
import ErrorPopup from '@/components/InputView/ErrorPopup.vue'
import ProcessDataPopup from '@/components/InputView/ProcessDataPopup.vue'

// Initialize inputs 
const file = ref<File | null>(null);
const url = ref("");
const username = ref("");
const password = ref("");

// Key to force the file input to reset if inputs are resetted
const fileInputKey = ref(0); 

// Shows error popup when true
const showError = ref(false);

// Error message that is wanted to be displayed
// Reusable for different errors
const errorMessage = ref("");

// Popup visibility variable
const showPopup = ref(false);

// Handle file input
const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;

  // Clear any previous error in file input
  showError.value = false;
  
  // Ensure that a file was selected
  if (target.files?.[0]) {
    const selectedFile = target.files[0];
    const fileName = selectedFile.name;

    // Check for .pdf or .txt
    if (fileName.endsWith('.pdf') || fileName.endsWith('.txt')) {
        file.value = selectedFile;
    } else {
        // Validation failed, show error popup
        errorMessage.value = "Only PDF (.pdf) or Text (.txt) files are allowed!";
        showError.value = true;
        file.value = null;

        // Force reset the input field to clear the filename display
        fileInputKey.value++; 
    }
  } 
  else {
    file.value = null;
  }
};

// Show popup after clicking the "Process data button"
// TODO: pass the inputs to the backend
const processdata = () => {
  showError.value = false; // Reset URL error always

  try {
    // Try to validate URL
    new URL(url.value);
    
    // If successful, proceed to show the popup
    showPopup.value = true;
  } 
  catch (e) {
    // If invalid, show error and reset url field
    errorMessage.value = "Please enter a valid URL!";
    showError.value = true;
    url.value = "";
  }
};

// Reset the inputs
const resetInputs = () => {
  file.value = null;
  url.value = "";
  username.value = "";
  password.value = "";
  fileInputKey.value++; 
};

// "Continue" button pressed in popup
// String "selected" is the option selected to create BDD:s and tests to
// TODO: pass the selected option to backend
const handleContinue = (selected: string) => {
    showPopup.value = false;

    // Show the selected option in console for now
    console.log("Selected option from popup:", selected);
}

</script>

<template>
  <!-- Inputview -->  
  <div class="inputview">
    
    <!-- File input -->
    <div class="titles">
      <span>Add requirements file <span class="required-input">*</span></span>
      <input type="file" @change="handleFileUpload" :key="fileInputKey"/>
      <p class="input-description">PDF (.pdf) or Text (.txt) file accepted</p>
    </div>

    <!-- URL input -->
    <div class="titles">
      <span>URL <span class="required-input">*</span></span>
      <input type="text" v-model="url" placeholder="URL" class="url-input"/>
    </div>

    <!-- Username input -->
    <div class="titles">
      <span>Username <small class="input-description">(optional)</small></span>
      <input type="text" v-model="username" placeholder="Username" class="text-input"/>
    </div>

    <!-- Password input -->
    <div class="titles">
      <span>Password <small class="input-description">(optional)</small></span>
      <input type="password" v-model="password" placeholder="Password" class="text-input"/>
    </div>

    <!-- Buttons -->
    <div class="buttons">
      <button class="primary" @click="processdata" :disabled="!file || !url.trim()">Process data</button>
      <button class="secondary" @click="resetInputs">Reset Inputs</button>
    </div>
  </div>

    <!-- Reusable error popup -->
    <ErrorPopup
    :visible="showError"
    :message="errorMessage"
    @close="showError = false"
    />

    <!-- Process data popup -->
    <ProcessDataPopup
    :visible="showPopup"
    @close="showPopup = false"
    @continue="handleContinue"
    />

</template>

<!-- Styles -->
<style scoped>

/* Input field properties */
.inputview {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  font-family: 'Inter', sans-serif;
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

.required-input{
  color: #cc0000be;
}

.input-description {
    font-size: 12px; 
    color: #777; 
    margin-top: 5px; 
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

button.primary:disabled {
    cursor: not-allowed !important;
    background: #cccccc;
    color: #666666;
}

button.secondary {
  background: #218a9138;
  color: black;
}
</style>
