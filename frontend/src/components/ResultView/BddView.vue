<script setup lang="ts"></script>

<template>
    <div class="bdd-view">
        <div class="column">
            <h3 class="title">BDD Scenarios</h3>
            <button class="primary">Generate Tests</button>
        </div>
        <div class="code-block">
            BDD Scenarios
        </div>
    </div>
</template>

<style scoped>
.bdd-view {
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
    flex: 8;
    justify-self: start;
    align-self: center;
    margin-top: 0.5rem;
}
button {
    flex: 2;
}
</style>
