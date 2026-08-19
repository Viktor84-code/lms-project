# LMS — Система управления обучением

Бэкенд-сервис для управления курсами и уроками на Django + DRF.

## Стек

- Python 3.13
- Django 6.0
- Django REST Framework
- PostgreSQL (по умолчанию SQLite)
- Docker
- Git

## 🚀 Быстрый старт (локально)

```bash
git clone https://github.com/Viktor84-code/lms-project.git
cd lms-project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
🐳 Запуск через Docker
1. Подготовка
Убедитесь, что Docker установлен на вашей машине.

2. Настройка переменных окружения
Создайте файл .env в корне проекта:

env
DB_NAME=lms_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
3. Сборка и запуск
bash
docker-compose up -d --build
4. Доступ
API: http://localhost:8000/api/

Swagger: http://localhost:8000/api/docs/

5. Остановка
bash
docker-compose down
📚 API Эндпоинты
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