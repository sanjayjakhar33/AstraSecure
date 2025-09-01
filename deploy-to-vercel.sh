#!/bin/bash

# =============================================================================
# AstraSecure Single-Step Vercel Deployment Script
# =============================================================================
# This script automates the complete deployment of AstraSecure to Vercel
# with database and backend setup on cloud providers.
#
# Prerequisites:
# - Node.js 18+ installed
# - npm or yarn installed  
# - Git configured
# - Accounts created on: Vercel, Railway/Render (for backend), Neon/Supabase (for database)
#
# Usage: ./deploy-to-vercel.sh
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Utility functions
print_header() {
    echo -e "\n${BLUE}==============================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}==============================================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verify prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Node.js
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_success "Node.js installed: $NODE_VERSION"
    else
        print_error "Node.js is required but not installed. Please install Node.js 18+"
        exit 1
    fi
    
    # Check npm
    if command_exists npm; then
        NPM_VERSION=$(npm --version)
        print_success "npm installed: $NPM_VERSION"
    else
        print_error "npm is required but not installed."
        exit 1
    fi
    
    # Check git
    if command_exists git; then
        GIT_VERSION=$(git --version)
        print_success "Git installed: $GIT_VERSION"
    else
        print_error "Git is required but not installed."
        exit 1
    fi
}

# Install and setup Vercel CLI
setup_vercel_cli() {
    print_header "Setting Up Vercel CLI"
    
    if ! command_exists vercel; then
        print_info "Installing Vercel CLI globally..."
        npm install -g vercel
        print_success "Vercel CLI installed successfully"
    else
        print_success "Vercel CLI already installed"
    fi
}

# Database setup guidance
setup_database() {
    print_header "Database Setup Instructions"
    
    echo -e "${YELLOW}Choose your database provider:${NC}"
    echo "1. Neon (Recommended - Free tier available)"
    echo "2. Supabase (Free tier available)"
    echo "3. Railway (Simple setup)"
    echo "4. Render (Integrated with hosting)"
    echo "5. I'll set this up later"
    
    read -p "Enter your choice (1-5): " db_choice
    
    case $db_choice in
        1)
            print_info "Neon Database Setup:"
            echo "1. Go to https://neon.tech and create an account"
            echo "2. Create a new project"
            echo "3. Copy the connection string"
            echo "4. Format: postgresql://username:password@ep-hostname.neon.tech/database_name?sslmode=require"
            ;;
        2)
            print_info "Supabase Database Setup:"
            echo "1. Go to https://supabase.com and create an account"
            echo "2. Create a new project"
            echo "3. Go to Settings > Database"
            echo "4. Copy the connection string"
            echo "5. Format: postgresql://postgres:password@db.hostname.supabase.co:5432/postgres"
            ;;
        3)
            print_info "Railway Database Setup:"
            echo "1. Go to https://railway.app and create an account"
            echo "2. Create a new project"
            echo "3. Add PostgreSQL service"
            echo "4. Copy the DATABASE_URL from the Variables tab"
            ;;
        4)
            print_info "Render Database Setup:"
            echo "1. Go to https://render.com and create an account"
            echo "2. Create a new PostgreSQL database"
            echo "3. Copy the external connection string"
            ;;
        5)
            print_warning "Database setup skipped. You'll need to configure this later."
            return
            ;;
        *)
            print_error "Invalid choice. Skipping database setup."
            return
            ;;
    esac
    
    echo ""
    read -p "Enter your database URL: " DATABASE_URL
    
    if [[ -n "$DATABASE_URL" ]]; then
        print_success "Database URL saved"
        echo "DATABASE_URL=$DATABASE_URL" > .env.production.local
    else
        print_warning "No database URL provided"
    fi
}

# Backend deployment guidance
setup_backend() {
    print_header "Backend Deployment Instructions"
    
    echo -e "${YELLOW}Choose your backend hosting provider:${NC}"
    echo "1. Railway (Recommended - Easy Python deployment)"
    echo "2. Render (Free tier available)"
    echo "3. Fly.io (Global edge deployment)"
    echo "4. I'll deploy this separately"
    
    read -p "Enter your choice (1-4): " backend_choice
    
    case $backend_choice in
        1)
            print_info "Railway Backend Deployment:"
            echo "1. Go to https://railway.app"
            echo "2. Create a new project"
            echo "3. Connect your GitHub repository"
            echo "4. Select the backend_python folder as root"
            echo "5. Railway will auto-deploy your Python app"
            echo "6. Copy the generated URL"
            ;;
        2)
            print_info "Render Backend Deployment:"
            echo "1. Go to https://render.com"
            echo "2. Create a new Web Service"
            echo "3. Connect your GitHub repository"
            echo "4. Set Root Directory to 'backend_python'"
            echo "5. Set Build Command: 'pip install -r requirements.txt'"
            echo "6. Set Start Command: 'uvicorn app.main:app --host 0.0.0.0 --port \$PORT'"
            echo "7. Deploy and copy the URL"
            ;;
        3)
            print_info "Fly.io Backend Deployment:"
            echo "1. Install Fly.io CLI: curl -L https://fly.io/install.sh | sh"
            echo "2. Run: fly auth login"
            echo "3. In backend_python directory, run: fly launch"
            echo "4. Follow the prompts to deploy"
            ;;
        4)
            print_warning "Backend deployment skipped. You'll need to deploy this separately."
            return
            ;;
        *)
            print_error "Invalid choice. Skipping backend setup."
            return
            ;;
    esac
    
    echo ""
    read -p "Enter your backend URL (without /api/v1): " BACKEND_URL
    
    if [[ -n "$BACKEND_URL" ]]; then
        print_success "Backend URL saved"
        REACT_APP_API_URL="$BACKEND_URL/api/v1"
        echo "REACT_APP_API_URL=$REACT_APP_API_URL" >> .env.production.local
        
        # Update vercel.json with the backend URL
        sed -i.bak "s|https://your-backend-url.com|$BACKEND_URL|g" vercel.json
    else
        print_warning "No backend URL provided"
    fi
}

