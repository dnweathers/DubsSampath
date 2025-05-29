from typing import Annotated, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, StringConstraints
from app.models.sample import SampleStatus

class SampleBase(BaseModel):
    sample_id: Annotated[
           str, 
           Field(..., description="Unique sample ID"), 
           StringConstraints(min_length=1, pattern=r'^[a-zA-Z0-9_-]+$')
        ]
    
    source: Annotated[
            str, 
            Field(..., description="Source or origin of the sample"),
            StringConstraints(min_length=1)
        ]
    
    status: SampleStatus = Field(..., description="Status of the sample (pending, in-progress, complete)")

    type: Annotated[
            str, 
            Field(..., description="Sample type, e.g., blood, powder, etc."), 
            StringConstraints(min_length=1, pattern=r'^[a-zA-Z]+$')
        ]
    
    assigned_user_id: Optional[UUID] = Field(..., description="Optional UUID of the assigned user")
    
    date_collected: datetime = Field(..., description="Date the sample was collected or received")