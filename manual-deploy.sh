#!/bin/bash

echo "🚀 Manual Deployment Script for Vacation Project"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[INFO]${NC} Stopping existing containers..."
docker-compose -f docker-compose.production.yml down --remove-orphans || true

echo -e "${GREEN}[INFO]${NC} Cleaning up old Docker images..."
docker system prune -f

echo -e "${GREEN}[INFO]${NC} Building and starting all services..."
docker-compose -f docker-compose.production.yml up -d --build

echo -e "${GREEN}[INFO]${NC} Waiting for services to start..."
sleep 30

echo -e "${GREEN}[INFO]${NC} Checking service status..."
docker-compose -f docker-compose.production.yml ps

echo -e "${GREEN}[INFO]${NC} Recent logs:"
docker-compose -f docker-compose.production.yml logs --tail=20

echo ""
echo -e "${GREEN}🎉 Deployment completed!${NC}"
echo ""
echo "📱 Access URLs:"
echo "   Main Website (Django): http://56.228.81.220/django/"
echo "   Statistics Dashboard (React): http://56.228.81.220/"
echo "   API Endpoints: http://56.228.81.220/api/"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs: docker-compose -f docker-compose.production.yml logs -f"
echo "   Stop services: docker-compose -f docker-compose.production.yml down"
echo "   Restart services: docker-compose -f docker-compose.production.yml restart"
