"""Тесты для cli.py-команд — что они шлют правильный URL/body."""
from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def run_cli(argv: list[str], rec):
    """Запустить cli.main() с подменённым sys.argv. Возвращает stdout."""
    import cli  # импортируется из conftest pre-set sys.path
    buf = StringIO()
    with patch.object(sys, "argv", ["uon", *argv]), patch.object(sys, "stdout", buf):
        try:
            cli.main()
        except SystemExit as e:
            if e.code not in (None, 0):
                raise
    return buf.getvalue()


def test_statuses_requests(uon):
    _, rec = uon
    run_cli(["statuses", "requests"], rec)
    assert rec.calls[-1]["url"].endswith("/status.json")
    assert rec.calls[-1]["method"] == "GET"


def test_statuses_leads(uon):
    _, rec = uon
    run_cli(["statuses", "leads"], rec)
    assert rec.calls[-1]["url"].endswith("/status_lead.json")


def test_statuses_pay(uon):
    _, rec = uon
    run_cli(["statuses", "pay"], rec)
    assert rec.calls[-1]["url"].endswith("/status_pay.json")


def test_managers_list(uon):
    _, rec = uon
    run_cli(["managers", "list"], rec)
    assert rec.calls[-1]["url"].endswith("/manager.json")


def test_leads_list_period(uon):
    _, rec = uon
    run_cli(["leads", "list", "--from", "2026-05-01", "--to", "2026-05-29"], rec)
    assert "/leads/2026-05-01/2026-05-29/1.json" in rec.calls[-1]["url"]


def test_leads_list_with_source(uon):
    _, rec = uon
    run_cli(["leads", "list", "--from", "2026-05-01", "--to", "2026-05-29", "--source-id", "5"], rec)
    assert "/leads/2026-05-01/2026-05-29/5/1.json" in rec.calls[-1]["url"]


def test_requests_list_closed(uon):
    _, rec = uon
    run_cli(["requests", "list", "--from", "2026-05-01", "--to", "2026-05-29", "--closed"], rec)
    assert "/requests/closed/2026-05-01/2026-05-29/1.json" in rec.calls[-1]["url"]


def test_requests_list_updated(uon):
    _, rec = uon
    run_cli(["requests", "list", "--from", "2026-05-01", "--to", "2026-05-29", "--updated"], rec)
    assert "/requests/updated/2026-05-01/2026-05-29/1.json" in rec.calls[-1]["url"]


def test_users_find_phone_strips_plus(uon):
    _, rec = uon
    run_cli(["users", "find", "--phone", "+7 999 123-45-67"], rec)
    # Должны быть только цифры
    assert "/user/phone/79991234567.json" in rec.calls[-1]["url"]


def test_users_create_minimal(uon):
    _, rec = uon
    run_cli(["users", "create", "--name", "Иван", "--phone", "+79991234567"], rec)
    call = rec.calls[-1]
    assert call["method"] == "POST"
    assert call["url"].endswith("/user/create.json")
    assert "u_name=" in call["body"]
    assert "u_phone_mobile=" in call["body"]


def test_requests_update_uses_request_status_id(uon):
    """Критический gotcha: /request/update использует request_status_id, НЕ status_id."""
    _, rec = uon
    run_cli(["requests", "update", "42", "--status-id", "2"], rec)
    call = rec.calls[-1]
    assert call["method"] == "POST"
    assert call["url"].endswith("/request/update/42.json")
    assert "request_status_id=2" in call["body"]
    # ловим обе формы: "status_id=2" в начале (без префикса) или после &
    assert not (call["body"].startswith("status_id=") or "&status_id=" in call["body"])


def test_services_add_uses_type_id_not_type(uon):
    """Критический gotcha: /service/create требует type_id, НЕ type."""
    _, rec = uon
    run_cli([
        "services", "add",
        "--request-id", "42", "--type", "1",
        "--name", "Hilton 5*", "--price-client", "50000",
    ], rec)
    call = rec.calls[-1]
    assert call["url"].endswith("/service/create.json")
    assert "type_id=1" in call["body"]
    # description вместо name, price вместо price_client
    assert "description=" in call["body"]
    assert "price=" in call["body"]
    # эти НЕ должны попасть
    assert "type=1&" not in call["body"]
    assert "type=1$" not in call["body"]


