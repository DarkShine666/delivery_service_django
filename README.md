
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
# Инструкция по запуску проекта

## Предварительные требования

Убедитесь, что на вашей машине установлены:

- [Docker](https://www.docker.com/)  
- [Docker Compose](https://docs.docker.com/compose/)  
- [Git](https://git-scm.com/)  

---

## 1. Клонирование репозитория

```bash
git clone https://github.com/DarkShine666/delivery_service_django.git
cd delivery_service_django
```

---

## 2. Конфигурация окружения
В корне проекта создайте файл .env со следующим содержимым:

```python
# Django
SECRET_KEY=super-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=delivery
DB_USER=postgres
DB_PASSWORD=secret
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_CACHE_DB=1      # для кэша
REDIS_CELERY_DB=0     # для брокера

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
```

---

## 3. Запуск в Docker
```bash
docker-compose up -d --build
```

---

## 4. (Опционально) Ручное выполнение миграций и сбора статики

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py makemigrations

```

---

## 5. Создайте суперпользователя

```bash
docker-compose exec backend python manage.py createsuperuser
```

---

## 6. Инициализируйте типы посылок.

```bash
docker-compose exec web python manage.py shell -c "\
from parcels.models import ParcelType;\
ParcelType.objects.bulk_create([\
    ParcelType(name='clothes'),\
    ParcelType(name='electronics'),\
    ParcelType(name='other'),\
])
```

---

## 7. Откройте приложение.

Перейдите в браузере по адресу:
http://localhost:8000
