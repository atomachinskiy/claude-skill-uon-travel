# Поля POST-запросов (обязательные + опциональные)

Извлечено автоматически из публичной документации `api.u-on.ru/doc`.
Используется в скилле как референс при сборке create-запросов.

---

## POST /lead/create

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `r_id_internal` | string |  | Номер заявки / The application number |
| `r_dat` | datetime |  | Дата создания, формат: Y-m-d H:i:s / Creation date, format: Y-m-d H:i:s |
| `r_u_id` | integer |  | ID менеджера, на которого будет назначен лид / ID Manager, who will be assigned to lead |
| `r_cl_id` | integer |  | ID клиента / Client ID |
| `r_ci_id` | integer |  | ID компании, на который будет назначен лид / Company ID, who will be assigned to lead |
| `r_co_id` | integer |  | ID офиса, на который будет назначен лид / Office ID, who will be assigned to lead |
| `status_id` | integer |  | ID статуса (см.метод /status_lead) / ID status (see method /status_lead) |
| `reason_deny_id` | integer |  | ID причины отказа в обращении / ID reason deny in lead |
| `source` | string |  | Источник заявки / Source applications |
| `touroperator_id` | integer |  | ID партнера (см. метод /supplier) / Partner s ID (see method /supplier) |
| `travel_type_id` | integer |  | ID типа тура (см. метод /travel-type) / Type ID of the tour (see method /travel-type) |
| `visa_id` | integer |  | Статус для поля Виза в заявке (см.метод /visa) / Visa status (see method /visa) |
| `insurance_id` | integer |  | Статус для поля Страховка в заявке (см.метод /insurance) / Insurance status (see method /insurance) |
| `note` | string |  | Примечание / Note |
| `date_from` | string |  | Пожелания клиента: дата начала, формат: Y-m-d / The wishes of the client: start date, format: Y-m-d |
| `date_to` | string |  | Пожелания клиента: дата окончания, формат: Y-m-d / Client s wishes: end date, format: Y-m-d |
| `nights_from` | string |  | Пожелания клиента: кол-во ночей (от) / Client s wishes: number of nights () |
| `nights_to` | string |  | Пожелания клиента: кол-во ночей (до) / Client s wishes: number of nights (up to) |
| `countries` | string |  | Пожелания клиента: ID стран (через запятую, см.метод /countries) / The wishes of the client: ID countries (see method /countries) |
| `hotel_types` | string |  | Пожелания клиента: категории отелей (через запятую из списка 1&#42;,2&#42;,3&#42;,4&#42;,5&#42;,5&#43;&#42;,Apts,Villa) / Client s wishes: hotel categories (comma separated list 1&#42;,2&#42;,3&#42;,4&#42;,5&#42;,5&#43;&#42;,Apts,Villa) |
| `nutrition` | string |  | Пожелания клиента: типы питания (через запятую из списка RO,BB,HB,HB&#43;,FB,FB&#43;,AI,UAI) / The wishes of the client: food types (comma separated list RO,BB,HB,HB&#43;,FB,FB&#43;,AI,UAI) |
| `tourist_count` | string |  | Пожелания клиента: Количество туристов (взрослые) / The number of tourists (adults) |
| `tourist_child_count` | string |  | Пожелания клиента: Количество туристов (дети) / The number of tourists (children) |
| `tourist_baby_count` | string |  | Пожелания клиента: Количество туристов (младенцы) / The number of tourists (infants) |
| `budget` | integer |  | Пожелания клиента: Бюджет клиента / The budget of the client |
| `requirements_note` | string |  | Пожелания клиента: Примечание / Client requirements note |
| `requirements_countries` | string |  | Пожелания клиента: ID стран (через запятую, см.метод /countries) / The wishes of the client: ID countries (see method /countries) |
| `u_surname` | string |  | Фамилия клиента / The surname of the client |
| `u_sname` | string |  | Отчество клиента / The second name of the client |
| `u_name` | string |  | Имя клиента / The name of the customer |
| `u_phone` | string | ✓ | Телефон клиента (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / Phone client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber must be specified) |
| `u_phone_mobile` | string | ✓ | Телефон клиента мобильный (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / Phone client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber must be speci |
| `u_phone_home` | string | ✓ | Телефон клиента домашний (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / Phone client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber must be specif |
| `u_email` | string | ✓ | E-mail клиента (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / E-mail client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber must be specified) |
| `u_social_vk` | string | ✓ | Аккаунт клиента ВКонтакте (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / VK account of client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber must  |
| `u_social_fb` | string | ✓ | Аккаунт клиента Facebook (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / FB account of client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber must b |
| `u_social_ok` | string | ✓ | Аккаунт клиента Oдноклассники (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / Odnoklassniki account of client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsap |
| `u_telegram` | string | ✓ | Аккаунт клиента Telegram (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / Telegram account of client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber  |
| `u_instagram` | string | ✓ | Аккаунт клиента Instagram (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / Instagram account of client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Vibe |
| `u_whatsapp` | string | ✓ | Аккаунт клиента Whatsapp (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / Whatsapp account of client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber  |
| `u_viber` | string | ✓ | Аккаунт клиента Viber (одно из полей Телефон / E-mail / ВКонтакте / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber должно быть указано) / Viber account of client (one of the fields Telephone / E-mail / VK / Facebook / Odnoklassniki / Telegram / Instagram / Whatsapp / Viber must b |
| `u_password` | string |  | Пароль клиента / The client password |
| `u_address` | string |  | Адрес клиента / Address of client |
| `u_birthday` | string |  | Дата рождения клиента (формат YYYY-mm-dd) / Note of client (format YYYY-mm-dd) |
| `u_note` | string |  | Примечание клиента / Note of client |
| `extended_fields` | array |  | Массив значений дополнительных полей в виде [ID доп.поля => значение, ID доп.поля2 => значение2, ...] (см.метод /extended_field). ВАЖНО! Чтобы дополнительное поле относилось к обращению / Array of values for extended fields [ID field => value, ID field2 => value2, ...] (see method /extended_field) |
| `utm_source` | string |  | utm_source / utm_source |
| `utm_medium` | string |  | utm_medium / utm_medium |
| `utm_campaign` | string |  | utm_campaign / utm_campaign |
| `utm_content` | string |  | utm_content / utm_content |
| `utm_term` | string |  | utm_term / utm_term |
| `ignore_actions_and_reminders` | integer |  | Игнорировать автоматическое создание начального комментария и напоминания (=1) / Ignore auto-creating of note and task (=1) |
| `ignore_tourist_notification` | integer |  | Не уведомлять туриста (=1) / Ignore client notification (=1) |
| `ignore_manager_notification` | integer |  | Не уведомлять менеджера (=1) / Ignore manager notification (=1) |
| `reminder_datetime` | datetime |  | Дата напоминания (замена стандартному напоминанию 'Заполнить данные клиента (через 1 час)'), формат: Y-m-d H:i / Date reminders (replacement for the standard reminder to Fill in the data client (1 hour) ), format: Y-m-d H:i |
| `reminder_text` | string |  | Текст напоминания (замена стандартному напоминанию 'Заполнить данные клиента (через 1 час)') / The reminder text (replacing the standard reminder to Fill in the data client (1 hour) ) |

## POST /request/create

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `r_id_internal` | string |  | Номер заявки / The application number |
| `r_dat` | datetime |  | Дата создания, формат: Y-m-d H:i:s / Creation date, format: Y-m-d H:i:s |
| `r_dat_lead` | datetime |  | Дата создания обращения (лида), формат: Y-m-d H:i:s / Creation date of lead, format: Y-m-d H:i:s |
| `r_dat_begin` | datetime |  | Дата начала заявки, формат: Y-m-d H:i:s / The start date of the application, the format: Y-m-d H:i:s |
| `r_dat_end` | datetime |  | Дата окончания заявки, формат: Y-m-d H:i:s / The end date of the application, the format: Y-m-d H:i:s |
| `r_u_id` | integer |  | ID менеджера, на которого будет назначена заявка / ID Manager, who will be assigned to the application |
| `r_cl_id` | integer |  | ID клиента (если известен) / Client ID (if known) |
| `r_ci_id` | integer |  | ID компании (юридического лица), на которую будет назначена заявка / Company ID, who will be assigned to the application |
| `r_co_id` | integer |  | ID офиса, на который будет назначена заявка / Office ID, who will be assigned to the application |
| `r_tour_operator_id` | integer |  | ID туроператора (см.метод /supplier) / ID of the operator (see method /supplier) |
| `r_tour_operator_link` | string |  | Ссылка на тур на сайте туроператора / Tour link of the operator |
| `r_travel_type_id` | integer |  | ID типа заявки (см.метод /travel-type) / ID of travel type (see method /travel-type) |
| `r_reservation_number` | string |  | Номер заявки у туроператора / The number of applications from tour operator |
| `status_id` | integer |  | ID статуса (см.метод /status) / ID status (see method /status) |
| `status_pay_id` | integer |  | ID статуса оплаты (см.метод /status_pay) / ID status pay (see method /status_pay) |
| `country_id` | integer |  | ID страны (см.метод /countries) , если не передается массив услуг в поле services / ID of the country (see method /countries), if it doesn't passed in field services |
| `city_id` | integer |  | ID города (см.метод /cities), если не передается массив услуг в поле services / ID of the city (see method /cities), if it doesn't passed in field services |
| `hotel_id` | integer |  | ID отеля (см.метод /hotels), если не передается массив услуг в поле services / ID of the hotel (see method /hotels), if it doesn't passed in field services |
| `reason_deny_id` | integer |  | ID причины отказа / ID reason deny |
| `visa_id` | integer |  | Статус для поля Виза в заявке (см.метод /visa) / Visa status (see method /visa) |
| `insurance_id` | integer |  | Статус для поля Страховка в заявке (см.метод /insurance) / Insurance status (see method /insurance) |
| `source` | string |  | Источник заявки / Source applications |
| `price` | string |  | Стоимость заявки / The cost of applying |
| `price_netto` | string |  | Стоимость нетто заявки / The net value of the application |
| `note` | string |  | Примечание / Note |
| `u_type` | integer |  | Тип записи (1 - физ.лицо, 2 - юр.лицо, 3 - турагентство) / Record type (1 - individual, 2 - Jur.person 3 - travel Agency) |
| `u_surname` | string |  | Фамилия клиента / The surname of the client |
| `u_sname` | string |  | Отчество клиента / Second name of client |
| `u_name` | string |  | Имя клиента / The name of the customer |
| `u_surname_en` | string |  | Фамилия клиента (латиницей) / The name of the client (Latin) |
| `u_name_en` | string |  | Имя клиента (латиницей) / Client name (Latin) |
| `u_phone` | string |  | Телефон клиента / Phone customer |
| `u_phone_mobile` | string |  | Телефон клиента (мобильный) / Phone client (mobile) |
| `u_email` | string |  | E-mail клиента / E-mail client |
| `u_password` | string |  | Пароль клиента / The client password |
| `u_note` | string |  | Примечание клиента / Note client |
| `u_sex` | string |  | Пол клиента ('м' или 'ж') / Customer s gender ( m or W ) |
| `u_address` | string |  | Адрес клиента / The address of the client |
| `u_passport_number` | string |  | Серия и номер гражданского паспорта клиента / Series and number of passport of the client |
| `u_passport_code` | string |  | Код подразделения гражданского паспорта клиента / Code of passport of the client |
| `u_passport_date` | datetime |  | Дата выдачи паспорта, YYYY-mm-dd / Issue date, YYYY-mm-dd |
| `u_passport_taken` | string |  | Организация, выдавшая гражданский паспорт клиенту / The organization that issued the passport to the client |
| `nationality_id` | integer |  | Гражданство (ID страны, см.метод /countries) / Nationality (country ID, see method /countries) |
| `u_birthday` | datetime |  | День рождения клиента, YYYY-mm-dd / The customer s birthday, YYYY-mm-dd |
| `u_zagran_number` | string |  | Серия и номер загранпаспорта клиента / Series and number of passport of the client |
| `u_zagran_organization` | string |  | Орган выдачи загранпаспорта клиента / The organization of passport given |
| `u_zagran_given` | datetime |  | Дата выдачи загранпаспорта, YYYY-mm-dd / Date of issue of passport, in YYYY-mm-dd |
| `u_zagran_expire` | datetime |  | Дата окончания загранпаспорта, YYYY-mm-dd / The expiry date of the passport, YYYY-mm-dd |
| `u_company` | string |  | Название компании (для юр.лица) / Company name (for legal.person) |
| `u_address_u` | string |  | Юридический адрес (для юр.лиц) / Legal address (for Jur.persons) |
| `u_fax` | string |  | Факс (для юр.лиц) / Fax (for Jur.persons) |
| `u_inn` | string |  | ИНН (для юр.лиц) / INN (for Jur.persons) |
| `u_kpp` | string |  | КПП (для юр.лиц) / Transmission (for Jur.persons) |
| `u_ogrn` | string |  | ОГРН (для юр.лиц) / OGRN (for Jur.persons) |
| `u_okved` | string |  | ОКВЭД (для юр.лиц) / NACE (for Jur.persons) |
| `u_finance_bank` | string |  | Наименование банка (для юр.лиц) / Name of the Bank (for Jur.persons) |
| `u_finance_rs` | string |  | Расчетный счет (для юр.лиц) / Current account (for Jur.persons) |
| `u_finance_ks` | string |  | Кор.счет (для юр.лиц) / Cor.account (for Jur.persons) |
| `u_finance_bik` | string |  | БИК банка (для юр.лиц) / BIC Bank (for Jur.persons) |
| `u_finance_okpo` | string |  | ОКПО (для юр.лиц) / OKPO (for Jur.persons) |
| `u_discount_card_number` | string |  | Номер бонусной карты / The number of bonus cards |
| `u_discount_card_bonus` | integer |  | Количество бонусов на карте / The number of bonuses on the map |
| `extended_fields` | array |  | Массив значений дополнительных полей в виде [ID доп.поля => значение, ID доп.поля2 => значение2, ...] (см.метод /extended_field). ВАЖНО! Чтобы дополнительное поле относилось к заявке / Array of values for extended fields [ID field => value, ID field2 => value2, ...] (see method /extended_field) |
| `utm_source` | string |  | utm_source / utm_source |
| `utm_medium` | string |  | utm_medium / utm_medium |
| `utm_campaign` | string |  | utm_campaign / utm_campaign |
| `utm_content` | string |  | utm_content / utm_content |
| `utm_term` | string |  | utm_term / utm_term |
| `tourists` | collection |  | Массив туристов (см.метод /user/create) / An array of tourists (see method /user/create) |
| `services` | collection |  | Массив услуг (см.метод /service/create, поле 'r_id' указывать НЕ надо) / An array of services (see method /service/create field r_id should NOT be specified) |
| `payments` | collection |  | Массив платежей (см.метод /payment/create, поле 'r_id' указывать НЕ надо) / An array of payments (see method /payment/create field r_id should NOT be specified) |
| `ignore_tourist_notification` | integer |  | Не уведомлять туриста (=1) / Ignore client notification (=1) |
| `ignore_manager_notification` | integer |  | Не уведомлять менеджера (=1) / Ignore manager notification (=1) |

## POST /user/create

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `u_type` | integer |  | Тип записи (1 - физ.лицо, 2 - юр.лицо, 3 - турагентство) / Record type (1 - individual, 2 - Jur.person 3 - travel Agency) |
| `u_tk_id` | integer |  | Тип клиента (1 - Mr, 2 - Mrs, 3 - Miss, 4 - Child, 5 - Infant) / Client type (1 - Mr, 2 - Mrs, 3 - Miss, 4 - Child, 5 - Infant) |
| `u_company` | string |  | Название компании (для юр.лица) / Company name (for legal.person) |
| `u_position` | string |  | Должность контактного лица (для юр.лица) / Position in company structure (for legal.person) |
| `u_position_rod` | string |  | Должность контактного лица в родительном падеже (для юр.лица) / Position in company structure (for legal.person) |
| `u_name` | string |  | Имя туриста / The name of the tourist |
| `u_surname` | string |  | Фамилия туриста / The name of the tourist |
| `u_sname` | string |  | Отчество туриста / First name of camper |
| `u_name_en` | string |  | Имя туриста (латиницей) / The name of the tourist (Latin) |
| `u_surname_en` | string |  | Фамилия туриста (латиницей) / The name of the tourist (Latin) |
| `u_phone` | string |  | Телефон туриста / Phone tourist |
| `u_phone_mobile` | string |  | Телефон туриста (мобильный) / Telephone tourist (mobile) |
| `u_phone_home` | string |  | Телефон туриста (домашний) / Telephone tourist (home) |
| `u_email` | string |  | E-mail туриста / E-mail tourist |
| `u_birthday` | datetime |  | День рождения туриста, формат: Y-m-d / Birthday camper, format: Y-m-d |
| `u_birthday_place` | string |  | Место рождения туриста / Place of tourist birth |
| `u_birthday_certificate` | string |  | Свидетельство о рождении / Birthday certificate |
| `u_birthday_certificate_given` | datetime |  | Свидетельство о рождении, дата выдачи, формат: Y-m-d / Birthday certificate,date given, format: Y-m-d |
| `u_birthday_certificate_organization` | string |  | Свидетельство о рождении, кем выдано / Birthday certificate (organization) |
| `u_zagran_number` | string |  | Серия и номер загранпаспорта туриста / Series and number of passport of the tourist |
| `u_zagran_given` | datetime |  | Дата выдачи загранпаспорта, формат: Y-m-d / Date of issue of passport, format: Y-m-d |
| `u_zagran_expire` | datetime |  | Дата окончания загранпаспорта, формат: Y-m-d / The expiry date of the passport, format: Y-m-d |
| `u_zagran_organization` | string |  | Организация, выдавшая загранпаспорт / The organization that issued the passport |
| `u_passport_number` | string |  | Серия и номер гражданского паспорта туриста / Series and number of passport of the tourist |
| `u_passport_taken` | string |  | Кем выдан гражданский паспорт / Who issued your passport |
| `u_passport_date` | datetime |  | Дата выдачи гражданского паспорта, формат: Y-m-d / Date of issue of passport, format: Y-m-d |
| `u_passport_code` | string |  | Код подразделения гражданского паспорта / Passport code |
| `u_address` | string |  | Адрес туриста / Address |
| `u_password` | string |  | Пароль туриста / The password for the tourist |
| `u_sex` | string |  | Пол туриста (м / ж) / Camper gender (m / f) |
| `u_note` | string |  | Примечание / Note |
| `u_address_u` | string |  | Юридический адрес (для юр.лиц) / Legal address (for Jur.persons) |
| `u_fax` | string |  | Факс (для юр.лиц) / Fax (for Jur.persons) |
| `u_inn` | string |  | ИНН (для юр.лиц) / INN (for Jur.persons) |
| `u_kpp` | string |  | КПП (для юр.лиц) / Transmission (for Jur.persons) |
| `u_ogrn` | string |  | ОГРН (для юр.лиц) / OGRN (for Jur.persons) |
| `u_okved` | string |  | ОКВЭД (для юр.лиц) / NACE (for Jur.persons) |
| `u_finance_bank` | string |  | Наименование банка (для юр.лиц) / Name of the Bank (for Jur.persons) |
| `u_finance_rs` | string |  | Расчетный счет (для юр.лиц) / Current account (for Jur.persons) |
| `u_finance_ks` | string |  | Кор.счет (для юр.лиц) / Cor.account (for Jur.persons) |
| `u_finance_bik` | string |  | БИК банка (для юр.лиц) / BIC Bank (for Jur.persons) |
| `u_finance_okpo` | string |  | ОКПО (для юр.лиц) / OKPO (for Jur.persons) |
| `u_social_vk` | string |  | Аккаунт во Вконтакте / VKontakte account |
| `u_social_fb` | string |  | Аккаунт в Facebook / Facebook account |
| `u_social_ok` | string |  | Аккаунт в Одноклассниках / Odnoklassniki account |
| `u_telegram` | string |  | Аккаунт в Telegram / Telegram account |
| `u_max` | string |  | Аккаунт в MAX / MAX account |
| `u_whatsapp` | string |  | Аккаунт в Whatsapp / Whatsapp account |
| `u_viber` | string |  | Аккаунт в Viber / Viber account |
| `u_instagram` | string |  | Аккаунт в Instagram / Instagram account |
| `u_discount_card_number` | string |  | Номер бонусной карты / The number of bonus cards |
| `u_discount_card_bonus` | integer |  | Количество бонусов на карте / The number of bonuses on the map |
| `u_discount` | integer |  | Скидка клиента / Client discount |
| `u_labels` | string |  | Список меток (через запятую) / The list of labels (comma separated) |
| `nationality_id` | integer |  | ID страны (см. метод /countries) / Country ID (see method /countries) |
| `u_office_id` | integer |  | ID офиса (см. метод /company-office) / Office ID (see method /company-office) |
| `u_manager_id` | integer |  | ID прикрепленного менеджера (см. метод /manager) / Attached manager ID (see method /manager) |
| `u_source` | integer |  | ID туриста, который привел добавляемого туриста (см. метод /users) / Tourist ID, who is the source of new tourist (see method /users) |
| `extended_fields` | array |  | Массив значений дополнительных полей в виде [ID доп.поля => значение, ID доп.поля2 => значение2, ...] (см.метод /extended_field). ВАЖНО! Чтобы дополнительное поле относилось к туристам / Array of values for extended fields [ID field => value, ID field2 => value2, ...] (see method /extended_field) |

## POST /payment/create

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `r_id` | integer |  | ID заявки (см.метод /request/{id}) / ID of the application (see method /request/{id}) |
| `type_id` | integer |  | Тип платежа (1 - расчеты с клиентами, 2 - расчеты с партнерами) / Payment type (1 - accounts receivable 2 - accounts with partners) |
| `other_type_id` | integer |  | Тип косвенного платежа (см.метод /payment_other_type) / Payment other type (see /payment_other_type) |
| `cio_id` | integer | ✓ | Вид платежа (1 - приход, 2 - расход) / Type of payment (1 arrival, 2 - expense) |
| `reason` | string |  | Основание платежа / Basis of payment |
| `date` | datetime |  | Дата платежа, формат: Y-m-d H:i:s, по-умолчанию, ставится текущая дата / Payment date, format: Y-m-d H:i:s, default is the current date |
| `is_plan` | integer |  | Плановый платеж (1 - да, 0 - нет) / Scheduled payment (1 - Yes, 0 - no) |
| `parent_payment_id` | integer |  | ID родительского платежа, используется при создании комиссии и прикреплении к платежу в заявке / Parent payment ID, use for commission and attaching of it to payment inside request |
| `prepay_id` | integer |  | Тип предоплаты (1 - предоплата, 2 - доплата, 3 - полная оплата) / Scheduled payment (1 - prepay, 2 - postpay, 3 - full payment) |
| `is_bonus_pay` | integer |  | Оплата бонусами (1 - да, 0 - нет) / Payment by bonuses (1 - Yes, 0 - no) |
| `is_deposit` | integer |  | Депозитная операция? (1 - да, 0 - нет), по-умолчанию = 0 / Deposit payment? (1 - Yes, 0 - no), default = 0 |
| `date_plan` | datetime |  | Плановая дата платежа, формат: Y-m-d H:i:s / Scheduled payment date, format: Y-m-d H:i:s |
| `from1c` | integer |  | Платеж создан в CRM (= 0) или пришел из 1С (= 1) / The payment is created in CRM (= 0) or 1C (= 1) |
| `supplier_id` | integer |  | ID партнера / туроператора (см.метод /supplier) / ID of the partner / tour operator (see method /supplier) |
| `client_id` | integer |  | ID заказчика (см.метод /user) / ID of client (see method /user) |
| `form_id` | integer |  | ID вида платежа (см.метод /payment_form) / ID payment form (see method /payment_form) |
| `cash_id` | integer |  | ID кассы (см.метод /cash), по-умолчанию, берется первая касса / ID cash (see method /cash), by default, takes the first cash |
| `number` | string |  | Номер платежа (по-умолчанию, берется следующий порядковый номер) / Payment number (by default, it takes the next sequence number) |
| `currency_id` | integer |  | ID валюты (см.метод /currency) / The currency ID (see method /currency) |
| `koef` | float |  | Курс валюты (по-умолчанию, 1.00) / Currency (default: 1.00) |
| `price` | float |  | Стоимость клиенту / The cost to the client |
| `note` | string |  | Примечание по платежу / Note on payment |
| `manager_id` | integer |  | ID менеджера (см.метод /managers) / ID manager (see method /managers) |
| `office_id` | integer |  | ID офиса (см.метод /office) / ID office (see method /office) |
| `manager_id_creator` | integer |  | ID менеджера, кто создает платеж (см.метод /managers) / ID manager, who create payment (see method /managers) |
| `extended_fields` | array |  | Массив значений дополнительных полей в виде [ID доп.поля => значение, ID доп.поля2 => значение2, ...] (см.метод /extended_field). ВАЖНО! Чтобы дополнительное поле относилось к платежам / Array of values for extended fields [ID field => value, ID field2 => value2, ...] (see method /extended_field) |
| `notification_to_client` | boolean |  | Уведомление клиента по заявке об оплате (true/false), должно быть включено соответствующее уведомление в разделе СМС/Email - Уведомления туристам / Client notification, who is attached to request (true/false) |
| `notification_to_manager` | boolean |  | Копия уведомления клиента по заявке об оплате будет отправлена менеджеру, прикрепленному к заявке (true/false), должно быть включено соответствующее уведомление в разделе СМС/Email - Уведомления туристам / Client notification will be sent to request manager (true/false) |

## POST /service/create

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `r_id` | integer | ✓ | ID заявки (см.метод /request/{id}) / ID of the application (see method /request/{id}) |
| `type_id` | integer | ✓ | Тип услуги (см.метод /service_type) / The service type (see method /service_type) |
| `in_package` | integer |  | Входит в состав пакетного тура (1) или нет (0) / Is part of a packaged tour (1) or not (0) |
| `description` | string |  | Описание услуги / Description of service |
| `date_begin` | datetime |  | Дата начала услуги, формат: Y-m-d / Date of commencement of services, format: Y-m-d |
| `date_end` | datetime |  | Дата окончания услуги, формат: Y-m-d / Date of completion of the services, format: Y-m-d |
| `country` | string |  | Страна / Country |
| `city` | string |  | Курорт / Resort |
| `hotel` | string |  | Отель / The hotel |
| `hotel_type` | string |  | Тип номера / Hotel room type |
| `hotel_place` | string |  | Тип размещения / Hotel placement |
| `nutrition` | string |  | Питание / Food |
| `course` | string |  | Маршрут / Route |
| `duration` | string |  | Длительность / Duration |
| `tourists_count` | integer |  | Количество туристов (взрослые) / The number of tourists (adults) |
| `tourists_child_count` | integer |  | Количество туристов (дети) / The number of tourists (children) |
| `tourists_baby_count` | integer |  | Количество туристов (младенцы) / The number of tourists (infants) |
| `supplier_id` | integer |  | ID партнера / туроператора (см.метод /supplier) / ID of the partner / tour operator (see method /supplier) |
| `currency_id` | integer |  | ID валюты (см.метод /currency) / The currency ID (see method /currency) |
| `currency_id_netto` | integer |  | ID валюты себестоимости (см.метод /currency) / The currency ID of cost (see method /currency) |
| `koef_netto` | float |  | Курс валюты себестоимости (по-умолчанию, 1.00) / Rate cost (default: 1.00) |
| `fix_koef_netto` | integer |  | Фиксировать курс валюты себестоимости / Fix currency rate cost |
| `koef` | float |  | Курс валюты (по-умолчанию, 1.00) / Currency (default: 1.00) |
| `fix_koef` | integer |  | Фиксировать курс валюты / Fix currency rate |
| `price_netto` | float |  | Себестоимость / The cost |
| `price_netto_operator` | float |  | Себестоимость оператора (только для схемы ЦБ - ТА)/ Operator cost (for scheme CB - TA) |
| `price` | float |  | Стоимость клиенту (итоговая) / The cost to the client (final) |
| `price_without_discount` | float |  | Стоимость клиенту без скидки / The cost to the customer without discount |
| `price_discount` | float |  | Размер скидки / The discount |
| `price_discount_is_percent` | integer |  | 0 - скидка в деньгах, 1 - скидка в процентах / 0 - discount-the-money, 1 - the percentage discount |
| `catalog_service_request_id` | integer |  | ID услуги из раздела Я оператор / Service ID from section I operator |
| `catalog_package_id` | integer |  | ID пакета из раздела Я оператор / Package ID from section I operator |
| `catalog_quota_count` | integer |  | Количество услуг/пакета из раздела Я оператор / Service/package ID quota from section I operator |
| `avia_flights` | collection |  | Массив авиаперелетов (см.метод /avia/create) / An array of flights (see method /avia/create) |
| `extended_fields` | array |  | Массив значений дополнительных полей в виде [ID доп.поля => значение, ID доп.поля2 => значение2, ...] (см.метод /extended_field). ВАЖНО! Чтобы дополнительное поле относилось к услуге / Array of values for extended fields [ID field => value, ID field2 => value2, ...] (see method /extended_field) |

## POST /tourists-requests/create

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `r_id` | integer | ✓ | ID заявки (см.метод /request/{id}) / ID of the application (see method /request/{id}) |
| `tourist_id` | integer | ✓ | ID туриста (см.метод /user) / ID of tourist (see method /user) |

## POST /reminder/create

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `r_id` | integer |  | ID заявки (см.метод /request/{id}) / ID of the request (see method /request/{id}) |
| `tr_id` | integer |  | ID туриста (см.метод /user/{id}) / ID of tourist (see method /user/{id}) |
| `type_id` | integer | ✓ | Тип (1 - звонок, 2 - письмо, 3 - встреча, 0 - не определено) / Type (1 - bell, 2 - letter, 3 - meeting, 0 - not identified) |
| `datetime` | datetime | ✓ | Дата напоминания (от), формат: Y-m-d H:i:s (локальное время пользователя) / The reminder date (local time) |
| `datetime_to` | datetime | ✓ | Дата напоминания (до), формат: Y-m-d H:i:s (локальное время пользователя) / The reminder date (local time) |
| `text` | string | ✓ | Текст напоминания / The reminder text |
| `manager_id` | integer |  | ID ответственного менеджера (см.метод /manager), по-умолчанию, прикрепленный менеджер в заявке или в карточке туриста / Manager ID (see /manager), by default attached manager in request or in client |
| `created_u_id` | integer |  | Кто создал напоминание? См.метод /user.json / Who created the reminder? Cm.method /user.json |
| `done` | integer |  | Завершено? (0 - нет, 1 - да), по-умолчанию, = 0 / Is done? (0 - no, 1 - yes), by default = 0 |
| `done_u_id` | integer |  | Кто завершил напоминание? См.метод /user.json / Who completed the reminder? Cm.method /user.json |
| `done_datetime` | datetime |  | Дата завершения напоминания, формат: Y-m-d H:i:s / The reminder complete date, format: Y-m-d H:i:s |

## POST /webhook/create

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `type_id` | integer | ✓ | Тип вебхука / Webhook type: 1 = 'Создание обращения', 2 = 'Создание заявки', 3 = 'Создание клиента', 4 = 'Изменение клиента', 5 = 'Удаление клиента', 6 = 'Создание партнера', 7 = 'Изменение партнера', 8 = 'Удаление партнера', 9 = 'Создание платежа', 10 = 'Изменение платежа', 11 = 'Удаление платежа', |
| `url` | string | ✓ | URL |
| `method` | string |  | Метод (GET/POST/PUT/DELETE), по-умолчанию GET / Method (GET/POST/PUT/DELETE), by default GET |
| `note` | string |  | Примечание / Note |

## POST /request-action/create

| Поле | Тип | Обяз. | Описание |
|------|-----|:-----:|----------|
| `r_id` | integer | ✓ | ID заявки (см.метод /request/{id}). Достаточно передать ИЛИ r_id, ИЛИ tr_id / ID of the application (see method /request/{id}) |
| `tr_id` | integer | ✓ | ID туриста (см.метод /user/{id}). Достаточно передать ИЛИ r_id, ИЛИ tr_id / ID of tourist (see method /user/{id}) |
| `type_id` | integer | ✓ | Тип (1 - звонок, 2 - письмо, 3 - встреча, 0 - не определено) / Type (1 - bell, 2 - letter, 3 - meeting, 0 - not identified) |
| `messenger_id` | string |  | Касание из мессенджера ('vk' - это Вконтакте, 'fb' - это Facebook, 'ok' - это Одноклассники, 'telegram' - это Телеграм, 'max' - это MAX, 'whatsapp' - это WhatsApp, 'viber' - это Viber, 'instagram' - это Instagram), по-умолчанию пусто / Action from messenger ('vk' - vkontakte, 'fb' - facebook, 'ok' - |
| `timezone` | integer |  | Часовой пояс, формат: +ЧЧ:ММ / +Ч / -ЧЧ:ММ / -Ч, по-умолчанию, ставится +03:00 / Timezone, format: +HH:MM / +H / -HH:MM / -H, default is +03:00 |
| `datetime` | datetime | ✓ | Дата касания в часовом поясе параметра timezone, формат: Y-m-d H:i:s / Touch date in timezone parameter, format: Y-m-d H:i:s |
| `text` | string | ✓ | Текст касания / Text touch |
| `u_id` | string |  | Кто создал касание? См.метод /user.json / Who created the touch? Cm.method /user.json |
| `to_u_id` | string |  | Кому создали касание? Используется для мессенджеров. См.метод /user.json / For whom created the touch? Use for messengers. See method /user.json |

