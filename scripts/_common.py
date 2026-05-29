"""Общие функции для U-On API Python-скриптов.

Использование::

    from _common import UonClient
    uon = UonClient()
    leads = uon.get("leads/2026-05-01/2026-05-29/1")
    new_user = uon.post("user/create", {"u_name": "Иван", "u_phone_mobile": "+79..."})
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_env() -> None:
    env_path = REPO_ROOT / "config" / ".env"
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


def _load_key() -> str:
    _load_env()
    key = os.environ.get("UON_API_KEY", "").strip()
    if key:
        return key
    secret_path = Path.home() / ".claude" / "secrets" / "uon-api-key"
    if secret_path.is_file():
        return secret_path.read_text(encoding="utf-8").strip()
    sys.exit("❌ UON_API_KEY не задан (config/.env или ~/.claude/secrets/uon-api-key)")


class UonClient:
    """Тонкий клиент к https://api.u-on.ru/{key}.

    Делает urllib-запросы, без сторонних зависимостей.
    Лимит 10 req/sec соблюдается через throttle_ms задержку.
    """

    def __init__(
        self,
        api_key: str | None = None,
        fmt: str = "json",
        timeout: int = 30,
        throttle_ms: int = 150,
    ) -> None:
        self.api_key = api_key or _load_key()
        self.fmt = fmt
        self.timeout = timeout
        self.throttle_s = throttle_ms / 1000.0
        self.base = f"https://api.u-on.ru/{self.api_key}"
        self._last_call = 0.0

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_call
        if elapsed < self.throttle_s:
            time.sleep(self.throttle_s - elapsed)
        self._last_call = time.monotonic()

    def _url(self, endpoint: str) -> str:
        return f"{self.base}/{endpoint}.{self.fmt}"

    def get(self, endpoint: str) -> dict[str, Any]:
        self._throttle()
        url = self._url(endpoint)
        req = Request(url, method="GET", headers={"Accept": "application/json"})
        return self._call(req)

    def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        self._throttle()
        url = self._url(endpoint)
        body = "&".join(f"{quote(str(k))}={quote(str(v))}" for k, v in data.items() if v is not None)
        req = Request(
            url,
            data=body.encode("utf-8"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        return self._call(req)

    def _call(self, req: Request) -> dict[str, Any]:
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                sys.exit(f"❌ HTTP {e.code}: {body[:500]}")
        except URLError as e:
            sys.exit(f"❌ Network: {e.reason}")


def dump(obj: Any) -> None:
    """Печать JSON в stdout с русскими буквами и отступом."""
    print(json.dumps(obj, ensure_ascii=False, indent=2))
