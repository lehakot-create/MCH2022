### Парсер компаний МО из каталога производитель.рф
URL_parse.py - сбор ссылок на профили компаний

producersMO_parse.py - упаковка в json данных по компаниями


##Команда заполнения БД
py manage.py fill_database -f data

#Запускаем докер
Клонируем репозиторий: git clone https://github.com/Space-dreams/parse_producersMO.git

Переходим в ветку develop: git checkout models

Переходим в папку с файлом docker-compose.yml

Набираем в консоли:
1. docker-compose up -d --build  - собрать и запустить два контейнера

Должно появиться сообщение:
Creating prj_db_1 ... done

Creating prj_web_1 ... done

2. docker-compose exec web python manage.py makemigrations
3. docker-compose exec web python manage.py migrate   - сделать миграции
4. docker-compose exec web python manage.py fill_database  - заполняет базу данных


Не обязательные команды:
4. docker-compose exec web python manage.py createsuperuser  - создает суперпользователя
5. docker volume inspect prj_postgres_data  - проверки создан ли том
6. docker-compose logs -f    -логи



## Описание API:
https://msh777.herokuapp.com/api/v1/regions/ - вернет список регионов

https://msh777.herokuapp.com/api/v1/region/Московская область/ - вернет все записи с регионом Московская область 


https://msh777.herokuapp.com/api/v1/locality/ - вернет список городов

https://msh777.herokuapp.com/api/v1/locality/д. Барабаново/ - вернет все записи с городом д. Барабаново 


https://msh777.herokuapp.com/api/v1/locality/5047112414/ - вернет все записи с ИНН 5047112414


https://msh777.herokuapp.com/api/v1/categories/ - вернет все категории (осторожно их очень много)

https://msh777.herokuapp.com/api/v1/category/Авиатранспорт моторный/ - вернет все записи которые относятся к категории Авиатранспорт моторный


https://msh777.herokuapp.com/api/v1/products/ - вернет все продукты

https://msh777.herokuapp.com/api/v1/product/Посуда пластиковая/ - вернет все записи которые содержат продукт Посуда пластиковая


https://msh777.herokuapp.com/api/v1/api_id/1/ - вернет запись компании по её id

https://msh777.herokuapp.com/api/v1/favourite/ - метод GET вернет все избранные компании для зарегистрированного пользователя

https://msh777.herokuapp.com/api/v1/favourite/ - метод POST добавить список компаний в избранное для данного пользователя.
Список указывать в теле запроса: {
    "favourite": [5, 4]
}

https://msh777.herokuapp.com/api/v1/favourite/ - метод DELETE удалит список компаний из избранных для данного пользователя.
Список указывать в теле запроса: {
    "favourite": [5, 4]
}

https://msh777.herokuapp.com/api/v1/find/ - метод GET - возвращает результаты поиска по полям: если введен ИНН, то ищет по полю ИНН,
если что-то другое - то ищет по полям компания, категория, продукт, регион, город, адрес. 
Пример https://msh777.herokuapp.com/api/v1/find/?find=Корсарус

https://msh777.herokuapp.com/api/v1/last/ - метод GET - возвращает последний запрос пользователя

https://msh777.herokuapp.com/api/v1/quantity/ - метод GET - возвращает количество компаний и количество продуктов в БД

https://msh777.herokuapp.com/api/v1/analitics/categories/ - метод GET - возвращает количество компаний в каждой категории (только 20 самых больших категорий)

https://msh777.herokuapp.com/api/v1/analitics/directions/ - метод GET - возвращает количество компаний по каждому направлению (только 20 самых больших направлений)

https://msh777.herokuapp.com/api/v1/analitics/locality/ - метод GET - возвращает количество компаний в каждом городе (только 20 самых больших городов)


http://127.0.0.1:8000/api/v1/auth/ - регистрация и аутентификация

- про все эндпоинты инфа тут https://djoser.readthedocs.io/en/latest/base_endpoints.html
- пример запроса регистрации - POST на http://127.0.0.1:8000/api/v1/auth/users/ username=user, password=password, 
email=mail@mail.ru
- пример логин на сайт - POST на http://127.0.0.1:8000/api/v1/auth/token/login/ username=user, password=password
- - получаем значение токена "auth_token": "l3wg423l42345h235l2354hh2453l5" <- токен взят рандомный для примера
- в запросах GET/POST/... где требуется аутентификация писать (ПРИМЕР) - "Token l3wg423l42345h235l2354hh2453l5"
