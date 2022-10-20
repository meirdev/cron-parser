# Cron Parser

A parser for cron expressions, it only supports the standard cron format as described at https://linux.die.net/man/5/crontab.

## Example

```python
from cron_parser import parse_expression

expression = parse_expression("15 14 1 * *")

it = expression.iterator()

for i in range(5):
    print(next(it))
```

```text
2022-11-01 14:15:00
2022-12-01 14:15:00
2023-01-01 14:15:00
2023-02-01 14:15:00
2023-03-01 14:15:00
```

## To-do

- [ ] Support for the non-standard cron format: http://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html
