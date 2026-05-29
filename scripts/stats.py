#!/usr/bin/env python3
"""stats — BI / аналитика воронки U-On.

Подкоманды:
    funnel      — lead → request → won по периоду (опц. по источнику)
    revenue     — выручка по менеджерам / офисам за период
    avg-check   — средний чек, медиана, распределение
    cycle       — среднее время от lead до won (дни)
    churn       — топ причин отказа
    overdue     — список заявок с просроченной оплатой
    html-report — собрать единый HTML-отчёт в стиле offer.html

Примеры:
    stats.py funnel --from 2026-01-01 --to 2026-05-31
    stats.py revenue --from 2026-01-01 --to 2026-05-31 --group manager
    stats.py html-report --from 2026-01-01 --to 2026-05-31 -o report.html
"""
from __future__ import annotations

import argparse
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import UonClient  # noqa: E402


def _fetch_paginated(uon: UonClient, ep_template: str, key: str = "requests") -> list[dict]:
    """Постранично выгрузить все записи. ep_template должен содержать {page}."""
    items = []
    page = 1
    while True:
        ep = ep_template.format(page=page)
        resp = uon.get(ep)
        chunk = resp.get(key, []) or resp.get("records", []) or resp.get("leads", []) or []
        if not chunk:
            break
        items.extend(chunk)
        pages = resp.get("pages_all")
        if pages and page >= int(pages or 1):
            break
        page += 1
        if page > 100:  # safety
            break
    return items


def _load_status_maps(uon: UonClient) -> dict[str, dict[int, dict]]:
    return {
        "request": {int(r["id"]): r for r in uon.get("status").get("records", [])},
        "lead": {int(r["id"]): r for r in uon.get("status_lead").get("records", [])},
        "pay": {int(r["id"]): r for r in uon.get("status_pay").get("records", [])},
    }


def _safe_float(v: Any) -> float:
    try:
        return float(v) if v not in (None, "", "null") else 0.0
    except (ValueError, TypeError):
        return 0.0


def cmd_funnel(args) -> None:
    uon = UonClient()
    statuses = _load_status_maps(uon)
    leads = _fetch_paginated(uon, f"leads/{args.date_from}/{args.date_to}/{{page}}", "leads")
    requests = _fetch_paginated(uon, f"requests/{args.date_from}/{args.date_to}/{{page}}", "requests")

    won = sum(1 for r in requests if statuses["request"].get(int(r.get("status_id", 0) or 0), {}).get("is_confirmed") == 1)
    lost = sum(1 for r in requests if statuses["request"].get(int(r.get("status_id", 0) or 0), {}).get("is_cancel") == 1)
    active = len(requests) - won - lost

    total_leads = len(leads)
    total_reqs = len(requests)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Воронка {args.date_from} → {args.date_to}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Обращения (lead):  {total_leads}")
    print(f"  Заявки (request):  {total_reqs}")
    print(f"    в работе:        {active}")
    print(f"    подтверждено:    {won}")
    print(f"    отказ:           {lost}")
    if total_leads > 0:
        print(f"  Конверсия lead→request:    {total_reqs/total_leads*100:.1f}%")
    if total_reqs > 0:
        print(f"  Конверсия request→won:     {won/total_reqs*100:.1f}%")
    if total_leads > 0:
        print(f"  Сквозная конверсия:        {won/total_leads*100:.1f}%")

    if args.by_source:
        by_src = Counter(r.get("source_name", "не указан") or "не указан" for r in requests)
        print("\n  Заявки по источникам:")
        for src, n in by_src.most_common(10):
            print(f"    {src:30s} {n}")


def cmd_revenue(args) -> None:
    uon = UonClient()
    requests = _fetch_paginated(uon, f"requests/{args.date_from}/{args.date_to}/{{page}}", "requests")

    def amount(r: dict) -> float:
        # Цена клиенту по заявке = сумма услуг
        srv = r.get("services") or []
        return sum(_safe_float(s.get("price")) for s in srv)

    group_field = {"manager": ("manager_name", "manager_id"), "office": ("office_name", "office_id"), "source": ("source_name",)}[args.group]
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for r in requests:
        key = r.get(group_field[0]) or "не указан"
        sums[str(key)] += amount(r)
        counts[str(key)] += 1

    total = sum(sums.values())
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Выручка по {args.group} за {args.date_from} → {args.date_to}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Всего: {total:,.0f} ₽ ({len(requests)} заявок)")
    print()
    for k, v in sorted(sums.items(), key=lambda x: x[1], reverse=True):
        n = counts[k]
        avg = v / n if n else 0
        print(f"  {k:30s} {v:>12,.0f} ₽   ({n} зв, avg {avg:,.0f})")


