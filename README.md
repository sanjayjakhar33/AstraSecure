# AstraSecure

A comprehensive, multi-tenant SaaS cybersecurity auditing platform for automated AI-driven security assessments of IT infrastructure.

## 🚀 Features

### Core Capabilities
- **Multi-tenant Architecture**: Secure company isolation with role-based access control
- **Automated Vulnerability Scanning**: Network, web application, and cloud configuration scanning
- **AI-Driven Risk Assessment**: Intelligent vulnerability classification and risk scoring
- **Compliance Management**: SOC2, PCI-DSS, ISO27001, and other framework support
- **Real-time Dashboard**: Interactive security metrics and trend analysis
- **Automated Reporting**: PDF/CSV reports with actionable remediation guidance

### Security Modules
- **Network Scanning**: Nmap-based port scanning and service detection
- **Web Application Security**: Nikto and custom vulnerability checks
- **Cloud Configuration**: AWS, GCP, and Azure security assessments
- **Code Security**: Repository scanning for secrets and misconfigurations
- **Compliance Auditing**: Automated compliance check execution

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python FastAPI with async support
- **Frontend**: React 18 with Tailwind CSS
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based with role management
- **Task Queue**: Celery with Redis
- **Containerization**: Docker and Docker Compose

### Project Structure
```
AstraSecure/
├── backend_python/          # FastAPI backend application
│   ├── app/
│   │   ├── api/             # API endpoints
│   │   ├── core/            # Core utilities (auth, config, db)
│   │   ├── models/          # SQLAlchemy database models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── services/        # Business logic and scanners
│   │   └── main.py          # FastAPI application entry point
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container configuration
├── frontend_react/          # React frontend application
│   ├── src/                 # React source code
│   ├── package.json         # Node.js dependencies
│   └── Dockerfile           # Frontend container configuration
├── backend/                 # Legacy Node.js backend (for reference)
├── infrastructure/          # Docker Compose and deployment
│   └── docker-compose.yml   # Multi-service orchestration
└── docs/                    # Documentation and compliance guides
```

## 🚀 Quick Start

### ⚡ Deploy to Vercel in 10 Minutes (Recommended)

**Want to get AstraSecure running in production quickly?**

```bash
git clone https://github.com/sanjayjakhar33/AstraSecure.git
cd AstraSecure
./deploy-to-vercel.sh
```

📖 **[Complete Vercel Deployment Guide →](./VERCEL_DEPLOYMENT.md)**

### 🔧 Local Development Setup

### Prerequisites
- Docker and Docker Compose
- Git
- Python 3.12+ (for local development)
- Node.js 18+ (for frontend development)

### 1. Clone Repository
```bash
git clone https://github.com/sanjayjakhar33/AstraSecure.git
cd AstraSecure
```

### 2. Environment Configuration
```bash
# Backend configuration
cp backend_python/.env.example backend_python/.env
# Edit backend_python/.env with your settings

# Frontend configuration  
cp frontend_react/.env.example frontend_react/.env
# Edit frontend_react/.env with your settings
```

### 3. Launch with Docker Compose
```bash
cd infrastructure
docker-compose up -d
```

### 4. Access the Application
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 5. Create First User
```bash
# Use the API or register through the frontend
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourcompany.com",
    "password": "securepassword123",
    "full_name": "Security Admin",
    "role": "company_admin"
  }'
```

## 🔧 Development Setup

### Backend Development
```bash
cd backend_python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend_react

# Install dependencies
npm install

# Start development server
npm start
```

### Database Setup
```bash
# Start PostgreSQL
docker run -d --name astrasecure-db \
  -e POSTGRES_DB=astrasecure \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 postgres:15

# Run migrations
cd backend_python
alembic upgrade head
```

## 📊 Usage Guide

### 1. Company Setup
1. Register as a company admin
2. Configure company profile and compliance requirements
3. Add cloud provider credentials (AWS, GCP, Azure)
4. Invite team members with appropriate roles

### 2. Scan Target Configuration
1. Navigate to "Scan Targets" in the dashboard
2. Add targets:
   - **Network**: IP addresses or CIDR ranges
   - **Web Applications**: Domain names or URLs
   - **Cloud Resources**: Using configured credentials
   - **Code Repositories**: GitHub/GitLab repository URLs

### 3. Running Security Scans
1. Select scan targets
2. Choose scan type (Quick, Basic, Comprehensive)
3. Schedule or run immediate scans
4. Monitor progress in real-time

### 4. Reviewing Results
1. View dashboard for risk score trends
2. Examine detailed vulnerability reports
3. Review compliance check results
4. Generate and export reports

### 5. Remediation Management
1. Assign vulnerabilities to team members
2. Track remediation progress
3. Validate fixes with re-scans
4. Update compliance status

## 🔐 Security Features

### Authentication & Authorization
- JWT-based authentication with configurable expiry
- Role-based access control (Super Admin, Company Admin, Analyst, Viewer)
- Multi-tenant data isolation
- API key support for programmatic access

### Data Protection
- Encryption at rest and in transit
- Secure credential storage
- Audit logging for all actions
- GDPR compliance features

### Scanning Security
- Isolated scan execution environments
- Rate limiting and resource controls
- Secure credential handling
- Scan result validation

## 🔧 Configuration

### Environment Variables

#### Backend Configuration
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/astrasecure

# Security
JWT_SECRET_KEY=your_super_secret_jwt_key_change_this_in_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Cloud Providers
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
GCP_SERVICE_ACCOUNT_FILE=path/to/service-account.json

# Scanning
NMAP_SCAN_TIMEOUT=300
MAX_CONCURRENT_SCANS=5
```

#### Frontend Configuration
```bash
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
REACT_APP_APP_NAME=AstraSecure
```

### Compliance Frameworks
- SOC 2 Type II
- PCI-DSS
- ISO 27001
- HIPAA
- GDPR
- NIST Cybersecurity Framework

## 🧪 Testing

### Backend Testing
```bash
cd backend_python
pytest app/tests/ -v
```

### Frontend Testing
```bash
cd frontend_react
npm test
```

### Integration Testing
```bash
cd infrastructure
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📈 Monitoring & Observability

### Health Checks
- `/health` - Application health status
- `/metrics` - Prometheus metrics endpoint
- Database connection monitoring
- External service connectivity checks

### Logging
- Structured JSON logging
- Configurable log levels
- Audit trail for security events
- Scan execution logs

## 🚀 Deployment

### Production Deployment
1. Configure production environment variables
2. Set up SSL/TLS certificates
3. Configure backup strategy
4. Deploy using Docker Compose or Kubernetes

### Scaling Considerations
- Horizontal scaling of API servers
- Database read replicas
- Redis clustering for high availability
- CDN for frontend assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issue Tracker**: [GitHub Issues](https://github.com/sanjayjakhar33/AstraSecure/issues)
- **Security Issues**: security@astrasecure.com

---

**⚠️ Security Notice**: This platform performs security scanning operations. Ensure you have proper authorization before scanning any systems or networks. The platform should only be used for legitimate security assessment purposes.