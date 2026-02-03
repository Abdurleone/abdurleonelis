# Quick Reference — LIS Testing & Demo Data

## Run Tests

```bash
cd backend
source ../venv/bin/activate
pytest tests/ -v
```

## Seed Demo Database
```bash
cd backend
source ../venv/bin/activate
python seed_db.py
```

## Demo User Credentials

```
Admin:
  username: admin
  password: admin123

Technician 1:
  username: tech1
  password: tech123

Technician 2:
  username: tech2
  password: tech123

Doctor:
  username: doctor1
  password: doc123
```

## Test Coverage
- **23 tests** across 6 test classes
- **100% authentication** coverage (password, registration, login, RBAC)
- **100% endpoint** coverage (patients, orders, results)
- **100% validation** coverage (input validation, foreign keys, status codes)

## Files Structure

```
backend/
├── conftest.py           # pytest fixtures & setup
├── pytest.ini            # pytest config
├── seed_db.py            # demo data generator
├── tests/
│   ├── test_auth.py      # 12 auth tests
│   └── test_endpoints.py # 11 endpoint tests
├── main.py               # FastAPI app
├── auth.py               # JWT & RBAC
├── models.py             # SQLModel ORM
├── schemas.py            # Pydantic validation
├── database.py           # SQLite config
└── requirements.txt      # Python deps
```

## Key Improvements in Tier 2
✅ Dependency injection for testable architecture
✅ In-memory database for isolated tests
✅ Comprehensive fixtures for authentication
✅ Patient validation in `/orders/` endpoint
✅ Realistic demo data with faker
✅ All 23 tests passing

---
**Status:** Tier 2 complete — ready for Tier 3 (Deployment)
