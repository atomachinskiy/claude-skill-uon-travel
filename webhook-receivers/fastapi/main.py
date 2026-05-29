"""U-On.Travel webhook receiver (FastAPI).

Принимает POST/GET, парсит payload, сохраняет в SQLite,
опционально форвардит в Telegram или другой webhook.
"""
from __future__ import annotations

import json
import os
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import httpx
from fastapi import FastAPI, Request

DB_PATH = Path(os.environ.get("DB_PATH", "/app/data/uon-events.db"))
TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
TG_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
FORWARD_URL = os.environ.get("FORWARD_WEBHOOK_URL", "").strip()
KEEP_DAYS = int(os.environ.get("KEEP_DAYS", "30"))

EVENT_NAMES: dict[int, str] = {
    1: "Создание обращения",
    2: "Создание заявки",
    3: "Создание клиента",
    4: "Изменение клиента",
    5: "Удаление клиента",
    6: "Создание партнёра",
    7: "Изменение партнёра",
    8: "Удаление партнёра",
    9: "Создание платежа",
    10: "Изменение платежа",
    11: "Удаление платежа",
    12: "Создание услуги в заявке",
    13: "Изменение услуги в заявке",
    14: "Удаление услуги из заявки",
    15: "Отправка сообщения в чате",
    16: "Изменение статуса в обращении",
    17: "Изменение статуса в заявке",
    18: "Изменение цены нетто в заявке",
    19: "Изменение цены клиента в заявке",
    20: "Прикрепление файла в заявке",
    21: "Удаление файла из заявки",
    22: "Добавление туриста в заявке",
    23: "Удаление туриста из заявки",
    24: "Начисление баллов клиенту",
    27: "Изменение причины отказа в обращении",
    28: "Прикрепление бонусной карты к туристу",
    29: "Изменение менеджера в обращении",
    30: "Изменение менеджера в заявке",
    31: "Добавление комментария",
    32: "Уведомление туриста о событиях",
    33: "Создание менеджера",
    34: "Добавление задачи",
    35: "Добавление номера брони в заявке",
    36: "Изменение номера брони в заявке",
    37: "Получение письма от туроператора по номеру брони",
    40: "Изменение статуса в заявке (по оплате)",
    44: "Удаление заявки",
    45: "Удаление обращения",
    46: "Создание счёта на оплату",
    47: "Создание копии заявки",
    52: "Изменение типа заявки",
    54: "Изменение туроператора в заявке",
    55: "Изменение офиса в заявке",
    57: "Изменение примечания в заявке",
    59: "Изменение планового платежа на оплаченный",
    61: "Клик по номеру телефона клиента",
    63: "Пропущенный звонок по телефонии",
    64: "Добавление отзыва туриста",
    67: "Онлайн-оплата: заморозка средств",
    68: "Онлайн-оплата: списание средств",
    69: "Ошибка фискализации",
    72: "Отправка кода подтверждения на подпись по смс",
    73: "Отправка ссылки на подпись документа по смс",
    74: "Подпись документа по смс",
}


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as cn:
        cn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_id INTEGER,
                event_name TEXT,
                uon_id TEXT,
                payload_json TEXT,
                received_at TEXT
            )
            """
        )
        cn.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(type_id)")
        cn.execute("CREATE INDEX IF NOT EXISTS idx_events_received ON events(received_at)")


def cleanup_old() -> None:
    if KEEP_DAYS <= 0:
        return
    cutoff = (datetime.utcnow().timestamp() - KEEP_DAYS * 86400)
    with sqlite3.connect(DB_PATH) as cn:
        cn.execute(
            "DELETE FROM events WHERE strftime('%s', received_at) < ?",
            (str(int(cutoff)),),
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    cleanup_old()
    yield


app = FastAPI(title="U-On Webhook Receiver", lifespan=lifespan)


@app.get("/health")
async def health() -> dict:
    return {"ok": True, "ts": datetime.utcnow().isoformat()}


@app.api_route("/uon-webhook", methods=["GET", "POST"])
async def receive(request: Request) -> dict:
    if request.method == "POST":
        ct = request.headers.get("content-type", "")
        if "json" in ct:
            payload = await request.json()
        else:
            form = await request.form()
            payload = dict(form)
    else:
        payload = dict(request.query_params)

    type_id = int(payload.get("type_id", 0) or 0)
    event_name = EVENT_NAMES.get(type_id, f"Событие #{type_id}")
    uon_id = str(payload.get("uon_id", ""))

    with sqlite3.connect(DB_PATH) as cn:
        cn.execute(
            "INSERT INTO events(type_id, event_name, uon_id, payload_json, received_at) VALUES (?, ?, ?, ?, ?)",
            (
                type_id,
                event_name,
                uon_id,
                json.dumps(payload, ensure_ascii=False),
                datetime.utcnow().isoformat(),
            ),
        )

    if TG_TOKEN and TG_CHAT:
        await forward_telegram(type_id, event_name, payload)
    if FORWARD_URL:
        await forward_general(type_id, event_name, payload)

    return {"ok": True, "type_id": type_id, "event_name": event_name}


@app.get("/events")
async def list_events(limit: int = 100) -> list:
    with sqlite3.connect(DB_PATH) as cn:
        cn.row_factory = sqlite3.Row
        rows = cn.execute(
            "SELECT * FROM events ORDER BY id DESC LIMIT ?", (min(limit, 500),)
        ).fetchall()
    return [dict(r) for r in rows]


@app.get("/events/{type_id}")
async def list_by_type(type_id: int, limit: int = 100) -> list:
    with sqlite3.connect(DB_PATH) as cn:
        cn.row_factory = sqlite3.Row
        rows = cn.execute(
            "SELECT * FROM events WHERE type_id = ? ORDER BY id DESC LIMIT ?",
            (type_id, min(limit, 500)),
        ).fetchall()
    return [dict(r) for r in rows]


async def forward_telegram(type_id: int, name: str, p: dict) -> None:
    lines = [f"🔔 *U-On: {esc(name)}* \\(type={type_id}\\)"]
    if p.get("request_id"):
        lines.append(f"📋 Заявка \\#{p['request_id']}")
    if p.get("client_id") or p.get("tourist_id"):
        lines.append(f"👤 Клиент \\#{p.get('client_id') or p.get('tourist_id')}")
    if p.get("status_old") and p.get("status_new"):
        lines.append(f"📊 {esc(p['status_old'])} → {esc(p['status_new'])}")
    if p.get("price") or p.get("summa"):
        lines.append(f"💰 {p.get('price') or p.get('summa')} ₽")
    if p.get("text"):
        lines.append(f"💬 {esc(str(p['text'])[:300])}")
    if p.get("uon_subdomain"):
        lines.append(f"🔗 [Открыть кабинет](https://{p['uon_subdomain']}\\.u-on\\.ru)")
    text = "\n".join(lines)

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            await client.post(
                f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                json={
                    "chat_id": TG_CHAT,
                    "text": text,
                    "parse_mode": "MarkdownV2",
                    "disable_web_page_preview": True,
                },
            )
        except httpx.HTTPError:
            pass


async def forward_general(type_id: int, name: str, p: dict) -> None:
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            await client.post(
                FORWARD_URL,
                json={
                    "source": "uon-travel",
                    "type_id": type_id,
                    "event_name": name,
                    "payload": p,
                    "received_at": datetime.utcnow().isoformat(),
                },
            )
        except httpx.HTTPError:
            pass


def esc(s: str) -> str:
    """MarkdownV2 escape."""
    for c in "_*[]()~`>#+-=|{}.!":
        s = s.replace(c, f"\\{c}")
    return s
