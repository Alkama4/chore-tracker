<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { type ChoreRead, type ChoreReplace, type ChoreCreate, type ChoreFieldReplace, ChoreFieldType } from '@/types';
import { queryFastApi } from '@/utils/fastApi';
import { Edit, Trash } from '@boxicons/vue';

const chores = ref<ChoreRead[]>([]);

// Edit State
const editingId = ref<number | null>(null);
const draftChore = ref<ChoreReplace | null>(null);

// Create State
const showCreateForm = ref(false);
const newChore = ref<ChoreCreate>({ name: '', manual_cadence: null, fields: [] });

async function getChores() {
    const data = await queryFastApi<{ chores: ChoreRead[] }>("/chore");
    chores.value = data.chores ?? [];
}

// --- CREATE ACTIONS ---
function addFieldToNew() {
    newChore.value.fields?.push({ name: '', value_type: ChoreFieldType.string });
}

function removeFieldFromNew(index: number) {
    newChore.value.fields?.splice(index, 1);
}

async function saveNewChore() {
    await queryFastApi("/chore", {
        method: "POST",
        body: JSON.stringify(newChore.value)
    });
    showCreateForm.value = false;
    newChore.value = { name: '', manual_cadence: null, fields: [] };
    await getChores();
}

// --- EDIT ACTIONS ---
function startEdit(chore: ChoreRead) {
    editingId.value = chore.chore_id;
    // Deep clone to avoid reactive mutation before saving
    draftChore.value = JSON.parse(JSON.stringify(chore));
}

function cancelEdit() {
    editingId.value = null;
    draftChore.value = null;
}

function addFieldToDraft() {
    // Note: Your OpenAPI spec requires a `field_id` for ChoreFieldReplace. 
    // Sending 0 or -1 usually indicates a "new" field to the backend during a PUT request.
    draftChore.value?.fields?.push({ name: '', value_type: ChoreFieldType.string, field_id: 0 });
}

function removeFieldFromDraft(index: number) {
    draftChore.value?.fields?.splice(index, 1);
}

async function saveEdit() {
    if (!draftChore.value || editingId.value === null) return;
    
    await queryFastApi(`/chore/${editingId.value}`, {
        method: "PUT",
        body: JSON.stringify(draftChore.value)
    });
    
    cancelEdit();
    await getChores();
}

async function deleteChore(id: number) {
    if(!confirm("Are you sure you want to delete this chore?")) return;
    await queryFastApi(`/chore/${id}`, { method: "DELETE" });
    await getChores();
}

onMounted(() => {
    getChores();
});
</script>

<template>
    <div class="chores-page layout-contained">
        <div class="header-actions">
            <h1>Chores</h1>
            <button @click="showCreateForm = !showCreateForm" class="btn btn-primary">
                {{ showCreateForm ? 'Cancel New Chore' : '+ Add Chore' }}
            </button>
        </div>

        <div class="chores-wrapper">
            
            <!-- CREATE NEW CHORE INLINE FORM -->
            <div v-if="showCreateForm" class="card create-card">
                <h3>Create New Chore</h3>
                <input v-model="newChore.name" placeholder="Chore Name" />
                <input v-model="newChore.manual_cadence" placeholder="Cadence (e.g., Weekly)" />
                
                <div class="fields-edit-wrapper">
                    <h4>Fields</h4>
                    <div v-for="(field, index) in newChore.fields" :key="index" class="field-row">
                        <input v-model="field.name" placeholder="Field Name" />
                        <select v-model="field.value_type">
                            <option v-for="t in ChoreFieldType" :value="t">{{ t }}</option>
                        </select>
                        <button @click="removeFieldFromNew(index)">X</button>
                    </div>
                    <button @click="addFieldToNew" class="btn-text">+ Add Field</button>
                </div>
                
                <div class="card-actions">
                    <button @click="saveNewChore" class="btn btn-primary">Save Chore</button>
                </div>
            </div>

            <!-- CHORES LIST -->
            <div v-for="chore in chores" :key="chore.chore_id" class="card">
                
                <!-- EDIT MODE -->
                <div v-if="editingId === chore.chore_id && draftChore">
                    <input v-model="draftChore.name" placeholder="Chore Name" class="edit-input" />
                    <input v-model="draftChore.manual_cadence" placeholder="Cadence (optional)" class="edit-input" />
                    
                    <hr>
                    <div class="fields-edit-wrapper">
                        <h4>Fields</h4>
                        <div v-for="(field, index) in draftChore.fields" :key="index" class="field-row">
                            <input v-model="field.name" placeholder="Field Name" />
                            <select v-model="field.value_type">
                                <option v-for="t in ChoreFieldType" :value="t">{{ t }}</option>
                            </select>
                            <button @click="removeFieldFromDraft(index)">X</button>
                        </div>
                        <button @click="addFieldToDraft" class="btn-text">+ Add Field</button>
                    </div>

                    <div class="card-actions">
                        <button @click="saveEdit" class="btn btn-primary">Save</button>
                        <button @click="cancelEdit" class="btn btn-secondary">Cancel</button>
                    </div>
                </div>

                <!-- VIEW MODE -->
                <div v-else>
                    <div class="card-header">
                        <div class="header-wrapper">
                            <h4 class="name">{{ chore.name }}</h4>
                            <span class="badge" :class="{ 'badge-primary': chore.manual_cadence }">
                                {{ chore.manual_cadence || 'Automatic cadence' }}
                            </span>
                        </div>
                        <div>
                            <button @click="startEdit(chore)" class="btn-text">
                                <Edit pack="filled" size="sm"/>
                                <span>Edit</span>
                            </button>
                            <button @click="deleteChore(chore.chore_id)" class="btn-text">
                                <Trash pack="filled" size="sm"/>
                                <span>Delete</span>
                            </button>
                        </div>
                    </div>
                    <hr>
                    <div class="fields-wrapper">
                        <div v-for="field in chore.fields" :key="field.field_id" class="field-display">
                            <strong>{{ field.name }}</strong> ({{ field.value_type }})
                        </div>
                        <div v-if="!chore.fields?.length" class="text-muted">No fields assigned.</div>
                    </div>
                </div>

            </div>

            <div v-if="chores.length === 0 && !showCreateForm" class="empty-state">
                No chores found
            </div>
        </div>
    </div>
</template>

<style scoped>
.header-actions,
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.chores-wrapper {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}
h4.name {
    margin-top: 0;
    margin-bottom: var(--spacing-sm);
}
</style>
