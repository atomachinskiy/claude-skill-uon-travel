"""Тесты для _common.UonClient — auth, URL-builder, GET/POST."""
from __future__ import annotations


def test_get_returns_fixture(uon):
    client, rec = uon
    data = client.get("manager")
    assert "users" in data
    assert len(data["users"]) >= 1
    assert rec.calls[0]["method"] == "GET"
    assert rec.calls[0]["url"].endswith("/manager.json")


def test_get_statuses(uon):
    client, rec = uon
    data = client.get("status")
    assert "records" in data
    assert any(r.get("name") == "В работе" for r in data["records"])


def test_get_payment_forms(uon):
    client, rec = uon
    data = client.get("payment_form")
    names = [r["name"] for r in data.get("records", [])]
    assert "Наличный" in names
    assert "По карте" in names


def test_post_builds_form_body(uon):
    client, rec = uon
    client.post("user/create", {"u_name": "Иван", "u_phone_mobile": "+79991234567"})
    call = rec.calls[0]
    assert call["method"] == "POST"
    assert call["url"].endswith("/user/create.json")
    assert "u_name=" in call["body"]
    assert "u_phone_mobile=" in call["body"]


def test_post_empty_body(uon):
    # POST с пустым словарём — тело None или пустая строка
    client, rec = uon
    client.post("ping", {})
    assert rec.calls[0]["body"] in (None, "")


def test_url_contains_api_key(uon):
    client, rec = uon
    client.get("manager")
    assert "TEST_KEY_FAKE" in rec.calls[0]["url"]
    assert rec.calls[0]["url"].startswith("https://api.u-on.ru/TEST_KEY_FAKE/")
