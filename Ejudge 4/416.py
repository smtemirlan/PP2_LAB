import sys
from datetime import datetime, timedelta

def parse_time(s: str) -> datetime:
    # Example: "2026-01-01 10:00:00 UTC+03:00"
    date_part, time_part, tz_part = s.strip().split()

    dt = datetime.strptime(date_part + " " + time_part, "%Y-%m-%d %H:%M:%S")

    # tz_part like "UTC+03:00" or "UTC-05:30"
    sign = 1 if tz_part[3] == '+' else -1
    hh = int(tz_part[4:6])
    mm = int(tz_part[7:9])
    offset = timedelta(hours=hh, minutes=mm) * sign

    # Convert to UTC: local_time - offset
    return dt - offset

lines = sys.stdin.read().splitlines()
start = parse_time(lines[0])
end = parse_time(lines[1])

print(int((end - start).total_seconds()))