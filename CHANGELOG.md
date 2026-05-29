# Changelog

Все важные изменения этого проекта документируются здесь. Формат — [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/). Семантическое версионирование — [SemVer](https://semver.org/lang/ru/).

## [1.0.0] — 2026-05-29

Первый стабильный релиз. Полное покрытие read+write+webhooks+BI на чистом Python без зависимостей.

### Добавлено

**MVP — Read API**
- `_common.sh` и `_common.py` — общая логика (auth через env/secret-file, throttle 150ms, error handling)
- `cli.py` — единая CLI `uon` с 12 главными подкомандами
- `scripts/uon` — тонкая bash-обёртка
- Read-only команды: `leads list/get/by-client`, `requests list/get/by-client/closed/updated`, `users list/get/find`, `payments list/get`, `managers list`, `statuses {requests|leads|pay|cb}`, `sources list`, `webhooks list`

**Write API**
- `leads create`, `requests create/update`, `users create/update`, `services add/update/delete/types`, `payments create/update/delete/forms`, `paydocs create/delete`, `tourists-requests add/remove`, `actions create`, `deadlines create/delete`, `webhooks create/delete`, `reminders create`
- Escape hatch `raw get/post` для неизвестных endpoint-ов

**Webhooks**
- `scripts/register-all-webhooks.sh` — массовая регистрация 69 типов на один URL, с фильтром `--types 2,9,17`
- `webhook-receivers/cloudflare-worker/` — JS Worker, free до 100k req/day, опц. KV-хранилище + TG/общий форвард
- `webhook-receivers/fastapi/` — Python receiver с SQLite-историей, Dockerfile + docker-compose, эндпоинты `/uon-webhook`, `/events`, `/events/{type_id}`, `/health`
- `webhook-receivers/n8n/` — JSON-template для импорта в n8n, готовый switch по type_id с ветками «Новая заявка»/«Платёж»/«Смена статуса»
- `webhook-receivers/telegram-bridge/` — минимальный TS для индивидуального турагента, форвард в личный TG-чат (Cloudflare/Deno/Vercel)

**BI / аналитика**
- `scripts/stats.py funnel` — воронка lead→request→won, опц. `--by-source`
- `scripts/stats.py revenue` — выручка по `--group manager|office|source`
- `scripts/stats.py avg-check` — средний чек, медиана, min/max
- `scripts/stats.py cycle` — среднее время от lead до won
- `scripts/stats.py churn` — топ причин отказа
- `scripts/stats.py overdue` — список просроченных по оплате заявок
- `scripts/stats.py html-report` — единый HTML-отчёт в стиле offer.html

**Документация**
- `SKILL.md` — описание для Claude Code, триггеры, команды
- `README.md` — для GitHub-аудитории
- `BACKLOG.md` — что ещё не сделано (доп. ресурсы, тесты, examples)
- `references/auth.md` — авторизация, whitelist, лимиты
- `references/endpoints.md` — полный каталог 150 операций по семействам
- `references/fields.md` — автодок полей POST-запросов
- `references/conventions.md` — 15 эмпирических подводных камней API
- `references/lifecycle.md` — жизненный цикл Lead→Request→Service→Payment с диаграммой и минимальным create-flow
- `references/statuses.md` — справочники статусов с маппингом на флаги BI
- `references/webhook-events.md` — все 69 событий с полями payload

### Протестировано

Все write-команды end-to-end на боевом кабинете U-On `id72529`:
- 1 lead создан (id=1)
- 1 request создан (id=2) со связанным клиентом, датами тура, услугой-отелем (Hilton Hurghada, 50k/40k), платежом-предоплатой (30k руб), дедлайном на доплату (20k руб к 2026-06-15), касанием-комментарием
- Status update 2 → "В работе" работает через `request_status_id`
- 3 типа webhook-ов зарегистрированы + удалены (приёмка/cleanup)
- BI funnel/revenue/html-report — сгенерировано

[1.0.0]: https://github.com/atomachinskiy/claude-skill-uon-travel/releases/tag/v1.0.0
