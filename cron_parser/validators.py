from typing import NamedTuple


def inclusive(min: int, max: int) -> range:
    return range(min, max)


class Validator(NamedTuple):
    range: range
    alias: dict[str, int] = {}

    def get_value(self, value: str | int) -> int:
        if isinstance(value, str):
            val = int(self.alias.get(value.lower(), value))
        else:
            val = value

        if not self.range.start <= val <= self.range.stop:
            raise ValueError(
                f"{val=!r} out of bound ({self.range.start}-{self.range.stop})"
            )

        return val


SECOND = Validator(
    range=inclusive(min=0, max=59),
)

MINUTE = Validator(
    range=inclusive(min=0, max=59),
)

HOUR = Validator(
    range=inclusive(min=0, max=23),
)

DAY_OF_MONTH = Validator(
    range=inclusive(min=1, max=31),
)

MONTH = Validator(
    range=inclusive(min=1, max=12),
    alias={
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    },
)

DAY_OF_WEEK = Validator(
    range=inclusive(min=0, max=7),
    alias={
        "sun": 0,
        "mon": 1,
        "tue": 2,
        "wed": 3,
        "thu": 4,
        "fri": 5,
        "sat": 6,
    },
)

YEAR = Validator(
    range=inclusive(min=1970, max=2099),
)
