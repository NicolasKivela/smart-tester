<script setup lang="ts">
import { ref } from "vue";

// Initialize inputs 
const file = ref<File | null>(null);
const url = ref("");
const username = ref("");
const password = ref("");

// Key to force the file input to reset if inputs are resetted
const fileInputKey = ref(0); 

// Error state for file validation
const fileError = ref(false);

// Error state for URL validation
const urlError = ref(false);

// Popup visibility variable
const showPopup = ref(false);

// Selected option for implementing BDD:s
const selectedOption = ref<string | null>(null);

// Temporary list of the scenarios for demo effect
// TODO: fetch the actual options of req. file from backend 
const options = ["Login", "Checkout", "Add to cart"];

// Handle file input
const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;

  // Clear any previous error in file input
  fileError.value = false;
  
  // Ensure that a file was selected
  if (target.files?.[0]) {
    const selectedFile = target.files[0];
    const fileName = selectedFile.name;

    // Check for .pdf or .txt
    if (fileName.endsWith('.pdf') || fileName.endsWith('.txt')) {
        file.value = selectedFile;
    } else {
        // Validation failed, show error popup
        fileError.value = true;
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
  urlError.value = false; // Reset URL error always

  try {
    // Try to validate URL
    new URL(url.value);
    
    // If successful, proceed to show the popup
    selectedOption.value = null; // Reset options always when opening
    showPopup.value = true;
  } 
  catch (e) {
    // If invalid, show error
    urlError.value = true;
    showPopup.value = false;
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

// "Continue" button pressed in popup, only closes the popup for now
// TODO: pass the selected option to backend
const handleContinue = () => {
    showPopup.value = false;
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

  <!-- FileError popup -->
  <div v-if="fileError" class="popup-overlay">
    <div class="popup">
      <!-- Close button (X) in top right -->
      <button class="close-btn" @click="fileError = false">&times;</button>

      <!-- Error instruction text -->
      <p class="instruction-text error-instruction">Only PDF (.pdf) or Text (.txt) files are allowed!</p>

    </div>
  </div>

  <!-- UrlError popup -->
  <div v-if="urlError" class="popup-overlay">
    <div class="popup">
      <!-- Close button (X) in top right -->
      <button class="close-btn" @click="urlError = false">&times;</button>

      <!-- Error instruction text -->
      <p class="instruction-text error-instruction">Please enter a valid URL!</p>

    </div>
  </div>

  <!-- Process data popup -->
  <div v-if="showPopup" class="popup-overlay">
    <div class="popup">

      <!-- Close button (X) in top right -->
      <button class="close-btn" @click="showPopup = false">&times;</button>
      
      <h2>Requirements have been processed</h2>
        <!-- Instruction text -->
        <p class="instruction-text">Choose the feature you want to continue making BDD scenarios and tests for.</p>

      <!-- Radio Buttons -->
      <div class="radio-group">
        <label v-for="option in options" :key="option" class="radio-label">
          <input type="radio" :value="option" v-model="selectedOption"/>
          {{ option }}
        </label>
      </div>

      <!-- Action Buttons -->
      <div class="popup-buttons">
        <button class="secondary cancel-btn" @click="showPopup = false">Cancel</button>
        <button class="primary continue-btn" @click="handleContinue" :disabled="!selectedOption" >Continue</button>
      </div>

    </div>
  </div>
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

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.popup {
  font-family: 'Inter', sans-serif;
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
  position: relative;
  text-align: left;
}

.popup h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 10px;
  line-height: 1.2;
}

.instruction-text {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
}

/* Red color for error messages */
.error-instruction {
    color: #cc0000be; 
    font-weight: 600; 
}

/* Close 'X' Button Style */
.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: #999;
  padding: 5px 10px;
  cursor: pointer;
}

.close-btn:hover {
  color: #333;
}

/* Radio Button Group Styling */
.radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 30px;
}

.radio-label {
  display: flex;
  align-items: center;
  font-size: 1rem;
  cursor: pointer;
}

.radio-label input[type="radio"] {
  /* Default radio button appearance */
  margin-right: 10px;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* Popup Action Buttons */
.popup-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 15px;
  border-top: 1px solid #eee;
  margin-left: -30px;
  margin-right: -30px;
  margin-bottom: -30px;
  padding-right: 30px;
  padding-bottom: 30px;
  background: #f7f7f7;
  border-radius: 0 0 8px 8px;
}

.popup-buttons button {
  padding: 10px 20px;
}
</style>
