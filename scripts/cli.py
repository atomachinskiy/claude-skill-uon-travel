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
    dump(uon.post("user/create", {k: v for k, v in data.items() if v is not None}))


def cmd_payments_list(args, uon: UonClient) -> None:
    ep = f"payment/list/{args.date_from}/{args.date_to}/{args.page}"
    dump(uon.get(ep))


def cmd_payments_get(args, uon: UonClient) -> None:
    dump(uon.get(f"payment/{args.id}"))


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
    uc.set_defaults(func=cmd_users_create)

    # payments
    pays = sub.add_parser("payments", help="Платежи")
    pays_sub = pays.add_subparsers(dest="sub", required=True)
    _add_period(pays_sub.add_parser("list", help="Список платежей за период")).set_defaults(
        func=cmd_payments_list
    )
    pg = pays_sub.add_parser("get", help="Платёж по id")
    pg.add_argument("id", type=int)
    pg.set_defaults(func=cmd_payments_get)

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
