from datetime import datetime, timedelta

import pytest

from cron_parser import parse_expression


@pytest.mark.parametrize(
    "expression,expected",
    [
        (
            "5,6,9-12 0 * 8 *",
            [
                "2023-08-01 00:05:00",
                "2023-08-01 00:06:00",
                "2023-08-01 00:09:00",
                "2023-08-01 00:10:00",
                "2023-08-01 00:11:00",
            ],
        ),
        (
            "5 4 * * sun",
            [
                "2022-10-23 04:05:00",
                "2022-10-30 04:05:00",
                "2022-11-06 04:05:00",
                "2022-11-13 04:05:00",
                "2022-11-20 04:05:00",
            ],
        ),
        (
            "0 0,12 1 */2 *",
            [
                "2022-11-01 00:00:00",
                "2022-11-01 12:00:00",
                "2023-01-01 00:00:00",
                "2023-01-01 12:00:00",
                "2023-03-01 00:00:00",
            ],
        ),
        (
            "0 4 8-14 * *",
            [
                "2022-11-08 04:00:00",
                "2022-11-09 04:00:00",
                "2022-11-10 04:00:00",
                "2022-11-11 04:00:00",
                "2022-11-12 04:00:00",
            ],
        ),
    ],
)
def test_iterator(expression, expected):
    exp = parse_expression(expression)

    it = exp.iterator(start=datetime(year=2022, month=10, day=19, hour=9, minute=0))

    for i, e in zip(range(5), expected):
        assert str(next(it)) == e


def test_iterator_from_now():
    now = datetime.now().replace(second=0, microsecond=0)

    exp = parse_expression("@hourly")

    it = exp.iterator()

    assert next(it).replace(minute=0) == (now + timedelta(hours=1)).replace(minute=0)


def test_iterator_end():
    start = datetime.now().replace(second=0, microsecond=0)
    end = start + timedelta(hours=3)

    exp = parse_expression("@hourly")

    it = exp.iterator(start, end)

    i = 0

    with pytest.raises(StopIteration):
        while True:
            next(it)
            i += 1

    assert i == 3


def test_invalid_date():
    exp = parse_expression("@hourly")

    with pytest.raises(ValueError) as error:
        exp.iterator(start=datetime(year=2021, month=2, day=29))

    assert "day is out of range for month" in error.value.args[0]
