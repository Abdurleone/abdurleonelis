# abdurleonelis — Laboratory Information System (LIS)

A small-scale Laboratory Information System (LIS) prototype built with FastAPI and SQLModel. Provides patient management, lab order tracking, and test result recording with JWT-based authentication and role-based access control.

## Features

- **Patient Management** — Register and manage patient records with DOB tracking.
- **Lab Orders** — Create and track laboratory test orders for patients.
- **Test Results** — Record and retrieve lab test results linked to orders.
- **JWT Authentication** — Secure token-based API access with OAuth2 flow.
- **Role-Based Access Control (RBAC)** — Three roles: `admin`, `technician`, `doctor`.
  - `admin` / `technician`: Can create patients, orders, results.
  - `doctor`: Read-only access (future enhancement).
- **Input Validation** — Pydantic schemas validate all request payloads.
- **SQLite Database** — Simple local persistence; easily swappable for PostgreSQL.

## Tech Stack

- **Backend:** FastAPI, Uvicorn, SQLModel (ORM)
- **Database:** SQLite (development)
- **Authentication:** python-jose (JWT), passlib (password hashing)
- **Validation:** Pydantic

## Project Structure

```
backend/
├── main.py           # FastAPI app & route handlers
├── models.py         # SQLModel ORM models (Patient, LabOrder, Result, User)
├── schemas.py        # Pydantic validation schemas
├── auth.py           # JWT & RBAC logic
├── database.py       # SQLite engine config
├── requirements.txt  # Python dependencies
└── Dockerfile        # Container image definition

docker-compose.yml    # Multi-container orchestration
.gitignore            # Git exclusions (*.pyc, lab.db, etc.)
README.md             # This file
```

## Quick Start

### Prerequisites

- Python 3.11+
- pip / venv
- (Optional) Docker & Docker Compose

### Local Setup

1. **Clone and navigate:**

```bash
cd /root/abdurleonelis
```

2. **Create virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
cd backend
pip install -r requirements.txt
```

4. **Run the backend:**

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

5. **Open API docs:**

```
http://localhost:8000/docs
```

Use the Swagger UI to test endpoints interactively.

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register a new user | None |
| POST | `/auth/token` | Login and get JWT token | None |

### Patients

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/patients/` | Create a patient | admin, technician |
| GET | `/patients/` | List all patients | None |
| GET | `/patients/{id}` | Get patient by ID | None |

### Lab Orders

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/orders/` | Create a lab order | admin, technician |
| GET | `/orders/` | List all orders | None |

### Results

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/results/` | Create a test result | admin, technician |
| GET | `/results/` | List all results | None |

## Authentication Flow

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "lab_tech",
    "password": "secure_pass123",
    "role": "technician"
  }'
```

Response:
```json
{
  "username": "lab_tech",
  "id": 1,
  "role": "technician"
}
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=lab_tech&password=secure_pass123"
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 3. Use Token in Protected Endpoints

```bash
TOKEN="<access_token_from_login>"

curl -X POST "http://localhost:8000/patients/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "dob": "1990-01-15"
  }'
```

## Configuration

Update settings in `backend/auth.py`:

```python
SECRET_KEY = "change-this-secret"  # Change in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
```

In production, use environment variables:

```bash
export SECRET_KEY="your-secure-key"
export DATABASE_URL="postgresql://user:pass@host/db"
```

## Running with Docker

Build and run:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## Testing

### Example: Create Patient, Order, Result

```bash
# Register technician
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"tech1","password":"pass123","role":"technician"}'

# Login
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=tech1&password=pass123" | jq -r .access_token)

# Create patient
PATIENT_ID=$(curl -s -X POST "http://localhost:8000/patients/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Smith","dob":"1985-06-20"}' | jq -r .id)

# Create lab order
ORDER_ID=$(curl -s -X POST "http://localhost:8000/orders/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"patient_id\":$PATIENT_ID,\"test_name\":\"Blood Test\"}" | jq -r .id)

# Add result
curl -s -X POST "http://localhost:8000/results/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"order_id\":$ORDER_ID,\"value\":\"Normal\"}"

# List results
curl -s -X GET "http://localhost:8000/results/" | jq .
```

## Tier 2: Testing & Quality Assurance

### Test Infrastructure

The project includes comprehensive test coverage with **pytest**, **fixtures**, and an **in-memory SQLite database** for isolated testing.

**Files:**
- `tests/test_auth.py` — Authentication and RBAC tests (12 tests)
- `tests/test_endpoints.py` — Integration tests for endpoints (11 tests)
- `conftest.py` — pytest fixtures for database and authentication
- `pytest.ini` — pytest configuration

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests with verbose output
cd backend
pytest tests/ -v

# Run specific test class
pytest tests/test_auth.py::TestAuth -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage

- **TestPasswordHashing** (3 tests)
  - ✅ Password hashing creates different salts
  - ✅ Verify correct password
  - ✅ Reject incorrect password

- **TestAuth** (5 tests)
  - ✅ User registration
  - ✅ Reject duplicate usernames
  - ✅ Login with correct credentials
  - ✅ Reject incorrect credentials
  - ✅ Reject nonexistent user

- **TestRBAC** (4 tests)
  - ✅ Protected endpoints require token (401 Unauthorized)
  - ✅ Technician can create patients
  - ✅ Admin can create patients
  - ✅ Invalid tokens rejected

