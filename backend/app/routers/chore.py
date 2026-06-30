from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models import Chore, ChoreField, ChoreEvent, ChoreEventFieldValue
from app.schemas import (
    ChoreCreate,
    ChoreReplace,
    ChoreRead,
    ChoreReadList,
    ChoreEventCreate,
    ChoreEventReplace,
    ChoreEventRead,
    ConfirmationResponse,
)

router = APIRouter()


@router.get("", response_model=ChoreReadList)
async def get_chores(
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Chore).options(selectinload(Chore.fields))
    result = await db.execute(stmt)
    
    chores = result.scalars().all()
    return {
        "chores": chores
    }


@router.post("", response_model=ChoreRead, status_code=201)
async def create_chore(
    chore: ChoreCreate,
    db: AsyncSession = Depends(get_db)
):
    chore_model = Chore(
        name=chore.name,
        manual_cadence=chore.manual_cadence,
    )
    for field in chore.fields or []:
        chore_model.fields.append(ChoreField(
            name=field.name,
            value_type=field.value_type,
        ))
    db.add(chore_model)
    await db.commit()
    await db.refresh(chore_model, attribute_names=["fields"])

    return chore_model


@router.put("/{chore_id}", response_model=ChoreRead)
async def update_chore(
    chore_id: int,
    chore: ChoreReplace,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Chore).where(Chore.chore_id == chore_id).options(selectinload(Chore.fields))
    result = await db.execute(stmt)
    chore_model = result.scalar_one_or_none()
    if not chore_model:
        raise HTTPException(status_code=404, detail="Chore not found")
    
    chore_model.name = chore.name
    chore_model.manual_cadence = chore.manual_cadence
    
    # Handle fields: update existing, create new, or delete removed
    if chore.fields is not None:
        existing_field_ids = {f.field_id for f in chore_model.fields}
        updated_field_ids = set()
        current_fields = list(chore_model.fields)
        
        for field in chore.fields:
            if hasattr(field, 'field_id') and field.field_id is not None:
                existing = next((f for f in current_fields if f.field_id == field.field_id), None)
                if existing:
                    existing.name = field.name
                    existing.value_type = field.value_type
                    updated_field_ids.add(field.field_id)
            else:
                chore_model.fields.append(ChoreField(
                    name=field.name,
                    value_type=field.value_type,
                ))
        
        for f in current_fields:
            if f.field_id in existing_field_ids and f.field_id not in updated_field_ids:
                chore_model.fields.remove(f)
                await db.delete(f)
    
    await db.commit()
    await db.refresh(chore_model, attribute_names=["fields"])
    return chore_model


@router.delete("/{chore_id}", response_model=ConfirmationResponse)
async def delete_chore(
    chore_id: int,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Chore).where(Chore.chore_id == chore_id).options(selectinload(Chore.fields))
    result = await db.execute(stmt)
    chore_model = result.scalar_one_or_none()
    if not chore_model:
        raise HTTPException(status_code=404, detail="Chore not found")
    
    await db.delete(chore_model)
    await db.commit()

    return {
        "id": chore_id,
        "success": True,
        "msg": "Chore deleted successfully!"
    }



# ---- CHORE EVENTS ENDPOINTS ----

