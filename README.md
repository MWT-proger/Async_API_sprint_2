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
**Либо запустить проект вручную**

для начала загрузить образы и развернуть контейнеры
```
docker-compose up -d --build
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
## Тестирование проекта
**Для тестирования проекта необходимо развернуть отдельный docker-compose** 

**Если установлена утилита для запуска Makefile**

 использовать  команду ниже для запуска проекта разработки 
```
make dev_full_upload
```

 и команду для запуска самих тестов 
```
make api_tests
```
**Либо запустить проект разработки вручную**

для начала загрузить образы и развернуть контейнеры
```
docker-compose -f docker-compose.dev.yml up -d --build
```

и запустить сами тесты
```
docker-compose -f tests/functional/docker-compose.yml up
```


**Также в обоих случаях можно запускать тесты через команду**
```
pytest
```

при условиях:

1. Запущен проект для разработки
2. установлены все зависимости из tests/functional/requirements.txt

## Краткое руководство использования

### API для онлайн-кинотеатра 
**Read-only API для онлайн-кинотеатра** 

после запуска доступен по [http://localhost/api/openapi](http://localhost/api/openapi)

Там вы можете найти все ручки 

Такие как:

1. Полнотекстовый поиск по кинопроизведениям  [http://localhost/api/v1/films/search/](http://localhost/api/v1/films/search/)

1. Список фильмов с возможность филтрации, сортировки и пагинации [http://localhost/api/v1​/films​/](http://localhost/api​/v1​/films​/)

1. Отдельную страницу фильма [http://localhost/api/v1/films/{film_id}](http://localhost/api/v1/films/{film_id})

1. Список жанров [http://localhost/api/v1/genres/](http://localhost/api/v1/genres/)

1. Отдельную страницу жанра [http://localhost/api/v1/genres/{genre_id}](http://localhost/api/v1/genres/{genre_id})

1. Полнотекстовый поиск по персонам [http://localhost/api/v1/persons/search](http://localhost/api/v1/persons/search)

1. Отдельную страницу персоны [http://localhost/api/v1/persons/{person_id}](http://localhost/api/v1/persons/{person_id})

### Админ панель 
после запуска доступна по [http://localhost/admin/](http://localhost/admin/)

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
**ссылка для ревью на GitHub**  [https://github.com/MWT-proger/Async_API_sprint_2](https://github.com/MWT-proger/Async_API_sprint_2)