# Build the frontend
build_frontend() {
    print_header "Building Frontend Application"
    
    cd frontend_react
    
    # Install dependencies
    print_info "Installing frontend dependencies..."
    npm install
    print_success "Dependencies installed"
    
    # Create production build
    print_info "Creating production build..."
    npm run build
    print_success "Frontend build completed"
    
    cd ..
}

# Deploy to Vercel
deploy_to_vercel() {
    print_header "Deploying to Vercel"
    
    # Login to Vercel if not already logged in
    print_info "Checking Vercel authentication..."
    if ! vercel whoami >/dev/null 2>&1; then
        print_info "Please log in to Vercel..."
        vercel login
    else
        print_success "Already logged in to Vercel"
    fi
    
    # Deploy the application
    print_info "Deploying application to Vercel..."
    vercel --prod --yes
    
    print_success "Deployment completed!"
}

# Setup environment variables in Vercel
setup_vercel_env() {
    print_header "Setting Up Environment Variables"
    
    if [[ -f ".env.production.local" ]]; then
        print_info "Setting up environment variables in Vercel..."
        
        # Read environment variables and set them in Vercel
        while IFS='=' read -r key value; do
            if [[ -n "$key" && -n "$value" && ! "$key" =~ ^#.* ]]; then
                vercel env add "$key" production <<< "$value"
                print_success "Set $key in Vercel"
            fi
        done < .env.production.local
    else
        print_warning "No local environment file found. You'll need to set environment variables manually in Vercel dashboard."
    fi
}

# Post-deployment instructions
post_deployment() {
    print_header "Post-Deployment Setup"
    
    print_info "Complete these final steps:"
    echo ""
    echo "1. 📊 Set up monitoring and analytics"
    echo "   - Add your domain to Vercel project settings"
    echo "   - Configure custom domain (optional)"
    echo "   - Set up Vercel Analytics"
    echo ""
    echo "2. 🗄️  Database initialization"
    echo "   - Run database migrations on your backend service"
    echo "   - Create initial admin user"
    echo ""
    echo "3. 🔒 Security checklist"
    echo "   - Review and update CORS settings"
    echo "   - Verify environment variables are set correctly"
    echo "   - Test SSL/HTTPS configuration"
    echo ""
    echo "4. 🧪 Testing"
    echo "   - Test all application features"
    echo "   - Verify API connections"
    echo "   - Check responsive design"
    echo ""
    
    # Show the deployed URL
    VERCEL_URL=$(vercel --scope=team ls | grep "$(basename $(pwd))" | awk '{print $2}' | head -1)
    if [[ -n "$VERCEL_URL" ]]; then
        print_success "Your application is deployed at: https://$VERCEL_URL"
    fi
}

# Troubleshooting tips
show_troubleshooting() {
    print_header "Troubleshooting Tips"
    
    echo "Common issues and solutions:"
    echo ""
    echo "🔧 Build failures:"
    echo "   - Check Node.js version (requires 18+)"
    echo "   - Clear npm cache: npm cache clean --force"
    echo "   - Delete node_modules and reinstall: rm -rf node_modules && npm install"
    echo ""
    echo "🌐 API connection issues:"
    echo "   - Verify backend URL in environment variables"
    echo "   - Check CORS settings on backend"
    echo "   - Ensure backend is deployed and accessible"
    echo ""
    echo "🗄️  Database connection issues:"
    echo "   - Verify database URL format"
    echo "   - Check database credentials"
    echo "   - Ensure database allows external connections"
    echo ""
    echo "📞 Get help:"
    echo "   - GitHub Issues: https://github.com/sanjayjakhar33/AstraSecure/issues"
    echo "   - Vercel Documentation: https://vercel.com/docs"
    echo "   - Check application logs in Vercel dashboard"
}

# Main execution
main() {
    print_header "🚀 AstraSecure Single-Step Vercel Deployment"
    echo "This script will guide you through deploying AstraSecure to Vercel"
    echo "with complete database and backend setup."
    echo ""
    
    read -p "Continue with deployment? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_info "Deployment cancelled"
        exit 0
    fi
    
    # Execute deployment steps
    check_prerequisites
    setup_vercel_cli
    setup_database
    setup_backend
    build_frontend
    deploy_to_vercel
    setup_vercel_env
    post_deployment
    show_troubleshooting
    
    print_header "🎉 Deployment Complete!"
    print_success "AstraSecure has been successfully deployed to Vercel!"
    echo ""
    echo "Next steps:"
    echo "1. Complete the post-deployment setup above"
    echo "2. Test your application thoroughly"  
    echo "3. Set up monitoring and backups"
    echo ""
    print_info "Happy securing! 🔒"
}

# Execute main function
main "$@"