def test_payments_create_required_cio_id(uon):
    """Платёж требует cio_id (1=приход, 2=расход)."""
    _, rec = uon
    run_cli(["payments", "create", "--request-id", "42", "--amount", "30000", "--form-id", "1"], rec)
    body = rec.calls[-1]["body"]
    assert "cio_id=1" in body  # default direction=in
    assert "type_id=1" in body  # default — с клиентом
    assert "price=30000" in body
    assert "r_id=42" in body


def test_payments_create_outgoing(uon):
    _, rec = uon
    run_cli(["payments", "create", "--request-id", "42", "--amount", "30000", "--direction", "out"], rec)
    assert "cio_id=2" in rec.calls[-1]["body"]


def test_actions_create_default_type_id_0(uon):
    _, rec = uon
    run_cli(["actions", "create", "--request-id", "42", "--text", "Перезвонить"], rec)
    body = rec.calls[-1]["body"]
    assert "type_id=0" in body
    assert "text=" in body
    assert "datetime=" in body  # автозаполнен сейчасным временем


def test_deadlines_create_uses_summ_not_amount(uon):
    """Дедлайны: поле summ, НЕ amount."""
    _, rec = uon
    run_cli(["deadlines", "create", "--request-id", "42", "--amount", "20000", "--date", "2026-06-15"], rec)
    body = rec.calls[-1]["body"]
    assert "summ=20000" in body
    assert "type_id=1" in body
    assert "date=2026-06-15" in body


def test_webhook_create(uon):
    _, rec = uon
    run_cli(["webhooks", "create", "--type", "2", "--url", "https://example.com/wh"], rec)
    call = rec.calls[-1]
    assert call["url"].endswith("/webhook/create.json")
    body = call["body"]
    assert "type_id=2" in body
    assert "url=https" in body


def test_tourists_link(uon):
    _, rec = uon
    run_cli(["tourists-requests", "add", "--request-id", "42", "--tourist-id", "5"], rec)
    body = rec.calls[-1]["body"]
    assert "r_id=42" in body
    assert "tourist_id=5" in body


def test_calls_log_inbound(uon):
    _, rec = uon
    run_cli(["calls", "log", "--phone", "+79991234567", "--inbound", "--duration", "180"], rec)
    body = rec.calls[-1]["body"]
    assert "phone=" in body
    assert "direction=2" in body  # 2 = входящий
    assert "duration=180" in body


def test_calls_log_outbound_default(uon):
    _, rec = uon
    run_cli(["calls", "log", "--phone", "+79991234567"], rec)
    assert "direction=1" in rec.calls[-1]["body"]


def test_hotels_create(uon):
    _, rec = uon
    run_cli(["hotels", "create", "--name", "Hilton", "--stars", "5"], rec)
    body = rec.calls[-1]["body"]
    assert "name=Hilton" in body
    assert "stars=5" in body


def test_suppliers_create(uon):
    _, rec = uon
    run_cli(["suppliers", "create", "--name", "Pegas", "--type-id", "4", "--inn", "1234567890"], rec)
    body = rec.calls[-1]["body"]
    assert "name=Pegas" in body
    assert "type_id=4" in body
    assert "inn=1234567890" in body


def test_raw_get(uon):
    _, rec = uon
    run_cli(["raw", "get", "company-office"], rec)
    assert rec.calls[-1]["url"].endswith("/company-office.json")


def test_raw_post(uon):
    _, rec = uon
    run_cli(["raw", "post", "service/create", "-F", "r_id=42", "-F", "type_id=1"], rec)
    body = rec.calls[-1]["body"]
    assert "r_id=42" in body
    assert "type_id=1" in body


def test_leads_create_full_card(uon):
    """Карточка lead с пожеланиями + UTM + соцсетями."""
    _, rec = uon
    run_cli([
        "leads", "create",
        "--name", "Анна", "--surname", "Тестова", "--phone", "+79992223344",
        "--email", "anna@test.ru", "--telegram", "@anna",
        "--countries", "1", "--budget", "200000",
        "--wish-date-from", "2026-08-01", "--wish-date-to", "2026-08-14",
        "--nights-from", "10", "--nights-to", "14",
        "--adults", "2", "--children", "1",
        "--hotel-types", "4*,5*", "--nutrition", "AI,UAI",
        "--utm-source", "instagram", "--utm-campaign", "turkey",
    ], rec)
    body = rec.calls[-1]["body"]
    assert "u_name=" in body and "u_phone_mobile=" in body
    assert "u_telegram=" in body
    assert "countries=1" in body
    assert "budget=200000" in body
    assert "tourist_count=2" in body
    assert "tourist_child_count=1" in body
    assert "hotel_types=" in body
    assert "nutrition=" in body
    assert "utm_source=instagram" in body
    assert "utm_campaign=turkey" in body


