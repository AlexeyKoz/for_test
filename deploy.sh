#!/bin/bash

# Vacation Project AWS EC2 Deployment Script
# This script deploys all three projects (Django, Flask, React) to AWS EC2

set -e

echo "🚀 Starting Vacation Project Deployment to AWS EC2..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Get EC2 public IP - try multiple methods
EC2_PUBLIC_IP=""
if command -v curl &> /dev/null; then
    # Try AWS metadata service
    EC2_PUBLIC_IP=$(curl -s --connect-timeout 5 http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "")
    
    # If that fails, try to get from instance metadata
    if [ -z "$EC2_PUBLIC_IP" ]; then
        EC2_PUBLIC_IP=$(curl -s --connect-timeout 5 http://169.254.169.254/latest/meta-data/public-hostname 2>/dev/null | sed 's/.*\.compute\.amazonaws\.com//' 2>/dev/null || echo "")
    fi
fi

# If still empty, use localhost
if [ -z "$EC2_PUBLIC_IP" ]; then
    EC2_PUBLIC_IP="localhost"
    print_warning "Could not detect EC2 public IP, using localhost"
else
    print_status "Detected EC2 Public IP: $EC2_PUBLIC_IP"
fi

# Update production.env with EC2 IP (only if it's not localhost)
if [ "$EC2_PUBLIC_IP" != "localhost" ]; then
    print_status "Updating production environment configuration..."
    sed -i "s/your-ec2-public-ip/$EC2_PUBLIC_IP/g" production.env
fi

# Generate secure secrets if not already set
if grep -q "your_secure_db_password_here" production.env; then
    print_warning "Generating secure passwords..."
    
    # Generate passwords without special characters that might break sed
    DB_PASSWORD=$(openssl rand -hex 32)
    DJANGO_SECRET=$(openssl rand -hex 64)
    JWT_SECRET=$(openssl rand -hex 64)
    
    # Use perl instead of sed for better handling of special characters
    perl -pi -e "s/your_secure_db_password_here/$DB_PASSWORD/g" production.env
    perl -pi -e "s/your_django_secret_key_here_change_this_in_production/$DJANGO_SECRET/g" production.env
    perl -pi -e "s/your_jwt_secret_key_here_change_this_in_production/$JWT_SECRET/g" production.env
    
    print_status "Secure passwords generated and updated in production.env"
fi

# Stop any existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.production.yml down --remove-orphans || true

# Remove old images to free up space
print_status "Cleaning up old Docker images..."
docker system prune -f

# Build and start all services
print_status "Building and starting all services..."
docker-compose -f docker-compose.production.yml up -d --build

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 30

# Check service health
print_status "Checking service health..."

# Check database
if docker-compose -f docker-compose.production.yml exec -T database pg_isready -U postgres > /dev/null 2>&1; then
    print_status "✅ Database is healthy"
else
    print_warning "⚠️  Database health check failed (may still be starting)"
fi

# Check Django website
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "✅ Django website is healthy"
else
    print_warning "⚠️  Django website health check failed (may still be starting)"
fi

# Check Flask API
if curl -f http://localhost:5001/health > /dev/null 2>&1; then
    print_status "✅ Flask API is healthy"
else
    print_warning "⚠️  Flask API health check failed (may still be starting)"
fi

# Check React frontend
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    print_status "✅ React frontend is healthy"
else
    print_warning "⚠️  React frontend health check failed (may still be starting)"
fi

# Check nginx proxy
if curl -f http://localhost/health > /dev/null 2>&1; then
    print_status "✅ Nginx proxy is healthy"
else
    print_warning "⚠️  Nginx proxy health check failed (may still be starting)"
fi

# Show service status
print_status "Service Status:"
docker-compose -f docker-compose.production.yml ps

# Show logs
print_status "Recent logs:"
docker-compose -f docker-compose.production.yml logs --tail=20

# Show access URLs
echo ""
print_status "🎉 Deployment completed successfully!"
echo ""
echo "📱 Access URLs:"
echo "   Main Website (Django): http://$EC2_PUBLIC_IP/django/"
echo "   Statistics Dashboard (React): http://$EC2_PUBLIC_IP/"
echo "   API Endpoints: http://$EC2_PUBLIC_IP/api/"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs: docker-compose -f docker-compose.production.yml logs -f"
echo "   Stop services: docker-compose -f docker-compose.production.yml down"
echo "   Restart services: docker-compose -f docker-compose.production.yml restart"
echo "   Update services: ./deploy.sh"
echo ""
print_status "Deployment script completed!"

