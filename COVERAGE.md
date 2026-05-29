# Покрытие API U-On.Travel в claude-skill-uon-travel

Полная документация: https://api.u-on.ru/doc
Всего эндпоинтов в доке: **150** (уникальных URL: 150)
Покрыто в CLI: **104** прямыми командами
Через `raw get/post` доступны все, дополнительно `(через raw)` помечены — есть пример использования.

## По группам — статус

### 🔴 Прямо не покрыто командой (46 шт)

- `bcard-activate/create`
- `bcard-bonus-by-card/{id}`
- `bcard-bonus-by-user/{id}`
- `bcard-bonus/create`
- `bcard/create`
- `bill/{id}`
- `bills/{page}`
- `cash/create`
- `catalog-package/update/{id}`
- `catalog-package/{id}`
- `catalog-packages/{page}`
- `catalog-service/create`
- `catalog-service/update/{id}`
- `catalog-service/{page}`
- `chat-message/create`
- `city/create`
- `city/update/{id}`
- `country/create`
- `country/update/{id}`
- `mail/create`
- `manager/create`
- `notification/create`
- `notification/{id}`
- `notifications/{page}`
- `nutrition/create`
- `nutrition/update/{id}`
- `paydoc/list/{date_from}/{date_to}`
- `paydoc/list/{date_from}/{date_to}/{page}`
- `paydoc/update/{id}`
- `paydoc/{id}`
- `payment_other_type`
- `reminder-one/{id}`
- `reminder/close/{id}`
- `reminder/{page}`
- `reminder/{r_id}`
- `request-document`
- `request-file/create`
- `request-file/delete/{id}`
- `service-price/delete`
- `service-price/update/{id}`
- `source/create`
- `supplier_type/create`
- `travel-type/create`
- `user-cabinet/create`
- `user-file/create`
- `webhook/update/{id}`

### 🟡 Покрыто через `raw` (есть в примерах)

- `cash`
- `cities/{country_id}`
- `cities/{country_id}/{page}`
- `company`
- `company-office`
- `countries`
- `currency`
- `insurance`
- `manager/{user_id}`
- `nutrition`
- `reason_deny`
- `request-action/{date_from}/{date_to}`
- `request-action/{date_from}/{date_to}/{page}`
- `request-action/{r_id}`
- `request-by-tourist/{id}`
- `request-by-tourist/{id}/{page}`
- `request-deadline/{r_id}`
- `request/search`
- `service/search`
- `travel-type`
- `user/phone/{phone}/{office}`
- `user/search`
- `user/updated/{date_from}/{date_to}`
- `user/updated/{date_from}/{date_to}/{page}`
- `visa`

### 🟢 Покрыто прямой командой (78 шт)

- `avia/create` → `MISSING (можно через services add --type 2)`
- `service-price/create` → `MISSING (расш. блок цена-период для отеля)`
- `request-action/create` → `actions create`
- `call_history_by_request/{r_id}/{page}` → `calls by-request`
- `call_history_by_user/{u_id}/{page}` → `calls by-user`
- `call_history/{page}` → `calls list`
- `call_history/create` → `calls log`
- `request-deadline/create` → `deadlines create`
- `request-deadline/delete` → `deadlines delete`
- `extended_field/create` → `fields create`
- `extended_field/delete/{id}` → `fields delete`
- `extended_field/{page}` → `fields list`
- `extended_field/update/{id}` → `fields update`
- `hotel/create` → `hotels create`
- `hotel/delete/{id}` → `hotels delete`
- `hotel/{id}` → `hotels get`
- `hotels/{page}` → `hotels list`
- `hotel/update/{id}` → `hotels update`
- `user-label` → `labels list`
- `lead-by-client/{id}` → `leads by-client`
- `lead-by-client/{id}/{page}` → `leads by-client --page`
- `lead/create` → `leads create`
- `lead/{id}` → `leads get`
- `lead/{date_from}/{date_to}` → `leads list`
- `leads/{date_from}/{date_to}/{page}` → `leads list`
- `lead/{date_from}/{date_to}/{source_id}` → `leads list --source-id`
- `leads/{date_from}/{date_to}/{source_id}/{page}` → `leads list --source-id`
- `leads/updated/{date_from}/{date_to}/{page}` → `leads updated`
- `manager` → `managers list`
- `manager/office/{office_id}` → `managers list --office-id`
- `paydoc/create` → `paydocs create`
- `paydoc/delete/{id}` → `paydocs delete`
- `payment/create` → `payments create`
- `payment/delete/{id}` → `payments delete`
- `payment_form` → `payments forms`
- `payment/{id}` → `payments get`
- `payment/list/{date_from}/{date_to}/{page}` → `payments list`
- `payment/list/{date_from}/{date_to}` → `payments list (page=1)`
- `payment/update/{id}` → `payments update`
- `reminder/create` → `reminders create`
- `request-by-client/{id}` → `requests by-client`
- `request-by-client/{id}/{page}` → `requests by-client --page`
- `request/create` → `requests create`
- `request/{id}` → `requests get`
- `request/{date_from}/{date_to}` → `requests list`
- `requests/{date_from}/{date_to}/{page}` → `requests list`
- `requests/{date_from}/{date_to}/{source_id}/{page}` → `requests list`
- `requests/closed/{date_from}/{date_to}/{page}` → `requests list --closed`
- `request/{date_from}/{date_to}/{source_id}` → `requests list --source-id`
- `requests/updated/{date_from}/{date_to}/{page}` → `requests list --updated`
- `request/update/{id}` → `requests update / leads update`
- `service/create` → `services add`
- `service/delete` → `services delete`
- `service_type` → `services types`
- `service/update/{id}` → `services update`
- `source` → `sources list`
- `status_cb` → `statuses cb`
- `status_lead` → `statuses leads`
- `status_pay` → `statuses pay`
- `status` → `statuses requests`
- `supplier/create` → `suppliers create`
- `supplier/{id}` → `suppliers get`
- `supplier` → `suppliers list`
- `suppliers/{page}` → `suppliers list --page`
- `supplier_type` → `suppliers types`
- `supplier/update/{id}` → `suppliers update`
- `tourists-requests/create` → `tourists-requests add`
- `tourists-requests/delete` → `tourists-requests remove`
- `user/create` → `users create`
- `user/email` → `users find --email`
- `user/phone/{phone}` → `users find --phone`
- `user/{id}` → `users get`
- `users/{page}` → `users list`
- `user.json` → `users list (deprecated)`
- `user/update/{id}` → `users update`
- `webhook/create` → `webhooks create`
- `webhook/delete/{id}` → `webhooks delete`
- `webhook/{page}` → `webhooks list`

### ⚠️ Не нашёл в доке (наш справочник промахнулся)

- `user.json` (отметка в `covered` но в реальной доке URL отличается)