def test_leads_update_status(uon):
    """leads update двигает по статусам через /request/update с lead_status_id."""
    _, rec = uon
    run_cli(["leads", "update", "1", "--status-id", "5"], rec)
    call = rec.calls[-1]
    assert call["url"].endswith("/request/update/1.json")
    assert "lead_status_id=5" in call["body"]


def test_leads_update_reason_deny(uon):
    _, rec = uon
    run_cli(["leads", "update", "1", "--reason-deny-id", "3"], rec)
    assert "reason_deny_id=3" in rec.calls[-1]["body"]


def test_leads_update_requires_payload(uon):
    """Без аргументов — должна быть ошибка, не пустой POST."""
    import pytest as _p
    _, rec = uon
    with _p.raises(SystemExit):
        run_cli(["leads", "update", "1"], rec)


def test_users_create_full_card(uon):
    """Карточка туриста с паспортами, мессенджерами, метками, гражданством."""
    _, rec = uon
    run_cli([
        "users", "create",
        "--name", "Анна", "--surname", "Иванова", "--phone", "+79991234567",
        "--patronymic", "Петровна", "--sex", "ж", "--birthday", "1990-05-15",
        "--email", "a@example.com",
        "--telegram", "@anna", "--whatsapp", "+79991234567", "--max", "anna_max",
        "--zagran-number", "73 1234567", "--zagran-given", "2023-01-01",
        "--zagran-expire", "2033-01-01", "--zagran-org", "УВД Москвы",
        "--passport-number", "4515 987654", "--passport-taken", "ОВД Тверского",
        "--passport-date", "2010-03-01", "--passport-code", "770-001",
        "--inn", "770123456789",
        "--nationality-id", "1",
        "--labels", "VIP,Семья,Активный отдых",
        "--discount", "10",
    ], rec)
    body = rec.calls[-1]["body"]
    # ФИО
    assert "u_name=" in body and "u_surname=" in body and "u_sname=" in body
    # Демография
    assert "u_sex=" in body and "u_birthday=" in body
    # Мессенджеры
    assert "u_telegram=" in body and "u_max=" in body
    # Паспорта
    assert "u_zagran_number=" in body and "u_zagran_organization=" in body
    assert "u_passport_number=" in body and "u_passport_taken=" in body
    # Юр. лицо
    assert "u_inn=" in body
    # Связи
    assert "nationality_id=1" in body
    assert "u_labels=" in body
    # Скидка
    assert "u_discount=10" in body


def test_users_update_single_field(uon):
    _, rec = uon
    run_cli(["users", "update", "5", "--labels", "VIP"], rec)
    call = rec.calls[-1]
    assert call["url"].endswith("/user/update/5.json")
    assert "u_labels=VIP" in call["body"]


def test_users_update_requires_payload(uon):
    import pytest as _p
    _, rec = uon
    with _p.raises(SystemExit):
        run_cli(["users", "update", "5"], rec)


def test_labels_list(uon):
    _, rec = uon
    run_cli(["labels", "list"], rec)
    assert rec.calls[-1]["url"].endswith("/user-label.json")


def test_fields_list_filtered_by_section(uon):
    _, rec = uon
    run_cli(["fields", "list", "--section", "3"], rec)
    assert rec.calls[-1]["url"].endswith("/extended_field/1.json")


def test_fields_create(uon):
    _, rec = uon
    run_cli([
        "fields", "create", "--section", "2", "--name", "Канал",
        "--type", "2", "--options", "Сайт,IG,TG",
    ], rec)
    body = rec.calls[-1]["body"]
    assert "section=2" in body
    assert "name=" in body
    assert "type=2" in body
    assert "options=" in body


def test_extended_field_via_minus_F(uon):
    """Доп.поле прокидывается в lead через -F."""
    _, rec = uon
    run_cli([
        "leads", "create", "--name", "Иван", "--phone", "+79991234567",
        "-F", "extended_fields[199888]=Соцсети",
    ], rec)
    body = rec.calls[-1]["body"]
    # urlencoded: extended_fields[199888] становится %5B...%5D
    assert "extended_fields" in body
    assert "199888" in body
