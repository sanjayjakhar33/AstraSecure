# AstraSecure Setup Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL (if running without Docker)

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanjayjakhar33/AstraSecure.git
   cd AstraSecure
   ```

2. **Configure environment variables**
   ```bash
   # Backend configuration
   cp backend_python/.env.example backend_python/.env
   
   # Frontend configuration
   cp frontend_react/.env.example frontend_react/.env
   
   # Edit the files with your specific settings
   ```

3. **Start all services**
   ```bash
   cd infrastructure
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development Setup

### Backend Development

1. **Navigate to backend directory**
   ```bash
   cd backend_python
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start PostgreSQL and Redis**
   ```bash
   # Using Docker
   docker run -d --name astrasecure-db -e POSTGRES_DB=astrasecure -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
   docker run -d --name astrasecure-redis -p 6379:6379 redis:7-alpine
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Development

1. **Navigate to frontend directory**
   ```bash
   cd frontend_react
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

## First-time Setup

### Create Admin User

1. **Register first user via API**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@yourcompany.com",
       "password": "securepassword123",
       "full_name": "Security Admin",
       "role": "company_admin"
     }'
   ```

2. **Create company profile**
   ```bash
   # Login first to get token
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@yourcompany.com&password=securepassword123"
   
   # Use the returned token to create company
   curl -X POST http://localhost:8000/api/v1/companies/ \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Your Company Name",
       "domain": "yourcompany.com",
       "industry": "Technology"
     }'
   ```

## Configuration

### Environment Variables

#### Backend (`.env`)
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/astrasecure

# Security
JWT_SECRET_KEY=your_super_secret_jwt_key_change_this_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Scanning
NMAP_SCAN_TIMEOUT=300
MAX_CONCURRENT_SCANS=5

# Cloud Providers (Optional)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
GCP_SERVICE_ACCOUNT_FILE=path/to/service-account.json
```

#### Frontend (`.env`)
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
REACT_APP_APP_NAME=AstraSecure
```

### Docker Compose Services

- **PostgreSQL**: Database server on port 5432
- **Redis**: Cache and task queue on port 6379  
- **Backend**: Python FastAPI on port 8000
- **Frontend**: React application on port 3000

## API Documentation

Once the backend is running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Common Issues

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# View database logs
docker logs astrasecure-db
```

### Frontend Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Backend Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Install missing dependencies
pip install -r requirements.txt
```

## Production Deployment

### Environment Setup
1. Set `DEBUG=false` in backend environment
2. Configure proper JWT secret keys
3. Set up SSL/TLS certificates
4. Configure production database
5. Set up monitoring and logging

### Security Checklist
- [ ] Change default passwords
- [ ] Configure firewall rules
- [ ] Set up SSL/TLS certificates
- [ ] Enable audit logging
- [ ] Configure backup strategy
- [ ] Set up monitoring alerts

## Support

For technical support or questions:
- Review the documentation in `docs/`
- Check existing GitHub issues
- Contact the development team

## License

This project is licensed under the MIT License - see the LICENSE file for details.