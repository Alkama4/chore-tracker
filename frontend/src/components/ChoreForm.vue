<script setup lang="ts">
import { computed, reactive } from 'vue';
import { queryFastApi } from '@/utils/fastApi';
import type { ChoreCreate, ChoreFieldCreate, ChoreRead, ChoreReplace } from '@/types';
import { ChoreFieldType } from '@/types';
import { X } from '@boxicons/vue';

const props = defineProps<{ chore?: ChoreRead }>();

const emit = defineEmits<{
    saved: [];
    cancel: [];
}>();

type FormField = ChoreFieldCreate & { field_id?: number };

const isEditing = computed(() => !!props.chore);

const form = reactive<{
    name: string;
    manual_cadence: string;
    fields: FormField[];
}>({
    name: props.chore?.name ?? '',
    manual_cadence: props.chore?.manual_cadence ?? '',
    fields: props.chore?.fields?.map(field => ({
        field_id: field.field_id,
        name: field.name,
        value_type: field.value_type
    })) ?? []
});

function addField() {
    form.fields.push({
        name: '',
        value_type: ChoreFieldType.string
    });
}

function removeField(index: number) {
    form.fields.splice(index, 1);
}

async function handleSubmit() {
    const payload: ChoreCreate = {
        name: form.name,
        manual_cadence: form.manual_cadence || null,
        fields: form.fields.map(({ field_id, ...field }) => field)
    };

    if (isEditing.value) {
        const replacePayload: ChoreReplace = {
            ...payload,
            fields: form.fields.map(({ field_id, ...field }) => ({
                ...field,
                ...(field_id === undefined ? {} : { field_id })
            }))
        };

        await queryFastApi(
            `/chore/${props.chore.chore_id}`,
            {
                method: 'PUT',
                body: replacePayload
            }
        );
    } else {
        await queryFastApi('/chore', {
            method: 'POST',
            body: payload
        });
    }

    emit('saved');
}
</script>

<template>
    <form
        class="chore-form"
        :class="{'editing': isEditing}"
        @submit.prevent="handleSubmit"
    >
        <h3>
            {{ isEditing ? 'Edit Chore' : 'Create Chore' }}
        </h3>

        <div class="form-fields">
            <div class="base-details">
                <label>
                    Chore Name
        
                    <input
                        v-model="form.name"
                        required
                    />
                </label>
        
                <label>
                    Cadence
        
                    <input
                        v-model="form.manual_cadence"
                        placeholder="Every 7 days"
                    />
                </label>
            </div>
    
            <div class="chore-fields-section">
                <h4>Fields</h4>

                <div
                    v-for="(field, index) in form.fields"
                    :key="field.field_id ?? index"
                    class="field-row"
                >
                    <input
                        v-model="field.name"
                        placeholder="Field name"
                        required
                    />
    
                    <select v-model="field.value_type">
                        <option value="string">
                            Text
                        </option>
    
                        <option value="int">
                            Integer
                        </option>
    
                        <option value="float">
                            Decimal
                        </option>
    
                        <option value="bool">
                            Yes / No
                        </option>
                    </select>
    
                    <button
                        type="button"
                        class="btn-text btn-even-padding"
                        @click="removeField(index)"
                    >
                        <X/>
                    </button>
                </div>

                <div v-if="!form.fields.length">
                    The chore currently doesn't have any custom fields.
                </div>

                <button
                    type="button"
                    class="add-field-button"
                    @click="addField"
                >
                    Add Field
                </button>
            </div>
        </div>

        <div class="form-actions">
            <button
                type="submit"
                class="btn-primary"
            >
                {{ isEditing ? 'Save Changes' : 'Create Chore' }}
            </button>

            <button
                type="button"
                class="btn-secondary"
                @click="$emit('cancel')"
            >
                Cancel
            </button>
        </div>
    </form>
</template>

<style scoped>
form {
    box-sizing: border-box;
}
form.editing {
    background-color: var(--c-bg-level-2);
    padding: var(--spacing-md);
    border-radius: var(--border-radius-md);
}

.form-fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
}

label {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    max-width: 400px;
}

.chore-fields-section  {
    .field-row {
        display: flex;
        align-items: center;
        column-gap: var(--spacing-xs);
    }

    input,
    select {
        margin: 0;
    }

    .add-field-button {
        margin-top: var(--spacing-md);
    }
}

.form-actions {
    display: flex;
    gap: var(--spacing-sm);
}
</style>
