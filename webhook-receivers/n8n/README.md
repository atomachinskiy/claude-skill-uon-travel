# U-On Webhook Receiver — n8n template

Импортируйте `uon-webhook-flow.json` в n8n. Получите готовый flow:

```
[Webhook] → [Switch by type_id] → [TG/Sheets/Notion/…]
```

## Импорт

1. Откройте n8n → Workflows → Import from File
2. Выберите `uon-webhook-flow.json`
3. Активируйте workflow
4. Скопируйте Production URL ноды Webhook

## Регистрация в U-On

```bash
cd ../..
./scripts/register-all-webhooks.sh https://your-n8n.example.com/webhook/uon
```

## Что внутри

- Webhook нода слушает `POST /webhook/uon` (или ваш path)
- Switch нода разбирает payload по `type_id`:
  - **2** (создание заявки) → ветка «Новая заявка»
  - **9** (создание платежа) → ветка «Оплата»
  - **16/17** (смена статуса) → ветка «Изменение статуса»
  - **17 + status=4** (Аннулирована) → ветка «Отказ»
  - **default** → лог
- Каждая ветка — заготовка под действие (Slack/TG/Sheets/Notion/Email)

## Кастомизация

Добавьте ветки под другие type_id (см. `references/webhook-events.md` — все 69). Для каждой ветки настраивайте connector под свой стек.
