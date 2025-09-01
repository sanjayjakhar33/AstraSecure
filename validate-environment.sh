#!/bin/bash

# =============================================================================
# AstraSecure Environment Validation Script
# =============================================================================
# This script validates your environment variables for deployment
#
# Usage: ./validate-environment.sh
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Validate environment file
validate_env_file() {
    local env_file="$1"
    local service_name="$2"
    
    if [[ ! -f "$env_file" ]]; then
        print_warning "$service_name environment file not found: $env_file"
        return 1
    fi
    
    print_success "$service_name environment file found: $env_file"
    
    # Check for common required variables
    while IFS='=' read -r key value; do
        if [[ -n "$key" && ! "$key" =~ ^#.* ]]; then
            if [[ -z "$value" || "$value" == "your-*" || "$value" == "change-this*" ]]; then
                print_warning "$service_name: Variable '$key' needs to be set"
            else
                print_success "$service_name: Variable '$key' is configured"
            fi
        fi
    done < "$env_file"
}

# Validate URL format
validate_url() {
    local url="$1"
    local name="$2"
    
    if [[ "$url" =~ ^https?:// ]]; then
        print_success "$name URL format is valid"
        return 0
    else
        print_error "$name URL format is invalid (should start with http:// or https://)"
        return 1
    fi
}

# Validate database URL
validate_database_url() {
    local db_url="$1"
    
    if [[ "$db_url" =~ ^postgresql:// ]]; then
        print_success "Database URL format is valid"
        return 0
    else
        print_error "Database URL format is invalid (should start with postgresql://)"
        return 1
    fi
}

# Main validation
main() {
    print_header "🔍 AstraSecure Environment Validation"
    
    local errors=0
    
    # Check for environment files
    print_info "Checking environment configuration files..."
    
    if validate_env_file ".env.production.local" "Production"; then
        # Validate specific production variables
        if [[ -f ".env.production.local" ]]; then
            source .env.production.local
            
            if [[ -n "$REACT_APP_API_URL" ]]; then
                validate_url "$REACT_APP_API_URL" "Backend API" || ((errors++))
            else
                print_warning "REACT_APP_API_URL not set"
                ((errors++))
            fi
            
            if [[ -n "$DATABASE_URL" ]]; then
                validate_database_url "$DATABASE_URL" || ((errors++))
            else
                print_warning "DATABASE_URL not set"
                ((errors++))
            fi
        fi
    else
        ((errors++))
    fi
    
    # Check Vercel configuration
    print_info "Checking Vercel configuration..."
    
    if [[ -f "vercel.json" ]]; then
        print_success "vercel.json found"
        
        # Check if backend URL is updated
        if grep -q "your-backend-url" vercel.json; then
            print_warning "Backend URL in vercel.json needs to be updated"
            ((errors++))
        else
            print_success "Backend URL in vercel.json appears to be configured"
        fi
    else
        print_error "vercel.json not found"
        ((errors++))
    fi
    
    # Check frontend build
    print_info "Checking frontend build status..."
    
    if [[ -d "frontend_react/build" ]]; then
        print_success "Frontend build directory exists"
    else
        print_warning "Frontend build directory not found. Run: cd frontend_react && npm run build"
    fi
    
    # Check dependencies
    print_info "Checking dependencies..."
    
    if [[ -f "frontend_react/node_modules/.package-lock.json" ]]; then
        print_success "Frontend dependencies installed"
    else
        print_warning "Frontend dependencies not installed. Run: cd frontend_react && npm install"
    fi
    
    # Summary
    print_header "📊 Validation Summary"
    
    if [[ $errors -eq 0 ]]; then
        print_success "All validations passed! Your environment is ready for deployment."
        echo ""
        print_info "You can now run: vercel --prod"
    else
        print_error "Found $errors issues that need to be addressed before deployment."
        echo ""
        print_info "Please fix the issues above and run this script again."
        echo ""
        print_info "For help with configuration, see:"
        echo "  - VERCEL_DEPLOYMENT.md"
        echo "  - .env.production.example"
    fi
    
    return $errors
}

# Execute main function
main "$@"