#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Placeholder logo trio for SkillGems (until 主人 provides the real logo art).
Pure-python PNG writer + supersampled rasterizer — no dependencies.
Outputs: logo.png 256 (transparent rounded corners), favicon.png 64,
apple-touch-icon.png 180 (full-bleed solid bg; iOS applies its own mask).
Rerun: python3 scripts/gen_assets.py
"""
import math, struct, zlib, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def lerp(a, b, t): return tuple(a[i] + (b[i]-a[i])*t for i in range(3))

C1 = (29, 93, 169)    # #1d5da9
C2 = (94, 160, 230)   # #5ea0e6
GEM_TOP = (219, 233, 251)
GEM_BODY = (255, 255, 255)
GEM_LOW = (234, 242, 252)
SPARK = (240, 194, 94)

def rounded_rect_sdf(x, y, size, r):
    # distance to rounded square [0,size]^2, corner radius r
    cx, cy = size/2, size/2
    hx, hy = size/2 - r, size/2 - r
    dx, dy = abs(x-cx) - hx, abs(y-cy) - hy
    ax, ay = max(dx, 0), max(dy, 0)
    return math.hypot(ax, ay) + min(max(dx, dy), 0) - r

def poly_contains(px, py, pts):
    inside = False
    j = len(pts)-1
    for i in range(len(pts)):
        xi, yi = pts[i]; xj, yj = pts[j]
        if (yi > py) != (yj > py) and px < (xj-xi)*(py-yi)/(yj-yi)+xi:
            inside = not inside
        j = i
    return inside

# 64-unit viewBox geometry, scaled by k
GEM   = [(32,15),(46,27),(32,49),(18,27)]
FACET = [(32,15),(46,27),(18,27)]
LOWER = [(25,27),(32,49),(39,27)]
def spark_pts(cx, cy, s):
    # 4-point star: tips at distance s, waist at 0.35s
    return [(cx, cy-s), (cx+0.35*s, cy-0.35*s), (cx+s, cy), (cx+0.35*s, cy+0.35*s),
            (cx, cy+s), (cx-0.35*s, cy+0.35*s), (cx-s, cy), (cx-0.35*s, cy-0.35*s)]

def render(size, full_bleed=False):
    k = size/64.0
    ss = 2  # supersample factor per axis
    rows = []
    gem = [(x*k, y*k) for x, y in GEM]
    facet = [(x*k, y*k) for x, y in FACET]
    lower = [(x*k, y*k) for x, y in LOWER]
    spark = spark_pts(49.4*k, 19.4*k, 6.2*k)
    rr = size*0.20
    for py in range(size):
        row = bytearray([0])  # filter type 0
        for px in range(size):
            acc = [0.0, 0.0, 0.0, 0.0]
            for sy in range(ss):
                for sx in range(ss):
                    x = px + (sx+0.5)/ss
                    y = py + (sy+0.5)/ss
                    if full_bleed:
                        a = 1.0
                    else:
                        d = rounded_rect_sdf(x, y, size, rr)
                        a = max(0.0, min(1.0, 0.5 - d))  # 1px AA edge
                    if a <= 0: continue
                    if full_bleed:
                        # solid gradient bg (iOS masks corners itself)
                        t = (x/size + y/size)/2
                        col = lerp(C1, C2, t); alpha = 1.0
                    else:
                        t = (x/size + y/size)/2
                        col = lerp(C1, C2, t); alpha = a
                    # gem (drawn at 64-unit coords * k)
                    if poly_contains(x, y, lower):
                        col = GEM_LOW; alpha = max(alpha, a)
                    if poly_contains(x, y, gem):
                        col = GEM_BODY; alpha = a
                    if poly_contains(x, y, facet):
                        col = GEM_TOP; alpha = a
                    if poly_contains(x, y, spark):
                        col = SPARK; alpha = a
                    acc[0] += col[0]*alpha; acc[1] += col[1]*alpha; acc[2] += col[2]*alpha
                    acc[3] += alpha
            n = acc[3]
            if n > 0:
                r8, g8, b8 = (round(acc[0]/n), round(acc[1]/n), round(acc[2]/n))
                a8 = round(255 * min(1.0, n))
            else:
                r8 = g8 = b8 = a8 = 0
            row += bytes((r8, g8, b8, a8))
        rows.append(bytes(row))
    return rows

def write_png(path, size, rows):
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
    raw = b"".join(rows)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    print(path, os.path.getsize(path), "bytes")

if __name__ == "__main__":
    # v1 placeholder mark — bump ?v=N in index.html references when replacing
    write_png(os.path.join(ROOT, "logo.png"), 256, render(256))
    write_png(os.path.join(ROOT, "favicon.png"), 64, render(64))
    write_png(os.path.join(ROOT, "apple-touch-icon.png"), 180, render(180, full_bleed=True))
