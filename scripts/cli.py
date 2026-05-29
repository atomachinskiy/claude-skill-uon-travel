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
        "u_name": args.name,
        "u_surname": args.surname,
        "u_phone_mobile": args.phone,
        "u_email": args.email,
        "source_id": args.source_id,
        "status_id": args.status_id,
        "manager_id": args.manager_id,
        "text": args.text,
    }
    dump(uon.post("lead/create", {k: v for k, v in data.items() if v is not None}))


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


def cmd_users_create(args, uon: UonClient) -> None:
    data = {
        "u_name": args.name,
        "u_surname": args.surname,
        "u_phone_mobile": args.phone,
        "u_email": args.email,
        "manager_id": args.manager_id,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    dump(uon.post("user/create", {k: v for k, v in data.items() if v is not None}))


def cmd_users_update(args, uon: UonClient) -> None:
    data = {
        "u_name": args.name,
        "u_surname": args.surname,
        "u_phone_mobile": args.phone,
        "u_email": args.email,
        "manager_id": args.manager_id,
    }
    for kv in args.field or []:
        k, _, v = kv.partition("=")
        data[k.strip()] = v.strip()
    payload = {k: v for k, v in data.items() if v is not None}
    if not payload:
        sys.exit("Нечего обновлять — задайте хотя бы одно поле")
    dump(uon.post(f"user/update/{args.id}", payload))


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


def cmd_webhooks_list(args, uon: UonClient) -> None:
    dump(uon.get(f"webhook/{args.page}"))


def cmd_webhooks_create(args, uon: UonClient) -> None:
    dump(uon.post("webhook/create", {"type_id": args.type, "url": args.url, "note": args.note or ""}))


def cmd_webhooks_delete(args, uon: UonClient) -> None:
    dump(uon.post(f"webhook/delete/{args.id}", {}))


def cmd_reminders_create(args, uon: UonClient) -> None:
    data = {
        "r_id": args.request_id,
        "u_id": args.tourist_id,
        "manager_id": args.manager_id,
        "text": args.text,
        "date_from": args.date_from,
        "date_to": args.date_to,
    }
    dump(uon.post("reminder/create", {k: v for k, v in data.items() if v is not None}))


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
    cr = leads_sub.add_parser("create", help="Создать обращение")
    cr.add_argument("--name", required=True)
    cr.add_argument("--surname", default=None)
    cr.add_argument("--phone", required=True)
    cr.add_argument("--email", default=None)
    cr.add_argument("--source-id", type=int, default=None, dest="source_id")
    cr.add_argument("--status-id", type=int, default=None, dest="status_id")
    cr.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    cr.add_argument("--text", default=None, help="Текст обращения")
    cr.set_defaults(func=cmd_leads_create)

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
    uc = users_sub.add_parser("create", help="Создать туриста")
    uc.add_argument("--name", required=True)
    uc.add_argument("--surname", default=None)
    uc.add_argument("--phone", required=True)
    uc.add_argument("--email", default=None)
    uc.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    uc.add_argument("-F", "--field", action="append", help="доп. поле key=value")
    uc.set_defaults(func=cmd_users_create)

    uu = users_sub.add_parser("update", help="Обновить туриста")
    uu.add_argument("id", type=int)
    uu.add_argument("--name", default=None)
    uu.add_argument("--surname", default=None)
    uu.add_argument("--phone", default=None)
    uu.add_argument("--email", default=None)
    uu.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    uu.add_argument("-F", "--field", action="append")
    uu.set_defaults(func=cmd_users_update)

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

    # statuses
    st = sub.add_parser("statuses", help="Справочники статусов")
    st.add_argument("kind", choices=["requests", "leads", "pay", "cb"])
    st.set_defaults(func=cmd_statuses)

    # sources
    src = sub.add_parser("sources", help="Источники обращений")
    src.add_argument("--list", action="store_true")
    src.set_defaults(func=cmd_sources_list)

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

    # reminders
    rem = sub.add_parser("reminders", help="Напоминания")
    rem_sub = rem.add_subparsers(dest="sub", required=True)
    rc = rem_sub.add_parser("create", help="Создать напоминание")
    rc.add_argument("--request-id", type=int, default=None, dest="request_id")
    rc.add_argument("--tourist-id", type=int, default=None, dest="tourist_id")
    rc.add_argument("--manager-id", type=int, default=None, dest="manager_id")
    rc.add_argument("--text", required=True)
    rc.add_argument("--from", default=None, dest="date_from", help="YYYY-MM-DD HH:MM:SS")
    rc.add_argument("--to", default=None, dest="date_to")
    rc.set_defaults(func=cmd_reminders_create)

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
