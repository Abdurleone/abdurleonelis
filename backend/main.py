from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from typing import List
from models import Patient, LabOrder, Result, User
from database import engine
from auth import router as auth_router, get_current_user, require_role
from schemas import PatientCreate, PatientResponse, LabOrderCreate, LabOrderResponse, ResultCreate, ResultResponse

app = FastAPI(title="LIS - Lab Information System")
app.include_router(auth_router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# Patients
@app.post("/patients/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, current_user: User = Depends(require_role("admin", "technician"))):
    with Session(engine) as session:
        db_patient = Patient(**patient.dict())
        session.add(db_patient)
        session.commit()
        session.refresh(db_patient)
        return db_patient


@app.get("/patients/", response_model=List[PatientResponse])
def list_patients():
    with Session(engine) as session:
        return session.exec(select(Patient)).all()


@app.get("/patients/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int):
    with Session(engine) as session:
        patient = session.get(Patient, patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient


# Lab orders
@app.post("/orders/", response_model=LabOrderResponse)
def create_order(order: LabOrderCreate, current_user: User = Depends(require_role("admin", "technician"))):
    with Session(engine) as session:
        db_order = LabOrder(**order.dict())
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order


@app.get("/orders/", response_model=List[LabOrderResponse])
def list_orders():
    with Session(engine) as session:
        return session.exec(select(LabOrder)).all()


# Results
@app.post("/results/", response_model=ResultResponse)
def create_result(result: ResultCreate, current_user: User = Depends(require_role("admin", "technician"))):
    with Session(engine) as session:
        db_result = Result(**result.dict())
        session.add(db_result)
        session.commit()
        session.refresh(db_result)
        return db_result


@app.get("/results/", response_model=List[ResultResponse])
def list_results():
    with Session(engine) as session:
        return session.exec(select(Result)).all()
