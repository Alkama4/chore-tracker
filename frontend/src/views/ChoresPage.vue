<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { ChoreRead } from '@/types';
import { queryFastApi } from '@/utils/fastApi';

const chores = ref<ChoreRead[]>([]);

async function getChores() {
    const data = await queryFastApi<{ chores: ChoreRead[] }>("/chore");
    chores.value = data.chores ?? [];
}

onMounted(() => {
    getChores();
});
</script>

<template>
    <div class="chores-page layout-contained">
        <h1>Chores</h1>
        <button @click="getChores">Click</button>
        <div class="chores-wrapper">
            <div v-for="chore in chores" :key="chore.chore_id">
                <h3>{{ chore.name }}</h3>
                <p v-if="chore.manual_cadence">Cadence: {{ chore.manual_cadence }}</p>
                <div v-for="field in chore.fields">
                    {{ field.field_id }} | {{ field.name }} | {{ field.value_type }}
                </div>
            </div>
            <div v-if="chores.length === 0">
                No chores found
            </div>
        </div>
    </div>
</template>

<style scoped>
.chores-wrapper {
    display: flex;
    flex-direction: column;
}
</style>
