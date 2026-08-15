<script setup>
import { queryFastApi } from '@/utils/fastApi';
import { onMounted, ref } from 'vue';

const chores = ref([]);

async function getChores() {
    const response = await queryFastApi('/chore');
    chores.value = response.chores;
}

onMounted(() => {
    getChores();
})
</script>

<template>
    <div class="chores-page">
        <h1>Chores</h1>
        <button @click="getChores">Click</button>
        <div class="chores-wrapper">
            <div v-for="chore in chores" class="chore">
                {{ chore }}
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
