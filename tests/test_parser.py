import pytest

from cron_parser import parse_expression


def inclusive_range(start: int, stop: int, step: int = 1) -> list[int]:
    return list(range(start, stop + 1, step))


def test_valid():
    exp = parse_expression("23 0-20/2 * * *")

    assert exp.minute == [23]
    assert exp.hour == inclusive_range(0, 20, 2)
    assert exp.day_of_month == inclusive_range(1, 31)
    assert exp.month == inclusive_range(1, 12)
    assert exp.day_of_week == inclusive_range(0, 6)


def test_7_in_weekday():
    exp = parse_expression("0 0 1 1 5-7")

    assert exp.day_of_week == [0, 5, 6]


def test_invalid_predefined():
    with pytest.raises(ValueError) as error:
        parse_expression("@invalid")

    assert "'@invalid' is not predefined" in error.value.args[0]


def test_valid_predefined():
    exp = parse_expression("@daily")

    assert exp.minute == [0]
    assert exp.hour == [0]
    assert exp.day_of_month == inclusive_range(1, 31)
    assert exp.month == inclusive_range(1, 12)
    assert exp.day_of_week == inclusive_range(0, 6)


def test_invalid_number_of_fields():
    with pytest.raises(ValueError) as error:
        parse_expression("1 2 3 4 5 6")

    assert "expected 1 or 5 fields, got 6" in error.value.args[0]


def test_invalid_step_value():
    with pytest.raises(ValueError) as error:
        parse_expression("1-6/0 * * * *")

    assert "must be greater than 0" in error.value.args[0]

    with pytest.raises(ValueError) as error:
        parse_expression("1-6/-2 * * * *")

    assert "must be greater than 0" in error.value.args[0]


def test_invalid_step_field():
    with pytest.raises(ValueError) as error:
        parse_expression("6/0 * * * *")

    assert "step is only allowed in the range or *" in error.value.args[0]


def test_invalid_range():
    with pytest.raises(ValueError) as error:
        parse_expression("6-1 * * * *")

    assert "cannot be less than" in error.value.args[0]


def test_invalid_range_out_of_bounds():
    with pytest.raises(ValueError) as error:
        parse_expression("1-60 * * * *")

    assert "out of bound" in error.value.args[0]
