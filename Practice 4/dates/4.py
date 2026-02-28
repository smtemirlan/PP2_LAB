from datetime import datetime

date1 = datetime(2026, 2, 20, 12, 0, 0)
date2 = datetime(2026, 2, 28, 15, 30, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print("Difference in seconds:", int(seconds))   