<script setup>
import Chore from '@/components/Chore.vue';
import ChoreForm from '@/components/ChoreForm.vue';
import { fastApi } from '@/utils/fastApi';
import { Plus } from '@boxicons/vue';
import { ref, onMounted } from 'vue';

const chores = ref([]);

const isCreating = ref(false);
const editingChoreId = ref(null);

async function getChores() {
    const data = await fastApi('/chore', {
        method: 'GET'
    });

    chores.value = data.chores ?? [];
}

function handleCreate() {
    isCreating.value = true;
    editingChoreId.value = null;
}

function handleEdit(chore) {
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

async function handleDelete(choreId) {
    if (!confirm("Are you sure you want to delete this chore?")) {
        return;
    }

    await fastApi(`/chore/${choreId}`, {
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

        <div class="card create-chore-card" v-if="isCreating">
            <ChoreForm
                @saved="handleSaved"
                @cancel="handleCancel"
            />
        </div>

        <div class="card">
            <!-- CREATE FORM -->

            <!-- EXISTING CHORES -->
            <div class="chores-wrapper" v-if="chores.length">
                <div
                    v-for="(chore, index) in chores"
                    :key="chore.chore_id"
                    class="chore-wrapper"
                >
                    <hr v-if="index != 0">

                    <!-- EDIT FORM -->
                    <ChoreForm
                        v-if="editingChoreId === chore.chore_id"
                        :chore="chore"
                        @saved="handleSaved"
                        @cancel="handleCancel"
                    />

                    <!-- NORMAL CHORE -->
                    <Chore
                        v-else
                        :chore-data="chore"
                        @edit="handleEdit"
                        @delete="handleDelete"
                    />
                </div>
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

.create-chore-card {
    margin-bottom: var(--spacing-md);
}

.chores-wrapper {
    display: flex;
    flex-direction: column;
    /* gap: var(--spacing-md); */
}
.chore-wrapper hr {
    margin-inline: unset;
}
</style>