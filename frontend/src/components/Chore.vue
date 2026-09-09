<script setup>
import { ChevronDown, Edit, EditAlt, Trash } from '@boxicons/vue';
import { ref } from 'vue';

const props = defineProps({
    choreData: {
        type: Object,
        required: true
    },
});

defineEmits(['edit', 'delete']);

const isExpanded = ref(false);

function toggleExpand() {
    isExpanded.value = !isExpanded.value;
}
</script>

<template>
    <div class="chore" :class="{ 'is-expanded': isExpanded }">
        <!-- Clickable Header Area -->
        <div class="chore-main" @click="toggleExpand">
            <div class="chore-info">
                <div class="title-row">
                    <h4>{{ choreData?.name }}</h4>
                    <span class="cadence-badge">{{ choreData?.manual_cadence ?? 'No cadence' }}</span>
                </div>
                
                <!-- Fields rendered as pills -->
                <div class="fields-row" v-if="choreData?.fields?.length">
                    <span 
                        v-for="field in choreData.fields" 
                        :key="field.field_id || field.name" 
                        class="field-pill"
                    >
                        {{ field.name }} <small>({{ field.value_type }})</small>
                    </span>
                </div>
            </div>
        </div>

        <!-- Expandable Action Drawer -->
        <div class="chore-actions">
            <button class="btn-primary" @click="$emit('edit', choreData)">
                <EditAlt size="xs" pack="filled"/> Edit
            </button>
            <button class="btn-outline" @click="$emit('delete', choreData.chore_id)">
                <Trash size="xs" pack="filled"/> Delete
            </button>
        </div>
    </div>
</template>

<style scoped>
.chore {
    border-radius: var(--border-radius-md);
    /* background-color: var(--c-bg-level-1); */
    padding: var(--spacing-sm) 0;
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    /* transition: background-color 0.2s ease; */
}
.chore:hover {
    /* background-color: var(--c-bg-level-2); */
    /* box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); */
}

h4 {
    margin-top: 0;
}

.chore-actions {
    display: flex;
    gap: var(--spacing-sm);
}
</style>