import pytest
from datetime import datetime, timezone
from uuid import uuid4
from pydantic import ValidationError
from app.schemas.sample_schema import SampleBase
from app.models.sample import SampleStatus

def test_samplebase_valid_data():
    valid_data = {
        "sample_id": "SAMPLE123",
        "source": "LabA",
        "status": SampleStatus.pending,
        "type": "blood",
        "assigned_user_id": uuid4(),
        "date_collected": datetime.now()
    }

    sample = SampleBase(**valid_data)
    assert sample.sample_id == valid_data["sample_id"]
    assert sample.status == SampleStatus.pending

def test_samplebase_missing_required_field():
    invalid_data = {
        "sample_id": "SAMPLE123",
        "source": "LabA",
        # missing "status"
        "type": "blood",
        "date_collected": datetime.now(timezone.utc)
    }

    with pytest.raises(ValidationError):
        SampleBase(**invalid_data)

def test_samplebase_invalid_sample_id_pattern():
    invalid_data = {
        "sample_id": "Invalid Sample!",  # spaces and punctuation not allowed by regex
        "source": "LabA",
        "status": SampleStatus.pending,
        "type": "blood",
        "date_collected": datetime.now()
    }
    with pytest.raises(ValidationError):
        SampleBase(**invalid_data)