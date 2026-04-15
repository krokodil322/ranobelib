# Как запустить?

1. Нужно скачать и установить python на комп.
2. Скачай данный репозиторий.
3. Скопируй путь в корень репозиторий
4. Открой консоль и введи:
```bash
cd путь_к_корню_проекта
```
5. Запусти venv:
```bash
./venv/Scripts/activate
```
После запуска, слева должно появится (venv).

6. Теперь нужно перейти в папку с приложением:
```bash
cd fan_guild
```
7. Введи команду:
```bash
python manage.py runserver
```
8. В консоли выведется URL http://ip адрес локального сервера:
```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 15, 2026 - 22:31:39
Django version 5.2.13, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
9. Скопируй этот URL и вставь в адресную строку браузера. 
10. Подставь к нему: /admin. Должно получится:
```bash
http://127.0.0.1:8000/admin
```
11. Введи эти данные:
```bash
username: admin228
password: HBdB#?HUssX#SW'd*K+~+5M^!#Qu9h.R
```
12. Можно тестить

# Схема базы данных

В корне проекта есть файл db_schema.drawio. Там точная текущая схема базы данных.
Чтобы посмотреть этот файл нужно скачать программу draw.io.



