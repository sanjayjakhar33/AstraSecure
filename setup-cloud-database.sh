#!/bin/bash

# =============================================================================
# AstraSecure Database Setup for Cloud Deployment
# =============================================================================
# This script sets up the database schema and initial data for cloud deployment
#
# Usage: ./setup-cloud-database.sh [DATABASE_URL]
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

# Check if DATABASE_URL is provided
if [ -z "$1" ]; then
    echo "Usage: $0 [DATABASE_URL]"
    echo "Example: $0 'postgresql://username:password@hostname:port/database'"
    exit 1
fi

DATABASE_URL="$1"

print_header "🗄️  AstraSecure Cloud Database Setup"

# Validate DATABASE_URL format
if [[ ! "$DATABASE_URL" =~ ^postgresql:// ]]; then
    print_error "Invalid DATABASE_URL format. Must start with 'postgresql://'"
    exit 1
fi

print_info "Database URL: ${DATABASE_URL}"

# Test database connection
print_info "Testing database connection..."
if command -v psql >/dev/null 2>&1; then
    if psql "$DATABASE_URL" -c "SELECT version();" >/dev/null 2>&1; then
        print_success "Database connection successful"
    else
        print_error "Failed to connect to database"
        exit 1
    fi
else
    print_warning "psql not found. Skipping connection test."
fi

# Create database schema SQL
print_info "Creating database schema..."

cat << 'EOF' > /tmp/create_schema.sql
-- AstraSecure Database Schema for Cloud Deployment

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Companies table
CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE NOT NULL,
    industry VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'analyst',
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Scan targets table
CREATE TABLE IF NOT EXISTS scan_targets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    target_type VARCHAR(50) NOT NULL, -- 'network', 'web', 'cloud', 'code'
    target_url VARCHAR(500) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Scan results table
CREATE TABLE IF NOT EXISTS scan_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    target_id UUID REFERENCES scan_targets(id) ON DELETE CASCADE,
    scan_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    results JSONB,
    risk_score INTEGER,
    vulnerability_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Vulnerabilities table
CREATE TABLE IF NOT EXISTS vulnerabilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scan_result_id UUID REFERENCES scan_results(id) ON DELETE CASCADE,
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    severity VARCHAR(20) NOT NULL, -- 'critical', 'high', 'medium', 'low'
    title VARCHAR(255) NOT NULL,
    description TEXT,
    cve_id VARCHAR(50),
    cvss_score DECIMAL(3,1),
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'in_progress', 'resolved', 'false_positive'
    assigned_to UUID REFERENCES users(id),
    remediation_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Compliance frameworks table
CREATE TABLE IF NOT EXISTS compliance_frameworks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Company compliance table
CREATE TABLE IF NOT EXISTS company_compliance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    framework_id UUID REFERENCES compliance_frameworks(id),
    status VARCHAR(50) DEFAULT 'not_started', -- 'not_started', 'in_progress', 'compliant', 'non_compliant'
    last_assessment_date TIMESTAMP WITH TIME ZONE,
    next_assessment_date TIMESTAMP WITH TIME ZONE,
    compliance_score INTEGER, -- 0-100
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- API keys table
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    permissions JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE,
    last_used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_company_id ON users(company_id);
CREATE INDEX IF NOT EXISTS idx_scan_targets_company_id ON scan_targets(company_id);
CREATE INDEX IF NOT EXISTS idx_scan_results_company_id ON scan_results(company_id);
CREATE INDEX IF NOT EXISTS idx_scan_results_target_id ON scan_results(target_id);
CREATE INDEX IF NOT EXISTS idx_vulnerabilities_company_id ON vulnerabilities(company_id);
CREATE INDEX IF NOT EXISTS idx_vulnerabilities_scan_result_id ON vulnerabilities(scan_result_id);
CREATE INDEX IF NOT EXISTS idx_vulnerabilities_severity ON vulnerabilities(severity);
CREATE INDEX IF NOT EXISTS idx_audit_logs_company_id ON audit_logs(company_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Insert default compliance frameworks
INSERT INTO compliance_frameworks (name, version, description) VALUES
    ('SOC 2', 'Type II', 'Service Organization Control 2 Type II compliance framework'),
    ('PCI DSS', '4.0', 'Payment Card Industry Data Security Standard'),
    ('ISO 27001', '2022', 'Information Security Management System standard'),
    ('HIPAA', '2013', 'Health Insurance Portability and Accountability Act'),
    ('GDPR', '2018', 'General Data Protection Regulation'),
    ('NIST CSF', '1.1', 'NIST Cybersecurity Framework')
ON CONFLICT DO NOTHING;

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scan_targets_updated_at BEFORE UPDATE ON scan_targets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vulnerabilities_updated_at BEFORE UPDATE ON vulnerabilities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_company_compliance_updated_at BEFORE UPDATE ON company_compliance
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
EOF

# Execute schema creation
print_info "Executing database schema creation..."
if command -v psql >/dev/null 2>&1; then
    psql "$DATABASE_URL" -f /tmp/create_schema.sql
    print_success "Database schema created successfully"
else
    print_warning "psql not found. Please execute the SQL file manually:"
    echo "File created at: /tmp/create_schema.sql"
fi

# Clean up
rm -f /tmp/create_schema.sql

print_header "✅ Database Setup Complete"

print_info "Next steps:"
echo "1. Update your backend environment variables with the DATABASE_URL"
echo "2. Deploy your backend application"
echo "3. Create your first admin user via the API or admin interface"
echo ""
echo "Example admin user creation:"
echo "curl -X POST https://your-backend-url/api/v1/auth/register \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{"
echo "    \"email\": \"admin@yourcompany.com\","
echo "    \"password\": \"securepassword123\","
echo "    \"full_name\": \"Security Admin\","
echo "    \"role\": \"company_admin\""
echo "  }'"
echo ""

print_success "Database is ready for production use!"