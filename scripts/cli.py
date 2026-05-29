#!/usr/bin/env python3
"""uon — единая CLI-обёртка над U-On.Travel API.

Подкоманды покрывают типичные сценарии. Read-only по умолчанию,
write-операции требуют явного --confirm для опасных действий.

Примеры:
    uon leads list --from 2026-05-01 --to 2026-05-29
    uon requests list --from 2026-05-01 --to 2026-05-29 --closed
    uon users find --phone +79991234567
    uon users find --email test@example.com
    uon payments list --from 2026-05-01 --to 2026-05-29
    uon managers list
    uon statuses requests
    uon statuses leads
    uon statuses pay
    uon webhooks list
    uon webhooks create --type 2 --url https://example.com/wh
    uon lead create --name Иван --phone +79991234567 --source-id 1
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import UonClient, dump  # noqa: E402


def cmd_leads_list(args, uon: UonClient) -> None:
    ep = f"leads/{args.date_from}/{args.date_to}/{args.page}"
    if args.source_id:
        ep = f"leads/{args.date_from}/{args.date_to}/{args.source_id}/{args.page}"
    if args.updated:
        ep = f"leads/updated/{args.date_from}/{args.date_to}/{args.page}"
    dump(uon.get(ep))


def cmd_leads_get(args, uon: UonClient) -> None:
    dump(uon.get(f"lead/{args.id}"))


def cmd_leads_by_client(args, uon: UonClient) -> None:
    dump(uon.get(f"lead-by-client/{args.client_id}/{args.page}"))


def cmd_leads_create(args, uon: UonClient) -> None:
    data = {
        # Клиент
        "u_name": args.name,
        "u_surname": args.surname,
        "u_sname": args.patronymic,
        "u_phone_mobile": args.phone,
        "u_email": args.email,
        "u_telegram": args.telegram,
        "u_instagram": args.instagram,
        "u_whatsapp": args.whatsapp,
        "u_viber": args.viber,
        "u_social_vk": args.vk,
        # Бизнес-параметры
        "source": args.source,
        "source_id": args.source_id,
        "status_id": args.status_id,
        "r_u_id": args.manager_id,
        "r_co_id": args.office_id,
        "travel_type_id": args.travel_type_id,
        "touroperator_id": args.touroperator_id,
        "note": args.note,
        # Пожелания клиента
        "countries": args.countries,
        "date_from": args.wish_date_from,
        "date_to": args.wish_date_to,
        "nights_from": args.nights_from,
        "nights_to": args.nights_to,
        "tourist_count": args.adults,
        "tourist_child_count": args.children,
        "tourist_baby_count": args.babies,
        "budget": args.budget,
        "hotel_types": args.hotel_types,
        "nutrition": args.nutrition,
        "requirements_note": args.wish_note,
        # UTM
        "utm_source": args.utm_source,
        "utm_medium": args.utm_medium,
        "utm_campaign": args.utm_campaign,
        "utm_content": args.utm_content,
        "utm_term": args.utm_term,
        # Поведение
        "ignore_actions_and_reminders": 1 if args.no_auto else None,
        "text": args.text,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("lead/create", {k: v for k, v in data.items() if v is not None}))


def cmd_leads_update(args, uon: UonClient) -> None:
    """Lead и Request живут в одной таблице по r_id.
    Обновление идёт через /request/update/{id}, но lead-статус сидит в поле lead_status_id."""
    data = {
        "lead_status_id": args.status_id,
        "manager_id": args.manager_id,
        "r_cl_id": args.client_id,
        "source_id": args.source_id,
        "touroperator_id": args.touroperator_id,
        "reason_deny_id": args.reason_deny_id,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    payload = {k: v for k, v in data.items() if v is not None}
    if not payload:
        sys.exit("Нечего обновлять — задайте --status-id, --manager-id или -F")
    dump(uon.post(f"request/update/{args.id}", payload))


def cmd_requests_list(args, uon: UonClient) -> None:
    if args.closed:
        ep = f"requests/closed/{args.date_from}/{args.date_to}/{args.page}"
    elif args.updated:
        ep = f"requests/updated/{args.date_from}/{args.date_to}/{args.page}"
    elif args.source_id:
        ep = f"requests/{args.date_from}/{args.date_to}/{args.source_id}/{args.page}"
    else:
        ep = f"requests/{args.date_from}/{args.date_to}/{args.page}"
    dump(uon.get(ep))


def cmd_requests_get(args, uon: UonClient) -> None:
    dump(uon.get(f"request/{args.id}"))


def cmd_requests_by_client(args, uon: UonClient) -> None:
    dump(uon.get(f"request-by-client/{args.client_id}/{args.page}"))


def cmd_requests_create(args, uon: UonClient) -> None:
    data = {
        "r_dat_begin": args.date_begin,
        "r_dat_end": args.date_end,
        "r_u_id": args.manager_id,
        "r_cl_id": args.client_id,
        "status_id": args.status_id,
        "source_id": args.source_id,
        "touroperator_id": args.touroperator_id,
        "travel_type_id": args.travel_type_id,
        "countries": args.countries,
        "note": args.note,
        "u_name": args.name,
        "u_surname": args.surname,
        "u_phone_mobile": args.phone,
        "u_email": args.email,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("request/create", {k: v for k, v in data.items() if v is not None}))


def cmd_requests_update(args, uon: UonClient) -> None:
    # NB: поля в /request/update отличаются от /request/create:
    # request_status_id (не status_id), manager_id (без r_), r_cl_id для клиента
    data = {
        "request_status_id": args.status_id,
        "lead_status_id": args.lead_status_id,
        "manager_id": args.manager_id,
        "r_cl_id": args.client_id,
        "source_id": args.source_id,
        "touroperator_id": args.touroperator_id,
        "reservation_number": args.reservation_number,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    payload = {k: v for k, v in data.items() if v is not None}
    if not payload:
        sys.exit("Нечего обновлять — задайте хотя бы один --field или --status-id/--manager-id")
    dump(uon.post(f"request/update/{args.id}", payload))


def cmd_users_list(args, uon: UonClient) -> None:
    dump(uon.get(f"users/{args.page}"))


def cmd_users_get(args, uon: UonClient) -> None:
    dump(uon.get(f"user/{args.id}"))


def cmd_users_find(args, uon: UonClient) -> None:
    if args.phone:
        # phone endpoint требует sanitize
        phone = args.phone.replace("+", "").replace(" ", "").replace("-", "")
        dump(uon.get(f"user/phone/{phone}"))
    elif args.email:
        dump(uon.post("user/email", {"u_email": args.email}))
    else:
        sys.exit("Нужен либо --phone, либо --email")


def _users_payload(args) -> dict:
    """Общий маппинг CLI-аргументов на поля /user/create и /user/update."""
    return {
        # Тип записи и роль клиента
        "u_type": args.type,
        "u_tk_id": args.kind,
        # ФИО
        "u_name": args.name,
        "u_surname": args.surname,
        "u_sname": args.patronymic,
        "u_name_en": args.name_en,
        "u_surname_en": args.surname_en,
        # Демография
        "u_sex": args.sex,
        "u_birthday": args.birthday,
        "u_birthday_place": args.birth_place,
        # Контакты
        "u_phone": args.phone_home_extra,
        "u_phone_mobile": args.phone,
        "u_phone_home": args.phone_home,
        "u_email": args.email,
        "u_address": args.address,
        # Соцсети и мессенджеры
        "u_social_vk": args.vk,
        "u_social_fb": args.fb,
        "u_social_ok": args.ok,
        "u_telegram": args.telegram,
        "u_max": args.max,
        "u_whatsapp": args.whatsapp,
        "u_viber": args.viber,
        "u_instagram": args.instagram,
        # Загранпаспорт
        "u_zagran_number": args.zagran_number,
        "u_zagran_given": args.zagran_given,
        "u_zagran_expire": args.zagran_expire,
        "u_zagran_organization": args.zagran_org,
        # Гражданский паспорт
        "u_passport_number": args.passport_number,
        "u_passport_taken": args.passport_taken,
        "u_passport_date": args.passport_date,
        "u_passport_code": args.passport_code,
        # Свидетельство о рождении
        "u_birthday_certificate": args.cert_number,
        "u_birthday_certificate_given": args.cert_given,
        # Юр. лицо
        "u_company": args.company,
        "u_position": args.position,
        "u_inn": args.inn,
        "u_kpp": args.kpp,
        "u_ogrn": args.ogrn,
        # Связи
        "nationality_id": args.nationality_id,
        "u_office_id": args.office_id,
        "u_manager_id": args.manager_id,
        "u_source": args.referrer_id,
        "u_labels": args.labels,
        # Бонусы и скидки
        "u_discount": args.discount,
        "u_discount_card_number": args.bonus_card,
        "u_note": args.note,
    }


def cmd_users_create(args, uon: UonClient) -> None:
    data = _users_payload(args)
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("user/create", {k: v for k, v in data.items() if v is not None}))


def cmd_users_update(args, uon: UonClient) -> None:
    data = _users_payload(args)
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    payload = {k: v for k, v in data.items() if v is not None}
    if not payload:
        sys.exit("Нечего обновлять — задайте хотя бы одно поле")
    dump(uon.post(f"user/update/{args.id}", payload))


def cmd_labels_list(args, uon: UonClient) -> None:
    dump(uon.get("user-label"))


def cmd_payments_list(args, uon: UonClient) -> None:
    ep = f"payment/list/{args.date_from}/{args.date_to}/{args.page}"
    dump(uon.get(ep))


def cmd_payments_get(args, uon: UonClient) -> None:
    dump(uon.get(f"payment/{args.id}"))


def cmd_payments_create(args, uon: UonClient) -> None:
    # Map "direction" string to cio_id integer
    cio_map = {"in": 1, "income": 1, "arrival": 1, "out": 2, "expense": 2}
    cio_id = cio_map.get((args.direction or "").lower(), 1)
    data = {
        "r_id": args.request_id,
        "client_id": args.tourist_id,
        "cio_id": cio_id,
        "type_id": args.type_id,
        "price": args.amount,
        "currency_id": args.currency_id,
        "form_id": args.form_id,
        "cash_id": args.cash_id,
        "date": args.date,
        "is_plan": 1 if args.plan else None,
        "prepay_id": args.prepay_id,
        "note": args.note,
        "manager_id": args.manager_id,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("payment/create", {k: v for k, v in data.items() if v is not None}))


def cmd_payments_update(args, uon: UonClient) -> None:
    data = {"summa": args.amount, "note": args.note}
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    payload = {k: v for k, v in data.items() if v is not None}
    if not payload:
        sys.exit("Нечего обновлять")
    dump(uon.post(f"payment/update/{args.id}", payload))


def cmd_payments_delete(args, uon: UonClient) -> None:
    if not args.confirm:
        sys.exit("Опасная операция. Подтвердите --confirm")
    dump(uon.post(f"payment/delete/{args.id}", {}))


def cmd_payments_forms(args, uon: UonClient) -> None:
    dump(uon.get("payment_form"))


def cmd_paydocs_get(args, uon: UonClient) -> None:
    dump(uon.get(f"paydoc/{args.id}"))


def cmd_paydocs_list(args, uon: UonClient) -> None:
    ep = f"paydoc/list/{args.date_from}/{args.date_to}/{args.page}"
    dump(uon.get(ep))


def cmd_paydocs_update(args, uon: UonClient) -> None:
    data = {k: v for k, v in {
        "doc_number": args.number, "doc_date": args.date, "summa": args.amount,
    }.items() if v is not None}
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    if not data:
        sys.exit("Нечего обновлять")
    dump(uon.post(f"paydoc/update/{args.id}", data))


def cmd_paydocs_create(args, uon: UonClient) -> None:
    data = {
        "payment_id": args.payment_id,
        "doc_number": args.number,
        "doc_date": args.date,
        "summa": args.amount,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("paydoc/create", {k: v for k, v in data.items() if v is not None}))


def cmd_paydocs_delete(args, uon: UonClient) -> None:
    if not args.confirm:
        sys.exit("Опасная операция. Подтвердите --confirm")
    dump(uon.post(f"paydoc/delete/{args.id}", {}))


def cmd_services_add(args, uon: UonClient) -> None:
    data = {
        "r_id": args.request_id,
        "type_id": args.type,
        "description": args.name,
        "price": args.price_client,
        "price_netto": args.price_netto,
        "currency_id": args.currency_id,
        "date_begin": args.date_begin,
        "date_end": args.date_end,
        "supplier_id": args.supplier_id,
        "hotel": args.hotel,
        "city": args.city,
        "country": args.country,
        "tourists_count": args.tourists_count,
        "nutrition": args.nutrition,
        "hotel_type": args.hotel_type,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("service/create", {k: v for k, v in data.items() if v is not None}))


def cmd_services_update(args, uon: UonClient) -> None:
    data = {
        "price_client": args.price_client,
        "price_netto": args.price_netto,
        "note": args.note,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    payload = {k: v for k, v in data.items() if v is not None}
    if not payload:
        sys.exit("Нечего обновлять")
    dump(uon.post(f"service/update/{args.id}", payload))


def cmd_services_delete(args, uon: UonClient) -> None:
    if not args.confirm:
        sys.exit("Опасная операция. Подтвердите --confirm")
    dump(uon.post("service/delete", {"id": args.id}))


def cmd_services_types(args, uon: UonClient) -> None:
    dump(uon.get("service_type"))


def cmd_bcards_create(args, uon: UonClient) -> None:
    data = {
        "number": args.number, "bonuses": args.bonuses,
        "user_id": args.tourist_id, "manager_id": args.manager_id,
        "active": 0 if args.inactive else None,
    }
    dump(uon.post("bcard/create", {k: v for k, v in data.items() if v is not None}))


def cmd_bcards_activate(args, uon: UonClient) -> None:
    dump(uon.post("bcard-activate/create", {"bc_number": args.number, "user_id": args.tourist_id}))


def cmd_bcards_bonus(args, uon: UonClient) -> None:
    import datetime as _dt
    op_type = 1 if args.add else 2
    data = {
        "bc_id": args.card_id,
        "datetime": args.datetime or _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": op_type,
        "bonuses": args.amount,
        "manager_id": args.manager_id,
        "reason": args.reason,
        "till_date": args.till,
    }
    dump(uon.post("bcard-bonus/create", {k: v for k, v in data.items() if v is not None}))


def cmd_bcards_bonus_by_card(args, uon: UonClient) -> None:
    dump(uon.get(f"bcard-bonus-by-card/{args.card_id}"))


def cmd_bcards_bonus_by_user(args, uon: UonClient) -> None:
    dump(uon.get(f"bcard-bonus-by-user/{args.tourist_id}"))


def cmd_mail_send(args, uon: UonClient) -> None:
    data = {
        "email_to": args.to, "email_from": args.from_,
        "subject": args.subject, "text": args.text,
        "datetime": args.datetime,
    }
    dump(uon.post("mail/create", {k: v for k, v in data.items() if v is not None}))


def cmd_chat_send(args, uon: UonClient) -> None:
    dump(uon.post("chat-message/create", {
        "user_id_from": args.from_id, "user_id_to": args.to_id, "text": args.text,
    }))


def cmd_notifications_list(args, uon: UonClient) -> None:
    dump(uon.get(f"notifications/{args.page}"))


def cmd_notifications_get(args, uon: UonClient) -> None:
    dump(uon.get(f"notification/{args.id}"))


def cmd_notifications_create(args, uon: UonClient) -> None:
    data = {
        "manager_id": args.manager_id, "text": args.text,
        "type": args.type, "request_id": args.request_id,
        "tourist_id": args.tourist_id,
    }
    dump(uon.post("notification/create", {k: v for k, v in data.items() if v is not None}))


def cmd_cash_list(args, uon: UonClient) -> None:
    dump(uon.get("cash"))


def cmd_cash_create(args, uon: UonClient) -> None:
    dump(uon.post("cash/create", {"name": args.name}))


def cmd_bills_get(args, uon: UonClient) -> None:
    dump(uon.get(f"bill/{args.id}"))


def cmd_bills_list(args, uon: UonClient) -> None:
    dump(uon.get(f"bills/{args.page}"))


def cmd_service_price_create(args, uon: UonClient) -> None:
    data = {
        "sr_id": args.service_id,
        "datetime_begin": args.date_begin, "datetime_end": args.date_end,
        "nights": args.nights,
        "price_netto": args.netto_adult, "price_netto_child": args.netto_child, "price_netto_baby": args.netto_baby,
        "price": args.price_adult, "price_child": args.price_child, "price_baby": args.price_baby,
    }
    dump(uon.post("service-price/create", {k: v for k, v in data.items() if v is not None}))


def cmd_service_price_update(args, uon: UonClient) -> None:
    data = {k: v for k, v in {
        "datetime_begin": args.date_begin, "datetime_end": args.date_end,
        "nights": args.nights,
        "price_netto": args.netto_adult, "price": args.price_adult,
        "price_netto_child": args.netto_child, "price_child": args.price_child,
        "price_netto_baby": args.netto_baby, "price_baby": args.price_baby,
    }.items() if v is not None}
    if not data:
        sys.exit("Нечего обновлять")
    dump(uon.post(f"service-price/update/{args.id}", data))


def cmd_service_price_delete(args, uon: UonClient) -> None:
    if not args.confirm:
        sys.exit("Опасная операция. --confirm")
    dump(uon.post("service-price/delete", {"id": args.id}))


def cmd_user_cabinet_create(args, uon: UonClient) -> None:
    dump(uon.post("user-cabinet/create", {"u_id": args.tourist_id}))


def cmd_request_file_attach(args, uon: UonClient) -> None:
    data = {
        "r_id": args.request_id,
        "file_name": args.name,
        "file_url": args.url,
        "file_note": args.note,
        "file_is_private": 1 if args.private else None,
    }
    dump(uon.post("request-file/create", {k: v for k, v in data.items() if v is not None}))


def cmd_request_file_delete(args, uon: UonClient) -> None:
    if not args.confirm:
        sys.exit("Опасная операция. --confirm")
    dump(uon.post(f"request-file/delete/{args.id}", {}))


def cmd_user_file_attach(args, uon: UonClient) -> None:
    data = {
        "u_id": args.tourist_id,
        "filename": args.name,
        "name": args.url,
        "file_note": args.note,
    }
    dump(uon.post("user-file/create", {k: v for k, v in data.items() if v is not None}))


def cmd_webhook_update(args, uon: UonClient) -> None:
    data = {k: v for k, v in {
        "type_id": args.type, "url": args.url, "method": args.method, "note": args.note,
    }.items() if v is not None}
    if not data:
        sys.exit("Нечего обновлять")
    dump(uon.post(f"webhook/update/{args.id}", data))


def cmd_manager_create(args, uon: UonClient) -> None:
    data = {
        "u_name": args.name,
        "u_surname": args.surname,
        "u_sname": args.patronymic,
        "u_email": args.email,
        "u_password": args.password,
        "u_phone_mobile": args.phone,
        "u_company_id": args.company_id,
        "u_office_id": args.office_id,
        "u_gr_id": 2,
        "u_birthday": args.birthday,
        "u_note": args.note,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("manager/create", {k: v for k, v in data.items() if v is not None}))


def cmd_payment_other_types(args, uon: UonClient) -> None:
    dump(uon.get("payment_other_type"))


def cmd_document_generate(args, uon: UonClient) -> None:
    data = {
        "template_id": args.template_id,
        "request_id": args.request_id,
        "bill_id": args.bill_id,
        "supplier_id": args.supplier_id,
        "tourist_id": args.tourist_id,
        "print_and_sign": 1 if args.with_sign else None,
        "date": args.date,
        "format": args.format,
        "locale": args.locale,
        "is_custom": 1 if args.custom else None,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("request-document", {k: v for k, v in data.items() if v is not None}))


def cmd_tourists_add(args, uon: UonClient) -> None:
    dump(uon.post("tourists-requests/create", {"r_id": args.request_id, "tourist_id": args.tourist_id}))


def cmd_tourists_remove(args, uon: UonClient) -> None:
    if not args.confirm:
        sys.exit("Опасная операция. Подтвердите --confirm")
    dump(uon.post("tourists-requests/delete", {"r_id": args.request_id, "tourist_id": args.tourist_id}))


def cmd_actions_create(args, uon: UonClient) -> None:
    import datetime as _dt
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "r_id": args.request_id,
        "tr_id": args.tourist_id,
        "type_id": args.type_id,
        "datetime": args.datetime or now,
        "text": args.text,
        "u_id": args.manager_id,
        "messenger_id": args.messenger,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("request-action/create", {k: v for k, v in data.items() if v is not None}))


def cmd_deadlines_create(args, uon: UonClient) -> None:
    data = {
        "r_id": args.request_id,
        "date": args.date,
        "type_id": args.type_id,
        "summ": args.amount,
        "percent": args.percent,
        "is_current": 1 if args.current else None,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("request-deadline/create", {k: v for k, v in data.items() if v is not None}))


def cmd_deadlines_delete(args, uon: UonClient) -> None:
    if not args.confirm:
        sys.exit("Опасная операция. Подтвердите --confirm")
    dump(uon.post("request-deadline/delete", {"id": args.id}))


def cmd_managers_list(args, uon: UonClient) -> None:
    if args.office_id:
        dump(uon.get(f"manager/office/{args.office_id}"))
    else:
        dump(uon.get("manager"))


def cmd_statuses(args, uon: UonClient) -> None:
    mapping = {
        "requests": "status",
        "leads": "status_lead",
        "pay": "status_pay",
        "cb": "status_cb",
    }
    dump(uon.get(mapping[args.kind]))


def cmd_sources_list(args, uon: UonClient) -> None:
    dump(uon.get("source"))


def cmd_sources_create(args, uon: UonClient) -> None:
    dump(uon.post("source/create", {"rs_name": args.name}))


def cmd_travel_types_list(args, uon: UonClient) -> None:
    dump(uon.get("travel-type"))


def cmd_travel_types_create(args, uon: UonClient) -> None:
    dump(uon.post("travel-type/create", {"name": args.name}))


def cmd_nutrition_list(args, uon: UonClient) -> None:
    dump(uon.get("nutrition"))


def cmd_nutrition_create(args, uon: UonClient) -> None:
    dump(uon.post("nutrition/create", {"name": args.name}))


def cmd_nutrition_update(args, uon: UonClient) -> None:
    dump(uon.post(f"nutrition/update/{args.id}", {"name": args.name}))


def cmd_countries_list(args, uon: UonClient) -> None:
    dump(uon.get("countries"))


def cmd_countries_create(args, uon: UonClient) -> None:
    dump(uon.post("country/create", {"name": args.name}))


def cmd_countries_update(args, uon: UonClient) -> None:
    dump(uon.post(f"country/update/{args.id}", {"name": args.name}))


def cmd_cities_list(args, uon: UonClient) -> None:
    ep = f"cities/{args.country_id}/{args.page}" if args.page > 1 else f"cities/{args.country_id}"
    dump(uon.get(ep))


def cmd_cities_create(args, uon: UonClient) -> None:
    dump(uon.post("city/create", {"name": args.name, "country_id": args.country_id}))


def cmd_cities_update(args, uon: UonClient) -> None:
    dump(uon.post(f"city/update/{args.id}", {"name": args.name}))


def cmd_supplier_type_create(args, uon: UonClient) -> None:
    dump(uon.post("supplier_type/create", {"name": args.name}))


def cmd_webhooks_list(args, uon: UonClient) -> None:
    dump(uon.get(f"webhook/{args.page}"))


def cmd_webhooks_create(args, uon: UonClient) -> None:
    dump(uon.post("webhook/create", {"type_id": args.type, "url": args.url, "note": args.note or ""}))


def cmd_webhooks_delete(args, uon: UonClient) -> None:
    dump(uon.post(f"webhook/delete/{args.id}", {}))


def cmd_reminders_list(args, uon: UonClient) -> None:
    dump(uon.get(f"reminder/{args.page}"))


def cmd_reminders_get(args, uon: UonClient) -> None:
    dump(uon.get(f"reminder-one/{args.id}"))


def cmd_reminders_by_request(args, uon: UonClient) -> None:
    dump(uon.get(f"reminder/{args.request_id}"))


def cmd_reminders_close(args, uon: UonClient) -> None:
    import datetime as _dt
    data = {
        "done_u_id": args.done_by,
        "done_datetime": args.done_at or _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    payload = {k: v for k, v in data.items() if v is not None}
    dump(uon.post(f"reminder/close/{args.id}", payload))


def cmd_reminders_create(args, uon: UonClient) -> None:
    data = {
        "r_id": args.request_id,
        "tr_id": args.tourist_id,
        "manager_id": args.manager_id,
        "text": args.text,
        "type_id": args.type_id,
        "datetime": args.date_from,
        "datetime_to": args.date_to,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("reminder/create", {k: v for k, v in data.items() if v is not None}))


def cmd_fields_list(args, uon: UonClient) -> None:
    resp = uon.get(f"extended_field/{args.page}")
    # фильтр по разделу если указан
    if args.section:
        recs = resp.get("records", [])
        recs = [r for r in recs if r.get("section") == args.section]
        resp["records"] = recs
    dump(resp)


def cmd_fields_create(args, uon: UonClient) -> None:
    data = {
        "section": args.section,
        "name": args.name,
        "type": args.type,
        "options": args.options,
    }
    dump(uon.post("extended_field/create", {k: v for k, v in data.items() if v is not None}))


def cmd_fields_update(args, uon: UonClient) -> None:
    data = {k: v for k, v in {
        "section": args.section, "name": args.name, "type": args.type, "options": args.options,
    }.items() if v is not None}
    if not data:
        sys.exit("Нечего обновлять")
    dump(uon.post(f"extended_field/update/{args.id}", data))


def cmd_fields_delete(args, uon: UonClient) -> None:
    if not args.confirm:
        sys.exit("Опасная операция. --confirm")
    dump(uon.post(f"extended_field/delete/{args.id}", {}))


def cmd_calls_log(args, uon: UonClient) -> None:
    import datetime as _dt
    data = {
        "phone": args.phone,
        "start": args.start or _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "direction": 2 if args.inbound else 1,
        "duration": args.duration,
        "record_link": args.record,
        "manager_id": args.manager_id,
        "office_id": args.office_id,
        "note": args.note,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("call_history/create", {k: v for k, v in data.items() if v is not None}))


def cmd_calls_list(args, uon: UonClient) -> None:
    dump(uon.get(f"call_history/{args.page}"))


def cmd_calls_by_request(args, uon: UonClient) -> None:
    dump(uon.get(f"call_history_by_request/{args.request_id}/{args.page}"))


def cmd_calls_by_user(args, uon: UonClient) -> None:
    dump(uon.get(f"call_history_by_user/{args.tourist_id}/{args.page}"))


def cmd_hotels_list(args, uon: UonClient) -> None:
    dump(uon.get(f"hotels/{args.page}"))


def cmd_hotels_get(args, uon: UonClient) -> None:
    dump(uon.get(f"hotel/{args.id}"))


def cmd_hotels_create(args, uon: UonClient) -> None:
    data = {
        "name": args.name,
        "city_id": args.city_id,
        "country_id": args.country_id,
        "stars": args.stars,
        "address": args.address,
        "phone": args.phone,
        "website": args.website,
        "email": args.email,
        "note": args.note,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("hotel/create", {k: v for k, v in data.items() if v is not None}))


def cmd_hotels_update(args, uon: UonClient) -> None:
    data = {k: v for k, v in {
        "name": args.name, "stars": args.stars, "address": args.address,
        "phone": args.phone, "website": args.website, "email": args.email,
        "note": args.note,
    }.items() if v is not None}
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    if not data:
        sys.exit("Нечего обновлять")
    dump(uon.post(f"hotel/update/{args.id}", data))


def cmd_hotels_delete(args, uon: UonClient) -> None:
    if not args.confirm:
        sys.exit("Опасная операция. --confirm")
    dump(uon.post(f"hotel/delete/{args.id}", {}))


def cmd_suppliers_list(args, uon: UonClient) -> None:
    if args.page > 1:
        dump(uon.get(f"suppliers/{args.page}"))
    else:
        dump(uon.get("supplier"))


def cmd_suppliers_get(args, uon: UonClient) -> None:
    dump(uon.get(f"supplier/{args.id}"))


def cmd_suppliers_create(args, uon: UonClient) -> None:
    data = {
        "name": args.name,
        "name_official": args.name_official,
        "type_id": args.type_id,
        "inn": args.inn,
        "kpp": args.kpp,
        "phone": args.phone,
        "email": args.email,
        "website": args.website,
        "note": args.note,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("supplier/create", {k: v for k, v in data.items() if v is not None}))


def cmd_suppliers_update(args, uon: UonClient) -> None:
    data = {k: v for k, v in {
        "name": args.name, "phone": args.phone, "email": args.email,
        "website": args.website, "note": args.note,
    }.items() if v is not None}
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    if not data:
        sys.exit("Нечего обновлять")
    dump(uon.post(f"supplier/update/{args.id}", data))


def cmd_supplier_types(args, uon: UonClient) -> None:
    dump(uon.get("supplier_type"))


def cmd_raw_get(args, uon: UonClient) -> None:
    dump(uon.get(args.endpoint))


def cmd_raw_post(args, uon: UonClient) -> None:
    data = {}
    for pair in args.field or []:
        k, _, v = pair.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post(args.endpoint, data))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="uon", description="U-On.Travel API CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    # leads
    leads = sub.add_parser("leads", help="Обращения (lead — до конверсии в заявку)")
    leads_sub = leads.add_subparsers(dest="sub", required=True)
    _add_period(leads_sub.add_parser("list", help="Список за период")).set_defaults(
        func=cmd_leads_list, source_id=None, updated=False
    )
    _add_period(leads_sub.add_parser("updated", help="Только обновлённые за период")).set_defaults(
        func=cmd_leads_list, source_id=None, updated=True
    )
    g = leads_sub.add_parser("get", help="Получить обращение по id")
    g.add_argument("id", type=int)
    g.set_defaults(func=cmd_leads_get)
    bc = leads_sub.add_parser("by-client", help="Обращения по клиенту")
    bc.add_argument("client_id", type=int)
    bc.add_argument("--page", type=int, default=1)
    bc.set_defaults(func=cmd_leads_by_client)
    cr = leads_sub.add_parser("create", help="Создать обращение со всеми полями карточки")
    # Клиент
    cr.add_argument("--name", required=True, help="Имя клиента")
    cr.add_argument("--surname", default=None)
    cr.add_argument("--patronymic", default=None, help="Отчество (u_sname)")
    cr.add_argument("--phone", required=True)
    cr.add_argument("--email", default=None)
    cr.add_argument("--telegram", default=None)
    cr.add_argument("--instagram", default=None)
    cr.add_argument("--whatsapp", default=None)
    cr.add_argument("--viber", default=None)
    cr.add_argument("--vk", default=None, help="ВКонтакте")
    # Бизнес
    cr.add_argument("--source", default=None, help="Источник (строкой). Если есть в кабинете — используй --source-id")
    cr.add_argument("--source-id", type=int, default=None, dest="source_id")
    cr.add_argument("--status-id", type=int, default=None, dest="status_id", help="ID lead-статуса (см. statuses leads)")
    cr.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    cr.add_argument("--office-id", type=int, default=None, dest="office_id")
    cr.add_argument("--travel-type-id", type=int, default=None, dest="travel_type_id")
    cr.add_argument("--touroperator-id", type=int, default=None, dest="touroperator_id")
    cr.add_argument("--note", default=None, help="Примечание для менеджера")
    cr.add_argument("--text", default=None, help="Текст обращения (что просит клиент)")
    # Пожелания клиента
    cr.add_argument("--countries", default=None, help="ID стран через запятую (см. uon raw get countries)")
    cr.add_argument("--wish-date-from", default=None, dest="wish_date_from", help="Желаемая дата начала YYYY-MM-DD")
    cr.add_argument("--wish-date-to", default=None, dest="wish_date_to")
    cr.add_argument("--nights-from", default=None, dest="nights_from")
    cr.add_argument("--nights-to", default=None, dest="nights_to")
    cr.add_argument("--adults", default=None, help="Кол-во взрослых (tourist_count)")
    cr.add_argument("--children", default=None, help="Кол-во детей (tourist_child_count)")
    cr.add_argument("--babies", default=None, help="Кол-во младенцев (tourist_baby_count)")
    cr.add_argument("--budget", default=None, help="Бюджет клиента (число)")
    cr.add_argument("--hotel-types", default=None, dest="hotel_types",
                    help="Категории отелей через запятую из 1*,2*,3*,4*,5*,5+*,Apts,Villa")
    cr.add_argument("--nutrition", default=None,
                    help="Питание через запятую из RO,BB,HB,HB+,FB,FB+,AI,UAI")
    cr.add_argument("--wish-note", default=None, dest="wish_note", help="Примечание к пожеланиям")
    # UTM
    cr.add_argument("--utm-source", default=None, dest="utm_source")
    cr.add_argument("--utm-medium", default=None, dest="utm_medium")
    cr.add_argument("--utm-campaign", default=None, dest="utm_campaign")
    cr.add_argument("--utm-content", default=None, dest="utm_content")
    cr.add_argument("--utm-term", default=None, dest="utm_term")
    # Поведение
    cr.add_argument("--no-auto", action="store_true", dest="no_auto",
                    help="Не создавать стандартный 'Заполнить данные клиента' напоминание")
    cr.add_argument("-F", "--field", action="append", help="Доп. поле key=value (extended_fields[N], reason_deny_id, ...)")
    cr.set_defaults(func=cmd_leads_create)

    lup = leads_sub.add_parser("update", help="Обновить обращение / двинуть статус")
    lup.add_argument("id", type=int)
    lup.add_argument("--status-id", type=int, default=None, dest="status_id",
                     help="Новый lead_status_id (см. statuses leads)")
    lup.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    lup.add_argument("--client-id", type=int, default=None, dest="client_id")
    lup.add_argument("--source-id", type=int, default=None, dest="source_id")
    lup.add_argument("--touroperator-id", type=int, default=None, dest="touroperator_id")
    lup.add_argument("--reason-deny-id", type=int, default=None, dest="reason_deny_id",
                     help="ID причины отказа (для перевода в статус 'Отказ')")
    lup.add_argument("-F", "--field", action="append")
    lup.set_defaults(func=cmd_leads_update)

    # requests
    reqs = sub.add_parser("requests", help="Заявки (request — реальный тур)")
    reqs_sub = reqs.add_subparsers(dest="sub", required=True)
    rl = _add_period(reqs_sub.add_parser("list", help="Список за период"))
    rl.add_argument("--closed", action="store_true", help="Только закрытые")
    rl.add_argument("--updated", action="store_true", help="Только обновлённые")
    rl.set_defaults(func=cmd_requests_list)
    rg = reqs_sub.add_parser("get", help="Получить заявку по id")
    rg.add_argument("id", type=int)
    rg.set_defaults(func=cmd_requests_get)
    rbc = reqs_sub.add_parser("by-client", help="Заявки по клиенту")
    rbc.add_argument("client_id", type=int)
    rbc.add_argument("--page", type=int, default=1)
    rbc.set_defaults(func=cmd_requests_by_client)

    rcr = reqs_sub.add_parser("create", help="Создать заявку")
    rcr.add_argument("--name", default=None, help="Имя клиента (если нет client_id)")
    rcr.add_argument("--surname", default=None)
    rcr.add_argument("--phone", default=None, help="Моб. телефон клиента")
    rcr.add_argument("--email", default=None)
    rcr.add_argument("--client-id", type=int, default=None, dest="client_id")
    rcr.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    rcr.add_argument("--status-id", type=int, default=None, dest="status_id")
    rcr.add_argument("--source-id", type=int, default=None, dest="source_id")
    rcr.add_argument("--touroperator-id", type=int, default=None, dest="touroperator_id")
    rcr.add_argument("--travel-type-id", type=int, default=None, dest="travel_type_id")
    rcr.add_argument("--countries", default=None, help="ID стран через запятую")
    rcr.add_argument("--date-begin", default=None, dest="date_begin", help="YYYY-MM-DD HH:MM:SS")
    rcr.add_argument("--date-end", default=None, dest="date_end")
    rcr.add_argument("--note", default=None)
    rcr.add_argument("-F", "--field", action="append", help="дополнительное поле key=value")
    rcr.set_defaults(func=cmd_requests_create)

    rup = reqs_sub.add_parser("update", help="Обновить заявку (поля отличаются от create!)")
    rup.add_argument("id", type=int)
    rup.add_argument("--status-id", type=int, default=None, dest="status_id", help="request_status_id (отличается от create!)")
    rup.add_argument("--lead-status-id", type=int, default=None, dest="lead_status_id")
    rup.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    rup.add_argument("--client-id", type=int, default=None, dest="client_id", help="r_cl_id")
    rup.add_argument("--source-id", type=int, default=None, dest="source_id")
    rup.add_argument("--touroperator-id", type=int, default=None, dest="touroperator_id")
    rup.add_argument("--reservation-number", default=None, dest="reservation_number")
    rup.add_argument("-F", "--field", action="append", help="Доп. поле key=value (см. references/fields.md)")
    rup.set_defaults(func=cmd_requests_update)

    # users
    users = sub.add_parser("users", help="Туристы / клиенты")
    users_sub = users.add_subparsers(dest="sub", required=True)
    ul = users_sub.add_parser("list", help="Список туристов")
    ul.add_argument("--page", type=int, default=1)
    ul.set_defaults(func=cmd_users_list)
    ug = users_sub.add_parser("get", help="Получить туриста по id")
    ug.add_argument("id", type=int)
    ug.set_defaults(func=cmd_users_get)
    uf = users_sub.add_parser("find", help="Поиск по телефону или email")
    uf.add_argument("--phone", default=None)
    uf.add_argument("--email", default=None)
    uf.set_defaults(func=cmd_users_find)
    def _user_args(p, *, name_required: bool, phone_required: bool):
        # ФИО
        p.add_argument("--name", required=name_required)
        p.add_argument("--surname", default=None)
        p.add_argument("--patronymic", default=None, help="Отчество (u_sname)")
        p.add_argument("--name-en", default=None, dest="name_en", help="Имя латиницей (для виз)")
        p.add_argument("--surname-en", default=None, dest="surname_en")
        # Демография
        p.add_argument("--sex", default=None, choices=["м", "ж"], help="Пол")
        p.add_argument("--birthday", default=None, help="День рождения YYYY-MM-DD")
        p.add_argument("--birth-place", default=None, dest="birth_place", help="Место рождения")
        # Тип записи
        p.add_argument("--type", type=int, default=None, choices=[1, 2, 3],
                       help="1=физ.лицо (default), 2=юр.лицо, 3=турагентство")
        p.add_argument("--kind", type=int, default=None, choices=[1, 2, 3, 4, 5],
                       help="Тип клиента: 1=Mr, 2=Mrs, 3=Miss, 4=Child, 5=Infant")
        # Контакты
        p.add_argument("--phone", required=phone_required, help="Моб. телефон (u_phone_mobile)")
        p.add_argument("--phone-home", default=None, dest="phone_home", help="Домашний (u_phone_home)")
        p.add_argument("--phone-extra", default=None, dest="phone_home_extra", help="Доп. контактный (u_phone)")
        p.add_argument("--email", default=None)
        p.add_argument("--address", default=None, help="Адрес фактический")
        # Соцсети и мессенджеры
        p.add_argument("--vk", default=None, help="Ссылка ВКонтакте")
        p.add_argument("--fb", default=None, help="Ссылка Facebook")
        p.add_argument("--ok", default=None, help="Ссылка Одноклассники")
        p.add_argument("--telegram", default=None)
        p.add_argument("--max", default=None, help="Мессенджер MAX")
        p.add_argument("--whatsapp", default=None)
        p.add_argument("--viber", default=None)
        p.add_argument("--instagram", default=None)
        # Загранпаспорт
        p.add_argument("--zagran-number", default=None, dest="zagran_number", help="Серия+номер загранпаспорта")
        p.add_argument("--zagran-given", default=None, dest="zagran_given", help="Дата выдачи YYYY-MM-DD")
        p.add_argument("--zagran-expire", default=None, dest="zagran_expire", help="Дата окончания YYYY-MM-DD")
        p.add_argument("--zagran-org", default=None, dest="zagran_org", help="Орган, выдавший загранпаспорт")
        # Гражданский паспорт
        p.add_argument("--passport-number", default=None, dest="passport_number", help="Серия+номер гражданского")
        p.add_argument("--passport-taken", default=None, dest="passport_taken", help="Кем выдан")
        p.add_argument("--passport-date", default=None, dest="passport_date", help="Дата выдачи YYYY-MM-DD")
        p.add_argument("--passport-code", default=None, dest="passport_code", help="Код подразделения")
        # Свидетельство о рождении
        p.add_argument("--cert-number", default=None, dest="cert_number", help="Серия+номер свидетельства о рождении")
        p.add_argument("--cert-given", default=None, dest="cert_given", help="Дата выдачи YYYY-MM-DD")
        # Юр. лицо
        p.add_argument("--company", default=None, help="Название компании (для юр.лица)")
        p.add_argument("--position", default=None, help="Должность (для юр.лица)")
        p.add_argument("--inn", default=None)
        p.add_argument("--kpp", default=None)
        p.add_argument("--ogrn", default=None)
        # Связи и метки
        p.add_argument("--nationality-id", type=int, default=None, dest="nationality_id", help="ID страны гражданства")
        p.add_argument("--office-id", type=int, default=None, dest="office_id")
        p.add_argument("--manager-id", type=int, default=None, dest="manager_id")
        p.add_argument("--referrer-id", type=int, default=None, dest="referrer_id",
                       help="ID туриста, который привёл этого клиента (u_source)")
        p.add_argument("--labels", default=None, help="Метки через запятую (см. labels list): VIP,Семья,Эконом")
        # Бонусы
        p.add_argument("--discount", default=None, help="Скидка клиента")
        p.add_argument("--bonus-card", default=None, dest="bonus_card", help="Номер бонусной карты")
        # Прочее
        p.add_argument("--note", default=None, help="Примечание")
        p.add_argument("-F", "--field", action="append", help="Доп. поле: -F extended_fields[ID]=value")

    uc = users_sub.add_parser("create", help="Создать туриста / клиента / юр.лицо")
    _user_args(uc, name_required=True, phone_required=True)
    uc.set_defaults(func=cmd_users_create)

    uu = users_sub.add_parser("update", help="Обновить любое поле карточки клиента")
    uu.add_argument("id", type=int)
    _user_args(uu, name_required=False, phone_required=False)
    uu.set_defaults(func=cmd_users_update)

    # labels
    lb = sub.add_parser("labels", help="Метки клиентов")
    lb_sub = lb.add_subparsers(dest="sub", required=True)
    lbl = lb_sub.add_parser("list", help="Список меток (создание/удаление только в UI)")
    lbl.set_defaults(func=cmd_labels_list)

    # payments
    pays = sub.add_parser("payments", help="Платежи")
    pays_sub = pays.add_subparsers(dest="sub", required=True)
    _add_period(pays_sub.add_parser("list", help="Список платежей за период")).set_defaults(
        func=cmd_payments_list
    )
    pg = pays_sub.add_parser("get", help="Платёж по id")
    pg.add_argument("id", type=int)
    pg.set_defaults(func=cmd_payments_get)

    pcr = pays_sub.add_parser("create", help="Создать платёж")
    pcr.add_argument("--request-id", type=int, required=True, dest="request_id")
    pcr.add_argument("--tourist-id", type=int, default=None, dest="tourist_id", help="ID клиента-заказчика (поле client_id)")
    pcr.add_argument("--amount", required=True, help="Сумма платежа (поле price)")
    pcr.add_argument("--direction", default="in", choices=["in", "out", "income", "expense"], help="Приход (in) или расход (out); default=in")
    pcr.add_argument("--type-id", type=int, default=1, dest="type_id", help="1=расчёты с клиентами, 2=с партнёрами; default=1")
    pcr.add_argument("--currency-id", type=int, default=1, dest="currency_id", help="Default: 1 (рубль)")
    pcr.add_argument("--form-id", type=int, default=None, dest="form_id", help="ID формы оплаты (1=наличный, 2=безналичный, 3=карта... см. payments forms)")
    pcr.add_argument("--cash-id", type=int, default=None, dest="cash_id")
    pcr.add_argument("--date", default=None, help="YYYY-MM-DD HH:MM:SS, default — сейчас")
    pcr.add_argument("--plan", action="store_true", help="Плановый платёж (is_plan=1)")
    pcr.add_argument("--prepay-id", type=int, default=None, dest="prepay_id", help="1=предоплата, 2=доплата, 3=полная оплата")
    pcr.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    pcr.add_argument("--note", default=None)
    pcr.add_argument("-F", "--field", action="append")
    pcr.set_defaults(func=cmd_payments_create)

    pup = pays_sub.add_parser("update", help="Обновить платёж")
    pup.add_argument("id", type=int)
    pup.add_argument("--amount", default=None)
    pup.add_argument("--note", default=None)
    pup.add_argument("-F", "--field", action="append")
    pup.set_defaults(func=cmd_payments_update)

    pdl = pays_sub.add_parser("delete", help="Удалить платёж")
    pdl.add_argument("id", type=int)
    pdl.add_argument("--confirm", action="store_true")
    pdl.set_defaults(func=cmd_payments_delete)

    pf = pays_sub.add_parser("forms", help="Список форм оплаты (наличные, картой, банк, СБП...)")
    pf.set_defaults(func=cmd_payments_forms)
    pot = pays_sub.add_parser("other-types", help="Типы косвенных платежей (списания/комиссии)")
    pot.set_defaults(func=cmd_payment_other_types)

    # paydocs
    pd = sub.add_parser("paydocs", help="Счета (paydoc) внутри платежей")
    pd_sub = pd.add_subparsers(dest="sub", required=True)
    pdc = pd_sub.add_parser("create", help="Добавить счёт в платёж")
    pdc.add_argument("--payment-id", type=int, required=True, dest="payment_id")
    pdc.add_argument("--number", required=True, help="Номер документа")
    pdc.add_argument("--date", required=True, help="YYYY-MM-DD")
    pdc.add_argument("--amount", required=True)
    pdc.add_argument("-F", "--field", action="append")
    pdc.set_defaults(func=cmd_paydocs_create)
    pdd = pd_sub.add_parser("delete", help="Удалить счёт")
    pdd.add_argument("id", type=int)
    pdd.add_argument("--confirm", action="store_true")
    pdd.set_defaults(func=cmd_paydocs_delete)
    pdg = pd_sub.add_parser("get", help="Счёт по id")
    pdg.add_argument("id", type=int)
    pdg.set_defaults(func=cmd_paydocs_get)
    pdl = pd_sub.add_parser("list", help="Список счетов за период")
    pdl.add_argument("--from", required=True, dest="date_from")
    pdl.add_argument("--to", required=True, dest="date_to")
    pdl.add_argument("--page", type=int, default=1)
    pdl.set_defaults(func=cmd_paydocs_list)
    pdu = pd_sub.add_parser("update", help="Обновить счёт")
    pdu.add_argument("id", type=int)
    pdu.add_argument("--number", default=None)
    pdu.add_argument("--date", default=None)
    pdu.add_argument("--amount", default=None)
    pdu.add_argument("-F", "--field", action="append")
    pdu.set_defaults(func=cmd_paydocs_update)

    # services (внутри заявки)
    svc = sub.add_parser("services", help="Услуги в заявке (отель, авиа, страховка, виза, питание, трансфер)")
    svc_sub = svc.add_subparsers(dest="sub", required=True)
    sa = svc_sub.add_parser("add", help="Добавить услугу в заявку")
    sa.add_argument("--request-id", type=int, required=True, dest="request_id")
    sa.add_argument("--type", type=int, required=True, help="ID типа услуги (1=Отель, 2=Трансфер... см. services types)")
    sa.add_argument("--name", default=None, help="description (название/описание услуги)")
    sa.add_argument("--price-client", default=None, dest="price_client", help="Цена клиенту (поле price)")
    sa.add_argument("--price-netto", default=None, dest="price_netto", help="Цена-нетто (закупка)")
    sa.add_argument("--currency-id", type=int, default=1, dest="currency_id")
    sa.add_argument("--date-begin", default=None, dest="date_begin", help="YYYY-MM-DD HH:MM:SS")
    sa.add_argument("--date-end", default=None, dest="date_end")
    sa.add_argument("--supplier-id", type=int, default=None, dest="supplier_id")
    sa.add_argument("--hotel", default=None, help="Название отеля (строкой)")
    sa.add_argument("--city", default=None, help="Город (строкой)")
    sa.add_argument("--country", default=None, help="Страна (строкой)")
    sa.add_argument("--tourists-count", type=int, default=None, dest="tourists_count")
    sa.add_argument("--nutrition", default=None, help="Тип питания (для type=1): RO/BB/HB/FB/AI/UAI")
    sa.add_argument("--hotel-type", default=None, dest="hotel_type", help="Категория (для type=1): 3*/4*/5*/Apts/Villa")
    sa.add_argument("-F", "--field", action="append", help="Доп. поле key=value")
    sa.set_defaults(func=cmd_services_add)
    su = svc_sub.add_parser("update", help="Обновить услугу")
    su.add_argument("id", type=int)
    su.add_argument("--price-client", default=None, dest="price_client")
    su.add_argument("--price-netto", default=None, dest="price_netto")
    su.add_argument("--note", default=None)
    su.add_argument("-F", "--field", action="append")
    su.set_defaults(func=cmd_services_update)
    sd = svc_sub.add_parser("delete", help="Удалить услугу из заявки")
    sd.add_argument("id", type=int)
    sd.add_argument("--confirm", action="store_true")
    sd.set_defaults(func=cmd_services_delete)
    st_ = svc_sub.add_parser("types", help="Список типов услуг")
    st_.set_defaults(func=cmd_services_types)

    # bcards (bonus cards)
    bc = sub.add_parser("bcards", help="Бонусные карты (программа лояльности)")
    bc_sub = bc.add_subparsers(dest="sub", required=True)
    bcc = bc_sub.add_parser("create", help="Выпустить карту")
    bcc.add_argument("--number", required=True)
    bcc.add_argument("--tourist-id", type=int, default=None, dest="tourist_id")
    bcc.add_argument("--bonuses", default=None, help="Начальные баллы")
    bcc.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    bcc.add_argument("--inactive", action="store_true", help="Создать неактивной")
    bcc.set_defaults(func=cmd_bcards_create)
    bca = bc_sub.add_parser("activate", help="Активировать карту для клиента")
    bca.add_argument("--number", required=True)
    bca.add_argument("--tourist-id", type=int, required=True, dest="tourist_id")
    bca.set_defaults(func=cmd_bcards_activate)
    bcb = bc_sub.add_parser("bonus", help="Начислить/списать баллы")
    bcb.add_argument("--card-id", type=int, required=True, dest="card_id")
    bcb.add_argument("--amount", required=True, help="Количество баллов")
    bcb.add_argument("--add", action="store_true", help="Начислить (default — добавить)")
    bcb.add_argument("--debit", action="store_true", help="Списать (включает --add=false)")
    bcb.add_argument("--datetime", default=None)
    bcb.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    bcb.add_argument("--reason", default=None)
    bcb.add_argument("--till", default=None, help="До какой даты действуют YYYY-MM-DD")
    bcb.set_defaults(func=cmd_bcards_bonus)
    bcbc = bc_sub.add_parser("history-by-card", help="История бонусов по карте")
    bcbc.add_argument("card_id", type=int)
    bcbc.set_defaults(func=cmd_bcards_bonus_by_card)
    bcbu = bc_sub.add_parser("history-by-user", help="История бонусов по клиенту")
    bcbu.add_argument("tourist_id", type=int)
    bcbu.set_defaults(func=cmd_bcards_bonus_by_user)

    # mail
    ml_ = sub.add_parser("mail", help="Письма")
    ml_sub = ml_.add_subparsers(dest="sub", required=True)
    mls = ml_sub.add_parser("send", help="Отправить письмо")
    mls.add_argument("--to", required=True)
    mls.add_argument("--from", required=True, dest="from_")
    mls.add_argument("--subject", required=True)
    mls.add_argument("--text", required=True)
    mls.add_argument("--datetime", default=None)
    mls.set_defaults(func=cmd_mail_send)

    # chat (внутренний)
    ch = sub.add_parser("chat", help="Внутренний чат CRM")
    ch_sub = ch.add_subparsers(dest="sub", required=True)
    chs = ch_sub.add_parser("send", help="Отправить сообщение")
    chs.add_argument("--from-id", type=int, required=True, dest="from_id")
    chs.add_argument("--to-id", type=int, required=True, dest="to_id")
    chs.add_argument("--text", required=True)
    chs.set_defaults(func=cmd_chat_send)

    # notifications
    nt = sub.add_parser("notifications", help="Уведомления менеджерам в кабинете")
    nt_sub = nt.add_subparsers(dest="sub", required=True)
    ntl = nt_sub.add_parser("list", help="Список уведомлений")
    ntl.add_argument("--page", type=int, default=1)
    ntl.set_defaults(func=cmd_notifications_list)
    ntg = nt_sub.add_parser("get", help="Уведомление по id")
    ntg.add_argument("id", type=int)
    ntg.set_defaults(func=cmd_notifications_get)
    ntc = nt_sub.add_parser("create", help="Создать уведомление менеджеру")
    ntc.add_argument("--manager-id", required=True, dest="manager_id", help="ID или IDs через запятую")
    ntc.add_argument("--text", required=True)
    ntc.add_argument("--type", default=None, choices=["vk", "fb", "ok", "telegram", "whatsapp", "viber", "instagram"])
    ntc.add_argument("--request-id", type=int, default=None, dest="request_id")
    ntc.add_argument("--tourist-id", type=int, default=None, dest="tourist_id")
    ntc.set_defaults(func=cmd_notifications_create)

    # cash
    cs = sub.add_parser("cash", help="Кассы")
    cs_sub = cs.add_subparsers(dest="sub", required=True)
    csl = cs_sub.add_parser("list")
    csl.set_defaults(func=cmd_cash_list)
    csc = cs_sub.add_parser("create", help="Добавить кассу")
    csc.add_argument("--name", required=True)
    csc.set_defaults(func=cmd_cash_create)

    # bills
    bl = sub.add_parser("bills", help="Счета (для отчётности)")
    bl_sub = bl.add_subparsers(dest="sub", required=True)
    bll = bl_sub.add_parser("list")
    bll.add_argument("--page", type=int, default=1)
    bll.set_defaults(func=cmd_bills_list)
    blg = bl_sub.add_parser("get")
    blg.add_argument("id", type=int)
    blg.set_defaults(func=cmd_bills_get)

    # service-price (сезонные цены отеля)
    sp = sub.add_parser("service-price", help="Сезонные цены услуги (по периодам)")
    sp_sub = sp.add_subparsers(dest="sub", required=True)
    spc = sp_sub.add_parser("create", help="Добавить блок цена-период")
    spc.add_argument("--service-id", type=int, required=True, dest="service_id")
    spc.add_argument("--date-begin", required=True, dest="date_begin", help="YYYY-MM-DD HH:MM:SS")
    spc.add_argument("--date-end", required=True, dest="date_end")
    spc.add_argument("--nights", type=int, default=None)
    spc.add_argument("--netto-adult", default=None, dest="netto_adult")
    spc.add_argument("--netto-child", default=None, dest="netto_child")
    spc.add_argument("--netto-baby", default=None, dest="netto_baby")
    spc.add_argument("--price-adult", default=None, dest="price_adult")
    spc.add_argument("--price-child", default=None, dest="price_child")
    spc.add_argument("--price-baby", default=None, dest="price_baby")
    spc.set_defaults(func=cmd_service_price_create)
    spu = sp_sub.add_parser("update", help="Обновить блок цена-период")
    spu.add_argument("id", type=int)
    spu.add_argument("--date-begin", default=None, dest="date_begin")
    spu.add_argument("--date-end", default=None, dest="date_end")
    spu.add_argument("--nights", type=int, default=None)
    spu.add_argument("--netto-adult", default=None, dest="netto_adult")
    spu.add_argument("--netto-child", default=None, dest="netto_child")
    spu.add_argument("--netto-baby", default=None, dest="netto_baby")
    spu.add_argument("--price-adult", default=None, dest="price_adult")
    spu.add_argument("--price-child", default=None, dest="price_child")
    spu.add_argument("--price-baby", default=None, dest="price_baby")
    spu.set_defaults(func=cmd_service_price_update)
    spd = sp_sub.add_parser("delete")
    spd.add_argument("id", type=int)
    spd.add_argument("--confirm", action="store_true")
    spd.set_defaults(func=cmd_service_price_delete)

    # user-cabinet
    uc_ = sub.add_parser("user-cabinet", help="Личный кабинет туриста")
    uc_sub = uc_.add_subparsers(dest="sub", required=True)
    ucc = uc_sub.add_parser("create", help="Создать туристу ЛК на стороне U-On")
    ucc.add_argument("--tourist-id", type=int, required=True, dest="tourist_id")
    ucc.set_defaults(func=cmd_user_cabinet_create)

    # request-file (файлы заявки)
    rf = sub.add_parser("request-files", help="Файлы заявки (прикрепить/удалить по URL)")
    rf_sub = rf.add_subparsers(dest="sub", required=True)
    rfa = rf_sub.add_parser("attach", help="Прикрепить файл к заявке по URL")
    rfa.add_argument("--request-id", type=int, required=True, dest="request_id")
    rfa.add_argument("--name", required=True, help="Отображаемое имя файла")
    rfa.add_argument("--url", required=True, help="URL на файл (S3/наш сервер/любой http)")
    rfa.add_argument("--note", default=None)
    rfa.add_argument("--private", action="store_true",
                     help="Скрыть от туриста в его ЛК")
    rfa.set_defaults(func=cmd_request_file_attach)
    rfd = rf_sub.add_parser("delete", help="Удалить файл")
    rfd.add_argument("id", type=int)
    rfd.add_argument("--confirm", action="store_true")
    rfd.set_defaults(func=cmd_request_file_delete)

    # user-file
    uf = sub.add_parser("user-files", help="Файлы карточки клиента")
    uf_sub = uf.add_subparsers(dest="sub", required=True)
    ufa = uf_sub.add_parser("attach", help="Прикрепить файл к карточке клиента (скан паспорта и т.д.)")
    ufa.add_argument("--tourist-id", type=int, required=True, dest="tourist_id")
    ufa.add_argument("--name", required=True, help="Отображаемое имя")
    ufa.add_argument("--url", required=True, help="URL на файл")
    ufa.add_argument("--note", default=None)
    ufa.set_defaults(func=cmd_user_file_attach)

    # webhook update
    # tourists-requests (привязка туристов к заявке)
    tr = sub.add_parser("tourists-requests", help="Привязка туристов к заявке")
    tr_sub = tr.add_subparsers(dest="sub", required=True)
    tra = tr_sub.add_parser("add", help="Привязать туриста к заявке")
    tra.add_argument("--request-id", type=int, required=True, dest="request_id")
    tra.add_argument("--tourist-id", type=int, required=True, dest="tourist_id")
    tra.set_defaults(func=cmd_tourists_add)
    trr = tr_sub.add_parser("remove", help="Отвязать туриста")
    trr.add_argument("--request-id", type=int, required=True, dest="request_id")
    trr.add_argument("--tourist-id", type=int, required=True, dest="tourist_id")
    trr.add_argument("--confirm", action="store_true")
    trr.set_defaults(func=cmd_tourists_remove)

    # request-action (касания)
    ra = sub.add_parser("actions", help="Касания в заявке или карточке туриста")
    ra_sub = ra.add_subparsers(dest="sub", required=True)
    rac = ra_sub.add_parser("create", help="Создать касание (комментарий, звонок, встречу)")
    rac.add_argument("--request-id", type=int, default=None, dest="request_id", help="ID заявки ИЛИ --tourist-id")
    rac.add_argument("--tourist-id", type=int, default=None, dest="tourist_id", help="ID туриста ИЛИ --request-id")
    rac.add_argument("--type-id", type=int, default=0, dest="type_id", help="0=не определено (комментарий), 1=звонок, 2=письмо, 3=встреча")
    rac.add_argument("--text", required=True)
    rac.add_argument("--datetime", default=None, help="YYYY-MM-DD HH:MM:SS; default — сейчас")
    rac.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    rac.add_argument("--messenger", default=None, help="vk|fb|ok|telegram|instagram|whatsapp|viber")
    rac.add_argument("-F", "--field", action="append")
    rac.set_defaults(func=cmd_actions_create)

    # request-deadline (дедлайны оплаты)
    rd = sub.add_parser("deadlines", help="Дедлайны оплаты в заявке")
    rd_sub = rd.add_subparsers(dest="sub", required=True)
    rdc = rd_sub.add_parser("create", help="Создать дедлайн оплаты")
    rdc.add_argument("--request-id", type=int, required=True, dest="request_id")
    rdc.add_argument("--date", required=True, help="YYYY-MM-DD")
    rdc.add_argument("--type-id", type=int, default=1, dest="type_id", help="1=для туриста (default), 2=для партнёра")
    rdc.add_argument("--amount", default=None, help="Сумма (поле summ); либо --amount, либо --percent")
    rdc.add_argument("--percent", default=None, help="Процент от стоимости заявки")
    rdc.add_argument("--current", action="store_true", help="Сделать текущим дедлайном (is_current=1)")
    rdc.add_argument("-F", "--field", action="append")
    rdc.set_defaults(func=cmd_deadlines_create)
    rdd = rd_sub.add_parser("delete", help="Удалить дедлайн")
    rdd.add_argument("id", type=int)
    rdd.add_argument("--confirm", action="store_true")
    rdd.set_defaults(func=cmd_deadlines_delete)

    # managers
    mng = sub.add_parser("managers", help="Сотрудники")
    mng_sub = mng.add_subparsers(dest="sub", required=True)
    ml = mng_sub.add_parser("list", help="Все сотрудники (опц. по офису)")
    ml.add_argument("--office-id", type=int, default=None, dest="office_id")
    ml.set_defaults(func=cmd_managers_list)
    mc = mng_sub.add_parser("create", help="Добавить сотрудника в кабинет")
    mc.add_argument("--name", required=True)
    mc.add_argument("--surname", default=None)
    mc.add_argument("--patronymic", default=None)
    mc.add_argument("--email", required=True)
    mc.add_argument("--password", required=True, help="Минимум 10 символов")
    mc.add_argument("--company-id", type=int, required=True, dest="company_id")
    mc.add_argument("--office-id", type=int, default=None, dest="office_id")
    mc.add_argument("--phone", default=None)
    mc.add_argument("--birthday", default=None, help="YYYY-MM-DD")
    mc.add_argument("--note", default=None)
    mc.add_argument("-F", "--field", action="append")
    mc.set_defaults(func=cmd_manager_create)

    # statuses
    st = sub.add_parser("statuses", help="Справочники статусов")
    st.add_argument("kind", choices=["requests", "leads", "pay", "cb"])
    st.set_defaults(func=cmd_statuses)

    # sources
    src = sub.add_parser("sources", help="Источники обращений")
    src_sub = src.add_subparsers(dest="sub", required=True)
    srl = src_sub.add_parser("list")
    srl.set_defaults(func=cmd_sources_list)
    src_c = src_sub.add_parser("create", help="Добавить источник")
    src_c.add_argument("--name", required=True)
    src_c.set_defaults(func=cmd_sources_create)

    # travel-types
    tt = sub.add_parser("travel-types", help="Типы поездок")
    tt_sub = tt.add_subparsers(dest="sub", required=True)
    ttl = tt_sub.add_parser("list")
    ttl.set_defaults(func=cmd_travel_types_list)
    ttc = tt_sub.add_parser("create")
    ttc.add_argument("--name", required=True)
    ttc.set_defaults(func=cmd_travel_types_create)

    # nutrition
    nt2 = sub.add_parser("nutrition", help="Типы питания")
    nt2_sub = nt2.add_subparsers(dest="sub", required=True)
    nt2l = nt2_sub.add_parser("list")
    nt2l.set_defaults(func=cmd_nutrition_list)
    nt2c = nt2_sub.add_parser("create")
    nt2c.add_argument("--name", required=True)
    nt2c.set_defaults(func=cmd_nutrition_create)
    nt2u = nt2_sub.add_parser("update")
    nt2u.add_argument("id", type=int)
    nt2u.add_argument("--name", required=True)
    nt2u.set_defaults(func=cmd_nutrition_update)

    # countries
    co = sub.add_parser("countries", help="Страны")
    co_sub = co.add_subparsers(dest="sub", required=True)
    col = co_sub.add_parser("list")
    col.set_defaults(func=cmd_countries_list)
    coc = co_sub.add_parser("create")
    coc.add_argument("--name", required=True)
    coc.set_defaults(func=cmd_countries_create)
    cou = co_sub.add_parser("update")
    cou.add_argument("id", type=int)
    cou.add_argument("--name", required=True)
    cou.set_defaults(func=cmd_countries_update)

    # cities
    ci = sub.add_parser("cities", help="Города (по стране)")
    ci_sub = ci.add_subparsers(dest="sub", required=True)
    cil = ci_sub.add_parser("list")
    cil.add_argument("country_id", type=int, help="ID страны (см. countries list)")
    cil.add_argument("--page", type=int, default=1)
    cil.set_defaults(func=cmd_cities_list)
    cic = ci_sub.add_parser("create")
    cic.add_argument("--name", required=True)
    cic.add_argument("--country-id", type=int, required=True, dest="country_id")
    cic.set_defaults(func=cmd_cities_create)
    ciu = ci_sub.add_parser("update")
    ciu.add_argument("id", type=int)
    ciu.add_argument("--name", required=True)
    ciu.set_defaults(func=cmd_cities_update)

    # webhooks
    wh = sub.add_parser("webhooks", help="Управление вебхуками")
    wh_sub = wh.add_subparsers(dest="sub", required=True)
    whl = wh_sub.add_parser("list", help="Список вебхуков")
    whl.add_argument("--page", type=int, default=1)
    whl.set_defaults(func=cmd_webhooks_list)
    whc = wh_sub.add_parser("create", help="Зарегистрировать вебхук")
    whc.add_argument("--type", type=int, required=True, dest="type", help="ID типа (1..74)")
    whc.add_argument("--url", required=True, help="URL приёмника")
    whc.add_argument("--note", default=None)
    whc.set_defaults(func=cmd_webhooks_create)
    whd = wh_sub.add_parser("delete", help="Удалить вебхук")
    whd.add_argument("id", type=int)
    whd.set_defaults(func=cmd_webhooks_delete)
    whu = wh_sub.add_parser("update", help="Обновить вебхук (URL/метод/тип/заметка)")
    whu.add_argument("id", type=int)
    whu.add_argument("--type", type=int, default=None)
    whu.add_argument("--url", default=None)
    whu.add_argument("--method", default=None, choices=["GET", "POST", "PUT", "DELETE"])
    whu.add_argument("--note", default=None)
    whu.set_defaults(func=cmd_webhook_update)

    # reminders
    rem = sub.add_parser("reminders", help="Напоминания")
    rem_sub = rem.add_subparsers(dest="sub", required=True)
    rc = rem_sub.add_parser("create", help="Создать напоминание")
    rc.add_argument("--request-id", type=int, default=None, dest="request_id")
    rc.add_argument("--tourist-id", type=int, default=None, dest="tourist_id")
    rc.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    rc.add_argument("--text", required=True)
    rc.add_argument("--type-id", type=int, default=1, dest="type_id",
                    help="0=не определено, 1=звонок (default), 2=письмо, 3=встреча")
    rc.add_argument("--from", required=True, dest="date_from", help="YYYY-MM-DD HH:MM:SS")
    rc.add_argument("--to", required=True, dest="date_to", help="YYYY-MM-DD HH:MM:SS")
    rc.add_argument("-F", "--field", action="append")
    rc.set_defaults(func=cmd_reminders_create)
    rls = rem_sub.add_parser("list", help="Список напоминаний (постранично)")
    rls.add_argument("--page", type=int, default=1)
    rls.set_defaults(func=cmd_reminders_list)
    rg = rem_sub.add_parser("get", help="Получить одно напоминание по id")
    rg.add_argument("id", type=int)
    rg.set_defaults(func=cmd_reminders_get)
    rbr = rem_sub.add_parser("by-request", help="Напоминания по заявке")
    rbr.add_argument("request_id", type=int)
    rbr.set_defaults(func=cmd_reminders_by_request)
    rcl = rem_sub.add_parser("close", help="Завершить напоминание")
    rcl.add_argument("id", type=int)
    rcl.add_argument("--done-by", type=int, default=None, dest="done_by", help="ID менеджера, кто закрыл")
    rcl.add_argument("--done-at", default=None, dest="done_at", help="YYYY-MM-DD HH:MM:SS; default — сейчас")
    rcl.set_defaults(func=cmd_reminders_close)

    # extended_fields (доп. поля карточек)
    ef = sub.add_parser("fields", help="Дополнительные поля карточек (extended_fields)")
    ef_sub = ef.add_subparsers(dest="sub", required=True)
    efl = ef_sub.add_parser("list", help="Список доп.полей (опц. по разделу)")
    efl.add_argument("--section", type=int, default=None, help="1=заявка, 2=обращение, 3=турист, 4=услуга, 5=платёж клиент, 6=платёж партнёр, 7=косв. платёж, 8=партнёр")
    efl.add_argument("--page", type=int, default=1)
    efl.set_defaults(func=cmd_fields_list)
    efc = ef_sub.add_parser("create", help="Добавить доп.поле")
    efc.add_argument("--section", type=int, required=True, help="1=заявка, 2=обращение, 3=турист, 4=услуга, 5..8=платежи и партнёры")
    efc.add_argument("--name", required=True, help="Название поля")
    efc.add_argument("--type", type=int, default=1, help="1=текст (default), 2=список значений, 3=многострочное, 4=дата, 5=текст+ссылка")
    efc.add_argument("--options", default=None, help="Значения списка через запятую (для type=2)")
    efc.set_defaults(func=cmd_fields_create)
    efu = ef_sub.add_parser("update", help="Обновить доп.поле")
    efu.add_argument("id", type=int)
    efu.add_argument("--section", type=int, default=None)
    efu.add_argument("--name", default=None)
    efu.add_argument("--type", type=int, default=None)
    efu.add_argument("--options", default=None)
    efu.set_defaults(func=cmd_fields_update)
    efd = ef_sub.add_parser("delete", help="Удалить доп.поле")
    efd.add_argument("id", type=int)
    efd.add_argument("--confirm", action="store_true")
    efd.set_defaults(func=cmd_fields_delete)

    # calls (call_history)
    cl = sub.add_parser("calls", help="История звонков (телефония)")
    cl_sub = cl.add_subparsers(dest="sub", required=True)
    clog = cl_sub.add_parser("log", help="Залогировать звонок")
    clog.add_argument("--phone", required=True)
    clog.add_argument("--inbound", action="store_true", help="Входящий (default — исходящий)")
    clog.add_argument("--duration", type=int, default=None, help="Длительность в секундах")
    clog.add_argument("--start", default=None, help="YYYY-MM-DD HH:MM:SS; default — сейчас")
    clog.add_argument("--record", default=None, help="URL записи разговора")
    clog.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    clog.add_argument("--office-id", type=int, default=None, dest="office_id")
    clog.add_argument("--note", default=None)
    clog.add_argument("-F", "--field", action="append")
    clog.set_defaults(func=cmd_calls_log)
    cll = cl_sub.add_parser("list", help="Список звонков")
    cll.add_argument("--page", type=int, default=1)
    cll.set_defaults(func=cmd_calls_list)
    clr = cl_sub.add_parser("by-request", help="Звонки по заявке")
    clr.add_argument("request_id", type=int)
    clr.add_argument("--page", type=int, default=1)
    clr.set_defaults(func=cmd_calls_by_request)
    clu = cl_sub.add_parser("by-user", help="Звонки по клиенту")
    clu.add_argument("tourist_id", type=int)
    clu.add_argument("--page", type=int, default=1)
    clu.set_defaults(func=cmd_calls_by_user)

    # hotels CRUD
    hot = sub.add_parser("hotels", help="Каталог отелей")
    hot_sub = hot.add_subparsers(dest="sub", required=True)
    hl = hot_sub.add_parser("list", help="Список отелей")
    hl.add_argument("--page", type=int, default=1)
    hl.set_defaults(func=cmd_hotels_list)
    hg = hot_sub.add_parser("get", help="Получить отель по id")
    hg.add_argument("id", type=int)
    hg.set_defaults(func=cmd_hotels_get)
    hc = hot_sub.add_parser("create", help="Добавить отель")
    hc.add_argument("--name", required=True)
    hc.add_argument("--city-id", type=int, default=None, dest="city_id")
    hc.add_argument("--country-id", type=int, default=None, dest="country_id")
    hc.add_argument("--stars", type=int, default=None)
    hc.add_argument("--address", default=None)
    hc.add_argument("--phone", default=None)
    hc.add_argument("--website", default=None)
    hc.add_argument("--email", default=None)
    hc.add_argument("--note", default=None)
    hc.add_argument("-F", "--field", action="append")
    hc.set_defaults(func=cmd_hotels_create)
    hu = hot_sub.add_parser("update", help="Обновить отель")
    hu.add_argument("id", type=int)
    hu.add_argument("--name", default=None)
    hu.add_argument("--stars", type=int, default=None)
    hu.add_argument("--address", default=None)
    hu.add_argument("--phone", default=None)
    hu.add_argument("--website", default=None)
    hu.add_argument("--email", default=None)
    hu.add_argument("--note", default=None)
    hu.add_argument("-F", "--field", action="append")
    hu.set_defaults(func=cmd_hotels_update)
    hd = hot_sub.add_parser("delete", help="Удалить отель")
    hd.add_argument("id", type=int)
    hd.add_argument("--confirm", action="store_true")
    hd.set_defaults(func=cmd_hotels_delete)

    # suppliers CRUD
    sup = sub.add_parser("suppliers", help="Поставщики / туроператоры / партнёры")
    sup_sub = sup.add_subparsers(dest="sub", required=True)
    sl = sup_sub.add_parser("list", help="Список поставщиков")
    sl.add_argument("--page", type=int, default=1)
    sl.set_defaults(func=cmd_suppliers_list)
    sg = sup_sub.add_parser("get", help="Получить поставщика по id")
    sg.add_argument("id", type=int)
    sg.set_defaults(func=cmd_suppliers_get)
    sc = sup_sub.add_parser("create", help="Добавить поставщика")
    sc.add_argument("--name", required=True)
    sc.add_argument("--name-official", default=None, dest="name_official")
    sc.add_argument("--type-id", type=int, default=None, dest="type_id", help="ID типа партнёра (см. suppliers types)")
    sc.add_argument("--inn", default=None)
    sc.add_argument("--kpp", default=None)
    sc.add_argument("--phone", default=None)
    sc.add_argument("--email", default=None)
    sc.add_argument("--website", default=None)
    sc.add_argument("--note", default=None)
    sc.add_argument("-F", "--field", action="append")
    sc.set_defaults(func=cmd_suppliers_create)
    su_ = sup_sub.add_parser("update", help="Обновить поставщика")
    su_.add_argument("id", type=int)
    su_.add_argument("--name", default=None)
    su_.add_argument("--phone", default=None)
    su_.add_argument("--email", default=None)
    su_.add_argument("--website", default=None)
    su_.add_argument("--note", default=None)
    su_.add_argument("-F", "--field", action="append")
    su_.set_defaults(func=cmd_suppliers_update)
    st_ = sup_sub.add_parser("types", help="Типы партнёров")
    st_.set_defaults(func=cmd_supplier_types)
    stc = sup_sub.add_parser("type-create", help="Добавить тип партнёра")
    stc.add_argument("--name", required=True)
    stc.set_defaults(func=cmd_supplier_type_create)

    # documents
    doc = sub.add_parser("documents", help="Генерация документов по шаблону U-On")
    doc_sub = doc.add_subparsers(dest="sub", required=True)
    dg = doc_sub.add_parser("generate", help="Сгенерировать документ из заявки")
    dg.add_argument("--template-id", type=int, required=True, dest="template_id",
                    help="5=Договор, 42=Договор 2, 13=Лист бронирования, 14=Расчёт тура, 15=Счёт из заявки")
    dg.add_argument("--request-id", type=int, required=True, dest="request_id")
    dg.add_argument("--bill-id", type=int, default=None, dest="bill_id")
    dg.add_argument("--supplier-id", type=int, default=None, dest="supplier_id")
    dg.add_argument("--tourist-id", type=int, default=None, dest="tourist_id")
    dg.add_argument("--with-sign", action="store_true", dest="with_sign",
                    help="Отображать печать и подпись")
    dg.add_argument("--date", default=None, help="Дата в документе YYYY-MM-DD")
    dg.add_argument("--format", default="pdf", choices=["text", "doc", "pdf"])
    dg.add_argument("--locale", default="ru", choices=["ru", "en", "uk", "az", "de", "fr", "hy", "it"])
    dg.add_argument("--custom", action="store_true", help="Вручную созданный (не системный) шаблон")
    dg.add_argument("-F", "--field", action="append")
    dg.set_defaults(func=cmd_document_generate)

    # raw escape hatch
    raw = sub.add_parser("raw", help="Сырой вызов API (для неизвестных endpoint-ов)")
    raw_sub = raw.add_subparsers(dest="sub", required=True)
    rg = raw_sub.add_parser("get", help="GET /<endpoint>.json")
    rg.add_argument("endpoint", help="например manager или leads/2026-05-01/2026-05-29/1")
    rg.set_defaults(func=cmd_raw_get)
    rp = raw_sub.add_parser("post", help="POST /<endpoint>.json")
    rp.add_argument("endpoint")
    rp.add_argument("--field", "-F", action="append", help="ключ=значение (повторяемо)")
    rp.set_defaults(func=cmd_raw_post)

    return p


def _add_period(p: argparse.ArgumentParser) -> argparse.ArgumentParser:
    p.add_argument("--from", required=True, dest="date_from", help="YYYY-MM-DD")
    p.add_argument("--to", required=True, dest="date_to", help="YYYY-MM-DD")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--source-id", type=int, default=None, dest="source_id")
    return p


def main() -> None:
    args = build_parser().parse_args()
    uon = UonClient()
    args.func(args, uon)


if __name__ == "__main__":
    main()
