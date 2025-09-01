# 🚀 AstraSecure Git Testing Guide

## 📋 Prerequisites

Before testing AstraSecure, ensure you have the following installed:

- **Git** (version 2.20+)
- **Node.js** (version 18+)
- **npm** (version 8+)
- **Python** (version 3.12+) - for backend testing
- **Docker** (optional, for containerized testing)

## 🔧 Step-by-Step Testing Guide

### Step 1: Clone the Repository

```bash
# Clone the AstraSecure repository
git clone https://github.com/sanjayjakhar33/AstraSecure.git

# Navigate to the project directory
cd AstraSecure

# Check the repository status
git status

# View available branches
git branch -a
```

### Step 2: Environment Setup

```bash
# Create environment files from examples
cp backend_python/.env.example backend_python/.env
cp frontend_react/.env.example frontend_react/.env

# Edit environment variables (optional)
nano backend_python/.env
nano frontend_react/.env
```

### Step 3: Frontend Testing

#### 3.1 Install Dependencies
```bash
# Navigate to frontend directory
cd frontend_react

# Install all dependencies
npm install

# Check for security vulnerabilities
npm audit

# Fix any security issues (if needed)
npm audit fix
```

#### 3.2 Build Testing
```bash
# Test production build
npm run build

# Check build output
ls -la build/

# Verify build assets
du -sh build/
```

#### 3.3 Development Server Testing
```bash
# Start development server
npm start

# The app will be available at:
# - Local: http://localhost:3000
# - Network: http://[your-ip]:3000
```

#### 3.4 Frontend Testing Commands
```bash
# Run test suite
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch

# Lint code for style issues
npm run lint (if available)
```

### Step 4: Backend Testing (Optional)

#### 4.1 Python Environment Setup
```bash
# Navigate to backend directory
cd ../backend_python

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 4.2 Database Setup
```bash
# Start PostgreSQL with Docker
docker run -d --name astrasecure-db \
  -e POSTGRES_DB=astrasecure \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 postgres:15

# Run database migrations
alembic upgrade head
```

#### 4.3 Backend Server Testing
```bash
# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger documentation
```

### Step 5: Docker Testing (Alternative)

```bash
# Navigate to infrastructure directory
cd infrastructure

# Start all services with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs frontend
docker-compose logs backend

# Stop services
docker-compose down
```

### Step 6: Git Workflow Testing

#### 6.1 Create Feature Branch
```bash
# Create and switch to a new branch
git checkout -b feature/test-enhancement

# Make some test changes
echo "# Test change" >> README.md

# Stage changes
git add .

# Commit changes
git commit -m "Test: Add sample change for testing"

# Push to remote
git push origin feature/test-enhancement
```

#### 6.2 Branch Management
```bash
# List all branches
git branch -a

# Switch between branches
git checkout main
git checkout feature/test-enhancement

# Merge branch (if needed)
git checkout main
git merge feature/test-enhancement

# Delete branch after testing
git branch -d feature/test-enhancement
git push origin --delete feature/test-enhancement
```

### Step 7: Testing Luxury UI Features

#### 7.1 Visual Testing Checklist

**Login Page:**
- [ ] Gradient background loads correctly
- [ ] Glassmorphism card effect is visible
- [ ] Floating animation elements are working
- [ ] Form inputs have luxury styling
- [ ] Buttons show shimmer effects on hover
- [ ] Responsive design works on different screen sizes

**Dashboard:**
- [ ] Sidebar has glassmorphism effect
- [ ] Navigation items show gradient backgrounds when active
- [ ] Metric cards have proper shadows and hover effects
- [ ] Header search bar styling is correct
- [ ] User dropdown menu works properly
- [ ] Quick action buttons have gradient effects
- [ ] Status indicators are animated

#### 7.2 Browser Compatibility Testing

Test in multiple browsers:
```bash
# Chrome/Chromium
google-chrome http://localhost:3000

# Firefox
firefox http://localhost:3000

