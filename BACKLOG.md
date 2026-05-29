# Backlog

## ✅ v1.0 — выпущен 2026-05-29

См. [CHANGELOG.md](CHANGELOG.md).

## v1.1 — дополнительные ресурсы (приоритет: средний)

- [ ] `hotels create/update/delete` — управление каталогом отелей
- [ ] `suppliers create/update` — поставщики/туроператоры/ОЦ
- [ ] `bcard create/activate` + `bonuses create` — бонусные карты и баллы
- [ ] `avia create` — детальная разбивка авиаперелётов внутри услуги
- [ ] `mail create` / SMS — отправка писем/SMS вручную
- [ ] `chat-message create` — сообщения в чате CRM
- [ ] `catalog-package` / `catalog-service` — для туроператоров на схеме «Я-оператор»
- [ ] `call_history create` — интеграция с телефонией (CallTracking)
- [ ] `notification create` — всплывающие в кабинете менеджеров

## v1.2 — Тестирование и CI

- [ ] Записанные фикстуры (VCR-style) для replay-тестов без live API
- [ ] Pytest-сюита с фикстурами по каждой команде
- [ ] Smoke-test cycle: lead → request → service → payment → close, на чистом triale
- [ ] GitHub Actions workflow: lint (ruff/shellcheck) + replay-tests + dry-run register-all
- [ ] Coverage badge
- [ ] Pre-commit hooks

## v1.3 — Примеры интеграций

- [ ] `examples/sheets-sync/` — Google Sheets sync (через `google-sheets-skill` + cron)
- [ ] `examples/notion-leads/` — каждый lead → новая страница в Notion базе
- [ ] `examples/amocrm-bridge/` — двусторонняя синхронизация U-On ↔ amoCRM
- [ ] `examples/bitrix24-bridge/` — то же для Bitrix24
- [ ] `examples/tochka-payment/` — заявка → платёжная ссылка Точки → автозакрытие на оплате
- [ ] `examples/telegram-lead-from-bot/` — TG-бот собирает заявку → создаёт lead

## v1.4 — Polish

- [ ] HMAC-валидация webhook-ов (если U-On добавит подпись — пока их нет)
- [ ] Pretty-print таблиц в CLI вместо JSON-дампа (опционально через `--format table`)
- [ ] Прогресс-бар для долгих BI-выгрузок
- [ ] Кэширование статусов/менеджеров/источников в локальном файле (TTL 1 час)
- [ ] CLI completion для bash/zsh/fish

## Идеи на потом

- [ ] AI-режим: `uon assistant` — REPL-сессия, естественный язык → CLI-команды
- [ ] Веб-интерфейс для невладельцев CLI (Streamlit/Gradio)
- [ ] Telegram-бот для турагента (CRUD заявок прямо из чата)
- [ ] Превратить в **MCP-сервер** для прямого подключения к Claude Desktop
- [ ] Публикация на PyPI (`pip install claude-skill-uon-travel`)
- [ ] Перевод документации на английский

## Не делаем

- Полноценный фронтенд для CRM (это работа U-On)
- ETL в data warehouse (это работа отдельных pipeline-ов, не скилла)
- Замена самого U-On (мы только адаптер к их API)
