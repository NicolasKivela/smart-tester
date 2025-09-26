<script setup lang="ts"></script>

<template>
    <div class="code-view">
        <div class="column">
            <h3 class="title">Generated Code</h3>
            <button class="secondary">Download .zip</button>
            <button class="secondary">Copy</button>
            <button class="primary">Reset Session</button>
        </div>
        <div class="code-block">
            Generated code
        </div>
    </div>
</template>

<style scoped>
.code-view {
    border: 2px solid #ccc;
    padding: 1rem;
    border-radius: 4px;
}
.code-block {
    background-color: black;
    color: white;
    height: 400px;
    border-radius: 4px;
    padding: 1rem;
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
    flex: 3;
}
</style>