
# Как запустить?

1) Запусти *start.bat*.
2) В консоли выведется URL http://ip адрес локального сервера:
```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 15, 2026 - 22:31:39
Django version 5.2.13, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
3. Скопируй этот URL и вставь в адресную строку браузера. 
4. Подставь к нему: /admin. Должно получится:
```bash
http://127.0.0.1:8000/admin
```
5. Введи эти данные:
```bash
username: admin228
password: HBdB#?HUssX#SW'd*K+~+5M^!#Qu9h.R
```
6. Можно тестить.

# Схема базы данных

В корне проекта есть файл db_schema.drawio. Там точная текущая схема базы данных.
Чтобы посмотреть этот файл нужно скачать программу draw.io.

# Зависимости проекта
---
Устанавливаются автоматически через *start.bat*.
```bash
pip install django
pip install pillow
```


