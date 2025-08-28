@echo off
echo.
echo ====================================
echo 🐳 VACATION MANAGEMENT SYSTEM
echo    Complete Docker Deployment
echo ====================================
echo.

echo Checking if Docker is running...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not running!
    echo Please install Docker Desktop and make sure it's running.
    pause
    exit /b 1
)

echo ✅ Docker is available
echo.

echo Checking if Docker Compose is available...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not available!
    echo Please make sure Docker Compose is installed.
    pause
    exit /b 1
)

echo ✅ Docker Compose is available
echo.

echo 📁 Navigating to Vacation_Statistics_Website directory...
cd Vacation_Statistics_Website

if %errorlevel% neq 0 (
    echo ❌ Failed to navigate to Vacation_Statistics_Website directory!
    echo Make sure the directory exists.
    pause
    exit /b 1
)

echo ✅ Successfully navigated to Vacation_Statistics_Website
echo.

echo 🚀 Starting all services...
echo This will start:
echo   - Vacations Website (Vacation_Website)
echo   - Vacations Statistic Dashboard (Vacation_Statistics_Website)
echo   - PostgreSQL Database
echo.
echo This may take a few minutes on first run (building containers)
echo.

echo 🧹 Cleaning up any existing containers...
docker-compose down -v >nul 2>&1

echo 🏗️ Building and starting containers...
docker-compose up -d --build

if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to start services!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ All services started successfully!
echo.

echo 🌐 Your applications are now available at:
echo ┌─────────────────────────────────────────────────────┐
echo │  Django Website:      http://localhost:8000        │
echo │  Dashboard:          http://localhost:3000        │  
echo │  Dashboard API:       http://localhost:5001/api    │
echo └─────────────────────────────────────────────────────┘
echo.

echo 🔐 Admin access:
echo    Default: admin@example.com / admin123
echo    Create custom admins: docker-compose exec django-website python manage.py create_dashboard_admin
echo.

echo 📋 Useful commands:
echo    docker-compose ps    (check status)
echo    docker-compose logs  (view logs)
echo    docker-compose down  (stop all)
echo.

echo 🆕 CONTAINER BENEFITS:
echo    ✅ Single container for dashboard (frontend + backend)
echo    ✅ Reduced resource usage
echo    ✅ Simplified deployment
echo    ✅ Better performance
echo.

echo Press any key to view container status...
pause >nul

echo.
echo 📊 Container Status:
docker-compose ps

echo.
echo 🎉 Setup complete! Your vacation management system is running!
echo.

echo 📝 Services included:
echo    ✅ Vacations Website (django_vacation_project_jb)
echo    ✅ Vacation Statistics Dashboard (Vacation_Statistics_Website)
echo    ✅ PostgreSQL Database
echo.

echo 🔧 Troubleshooting:
echo    - If services fail to start, check Docker Desktop is running
echo    - View logs: docker-compose logs [service-name]
echo    - Restart services: docker-compose restart
echo    - Full rebuild: docker-compose up -d --build
echo.
pause
