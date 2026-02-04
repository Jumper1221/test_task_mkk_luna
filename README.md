# Тестовое задание: REST API справочника организаций

Проект демонстрирует реализацию REST API для справочника организаций, зданий и видов деятельности, выполненную на стеке FastAPI + Pydantic + SQLAlchemy + Alembic.

**Стек**

- FastAPI
- Pydantic
- SQLAlchemy (async)
- Alembic
- PostgreSQL + PostGIS
- GeoAlchemy2

**Функциональность**

- Получение списка организаций в конкретном здании
- Поиск организаций по виду деятельности, включая подкатегории
- Поиск организаций по геокоординатам в заданном радиусе
- Поиск организаций по названию
- Получение организации по ID
- Список зданий и получение здания по ID
- Список видов деятельности и получение вида деятельности по ID
- Ограничение глубины дерева деятельностей до 3 уровней
- Документация Swagger UI и Redoc

**Быстрый запуск в Docker**

1. Создайте `.env` на основе `.env.example` и задайте значения `API_KEY` и параметров Postgres.
2. Соберите и запустите сервисы: `docker compose up -d --build`.
3. API будет доступен по адресу `http://localhost:8200/api`.

**Конфигурация**

- `API_KEY` — статический API ключ для доступа к сервису.
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` — параметры подключения к БД.

**Документация API**

- Swagger UI: `http://localhost:8200/api/docs`
- Redoc: `http://localhost:8200/api/redoc`

**Эндпоинты**
Базовый префикс API: `/api`

| Метод | Путь                                  | Описание                                                                                                      |
| ---------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| GET        | `/`                                     | Health check                                                                                                          |
| GET        | `/organizations/{org_id}`               | Информация об организации по ID                                                              |
| GET        | `/organizations/building/{building_id}` | Список организаций в здании                                                                   |
| GET        | `/organizations/activity/{activity_id}` | Список организаций по виду деятельности (с учетом подкатегорий) |
| GET        | `/organizations/search/by-name`         | Поиск организаций по названию, параметр `q`                                       |
| GET        | `/organizations/search/by-location`     | Поиск организаций по координатам, параметры `lat`, `lon`, `radius`        |
| GET        | `/buildings`                            | Список всех зданий                                                                                    |
| GET        | `/buildings/{building_id}`              | Информация о здании по ID                                                                          |
| GET        | `/activities`                           | Список видов деятельности                                                                      |
| GET        | `/activities/{activity_id}`             | Информация о виде деятельности по ID                                                     |

Все запросы требуют заголовок `X-API-Key` со значением из `.env`.

**Примеры запросов**

```bash
curl -H "X-API-Key: your_static_api_key_here" \
  "http://localhost:8200/api/organizations/search/by-name?q=SoftTech"
```

```bash
curl -H "X-API-Key: your_static_api_key_here" \
  "http://localhost:8200/api/organizations/search/by-location?lat=55.7558&lon=37.6173&radius=5"
```

**Тестовые данные**
Миграции создают таблицы и заполняют их примерными данными (дерево деятельностей, здания, организации и телефоны). Примеры категорий: `Еда`, `Автомобили`, `Образование`, `Медицина`, `Технологии`, `Строительство`.

**Тесты**
Для запуска тестов выполните: `pytest`.
