from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models.sample import Sample
from app.schemas.sample_schema import SampleCreate, SampleUpdate
from fastapi import HTTPException, status


def get_sample(db: Session, sample_id: UUID) -> Sample:
    """
    Fetch a single sample by its UUID.

    Raises:
        HTTPException 404 if sample does not exist.
    """
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sample with ID {sample_id} not found"
        )
    
    return sample


def get_samples(db: Session, skip: int = 0, limit: int = 100) -> list[Sample]:
    """
    Return paginated list of samples.
    """
    return db.query(Sample).offset(skip).limit(limit).all()


def create_sample(db: Session, sample: SampleCreate) -> Sample:
    """
    Insert a new sample record.
    """
    db_sample = Sample(
        sample_id=sample.sample_id,
        source=sample.source,
        status=sample.status,
        type=sample.type,
        assigned_user_id=sample.assigned_user_id,
        date_collected=sample.date_collected
    )

    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)

    return db_sample


def update_sample(db: Session, sample_id: UUID, sample_update: SampleUpdate) -> Sample:
    """
    Update sample fields.
    Raises:
        HTTPException 404 if sample does not exist.
    """
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sample with ID {sample_id} not found"
        )
    
    update_data = sample_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sample, key, value)

    db.commit()
    db.refresh(sample)
    
    return sample
    

def delete_sample(db: Session, sample_id: UUID) -> str:
    """
    Delete sample from the database.
    Raises:
        HTTPException 404 if sample does not exist.
    """
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sample with ID {sample_id} not found"
        )
    
    db.delete(sample)
    db.commit()

    return f"Sample with ID {sample_id} successfully deleted."
