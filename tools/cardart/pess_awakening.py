"""Pessimist deck, awakening and disillusion: cards 0-VII."""

import math

from .common import (ETCH_INK, IMAGE_BOX, PESS_PAPER, WASH, W, H, aquatint, f,
                     plate_close, plate_open, svg)


def giant_deer(rng):
    ink = ETCH_INK
    bone, verdigris = WASH["bone"], WASH["verdigris"]
    ix0, iy0, ix1, iy1 = IMAGE_BOX
    out = [plate_open()]

    out.append(aquatint())

    # Verdigris wash: mist band between the trunks and the ground
    out.append(f'<rect x="{ix0 - 40}" y="540" width="{ix1 - ix0 + 80}" height="300" fill="{verdigris}" opacity="0.22" filter="url(#mist)"/>')
    out.append(f'<rect x="{ix0 - 40}" y="860" width="{ix1 - ix0 + 80}" height="260" fill="{verdigris}" opacity="0.32" filter="url(#softwash)"/>')

    # Bare forest: thin leafless trunks, hatched on their shaded side
    for k in range(16):
        tx = ix0 + 10 + k * (ix1 - ix0 - 20) / 15 + rng.uniform(-12, 12)
        far = rng.random() < 0.5
        w = rng.uniform(2, 4) if far else rng.uniform(5, 10)
        op = 0.35 if far else 0.85
        top = iy0 - 10
        bot = rng.uniform(820, 880) if far else rng.uniform(900, 960)
        wob = rng.uniform(-8, 8)
        out.append(f'<path d="M{f(tx)},{f(bot)} C{f(tx + wob)},{f(bot - 300)} {f(tx - wob)},{f(top + 300)} {f(tx + wob / 2)},{top}" '
                   f'fill="none" stroke="{ink}" stroke-width="{f(w)}" opacity="{op}"/>')
        for _ in range(rng.randint(2, 5)):
            by = rng.uniform(iy0 + 40, 600)
            ln = rng.uniform(20, 70)
            sgn = rng.choice([-1, 1])
            out.append(f'<path d="M{f(tx)},{f(by)} q{f(sgn * ln * 0.6)},{f(-ln * 0.2)} {f(sgn * ln)},{f(-ln * 0.7)}" fill="none" '
                       f'stroke="{ink}" stroke-width="{f(max(0.8, w * 0.25))}" opacity="{op}"/>')

    # Ground: dry grass and fallen leaves, etched as short strokes
    for _ in range(500):
        gx, gy = rng.uniform(ix0, ix1), rng.uniform(930, iy1)
        h = rng.uniform(6, 20)
        out.append(f'<path d="M{f(gx)},{f(gy)} l{f(rng.uniform(-5, 5))},{f(-h)}" stroke="{ink}" stroke-width="0.8" opacity="{rng.uniform(0.4, 0.9):.2f}"/>')
    for _ in range(70):
        lx, ly = rng.uniform(ix0, ix1), rng.uniform(950, iy1)
        out.append(f'<ellipse cx="{f(lx)}" cy="{f(ly)}" rx="5" ry="2.2" fill="none" stroke="{ink}" stroke-width="0.8" '
                   f'transform="rotate({rng.uniform(0, 180):.0f} {f(lx)} {f(ly)})" opacity="0.7"/>')

    # The deer: profile facing left, head bowed almost to the ground
    out.append('<g transform="translate(12,-72)">')
    body = ("M 300,800 C 320,760 420,745 500,760 C 545,768 565,800 560,840 C 556,875 520,890 470,888 "
            "C 420,886 360,890 330,880 C 300,870 285,835 300,800 Z")
    neck = "M 330,805 C 300,820 270,860 245,905 L 268,918 C 292,880 320,850 352,840 Z"
    head = "M 232,898 C 222,905 205,930 200,948 C 198,956 208,960 214,956 C 228,945 252,932 268,918 Z"
    legs = [(345, 878, 340, 1005), (372, 882, 380, 1008), (490, 884, 482, 1004), (525, 878, 536, 1002)]
    hatch_id = "deerclip"
    out.append(f'<clipPath id="{hatch_id}"><path d="{body}"/><path d="{neck}"/><path d="{head}"/></clipPath>')
    for p in (body, neck, head):
        out.append(f'<path d="{p}" fill="#ece5d6"/>')
    # Bone ochre touch on the flank
    out.append(f'<ellipse cx="450" cy="815" rx="70" ry="34" fill="{bone}" opacity="0.6" filter="url(#wash)"/>')
    # Cross-hatching inside the body, denser toward the belly
    hatch = []
    for k in range(-60, 90):
        x = 180 + k * 5
        hatch.append(f"M{x},740 l160,200")
        if k % 2 == 0:
            hatch.append(f"M{x + 120},850 l-120,110")
    out.append(f'<g clip-path="url(#{hatch_id})"><path d="{" ".join(hatch)}" stroke="{ink}" stroke-width="0.7" opacity="0.6"/>'
               f'<rect x="280" y="855" width="300" height="60" fill="{ink}" opacity="0.25"/></g>')
    for p in (body, neck, head):
        out.append(f'<path d="{p}" fill="none" stroke="{ink}" stroke-width="2.2" stroke-linejoin="round"/>')
    for x0, y0, x1, y1 in legs:
        out.append(f'<path d="M{x0},{y0} C{x0 - 2},{y0 + 50} {x1 + 4},{y1 - 50} {x1},{y1}" fill="none" stroke="{ink}" stroke-width="10" stroke-linecap="round"/>'
                   f'<path d="M{x1 - 5},{y1} l9,0" stroke="{ink}" stroke-width="4"/>')
    out.append(f'<path d="M 560,808 q 12,-4 16,8" stroke="{ink}" stroke-width="3" fill="none"/>')  # short tail
    out.append(f'<circle cx="222" cy="918" r="2.2" fill="{ink}"/>')  # eye

    # Antlers: two broad palms rising from the bowed head, wider than the body
    def palm(sx, sy, side):
        # Irish elk: a short beam, then a broad palm rising to the side,
        # with short curved tines along its outer rim
        bx, by = sx + side * 45, sy - 60
        tip_x, tip_y = sx + side * 160, sy - 185
        d = [f"M{sx},{sy}", f"C{sx + side * 10},{sy - 30} {bx - side * 20},{by + 15} {bx},{by}"]
        n = 7
        prev = (bx, by)
        for k in range(1, n + 1):
            t_ = k / n
            ex = bx + (tip_x - bx) * t_
            ey = by + (tip_y - by) * t_ - 22 * math.sin(math.pi * t_)
            mx, my = (prev[0] + ex) / 2, (prev[1] + ey) / 2
            ln = rng.uniform(24, 42)
            tx_, ty_ = mx + side * ln * 0.45, my - ln
            d.append(f"Q{f(mx - side * 4)},{f(my - ln * 0.4)} {f(tx_)},{f(ty_)} Q{f(mx + side * 8)},{f(my - ln * 0.3)} {f(ex)},{f(ey)}")
            prev = (ex, ey)
        lower = [(tip_x + side * 4, tip_y + 45), (bx + side * 95, by + 20), (bx + side * 25, by + 32)]
        d.append(" ".join(f"L{f(a)},{f(b)}" for a, b in lower))
        d.append(f"C{bx},{by + 40} {sx + side * 8},{sy - 18} {sx + side * 4},{sy + 4} Z")
        return " ".join(d)

    for side, sx, sy in [(-1, 222, 900), (1, 238, 897)]:
        d = palm(sx, sy, side)
        cid = f"palm{side + 1}"
        out.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
        lines = " ".join(f"M{x},{sy - 420} l0,460" for x in range(0, W, 4))
        out.append(f'<g clip-path="url(#{cid})"><rect width="{W}" height="{H}" fill="#e6dcc6"/>'
                   f'<path d="{lines}" stroke="{ink}" stroke-width="0.6" opacity="0.55"/></g>')
        out.append(f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="2" stroke-linejoin="round"/>')
    out.append('</g>')  # deer group
    out.append(plate_close())
    return svg("".join(out), PESS_PAPER)


# ---------------------------------------------------------------- helpers
# A small etching toolkit: shapes are point lists, tone is hatching clipped
# to the shape, washes are thin and clipped as well.

PAPER_FILL = "#efe9db"
INK = ETCH_INK
IX0, IY0, IX1, IY1 = IMAGE_BOX


def _smooth_d(pts, closed=True):
    n = len(pts)
    d = [f"M{f(pts[0][0])},{f(pts[0][1])}"]
    for i in range(n if closed else n - 1):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}")
    return " ".join(d) + (" Z" if closed else "")


def _poly_d(pts, closed=True):
    return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + (" Z" if closed else "")


