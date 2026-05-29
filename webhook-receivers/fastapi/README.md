# U-On Webhook Receiver — FastAPI

Python/FastAPI receiver для запуска на любом VPS. Хранит события в SQLite, опционально пересылает в Telegram / общий webhook.

## Деплой через Docker

```bash
cd webhook-receivers/fastapi
cp .env.example .env
# Отредактировать .env (PORT, TELEGRAM_*, FORWARD_URL)
docker compose up -d
```

Сервер слушает на `0.0.0.0:8000`. Поставьте Nginx/Caddy впереди для HTTPS, или используйте Cloudflare Tunnel.

## Прямой запуск (без Docker)

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Регистрация в U-On

```bash
cd ../..
./scripts/register-all-webhooks.sh https://your-domain.com/uon-webhook
```

## API

| Метод | Путь | Что |
|-------|------|-----|
| `POST /uon-webhook` | Приём событий от U-On |
| `GET /events` | Последние 100 событий (для отладки) |
| `GET /events/{type_id}` | События по типу |
| `GET /health` | Health-check |

## Что хранится

SQLite-таблица `events`:
- `id` INTEGER PK
- `type_id` INTEGER (1..74)
- `event_name` TEXT
- `uon_id` INTEGER (кабинет)
- `payload_json` TEXT (полный payload)
- `received_at` TIMESTAMP

История очищается по cron'у через 30 дней (можно отключить в `.env`).

## Конфигурация

`.env`:

```
PORT=8000
TELEGRAM_BOT_TOKEN=     # опц., форвард в TG
TELEGRAM_CHAT_ID=       # опц.
FORWARD_WEBHOOK_URL=    # опц., общий URL для пересылки
KEEP_DAYS=30            # хранить события сколько дней
```
