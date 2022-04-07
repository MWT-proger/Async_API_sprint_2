build:
	docker-compose -f docker-compose.yml build $(c)
up:
	docker-compose -f docker-compose.yml up -d $(c)
start:
	docker-compose -f docker-compose.yml start $(c)
down:
	docker-compose -f docker-compose.yml down $(c)
destroy:
	docker-compose -f docker-compose.yml down -v $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
logs:
	docker-compose -f docker-compose.yml logs --tail=100 -f $(c)
create_demo_user:
	docker-compose -f docker-compose.yml exec movies python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
full_upload:
	docker-compose -f docker-compose.yml up  --build
	docker-compose -f docker-compose.yml exec movies python manage.py migrate movies --fake
	docker-compose -f docker-compose.yml exec movies python manage.py migrate
	docker-compose -f docker-compose.yml exec movies python manage.py collectstatic --noinput
	docker-compose -f docker-compose.yml exec movies python load_data.py
dev_full_upload:
	docker-compose -f docker-compose.dev.yml up -d --build
	docker-compose -f docker-compose.dev.yml exec movies python manage.py migrate movies --fake
	docker-compose -f docker-compose.dev.yml exec movies python manage.py migrate
	docker-compose -f docker-compose.dev.yml exec movies python manage.py collectstatic --noinput
api_tests:
	docker-compose -f tests/functional/docker-compose.yml up