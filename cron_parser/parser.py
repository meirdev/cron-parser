import enum
import re

from .expression import Expression
from .predefined import PREDEFINED
from .validators import DAY_OF_MONTH, DAY_OF_WEEK, HOUR, MINUTE, MONTH, Validator


class Token:
    STEP = "/"
    RANGE = "-"
    ALL = "*"
    SEPARATOR = ","


class Field(enum.IntEnum):
    MINUTE = 0
    HOUR = 1
    DAY_OF_MONTH = 2
    MONTH = 3
    DAY_OF_WEEK = 4


FIELD_VALIDATOR = {
    Field.MINUTE: MINUTE,
    Field.HOUR: HOUR,
    Field.DAY_OF_MONTH: DAY_OF_MONTH,
    Field.MONTH: MONTH,
    Field.DAY_OF_WEEK: DAY_OF_WEEK,
}


def _get_ignore_days(fields: list[str]) -> Validator | None:
    day_of_month, day_of_week = fields[Field.DAY_OF_MONTH], fields[Field.DAY_OF_WEEK]

    if day_of_month == Token.ALL and day_of_week != Token.ALL:
        return DAY_OF_MONTH

    if day_of_month != Token.ALL and day_of_week == Token.ALL:
        return DAY_OF_WEEK

    return None


def parse_expression(expression: str) -> Expression:
    fields = re.split(r"\s+", expression)

    if len(fields) == 1:
        predefined = fields[0]

        if predefined not in PREDEFINED:
            raise ValueError(f"{predefined=!r} is not predefined: {PREDEFINED}")

        fields = list(PREDEFINED[predefined])

    if len(fields) == 5:
        parsed_fields = []

        ignore_days = _get_ignore_days(fields)

        for i, field in enumerate(fields):
            validator = FIELD_VALIDATOR[Field(i)]

            times: list[int] = []

            for item in field.split(Token.SEPARATOR):
                min: str | int = ""
                max: str | int = ""
                step: str | int = ""

                if Token.STEP in item:
                    item, step = item.split(Token.STEP, 1)

                    if Token.RANGE in item:
                        min, max = item.split(Token.RANGE, 1)

                    elif Token.ALL == item:
                        min, max = validator.range.start, validator.range.stop

                    else:
                        raise ValueError(
                            f"{item=!r} step is only allowed in the range or *"
                        )

                elif Token.RANGE in item:
                    min, max = item.split(Token.RANGE, 1)
                    step = 1

                elif Token.ALL == item:
                    min, max, step = validator.range.start, validator.range.stop, 1

                else:
                    min, max, step = item, item, 1

                min, max, step = (
                    validator.get_value(min),
                    validator.get_value(max),
                    int(step),
                )

                if step <= 0:
                    raise ValueError(f"{step=!r} must be greater than 0")

                if max < min:
                    raise ValueError(f"{min=!r} cannot be less than {max=!r}")

                if validator is not ignore_days:
                    values = list(range(min, max + 1, step))

                    if validator is DAY_OF_WEEK:
                        if 0 in values and 7 in values:
                            values.remove(7)
                        elif 7 in values:
                            values.remove(7)
                            values.append(0)

                    times = sorted(times + values)

            parsed_fields.append(times)

        return Expression(*parsed_fields)

    raise ValueError(f"expected 1 or 5 fields, got {len(fields)}")
