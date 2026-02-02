from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PatientCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    dob: Optional[str] = Field(None, description="Date of birth")


class PatientResponse(PatientCreate):
    id: int


class LabOrderCreate(BaseModel):
    patient_id: int = Field(..., gt=0)
    test_name: str = Field(..., min_length=1, max_length=200)


class LabOrderResponse(LabOrderCreate):
    id: int
    ordered_at: datetime


class ResultCreate(BaseModel):
    order_id: int = Field(..., gt=0)
    value: str = Field(..., min_length=1, max_length=1000)


class ResultResponse(ResultCreate):
    id: int
    measured_at: datetime
