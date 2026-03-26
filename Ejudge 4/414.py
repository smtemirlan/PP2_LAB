import sys
from datetime import datetime, timedelta

def to_utc_midnight(line: str) -> datetime:
    # "YYYY-MM-DD UTC±HH:MM"
    date_str, tz_str = line.strip().split()
    y, m, d = map(int, date_str.split("-"))

    sign = 1 if tz_str[3] == '+' else -1
    hh = int(tz_str[4:6])
    mm = int(tz_str[7:9])
    offset = timedelta(hours=hh, minutes=mm) * sign

    local_midnight = datetime(y, m, d, 0, 0, 0)
    return local_midnight - offset  # convert to UTC

lines = sys.stdin.read().strip().splitlines()
t1 = to_utc_midnight(lines[0])
t2 = to_utc_midnight(lines[1])

delta = abs(int((t2 - t1).total_seconds()))
print(delta // 86400)