# Safari (macOS)
open -a Safari http://localhost:3000

# Edge (Windows)
start msedge http://localhost:3000
```

### Step 8: Performance Testing

```bash
# Build for production
npm run build

# Serve production build
npx serve -s build -l 3000

# Test performance with Lighthouse (Chrome DevTools)
# Or use online tools like PageSpeed Insights
```

### Step 9: Code Quality Testing

```bash
# Check TypeScript/JavaScript syntax
npm run build

# Run ESLint (if configured)
npx eslint src/

# Check for unused dependencies
npx depcheck

# Analyze bundle size
npx webpack-bundle-analyzer build/static/js/*.js
```

### Step 10: Deployment Testing

#### 10.1 Netlify/Vercel Deployment
```bash
# Build for production
npm run build

# Deploy to Netlify (if configured)
netlify deploy --dir=build --prod

# Deploy to Vercel (if configured)
vercel --prod
```

#### 10.2 Manual Server Deployment
```bash
# Create production bundle
npm run build

# Copy build files to server
scp -r build/* user@server:/var/www/astrasecure/

# Or use rsync
rsync -av build/ user@server:/var/www/astrasecure/
```

## 🐛 Troubleshooting Common Issues

### Frontend Issues

**Build Failures:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Port Conflicts:**
```bash
# Kill processes on port 3000
npx kill-port 3000

# Or start on different port
PORT=3001 npm start
```

**Styling Issues:**
```bash
# Rebuild Tailwind CSS
npm run build:css  # if configured

# Check Tailwind config
npx tailwindcss init --full
```

### Backend Issues

**Database Connection:**
```bash
# Check PostgreSQL status
docker ps | grep postgres

# View database logs
docker logs astrasecure-db

# Connect to database
docker exec -it astrasecure-db psql -U postgres -d astrasecure
```

**Python Dependencies:**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

## 📊 Testing Metrics & Benchmarks

### Performance Targets
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **Time to Interactive**: < 3.5s

### Bundle Size Targets
- **Main JavaScript Bundle**: < 250KB (gzipped)
- **CSS Bundle**: < 50KB (gzipped)
- **Total Assets**: < 500KB (initial load)

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📝 Testing Reports

### Generate Testing Report
```bash
# Create test results directory
mkdir -p test-results

# Run comprehensive tests
npm test -- --coverage --outputFile=test-results/test-report.json

# Generate lighthouse report
lighthouse http://localhost:3000 --output=json --output-path=test-results/lighthouse-report.json

# Bundle analysis
npx webpack-bundle-analyzer build/static/js/*.js --report --reportFilename=test-results/bundle-report.html
```

## 🔐 Security Testing

```bash
# Check for security vulnerabilities
npm audit

# Run security scanner (if available)
npx security-checker

# Check for hardcoded secrets
git secrets --scan

# HTTPS testing
curl -I https://localhost:3000
```

## 🌐 Production Deployment Checklist

- [ ] Environment variables configured
- [ ] SSL/TLS certificates installed
- [ ] Database migrations applied
- [ ] Static assets optimized
- [ ] CDN configured (if needed)
- [ ] Monitoring setup
- [ ] Backup strategy implemented
- [ ] Security headers configured
- [ ] Performance monitoring enabled
- [ ] Error tracking setup

## 📞 Support & Debugging

For issues during testing:

1. **Check logs**: Review browser console and server logs
2. **Network tab**: Inspect API calls and asset loading
3. **GitHub Issues**: Search existing issues or create new ones
4. **Documentation**: Review README.md and SETUP.md
5. **Discord/Slack**: Join community channels for support

---

## 🎉 Testing Complete!

Congratulations! You've successfully tested AstraSecure. The luxury UI should be working beautifully with all the premium features including:

- ✨ Glassmorphism effects
- 🎨 Gradient backgrounds
- 🚀 Smooth animations
- 💎 Premium styling
- 📱 Responsive design

If you encounter any issues, please refer to the troubleshooting section or reach out for support.