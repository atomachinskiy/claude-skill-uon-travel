# U-On Webhook Receivers

Готовые приёмники webhook-событий U-On.Travel под разные стеки. Выберите свой:

| Стек | Лучше всего для | Сложность |
|------|-----------------|-----------|
| **[Cloudflare Worker](cloudflare-worker/)** | Агентство без VPS, до 100k событий/день, нужно хранение + форвард | Низкая |
| **[FastAPI](fastapi/)** | Свой VPS, история событий в БД, аналитика, без лимитов | Средняя |
| **[n8n template](n8n/)** | Уже есть n8n, надо без кода роутить события в разные сервисы | Низкая |
| **[Telegram-bridge](telegram-bridge/)** | Один турагент, уведомления в личный TG-чат, без серверов | Минимальная |

## Что общего

Все receiver-ы:
- Принимают и POST (form-encoded или JSON), и GET (query-string)
- Возвращают HTTP 200 + краткий JSON
- Парсят `type_id`, `uon_id`, `datetime` и сущности (`request_id`, `client_id`, `price`, `text`)
- Не требуют валидации подписи (U-On пока не поддерживает HMAC)

## Как зарегистрировать receiver в U-On

После деплоя у вас есть URL. Регистрируем все 69 событий за один вызов:

```bash
cd ../..
./scripts/register-all-webhooks.sh https://your-receiver-url.example.com/

# Или только нужные типы
./scripts/register-all-webhooks.sh https://your-receiver.example.com/ --types 2,9,17,40,59
```

Полный список типов — `references/webhook-events.md`.

## Что делать с принятыми событиями

Базовая схема:

```
U-On → Receiver → KV/SQLite (хранение) → форвард в:
                                          ├─ Telegram
                                          ├─ Slack
                                          ├─ Notion
                                          ├─ Google Sheets
                                          ├─ Bitrix24 / amoCRM
                                          └─ Ваш бэкенд
```

Все receiver-ы поддерживают:
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` — форвард в TG
- `FORWARD_WEBHOOK_URL` — пересылка в один общий URL (для своего бэкенда)

n8n template нативно даёт распиновку по типам события для роутинга в любой сервис.

## Безопасность

- U-On не подписывает webhook-ы. Любой, кто узнает URL, может слать события.
- Если URL утёк — обновляйте URL receiver-а и регистрируйте новый в U-On (старый удаляйте через `uon webhooks delete <id>`).
- Для production рекомендуем proxy-секрет: `?token=secret123` в URL, валидация на receiver-е.

## Дебаг: куда смотреть когда receiver «молчит»

`https://idXXXXX.u-on.ru/logs_webhooks.php` — встроенные логи U-On показывают:
- Все исходящие webhook-вызовы с timestamp и type_id
- Полный payload, который ушёл
- HTTP-статус и тело ответа receiver-а
- Retry-логика (U-On переотправляет при HTTP 5xx)

Это первое место для дебага — быстрее, чем разбирать логи на стороне receiver-а. Подробнее в [`references/debugging.md`](../references/debugging.md).
