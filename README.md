# LMS — Система управления обучением

Бэкенд-сервис для управления курсами и уроками на Django + DRF.

---

## 🌐 Демо

Проект доступен по адресу:  
**[http://93.77.166.84](http://93.77.166.84)**

---

## 🧰 Стек

- Python 3.13
- Django 6.0
- Django REST Framework
- PostgreSQL
- Docker + Docker Compose
- Gunicorn + Nginx
- GitHub Actions (CI/CD)

---

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
Убедитесь, что Docker и Docker Compose установлены.

2. Настройка переменных окружения
Скопируйте .env.template в .env и заполните значения:

bash
```
cp .env.template .env
3. Сборка и запуск
bash
docker-compose up -d --build
```
4. Доступ
API: http://localhost:8000/api/

Swagger: http://localhost:8000/api/docs/

5. Остановка
```bash
docker-compose down
```
⚙️ Продакшен-деплой
Проект развёрнут на сервере с использованием:

Gunicorn — WSGI-сервер

Nginx — reverse-proxy

Docker Compose — оркестрация контейнеров

GitHub Actions — автоматический деплой при push в main

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