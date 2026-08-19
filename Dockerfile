FROM python:3.13-slim

WORKDIR /app

COPY requirements.prod.txt .

RUN pip install --no-cache-dir -r requirements.prod.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
