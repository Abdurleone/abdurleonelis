# Deployment Quick Reference

## Local Development with Docker Compose

### 1. First Time Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your values (optional for dev)
# nano .env

# Start all services
docker-compose up --build
```

### 2. Access Services

```
Frontend:     http://localhost:3000
API Docs:     http://localhost:8000/docs
PostgreSQL:   localhost:5432
```

### 3. Seed Demo Data

```bash
docker-compose exec backend python seed_db.py
```

### 4. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### 5. Stop Services

```bash
docker-compose down

# With volume cleanup (removes database)
docker-compose down -v
```

## Common Docker Commands

```bash
# Build without starting
docker-compose build

# Start in background
docker-compose up -d

# Restart a service
docker-compose restart backend

# Run command in container
docker-compose exec backend bash
docker-compose exec backend python seed_db.py

# Check service health
docker-compose ps

# Remove stopped containers
docker-compose rm

# Full cleanup
docker-compose down -v --rmi all
```

## Environment Variables

### Required

```bash
DATABASE_URL=postgresql://user:password@postgres:5432/lis_db
SECRET_KEY=your-super-secret-key-min-32-chars-random
```

### Optional (has defaults)

```bash
POSTGRES_USER=lis_user
POSTGRES_PASSWORD=lis_secure_password
POSTGRES_DB=lis_db
ACCESS_TOKEN_EXPIRE_MINUTES=1440
VITE_API_URL=http://localhost:3000/api
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

## Production Deployment

### Pre-deployment Checklist

- [ ] Create strong `SECRET_KEY` (use: `openssl rand -hex 32`)
- [ ] Create strong `POSTGRES_PASSWORD`
- [ ] Enable HTTPS/TLS
- [ ] Configure backups
- [ ] Test disaster recovery

### Docker Build for Registry

```bash
# Build images locally
docker build -t myregistry/lis-backend:latest ./backend
docker build -t myregistry/lis-frontend:latest ./frontend

# Push to registry
docker push myregistry/lis-backend:latest
docker push myregistry/lis-frontend:latest
```

### Deploy to AWS ECS

```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag myimage:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/myimage:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/myimage:latest
```

### Deploy to Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/<project-id>/lis-backend ./backend
gcloud builds submit --tag gcr.io/<project-id>/lis-frontend ./frontend

# Deploy
gcloud run deploy lis-backend \
  --image gcr.io/<project-id>/lis-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars DATABASE_URL=<postgresql-url>,SECRET_KEY=<secret>
```

## Troubleshooting

### Port Already in Use

```bash
# Change port in .env
BACKEND_PORT=8001
FRONTEND_PORT=3001

# Or kill process
lsof -i :8000
kill -9 <PID>
```

### Database Connection Issues

```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# Verify connection
docker-compose exec postgres psql -U lis_user -d lis_db -c "SELECT version();"
```

### Frontend Can't Connect to API

```bash
# Check VITE_API_URL in .env
# Must match your backend URL

# For local: http://localhost:3000/api
# For production: https://yourdomain.com/api
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## CI/CD Pipeline

GitHub Actions workflow: `.github/workflows/ci-cd.yml`

**Automatic on:**

- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**Does:**

- ✅ Run backend tests (pytest)
- ✅ Run linting (flake8, eslint)
- ✅ Build Docker images
- ✅ Push to GitHub Container Registry
- ✅ Security scan (Trivy)

**View results:**

- Go to: GitHub > Actions tab
- Click workflow run
- See test results and build logs

## Performance Tips

### Frontend

- Images are multi-stage for minimal size
- Static assets cached for 1 year
- Nginx handles SPA routing automatically

### Backend

- Connection pooling (10 connections to PostgreSQL)
- Health checks ensure reliability
- Auto-reload in development

### Database

- Use managed PostgreSQL in production (RDS, Cloud SQL, etc.)
- Configure automated backups
- Monitor query performance

---

**Quick Start:** `cp .env.example .env && docker-compose up`
