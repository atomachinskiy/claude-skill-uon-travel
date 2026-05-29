# Полный список endpoint-ов U-On.Travel API

Всего операций: **150** в **42** семействах.

Группировка — по первому сегменту пути после `/{key}/`.

---

## Авиаперелёты (1 опер.)

- `POST  ` `/avia/create.{_format}` — Добавление авиаперелета в услугу / Adding flight to the service in request

## Бонусные карты (5 опер.)

- `POST  ` `/bcard-activate/create.{_format}` — Активация бонусной карты / Bonus card activation
- `GET   ` `/bcard-bonus-by-card/{id}.{_format}` — Получение транзакций бонусной карты клиента (по ID карты) / Get bonus transactions by bonu
- `GET   ` `/bcard-bonus-by-user/{id}.{_format}` — Получение транзакций бонусной карты клиента (по ID клиента) / Get bonus transactions by cl
- `POST  ` `/bcard-bonus/create.{_format}` — Пополнение/списание баллов по бонусной карте / Bonuses add/delete by bonus card
- `POST  ` `/bcard/create.{_format}` — Добавление бонусной карты / Bonus card create

## Счета (для аналитики) (2 опер.)

- `GET   ` `/bill/{id}.{_format}` — Получение данных по счету / Get bill data
- `GET   ` `/bills/{page}.{_format}` — Получение списка счетов / Get the list of bills

## История звонков (4 опер.)

- `POST  ` `/call_history/create.{_format}` — Добавление информации о звонке / Add information about the phone call
- `GET   ` `/call_history/{page}.{_format}` — Список звонков / The list of telephony calls
- `GET   ` `/call_history_by_request/{r_id}/{page}.{_format}` — Список звонков по заявке / The list of telephony calls by request
- `GET   ` `/call_history_by_user/{u_id}/{page}.{_format}` — Список звонков по клиенту / The list of telephony calls by client

## Кассы (2 опер.)

- `GET   ` `/cash.{_format}` — Получение списка касс / Get the list of cashboxes
- `POST  ` `/cash/create.{_format}` — Добавление кассы / Add new cashbox

## Каталог "Я-оператор" (6 опер.)

- `POST  ` `/catalog-package/update/{id}.{_format}` — Обновление пакета услуг из раздела Я-оператор / Update catalog package of I am operator
- `GET   ` `/catalog-package/{id}.{_format}` — Получение пакета из раздела Я-оператор / Get catalog package of I am operator
- `GET   ` `/catalog-packages/{page}.{_format}` — Получение пакетов из раздела Я-оператор / Get catalog packages of I am operator
- `POST  ` `/catalog-service/create.{_format}` — Создание услуги Я-оператор / Create services of I am operator
- `POST  ` `/catalog-service/update/{id}.{_format}` — Обновление услуги Я-оператор / Update services of I am operator
- `GET   ` `/catalog-service/{page}.{_format}` — Получение услуг Я-оператор / Get services of I am operator

## Внутренний чат (1 опер.)

- `POST  ` `/chat-message/create.{_format}` — Отправка сообщения от менеджера другому менеджеру или туристу / Send message from manager 

## Города (справочник) (4 опер.)

- `GET   ` `/cities/{country_id}.{_format}` — Получение списка городов / Get list of cities
- `GET   ` `/cities/{country_id}/{page}.{_format}` — Получение списка городов / Get list of cities
- `POST  ` `/city/create.{_format}` — Добавление города / Add city
- `POST  ` `/city/update/{id}.{_format}` — Обновление данных по городу / Update city

## Компании и офисы (2 опер.)

- `GET   ` `/company-office.{_format}` — Получение списка офисов / Get the list of offices
- `GET   ` `/company.{_format}` — Получение списка ваших компаний / Get the list of your companies

## Страны (справочник) (3 опер.)

- `GET   ` `/countries.{_format}` — Получение списка стран / Get list of countries
- `POST  ` `/country/create.{_format}` — Добавление страны / Add country
- `POST  ` `/country/update/{id}.{_format}` — Обновление данных по стране / Update country

## Валюты (1 опер.)

- `GET   ` `/currency.{_format}` — Получение списка валют / Get list of currencies

## Кастомные поля (4 опер.)

- `POST  ` `/extended_field/create.{_format}` — Добавление дополнительного поля / Add extended field
- `POST  ` `/extended_field/delete/{id}.{_format}` — Удаление дополнительного поля / Delete extended field
- `POST  ` `/extended_field/update/{id}.{_format}` — Обновление дополнительного поля / Update extended field
- `GET   ` `/extended_field/{page}.{_format}` — Получение списка дополнительных полей / Get list of extended fields

## Отели (5 опер.)

