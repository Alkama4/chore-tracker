// ---- Enums ----

export enum LogFieldType {
    string = "string",
    float = "float",
    int = "int",
    bool = "bool"
}


// ---- Log Group ----

export interface LogGroupBase {
    name: string;
}

export interface LogGroupCreate extends LogGroupBase {}

export interface LogGroupReplace extends LogGroupBase {}

export interface LogGroupRead extends LogGroupBase {
    group_id: number;
}

export interface LogGroupReadList {
    groups: LogGroupRead[];
}


// ---- Log Field ----

export interface LogFieldBase {
    name: string;
    value_type: LogFieldType;
}

export interface LogFieldCreate extends LogFieldBase {}

export interface LogFieldReplace extends LogFieldBase {
    field_id?: number;
}

export interface LogFieldRead extends LogFieldBase {
    field_id: number;
}


// ---- Log Item ----

export interface LogItemBase {
    group_id: number;
    name: string;
    schedule_rrule?: string | null;
}

export interface LogItemCreate extends LogItemBase {
    fields?: LogFieldCreate[];
}

export interface LogItemReplace extends LogItemBase {
    fields?: LogFieldReplace[];
}

export interface LogItemRead extends LogItemBase {
    item_id: number;
    fields?: LogFieldRead[];
}

export interface LogItemReadList {
    items: LogItemRead[];
}


// ---- Log Entry Value ----

export interface LogEntryValueBase {
    field_id: number;
    value: string;
}

export interface LogEntryValueCreate extends LogEntryValueBase {}

export interface LogEntryValueReplace extends LogEntryValueBase {
    value_id: number;
}

export interface LogEntryValueRead {
    value_id: number;
    field_id: number;
    field: LogFieldRead;
    value: string;
}


// ---- Log Entry ----

export interface LogEntryBase {
    item_id: number;
    logged_at: string; // ISO 8601 datetime string from API
    notes?: string | null;
}

export interface LogEntryCreate extends LogEntryBase {
    field_values?: LogEntryValueCreate[];
}

export interface LogEntryReplace extends LogEntryBase {
    entry_id: number;
    field_values?: LogEntryValueReplace[];
}

export interface LogEntryRead extends LogEntryBase {
    entry_id: number;
    field_values?: LogEntryValueRead[];
}

export interface LogEntryReadList {
    entries: LogEntryRead[];
}


// ---- Generic ----

export interface ConfirmationResponse {
    id: number;
    success: boolean;
    msg: string;
}