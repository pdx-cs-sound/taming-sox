#!/usr/bin/env python3
"""Generate fade-curves.svg showing the 5 sox fade-in shapes.

Curves come from sox's effects/fade.c:
  q (quarter sine):   sin(f * pi/2)
  h (half sine):      (1 - cos(f * pi)) / 2
  t (linear):         f
  l (logarithmic):    10^(-5(1-f))
  p (inv. parabola):  1 - (1-f)^2
where f is normalized time in [0, 1].
"""

import math

W, H = 280, 180
L, R, T, B = 32, 90, 10, 24    # margins (right wider for legend)
PW, PH = W - L - R, H - T - B

def x(f): return L + f * PW
def y(v): return T + (1 - v) * PH

curves = [
    ("q  quarter sine",   "#1f77b4", lambda f: math.sin(f * math.pi / 2)),
    ("h  half sine",      "#d62728", lambda f: (1 - math.cos(f * math.pi)) / 2),
    ("t  linear",         "#2ca02c", lambda f: f),
    ("l  logarithmic",    "#9467bd", lambda f: 10 ** (-5 * (1 - f))),
    ("p  inv. parabola",  "#ff7f0e", lambda f: 1 - (1 - f) ** 2),
]

N = 200
def path(fn):
    pts = [(x(i / N), y(fn(i / N))) for i in range(N + 1)]
    d = "M " + " L ".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    return d

out = []
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="sans-serif" font-size="9">')
out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>')

# Axes
out.append(f'<rect x="{L}" y="{T}" width="{PW}" height="{PH}" '
           f'fill="none" stroke="#888" stroke-width="1"/>')

# Gridlines + tick labels
for i in range(1, 4):
    gy = T + i * PH / 4
    out.append(f'<line x1="{L}" y1="{gy:.1f}" x2="{L+PW}" y2="{gy:.1f}" '
               f'stroke="#eee"/>')
for i in range(1, 4):
    gx = L + i * PW / 4
    out.append(f'<line x1="{gx:.1f}" y1="{T}" x2="{gx:.1f}" y2="{T+PH}" '
               f'stroke="#eee"/>')

# Y ticks
for v, lbl in [(0, "0"), (0.5, "0.5"), (1, "1")]:
    py = y(v)
    out.append(f'<text x="{L-6}" y="{py+3:.1f}" text-anchor="end">{lbl}</text>')
# X ticks
for v, lbl in [(0, "0"), (0.5, "0.5"), (1, "1")]:
    px = x(v)
    out.append(f'<text x="{px:.1f}" y="{T+PH+11}" text-anchor="middle">{lbl}</text>')

# Axis labels
out.append(f'<text x="{L+PW/2}" y="{H-4}" text-anchor="middle">'
           f'normalized time</text>')
out.append(f'<text x="10" y="{T+PH/2}" text-anchor="middle" '
           f'transform="rotate(-90 10 {T+PH/2})">amplitude</text>')

# Curves
for name, color, fn in curves:
    out.append(f'<path d="{path(fn)}" fill="none" stroke="{color}" '
               f'stroke-width="1.5"/>')

# Legend
lx = L + PW + 8
ly = T + 8
for i, (name, color, _) in enumerate(curves):
    cy = ly + i * 14
    out.append(f'<line x1="{lx}" y1="{cy}" x2="{lx+14}" y2="{cy}" '
               f'stroke="{color}" stroke-width="1.5"/>')
    out.append(f'<text x="{lx+18}" y="{cy+3}">{name}</text>')

out.append('</svg>')

with open("fade-curves.svg", "w") as f:
    f.write("\n".join(out))
print("wrote fade-curves.svg")
