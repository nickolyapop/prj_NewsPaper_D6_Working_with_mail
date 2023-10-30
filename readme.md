# Учебный проект Django для студентов Skillfactory

## Запуск проекта

1. Создать виртуальное окружение

        python -m venv venv

2. Активировать ВО

    2.1 В Windows _PowerShell_ или _cmd_

        venv\Scripts\activate

    2.2 В Windows _GitBash_

        source venv/Scripts/activate

    2.3 Linux, MacOS

        source venv/bin/activate

3. Установить зависимости командой

        pip install -r requirements.txt

4. Перейти в папку проекта, где находится файл manage.py с помощью команды cd название_папки, например, 

        cd project

5. Проверить, что находимся в нужной папке с помощью команды ls. Если после выполнения команды в терминале виден файл manage.py - можно запускать проект. Иначе - см. п. 4. 


6. Запускаем проект командой 

        python manage.py runserver

    или

        ./manage.py runserver


## Учётные записи

1. Администратор

   Логин: admin, пароль admin, email: admin@local.host


2. Рядовой пользователь

    Логин: user, пароль user, email: user@example.com

