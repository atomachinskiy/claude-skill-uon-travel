"""pytest-фикстуры: мокаем urlopen в _common, чтобы тесты ходили в фикстуры,
не в live API. Каждый тест получает access к "записаным" вызовам для проверки.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

# Подкладываем scripts/ в sys.path, чтобы импортировать _common
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

FIXTURES = Path(__file__).resolve().parent / "fixtures"
os.environ.setdefault("UON_API_KEY", "TEST_KEY_FAKE")


class FakeResponse:
    """Минимальный stand-in для http.client.HTTPResponse."""

    def __init__(self, body: bytes, status: int = 200):
        self._body = body
        self.status = status

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class CallRecorder:
    """Запоминает все запросы для assert-ов в тестах."""

    def __init__(self):
        self.calls: list[dict] = []

    def __call__(self, req, *a, **kw):
        # req — urllib.request.Request
        method = req.get_method()
        url = req.full_url
        body = req.data.decode("utf-8") if req.data else None

        record = {"method": method, "url": url, "body": body}
        self.calls.append(record)

        # Подбираем фикстуру по endpoint после /TEST_KEY_FAKE/
        from urllib.parse import urlparse
        path = urlparse(url).path
        # /TEST_KEY_FAKE/manager.json → manager
        parts = path.split("/")[2:]  # пропускаем "" и key
        ep = "/".join(parts).replace(".json", "").replace(".xml", "")
        fixture_name = ep.replace("/", "__") + ".json"
        fixture_path = FIXTURES / fixture_name

        if fixture_path.exists():
            return FakeResponse(fixture_path.read_bytes(), 200)
        # Default: empty success
        body = json.dumps({"result": 200, "id": "1"}).encode("utf-8")
        return FakeResponse(body, 200)


@pytest.fixture
def uon(monkeypatch):
    """Зачерчиваем urlopen, отдаём свежий UonClient + рекордер вызовов."""
    import _common

    recorder = CallRecorder()
    monkeypatch.setattr(_common, "urlopen", recorder)
    # Сбрасываем throttle чтобы тесты летели
    client = _common.UonClient(api_key="TEST_KEY_FAKE", throttle_ms=0)
    return client, recorder