def cmd_avg_check(args) -> None:
    uon = UonClient()
    requests = _fetch_paginated(uon, f"requests/{args.date_from}/{args.date_to}/{{page}}", "requests")
    checks = []
    for r in requests:
        srv = r.get("services") or []
        s = sum(_safe_float(svc.get("price")) for svc in srv)
        if s > 0:
            checks.append(s)
    if not checks:
        print("Нет данных по заявкам с услугами")
        return
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Чек по заявкам {args.date_from} → {args.date_to}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Заявок с услугами: {len(checks)}")
    print(f"  Сумма:             {sum(checks):,.0f} ₽")
    print(f"  Средний чек:       {statistics.mean(checks):,.0f} ₽")
    print(f"  Медиана:           {statistics.median(checks):,.0f} ₽")
    print(f"  Min/Max:           {min(checks):,.0f} / {max(checks):,.0f} ₽")


def cmd_cycle(args) -> None:
    uon = UonClient()
    requests = _fetch_paginated(uon, f"requests/closed/{args.date_from}/{args.date_to}/{{page}}", "requests")
    days = []
    for r in requests:
        dl = r.get("dat_lead") or r.get("date_lead")
        dc = r.get("dat_close") or r.get("date_close")
        if not (dl and dc):
            continue
        try:
            d1 = datetime.strptime(str(dl)[:16], "%Y-%m-%d %H:%M")
            d2 = datetime.strptime(str(dc)[:16], "%Y-%m-%d %H:%M")
            days.append((d2 - d1).total_seconds() / 86400)
        except ValueError:
            continue
    if not days:
        print("Нет закрытых заявок с датами в этом периоде")
        return
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Время сделки {args.date_from} → {args.date_to}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Закрытых заявок:   {len(days)}")
    print(f"  Среднее:           {statistics.mean(days):.1f} дн")
    print(f"  Медиана:           {statistics.median(days):.1f} дн")
    print(f"  Min/Max:           {min(days):.1f} / {max(days):.1f} дн")


def cmd_churn(args) -> None:
    uon = UonClient()
    leads = _fetch_paginated(uon, f"leads/{args.date_from}/{args.date_to}/{{page}}", "leads")
    reasons = Counter()
    for lead in leads:
        rd = lead.get("reason_deny_name") or lead.get("reason_deny")
        if rd:
            reasons[str(rd)] += 1
    if not reasons:
        print("Нет причин отказа в обращениях за период")
        return
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Топ причин отказа {args.date_from} → {args.date_to}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for r, n in reasons.most_common(15):
        print(f"  {n:4d}  {r}")


def cmd_overdue(args) -> None:
    uon = UonClient()
    today = datetime.now().date().isoformat()
    requests = _fetch_paginated(uon, f"requests/{args.date_from}/{today}/{{page}}", "requests")
    overdue = []
    for r in requests:
        # Заявка просрочена если она ещё не оплачена полностью и r_dat_end < сегодня
        end = r.get("date_end") or r.get("dat_end")
        pay_status = int(r.get("status_pay_id", 0) or 0)
        if not end or pay_status == 3:
            continue
        try:
            d = datetime.strptime(str(end)[:10], "%Y-%m-%d").date()
        except ValueError:
            continue
        if d < datetime.now().date():
            overdue.append({"id": r["id"], "client": f"{r.get('client_name','')} {r.get('client_surname','')}".strip(),
                            "end": str(end)[:10], "pay_status": pay_status})
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Просроченные заявки на {today}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Всего: {len(overdue)}")
    for o in overdue[:30]:
        print(f"  #{o['id']:6} {o['client']:30s}  end={o['end']}  pay_status={o['pay_status']}")


def cmd_html_report(args) -> None:
    """Собрать единый HTML отчёт по всем метрикам."""
    uon = UonClient()
    statuses = _load_status_maps(uon)
    leads = _fetch_paginated(uon, f"leads/{args.date_from}/{args.date_to}/{{page}}", "leads")
    requests = _fetch_paginated(uon, f"requests/{args.date_from}/{args.date_to}/{{page}}", "requests")

    def amount(r):
        return sum(_safe_float(s.get("price")) for s in (r.get("services") or []))

    revenue = sum(amount(r) for r in requests)
    won = sum(1 for r in requests if statuses["request"].get(int(r.get("status_id", 0) or 0), {}).get("is_confirmed") == 1)
    lost = sum(1 for r in requests if statuses["request"].get(int(r.get("status_id", 0) or 0), {}).get("is_cancel") == 1)
    checks = [amount(r) for r in requests if amount(r) > 0]
    avg = statistics.mean(checks) if checks else 0
    conv = won / len(requests) * 100 if requests else 0

    by_mgr: dict[str, list] = defaultdict(list)
    for r in requests:
        by_mgr[r.get("manager_name") or "не указан"].append(amount(r))

    by_src = Counter(r.get("source_name", "не указан") or "не указан" for r in requests)

    html = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<title>U-On отчёт {args.date_from} — {args.date_to}</title>
