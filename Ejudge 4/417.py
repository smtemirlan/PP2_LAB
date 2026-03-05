import sys
import math

data = sys.stdin.read().split()
R = float(data[0])
x1, y1 = float(data[1]), float(data[2])
x2, y2 = float(data[3]), float(data[4])

dx = x2 - x1
dy = y2 - y1

# If segment is a point
seg_len = math.hypot(dx, dy)
if seg_len == 0.0:
    inside = (x1 * x1 + y1 * y1) <= R * R + 1e-12
    print(f"{(0.0 if not inside else 0.0):.10f}")
    sys.exit(0)

# Solve |A + t*(B-A)|^2 = R^2
a = dx * dx + dy * dy
b = 2.0 * (x1 * dx + y1 * dy)
c = x1 * x1 + y1 * y1 - R * R

disc = b * b - 4.0 * a * c

# No intersection with the circle boundary
if disc < 0:
    # Either fully inside or fully outside (since continuous)
    if (x1 * x1 + y1 * y1 <= R * R + 1e-12) and (x2 * x2 + y2 * y2 <= R * R + 1e-12):
        print(f"{seg_len:.10f}")
    else:
        print(f"{0.0:.10f}")
    sys.exit(0)

sqrt_disc = math.sqrt(max(0.0, disc))
t1 = (-b - sqrt_disc) / (2.0 * a)
t2 = (-b + sqrt_disc) / (2.0 * a)
if t1 > t2:
    t1, t2 = t2, t1

# Inside region in parameter t is [t1, t2]
left = max(0.0, t1)
right = min(1.0, t2)

if right <= left:
    # Could still be fully inside if tangent/degenerate numeric
    if (x1 * x1 + y1 * y1 <= R * R + 1e-12) and (x2 * x2 + y2 * y2 <= R * R + 1e-12):
        print(f"{seg_len:.10f}")
    else:
        print(f"{0.0:.10f}")
else:
    inside_len = (right - left) * seg_len
    print(f"{inside_len:.10f}")