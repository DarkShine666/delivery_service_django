# 🛠 Установка зависимостей (если надо внутри web)
install:
	docker-compose exec web poetry install

# 🐳 Поднять контейнеры
up:
	docker-compose up --build -d

# 🔻 Остановить всё
down:
	docker-compose down -v --remove-orphans

# ⚙ Применить миграции
migrate:
	docker-compose exec web poetry run python manage.py migrate

# 🧱 Создать миграции
makemigrations:
	docker-compose exec web poetry run python manage.py makemigrations

# 🧪 Проверка
check:
	docker-compose exec web poetry run python manage.py check

# 👤 Создать суперюзера
createsuperuser:
	docker-compose exec web poetry run python manage.py createsuperuser

# 💬 Shell Django
shell:
	docker-compose exec web poetry run python manage.py shell

# 🧼 Чистка
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

test:
	docker-compose exec web poetry run pytest -q
