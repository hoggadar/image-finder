# Image Loader Service

Сервис для загрузки изображений из очереди RabbitMQ в хранилище MinIO.

## Описание

Асинхронный сервис, который читает сообщения из очереди RabbitMQ и загружает изображения в MinIO объектное хранилище.

## Функциональность

- Чтение сообщений из очереди `image_upload_queue`
- Загрузка изображений в MinIO bucket `images`
- Организация файлов по пользователям: `{user_id}/{uuid}.{extension}`

## Конфигурация

Настройки задаются через переменные окружения с префиксом `CONFIG__`:

### RabbitMQ
- `CONFIG__RABBITMQ__HOST` - хост RabbitMQ
- `CONFIG__RABBITMQ__PORT` - порт RabbitMQ (по умолчанию: 5672)
- `CONFIG__RABBITMQ__USER` - пользователь RabbitMQ (по умолчанию: guest)
- `CONFIG__RABBITMQ__PASSWORD` - пароль RabbitMQ (по умолчанию: guest)

### MinIO
- `CONFIG__MINIO__ENDPOINT` - endpoint MinIO
- `CONFIG__MINIO__ACCESS_KEY` - access key
- `CONFIG__MINIO__SECRET_KEY` - secret key
- `CONFIG__MINIO__SECURE` - использовать TLS (по умолчанию: false)
- `CONFIG__MINIO__BUCKET_NAME` - имя bucket (по умолчанию: images)

## Запуск

```bash
poetry install
poetry run python src/image_loader_service/main.py
```

Или через Docker:

```bash
docker build -t image-loader-service .
docker run image-loader-service
```

