from typing import Literal, NamedTuple

Value = Literal["0", "1", "*"]


class Predefined(NamedTuple):
    minute: Value
    hour: Value
    day_of_month: Value
    month: Value
    day_of_week: Value


YEARLY = Predefined(
    minute="0",
    hour="0",
    day_of_month="1",
    month="1",
    day_of_week="*",
)

ANNUALLY = YEARLY

MONTHLY = Predefined(
    minute="0",
    hour="0",
    day_of_month="1",
    month="*",
    day_of_week="*",
)

WEEKLY = Predefined(
    minute="0",
    hour="0",
    day_of_month="*",
    month="*",
    day_of_week="0",
)

DAILY = Predefined(
    minute="0",
    hour="0",
    day_of_month="*",
    month="*",
    day_of_week="*",
)

MIDNIGHT = DAILY

HOURLY = Predefined(
    minute="0",
    hour="*",
    day_of_month="*",
    month="*",
    day_of_week="*",
)

PREDEFINED: dict[str, Predefined] = {
    "@yearly": YEARLY,
    "@annually": ANNUALLY,
    "@monthly": MONTHLY,
    "@weekly": WEEKLY,
    "@daily": DAILY,
    "@midnight": MIDNIGHT,
    "@hourly": HOURLY,
    # "@reboot": None,
}