- `POST  ` `/hotel/create.{_format}` — Добавление отеля / Add hotel
- `POST  ` `/hotel/delete/{id}.{_format}` — Удаление отеля / Delete hotel
- `POST  ` `/hotel/update/{id}.{_format}` — Обновление данных по отелю / Update hotel
- `GET   ` `/hotel/{id}.{_format}` — Получение данных по отелю / Get hotel data
- `GET   ` `/hotels/{page}.{_format}` — Получение списка отелей (постранично, на каждой странице 100 отелей) / Get list of hotels 

## Статусы страховки (1 опер.)

- `GET   ` `/insurance.{_format}` — Получение списка статусов страховки / Get list of insurance statuses

## Обращения (lead) (10 опер.)

- `GET   ` `/lead-by-client/{id}.{_format}` — Получение обращений по покупателю / Get leads data by client ID
- `GET   ` `/lead-by-client/{id}/{page}.{_format}` — Получение обращений по покупателю / Get leads data by client ID
- `POST  ` `/lead/create.{_format}` — Добавление обращения / Add lead
- `POST  ` `/lead/search.{_format}` — Получение данных обращений по фильтрам / Get leads data by filters
- `GET   ` `/lead/{date_from}/{date_to}.{_format}` — Получение данных по обращениям / Get leads data
- `GET   ` `/lead/{date_from}/{date_to}/{source_id}.{_format}` — Получение данных по обращениям согласно источнику / Get leads data by source
- `GET   ` `/lead/{id}.{_format}` — Получение данных обращения / Get lead data
- `GET   ` `/leads/updated/{date_from}/{date_to}/{page}.{_format}` — Получение данных по обновленным заявкам / Get data by updated requests
- `GET   ` `/leads/{date_from}/{date_to}/{page}.{_format}` — Получение данных по обращениям / Get leads data
- `GET   ` `/leads/{date_from}/{date_to}/{source_id}/{page}.{_format}` — Получение данных по обращениям согласно источнику / Get leads data by source

## Email-уведомления (1 опер.)

- `POST  ` `/mail/create.{_format}` — Добавление информации о письме / Add information about mail item

## Сотрудники (4 опер.)

- `GET   ` `/manager.{_format}` — Список сотрудников компании / The list of company employees
- `POST  ` `/manager/create.{_format}` — Добавление сотрудника компании / Add company user
- `GET   ` `/manager/office/{office_id}.{_format}` — Список сотрудников компании / The list of company employees
- `GET   ` `/manager/{user_id}.{_format}` — Получение данных конкретного сотрудника компании / Data of specific company employee

## Уведомления в кабинете (3 опер.)

- `POST  ` `/notification/create.{_format}` — Отображение всплывающего окна (уведомления) менеджеру / Show notification to manager
- `GET   ` `/notification/{id}.{_format}` — Получение данных по уведомлению / Get notification data
- `POST  ` `/notifications/{page}.{_format}` — Получение списка уведомлений / Get list of notifications

## Типы питания (3 опер.)

- `GET   ` `/nutrition.{_format}` — Получение типов питания / Get list of nutrition
- `POST  ` `/nutrition/create.{_format}` — Добавление питания / Add nutrition
- `POST  ` `/nutrition/update/{id}.{_format}` — Обновление типа питания / Update nutrition

## Счета к платежам (6 опер.)

