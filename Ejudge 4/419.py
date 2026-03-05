import math
import sys

def dist_point_to_segment(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    vv = vx * vx + vy * vy
    if vv == 0.0:
        return math.hypot(px - ax, py - ay)
    t = (wx * vx + wy * vy) / vv
    if t < 0.0:
        return math.hypot(px - ax, py - ay)
    if t > 1.0:
        return math.hypot(px - bx, py - by)
    cx, cy = ax + t * vx, ay + t * vy
    return math.hypot(px - cx, py - cy)

def norm_angle(a):
    a %= (2.0 * math.pi)
    if a < 0:
        a += 2.0 * math.pi
    return a

data = sys.stdin.read().strip().split()
R = float(data[0])
x1, y1 = float(data[1]), float(data[2])
x2, y2 = float(data[3]), float(data[4])


direct = math.hypot(x2 - x1, y2 - y1)


if R == 0.0:
    print(f"{direct:.10f}")
    sys.exit(0)


dseg = dist_point_to_segment(0.0, 0.0, x1, y1, x2, y2)
eps = 1e-12
if dseg >= R - eps:
    print(f"{direct:.10f}")
    sys.exit(0)


d1 = math.hypot(x1, y1)
d2 = math.hypot(x2, y2)

ang1 = math.atan2(y1, x1)
ang2 = math.atan2(y2, x2)


c1 = min(1.0, max(-1.0, R / d1))
c2 = min(1.0, max(-1.0, R / d2))

alpha1 = math.acos(c1)   
alpha2 = math.acos(c2)   

tang_len1 = math.sqrt(max(0.0, d1 * d1 - R * R))
tang_len2 = math.sqrt(max(0.0, d2 * d2 - R * R))

cand1 = [norm_angle(ang1 + alpha1), norm_angle(ang1 - alpha1)]
cand2 = [norm_angle(ang2 + alpha2), norm_angle(ang2 - alpha2)]

best = float("inf")
for a in cand1:
    for b in cand2:
        diff = abs(a - b)
        diff = min(diff, 2.0 * math.pi - diff) 
        total = tang_len1 + tang_len2 + R * diff
        if total < best:
            best = total

print(f"{best:.10f}")