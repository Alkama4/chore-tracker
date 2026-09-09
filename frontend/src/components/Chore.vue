<script setup lang="ts">
import { ChevronDown, Clock, Edit, EditAlt, Trash } from '@boxicons/vue';
import { ref } from 'vue';
import type { ChoreRead } from '@/types';

defineProps<{ choreData: ChoreRead }>();

defineEmits<{
    edit: [chore: ChoreRead];
    delete: [choreId: number];
}>();

const isExpanded = ref(false);

function toggleExpand() {
    isExpanded.value = !isExpanded.value;
}
</script>

<template>
    <div class="chore card" :class="{ 'is-expanded': isExpanded }">
        <div class="chore-main" @click="toggleExpand">
            <div class="chore-info">
                <div class="title-row">
                    <h4>{{ choreData?.name }}</h4>
                    <span class="cadence"> <Clock pack="filled" height="12" width="12"/> {{ choreData?.manual_cadence ?? 'No cadence' }}</span>
                </div>
                
                <div class="fields-row" v-if="choreData?.fields?.length">
                    <span 
                        v-for="field in choreData.fields" 
                        :key="field.field_id || field.name" 
                        class="badge"
                    >
                        {{ field.name }} ({{ field.value_type }})
                    </span>
                </div>
            </div>
        </div>

        <div class="chore-actions">
            <button class="btn-text btn-even-padding" @click="$emit('edit', choreData)">
                <EditAlt size="xs" pack="filled"/>
            </button>
            <button class="btn-text btn-even-padding" @click="$emit('delete', choreData.chore_id)">
                <Trash size="xs" pack="filled"/>
            </button>
        </div>
    </div>
</template>

<style scoped>
.chore {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
}

.chore-info {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.title-row {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}
h4 {
    margin: 0;
}
.cadence {
    margin-left: var(--spacing-sm);
    color: var(--c-text-subtle);
    font-size: var(--fs-neg-1);
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}

.fields-row {
    display: flex;
    gap: var(--spacing-sm);
}

.chore-actions {
    opacity: 0.4;
    transition: opacity 0.1s ease-out;
}
.chore:hover .chore-actions {
    opacity: 1;
}
</style>