- `POST  ` `/paydoc/create.{_format}` — Добавление счета в платеж / Add paydoc into payment
- `POST  ` `/paydoc/delete/{id}.{_format}` — Удаление счета из платежа / Delete paydoc
- `GET   ` `/paydoc/list/{date_from}/{date_to}.{_format}` — Получение списка счетов из платежей (поля при получении см. /paydoc/create) / Get paydocs 
- `GET   ` `/paydoc/list/{date_from}/{date_to}/{page}.{_format}` — Получение списка счетов из платежей (поля при получении см. /paydoc/create) / Get paydocs 
- `POST  ` `/paydoc/update/{id}.{_format}` — Изменение счета в платеже / Update paydoc in payment
- `GET   ` `/paydoc/{id}.{_format}` — Получение счета из платежа (поля при получении см. /paydoc/create) / Get paydoc (upon rece

## Платежи (8 опер.)

- `POST  ` `/payment/create.{_format}` — Добавление платежа / Add payment
- `POST  ` `/payment/delete/{id}.{_format}` — Удаление платежа / Delete payment
- `GET   ` `/payment/list/{date_from}/{date_to}.{_format}` — Получение списка платежей (поля при получении см. /payment/create) / Get list of payments 
- `GET   ` `/payment/list/{date_from}/{date_to}/{page}.{_format}` — Получение списка платежей (поля при получении см. /payment/create) / Get list of payments 
- `POST  ` `/payment/update/{id}.{_format}` — Изменение платежа / Update payment
- `GET   ` `/payment/{id}.{_format}` — Получение платежа (поля при получении см. /payment/create) / Get payment data (upon receip
- `GET   ` `/payment_form.{_format}` — Получение списка видов платежей / Get list of payment views
- `GET   ` `/payment_other_type.{_format}` — Получение списка типов косвенных платежей / Get list of payment other types

## Причины отказа (1 опер.)

- `GET   ` `/reason_deny.{_format}` — Список отказов по обращениям / Get reason deny list

## Напоминания (5 опер.)

- `GET   ` `/reminder-one/{id}.{_format}` — Получение данных по напоминанию / Get reminder data
- `POST  ` `/reminder/close/{id}.{_format}` — Завершение напоминания в заявке или карточке туриста / Close reminder in request or in tou
- `POST  ` `/reminder/create.{_format}` — Добавление напоминания в заявку или карточку туриста / Add reminder in request or in touri
- `POST  ` `/reminder/{page}.{_format}` — Получение списка напоминаний / Get list of reminders
- `GET   ` `/reminder/{r_id}.{_format}` — Получение списка напоминаний по заявке / Get list of reminders by request

## Заявки (request) (24 опер.)

- `POST  ` `/request-action/create.{_format}` — Добавление касания в заявку или в карточку туриста / Add client contact in request or in t
- `GET   ` `/request-action/{date_from}/{date_to}.{_format}` — Получение списка касаний за период / Get list of client contacts for the period
- `GET   ` `/request-action/{date_from}/{date_to}/{page}.{_format}` — Получение списка касаний за период / Get list of client contacts for the period
- `GET   ` `/request-action/{r_id}.{_format}` — Получение списка касаний по заявке / Get list of client contacts by request
- `GET   ` `/request-by-client/{id}.{_format}` — Получение заявок по покупателю / Get requests data by client ID
- `GET   ` `/request-by-client/{id}/{page}.{_format}` — Получение заявок по покупателю / Get requests data by client ID
- `GET   ` `/request-by-tourist/{id}.{_format}` — Получение заявок по туристу / Get requests data by tourist ID
- `GET   ` `/request-by-tourist/{id}/{page}.{_format}` — Получение заявок по туристу / Get requests data by tourist ID
- `POST  ` `/request-deadline/create.{_format}` — Добавление дедлайна по оплате в заявке / Add payment deadline in request
- `POST  ` `/request-deadline/delete.{_format}` — Удаление дедлайном по оплате в заявке / Delete payment deadline in request
- `GET   ` `/request-deadline/{r_id}.{_format}` — Получение списка дедлайном по оплате в заявке / Get payment deadline list by request
- `POST  ` `/request-document.{_format}` — Получение сформированного документа из заявки / Get filled document from request
- `POST  ` `/request-file/create.{_format}` — Добавление файла в заявку / Add file into request
- `POST  ` `/request-file/delete/{id}.{_format}` — Удаление прикрепленного файла из заявки / Delete attached file from request
- `POST  ` `/request/create.{_format}` — Добавление заявки / Add request
- `POST  ` `/request/search.{_format}` — Получение данных заявок по фильтрам / Get requests data by filters
- `POST  ` `/request/update/{id}.{_format}` — Обновление данных по обращению или заявке / Update lead or request
- `GET   ` `/request/{date_from}/{date_to}.{_format}` — Получение данных по заявкам / Get requests data by period
- `GET   ` `/request/{date_from}/{date_to}/{source_id}.{_format}` — Получение данных по заявкам согласно источнику / Get requests data by source
- `GET   ` `/request/{id}.{_format}` — Получение данных заявки / Get request data
- `GET   ` `/requests/closed/{date_from}/{date_to}/{page}.{_format}` — Получение данных по закрытым заявкам / Get data by closed requests
- `GET   ` `/requests/updated/{date_from}/{date_to}/{page}.{_format}` — Получение данных по обновленным заявкам / Get data by updated requests
- `GET   ` `/requests/{date_from}/{date_to}/{page}.{_format}` — Получение данных по заявкам / Get requests data by period
- `GET   ` `/requests/{date_from}/{date_to}/{source_id}/{page}.{_format}` — Получение данных по заявкам согласно источнику / Get requests data by source

## Услуги в заявке (8 опер.)

- `POST  ` `/service-price/create.{_format}` — Добавление периода и цены для расширенной карточки услуги (при включенной расширенной карт
- `POST  ` `/service-price/delete.{_format}` — Удаление блока период-цена из услуги / Delete service-price from service
- `POST  ` `/service-price/update/{id}.{_format}` — Обновление данных периода-цены (при включенной расширенной карточке услуги, в которой есть
- `POST  ` `/service/create.{_format}` — Добавление услуги в заявку / Add service in request
- `POST  ` `/service/delete.{_format}` — Удаление услуги из заявки / Delete service from request
- `POST  ` `/service/search.{_format}` — Получение услуг из заявок по фильтрам / Get services from requests by filters
- `POST  ` `/service/update/{id}.{_format}` — Обновление данных по услуге / Update service
- `GET   ` `/service_type.{_format}` — Список типов услуг для заявки / Get list of service types

## Источники обращений (2 опер.)

- `GET   ` `/source.{_format}` — Список источников заявки / Get source list
- `POST  ` `/source/create.{_format}` — Добавление источника заявки / Add source

## Справочники статусов (4 опер.)

- `GET   ` `/status.{_format}` — Получение списка статусов / Get list of statuses
- `GET   ` `/status_cb.{_format}` — Получение списка статусов по бронированию (по схеме работы ЦБ - ТА) / Get list of reservat
- `GET   ` `/status_lead.{_format}` — Получение списка статусов обращений / Get list of leads statuses
- `GET   ` `/status_pay.{_format}` — Получение списка статусов оплаты / Get list of pay statuses

## Поставщики/партнёры (7 опер.)

- `GET   ` `/supplier.{_format}` — Получение списка партнеров / Get list of partners
- `POST  ` `/supplier/create.{_format}` — Добавление партнера / Add partner
- `POST  ` `/supplier/update/{id}.{_format}` — Обновление данных по партнеру / Update partner
- `GET   ` `/supplier/{id}.{_format}` — Получение партнера / Get partner data
- `GET   ` `/supplier_type.{_format}` — Получение типов партнеров / Get list of partner types
- `POST  ` `/supplier_type/create.{_format}` — Добавление типа партнера / Add partner type
- `GET   ` `/suppliers/{page}.{_format}` — Получение списка партнеров / Get list of partners

## Туристы в заявке (2 опер.)

- `POST  ` `/tourists-requests/create.{_format}` — Добавление туриста в заявку / Add tourist in request
- `POST  ` `/tourists-requests/delete.{_format}` — Удаление туриста из заявки / Delete tourist from request

## Типы поездок (2 опер.)

- `GET   ` `/travel-type.{_format}` — Получение типов заявки / Get list of Travel Type
- `POST  ` `/travel-type/create.{_format}` — Добавление типа заявки / Add travel type

## Туристы / клиенты (14 опер.)

- `POST  ` `/user-cabinet/create.{_format}` — Создание личного кабинета туристу / Create tourist cabinet
- `POST  ` `/user-file/create.{_format}` — Добавление файла в карточку туриста / Add file into tourists files
- `GET   ` `/user-label.{_format}` — Получение списка меток / Get list of labels
- `GET   ` `/user.{_format}` — Список туристов (использовать обновленный метод /users_by_page/{page}) / The list of the t
- `POST  ` `/user/create.{_format}` — Добавление туриста / Add tourist
- `POST  ` `/user/email.{_format}` — Поиск туриста по e-mail / The tourist search by e-mail
- `GET   ` `/user/phone/{phone}.{_format}` — Поиск туриста по номеру телефона / The tourist search by phone number
- `GET   ` `/user/phone/{phone}/{office}.{_format}` — Поиск туриста по номеру телефона в пределах конкретного офиса / The tourist search by phon
- `POST  ` `/user/search.{_format}` — Получение данных пользователей по фильтрам / Get users data by filters
- `POST  ` `/user/update/{id}.{_format}` — Обновление туриста / Update tourist
- `GET   ` `/user/updated/{date_from}/{date_to}.{_format}` — Список обновленных туристов / List of updated tourists
- `GET   ` `/user/updated/{date_from}/{date_to}/{page}.{_format}` — Список обновленных туристов / List of updated tourists
- `GET   ` `/user/{id}.{_format}` — Получение данных по конкретному туристу / Getting data on specific tourist
- `GET   ` `/users/{page}.{_format}` — Список туристов / The list of the tourists

## Статусы виз (1 опер.)

- `GET   ` `/visa.{_format}` — Получение списка статусов визы / Get list of visa statuses

## Webhooks (4 опер.)

- `POST  ` `/webhook/create.{_format}` — Добавление вебхука / Add webhook
- `POST  ` `/webhook/delete/{id}.{_format}` — Удаление вебхука / Delete webhook
- `POST  ` `/webhook/update/{id}.{_format}` — Обновление вебхука / Update webhook
- `GET   ` `/webhook/{page}.{_format}` — Получение списка вебхуков / Get list of webhooks

