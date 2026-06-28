from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models import Chore, ChoreField, ChoreEvent
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
