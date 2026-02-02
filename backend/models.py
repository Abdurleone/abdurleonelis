from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    dob: Optional[str] = None
    orders: List["LabOrder"] = Relationship(back_populates="patient")


class LabOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    test_name: str
    ordered_at: datetime = Field(default_factory=datetime.utcnow)
    results: List["Result"] = Relationship(back_populates="order")
    patient: Optional[Patient] = Relationship(back_populates="orders")


class Result(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="laborder.id")
    value: str
    measured_at: datetime = Field(default_factory=datetime.utcnow)
    order: Optional[LabOrder] = Relationship(back_populates="results")
