# Конвенции и подводные камни U-On API

Поведенческие особенности API, найденные эмпирически. Чем больше из них вы знаете до того, как пишете интеграцию, тем меньше боли.

---

## 0. Lead обновляется через /request/update, а не /lead/update

`POST /lead/update/{id}` **не существует** — отдаёт `404 No route found`. Чтобы двинуть lead по статусам, дёргаем `/request/update/{id}` с полем `lead_status_id`:

```bash
uon leads update 1 --status-id 5
# → POST /request/update/1 with lead_status_id=5
# Lead 1: status_id 1 → 5, status="Принимает решение по оплате"
```

Если нужно ОБА статуса одновременно (lead + request):

```bash
uon raw post "request/update/1" -F lead_status_id=5 -F request_status_id=2
```

Lead и request — отдельные сущности с разными id, но обновляются одним эндпоинтом.

## 1. Поля create ≠ поля update

Самый частый источник ошибок — в `POST /request/create` и `POST /request/update/{id}` поля называются **по-разному**, хотя относятся к одной сущности.

| Поле в create | Поле в update | Описание |
|---------------|---------------|----------|
| `status_id` | `request_status_id` | Статус заявки |
| `r_u_id` | `manager_id` | Менеджер |
| `r_cl_id` | `r_cl_id` | Клиент (одинаково) |
| `source_id` | `source_id` | Источник (одинаково) |
| `touroperator_id` | `touroperator_id` | Туроператор (одинаково) |

> **Откуда взято:** проверено на боевом кабинете 2026-05-29 — `status_id` в update возвращает HTTP 200 OK, но статус не меняется. После замены на `request_status_id` — меняется корректно.

То же может быть и для других сущностей. Если update вернул 200, а поле не обновилось — это первое место, куда смотреть.

---

## 2. Поля create ≠ поля read (response)

Сервер принимает одно имя, отдаёт другое:

| Принимает (write) | Возвращает (read) |
|-------------------|--------------------|
| `note` | `notes` |
| `r_dat_begin` | `date_begin` (без `r_`) |
| `r_dat_end` | `date_end` |
| `description` (в service) | `description` (одинаково) |
| `price` (в service) | `price` (одинаково) |
| `name` (в service create) | НЕ принимается — нужно `description` |
| `countries` (в lead create) | `client_requirements_country_ids` (pipe-формат `\|1\|`) |
| `budget` (в lead create) | `client_requirements_budget` |
| `date_from` / `date_to` (lead-wishes) | `client_requirements_date_from` / `_to` |
| `nights_from` / `nights_to` | `client_requirements_days_from` / `_to` |
| `tourist_count` | `client_requirements_tourists_adult_count` |
| `tourist_child_count` | `client_requirements_tourists_child_count` |
| `hotel_types` (CSV: `4*,5*`) | `client_requirements_hotel_stars` (pipe: `\|4*\|5*\|`) |
| `nutrition` (CSV: `AI,UAI`) | `client_requirements_nutrition_ids` (pipe: `\|AI\|UAI\|`) |
| `requirements_note` | `client_requirements_note` |
| `u_telegram` (в lead) | `telegram` (без `client_` префикса) |
| `u_whatsapp` (в lead) | `whatsapp` |

---

## 3. Платёж требует `cio_id`

`POST /payment/create` без `cio_id` отдаёт `404 "Parameter cio_id is wrong"`. Значения:

- `1` — приход (от клиента)
- `2` — расход (партнёру или возврат)

Также **обязателен** `type_id`:

- `1` — расчёты с клиентами
- `2` — расчёты с партнёрами

И сумма передаётся в поле `price`, а не `summa` или `amount`.

```bash
uon payments create --request-id 2 --amount 30000 --form-id 1 --direction in
# отправит: r_id=2, price=30000, form_id=1, cio_id=1, type_id=1
```

---

## 4. Услуги (`POST /service/create`)

Совсем другая конвенция чем у заявок:

| Что хочешь сказать | Поле |
|--------------------|------|
| ID типа услуги (1=Отель, 2=Трансфер...) | `type_id` (НЕ `type`) |
| Название/описание | `description` (НЕ `name`) |
| Цена клиенту | `price` (НЕ `price_client`) |
| Закупочная цена | `price_netto` |
| Отель | `hotel` (строка названия, НЕ `hotel_id`) |
| Город | `city` (строка) |
| Страна | `country` (строка) |

Справочник типов услуг:

```bash
uon services types
# 1=Отель, 2=Трансфер, 3=Экскурсия, 4=Виза, 5=Страховка, ...
```

---

## 5. Дедлайны и касания обязательно требуют `type_id`

`POST /request-deadline/create`:
- `type_id=1` — дедлайн для туриста (default в нашем CLI)
- `type_id=2` — дедлайн для партнёра
- сумма — поле `summ` (с двумя м), не `amount`

`POST /request-action/create`:
- `type_id=0` — не определено (комментарий)
- `type_id=1` — звонок
- `type_id=2` — письмо
- `type_id=3` — встреча
- обязательны `datetime`, `text` и одно из `r_id` или `tr_id`

---

## 6. Возвращаемый `id` — строка, не int

После любого `create` ответ выглядит так:

```json
{"result": 200, "id": "1"}
```

`id` приходит **строкой**. Если на своей стороне ожидаете int — конвертируйте.

---

## 7. `r_id` vs `id` в URL

