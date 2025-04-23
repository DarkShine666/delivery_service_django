## **Сколнировать репозиторий**
git clone https://github.com/DarkShine666/delivery_service_django.git

---

📦 **Микросервис международной доставки**  
Реализован на Django + DRF + Celery + Redis + MySQL.

---

## 🛠 Технологии

- Python 3.12
- Django 5.2, Django REST Framework
- Celery + Redis (брокер и кеш)
- MySQL (через Docker)
- Poetry, Docker, Docker Compose
- drf-spectacular (Swagger)
- pytest, pytest-django (тесты)

---

## 🚀 Запуск

1. Склонируйте репозиторий  
2. Создайте `.env`
   ```dotenv
   SECRET_KEY=...
   DB_HOST=db
   DB_PORT=3306
   REDIS_HOST=redis
   REDIS_PORT=6379