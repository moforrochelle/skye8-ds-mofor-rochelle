from src.load import (
    clean_boolean,
    clean_date,
    clean_distance,
    clean_integer,
    clean_timestamp,
)


def test_clean_boolean():
    assert clean_boolean("Yes") is True
    assert clean_boolean("TRUE") is True
    assert clean_boolean("1") is True
    assert clean_boolean("no") is False
    assert clean_boolean("FALSE") is False
    assert clean_boolean("0") is False


def test_clean_distance():
    assert clean_distance("10.3 km") == 10.3
    assert clean_distance("7.9") == 7.9
    assert clean_distance("") is None


def test_clean_integer():
    assert clean_integer("21 days") == 21
    assert clean_integer("7") == 7


def test_clean_date():
    assert str(clean_date("18/11/2024")) == "2024-11-18"
    assert str(clean_date("2026-01-22")) == "2026-01-22"


def test_clean_timestamp():
    assert clean_timestamp("15/04/2025 08:15") is not None
    assert clean_timestamp("2025-04-08 06:15:00") is not None
    assert clean_timestamp("1755699300") is not None