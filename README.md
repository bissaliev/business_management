# Business Management: Микросервисная система управления сотрудниками и задачами

Business Management — это микросервисное приложение для управления организационной структурой, задачами, встречами и календарем сотрудников. Обеспечивает гибкое взаимодействие между сервисами с использованием REST API, JWT-аутентификации и API Key для межсервисного общения.

## Архитектура

Проект состоит из следующих микросервисов, каждый из которых выполняет специализированную функцию:

### User Service

Управляет пользователями, их статусом доступа (admin, user) и JWT-токенами.
Предоставляет эндпоинт `/auth/verify-token` для проверки токенов.
Хранит данные о принадлежности пользователей к командам (team_id).

### Team Service

Управляет командами, их составом и ролями участников.
Позволяет создавать, обновлять и удалять команды, а также назначать администраторов.
Создание информационных сообщений для команды.
Использует SQLAdmin для административного интерфейса с аутентификацией через User Service.

### Org Structure Service

Управляет организационной структурой: департаменты, команды, дивизии, сотрудники.
Работники привязаны к департаментам, которые связаны с командами.
Ограничивает действия над сотрудниками администраторам соответствующих команд.

### Task Service

Управляет задачами сотрудников (создание, обновление, удаление).
Интегрируется с Calendar Service через вебхуки для синхронизации задач.
Использует SQLAdmin для административного интерфейса с аутентификацией через User Service.

### Meeting Service

Управляет встречами сотрудников, включая создание, обновление и удаление.
Проверяет доступность участников и синхронизирует встречи с Calendar Service через вебхуки.

### Calendar Service

Хранит и управляет событиями календаря (встречи, задачи).
Принимает вебхуки от Meeting Service и Task Service для создания/удаления событий.
Использует проверку API Key для доступа управления событиями через вебхуки.

## Технологии

Backend: Python, FastAPI, SQLAlchemy (Async), Pydantic
Базы данных: PostgreSQL (хранение данных)
Обратный прокси: Nginx (маршрутизация и балансировка нагрузки)
Контейнеризация: Docker, Docker Compose
Аутентификация: JWT, API Key
Миграции: Alembic
Админ-панель: SQLAdmin
Межсервисное взаимодействие: HTTPX (для межсервисных запросов)
Документация: OpenAPI/Swagger

Требования

Python 3.10+
Docker и Docker Compose
PostgreSQL 15
Nginx

Установка и запуск

Клонируйте репозиторий:

```bash
git clone git@github.com:bissaliev/business_management.git
cd business_management/
```

Настройте переменные окружения:

Скопируйте `.env.example` в `.env` для каждого сервиса:

```bash
cp auth_service/.env.example auth_service/.env
cp teams_service/.env.example teams_service/.env
cp org_structure_service/.env.example org_structure_service/.env
cp tasks_service/.env.example tasks_service/.env
cp meetings_service/.env.example meetings_service/.env
cp calendar_service/.env.example calendar_service/.env
```

Запустите сервисы:

```bash
docker-compose up --build
```

При выполнении команды контейнеры выполнят скрипты entrypoint.sh, которые выполнят миграции, загрузят некоторые фикстуры и запустят приложения.

Доступ к сервисам:

[User Service](http://localhost/users/)
[Team Service](http://localhost/teams/)
[Org Structure](http://localhost/org/)
[Task Service](http://localhost/tasks-service/)
[Meeting Service](http://localhost/meeting-service/)
[Calendar Service](http://localhost/calendar-service/)

### Доступ к админ-панели

Для входа в административный кабинет введите:

username: `admin@admin.com`

password: `admin`

Административный кабинет пользователей:

[http://localhost/users/admin](http://localhost/users/admin/)

Административный кабинет команд:

[Откройте http://localhost/teams/admin/](http://localhost/teams/admin/)

Административный кабинет задач:

[Откройте http://localhost/tasks-service/admin/](http://localhost/tasks-service/admin/)

Введите JWT-токен в поле Username

### Просмотр документации API

Откройте `/docs` для каждого сервиса, например:

Документация приложения пользователей:

[http://localhost/user/docs](http://localhost/users/docs)

Документация приложения команд:

[http://localhost/teams/docs](http://localhost/teams/docs)

Документация приложения организационной структуры команд:

[http://localhost/org/docs](http://localhost/org/docs)

Документация приложения задач:

[http://localhost/tasks-service/docs](http://localhost/tasks-service/docs)

Документация приложения встреч:

[http://localhost/meeting-service/docs](http://localhost/meeting-service/docs)

Документация приложения событий:

[http://localhost/calendar-service/docs](http://localhost/calendar-service/docs)
