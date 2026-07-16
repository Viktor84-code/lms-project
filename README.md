# LMS — Система управления обучением

Бэкенд-сервис для управления курсами и уроками на Django + DRF.

## Стек

- Python 3.10+
- Django 6.0
- Django REST Framework
- PostgreSQL (по умолчанию SQLite)
- Git

## Быстрый старт

```bash
git clone https://github.com/Viktor84-code/lms-project.git
cd lms-project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
API эндпоинты
Метод	Эндпоинт	Описание
GET	/api/courses/	Список курсов
POST	/api/courses/	Создание курса
GET	/api/courses/{id}/	Детали курса
PUT/PATCH	/api/courses/{id}/	Обновление курса
DELETE	/api/courses/{id}/	Удаление курса
GET	/api/lessons/	Список уроков
POST	/api/lessons/	Создание урока
GET	/api/lessons/{id}/	Детали урока
PUT/PATCH	/api/lessons/{id}/	Обновление урока
DELETE	/api/lessons/{id}/	Удаление урока
GET/PUT	/users/profile/{id}/	Профиль пользователя