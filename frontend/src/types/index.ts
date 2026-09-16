// ---- Enums ----

export enum ChoreFieldType {
    string = "string",
    float = "float",
    int = "int",
    bool = "bool"
}


// ---- Chore Field ----

export interface ChoreFieldBase {
    name: string;
    value_type: ChoreFieldType;
}

export interface ChoreFieldCreate extends ChoreFieldBase {}

export interface ChoreFieldReplace extends ChoreFieldBase {
    field_id?: number;
}

export interface ChoreFieldRead extends ChoreFieldBase {
    field_id: number;
}


// ---- Chore ----

export interface ChoreBase {
    name: string;
    manual_cadence?: string | null;
}

export interface ChoreCreate extends ChoreBase {
    fields?: ChoreFieldCreate[];
}

export interface ChoreReplace extends ChoreBase {
    fields?: ChoreFieldReplace[];
}

export interface ChoreRead extends ChoreBase {
    chore_id: number;
    fields?: ChoreFieldRead[];
}

export interface ChoreReadList {
    chores?: ChoreRead[];
}


// ---- Chore Event Field ----

export interface ChoreEventFieldBase {
    field_id: number;
    value: string;
}

export interface ChoreEventFieldCreate extends ChoreEventFieldBase {}

export interface ChoreEventFieldReplace extends ChoreEventFieldBase {
    value_id: number;
}

export interface ChoreEventFieldRead extends ChoreEventFieldBase {
    field: ChoreFieldRead;
    value_id: number;
}


// ---- Chore Event ----

export interface ChoreEventBase {
    chore_id: number;
    date: string; // ISO Date strings from API (e.g. "2026-08-15")
    notes?: string | null;
}

export interface ChoreEventCreate extends ChoreEventBase {
    field_values?: ChoreEventFieldCreate[];
}

export interface ChoreEventReplace extends ChoreEventBase {
    event_id: number;
    field_values?: ChoreEventFieldReplace[];
}

export interface ChoreEventRead extends ChoreEventBase {
    event_id: number;
    field_values?: ChoreEventFieldRead[];
}


// ---- Generic ----

export interface ConfirmationResponse {
    id: number;
    success: boolean;
    msg: string;
}