def _bbox(pts, pad=3):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def ellipse_pts(cx, cy, rx, ry, n=20, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


class Etch:
    """Collects SVG elements; hands out unique ids."""

    def __init__(self, rng, tag="e"):
        self.rng, self.tag, self.n, self.out = rng, tag, 0, []

    def uid(self, p="c"):
        self.n += 1
        return f"{self.tag}{p}{self.n}"

    def add(self, s):
        self.out.append(s)

    def done(self):
        return "".join(self.out)

    # -- tone
    def hatch_d(self, d, bbox, angle, gap, op=0.6, w=0.7, sub=None, color=INK, jitter=0.6):
        """Parallel lines at angle (degrees) clipped to path d, optionally to a sub-rectangle."""
        x0, y0, x1, y1 = sub or bbox
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        R = math.hypot(x1 - x0, y1 - y0) / 2 + 4
        lines = []
        k = int(2 * R / gap) + 1
        for i in range(k):
            y = cy - R + i * gap
            lines.append(f"M{f(cx - R)},{f(y)} L{f(cx + R)},{f(y + self.rng.uniform(-jitter, jitter))}")
        cid = self.uid("h")
        s = f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">'
        if sub:
            sid = self.uid("s")
            s += f'<clipPath id="{sid}"><rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}"/></clipPath><g clip-path="url(#{sid})">'
        s += (f'<g transform="rotate({angle} {f(cx)} {f(cy)})"><path d="{" ".join(lines)}" stroke="{color}" '
              f'stroke-width="{w}" opacity="{op}" fill="none"/></g>')
        s += "</g>" if sub else ""
        s += "</g>"
        self.add(s)

    def clipped(self, d, inner):
        cid = self.uid("k")
        self.add(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{inner}</g>')

    def shape(self, pts, smooth=True, fill=PAPER_FILL, wash=None, wash_op=0.3, hatches=(), sw=1.8,
              outline=True, grain=0.0):
        d = _smooth_d(pts) if smooth else _poly_d(pts)
        bb = _bbox(pts)
        if fill:
            self.add(f'<path d="{d}" fill="{fill}"/>')
        if wash:
            self.clipped(d, f'<rect x="{f(bb[0])}" y="{f(bb[1])}" width="{f(bb[2] - bb[0])}" height="{f(bb[3] - bb[1])}" '
                            f'fill="{wash}" opacity="{wash_op}"/>')
        if grain:
            self.clipped(d, f'<rect x="{f(bb[0])}" y="{f(bb[1])}" width="{f(bb[2] - bb[0])}" height="{f(bb[3] - bb[1])}" '
                            f'filter="url(#aqua)" opacity="{grain}"/>')
        for h in hatches:
            angle, gap, op = h[0], h[1], h[2]
            sub = h[3] if len(h) > 3 else None
            w = h[4] if len(h) > 4 else 0.7
            self.hatch_d(d, bb, angle, gap, op, w, sub)
        if outline:
            self.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
        return d

    def wash(self, pts, color, op=0.3, filt="wash", smooth=True):
        d = _smooth_d(pts) if smooth else _poly_d(pts)
        self.add(f'<path d="{d}" fill="{color}" opacity="{op}" filter="url(#{filt})"/>')

    def line(self, pts, w=1.5, op=1.0, smooth=True, dash=None, color=INK, cap="round"):
        d = _smooth_d(pts, False) if smooth and len(pts) > 2 else _poly_d(pts, False)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" opacity="{op}" '
                 f'stroke-linecap="{cap}" stroke-linejoin="round"{da}/>')

    def limb(self, pts, w, fill=PAPER_FILL, taper=False):
        """A limb with an etched outline: wide ink stroke under a narrower paper stroke."""
        d = _smooth_d(pts, False) if len(pts) > 2 else _poly_d(pts, False)
        self.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(w + 3)}" stroke-linecap="round" stroke-linejoin="round"/>')
        self.add(f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{f(w)}" stroke-linecap="round" stroke-linejoin="round"/>')

    def grain(self, pts, op=0.8, smooth=True):
        d = _smooth_d(pts) if smooth else _poly_d(pts)
        bb = _bbox(pts)
        self.clipped(d, f'<rect x="{f(bb[0])}" y="{f(bb[1])}" width="{f(bb[2] - bb[0])}" height="{f(bb[3] - bb[1])}" '
                        f'filter="url(#aqua)" opacity="{op}"/>')

    def strokes(self, x0, y0, x1, y1, n, hmin, hmax, op=(0.3, 0.8), w=0.8, lean=5):
        """Short vertical etched strokes (grass, stubble, texture)."""
        r = self.rng
        d = []
        for _ in range(n):
            x, y = r.uniform(x0, x1), r.uniform(y0, y1)
            d.append(f"M{f(x)},{f(y)} l{f(r.uniform(-lean, lean))},{f(-r.uniform(hmin, hmax))}")
        self.add(f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width="{w}" opacity="{(op[0] + op[1]) / 2:.2f}" fill="none"/>')


def head(E, cx, cy, r, face="front", look=0.0, mouth=0.0, rot=0, bald=True, hat=None, f_dir=-1,
         brow=0.0, wash=None, hair=False, ears=False):
    """Head with etched outline. face: front (features shifted by look), back (hair mass)."""
    a = f' transform="rotate({rot} {f(cx)} {f(cy)})"' if rot else ""
    E.add(f"<g{a}>")
    if ears:
        for sg in (-1, 1):
            E.shape([(cx + sg * r * 0.85, cy - r * 0.1), (cx + sg * r * 1.45, cy - r * 0.75),
                     (cx + sg * r * 1.0, cy + r * 0.25)], smooth=False, sw=1.4)
    skull = ellipse_pts(cx, cy, r * 0.88, r, 16)
    if face == "back":
        E.shape(skull, fill="#d9d2c2", hatches=[(35, 2.2, 0.7), (-35, 2.6, 0.5)], sw=1.6)
    else:
        E.shape(skull, wash=wash, wash_op=0.25, hatches=[(60, 3, 0.45, (cx + r * 0.15, cy - r, cx + r, cy + r))], sw=1.6)
        ex = cx + look * r * 0.5
        ey = cy - r * 0.12 + brow * 0
        for sg in (-1, 1):
            E.line([(ex + sg * r * 0.38 - r * 0.15, ey), (ex + sg * r * 0.38 + r * 0.15, ey)], w=1.5, smooth=False)
            E.add(f'<circle cx="{f(ex + sg * r * 0.38)}" cy="{f(ey + r * 0.07)}" r="{f(max(1.0, r * 0.06))}" fill="{INK}"/>')
            if brow:
                E.line([(ex + sg * r * 0.5 - r * 0.2, ey - r * 0.2 - brow * r * 0.12 * sg * -1),
                        (ex + sg * r * 0.2, ey - r * 0.2 + brow * r * 0.1 * sg * -1)], w=1.2, smooth=False)
        E.line([(ex, ey + r * 0.1), (ex + look * r * 0.1 + r * 0.06, ey + r * 0.4)], w=1.2, smooth=False)
        my = cy + r * 0.55
        if mouth > 0:
            mw, mh = r * 0.42, r * 0.3 * mouth
            E.add(f'<ellipse cx="{f(ex)}" cy="{f(my)}" rx="{f(mw)}" ry="{f(mh)}" fill="{INK}"/>')
            E.add(f'<path d="M{f(ex - mw * 0.7)},{f(my - mh * 0.6)} h{f(mw * 1.4)}" stroke="{PAPER_FILL}" stroke-width="{f(r * 0.1)}"/>')
        else:
            E.line([(ex - r * 0.25, my), (ex + r * 0.25, my + 1)], w=1.3, smooth=False)
    if hair and face != "front":
        pass
    E.add("</g>")
    if hat:
        draw_hat(E, hat, cx, cy, r, f_dir)


def draw_hat(E, hat, cx, cy, r, f_dir=-1):
    fd = f_dir
    if hat == "top":
        E.shape(ellipse_pts(cx, cy - r * 0.78, r * 1.45, r * 0.24, 14), fill="#3a342e", sw=1.2)
        E.shape([(cx - r * 0.8, cy - r * 0.8), (cx - r * 0.72, cy - r * 2.4), (cx + r * 0.72, cy - r * 2.4), (cx + r * 0.8, cy - r * 0.8)],
                smooth=False, fill="#3a342e", sw=1.2)
        E.line([(cx - r * 0.45, cy - r * 2.2), (cx - r * 0.45, cy - r * 1.0)], w=0.8, op=0.5, color=PAPER_FILL, smooth=False)
    elif hat == "bonnet":
        E.shape([(cx - r * 1.05, cy + r * 0.3), (cx - r * 1.1, cy - r * 0.6), (cx - r * 0.4, cy - r * 1.35),
                 (cx + r * 0.5, cy - r * 1.25), (cx + r * 1.1, cy - r * 0.5), (cx + r * 1.0, cy + r * 0.4),
                 (cx + r * 0.6, cy + r * 0.1), (cx, cy - r * 0.5), (cx - r * 0.6, cy + r * 0.05)],
                fill="#e2dac8", hatches=[(70, 2.4, 0.6)], sw=1.4)
        E.line([(cx - r * 0.9, cy + r * 0.3), (cx - r * 0.8, cy + r * 1.1)], w=1.0, smooth=False)
        E.line([(cx + r * 0.9, cy + r * 0.3), (cx + r * 0.8, cy + r * 1.1)], w=1.0, smooth=False)
    elif hat == "wide":
        E.shape([(cx - r * 0.95, cy - r * 0.5), (cx - r * 0.7, cy - r * 1.35), (cx, cy - r * 1.6), (cx + r * 0.7, cy - r * 1.35), (cx + r * 0.95, cy - r * 0.5)],
                fill="#d9d2c2", hatches=[(80, 2.4, 0.6)], sw=1.4)
        E.shape(ellipse_pts(cx, cy - r * 0.5, r * 2.0, r * 0.38, 16), fill="#d9d2c2", hatches=[(10, 2.4, 0.6)], sw=1.5)
    elif hat == "phrygian":
        pts = [(-1.0, -0.1), (-1.0, -0.9), (-0.5, -1.6), (0.2, -1.95), (0.9, -1.8), (1.4, -1.35), (1.15, -1.2),
               (0.75, -1.45), (0.2, -1.2), (0.95, -0.7), (1.0, -0.2)]
        P = [(cx + fd * x * r, cy + y * r) for x, y in pts]
        E.shape(P, fill="#e7ddc6", hatches=[(75, 2.3, 0.6)], sw=1.5)


def person(E, x, base, h, garment="robe", hat=None, face="back", look=0.0, arms=(), wash=None, wash_op=0.3,
           lean=0.0, mouth=0.0, stride=0.05, f_dir=-1, brow=0.0, cloth=PAPER_FILL, legs=True):
    """A standing figure of height h with feet at (x, base). Arms are (side, elbow, hand) with
    elbow and hand as offsets from the shoulder in units of h. Returns head centre and shoulder y."""
    r = h * 0.085 if garment != "tunic" else h * 0.1
    hy = base - h + r
    shy = hy + r * 1.35
    sw = h * (0.12 if garment in ("cloak", "tunic") else 0.1 if garment == "crinoline" else 0.11)
    lx = lean * h
    hx = x + lx
    hatch_body = [(70, 2.6, 0.5), (-50, 3.4, 0.4, (x, shy, x + h, base))]
    if garment == "robe":
        hw = h * 0.17
        pts = [(hx - sw, shy), (hx, shy - 2), (hx + sw, shy), (x + sw * 1.25 + lx * 0.4, base - h * 0.5), (x + hw, base - 3),
               (x + hw * 0.3, base + 2), (x - hw * 0.3, base - 2), (x - hw, base), (x - sw * 1.25 + lx * 0.4, base - h * 0.5)]
    elif garment == "cloak":
        hw = h * 0.21
        pts = [(hx - sw, shy), (hx, shy - 3), (hx + sw, shy), (x + sw * 1.4 + lx * 0.4, base - h * 0.55), (x + hw, base - 3),
               (x + hw * 0.3, base + 2), (x - hw * 0.3, base - 3), (x - hw, base), (x - sw * 1.4 + lx * 0.4, base - h * 0.55)]
    elif garment == "crinoline":
        waist = base - h * 0.5
        pts = [(hx - sw, shy), (hx, shy - 2), (hx + sw, shy), (x + h * 0.055 + lx * 0.3, waist), (x + h * 0.2, base - h * 0.2),
               (x + h * 0.27, base - 2), (x, base + 3), (x - h * 0.27, base - 2), (x - h * 0.2, base - h * 0.2),
               (x - h * 0.055 + lx * 0.3, waist)]
        legs = False
    else:  # coat or tunic: body to the thigh, legs below
        hip = base - h * (0.4 if garment == "coat" else 0.42)
        hw = h * (0.13 if garment == "coat" else 0.15)
        pts = [(hx - sw, shy), (hx, shy - 2), (hx + sw, shy), (x + hw * 0.9 + lx * 0.3, hip - h * 0.1), (x + hw, hip),
               (x - hw, hip), (x - hw * 0.9 + lx * 0.3, hip - h * 0.1)]
    if legs and garment in ("coat", "tunic"):
        hip = base - h * (0.4 if garment == "coat" else 0.42)
        lw = max(3.0, h * (0.028 if garment == "coat" else 0.034))
        col = "#c9c1b0" if garment == "coat" else PAPER_FILL
        for sg in (-1, 1):
            E.limb([(x + sg * h * 0.05, hip), (x + sg * stride * h * 1.4, base - 4)], lw * 2, fill=col)
    d = E.shape(pts, fill=cloth, wash=wash, wash_op=wash_op, hatches=hatch_body, sw=1.8)
    # head
    if garment == "cloak":
        hood = [(hx - r * 1.35, hy + r * 0.9), (hx - r * 1.3, hy - r * 0.3), (hx, hy - r * 1.5), (hx + r * 1.3, hy - r * 0.3), (hx + r * 1.35, hy + r * 0.9)]
        E.shape(hood, fill=cloth, wash=wash, wash_op=wash_op, hatches=[(80, 2.4, 0.55)], sw=1.6)
    head(E, hx, hy, r, face=face, look=look, mouth=mouth, hat=hat, f_dir=f_dir, brow=brow)
    for side, elbow, hand in arms:
        sx, sy = hx + side * sw * 0.9, shy + h * 0.02
        pts_ = [(sx, sy), (sx + elbow[0] * h, sy + elbow[1] * h), (sx + hand[0] * h, sy + hand[1] * h)]
        E.limb(pts_, max(4, h * 0.035), fill=cloth if garment != "crinoline" else cloth)
        hxp, hyp = pts_[-1]
        E.add(f'<circle cx="{f(hxp)}" cy="{f(hyp)}" r="{f(max(2, h * 0.02))}" fill="{PAPER_FILL}" stroke="{INK}" stroke-width="1.2"/>')
    return hx, hy, shy


def grass_ground(E, y0, y1, density=1.0, x0=IX0, x1=IX1):
    n = int((y1 - y0) * (x1 - x0) / 330 * density)
    E.strokes(x0, y0 + 8, x1, y1, n, 4, 12, w=0.7)


def paper_wash(E, x0, y0, x1, y1, color, op, filt="softwash"):
    E.add(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{color}" opacity="{op}" filter="url(#{filt})"/>')


def line_hatch(E, x0, y0, x1, y1, gap, op=0.4, angle=0, w=0.6, color=INK):
    """Free hatching over a rectangle (no clip to a shape)."""
    d = f"M{f(x0)},{f(y0)} h{f(x1 - x0)} v{f(y1 - y0)} h{f(x0 - x1)} Z"
    E.hatch_d(d, (x0, y0, x1, y1), angle, gap, op, w, color=color)


# ------------------------------------------------------------------ cards

# ---- 0: The Unborn
def unborn(rng):
    bone, verd = WASH["bone"], WASH["verdigris"]
    E = Etch(rng, "u")
    E.add(plate_open())
    E.add(aquatint(0.5))
    # ground: bone wash with dry grass; bare paper above
    paper_wash(E, IX0 - 30, 770, IX1 + 30, IY1 + 20, bone, 0.4)
    line_hatch(E, IX0, 790, IX1, IY1, 7, op=0.18, angle=-2)
    grass_ground(E, 770, IY1, 1.1)
    # rose bushes along the back
    for bx, by, br in [(95, 790, 52), (190, 775, 40), (440, 780, 46), (540, 790, 58), (600, 775, 36), (500, 765, 30)]:
        pts = [(bx + br * math.cos(a) * (1 + rng.uniform(-0.15, 0.15)), by + br * 0.8 * math.sin(a) * (1 + rng.uniform(-0.15, 0.15)))
               for a in [i * math.pi / 5 for i in range(10)]]
        pts = [(x, min(y, by + 18)) for x, y in pts]
        E.shape(pts, fill="#e6dfcf", hatches=[(40, 2.8, 0.55), (-30, 3.6, 0.4)], sw=1.4, grain=0.6)
        for _ in range(int(br / 6)):
            rx, ry = bx + rng.uniform(-br * 0.8, br * 0.8), by + rng.uniform(-br * 0.6, br * 0.2)
            E.add(f'<circle cx="{f(rx)}" cy="{f(ry)}" r="{rng.uniform(3.5, 5.5):.1f}" fill="{PAPER_FILL}" stroke="{INK}" stroke-width="1"/>'
                  f'<path d="M{f(rx - 2)},{f(ry)} q2,-3 4,0" stroke="{INK}" stroke-width="0.7" fill="none"/>')
    # low stone spring between the figures
    sx, sy = 285, 770
    E.shape([(sx, sy), (sx + 110, sy), (sx + 118, sy + 46), (sx - 8, sy + 46)], smooth=False, fill="#e2dac8",
            hatches=[(0, 3, 0.35), (90, 14, 0.5)], wash=bone, wash_op=0.3, sw=2)
    E.shape(ellipse_pts(sx + 55, sy, 55, 10, 16), fill="#d4cdbd", hatches=[(0, 2.4, 0.5)], sw=1.6)
    E.line([(sx + 8, sy + 2), (sx + 40, sy - 3), (sx + 80, sy + 3), (sx + 102, sy)], w=0.8, op=0.7)

    # Silenus: seated, laughing, head thrown back
    # legs and lap first
    E.limb([(262, 955), (330, 925), (395, 985)], 30, fill="#e6dcc5")
    E.add(f'<ellipse cx="398" cy="990" rx="16" ry="9" fill="{PAPER_FILL}" stroke="{INK}" stroke-width="1.5"/>')
    belly = [(125, 905), (140, 840), (205, 815), (278, 845), (312, 915), (298, 985), (210, 1008), (140, 975)]
    E.shape(belly, fill=PAPER_FILL, wash=bone, wash_op=0.35,
            hatches=[(65, 2.8, 0.55), (-55, 3.6, 0.45, (215, 800, 330, 1020)), (10, 3, 0.35, (120, 920, 330, 1020))], sw=2.2, grain=0.5)
    E.shape(ellipse_pts(218, 940, 30, 36, 14), fill="#e6dfcf", hatches=[(80, 3, 0.5)], sw=1.2)  # belly curve
    E.add(f'<circle cx="222" cy="948" r="2.5" fill="{INK}"/>')  # navel
    # drapery over the lap
    E.shape([(150, 985), (210, 960), (290, 962), (345, 940), (365, 985), (330, 1008), (230, 1020), (150, 1012)],
            fill="#e3dac4", wash=bone, wash_op=0.5, hatches=[(20, 3.2, 0.5), (95, 8, 0.45)], sw=1.8)
    # arms: one hugging the belly, one flung up
    E.limb([(150, 860), (112, 905), (165, 935)], 22, fill="#e6dcc5")
    E.limb([(262, 842), (312, 800), (338, 745)], 20, fill="#e6dcc5")
    E.add(f'<circle cx="340" cy="740" r="10" fill="{PAPER_FILL}" stroke="{INK}" stroke-width="1.5"/>')
    # head, thrown back
    head(E, 205, 785, 50, mouth=2.0, look=0.0, rot=-14, wash=bone, ears=True, brow=-0.5)
    for k in range(13):  # shaggy beard strokes
        E.add(f'<path d="M{170 + k * 5.5},{826 + (k % 3) * 2} l{(k - 6) * 0.9},{16 - abs(k - 6) * 1.3 + (k % 2) * 4}" stroke="{INK}" stroke-width="1"/>')
    # vine wreath with a verdigris touch
    leaves = []
    for k in range(11):
        a = math.pi * (1.05 + 0.9 * k / 10)
        lx, ly = 205 + 54 * math.cos(a) - 6, 785 + 55 * math.sin(a) - 4
        leaves.append(f'<ellipse cx="{f(lx)}" cy="{f(ly)}" rx="9" ry="5" transform="rotate({int(math.degrees(a) + 90 + rng.uniform(-30, 30))} {f(lx)} {f(ly)})" '
                      f'fill="{verd}" fill-opacity="0.55" stroke="{INK}" stroke-width="1.1"/>')
    E.add("".join(leaves))
    E.add(f'<path d="M153,775 q52,-60 108,-8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    # empty cup beside him
    E.shape([(352, 1030), (400, 1030), (394, 1048), (376, 1054), (358, 1048)], fill="#e2dac8", hatches=[(70, 2.2, 0.6)], sw=1.7)
    E.line([(376, 1054), (376, 1068)], w=3, smooth=False)
    E.shape(ellipse_pts(376, 1070, 18, 4, 10), fill="#e2dac8", sw=1.4)
    E.shape(ellipse_pts(376, 1031, 24, 4, 10), fill="#bfb7a6", sw=1.2)

    # Midas: upright, narrow, recoiling to the right
    mx, mb, mh = 494, 1018, 420
    # spear
    E.line([(mx + 90, mb + 10), (mx + 74, 520)], w=3, smooth=False)
    E.shape([(mx + 74, 470), (mx + 84, 518), (mx + 74, 528), (mx + 64, 518)], smooth=False, fill="#cfc7b6", hatches=[(80, 2, 0.6)], sw=1.6)
    # shadow on the ground
    E.add(f'<ellipse cx="{mx - 30}" cy="{mb + 6}" rx="110" ry="9" fill="{INK}" opacity="0.2" filter="url(#wash)"/>')
    person(E, mx, mb, mh, garment="robe", hat="phrygian", face="front", look=-0.9, mouth=0.9, lean=0.07,
           wash=bone, wash_op=0.45, f_dir=-1, brow=1.2,
           arms=[(-1, (-0.13, -0.02), (-0.12, -0.2)), (1, (0.08, 0.12), (0.15, 0.04))])
    # open palm: small fingers
    hx_, hy_ = mx + 0.07 * mh - 0.9 * 0.11 * mh - 0.12 * mh, 1018 - mh + mh * 0.085 * 2.35 + mh * 0.02 - 0.2 * mh
    for k in range(4):
        E.line([(hx_ - 6 + k * 4, hy_ - 4), (hx_ - 8 + k * 5, hy_ - 16)], w=1.8, smooth=False)
    E.add(plate_close())
    return svg(E.done(), PESS_PAPER)


# ---- II: The First Illusion, Happiness Here
def shadow(E, x, base, length, w=7, dirn=-1, op=0.45):
    pts = [(x - 12, base), (x + dirn * length, base + 5), (x + dirn * (length + 10), base + w + 5), (x + 12, base + w)]
    E.shape(pts, smooth=False, fill="#d6cfbf", hatches=[(0, 2.2, 0.7)], outline=False)


def happiness_here(rng):
    bone, verd = WASH["bone"], WASH["verdigris"]
    E = Etch(rng, "a")
    E.add(plate_open())
    E.add(aquatint(0.5))
    # garden wall
    E.shape([(IX0 - 5, 600), (IX1 + 5, 600), (IX1 + 5, 735), (IX0 - 5, 735)], smooth=False, fill="#e8e1d0", wash=bone, wash_op=0.3,
            hatches=[(0, 5, 0.3), (90, 22, 0.35)], sw=2, grain=0.5)
    for k in range(IX0, IX1, 44):
        E.line([(k, 600), (k, 735)], w=0.7, op=0.5, smooth=False)
    E.shape([(IX0 - 5, 590), (IX1 + 5, 590), (IX1 + 5, 604), (IX0 - 5, 604)], smooth=False, fill="#ded6c4", sw=1.6)
    # ground and gravel path
    paper_wash(E, IX0 - 30, 735, IX1 + 30, IY1 + 20, bone, 0.4)
    E.shape([(250, 735), (430, 735), (610, 1086), (70, 1086)], smooth=False, fill=None, wash=bone, wash_op=0.18,
            hatches=[(0, 5, 0.18)], outline=False)
    E.strokes(IX0, 740, IX1, IY1, 700, 1.5, 4, w=0.8, lean=3)
    # cypress at the right edge
    cy_pts = [(545, 885), (536, 700), (550, 500), (576, 250), (600, 500), (614, 700), (606, 885)]
    E.shape(cy_pts, fill="#dcd6c2", wash=verd, wash_op=0.5, hatches=[(88, 2.4, 0.7), (60, 4, 0.4)], sw=1.8, grain=0.6)
    # stone herm
    E.shape([(480, 880), (480, 860), (492, 850), (498, 690), (545, 690), (550, 850), (562, 860), (562, 880)], smooth=False, fill="#e8e1d0",
            wash=bone, wash_op=0.4, hatches=[(90, 3.2, 0.5), (0, 8, 0.3)], sw=2)
    head(E, 521, 650, 28, face="front", look=0.0, wash=bone)
    E.shape([(493, 622), (521, 600), (549, 622), (549, 640), (493, 640)], smooth=False, fill="#d9d2c2", hatches=[(80, 2.2, 0.6)], sw=1.4)
    E.line([(494, 666), (548, 666)], w=0.8, smooth=False)
    # fountain with a hairline crack
    E.shape([(150, 910), (150, 868), (166, 862), (166, 820), (192, 820), (192, 862), (208, 868), (208, 910)], smooth=False, fill="#e2dac8",
            hatches=[(90, 3, 0.5)], wash=bone, wash_op=0.4, sw=1.8)
    E.shape([(70, 800), (100, 836), (150, 856), (200, 856), (252, 836), (282, 800)], fill="#e8e1d0", wash=bone, wash_op=0.35,
            hatches=[(70, 3, 0.45, (160, 800, 290, 870))], sw=2)
    E.shape(ellipse_pts(176, 800, 106, 22, 24), fill="#cfc7b6", hatches=[(0, 2.4, 0.55)], sw=2)
    E.shape(ellipse_pts(176, 802, 92, 15, 24), fill="#c4bdad", hatches=[(0, 2, 0.5)], sw=1.2)
    E.line([(232, 806), (236, 822), (230, 836), (234, 852)], w=0.8, op=0.9)  # hairline crack
    # long shadows, light low from the right
    for sx, sb, ln in [(330, 880, 100), (205, 985, 150), (290, 988, 120), (410, 1042, 190), (480, 1012, 180)]:
        shadow(E, sx, sb, ln)
    shadow(E, 521, 880, 170, w=6)
    shadow(E, 575, 888, 160, w=5)

    kid = dict(garment="tunic", face="front", wash=bone, wash_op=0.4, cloth="#e9e1cf")
    # blower, behind the others
    person(E, 330, 880, 170, look=0.0, arms=[(-1, (-0.08, 0.1), (-0.04, -0.12)), (1, (0.12, 0.0), (0.14, -0.08))], **kid)
    E.line([(317, 770), (306, 784)], w=2, smooth=False)
    # bubble: bare paper with a ring and a highlight
    E.add(f'<circle cx="338" cy="575" r="38" fill="#fbf8f0" fill-opacity="0.55" stroke="{INK}" stroke-width="1.2"/>')
    E.add(f'<circle cx="338" cy="575" r="38" fill="none" stroke="{WASH["slate"]}" stroke-width="3" opacity="0.18"/>')
    E.add(f'<path d="M314,562 q8,-16 26,-18" stroke="#fff" stroke-width="5" fill="none" opacity="0.9"/>')
    E.add(f'<path d="M315,562 q8,-16 26,-18" stroke="{INK}" stroke-width="0.7" fill="none"/>')
    for k, (bx, by, br) in enumerate([(348, 700, 7), (330, 660, 4)]):
        E.add(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    # wreath: a kneeling child crowns a smaller one
    person(E, 140, 985, 125, look=0.4, legs=False, arms=[(1, (0.14, -0.08), (0.24, -0.26)), (-1, (0.1, 0.12), (0.2, 0.06))], **kid)
    E.limb([(120, 975), (180, 985), (205, 982)], 18, fill="#e9e1cf")
    person(E, 215, 990, 112, look=-0.3, arms=[(1, (0.12, 0.1), (0.1, 0.22)), (-1, (-0.1, 0.1), (-0.08, 0.2))], **kid)
    E.add(f'<ellipse cx="215" cy="{990 - 112 + 9}" rx="19" ry="6" fill="none" stroke="{verd}" stroke-width="4" opacity="0.7"/>'
          f'<ellipse cx="215" cy="{990 - 112 + 9}" rx="19" ry="6" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 2"/>')
    # hoop and its chasers
    E.add(f'<ellipse cx="318" cy="1020" rx="30" ry="46" fill="none" stroke="{INK}" stroke-width="5"/>'
          f'<ellipse cx="318" cy="1020" rx="30" ry="46" fill="none" stroke="{PAPER_FILL}" stroke-width="2"/>')
    person(E, 415, 1042, 222, look=-0.8, stride=0.09, lean=-0.03, arms=[(-1, (-0.1, 0.08), (-0.19, 0.0)), (1, (0.1, 0.08), (0.14, 0.18))], **kid)
    person(E, 490, 1015, 210, look=-0.8, stride=0.1, lean=-0.03, arms=[(-1, (-0.1, 0.1), (-0.17, 0.04)), (1, (0.1, 0.0), (0.16, -0.06))], **kid)
    E.add(plate_close())
    return svg(E.done(), PESS_PAPER)


# ---- III: The Second Illusion, Happiness Hereafter
def happiness_hereafter(rng):
    bone, slate = WASH["bone"], WASH["slate"]
    E = Etch(rng, "b")
    E.add(plate_open())
    E.add(aquatint(0.5))
    # slate sky, heavier toward the top
    paper_wash(E, IX0 - 30, IY0 - 30, IX1 + 30, 700, slate, 0.15)
    paper_wash(E, IX0 - 30, IY0 - 30, IX1 + 30, 330, slate, 0.12)
    line_hatch(E, IX0, IY0, IX1, 700, 8, op=0.14, angle=-2)
    line_hatch(E, IX0, IY0, IX1, 340, 5, op=0.16, angle=-2)
    for _ in range(26):  # drifting cloud strokes in the sky
        cx_, cy_ = rng.uniform(IX0 + 40, IX1 - 40), rng.uniform(110, 700)
        ln = rng.uniform(50, 130)
        E.add(f'<path d="M{f(cx_)},{f(cy_)} q{f(ln / 2)},{f(-rng.uniform(6, 14))} {f(ln)},0" stroke="{INK}" stroke-width="0.9" opacity="0.4" fill="none"/>')
    # mask: city thins toward the left and along its base, with gaps in the stonework
    holes = [(165, 440, 70, 80), (215, 360, 55, 55), (190, 300, 35, 30), (250, 515, 110, 40), (400, 525, 120, 45), (340, 548, 160, 40),
             (338, 330, 12, 26), (270, 470, 20, 18), (445, 390, 10, 22), (300, 400, 16, 14), (500, 470, 25, 25), (232, 285, 10, 16)]
    mk = "".join(f'<ellipse cx="{a}" cy="{b}" rx="{c}" ry="{d}" fill="#000" filter="url(#wash)"/>' for a, b, c, d in holes)
    E.add(f'<mask id="citymask" maskUnits="userSpaceOnUse" x="{IX0}" y="{IY0}" width="{IX1 - IX0}" height="{IY1 - IY0}">'
          f'<rect x="{IX0}" y="{IY0}" width="{IX1 - IX0}" height="{IY1 - IY0}" fill="#fff"/>{mk}</mask><g mask="url(#citymask)">')

    def tower(x, top, w, spire, bot=530, bone_top=False):
        body = [(x - w / 2, spire + 0), (x + w / 2, spire + 0), (x + w / 2, bot), (x - w / 2, bot)]
        E.shape(body, smooth=False, fill="#ece5d6", hatches=[(90, 2.6, 0.55, (x, top, x + w, bot)), (0, 9, 0.35)], sw=2, grain=0.5)
        E.shape([(x - w / 2 - 6, spire), (x, top), (x + w / 2 + 6, spire)], smooth=False, fill="#e0d8c6",
                wash=bone if bone_top else None, wash_op=0.6, hatches=[(90, 2.4, 0.6, (x, top, x + w, spire))], sw=2)
        for wy in range(spire + 30, bot - 60, 55):
            E.add(f'<path d="M{x - 4},{wy + 18} v-12 a4,4 0 0 1 8,0 v12 Z" fill="{INK}"/>')
    # walls first, towers over them
    E.shape([(160, 400), (520, 400), (520, 530), (160, 530)], smooth=False, fill="#ece5d6",
            hatches=[(0, 6, 0.3), (90, 16, 0.35), (90, 2.8, 0.4, (340, 400, 520, 530))], sw=2, grain=0.5)
    for k in range(166, 516, 18):
        E.shape([(k, 400), (k, 388), (k + 10, 388), (k + 10, 400)], smooth=False, fill="#ece5d6", sw=1.4)
    tower(230, 215, 50, 300)
    tower(450, 200, 50, 290, bone_top=True)
    tower(170, 310, 36, 360)
    tower(510, 295, 36, 350)
    tower(340, 120, 76, 240, bone_top=True)
    # gate
    E.add(f'<path d="M316,530 v-52 a24,24 0 0 1 48,0 v52 Z" fill="{INK}" opacity="0.85"/>')
    E.add(f'<path d="M322,530 v-48 a18,18 0 0 1 36,0 v48 Z" fill="#cfc7b6"/>')
    E.add("</g>")
    # cloud banks under the city
    for k, cx_ in enumerate(range(130, 600, 62)):
        cyy = 565 + (k % 2) * 18 + rng.uniform(-6, 6)
        E.shape(ellipse_pts(cx_, cyy, rng.uniform(68, 86), rng.uniform(34, 46), 16), fill="#f0ebdd", wash=slate, wash_op=0.12,
                hatches=[(0, 3.4, 0.4, (cx_ - 90, cyy + 8, cx_ + 90, cyy + 60))], sw=1.4, grain=0.3)
    paper_wash(E, IX0 - 20, 610, IX1 + 20, 780, slate, 0.16)
    line_hatch(E, IX0, 620, IX1, 770, 9, op=0.16, angle=-1)
    # rocky path
    E.shape([(IX0 - 5, 900), (180, 880), (330, 905), (470, 890), (IX1 + 5, 915), (IX1 + 5, IY1 + 5), (IX0 - 5, IY1 + 5)], smooth=False,
            fill="#e4ddcc", wash=slate, wash_op=0.22, hatches=[(30, 4, 0.35), (-40, 6, 0.3)], sw=1.8, grain=0.8)
    for rx_, ry_, rw, rh in [(120, 900, 70, 40), (500, 905, 80, 45), (300, 930, 40, 22), (580, 1010, 60, 50), (100, 1050, 70, 40)]:
        E.shape(ellipse_pts(rx_, ry_ + rh, rw, rh, 9), fill="#ddd6c4", wash=slate, wash_op=0.25,
                hatches=[(50, 3, 0.55), (-20, 4, 0.4)], sw=1.8)
    # pilgrims, mostly from behind, faces and hands turned up
    cl = dict(garment="cloak", face="back", hat="wide", wash=slate, wash_op=0.22, cloth="#e8e2d2")
    spots = [(250, 965, 150, -0.0), (330, 1000, 160, 0.01), (410, 960, 145, 0.0), (180, 1025, 165, 0.0), (480, 1030, 170, 0.0), (545, 975, 140, 0.0)]
    for i, (px, pb, ph, ln) in enumerate(spots):
        up = 1 if i % 2 == 0 else -1
        arms = [(up, (0.05 * up, -0.1), (0.07 * up, -0.28))]
        if i in (1, 4):
            arms = [(1, (0.05, -0.1), (0.07, -0.28)), (-1, (-0.05, -0.1), (-0.07, -0.28))]
        # staff
        E.line([(px + 0.19 * ph, pb + 6), (px + 0.19 * ph + 4, pb - ph * 1.1)], w=2.6, smooth=False)
        person(E, px, pb, ph, arms=arms, lean=0.0, **cl)
        # scallop shell on the shoulder
        sx_, sy_ = px - 0.14 * ph, pb - ph * 0.7
        E.shape([(sx_, sy_ + 9), (sx_ - 9, sy_), (sx_ - 4, sy_ - 6), (sx_ + 4, sy_ - 6), (sx_ + 9, sy_)], smooth=False,
                fill=PAPER_FILL, wash=bone, wash_op=0.6, hatches=[(90, 2, 0.8)], sw=1.1)
    E.add(plate_close())
    return svg(E.done(), PESS_PAPER)


# ---- IV: The Third Illusion, Progress
def progress(rng):
    bone, caput = WASH["bone"], WASH["caput"]
    E = Etch(rng, "p")
    E.add(plate_open())
    E.add(aquatint(0.5))
    VX, VY = 420, 470
    # sky: bone at the horizon, bare paper above
    paper_wash(E, IX0 - 30, 330, IX1 + 30, 500, bone, 0.5)
    # plain, hatched finer toward the horizon
    paper_wash(E, IX0 - 30, VY, IX1 + 30, IY1 + 20, bone, 0.12)
    y = VY
    while y < IY1:
        gap = 3 + (y - VY) / 40
        line_hatch(E, IX0, y, IX1, min(y + 60, IY1), gap, op=0.3, angle=0, w=0.6)
        y += 60

    def road_x(s_):
        return VX - (VX - 70) * s_, VX + 6 + (500 - VX - 6) * s_

    # railway tracks converging to the vanishing point, one each side of the road
    for xs in [(95, 135), (180, 215), (545, 590), (470, 505)]:
        for xx in xs:
            E.line([(xx, 780), (VX + (xx - VX) * 0.05, VY + 12)], w=1.0, op=0.7, smooth=False)
        for t in [0.08, 0.2, 0.34, 0.5, 0.7, 0.9]:
            yy = VY + 12 + (780 - VY - 12) * t
            xa = VX + (xs[0] - VX) * (0.05 + 0.95 * t)
            xb = VX + (xs[1] - VX) * (0.05 + 0.95 * t)
            E.line([(xa - 3, yy), (xb + 3, yy)], w=0.8, op=0.6, smooth=False)
    # embankments
    for ey, eh, op in [(458, 8, 0.35), (472, 12, 0.5)]:
        E.shape([(IX0 - 5, ey), (IX1 + 5, ey), (IX1 + 5, ey + eh), (IX0 - 5, ey + eh)], smooth=False, fill="#e2dac8",
                hatches=[(0, 2.2, op)], sw=1.0, grain=0.6)
    # factory rows, far to near; each row fainter and smaller
    rows = [(462, 0.4, 0.3, 14), (470, 0.65, 0.45, 11), (483, 1.0, 0.6, 8)]
    for by, sc, op, cnt in rows:
        xs = sorted(rng.uniform(IX0, IX1) for _ in range(cnt))
        for x in xs:
            w = 9 * sc + 3
            h = rng.uniform(70, 140) * sc
            # factory block with saw-tooth roof
            bw = rng.uniform(40, 80) * sc + 10
            bh = rng.uniform(14, 26) * sc + 4
            E.add(f'<g opacity="{op + 0.2:.2f}">')
            E.shape([(x - bw, by), (x - bw, by - bh), (x - bw / 2, by - bh - 5 * sc), (x - bw / 2, by - bh), (x, by - bh - 5 * sc),
                     (x, by - bh), (x + bw / 2, by - bh - 5 * sc), (x + bw / 2, by), ], smooth=False, fill="#e0d8c6",
                    hatches=[(90, 2, 0.6)], sw=0.9)
            cx0 = x + bw * 0.8
            E.shape([(cx0 - w / 2 - 1, by), (cx0 - w / 2 + 1, by - h), (cx0 + w / 2 - 1, by - h), (cx0 + w / 2 + 1, by)], smooth=False,
                    fill="#e0d8c6", hatches=[(90, 1.8, 0.7)], sw=1.0)
            E.add("</g>")
            # smoke, drifting right
            for k in range(4):
                E.add(f'<ellipse cx="{f(cx0 + k * 20 * sc * 1.4)}" cy="{f(by - h - k * 22 * sc - 6)}" rx="{f((14 + k * 9) * sc * 1.3)}" '
                      f'ry="{f((10 + k * 5) * sc * 1.3)}" fill="{caput}" opacity="{0.2 * (0.6 + op):.2f}" filter="url(#softwash)"/>')
    # small train on the far embankment
    tx, ty = 520, 459
    E.add(f'<g opacity="0.8"><rect x="{tx}" y="{ty - 7}" width="14" height="7" fill="{INK}"/><rect x="{tx + 2}" y="{ty - 12}" width="3" height="5" fill="{INK}"/>')
    for k in range(5):
        E.add(f'<rect x="{tx + 16 + k * 12}" y="{ty - 6}" width="10" height="6" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    E.add('</g>')
    E.add(f'<ellipse cx="{tx + 12}" cy="{ty - 24}" rx="14" ry="7" fill="{caput}" opacity="0.2" filter="url(#wash)"/>')
    # grain thickening toward the horizon
    E.add('<linearGradient id="hzgrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
          '<stop offset="0.65" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
          f'<mask id="hzmask"><rect x="{IX0}" y="250" width="{IX1 - IX0}" height="300" fill="url(#hzgrad)"/></mask>'
          f'<rect x="{IX0}" y="250" width="{IX1 - IX0}" height="300" filter="url(#aqua)" mask="url(#hzmask)" opacity="0.9"/>')
    # the road
    lx0, rx0 = road_x(1.0)
    E.shape([(VX - 3, VY + 4), (VX + 7, VY + 4), (rx0, IY1 + 10), (lx0, IY1 + 10)], smooth=False, fill=None, wash=caput, wash_op=0.14,
            hatches=[(0, 3.5, 0.2)], sw=1.4)
    E.line([(VX - 3, VY + 4), (lx0, IY1 + 10)], w=1.2, smooth=False)
    E.line([(VX + 7, VY + 4), (rx0, IY1 + 10)], w=1.2, smooth=False)
    # procession, far to near
    crowd = [(0.4, 0.5, "leader")]
    for i in range(14):
        s_ = 0.47 + 0.43 * i / 13 + rng.uniform(-0.01, 0.01)
        u = [0.12, 0.5, 0.88, 0.3, 0.7][i % 5] + rng.uniform(-0.04, 0.04)
        crowd.append((s_, u, "man" if i % 3 != 1 else "lady"))
    crowd.sort(key=lambda c: c[0])
    for s_, u, kind in crowd:
        l_, r_ = road_x(s_)
        px, pb = l_ + u * (r_ - l_), VY + 616 * s_
        h = 330 * s_
        coat = dict(face="back", wash=caput, wash_op=0.5, cloth="#dcd4c2", stride=0.07, lean=0.0)
        if kind == "lady":
            person(E, px, pb, h, garment="crinoline", hat="bonnet", arms=[(1, (0.04, 0.1), (0.07, 0.2))], **{k: v for k, v in coat.items() if k != "stride"})
        elif kind == "leader":
            px_, py_, sy_ = person(E, px, pb, h, garment="coat", hat="top", arms=[(1, (0.1, -0.02), (0.14, -0.14))], **coat)
            ph_ = px + 0.1 * h + 0.14 * h
            ptop = pb - h * 1.55
            E.line([(ph_ + 2, pb - h * 0.2), (ph_ + 2, ptop)], w=2.4, smooth=False)
            E.shape([(ph_ + 2, ptop), (ph_ + 70 * s_ * 2, ptop + 12 * s_ * 2), (ph_ + 2, ptop + 30 * s_ * 2)], smooth=False,
                    fill="#e8e1d0", hatches=[(0, 3, 0.4)], sw=1.4)
        else:
            person(E, px, pb, h, garment="coat", hat="top", arms=[(-1, (-0.04, 0.12), (-0.05, 0.25))], **coat)
    E.add(plate_close())
    return svg(E.done(), PESS_PAPER)


# ---- V: Vanity
def vanity(rng):
    bone, slate = WASH["bone"], WASH["slate"]
    E = Etch(rng, "v")
    E.add(plate_open())
    E.add(aquatint(0.45))
    paper_wash(E, IX0 - 30, IY0 - 30, IX1 + 30, 820, bone, 0.28)
    line_hatch(E, IX0, IY0, IX1, 800, 9, op=0.16, angle=90, w=0.6)
    # window at upper right: the sun is bare paper with fine rays
    wx0, wy0, wx1, wy1 = 395, 130, 590, 480
    E.shape([(wx0 - 14, wy0 - 14), (wx1 + 14, wy0 - 14), (wx1 + 14, wy1 + 14), (wx0 - 14, wy1 + 14)], smooth=False, fill="#e6dfcf",
            hatches=[(90, 3, 0.4)], sw=2.4)
    op_pts = [(wx0, wy0), (wx1, wy0), (wx1, wy1), (wx0, wy1)]
    E.shape(op_pts, smooth=False, fill="#f6f2e6", sw=1.6)
    sun = (505, 410)
    for yy in range(wy0 + 2, wy1, 5):
        t = max(0.0, 1 - math.hypot(0, yy - sun[1]) / 280)
        E.add(f'<path d="M{wx0},{yy} H{wx1}" stroke="{INK}" stroke-width="0.7" opacity="{0.55 * (1 - t) ** 1.3:.2f}"/>')
    E.add(f'<clipPath id="vwin"><rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}"/></clipPath><g clip-path="url(#vwin)">')
    for k in range(36):
        a = 2 * math.pi * k / 36
        E.add(f'<path d="M{f(sun[0] + 38 * math.cos(a))},{f(sun[1] + 38 * math.sin(a))} L{f(sun[0] + (120 + 40 * (k % 3)) * math.cos(a))},'
              f'{f(sun[1] + (120 + 40 * (k % 3)) * math.sin(a))}" stroke="{INK}" stroke-width="0.6" opacity="0.5"/>')
    E.add(f'<circle cx="{sun[0]}" cy="{sun[1]}" r="32" fill="#fcfaf3" stroke="{INK}" stroke-width="0.8" opacity="1"/>')
    # distant low hills
    E.shape([(wx0, 438), (440, 430), (480, 440), (530, 432), (wx1, 440), (wx1, wy1), (wx0, wy1)], fill="#e2dac8", hatches=[(0, 2.4, 0.6)], sw=1.2)
    E.add("</g>")
    # open sash, swung inward at left
    E.shape([(wx0 - 4, wy0 - 6), (wx0 + 52, wy0 + 20), (wx0 + 52, wy1 - 25), (wx0 - 4, wy1 + 6)], smooth=False, fill="#ece5d6",
            hatches=[(90, 2.6, 0.45)], sw=2)
    E.line([(wx0 + 24, wy0 + 6), (wx0 + 24, wy1 - 10)], w=1.2, smooth=False)
    E.line([(wx0 - 4, 300), (wx0 + 52, 290)], w=1.2, smooth=False)
    # slate shadow in the window reveal
    E.shape([(wx0 - 14, wy0 - 14), (wx0 + 8, wy0 + 6), (wx0 + 8, wy1 - 6), (wx0 - 14, wy1 + 14)], smooth=False, fill=None, wash=slate,
            wash_op=0.5, hatches=[(80, 2, 0.7)], outline=False)
    E.shape([(wx0 - 28, wy1 + 14), (wx1 + 28, wy1 + 14), (wx1 + 22, wy1 + 30), (wx0 - 22, wy1 + 30)], smooth=False, fill="#e2dac8",
            hatches=[(0, 2.4, 0.5)], sw=2)
    # table: top surface and front face
    E.shape([(IX0 - 5, 808), (IX1 + 5, 808), (IX1 + 5, 985), (IX0 - 5, 985)], smooth=False, fill="#e8e0cc", wash=bone, wash_op=0.45,
            hatches=[(0, 5, 0.3), (0, 11, 0.3)], sw=2, grain=0.6)
    E.shape([(IX0 - 5, 985), (IX1 + 5, 985), (IX1 + 5, IY1 + 5), (IX0 - 5, IY1 + 5)], smooth=False, fill="#ddd4be", wash=bone, wash_op=0.35,
            hatches=[(0, 3, 0.55), (0, 7, 0.3)], sw=2, grain=0.8)
    for k in range(5):
        yy = 820 + k * 34 + rng.uniform(-4, 4)
        E.line([(IX0, yy), (250 + rng.uniform(-30, 30), yy + 3), (IX1, yy - 2)], w=0.8, op=0.5)
    E.add(f'<rect x="{IX0}" y="800" width="{IX1 - IX0}" height="10" fill="{INK}" opacity="0.25" filter="url(#wash)"/>')

    def cast(pts):
        E.shape(pts, smooth=False, fill=None, wash=INK, wash_op=0.18, hatches=[(-4, 2.2, 0.7)], outline=False)

    # shadows toward the lower left (light from the sun at upper right)
    cast([(425, 892), (475, 892), (360, 925), (255, 935)])
    cast([(285, 895), (370, 895), (250, 930), (140, 940)])
    cast([(190, 897), (245, 897), (150, 925), (95, 925)])
    # leaning spade at the left wall
    E.line([(108, 330), (136, 820)], w=11, smooth=False, color=INK)
    E.line([(108, 330), (136, 820)], w=6, smooth=False, color="#e4dcc8")
    E.shape([(88, 320), (130, 320), (130, 336), (88, 336)], smooth=False, fill="#e4dcc8", sw=1.6)
    E.shape([(118, 800), (165, 806), (170, 868), (146, 896), (116, 868)], fill="#d8d0be", hatches=[(70, 2.4, 0.7), (-20, 3, 0.4)],
            wash=slate, wash_op=0.18, sw=2, grain=0.4)
    # candlestick, snuffed
    cx0 = 215
    E.shape(ellipse_pts(cx0, 892, 44, 10, 14), fill="#e4d4a8", wash=bone, wash_op=0.7, hatches=[(0, 2.2, 0.5)], sw=1.8)
    E.shape([(cx0 - 9, 886), (cx0 - 6, 845), (cx0 + 6, 845), (cx0 + 9, 886)], smooth=False, fill="#e4d4a8", wash=bone, wash_op=0.7,
            hatches=[(90, 2, 0.6, (cx0, 840, cx0 + 12, 890))], sw=1.8)
    E.shape([(cx0 - 15, 846), (cx0 - 11, 828), (cx0 + 11, 828), (cx0 + 15, 846)], smooth=False, fill="#e4d4a8", wash=bone, wash_op=0.7,
            hatches=[(90, 2, 0.6, (cx0, 826, cx0 + 16, 848))], sw=1.8)
    E.shape([(cx0 - 8, 830), (cx0 - 8, 770), (cx0 + 8, 770), (cx0 + 8, 830)], smooth=False, fill="#f4efe0",
            hatches=[(90, 2.4, 0.5, (cx0, 770, cx0 + 10, 830))], sw=1.6)
    E.add(f'<path d="M{cx0},770 v-8" stroke="{INK}" stroke-width="2"/>')
    smoke = [(cx0, 760)]
    for k in range(1, 12):
        smoke.append((cx0 + math.sin(k * 0.9) * (6 + k * 2.5), 760 - k * 22))
    E.line(smoke, w=1.1, op=0.75)
    E.line([(smoke[i][0] + 3, smoke[i][1]) for i in range(0, 8)], w=0.6, op=0.4)
    # skull
    sx, sy = 330, 835
    E.shape([(sx - 62, sy + 5), (sx - 60, sy - 38), (sx - 30, sy - 62), (sx + 8, sy - 66), (sx + 46, sy - 50), (sx + 62, sy - 14),
             (sx + 58, sy + 22), (sx + 40, sy + 36), (sx - 40, sy + 36)], fill="#ece3cc", wash=bone, wash_op=0.45,
            hatches=[(60, 2.2, 0.6, (sx - 70, sy - 70, sx - 8, sy + 40)), (-30, 3, 0.35, (sx - 70, sy - 10, sx + 70, sy + 40))], sw=2.2, grain=0.5)
    E.shape([(sx - 38, sy + 30), (sx - 34, sy + 70), (sx - 16, sy + 76), (sx + 16, sy + 76), (sx + 34, sy + 70), (sx + 38, sy + 30)],
            fill="#e2d8c0", wash=bone, wash_op=0.45, hatches=[(60, 2.2, 0.5, (sx - 40, sy + 30, sx, sy + 80))], sw=2)
    for ex_ in (-27, 27):
        E.shape(ellipse_pts(sx + ex_, sy + 2, 18, 20, 12), fill=INK, sw=1.6)
    E.shape([(sx, sy + 20), (sx - 10, sy + 42), (sx - 4, sy + 46), (sx, sy + 40), (sx + 4, sy + 46), (sx + 10, sy + 42)], smooth=False, fill=INK, sw=1)
    for k in range(-4, 5):
        E.line([(sx + k * 8, sy + 54), (sx + k * 8, sy + 72)], w=1.2, smooth=False)
    E.line([(sx - 33, sy + 54), (sx + 33, sy + 54)], w=1.2, smooth=False)
    E.line([(sx - 50, sy + 16), (sx - 38, sy + 40)], w=1.2, op=0.8)
    E.line([(sx + 50, sy + 16), (sx + 38, sy + 40)], w=1.2, op=0.8)
    E.line([(sx - 44, sy - 38), (sx - 14, sy - 52), (sx + 12, sy - 52)], w=1.0, op=0.55)
    # hourglass
    hx = 455
    for gx in (-26, 26):
        E.shape([(hx + gx - 3, 765), (hx + gx + 3, 765), (hx + gx + 3, 893), (hx + gx - 3, 893)], smooth=False, fill="#e2d8c0", hatches=[(90, 1.6, 0.6)], sw=1.4)
    top = [(hx - 22, 768), (hx + 22, 768), (hx + 20, 800), (hx + 4, 828), (hx + 4, 832), (hx - 4, 832), (hx - 4, 828), (hx - 20, 800)]
    bot = [(hx - 4, 832), (hx + 4, 832), (hx + 20, 860), (hx + 22, 892), (hx - 22, 892), (hx - 20, 860)]
    E.shape(top, fill="#f6f2e6", sw=1.6)
    E.shape(bot, fill="#f6f2e6", sw=1.6)
    E.shape([(hx - 17, 892), (hx + 17, 892), (hx + 14, 868), (hx + 3, 852), (hx - 3, 852), (hx - 14, 868)], smooth=False, fill=bone, sw=0.8)
    E.shape([(hx - 15, 770), (hx + 15, 770), (hx + 8, 786), (hx - 8, 786)], smooth=False, fill=bone, sw=0.8)
    E.line([(hx, 832), (hx, 855)], w=0.8, smooth=False)
    for yy, hh in ((755, 12), (893, 12)):
        E.shape([(hx - 40, yy), (hx + 40, yy), (hx + 40, yy + hh), (hx - 40, yy + hh)], smooth=False, fill="#d8ccae",
                hatches=[(0, 2, 0.6)], wash=bone, wash_op=0.4, sw=2)
    # ledger, closed, lying flat; no text
    E.shape([(498, 880), (596, 880), (608, 915), (486, 915)], smooth=False, fill="#e0d4b8", wash=bone, wash_op=0.3,
            hatches=[(-8, 4, 0.35)], sw=2)
    E.shape([(486, 915), (608, 915), (608, 930), (486, 930)], smooth=False, fill="#f0eadb", hatches=[(0, 1.6, 0.6)], sw=1.8)
    E.line([(510, 886), (590, 886), (600, 908)], w=0.8, op=0.6, smooth=False)
    # compasses in front
    E.limb([(262, 948), (222, 985)], 5, fill="#d8d0be")
    E.limb([(262, 948), (312, 982)], 5, fill="#d8d0be")
    E.add(f'<circle cx="262" cy="946" r="6" fill="#d8d0be" stroke="{INK}" stroke-width="1.8"/>')
    E.line([(262, 935), (262, 944)], w=3, smooth=False)
    E.line([(222, 985), (219, 993)], w=1.4, smooth=False)
    E.line([(312, 982), (315, 991)], w=1.4, smooth=False)
    # hammer in front
    E.shape([(362, 945), (410, 940), (414, 968), (366, 972)], smooth=False, fill="#cfc8b6", wash=slate, wash_op=0.2,
            hatches=[(60, 2.2, 0.7)], sw=2)
    E.limb([(410, 957), (545, 962)], 11, fill="#d8c8a0")
    E.add(plate_close())
    return svg(E.done(), PESS_PAPER)


# ---- VI: The Pendulum
def pendulum(rng):
    caput, slate = WASH["caput"], WASH["slate"]
    E = Etch(rng, "d")
    E.add(plate_open())
    E.add(aquatint(0.5))
    HY = 770  # horizon
    paper_wash(E, IX0 - 30, IY0 - 30, IX1 + 30, HY, caput, 0.1)
    line_hatch(E, IX0, IY0, IX1, HY, 9, op=0.12, angle=-1)
    paper_wash(E, IX0 - 30, HY, IX1 + 30, IY1 + 30, caput, 0.24)
    line_hatch(E, IX0, HY, IX1, IY1, 5, op=0.25, angle=0)
    E.shape([(IX0 - 5, HY), (IX1 + 5, HY), (IX1 + 5, HY + 8), (IX0 - 5, HY + 8)], smooth=False, fill=None, wash=INK, wash_op=0.15, outline=False)
    E.line([(IX0, HY), (IX1, HY)], w=1.4, smooth=False)
    E.strokes(IX0, HY + 20, IX1, IY1, 260, 3, 9, w=0.7)
    # the arc of the swing on the ground, dashed
    for k, (ry, w_) in enumerate([(70, 2.0), (52, 1.1)]):
        E.line([(IX0 + 40 + k * 14, 960 + k * 20), (200, 990 + ry * 0.6 + k * 12), (340, 1000 + ry + k * 8), (480, 990 + ry * 0.6 + k * 12), (IX1 - 40 - k * 14, 960 + k * 20)],
               w=w_, dash="9 7", op=0.85)
    # pendulum: rod from the top edge, heavy disc at mid-height
    E.shape([(318, IY0), (362, IY0), (366, IY0 + 36), (314, IY0 + 36)], smooth=False, fill="#cfc7b6", hatches=[(90, 2, 0.7)], sw=2.2)
    E.add(f'<rect x="334" y="{IY0 + 36}" width="12" height="470" fill="{INK}"/><rect x="338" y="{IY0 + 36}" width="3" height="470" fill="{PAPER_FILL}" opacity="0.6"/>')
    # faint ghost rods at the ends of the swing
    for sg in (-1, 1):
        E.line([(340, IY0 + 36), (340 + sg * 190, 690)], w=0.8, dash="3 8", op=0.35, smooth=False)
    cx, cy, R = 340, 660, 98
    E.add(f'<ellipse cx="{cx + 14}" cy="{cy + 14}" rx="{R}" ry="{R}" fill="{INK}" opacity="0.18" filter="url(#wash)"/>')
    E.shape(ellipse_pts(cx, cy, R, R, 28), fill="#b9b1a1", wash=caput, wash_op=0.45,
            hatches=[(45, 2.4, 0.7), (-45, 3.2, 0.6, (cx - R, cy - R, cx + R, cy + 20))], sw=3.4, grain=0.9)
    E.shape(ellipse_pts(cx, cy, R * 0.72, R * 0.72, 24), fill=None, hatches=[(0, 2.6, 0.45, (cx - R, cy, cx + R, cy + R))], sw=1.6)
    E.shape(ellipse_pts(cx, cy, R * 0.18, R * 0.18, 12), fill="#8d857a", sw=2)
    E.shape([(cx - 16, cy - R - 6), (cx + 16, cy - R - 6), (cx + 10, cy - R + 24), (cx - 10, cy - R + 24)], smooth=False, fill="#9f978a",
            hatches=[(90, 2, 0.8)], sw=2)
    # left: draped figure kneeling, doubled over in pain
    cloth = "#e6dfcd"
    E.add(f'<ellipse cx="190" cy="1018" rx="110" ry="9" fill="{INK}" opacity="0.2" filter="url(#wash)"/>')
    E.limb([(185, 1000), (255, 1008), (275, 1002)], 24, fill=cloth)
    E.limb([(190, 925), (160, 985), (150, 1010)], 16, fill="#e6dcc5")
    E.shape([(100, 1005), (105, 945), (150, 892), (215, 880), (262, 925), (270, 985), (250, 1012), (170, 1018)], fill=cloth,
            wash=caput, wash_op=0.35, hatches=[(70, 2.8, 0.55), (-60, 4, 0.45, (150, 940, 280, 1020)), (10, 6, 0.3)], sw=2.2, grain=0.4)
    E.line([(150, 905), (170, 960), (160, 1010)], w=1.0, op=0.7)
    E.line([(215, 895), (225, 950), (240, 1005)], w=1.0, op=0.7)
    head(E, 118, 950, 26, face="front", look=0.1, rot=-62, brow=-1.6, wash=caput)
    E.add(f'<path d="M104,928 q20,-26 44,-6 q-8,-12 -24,-14 q-14,2 -20,20 Z" fill="{INK}" opacity="0.75"/>')  # hair
    E.limb([(235, 905), (268, 960), (225, 978)], 14, fill="#e6dcc5")  # hand pressed to the side
    E.add(f'<circle cx="224" cy="978" r="8" fill="#e6dcc5" stroke="{INK}" stroke-width="1.4"/>')
    # right: the yawner, slouched on a stone block, arms overhead
    E.add(f'<ellipse cx="500" cy="1022" rx="120" ry="9" fill="{INK}" opacity="0.2" filter="url(#wash)"/>')
    E.shape([(440, 948), (580, 948), (590, 1020), (432, 1020)], smooth=False, fill="#ddd6c4", wash=caput, wash_op=0.2,
            hatches=[(90, 4, 0.4), (0, 8, 0.3)], sw=2.2, grain=0.6)
    E.shape([(440, 948), (580, 948), (572, 934), (452, 934)], smooth=False, fill="#e8e1d0", hatches=[(0, 3, 0.4)], sw=2)
    # legs forward, lower legs hanging
    E.limb([(520, 925), (455, 930), (440, 1005)], 26, fill="#cfc9bb")
    E.limb([(545, 925), (484, 940), (484, 1008)], 26, fill="#cfc9bb")
    E.shape([(424, 1008), (460, 1008), (462, 1022), (418, 1022)], smooth=False, fill=INK, sw=1.2)
    E.shape([(470, 1010), (506, 1010), (508, 1024), (464, 1024)], smooth=False, fill=INK, sw=1.2)
    E.shape([(492, 934), (488, 860), (516, 802), (572, 812), (590, 880), (570, 936)], fill="#d9d9d3", wash=slate, wash_op=0.3,
            hatches=[(70, 2.8, 0.5), (-50, 4, 0.4, (520, 820, 600, 940))], sw=2.2)
    E.limb([(510, 826), (478, 765), (470, 705)], 17, fill="#d9d9d3")
    E.limb([(562, 822), (580, 760), (572, 700)], 17, fill="#d9d9d3")
    for hx_, hy_ in ((470, 698), (572, 692)):
        E.add(f'<circle cx="{hx_}" cy="{hy_}" r="10" fill="#e6dcc5" stroke="{INK}" stroke-width="1.4"/>')
    head(E, 541, 770, 31, face="front", look=0.0, mouth=2.4, rot=22, brow=-0.4, wash=caput)
    # closed book at his feet
    E.shape([(380, 1040), (435, 1034), (440, 1052), (384, 1060)], smooth=False, fill="#cdbfa0", hatches=[(70, 2.4, 0.5)], sw=2)
    E.shape([(384, 1060), (440, 1052), (440, 1060), (386, 1068)], smooth=False, fill="#f0eadb", hatches=[(0, 1.4, 0.6)], sw=1.4)
    E.add(plate_close())
    return svg(E.done(), PESS_PAPER)


# ---- VII: Nature and the Icelander
def nature(rng):
    slate, bone = WASH["slate"], WASH["bone"]
    E = Etch(rng, "n")
    E.add(plate_open())
    E.add(aquatint(0.5))
    HY = 880
    paper_wash(E, IX0 - 30, IY0 - 30, IX1 + 30, HY, slate, 0.14)
    line_hatch(E, IX0, IY0, IX1, HY, 8, op=0.14, angle=-1)
    # the mountain, one mass with her back and elbow
    mtn = [(IX1 + 10, 120), (545, 112), (500, 150), (452, 250), (410, 360), (392, 440), (440, 560), (470, 700), (515, 790), (545, 850), (IX1 + 10, 850)]
    E.shape(mtn, smooth=True, fill="#d9d9d3", wash=slate, wash_op=0.4,
            hatches=[(62, 3, 0.6), (-55, 5, 0.4, (390, 100, 620, 700)), (62, 2, 0.5, (500, 100, 620, 880))], sw=2.4, grain=0.8)
    for k in range(7):  # ridges
        y0 = 160 + k * 90
        E.line([(IX1, y0 + 30), (560 - k * 6, y0), (520 - k * 12, y0 + 70)], w=1.0, op=0.6)
    # ground
    paper_wash(E, IX0 - 30, HY, IX1 + 30, IY1 + 30, bone, 0.4)
    line_hatch(E, IX0, HY, IX1, IY1, 6, op=0.2, angle=0)
    E.line([(IX0, HY), (IX1, HY)], w=1.3, smooth=False)
    for _ in range(14):  # dry cracks and stones
        x, y = rng.uniform(IX0 + 20, IX1 - 20), rng.uniform(HY + 30, IY1 - 20)
        E.line([(x, y), (x + rng.uniform(20, 50), y + rng.uniform(-4, 6)), (x + rng.uniform(50, 90), y + rng.uniform(-6, 10))], w=0.8, op=0.6)
    E.strokes(IX0, HY + 15, IX1, IY1, 120, 2, 5, w=0.7)
    robe = "#dedbd0"
    # robe and lap
    body = [(298, 400), (362, 400), (428, 440), (470, 540), (455, 660), (498, 790), (552, 880), (420, 905), (250, 912), (140, 890), (150, 790),
            (205, 640), (232, 500), (250, 440)]
    E.add(f'<ellipse cx="340" cy="896" rx="260" ry="12" fill="{INK}" opacity="0.22" filter="url(#wash)"/>')
    E.shape(body, fill=robe, wash=slate, wash_op=0.4,
            hatches=[(75, 3, 0.55), (-65, 5, 0.4, (330, 440, 560, 920)), (8, 6, 0.3, (130, 700, 560, 920))], sw=2.6, grain=0.7)
    for pts in [[(300, 470), (290, 600), (270, 760), (240, 880)], [(360, 470), (370, 620), (360, 780), (380, 900)],
                [(255, 560), (235, 680), (190, 800), (160, 880)], [(420, 600), (440, 720), (470, 830)]]:
        E.line(pts, w=1.2, op=0.75)
    # knee mass: the lap rises to a bent knee at left
    E.shape([(135, 880), (150, 780), (230, 720), (330, 740), (400, 820), (410, 900)], fill=robe, wash=slate, wash_op=0.3,
            hatches=[(15, 3.2, 0.5), (80, 4, 0.35)], sw=2.2)
    # left arm resting on the lap
    E.limb([(252, 452), (205, 585), (262, 725)], 38, fill=robe)
    E.add(f'<ellipse cx="270" cy="738" rx="22" ry="16" fill="{robe}" stroke="{INK}" stroke-width="1.8"/>')
    # right arm, elbow against the mountain
    E.limb([(425, 455), (484, 556), (418, 662)], 38, fill=robe)
    # neck, hair, face
    E.shape([(298, 380), (362, 380), (368, 430), (292, 430)], smooth=False, fill="#e2dccb", hatches=[(60, 2.4, 0.6)], sw=1.8)
    hair = [(255, 330), (248, 255), (292, 205), (360, 202), (415, 245), (424, 330), (452, 440), (430, 540), (385, 440), (290, 440), (238, 540), (212, 440)]
    E.shape(hair, fill=INK, sw=2.4)
    for k in range(14):  # strands catching light
        x = 232 + k * 15
        E.line([(x, 250 + abs(k - 7) * 6), (x + (k - 7) * 3, 400), (x + (k - 7) * 5, 520 - abs(k - 7) * 6)], w=0.7, op=0.45, color="#d8d0c0")
    E.add('<g transform="rotate(-5 334 332)">')
    E.shape([(334, 262), (378, 286), (396, 340), (380, 392), (334, 412), (288, 392), (272, 340), (290, 286)], fill="#ece5d6", wash=slate, wash_op=0.12,
            hatches=[(70, 2.4, 0.5, (340, 262, 400, 420)), (-10, 4, 0.25, (270, 370, 400, 420))], sw=2.2, grain=0.3)
    # brows, eyes with black irises, nose, firm mouth
    for sg in (-1, 1):
        ex = 334 + sg * 33
        E.line([(ex - sg * 24, 318 - sg * 2 * 0 - 4), (ex + sg * 18, 312 + 2)], w=4, smooth=False)
        E.shape([(ex - 24, 332), (ex, 322), (ex + 24, 332), (ex, 342)], fill="#fbf8f0", sw=1.6)
        E.add(f'<ellipse cx="{ex - 6}" cy="334" rx="11" ry="9" fill="{INK}"/><circle cx="{ex - 9}" cy="331" r="2" fill="#fbf8f0"/>')
        E.line([(ex - 26, 326), (ex, 316), (ex + 26, 326)], w=1.0, op=0.6)
    E.line([(334, 338), (330, 368), (344, 376)], w=1.4, smooth=False)
    E.line([(346, 372), (334, 380)], w=1.0, smooth=False)
    E.shape([(308, 392), (334, 388), (360, 392), (334, 399)], smooth=True, fill="#9a8f84", sw=1.6)
    E.line([(310, 392), (358, 392)], w=1.6, smooth=False)
    E.line([(290, 300), (300, 340), (306, 372)], w=0.8, op=0.5)
    E.add('</g>')
    # the Icelander: small, heavy coat, cap, staff
    tx, tb = 168, 1030
    E.add(f'<ellipse cx="{tx + 6}" cy="{tb + 2}" rx="26" ry="3" fill="{INK}" opacity="0.4"/>')
    E.line([(tx + 14, tb), (tx + 15, tb - 70)], w=1.8, smooth=False)
    person(E, tx, tb, 62, garment="robe", hat=None, face="back", cloth="#6e675c", wash=INK, wash_op=0.3,
           arms=[(1, (0.04, -0.1), (0.09, -0.08))])
    E.add(plate_close())
    return svg(E.done(), PESS_PAPER)


# Card id -> drawing function
CARDS = {"00": unborn, "01": giant_deer, "02": happiness_here, "03": happiness_hereafter, "04": progress, "05": vanity, "06": pendulum, "07": nature}
