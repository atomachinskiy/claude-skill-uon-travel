# U-On Webhook Receiver — Cloudflare Worker

Самый дешёвый и быстрый способ принимать webhook-события U-On.Travel CRM. Worker бесплатный до 100 000 запросов в день, деплой за 2 минуты, без VPS.

## Что делает

1. Принимает любой webhook от U-On (POST или GET).
2. Парсит payload (форма или query-string).
3. Логирует в Cloudflare KV-хранилище (опц.).
4. Опционально форвардит в Telegram-чат / Slack / Discord / Notion / Sheets / любой webhook.

## Быстрый старт

```bash
npm install -g wrangler
cd webhook-receivers/cloudflare-worker
cp wrangler.toml.example wrangler.toml
# Отредактировать wrangler.toml (account_id, secrets)
wrangler login
wrangler deploy
```

После деплоя у вас появится URL вида `https://uon-webhook-receiver.<your-name>.workers.dev`.

Регистрируем его в U-On:

```bash
cd ../..
./scripts/register-all-webhooks.sh https://uon-webhook-receiver.<your-name>.workers.dev/
```

Или конкретные события через `--types`:

```bash
# Только заявки и платежи
./scripts/register-all-webhooks.sh https://uon-webhook-receiver.<your-name>.workers.dev/ --types 2,17,9,10
```

## Конфигурация

В `wrangler.toml` задаём:

- `KV_NAMESPACE` — для хранения последних N событий (опц.)
- секрет `TELEGRAM_BOT_TOKEN` — если хотим форвардить в TG
- секрет `TELEGRAM_CHAT_ID` — куда форвардить
- секрет `FORWARD_WEBHOOK_URL` — общий URL для форварда (если нужен)

Секреты заводятся через `wrangler secret put TELEGRAM_BOT_TOKEN`.

## Что внутри payload U-On

Все вебхуки приходят с одинаковыми системными полями:

```
uon_id          — ID кабинета (например 72529)
uon_subdomain   — поддомен (id72529)
datetime        — Y-m-d H:i:s
type_id         — номер события (1..74)
```

Плюс специфичные для типа поля (см. `references/webhook-events.md`). Worker не интерпретирует payload — просто прокидывает дальше.

## Тестирование локально

```bash
wrangler dev
# в другом терминале:
curl -X POST http://localhost:8787/ -d 'type_id=2&uon_id=72529&request_id=999'
```

## Лимиты Cloudflare Workers Free

- 100 000 запросов/день (для большинства турагентств с запасом)
- 10ms CPU/запрос (наш receiver ~2ms)
- 1MB body (вебхуки U-On < 10KB)
- KV: 100k reads/день, 1k writes/день

Если упрётесь в лимиты — переходите на FastAPI receiver.
