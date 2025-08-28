@echo off
echo.
echo ====================================
echo 🧹 CLEANING DOCKER ENVIRONMENT
echo ====================================
echo.

echo Stopping and removing existing containers...
cd Vacation_Statistics_Website
docker-compose down -v

echo.
echo Removing any dangling images...
docker image prune -f

echo.
echo Removing any unused volumes...
docker volume prune -f

echo.
echo ✅ Docker environment cleaned!
echo.
pause
