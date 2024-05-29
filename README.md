<h1 align="center">API: Сервис поиска ближайших машин для перевозки грузов 🚚</h1>

<div align="center">

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)](http://www.celeryproject.org/)
[![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)](https://python-poetry.org/)


</div>

Выполнено в рамках [тестового задания](https://storlay.notion.site/web-Python-38a5c9972a2c47fd8c5261084f4421d8?pvs=4)

## Основные возможности

1. **Создание нового груза**
    - Указание локаций pick-up и delivery, веса и описания груза.
    - Локации определяются по введенному zip-коду.

<br>

2. **Получение списка грузов**
    - Включает локации pick-up и delivery, количество ближайших машин (<= 450 миль).

<br>

3. **Получение информации о конкретном грузе по ID**
    - Включает локации pick-up и delivery, вес, описание.
    - Список всех машин с расстоянием до выбранного груза (в милях).

<br>

4. **Редактирование машины по ID**
    - Изменение локации (определяется по введенному zip-коду).

<br>

5. **Редактирование груза по ID**
    - Изменение веса и описания груза.

<br>

6. **Удаление груза по ID**

<br>

7. **Фильтр списка грузов**
    - Фильтрация по весу и расстоянию до ближайших машин.

<br>

8. **Автоматическое обновление локаций всех машин**
    - Локации всех машин обновляются на другие случайные каждые 3 минуты.

## Установка и запуск

1. Склонируйте репозиторий:

```
git clone https://github.com/storlay/search_nearest_cars.git
```

2. При необходимости измените содержимое файла `.env-example`

```
POSTGRES_DB=your_postgres_db
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
```

3. Запустите проект с помощью Docker Compose*:

```
docker-compose up --build
```

> *При запуске приложение автоматически загружает и заполняет базу данных списком уникальных локаций
> из файла `app/data/uszips.csv` и создаёт 20 машин со случайными локациями.

4. Приложение будет доступно по адресу http://127.0.0.1:8000

## Использование

- **Документация API** доступна по адресам:
    - http://127.0.0.1:8000/docs (Swagger)
    - http://127.0.0.1:8000/redoc (Redoc)

- **Мониторинг и управление фоновыми задачами** доступно по адресу:
    - http://127.0.0.1:5555 (Flower)