from typing import Annotated, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, StringConstraints
from app.models.sample import SampleStatus

alphanumeric_str = Annotated[str, StringConstraints(min_length=1, pattern=r'^[a-zA-Z0-9_-]+$')]
alpha_str = Annotated[str, StringConstraints(min_length=1, pattern=r'^[a-zA-Z]+$')]
nonempty_str = Annotated[str, StringConstraints(min_length=1)]

class SampleBase(BaseModel):
    sample_id: alphanumeric_str = Field(description="Unique sample ID")
    
    source: nonempty_str = Field(description="Source or origin of the sample")
    
    status: SampleStatus = Field(description="Status of the sample (pending, in-progress, complete)")

    type: alpha_str = Field(description="Sample type, e.g., blood, powder, etc.")
    
    assigned_user_id: Optional[UUID] = Field(None, description="Optional UUID of the assigned user")
    
    date_collected: datetime = Field(description="Date the sample was collected or received")

class SampleCreate(SampleBase):
    pass

class SampleUpdate(SampleBase):
    sample_id: Optional[alphanumeric_str] = Field(None, description="Unique sample ID")
    
    source: Optional[nonempty_str] = Field(None, description="Source or origin of the sample")
    
    status: Optional[SampleStatus] = Field(None, description="Status of the sample (pending, in-progress, complete)")

    type: Optional[alpha_str] = Field(None, description="Sample type, e.g., blood, powder, etc.")
    
    assigned_user_id: Optional[UUID] = Field(None, description="Optional UUID of the assigned user")
    
    date_collected: Optional[datetime] = Field(None, description="Date the sample was collected or received")

class SampleRead(SampleBase):
    id: UUID = Field(description="Primary key id")

    created_at: datetime = Field(description="Time sample was created")

    updated_at: datetime = Field(description="Most recent time sample was updated")