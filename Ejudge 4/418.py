import sys

data = sys.stdin.read().split()
x1, y1 = float(data[0]), float(data[1])
x2, y2 = float(data[2]), float(data[3])


x2p, y2p = x2, -y2


dx = x2p - x1
dy = y2p - y1


t = -y1 / dy

x = x1 + t * dx
y = 0.0

print(f"{x:.10f} {y:.10f}")