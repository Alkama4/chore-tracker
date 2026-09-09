<script setup lang="ts">
import Chore from '@/components/Chore.vue';
import ChoreForm from '@/components/ChoreForm.vue';
import { queryFastApi } from '@/utils/fastApi';
import type { ChoreRead } from '@/types';
import { Plus } from '@boxicons/vue';
import { ref, onMounted } from 'vue';

const chores = ref<ChoreRead[]>([]);

const isCreating = ref(false);
const editingChoreId = ref<number | null>(null);

async function getChores() {
    const data = await queryFastApi<{ chores?: ChoreRead[] }>('/chore', {
        method: 'GET'
    });

    chores.value = data.chores ?? [];
}

function handleCreate() {
    isCreating.value = true;
    editingChoreId.value = null;
}

function handleEdit(chore: ChoreRead) {
    isCreating.value = false;
    editingChoreId.value = chore.chore_id;
}

function handleCancel() {
    isCreating.value = false;
    editingChoreId.value = null;
}

async function handleSaved() {
    await getChores();
    handleCancel();
}

async function handleDelete(choreId: number) {
    if (!confirm("Are you sure you want to delete this chore?")) {
        return;
    }

    await queryFastApi(`/chore/${choreId}`, {
        method: 'DELETE'
    });

    await getChores();
}

onMounted(getChores);
</script>

<template>
    <div class="chores-page layout-contained">
        <div class="page-header header-margin">
            <h1>Chores</h1>

            <button
                class="btn-primary"
                @click="handleCreate"
                :disabled="isCreating"
            >
                <Plus size="xs" />
                Add New Chore
            </button>
        </div>

        <div>
            
            <div class="chores-wrapper" v-if="chores.length">
                <ChoreForm
                    v-if="isCreating"
                    @saved="handleSaved"
                    @cancel="handleCancel"
                />

                <template
                    v-for="chore in chores"
                    :key="chore.chore_id"
                >
                    <ChoreForm
                        v-if="editingChoreId === chore.chore_id"
                        :chore="chore"
                        @saved="handleSaved"
                        @cancel="handleCancel"
                    />

                    <Chore
                        v-else
                        :chore-data="chore"
                        @edit="handleEdit"
                        @delete="handleDelete"
                    />
                </template>
            </div>

            <div
                v-else-if="!isCreating"
                class="not-found-section"
            >
                <h3>No chores found</h3>

                <div class="flex-row align-center">
                    Use the
                    <span class="badge">+ Add New Chore</span>
                    button to create one.
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h1 {
        margin: 0;
    }
}

.chores-wrapper {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}
</style>