Большинство методов по конкретной заявке используют ID в URL, но поля внутри payload зовутся `r_id` (request ID).

- `GET /request/{id}.json` — здесь `{id}` это ID заявки
- `POST /service/create.json` с body `r_id=2` — в body это `r_id`

Просто помните: в URL — `{id}`, в body — `r_id`.

---

## 8. Пустой массив vs HTTP 404

Если ресурс пустой, U-On может вернуть **`HTTP 404` с `result: 404`** вместо HTTP 200 + пустого массива. Это касается:

- `GET /webhook/{page}` когда вебхуков нет
- `GET /supplier` когда поставщиков нет
- `GET /extended_field/{page}` когда полей нет

Обрабатывайте 404 как «пусто», не как ошибку. CLI делает это автоматически.

---

## 9. Телефон сохраняется с лидирующим пробелом

При `POST /user/create` с `u_phone_mobile=+79991234567` U-On сохраняет `" 79991234567"` (пробел вместо `+`). Это видно при чтении.

При поиске через `GET /user/phone/{phone}` тот же номер ищется без `+` корректно. CLI это нормализует автоматически.

---

## 10. Формат дат

| Поле | Формат |
|------|--------|
| `r_dat_begin`, `r_dat_end`, `datetime` (касания) | `Y-m-d H:i:s` (`2026-07-01 00:00:00`) |
| `date` в дедлайнах | `Y-m-d` (без времени) |
| `u_birthday`, `u_passport_date` | `Y-m-d` |

Если передать дату без времени туда, где ждут полный datetime — она примет `00:00:00`, но иногда возвращается как `None`. Лучше всегда явно указывать время.

---

## 11. HTML-entities в названиях статусов

`GET /status` возвращает заголовки вроде `"Заявка &rarr; Лид"` (HTML entity `&rarr;` вместо `→`). Похоже на legacy quirk бэкенда — декодируйте на своей стороне.

---

## 12. Webhook метод по умолчанию — GET

При `POST /webhook/create` без явного `method` U-On регистрирует **GET-вебхук**, а не POST. Это неинтуитивно — payload передаётся в query-string, а не в body. Если хотите POST — передавайте `method=POST` явно в `-F method=POST`.

---

## 13. Пагинация — 100 на страницу

Все list-endpoint-ы с пагинацией возвращают по 100 записей. Чтобы выгрузить всё — итерируйте по `?page=1,2,3,...` пока не получите пустой массив.

Поле `pages_all` в ответе подсказывает общее число страниц.

---

## 14. Rate limit 10 req/sec

Превышение → HTTP 429 без retry-after. Скилл соблюдает throttle 150ms (≈6.6 req/sec). Если делаете большую выгрузку и хотите faster — пишите свой sleep, но не быстрее 100ms между запросами.

---

## 14a. Доп. поля (`extended_fields`) — массив-как-словарь

В U-On любая сущность может иметь кастомные поля. Управление — через `/extended_field/*`:

```bash
uon fields list                # все доп.поля
uon fields list --section 2    # только для обращений
uon fields create --section 2 --name "Откуда узнали?" --type 2 \
    --options "Рекомендация,Соцсети,Поиск Google,Реклама"
uon fields update 199888 --name "Канал привлечения"
uon fields delete 199888 --confirm
```

**Разделы (`section`):**

| section | Где появляется в кабинете |
|--------:|---------------------------|
| 1 | Заявка |
| 2 | Обращение |
| 3 | Турист (карточка клиента) |
| 4 | Услуга в заявке |
| 5 | Платёж клиента |
| 6 | Платёж партнёра |
| 7 | Косвенный платёж |
| 8 | Партнёр (поставщик) |

**Типы полей (`type`):**

| type | Описание |
|-----:|----------|
| 1 | Текст (default) |
| 2 | Список значений (нужен `--options "A,B,C"`) |
| 3 | Многострочное |
| 4 | Дата |
| 5 | Текст + ссылка |

**Заполнение в lead/request/user/payment:**

```bash
# Передаём массив-как-словарь через -F:
uon leads create --name Иван --phone +79... \
    -F "extended_fields[199888]=Соцсети"

uon users update 5 \
    -F "extended_fields[199889]=Аллергия на орехи, диета без глютена"

uon requests update 12 \
    -F "extended_fields[199890]=Виза готова, срок 2027-08-01"
```

**Чтение:** возвращается массив `[{id, value}, ...]` в поле `extended_fields` сущности.

```bash
uon leads get 4 | jq '.lead[0].extended_fields'
# [{"id": 199888, "value": "Соцсети"}]
```

ID полей — стабильные числа (199888, 199889...), у каждого кабинета свои. Жёстко прописывать в коде — плохо. Лучше хранить маппинг «человеческое название → ID» в config-файле и читать через `uon fields list` при инициализации.

## 15. Где взять «полный» список полей

Доку `api.u-on.ru/doc` стоит читать как первоисточник, но:
- многие поля помечены как «string» с подсказкой "Тип данных" вместо описания
- описания часто на двух языках в одной ячейке
- обязательные/опциональные не всегда корректно отражены
- автогенерированный референс полей лежит в [`references/fields.md`](fields.md)
- PHP-клиент [DrTeamRocks/uon](https://github.com/DrTeamRocks/uon) — хороший источник правды для имён endpoint-ов
- эмпирические проверки на реальном кабинете — единственный надёжный путь

Если нашли новый gotcha — добавьте сюда, не повторяйте ошибку.
