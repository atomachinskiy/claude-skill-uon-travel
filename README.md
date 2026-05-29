# claude-skill-uon-travel

Skill для Claude Code и Claude Desktop, дающий полный доступ к публичному API **[U-On.Travel CRM](https://u-on.ru)** — туристической CRM номер один в РФ.

- 150 операций (read + write) в 42 ресурс-семействах
- 69 типов webhook-событий с подпиской через API
- Статический API-ключ — без OAuth, без refresh-токенов
- 4 готовых webhook-receiver-а (Cloudflare Worker, FastAPI, n8n template, Telegram-bridge)
- BI-скрипты для воронки lead→request→won

> **MIT-лицензия.** Форкайте, дорабатывайте, используйте в коммерческих интеграциях.

---

## Быстрый старт

```bash
git clone https://github.com/atomachinskiy/claude-skill-uon-travel.git ~/.claude/skills/uon-travel
cd ~/.claude/skills/uon-travel
cp config/.env.example config/.env
# Положить UON_API_KEY=... в config/.env
ln -s "$PWD/scripts/uon" ~/.local/bin/uon   # опционально, для удобства

uon managers list
uon statuses requests
uon users find --phone +79991234567
uon leads list --from 2026-05-01 --to 2026-05-29
```

---

## Что внутри

```
claude-skill-uon-travel/
├── SKILL.md                    — описание скилла, триггеры, команды
├── README.md                   — этот файл
├── LICENSE                     — MIT
├── config/
│   └── .env.example            — UON_API_KEY=...
├── scripts/
│   ├── _common.sh / _common.py — общая логика (auth, throttle, errors)
│   ├── cli.py                  — единая CLI uon с подкомандами
│   └── uon                     — тонкая bash-обёртка над cli.py
├── references/
│   ├── auth.md                 — как выпустить ключ, whitelist, лимиты
│   ├── endpoints.md            — все 150 операций по семействам
│   ├── statuses.md             — дефолтные статусы заявок/обращений/оплат
│   └── webhook-events.md       — 69 типов событий с полями payload
└── webhook-receivers/          — готовые приёмники (cf-worker, fastapi, n8n, tg)
```

---

## Получить API-ключ

1. Создать кабинет на [u-on.ru](https://u-on.ru) (есть 14-дневный триал)
2. Зайти в **Настройки → Интеграции → API**
3. Создать ключ, **поставить галочки POST и GET**
4. Скопировать ключ при создании (потом доступа к нему нет)

Подробности — [`references/auth.md`](references/auth.md).

---

## Кому это

| Сценарий | Что даёт |
|----------|----------|
| Перформанс-агентство интегрирует CRM клиентов | Sync с Sheets, BI, AmoCRM, Bitrix24 без no-code-платформ |
| Разработчик AI-ассистента для турагента | Управление CRM на естественном языке через Claude |
| Команда строит дашборды по воронке | BI-скрипты + подписка на 69 событий в реалтайме |

Не подходит для: одиночных турагентов без программистов (для них есть [Albato](https://albato.ru/app-uon) или [APInita](https://apinita.ru)).

---

## Roadmap

- [x] **v1.0** MVP read-only + полная write API + bulk-регистрация 69 webhook-типов + 4 receiver-пакета + BI/stats + 7 reference-документов
- [ ] **v1.1** Расширение: hotels/suppliers/bonuses/avia/insurance CRUD
- [ ] **v1.2** Записанные фикстуры (replay-tests), CI на GitHub Actions
- [ ] **v1.3** Примеры интеграций: Sheets, Notion, AmoCRM, Bitrix24

См. [`BACKLOG.md`](BACKLOG.md) для деталей.

---

## Спасибы

- [@EvilFreelancer](https://github.com/EvilFreelancer) — за [PHP-клиент](https://github.com/DrTeamRocks/uon), из которого взяты модели полей
- Команде U-On.Travel за открытое API и подробную документацию
