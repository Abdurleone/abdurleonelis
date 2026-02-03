#!/usr/bin/env python3
"""
Seed the database with demo data for manual testing.

Usage:
  python seed_db.py
"""

from sqlmodel import Session, create_engine
from faker import Faker
from models import Patient, LabOrder, Result, User
from auth import get_password_hash
from database import engine
from datetime import datetime, timedelta, timezone
import random

fake = Faker()


def seed_users():
    """Create demo users."""
    with Session(engine) as session:
        users = [
            User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                role="admin"
            ),
            User(
                username="tech1",
                hashed_password=get_password_hash("tech123"),
                role="technician"
            ),
            User(
                username="tech2",
                hashed_password=get_password_hash("tech123"),
                role="technician"
            ),
            User(
                username="doctor1",
                hashed_password=get_password_hash("doc123"),
                role="doctor"
            ),
        ]
        for user in users:
            session.add(user)
        session.commit()
        print(f"✓ Created {len(users)} users")


def seed_patients(count=10):
    """Create demo patients."""
    with Session(engine) as session:
        patients = []
        for _ in range(count):
            patient = Patient(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                dob=fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat()
            )
            patients.append(patient)
            session.add(patient)
        session.commit()
        print(f"✓ Created {len(patients)} patients")
        return session.query(Patient).all()


def seed_orders(patients, count_per_patient=2):
    """Create demo lab orders."""
    test_names = [
        "Blood Test (CBC)",
        "Glucose Test",
        "Cholesterol Panel",
        "Liver Function Test",
        "Kidney Function Test",
        "Thyroid Test (TSH)",
        "Urinalysis",
        "Lipid Panel"
    ]
    
    with Session(engine) as session:
        orders = []
        for patient in patients:
            for _ in range(random.randint(1, count_per_patient)):
                order = LabOrder(
                    patient_id=patient.id,
                    test_name=random.choice(test_names),
                    ordered_at=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))
                )
                orders.append(order)
                session.add(order)
        session.commit()
        print(f"✓ Created {len(orders)} lab orders")
        return session.query(LabOrder).all()


def seed_results(orders, result_rate=0.7):
    """Create demo test results for some orders."""
    result_values = ["Normal", "Abnormal", "Borderline", "Pending Review"]
    
    with Session(engine) as session:
        results = []
        for order in orders:
            if random.random() < result_rate:
                result = Result(
                    order_id=order.id,
                    value=random.choice(result_values),
                    measured_at=order.ordered_at + timedelta(days=random.randint(1, 7))
                )
                results.append(result)
                session.add(result)
        session.commit()
        print(f"✓ Created {len(results)} test results")


def main():
    """Seed the database."""
    print("🌱 Seeding database with demo data...\n")
    
    seed_users()
    patients = seed_patients(count=5)
    orders = seed_orders(patients, count_per_patient=3)
    seed_results(orders, result_rate=0.8)
    
    print("\n✅ Database seeding complete!")
    print("\nDemo users:")
    print("  - admin / admin123 (role: admin)")
    print("  - tech1 / tech123 (role: technician)")
    print("  - tech2 / tech123 (role: technician)")
    print("  - doctor1 / doc123 (role: doctor)")


if __name__ == "__main__":
    main()
