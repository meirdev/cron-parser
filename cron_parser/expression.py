import calendar
import itertools
from datetime import datetime
from typing import Iterable, Iterator

_calendar = calendar.Calendar(6)


def _week_day(week_day: int) -> int:
    return (week_day + 1) % 7


def _month_days(year: int, month: int) -> list[tuple[int, int]]:
    days = []

    for day, weekday in _calendar.itermonthdays2(year, month):
        if day != 0:
            days.append((day, _week_day(weekday)))

    return days


class Expression:
    def __init__(
        self,
        minute: list[int],
        hour: list[int],
        day_of_month: list[int],
        month: list[int],
        day_of_week: list[int],
    ) -> None:
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week

    def iterator(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> Iterator[datetime]:
        if start is None:
            start = datetime.now()

        years: Iterable[int]

        if end is None:
            years = itertools.count(start.year)
        else:
            years = range(start.year, end.year + 1)

        for year in years:
            for month in self.month:
                for day_of_month, day_of_week in _month_days(year, month):
                    if (
                        day_of_month not in self.day_of_month
                        and day_of_week not in self.day_of_week
                    ):
                        continue

                    for hour in self.hour:
                        for minute in self.minute:
                            try:
                                date = datetime(
                                    year=year,
                                    month=month,
                                    day=day_of_month,
                                    hour=hour,
                                    minute=minute,
                                )
                            except ValueError:
                                continue

                            if date < start:
                                continue

                            if end and date > end:
                                return

                            yield date
