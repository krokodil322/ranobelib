chcp 65001 > nul

@echo off
echo === Создание виртуального окружения ===
python -m venv venv
echo =======================================

echo === Активация окружения ===
call venv\Scripts\activate
echo ===========================

echo === Установка зависимостей ===
pip install django
pip install pillow
echo ==============================

echo === Переход в проект ===
cd /d %~dp0fan_guild
echo ========================

echo === Миграции ===
python manage.py makemigrations
python manage.py migrate
echo ================

echo === Запуск сервера ===
python manage.py runserver
echo ======================

pause
