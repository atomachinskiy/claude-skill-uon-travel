# U-On → Telegram Bridge

Минимальный receiver, который перекладывает webhook-события U-On напрямую в Telegram-чат. Без БД, без UI, без серверов — деплой на Cloudflare Worker, Vercel или Deno Deploy.

Идеально для **индивидуального турагента**, который хочет получать в личный чат все события CRM.

## Что присылает

```
🔔 U-On: Создание заявки (type=2)
📋 Заявка #1234
👤 Клиент Иванов Иван (+7…)
💰 50 000 ₽
🔗 Открыть в CRM
```

Каждое событие — отдельное сообщение. Формат — MarkdownV2 с эмодзи.

## Деплой — вариант 1: Cloudflare Worker

```bash
cd webhook-receivers/telegram-bridge
cp wrangler.toml.example wrangler.toml
wrangler secret put TELEGRAM_BOT_TOKEN
wrangler secret put TELEGRAM_CHAT_ID
wrangler deploy
```

## Деплой — вариант 2: Deno Deploy

```bash
# main.ts уже готов под Deno
deno deploy main.ts --project=uon-telegram-bridge
```

## Деплой — вариант 3: Vercel

```bash
# Папку telegram-bridge можно импортировать в Vercel напрямую как Edge Function
vercel
```

## Регистрация в U-On

```bash
cd ../..
./scripts/register-all-webhooks.sh https://uon-tg-bridge.<your>.workers.dev/

# Или только критичные события (заявка/платёж/оплачено)
./scripts/register-all-webhooks.sh https://uon-tg-bridge.<your>.workers.dev/ --types 2,9,17,40,59
```

## Получить бот-токен и chat_id

1. Создать бота через [@BotFather](https://t.me/BotFather), получить `TELEGRAM_BOT_TOKEN`
2. Написать боту любое сообщение
3. Открыть `https://api.telegram.org/bot<TOKEN>/getUpdates` — там виден `chat.id`

## Лимиты

- Telegram: 30 сообщений/сек на бота. Если у вас не сотни заявок в час — норма.
- Cloudflare Worker free: 100k запросов/день
- Deno Deploy free: 100k запросов/день
