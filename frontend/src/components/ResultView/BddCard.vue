<script setup lang="ts">
import { ref, watch } from 'vue'
import type { BddScenario } from './types'
import EditBdd from '@/components/ResultView/EditBdd.vue'
import { updateBddScenario, deleteBddScenario } from '@/services/resultsService.ts'

const props = defineProps({
  modelValue: {
    type: Object as () => BddScenario,
    required: true,
  },
})

const emit = defineEmits(['updateScenario', 'delete'])
const allowEdit = ref(false)
const bddScenario = ref(props.modelValue)

watch(
  () => props.modelValue,
  (newValue) => {
    bddScenario.value = newValue
  },
)

const saveEdited = (editedScenario) => {
  allowEdit.value = false

  updateBddScenario(editedScenario).then((response) => {
    if (response === 'success') {
      emit('updateScenario', editedScenario)
    } else {
      console.error('Failed to update BDD scenario: ', response)
    }
  })
}

const editable = ref(false)
// const rows = ref(
//   2 +
//     bddScenario.value.given.length +
//     bddScenario.value.when.length +
//     bddScenario.value.then.length,
// )
const handleDelete = async () => {
  deleteBddScenario(bddScenario.value.id).then((response) => {
    if (response === 'success') {
      emit('delete', bddScenario.value)
    } else {
      console.error('Failed to delete BDD scenario: ', response)
    }
  })
}
</script>

<template>
  <div class="bdd-card">
    <div class="bdd-text">
      <textarea
        v-if="editable"
        :v-model="bddScenarioString"
        cols="50"
        :rows="5"
        @blur="saveEdited"
      ></textarea>
      <div v-else>
        <span>{{ bddScenario.content }}</span>
        <!-- <span>Feature: {{ bddScenario.feature }}<br /></span>
        <span>Scenario: {{ bddScenario.scenario }}<br /></span>
        <div style="margin-left: 20px">
          <span>Given {{ bddScenario.given[0] }}<br /></span>
          <span v-for="(given, index) in bddScenario.given.slice(1)" :key="index"
            >And {{ given }}<br
          /></span>
          <span>When {{ bddScenario.when[0] }}<br /></span>
          <span v-for="(when, index) in bddScenario.when.slice(1)" :key="index"
            >And {{ when }}<br
          /></span>
          <span>Then {{ bddScenario.then[0] }}<br /></span>
          <span v-for="(then, index) in bddScenario.then.slice(1)" :key="index"
            >And {{ then }}<br
          /></span>
        </div> -->
      </div>
    </div>
    <div class="actions">
      <button v-if="!allowEdit" class="round-button edit-button" @click="allowEdit = true">
        <span class="material-icons" style="font-size: 20px">edit</span>
      </button>
      <button v-else class="round-button save-button" @click="saveEdited">
        <span class="material-icons" style="font-size: 20px">check</span>
      </button>
      <button class="round-button delete-button" @click="handleDelete">
        <span class="material-icons" style="font-size: 20px">close</span>
      </button>
    </div>
  </div>
  <EditBdd
    :visible="allowEdit"
    :scenario="bddScenario"
    @close="allowEdit = false"
    @save="saveEdited"
  />
</template>

<style scoped>
.bdd-card {
  border: 2px solid #ccc;
  padding: 1rem;
  border-radius: 4px;
  font-size: 12px;
  display: flex;
  gap: 1rem;
  white-space: pre;
}
.actions {
  flex: 1;
  align-self: center;
}
.bdd-text {
  flex: 10;
}
.edit-button {
  margin-bottom: 16px;
}
.save-button {
  margin-bottom: 16px;
  background-color: green;
}
.delete-button {
  background-color: red;
}
</style>
