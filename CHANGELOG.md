# Changelog

Все важные изменения этого проекта документируются здесь. Формат — [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/). Семантическое версионирование — [SemVer](https://semver.org/lang/ru/).

## [1.3.0] — 2026-05-29

После аудита покрытия выяснилось: из 150 endpoint-ов прямой командой
покрыто было 104 (~70%). Закрыл все кроме 🔵 "Я-оператор" каталога —
прямое покрытие теперь **141/150 (94%)**.

### Добавлено в 🔴 ВАЖНОЕ

- `reminders list/get/by-request/close` — полный жизненный цикл задач
- `paydocs get/list/update` — полный CRUD счетов в платежах
- `request-files attach/delete` + `user-files attach` — прикрепление
  файлов по URL (документы, сканы паспортов)
- `webhooks update` — теперь можно менять URL/метод без удаления
- `managers create` — добавление сотрудника в кабинет (роль фиксирована: 2)
- `payments other-types` — справочник косвенных платежей
- `documents generate` — генерация документов из шаблонов U-On
  (5=Договор, 13=Лист брони, 14=Расчёт, 15=Счёт), форматы text/doc/pdf,
  8 локалей, опц. печать-и-подпись

### Добавлено в 🟡 СРЕДНЕЕ

- `bcards create/activate/bonus/history-by-card/history-by-user` — полная
  программа лояльности (выпуск, активация, начисление/списание баллов,
  история операций)
- `mail send` — отправка писем через CRM
- `chat send` — внутренний чат между менеджерами и туристами
- `notifications list/get/create` — всплывающие уведомления менеджерам
- `cash list/create` — кассы для платежей
- `bills list/get` — счета для бухгалтерской отчётности
- `service-price create/update/delete` — сезонные цены отеля
  (взрослый/ребёнок/младенец × нетто/цена клиенту)
- `user-cabinet create` — создание ЛК туристу

### Добавлено в 🟢 СПРАВОЧНИКИ

- `sources list/create` — источники обращений (gotcha: поле `rs_name`, не `name`!)
- `travel-types list/create` — типы поездок
- `nutrition list/create/update` — типы питания
- `countries list/create/update` — страны
- `cities list/create/update` — города (с фильтром по стране)
- `suppliers type-create` — типы партнёров

### Тесты

22 новых теста для новых команд. Итого 63 (было 41). Все зелёные.

### Документация

- `COVERAGE.md` — полный аудит покрытия 150 endpoint-ов с разбиением
  по категориям важности.

## [1.2.0] — 2026-05-29

### Добавлено

**v1.1 (частично)**
- `calls log/list/by-request/by-user` — интеграция с телефонией (Mango/UIS/Sipuni). Поля: direction, duration, record_link, start.
- `hotels list/get/create/update/delete` — каталог отелей. Поля: name, stars, address, country/city.
- `suppliers list/get/create/update` + `suppliers types` — поставщики/туроператоры. 5 дефолтных типов.

**v1.2**
- `tests/conftest.py` — pytest-фикстура с моком urlopen, реалистичные replay-фикстуры из живого кабинета.
- `tests/test_common.py` (6) + `tests/test_cli_commands.py` (24) — 30 тестов, проверяют URL paths и POST body field names, в т.ч. критичные gotcha (request_status_id vs status_id, type_id vs type, cio_id обязателен, summ vs amount).
- `tests/fixtures/` — 10 реальных JSON-ответов из кабинета.
- `pyproject.toml` — ruff config (E/F/I/B/UP, line=110) + pytest config.
- `.github/workflows/test.yml` — matrix на py3.11/3.12, ruff + pytest + shellcheck. Зелёный badge в README.

### Изменено

- `scripts/cli.py` вырос с 718 до ~900 строк (добавлены 13 новых команд).
- 19 авто-фиксов от ruff (импорты, `Optional` → `X | None`).

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

[1.3.0]: https://github.com/atomachinskiy/claude-skill-uon-travel/releases/tag/v1.3.0
[1.2.0]: https://github.com/atomachinskiy/claude-skill-uon-travel/releases/tag/v1.2.0
[1.0.0]: https://github.com/atomachinskiy/claude-skill-uon-travel/releases/tag/v1.0.0
