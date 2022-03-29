#  Онлайн кинотеатр (Проектная работа 4 спринта)

Микросервис отвечает за выдачу API. Работает в комплексе с разработанными ранее Админ панелью и ETL.


## Как развернуть и запустить проект
**Используя Makefile**

Достаточно клонировать проект

```
git clone https://github.com/MWT-proger/Async_API_sprint_1.git
```
**Если установлена утилита для запуска Makefile**

 использовать  команду ниже
```
make full_upload
```
**Либо запустить проект в ручную**

для начала загрузить образы и развернуть контейнеры
```
docker-compose up -d --build
docker-compose -f docker-compose.yml exec movies python manage.py migrate movies --fake
docker-compose -f docker-compose.yml exec movies python manage.py migrate
docker-compose -f docker-compose.yml exec movies python manage.py collectstatic --noinput
docker-compose -f docker-compose.yml exec movies python load_data.py
```

произвести миграции для Админ панели
```
docker-compose -f docker-compose.yml exec movies python manage.py migrate movies --fake
docker-compose -f docker-compose.yml exec movies python manage.py migrate
```
настроить статические файлы  для Админ панели
```
docker-compose -f docker-compose.yml exec movies python manage.py collectstatic --noinput
```
и скопировать из тестовай базы информацию в postgres
```
docker-compose -f docker-compose.yml exec movies python load_data.py
```
Всё! Можно пользоваться))


## Краткое руководство использования

### API для онлайн-кинотеатра 
**Read-only API для онлайн-кинотеатра** 

после запуска доступен по [http://localhost:9000/api/openapi](http://localhost:9000/api/openapi)

Там вы можете найти все ручки 

Такие как:

1. Полнотекстовый поиск по кинопроизведениям  [http://localhost:9000/api/v1/films/search/](http://localhost:9000/api/v1/films/search/)

1. Список фильмов с возможность филтрации, сортировки и пагинации [http://localhost:9000/api/v1​/films​/](http://localhost:9000/api​/v1​/films​/)

1. Отдельную страницу фильма [http://localhost:9000/api/v1/films/{film_id}](http://localhost:9000/api/v1/films/{film_id})

1. Список жанров [http://localhost:9000/api/v1/genres/](http://localhost:9000/api/v1/genres/)

1. Отдельную страницу жанра [http://localhost:9000/api/v1/genres/{genre_id}](http://localhost:9000/api/v1/genres/{genre_id})

1. Полнотекстовый поиск по персонам [http://localhost:9000/api/v1/persons/search](http://localhost:9000/api/v1/persons/search)

1. Отдельную страницу персоны [http://localhost:9000/api/v1/persons/{person_id}](http://localhost:9000/api/v1/persons/{person_id})

### Админ панель 
после запуска доступна по [http://localhost:8000/admin/](http://localhost:8000/admin/)

**В стадии разработки доступен демо пользователь!**

**Если установлена утилита для запуска Makefile**

 использовать  команду ниже
 
```
make create_demo_user
```
Username : `admin` 
Пароль : `adminpass` 

**Или создать самостоятельно**
```
docker-compose -f docker-compose.yml exec movies python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
```
Username : `admin` 
Пароль : `adminpass` 

либо (и дальше по инструкции)
```
docker-compose -f docker-compose.yml exec movies python manage.py createsuperuser
```

--------------------
**ссылка для ревью на GitHub**  [https://github.com/MWT-proger/Async_API_sprint_1](https://github.com/MWT-proger/Async_API_sprint_1)