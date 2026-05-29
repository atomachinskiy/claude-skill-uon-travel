# Backlog

## v0.2 (write API + extended sub-CRUD)

- [ ] `requests create` — создание заявки с туристом и услугой за один вызов
- [ ] `requests update` — смена статуса/менеджера/цены
- [ ] `services create/update/delete` — управление услугами внутри заявки (отель, авиа, страховка, питание, виза)
- [ ] `payments create/update/delete` — приходы/возвраты
- [ ] `paydocs create/delete` — счета к платежам
- [ ] `tourists-requests create/delete` — привязка туристов к заявке
- [ ] `request-action create` — касания внутри заявки
- [ ] `request-deadline create/delete` — дедлайны оплаты
- [ ] `request-file create/delete` — файлы заявки
- [ ] `user/update` — обновление туриста
- [ ] `user-file create` — файлы карточки туриста

## v0.3 (webhooks)

- [ ] `register-all-webhooks.sh` — массовая регистрация 69 типов на один URL с фильтрами
- [ ] Cloudflare Worker receiver (TypeScript)
- [ ] FastAPI receiver (Python, Docker)
- [ ] n8n template (JSON export для импорта)
- [ ] Telegram-bridge receiver (Bun, serverless)
- [ ] HMAC-валидация (если U-On добавит signed webhooks)

## v0.4 (BI / analytics)

- [ ] `stats funnel` — lead → request → won по периоду и источнику
- [ ] `stats revenue` — выручка по менеджерам/офисам
- [ ] `stats avg-cycle` — среднее время от lead до won
- [ ] `stats churn` — причины отказа (top-N по `reason_deny`)
- [ ] `stats payments-overdue` — просроченные платежи
- [ ] HTML-отчёт по шаблону `offer.html` (beige paper, Inter, табы)

## v0.5 (доп. ресурсы)

- [ ] `hotels create/update/delete` — отели
- [ ] `suppliers create/update` — поставщики/туроператоры
- [ ] `bonuses` — начисление/списание баллов
- [ ] `bcard create/activate` — бонусные карты
- [ ] `avia/insurance/visa/nutrition` — справочники услуг
- [ ] `mail/sms` — отправка писем и SMS вручную
- [ ] `catalog-package` / `catalog-service` — для туроператоров на схеме "Я-оператор"
- [ ] `chat-message` — отправка сообщений в чат CRM

## Тестирование

- [ ] Записанные фикстуры (replay-tests для CI без live API)
- [ ] Smoke-тест против реального кабинета (только GET)
- [ ] CI на GitHub Actions

## Документация

- [ ] `references/lifecycle.md` — диаграмма Lead → Request → Service → Payment → Document
- [ ] `references/conventions.md` — формат дат, пагинация, кодировка, что возвращает `{_format}`
- [ ] `examples/` — готовые рецепты: «новая заявка из Telegram», «синк в Sheets», «уведомление об оплате в Notion»

## Публикация

- [ ] Создать публичный репо `atomachinskiy/claude-skill-uon-travel`
- [ ] CHANGELOG.md
- [ ] Скриншоты использования в Claude Code
- [ ] Возможный пост на Хабр / в TG-канал
