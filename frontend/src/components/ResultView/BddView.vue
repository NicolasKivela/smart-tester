<script setup lang="ts">
import BddCard from '@/components/ResultView/BddCard.vue'
import { ref } from 'vue';

const bddScenarios = ref(['Feature: Login\n\tScenario: Successful login\n\tGiven user on login page\n\tWhen valid credentials are entered\n\tThen redirect to dashboard\n\tAnd show welcome message'])

const generateTests = () => {
    // TODO: Implement generating tests logic
    console.log('Generating tests...');
}
</script>

<template>
    <div class="bdd-view">
        <div class="column">
            <h3 class="title">BDD Scenarios</h3>
            <button class="primary" @click="generateTests">Generate Tests</button>
        </div>
        <ul v-for="(bddScenario, index) in bddScenarios" :key="index" style="list-style: none; padding-left: 0; margin-left: 0;">
            <BddCard :modelValue="bddScenario" @update:modelValue="value => bddScenarios[index] = value" />
        </ul>
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
