from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, select
from typing import List
from models import Patient, LabOrder, Result
from database import engine

app = FastAPI(title="LIS - Lab Information System")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# Patients
@app.post("/patients/", response_model=Patient)
def create_patient(patient: Patient):
    with Session(engine) as session:
        session.add(patient)
        session.commit()
        session.refresh(patient)
        return patient


@app.get("/patients/", response_model=List[Patient])
def list_patients():
    with Session(engine) as session:
        return session.exec(select(Patient)).all()


@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    with Session(engine) as session:
        patient = session.get(Patient, patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient


# Lab orders
@app.post("/orders/", response_model=LabOrder)
def create_order(order: LabOrder):
    with Session(engine) as session:
        session.add(order)
        session.commit()
        session.refresh(order)
        return order


@app.get("/orders/", response_model=List[LabOrder])
def list_orders():
    with Session(engine) as session:
        return session.exec(select(LabOrder)).all()


# Results
@app.post("/results/", response_model=Result)
def create_result(result: Result):
    with Session(engine) as session:
        session.add(result)
        session.commit()
        session.refresh(result)
        return result


@app.get("/results/", response_model=List[Result])
def list_results():
    with Session(engine) as session:
        return session.exec(select(Result)).all()
