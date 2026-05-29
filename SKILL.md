---
name: uon-travel
description: Работа с публичным API U-On.Travel CRM — туристическая CRM номер один в РФ для турагентств, туроператоров и сетей. Полное покрытие 150 операций (read+write): обращения и заявки, туристы, платежи и счета, услуги в заявке (туры, авиа, отели, страховки, питание, визы), напоминания, файлы, кассы, бонусные карты, поставщики, документы, чат и звонки. Подписка на 69 типов webhook-событий. Используй когда клиент работает в U-On и просит проанализировать воронку, найти туриста, посмотреть заявки за период, выставить счёт, создать заявку или обращение, поставить напоминание, подключить телефонию, сделать BI-отчёт или подписаться на события CRM.
allowed-tools: Bash, Read, Write, Edit
---

# U-On.Travel API skill

Тонкий клиент к публичному REST API U-On.Travel ([api.u-on.ru](https://api.u-on.ru/doc)) — туристическая CRM #1 в РФ (с 2013, Москва). Покрывает 150 операций в 42 ресурс-семействах + 69 типов вебхуков, статический API-ключ без OAuth.

> **Кому это:** перформанс-агентствам которые интегрируют CRM турагентств с сайтами/мессенджерами/Sheets/BI, разработчикам AI-ассистентов внутри Claude Code для турагентов, командам которые строят аналитические дашборды по воронке заявок и хотят слушать события CRM в реалтайме без opla-no-code-платформ.

---

## КОГДА ТРИГГЕРИТЬСЯ

**Чтение / аналитика**
- «Покажи активные заявки за неделю / месяц»
- «Какие обращения сейчас в работе по источнику Instagram?»
- «Сколько заявок закрыто в мае с конверсией»
- «Покажи платежи за июнь — кто оплатил, кто нет»
- «Сколько обращений у менеджера N»
- «Найди туриста Иванова по телефону / email»
- «Покажи историю заявок клиента X»
- «Все напоминания на сегодня у менеджера Y»

**Запись / автоматизация**
- «Создай обращение в U-On от Telegram-чата / с сайта»
- «Создай нового туриста с телефоном +7...»
- «Заведи заявку, привяжи туриста, добавь услугу-отель»
- «Поставь напоминание перезвонить клиенту завтра в 11»
- «Обнови статус заявки 12345 на "Подтверждена"»
- «Зарегистрируй счёт в платеже / отметь оплату»

**Webhooks (подписка на события CRM)**
- «Подключи U-On к нашему n8n / Cloudflare Worker / FastAPI / Telegram-боту»
- «Хочу получать уведомление каждый раз когда создаётся новая заявка»
- «Слушай событие "Изменение статуса в заявке" → пиши в Notion»
- «Получи уведомление при оплате заявки → отправь чек в Точку»

**BI / отчётность**
- «Сделай отчёт по воронке lead→request→won за месяц»
- «Выручка по менеджерам, средний чек, время цикла сделки»
- «Топ источников по конверсии»
- «Кто не оплатил вовремя — список просроченных заявок»

---

## БЫСТРЫЙ СТАРТ

### 1. Получить API-ключ в U-On

1. Зарегистрировать кабинет на [u-on.ru](https://u-on.ru) (есть 14-дневный триал).
2. Зайти в **Настройки → Интеграции → API**.
3. Нажать «Добавить новый API-ключ».
4. **Обязательно отметить чекбоксы POST и GET** — без этого API недоступен.
5. Опционально добавить IP в whitelist (для повышенной безопасности).
6. **Скопировать ключ сразу** — он показывается только при создании.

### 2. Установка скилла

```bash
git clone https://github.com/atomachinskiy/claude-skill-uon-travel.git ~/.claude/skills/uon-travel
cp ~/.claude/skills/uon-travel/config/.env.example ~/.claude/skills/uon-travel/config/.env
# Положить ключ в config/.env (UON_API_KEY=...)
# либо в ~/.claude/secrets/uon-api-key (скилл автоматически подхватит)
```

### 3. Первая команда

```bash
cd ~/.claude/skills/uon-travel
python3 scripts/cli.py managers list
python3 scripts/cli.py statuses requests
python3 scripts/cli.py statuses leads
```

Если видишь JSON с менеджерами и статусами — скилл работает.

---

## АРХИТЕКТУРА API

### Base URL и формат

```
https://api.u-on.ru/{key}/<endpoint>.{json|xml}
```

Ключ — часть URL, не header. Формат ответов через расширение в URL (`.json` или `.xml`). Скилл всегда работает в JSON.

### Авторизация

- Статический API-ключ выпускается в кабинете.
- Один ключ = один кабинет, ролевой модели нет.
- IP-whitelist опционален (рекомендую для production).
- Включаются галочки POST/GET — иначе соответствующие методы вернут 403.

### Ограничения

- Лимит — **10 запросов в секунду**. Скилл соблюдает через throttle 150ms между вызовами.
- Sandbox **нет** — тестируем на боевом кабинете или триальном U-On.
- Версионирования API нет, изменения ловим по реальным ответам.

### Иерархия сущностей

```
Lead (обращение)        → создаётся первым (с сайта/мессенджера/звонка)
   └─ конвертируется в
Request (заявка / тур)  → содержит туриста + услуги + платежи
   ├─ Tourists          → 1+ туристов привязаны к заявке
   ├─ Services          → отель, авиа, страховка, питание, виза, трансфер
   ├─ Payments          → платежи клиента → внутри PayDocs (счета)
   └─ Files / Documents → паспорта, ваучеры, договоры
```

---

## ОСНОВНЫЕ КОМАНДЫ

Все примеры — через `python3 scripts/cli.py <subcommand>`. Можно повесить на алиас `uon`.

### Обращения (leads)

```bash
uon leads list --from 2026-05-01 --to 2026-05-29
uon leads list --from 2026-05-01 --to 2026-05-29 --source-id 5
uon leads updated --from 2026-05-28 --to 2026-05-29   # только обновлённые
uon leads get 12345
uon leads by-client 678
uon leads create --name Иван --phone +79991234567 --source-id 1 --text "С сайта"
```

### Заявки (requests)

```bash
uon requests list --from 2026-05-01 --to 2026-05-29
uon requests list --from 2026-05-01 --to 2026-05-29 --closed
uon requests list --from 2026-05-01 --to 2026-05-29 --updated
uon requests get 12345
uon requests by-client 678
```

### Туристы (users)

```bash
uon users list
uon users get 678
uon users find --phone +79991234567
uon users find --email test@example.com
uon users create --name Иван --surname Иванов --phone +79... --email i@example.com
```

### Платежи

```bash
uon payments list --from 2026-05-01 --to 2026-05-29
uon payments get 999
```

### Справочники

```bash
uon managers list
uon managers list --office-id 2
uon statuses requests   # все статусы заявок
uon statuses leads      # статусы обращений
uon statuses pay        # статусы оплаты
uon sources --list
```

### Webhooks

```bash
uon webhooks list
uon webhooks create --type 2 --url https://example.com/wh --note "Создание заявки"
uon webhooks delete 12
```

Полный список 69 типов событий — см. [`references/webhook-events.md`](references/webhook-events.md).

### Напоминания

```bash
uon reminders create --request-id 12345 --text "Перезвонить" \
  --from "2026-05-30 11:00:00" --to "2026-05-30 11:30:00"
```

### Звонки (телефония)

```bash
uon calls log --phone "+79991234567" --inbound --duration 180 --note "Клиент уточнил детали"
uon calls log --phone "+79991234567" --record "https://my-pbx.example.com/rec/123.mp3"  # исходящий
uon calls list --page 1
uon calls by-request 123
uon calls by-user 678
```

### Отели и поставщики

```bash
uon hotels list
uon hotels get 5
uon hotels create --name "Hilton Resort" --stars 5 --country-id 1 --city-id 1
uon hotels update 5 --note "Обновили описание"
uon hotels delete 5 --confirm

uon suppliers types        # 1=Авиа, 2=Страховые, 3=Транспорт, 4=Туроператоры, 5=Турагентства
uon suppliers list
uon suppliers create --name "Pegas Touristik" --type-id 4 --inn 7704123456 --phone "+74951234567"
```

### Сырые вызовы (escape hatch)

```bash
uon raw get "company-office"
uon raw post "service/create" -F r_id=12345 -F type=1 -F price_client=50000
```

### Создание заявок

```bash
uon requests create --name Иван --phone +79991234567 \
    --date-begin "2026-07-01 00:00:00" --date-end "2026-07-08 00:00:00" \
    --note "Турция all-inclusive"
uon requests update 123 --status-id 2   # перевод в "Подтверждена"
uon requests update 123 -F manager_id=5 # любое поле
```

### Услуги в заявке

```bash
uon services types          # справочник типов (1=Отель, 2=Трансфер, ...)
uon services add --request-id 123 --type 1 \
    --name "Hilton Resort 5*" --price-client 80000 --price-netto 65000 \
    --hotel "Hilton" --city "Анталия" --country "Турция" --tourists-count 2
uon services update 999 --price-client 75000
uon services delete 999 --confirm
```

### Платежи

```bash
uon payments forms          # справочник форм оплаты
uon payments create --request-id 123 --amount 30000 --form-id 1 --direction in --prepay-id 1
uon payments update 555 --amount 35000
uon payments delete 555 --confirm
```

### Привязка туристов и касания

```bash
uon tourists-requests add --request-id 123 --tourist-id 678
uon actions create --request-id 123 --text "Клиент попросил скидку" --type-id 0
uon deadlines create --request-id 123 --amount 50000 --date "2026-06-15" --current
```

### Bulk-регистрация всех webhook-ов

```bash
./scripts/register-all-webhooks.sh https://my-receiver.example.com/
# Или только нужные:
./scripts/register-all-webhooks.sh https://my-receiver.example.com/ --types 2,9,17,40,59
```

### Webhook receivers — выбрать стек

| Стек | Когда | Деплой |
|------|-------|--------|
| `webhook-receivers/cloudflare-worker/` | Без VPS, ≤ 100k req/день, нужно хранение + форвард | `wrangler deploy` |
| `webhook-receivers/fastapi/` | Свой VPS, история в SQLite, аналитика, без лимитов | `docker compose up -d` |
| `webhook-receivers/n8n/` | Есть n8n, нужно роутить события в разные сервисы | Импорт JSON-шаблона |
| `webhook-receivers/telegram-bridge/` | Один турагент, уведомления в личный TG, без серверов | `wrangler deploy` |

### BI / аналитика

```bash
python3 scripts/stats.py funnel --from 2026-05-01 --to 2026-05-31 --by-source
python3 scripts/stats.py revenue --from 2026-05-01 --to 2026-05-31 --group manager
python3 scripts/stats.py avg-check --from 2026-05-01 --to 2026-05-31
python3 scripts/stats.py cycle --from 2026-01-01 --to 2026-05-31     # время от lead до won
python3 scripts/stats.py churn --from 2026-05-01 --to 2026-05-31     # причины отказа
python3 scripts/stats.py overdue --from 2026-01-01 --to 2026-05-29   # просроченные
python3 scripts/stats.py html-report --from 2026-05-01 --to 2026-05-31 -o report.html
```

---

## ОБЫЧНЫЕ ОШИБКИ

| Симптом | Причина | Что делать |
|---------|---------|------------|
| `HTTP 403` | Не отмечены POST/GET в кабинете | Зайти в Настройки → Интеграции → API, поставить галочки |
| `HTTP 404 result:404` | Сущности с таким id нет, или формат `users/{page}` спутан с `user/{id}` | Проверить, что вызывается правильный endpoint |
| `result:200, id:"3"` после POST | Это норма — поле `id` приходит строкой, не числом | Конвертировать на своей стороне |
| Пустой массив `records:[]` | Либо ресурс пустой, либо неправильная пагинация | Сначала проверить базовый список без фильтров |
| Сетевой timeout | IP не в whitelist, либо кабинет в режиме обслуживания | Проверить whitelist или повторить через 30 секунд |

---

## ДАЛЬШЕ ЧИТАТЬ

- [`references/auth.md`](references/auth.md) — детали авторизации и whitelist-а
- [`references/endpoints.md`](references/endpoints.md) — полная таблица всех 150 методов
- [`references/webhook-events.md`](references/webhook-events.md) — 69 типов webhook-событий с полями payload
- [`references/lifecycle.md`](references/lifecycle.md) — жизненный цикл Lead → Request → Service → Payment
- [`references/statuses.md`](references/statuses.md) — структура справочников статусов
- [`webhook-receivers/`](webhook-receivers/) — готовые receiver-ы под Cloudflare Worker, FastAPI, n8n, Telegram-bridge