@router.post("/events", response_model=ChoreEventRead, status_code=201)
async def create_chore_event(
    event_data: ChoreEventCreate,
    db: AsyncSession = Depends(get_db)
):
    # 1. Verify the parent chore exists and fetch its valid fields
    stmt = select(Chore).where(Chore.chore_id == event_data.chore_id).options(selectinload(Chore.fields))
    result = await db.execute(stmt)
    chore_model = result.scalar_one_or_none()
    
    if not chore_model:
        raise HTTPException(status_code=404, detail="Parent chore not found")
        
    # 2. Safety check: ensure incoming field_ids belong to this chore
    valid_field_ids = {f.field_id for f in chore_model.fields}
    incoming_field_ids = {fv.field_id for fv in event_data.field_values or []}
    
    if not incoming_field_ids.issubset(valid_field_ids):
        raise HTTPException(
            status_code=400, 
            detail="One or more field_ids do not belong to this specific chore template."
        )

    # 3. Construct the Event
    event_model = ChoreEvent(
        chore_id=event_data.chore_id,
        date=event_data.date,
        notes=event_data.notes
    )
    
    for fv in event_data.field_values or []:
        event_model.field_values.append(
            ChoreEventFieldValue(
                field_id=fv.field_id,
                value=fv.value
            )
        )
        
    db.add(event_model)
    await db.commit()
    
    # Refresh to ensure everything (including nested field schemas) loads up perfectly for response
    stmt_refresh = (
        select(ChoreEvent)
        .where(ChoreEvent.event_id == event_model.event_id)
        .options(
            selectinload(ChoreEvent.field_values)
            .selectinload(ChoreEventFieldValue.field)
        )
    )
    refresh_res = await db.execute(stmt_refresh)
    return refresh_res.scalar_one()


@router.get("/events/{event_id}", response_model=ChoreEventRead)
async def get_chore_event(
    event_id: int,
    db: AsyncSession = Depends(get_db)
):
    # We load field_values AND the matching configuration field definition
    stmt = (
        select(ChoreEvent)
        .where(ChoreEvent.event_id == event_id)
        .options(
            selectinload(ChoreEvent.field_values)
            .selectinload(ChoreEventFieldValue.field)
        )
    )
    result = await db.execute(stmt)
    event_model = result.scalar_one_or_none()
    
    if not event_model:
        raise HTTPException(status_code=404, detail="Chore event log not found")
        
    return event_model


@router.put("/events/{event_id}", response_model=ChoreEventRead)
async def update_chore_event(
    event_id: int,
    event_data: ChoreEventReplace,
    db: AsyncSession = Depends(get_db)
):
    # Fetch the event along with its values and the structural definitions
    stmt = (
        select(ChoreEvent)
        .where(ChoreEvent.event_id == event_id)
        .options(
            selectinload(ChoreEvent.field_values)
            .selectinload(ChoreEventFieldValue.field)
        )
    )
    result = await db.execute(stmt)
    event_model = result.scalar_one_or_none()
    
    if not event_model:
        raise HTTPException(status_code=404, detail="Chore event log not found")
        
    # Update core details
    event_model.date = event_data.date
    event_model.notes = event_data.notes

    # Sync custom field values
    if event_data.field_values is not None:
        current_values = list(event_model.field_values)
        updated_value_ids = set()
        
        for fv in event_data.field_values:
            # If value_id exists, modify the existing entity matching it
            if hasattr(fv, 'value_id') and fv.value_id is not None:
                existing = next((v for v in current_values if v.value_id == fv.value_id), None)
                if existing:
                    existing.value = fv.value
                    updated_value_ids.add(fv.value_id)
            else:
                # If no value_id, append a brand new field value entry
                event_model.field_values.append(
                    ChoreEventFieldValue(
                        field_id=fv.field_id,
                        value=fv.value
                    )
                )
                
        # Clean up values that were omitted from the payload
        for v in current_values:
            if v.value_id not in updated_value_ids:
                event_model.field_values.remove(v)
                await db.delete(v)
                
    await db.commit()
    
    # Reload fresh state
    stmt_refresh = (
        select(ChoreEvent)
        .where(ChoreEvent.event_id == event_id)
        .options(
            selectinload(ChoreEvent.field_values)
            .selectinload(ChoreEventFieldValue.field)
        )
    )
    refresh_res = await db.execute(stmt_refresh)
    return refresh_res.scalar_one()


@router.delete("/events/{event_id}", response_model=ConfirmationResponse)
async def delete_chore_event(
    event_id: int,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(ChoreEvent).where(ChoreEvent.event_id == event_id)
    result = await db.execute(stmt)
    event_model = result.scalar_one_or_none()
    
    if not event_model:
        raise HTTPException(status_code=404, detail="Chore event log not found")
        
    await db.delete(event_model)
    await db.commit()
    
    return {
        "id": event_id,
        "success": True,
        "msg": "Chore event history log deleted successfully!"
    }
