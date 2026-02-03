from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlmodel import SQLModel, Session, select
from typing import List
from models import Patient, LabOrder, Result, User
from database import engine, get_session
from auth import router as auth_router, get_current_user, require_role
from schemas import PatientCreate, PatientResponse, LabOrderCreate, LabOrderResponse, ResultCreate, ResultResponse

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Create database tables on startup
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="LIS - Lab Information System", lifespan=lifespan)
app.include_router(auth_router)


# Patients
@app.post("/patients/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, current_user: User = Depends(require_role("admin", "technician")), session: Session = Depends(get_session)):
    with session:
        db_patient = Patient(**patient.model_dump())
        session.add(db_patient)
        session.commit()
        session.refresh(db_patient)
        return db_patient


@app.get("/patients/", response_model=List[PatientResponse])
def list_patients(session: Session = Depends(get_session)):
    with session:
        return session.exec(select(Patient)).all()


@app.get("/patients/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, session: Session = Depends(get_session)):
    with session:
        patient = session.get(Patient, patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient


# Lab orders
@app.post("/orders/", response_model=LabOrderResponse)
def create_order(order: LabOrderCreate, current_user: User = Depends(require_role("admin", "technician")), session: Session = Depends(get_session)):
    with session:
        # Verify patient exists
        patient = session.get(Patient, order.patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        db_order = LabOrder(**order.model_dump())
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order


@app.get("/orders/", response_model=List[LabOrderResponse])
def list_orders(session: Session = Depends(get_session)):
    with session:
        return session.exec(select(LabOrder)).all()


# Results
@app.post("/results/", response_model=ResultResponse)
def create_result(result: ResultCreate, current_user: User = Depends(require_role("admin", "technician")), session: Session = Depends(get_session)):
    with session:
        db_result = Result(**result.model_dump())
        session.add(db_result)
        session.commit()
        session.refresh(db_result)
        return db_result


@app.get("/results/", response_model=List[ResultResponse])
def list_results(session: Session = Depends(get_session)):
    with session:
        return session.exec(select(Result)).all()
