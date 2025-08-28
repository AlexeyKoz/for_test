@echo off
REM Vacation Project AWS EC2 Deployment Script for Windows
REM This script deploys all three projects (Django, Flask, React) to AWS EC2

echo 🚀 Starting Vacation Project Deployment to AWS EC2...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

echo [INFO] Docker and Docker Compose are installed.

REM Stop any existing containers
echo [INFO] Stopping existing containers...
docker-compose -f docker-compose.production.yml down --remove-orphans 2>nul

REM Remove old images to free up space
echo [INFO] Cleaning up old Docker images...
docker system prune -f

REM Build and start all services
echo [INFO] Building and starting all services...
docker-compose -f docker-compose.production.yml up -d --build

REM Wait for services to be ready
echo [INFO] Waiting for services to be ready...
timeout /t 30 /nobreak >nul

REM Show service status
echo [INFO] Service Status:
docker-compose -f docker-compose.production.yml ps

REM Show logs
echo [INFO] Recent logs:
docker-compose -f docker-compose.production.yml logs --tail=20

echo.
echo 🎉 Deployment completed successfully!
echo.
echo 📱 Access URLs:
echo    Main Website (Django): http://localhost/django/
echo    Statistics Dashboard (React): http://localhost/
echo    API Endpoints: http://localhost/api/
echo.
echo 🔧 Useful Commands:
echo    View logs: docker-compose -f docker-compose.production.yml logs -f
echo    Stop services: docker-compose -f docker-compose.production.yml down
echo    Restart services: docker-compose -f docker-compose.production.yml restart
echo    Update services: deploy.bat
echo.
echo [INFO] Deployment script completed!
pause

