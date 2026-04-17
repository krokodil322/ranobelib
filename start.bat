@echo off
setlocal

set "ROOT=%~dp0"
set "PROJECT=%ROOT%fan_guild"
set "VENV_DIR=%ROOT%venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

set "DJANGO_SUPERUSER_USERNAME=admin228"
set "DJANGO_SUPERUSER_EMAIL=admin@example.com"
set "DJANGO_SUPERUSER_PASSWORD=admin123456"

echo ROOT=%ROOT%
echo PROJECT=%PROJECT%
echo.

if not exist "%VENV_PY%" (
    echo Creating virtual environment...
    py -3 -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo Installing dependencies...
"%VENV_PY%" -m pip install --upgrade pip
"%VENV_PY%" -m pip install django pillow
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Switching to project folder...
pushd "%PROJECT%"
if errorlevel 1 (
    echo Failed to open project folder: %PROJECT%
    pause
    exit /b 1
)

if not exist "manage.py" (
    echo manage.py not found in:
    cd
    dir
    pause
    popd
    exit /b 1
)

echo Running migrations...
"%VENV_PY%" manage.py makemigrations
if errorlevel 1 (
    echo makemigrations failed.
    pause
    popd
    exit /b 1
)

"%VENV_PY%" manage.py migrate
if errorlevel 1 (
    echo migrate failed.
    pause
    popd
    exit /b 1
)

echo Checking superuser...
"%VENV_PY%" manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); exit(0 if User.objects.filter(username='%DJANGO_SUPERUSER_USERNAME%').exists() else 1)"

if errorlevel 1 (
    echo Creating superuser...
    "%VENV_PY%" manage.py createsuperuser --noinput
    if errorlevel 1 (
        echo Failed to create superuser.
        pause
        popd
        exit /b 1
    )
) else (
    echo Superuser already exists.
)

echo Starting server...

start "" "%VENV_PY%" manage.py runserver

echo Waiting for server to start...
timeout /t 2 > nul

echo Opening browser...
start "" http://127.0.0.1:8000/admin

popd
pause