- **TestPatients** (4 tests)
  - ✅ Create patient with auth
  - ✅ Validate required fields
  - ✅ List patients after create
  - ✅ Get patient by ID

- **TestLabOrders** (3 tests)
  - ✅ Create order with auth
  - ✅ Reject invalid patient ID
  - ✅ List orders

- **TestResults** (1 test)
  - ✅ Create result with auth

**Total: 23 tests — all passing ✅**

### Seeding Demo Data

Populate the database with realistic demo data using the seeder script:

```bash
cd backend
python seed_db.py
```

Creates:
- **4 users** with different roles
  - `admin` / `admin123` (role: admin)
  - `tech1` / `tech123` (role: technician)
  - `tech2` / `tech123` (role: technician)
  - `doctor1` / `doc123` (role: doctor)
- **5 patients** with realistic names and DOBs
- **15 lab orders** distributed across patients
- **12 test results** with realistic test values

Use these demo credentials to test the API and frontend.

## Tier 3: Deployment & Infrastructure

### Docker Setup

The project is fully containerized with Docker and includes orchestration via Docker Compose.

**Components:**
- **PostgreSQL 15** — Production-grade database with persistent volumes
- **FastAPI Backend** — Multi-stage Docker build with health checks
- **React Frontend** — Nginx-served SPA with static caching
- **Docker Compose** — Orchestrates all services with networking and environment variables

### Environment Configuration

1. **Copy environment template:**

```bash
cp .env.example .env
```

2. **Edit `.env` with your values:**

```bash
# Database
DATABASE_URL=postgresql://lis_user:lis_secure_password@postgres:5432/lis_db
POSTGRES_USER=lis_user
POSTGRES_PASSWORD=lis_secure_password

# Backend
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Frontend
VITE_API_URL=http://localhost:3000/api
```

⚠️ **Security:** Change `SECRET_KEY` and `POSTGRES_PASSWORD` to strong, random values in production.

### Running with Docker Compose

**Development (with auto-reload):**

```bash
docker-compose up
```

Access the application:
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **PostgreSQL:** localhost:5432

**Production (optimized builds):**

```bash
docker-compose -f docker-compose.yml build
docker-compose up -d
```

**View logs:**

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Stop services:**

```bash
docker-compose down
```

### Database Initialization

When using PostgreSQL, tables are created automatically on first startup. To seed demo data in a running container:

```bash
docker-compose exec backend python seed_db.py
```

### Building Individual Docker Images

**Backend only:**

```bash
docker build -t lis-backend:latest ./backend
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  lis-backend:latest
```

**Frontend only:**

```bash
docker build -t lis-frontend:latest ./frontend
docker run -p 3000:3000 lis-frontend:latest
```

### CI/CD Pipeline

GitHub Actions automatically:
- ✅ Run backend tests on every push
- ✅ Lint Python and Node.js code
- ✅ Build Docker images
- ✅ Push images to GitHub Container Registry
- ✅ Run security scans (Trivy)

**Workflow files:** `.github/workflows/ci-cd.yml`

**Triggered on:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### Deployment Strategies

#### Option 1: Local Docker Compose (Development)
```bash
docker-compose up --build
```

#### Option 2: Kubernetes (Production)
- Export images to Kubernetes-compatible format
- Use Helm charts for templating
- Configure persistent volumes for PostgreSQL
- Set up ingress for traffic routing

#### Option 3: Cloud Platforms (AWS/GCP/Azure)
1. Push images to container registry (ECR, GCR, ACR)
2. Deploy via ECS, Cloud Run, or AKS
3. Configure managed PostgreSQL (RDS, Cloud SQL, etc.)
4. Set up CDN for frontend static assets

### Production Checklist

- ☐ Change `SECRET_KEY` to a cryptographically secure random string
- ☐ Change all default passwords (PostgreSQL, etc.)
- ☐ Enable HTTPS/TLS (use Let's Encrypt with Nginx/reverse proxy)
- ☐ Configure PostgreSQL backups and replication
- ☐ Set up monitoring (Prometheus, Grafana) and alerting
- ☐ Enable audit logging for compliance
- ☐ Configure rate limiting to prevent abuse
- ☐ Set up log aggregation (ELK Stack, Datadog, etc.)
- ☐ Test disaster recovery and backup restoration
- ☐ Configure auto-scaling for load handling

### Troubleshooting

**Port already in use:**
```bash
# Change port in .env or docker-compose.yml
docker-compose up -p 8080
```

**Database connection refused:**
```bash
# Wait for PostgreSQL to start
docker-compose logs postgres
docker-compose restart postgres
```

**Frontend not connecting to API:**
Check `VITE_API_URL` in .env matches your backend URL

**Permission denied on volumes:**
```bash
sudo chown -R $USER:$USER ./backend ./frontend
```

## Next Steps

- **Monitoring & Observability:** Add Prometheus metrics and Grafana dashboards
- **Audit Logging:** Track all sensitive operations for compliance
- **Advanced Caching:** Redis for session and query result caching
- **API Versioning:** Plan v2 endpoint design with backwards compatibility
- **Mobile App:** React Native frontend for iOS/Android
- **Load Testing:** JMeter or k6 for performance benchmarking

## License

MIT (or specify your preference in a LICENSE file).

## Contact

For questions or contributions, open an issue on GitHub.