<style>
:root {{ --paper:#f5f3ee; --ink:#0f0f0f; --purple:#6728e8; --orange:#ff7a21; --green:#baff2f; --line:#0f0f0f1a; }}
body {{ margin:0; background:var(--paper); color:var(--ink); font:14px/1.5 'Inter',system-ui,sans-serif; letter-spacing:-.01em; }}
.wrap {{ max-width:980px; margin:40px auto; padding:0 24px; }}
h1 {{ font-size:42px; margin:0 0 8px; letter-spacing:-.02em; }}
.sub {{ color:#666; margin-bottom:32px; }}
.grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }}
.card {{ background:#fff; border:1px solid var(--line); padding:20px; border-radius:12px; }}
.card .l {{ font-size:12px; color:#666; text-transform:uppercase; letter-spacing:.04em; margin-bottom:6px; }}
.card .v {{ font-size:28px; font-weight:700; letter-spacing:-.02em; }}
h2 {{ font-size:22px; margin:36px 0 14px; }}
table {{ width:100%; border-collapse:collapse; background:#fff; border-radius:12px; overflow:hidden; }}
th, td {{ padding:10px 16px; text-align:left; border-bottom:1px solid var(--line); }}
th {{ background:#0f0f0f08; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:.04em; }}
.bar {{ display:inline-block; background:var(--purple); height:8px; vertical-align:middle; border-radius:4px; }}
</style>
</head><body>
<div class="wrap">
<h1>U-On отчёт</h1>
<div class="sub">Период {args.date_from} → {args.date_to}</div>

<div class="grid">
  <div class="card"><div class="l">Обращений</div><div class="v">{len(leads)}</div></div>
  <div class="card"><div class="l">Заявок</div><div class="v">{len(requests)}</div></div>
  <div class="card"><div class="l">Подтверждено</div><div class="v">{won}</div></div>
  <div class="card"><div class="l">Выручка</div><div class="v">{revenue:,.0f} ₽</div></div>
  <div class="card"><div class="l">Средний чек</div><div class="v">{avg:,.0f} ₽</div></div>
  <div class="card"><div class="l">Конверсия</div><div class="v">{conv:.1f}%</div></div>
  <div class="card"><div class="l">Отказов</div><div class="v">{lost}</div></div>
  <div class="card"><div class="l">В работе</div><div class="v">{len(requests)-won-lost}</div></div>
</div>

<h2>Менеджеры</h2>
<table><thead><tr><th>Менеджер</th><th>Заявок</th><th>Выручка</th><th>Средний чек</th></tr></thead><tbody>
{"".join(f'<tr><td>{m}</td><td>{len(a)}</td><td>{sum(a):,.0f} ₽</td><td>{statistics.mean(a) if a else 0:,.0f} ₽</td></tr>' for m,a in sorted(by_mgr.items(), key=lambda x:-sum(x[1])))}
</tbody></table>

<h2>Источники</h2>
<table><thead><tr><th>Источник</th><th>Заявок</th><th>Доля</th></tr></thead><tbody>
{"".join(f'<tr><td>{s}</td><td>{n}</td><td><span class="bar" style="width:{n/max(by_src.values())*200}px"></span> {n/sum(by_src.values())*100:.1f}%</td></tr>' for s,n in by_src.most_common())}
</tbody></table>

</div></body></html>
"""
    out = Path(args.output)
    out.write_text(html, encoding="utf-8")
    print(f"Сохранено: {out.absolute()} ({len(html)} bytes)")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="stats", description="U-On BI / analytics")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, func, extra in [
        ("funnel", cmd_funnel, lambda x: x.add_argument("--by-source", action="store_true")),
        ("revenue", cmd_revenue, lambda x: x.add_argument("--group", choices=["manager", "office", "source"], default="manager")),
        ("avg-check", cmd_avg_check, lambda x: None),
        ("cycle", cmd_cycle, lambda x: None),
        ("churn", cmd_churn, lambda x: None),
        ("overdue", cmd_overdue, lambda x: None),
        ("html-report", cmd_html_report, lambda x: x.add_argument("-o", "--output", default="report.html")),
    ]:
        sp = sub.add_parser(name)
        sp.add_argument("--from", required=True, dest="date_from")
        sp.add_argument("--to", required=True, dest="date_to")
        extra(sp)
        sp.set_defaults(func=func)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
