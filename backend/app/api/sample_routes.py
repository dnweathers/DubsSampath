from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import sample_schema
from app.crud import sample_crud
from app.db.database import get_db

router = APIRouter(prefix="/samples", tags=["Samples"])

@router.get("/", response_model=list[sample_schema.SampleRead])
def read_samples(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return sample_crud.get_samples(db, skip=skip, limit=limit)

@router.get("/{sample_id}", response_model=sample_schema.SampleRead)
def read_sample(sample_id: UUID, db: Session = Depends(get_db)):
    db_sample = sample_crud.get_sample(db, sample_id)
    if db_sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")
    return db_sample

@router.post("/", response_model=sample_schema.SampleRead, status_code=201)
def create_sample(sample: sample_schema.SampleCreate, db: Session = Depends(get_db)):
    return sample_crud.create_sample(db, sample)

@router.put("/{sample_id}", response_model=sample_schema.SampleRead)
def update_sample(sample_id: UUID, sample_update: sample_schema.SampleUpdate, db: Session = Depends(get_db)):
    db_sample = sample_crud.update_sample(db, sample_id, sample_update)
    if db_sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")
    return db_sample

@router.delete("/{sample_id}", status_code=204)
def delete_sample(sample_id: UUID, db: Session = Depends(get_db)):
    result = sample_crud.delete_sample(db, sample_id)
    if not result:
        raise HTTPException(status_code=404, detail="Sample not found")
    return None