from cron_parser import parse_expression

expression = parse_expression("15 14 1 * *")

it = expression.iterator()

for i in range(5):
    print(next(it))
