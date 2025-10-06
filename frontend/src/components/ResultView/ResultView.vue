<script setup lang="ts">
    import bddView from '@/components/ResultView/BddView.vue'
    import codeView from '@/components/ResultView/CodeView.vue'
</script>

<template>
    <div class="column">
        <bddView />
        <codeView />
    </div>
</template>

<style>
.column {
    display: flex;
    gap: 1rem;
}

.column > * {
    flex: 1;
}
</style>