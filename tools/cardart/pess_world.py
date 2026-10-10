"""Pessimist deck, the world and its remedies: cards VIII-XV."""

import math

from .common import (ETCH_INK, IMAGE_BOX, PESS_PAPER, WASH, W, H, aquatint, f,
                     plate_close, plate_open, svg)

INK = ETCH_INK
FILL = "#ece5d6"    # figure and object fill, close to the plate tone
LIGHT = "#f7f3ea"   # pale paper for things lit against a dark ground
IX0, IY0, IX1, IY1 = IMAGE_BOX


# ------------------------------------------------------------------ toolkit

class Pen:
    """Collects SVG parts and hands out unique ids; all randomness comes from rng."""

    def __init__(self, tag, rng):
        self.tag, self.rng, self.n, self.o = tag, rng, 0, []

    def uid(self, kind="c"):
        self.n += 1
        return f"{self.tag}{kind}{self.n}"

    def add(self, s):
        self.o.append(s)

    def push(self, transform):
        self.o.append(f'<g transform="{transform}">')

    def pop(self):
        self.o.append("</g>")

    def done(self):
        return "".join(self.o)

    # -- tone ---------------------------------------------------------
    def hatch_lines(self, box, angle, gap, wob=0.6, drop=0.0):
        """Parallel pen lines covering box, as (path data, rotate transform)."""
        x0, y0, x1, y1 = box
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        r = math.hypot(x1 - x0, y1 - y0) / 2 + 2
        d, y = [], -r
        while y < r:
            if self.rng.random() >= drop:
                d.append(f"M{f(cx - r)},{f(cy + y)} l{f(2 * r)},{f(self.rng.uniform(-wob, wob))}")
            y += gap
        return " ".join(d), f"rotate({angle} {f(cx)} {f(cy)})"

    def hatch(self, d, box, hatches, s=1.0, ink=INK):
        """Hatching clipped to path d; hatches is a list of (angle, gap, opacity[, width])."""
        cid = self.uid("c")
        parts = [f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">']
        for hh in hatches:
            ang, gap, op = hh[:3]
            lw = hh[3] if len(hh) > 3 else 0.7
            dd, rt = self.hatch_lines(box, ang, gap / s, drop=0.06)
            parts.append(f'<g transform="{rt}"><path d="{dd}" stroke="{ink}" stroke-width="{f(lw / s)}" opacity="{op}"/></g>')
        parts.append("</g>")
        self.add("".join(parts))

    def shape(self, d, box, fill=FILL, hatches=(), sw=1.8, s=1.0, outline=True, wash=None, wash_op=0.45):
        """A filled shape with an optional thin wash, hatching and an etched outline."""
        if fill:
            self.add(f'<path d="{d}" fill="{fill}"/>')
        if wash:
            cid = self.uid("c")
            self.add(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
                     f'<path d="{d}" fill="{wash}" opacity="{wash_op}" clip-path="url(#{cid})"/>')
        if hatches:
            self.hatch(d, box, hatches, s)
        if outline:
            self.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(sw / s)}" stroke-linejoin="round"/>')

    def limb(self, pts, w, fill=FILL, s=1.0):
        """A tube with an etched outline, drawn as a wide ink stroke under a paper stroke."""
        d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts)
        self.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(w + 1.8 / s)}" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{f(w)}" stroke-linecap="round" stroke-linejoin="round"/>')

    def wash(self, x, y, w, h, colour, op, filt="softwash"):
        self.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{colour}" opacity="{op}" filter="url(#{filt})"/>')

    def blot(self, cx, cy, rx, ry, colour, op, filt="wash"):
        self.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{colour}" opacity="{op}" filter="url(#{filt})"/>')

    def sky_lines(self, y0, y1, gap=6, strongest=0.5, weakest=0.06, x0=IX0, x1=IX1, ink=INK, width=0.7):
        """Horizontal etched lines that thin from the first y to the last."""
        for k in range(int((y1 - y0) / gap)):
            y = y0 + k * gap
            t = k * gap / (y1 - y0)
            op = strongest + (weakest - strongest) * t
            self.add(f'<path d="M{x0},{f(y)} L{x1},{f(y + self.rng.uniform(-1, 1))}" stroke="{ink}" stroke-width="{width}" opacity="{op:.2f}"/>')

    def scatter(self, box, n, length, tilt=0.0, op=(0.3, 0.7), width=0.8, ink=INK):
        """Short pen strokes scattered over a box: grass, texture, snow marks."""
        x0, y0, x1, y1 = box
        d = []
        for _ in range(n):
            x, y = self.rng.uniform(x0, x1), self.rng.uniform(y0, y1)
            ln = self.rng.uniform(length * 0.5, length)
            d.append(f"M{f(x)},{f(y)} l{f(ln * math.cos(tilt) + self.rng.uniform(-2, 2))},{f(-ln * math.sin(tilt))}")
        self.add(f'<path d="{" ".join(d)}" stroke="{ink}" stroke-width="{width}" opacity="{(op[0] + op[1]) / 2:.2f}"/>')

    def bare_tree(self, x, y, h, op=0.8, width=None):
        """A leafless tree: a trunk with recursive forked branches."""
        width = width or max(0.8, h / 22)
        d = []

        def branch(bx, by, ang, ln, depth):
            ex, ey = bx + ln * math.sin(ang), by - ln * math.cos(ang)
            d.append((bx, by, ex, ey, depth))
            if depth < 3 and ln > 3:
                for da in (-0.5, 0.45):
                    branch(ex, ey, ang + da + self.rng.uniform(-0.2, 0.2), ln * self.rng.uniform(0.6, 0.72), depth + 1)

        branch(x, y, self.rng.uniform(-0.08, 0.08), h * 0.45, 0)
        out = [f'<g opacity="{op}" stroke="{INK}" stroke-linecap="round">']
        for bx, by, ex, ey, depth in d:
            out.append(f'<path d="M{f(bx)},{f(by)} L{f(ex)},{f(ey)}" stroke-width="{f(max(0.4, width * (1 - depth * 0.28)))}"/>')
        out.append("</g>")
        self.add("".join(out))


def ellipse_d(cx, cy, rx, ry):
    return (f"M{f(cx - rx)},{f(cy)} A{f(rx)},{f(ry)} 0 1 0 {f(cx + rx)},{f(cy)} "
            f"A{f(rx)},{f(ry)} 0 1 0 {f(cx - rx)},{f(cy)} Z")


def poly_d(pts):
    return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + " Z"


def head(p, cx, cy, r, nose=0, tilt=0, hair=True, s=1.0, hat=False):
    """A head: nose is +1 right, -1 left, 0 for a head seen from behind."""
    p.shape(ellipse_d(cx, cy, r * 0.88, r), (cx - r, cy - r, cx + r, cy + r), s=s, sw=1.5)
    if nose:
        n = nose
        p.shape(poly_d([(cx + n * r * 0.8, cy - r * 0.2), (cx + n * r * 1.45, cy + r * 0.3), (cx + n * r * 0.75, cy + r * 0.38)]),
                (cx - 2 * r, cy - r, cx + 2 * r, cy + r), s=s, sw=1.2)
        p.add(f'<circle cx="{f(cx + n * r * 0.5)}" cy="{f(cy - r * 0.1)}" r="{f(max(0.5, r * 0.1))}" fill="{INK}"/>')
    if hair:
        a = -nose if nose else 1
        p.add(f'<path d="M{f(cx - r * 0.88)},{f(cy)} C{f(cx - r * 0.9)},{f(cy - r * 1.15)} {f(cx + r * 0.9)},{f(cy - r * 1.15)} {f(cx + r * 0.88)},{f(cy - r * 0.2)} '
              f'C{f(cx + r * 0.3 * a)},{f(cy - r * 0.55)} {f(cx - r * 0.4)},{f(cy - r * 0.5)} {f(cx - r * 0.88)},{f(cy)} Z" fill="{INK}" opacity="0.8"/>')
    if hat:
        p.add(f'<path d="M{f(cx - r * 1.5)},{f(cy - r * 0.7)} L{f(cx + r * 1.5)},{f(cy - r * 0.7)} L{f(cx + r * 0.9)},{f(cy - r * 1.0)} '
              f'L{f(cx + r * 0.7)},{f(cy - r * 1.8)} L{f(cx - r * 0.7)},{f(cy - r * 1.8)} L{f(cx - r * 0.9)},{f(cy - r * 1.0)} Z" fill="{INK}" opacity="0.85"/>')


def walker_back(p, x, y, h, skirt=False, hat=False, look=0, tone=0.55, wash=None, stride=0.0, child=False):
    """A figure seen from behind, walking away. look=+1/-1 turns the head to show a nose."""
    s = h / 100.0
    p.push(f"translate({f(x)},{f(y)}) scale({f(s)})")
    bottom = -18 if not skirt else -4
    half = 13 if not skirt else 17
    # legs
    if not skirt:
        p.limb([(-5, -18), (-6 - stride, -9), (-6 - stride * 1.5, 0)], 5, FILL, s)
        p.limb([(5, -18), (6 + stride, -9), (7 + stride * 1.5, 0)], 5, FILL, s)
    body = (f"M-11,-80 C-14,-60 -{half + 1},-40 -{half},{bottom} L{half},{bottom} C{half + 1},-40 14,-60 11,-80 C6,-85 -6,-85 -11,-80 Z")
    box = (-20, -86, 20, 0)
    p.shape(body, box, hatches=[(62, 2.6, tone + 0.15, 0.8), (-30, 3.4, tone * 0.6, 0.7)], s=s, sw=1.7, wash=wash, wash_op=0.5)
    # arms hang along the coat
    p.add(f'<path d="M-11,-76 C-14,-60 -14,-46 -13,-36 M11,-76 C14,-60 14,-46 13,-36" stroke="{INK}" stroke-width="{f(1.2 / s)}" fill="none"/>')
    head(p, 0, -91, 7.5, nose=look, hair=True, s=s, hat=hat)
    p.pop()


def walker_profile(p, x, y, h, facing=1, kind="man", pose="walk", tone=0.5, wash=None, wash_op=0.5, stride=1.0):
    """A figure in profile. kind: man (long coat), tunic (short), woman (skirt), child.
    pose: walk, stand, open (standing, right arm held out, palm open)."""
    s = h / 100.0
    p.push(f"translate({f(x)},{f(y)}) scale({f(s * facing)},{f(s)})")
    long = {"man": -14, "woman": -3, "child": -12, "tunic": -38}[kind]
    sh = 8 if kind != "child" else 6
    hs = 7 if kind != "child" else 8
    hy = -91 if kind != "child" else -88
    if pose == "walk" and kind != "woman":
        st = stride
        p.limb([(-3, -38), (-9 * st, -19), (-19 * st, -3)], 6.5 if kind == "tunic" else 5, FILL, s)       # back leg
    # back arm
    p.limb([(-6, -78), (-10, -62), (-12, -50)], 4.5, FILL, s)
    tunic = (f"M-{sh},-83 C-{sh + 4},-70 -{sh + 4},-56 -{sh + 5},{long} L{sh + 6},{long} C{sh + 5},-56 {sh + 3},-70 {sh - 1},-83 Z")
    if kind == "woman":
        tunic = (f"M-{sh - 1},-83 C-{sh + 3},-70 -{sh + 1},-52 -17,{long} L18,{long} C{sh + 5},-52 {sh + 2},-70 {sh - 1},-83 Z")
    if pose == "walk" and kind != "woman":
        p.limb([(3, -38), (12 * stride, -19), (12 * stride, -1)], 6.5 if kind == "tunic" else 5, FILL, s)  # front leg
        p.add(f'<path d="M{f(12 * stride - 2)},-1 l8,0" stroke="{INK}" stroke-width="{f(3 / s)}" stroke-linecap="round"/>')
    elif kind != "woman":
        p.limb([(-4, long), (-5, -6), (-5, 0)], 5, FILL, s)
        p.limb([(5, long), (5, -6), (5, 0)], 5, FILL, s)
    p.shape(tunic, (-22, -86, 22, 0), hatches=[(62, 2.6, tone + 0.1, 0.8), (-30, 3.6, tone * 0.6, 0.7)], s=s, sw=1.8, wash=wash, wash_op=wash_op)
    if pose == "open":
        p.limb([(6, -78), (20, -71), (33, -67)], 4.5, FILL, s)
        p.shape(ellipse_d(37, -67, 4.2, 2.2), (30, -72, 44, -62), s=s, sw=1.2)
    else:
        p.limb([(6, -78), (10, -62), (14, -49)], 4.5, FILL, s)
    head(p, 2, hy, hs, nose=1, s=s)
    p.pop()


def aquatint_rect(p, box, op, fade=None):
    """Extra aquatint grain over a region (for darker passages)."""
    x0, y0, x1, y1 = box
    p.add(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" filter="url(#aqua)" opacity="{op}"/>')


def finish(p, grain=0.5, fade=True):
    p.add(aquatint(grain, fade))
    p.add(plate_close())
    return svg(p.done(), PESS_PAPER)


# ------------------------------------------------------------ VIII porcupines

def porcupine(p, x, y, s, facing=1, raised=False, rot=0, bone=True):
    """A porcupine in profile, quills swept back (relaxed) or standing out (raised)."""
    rng = p.rng
    # shadow on the snow, a slate wash with hatching
    p.blot(x - facing * 6 * s, y + 2 * s, 52 * s, 7 * s, WASH["slate"], 0.45)
    p.add(f'<path d="M{f(x - 44 * s * facing - 8)},{f(y + 3 * s)} h{f(100 * s)} M{f(x - 36 * s * facing)},{f(y + 6 * s)} h{f(80 * s)}" '
          f'stroke="{INK}" stroke-width="0.6" opacity="0.35"/>')
    p.push(f"translate({f(x)},{f(y)}) rotate({rot}) scale({f(s * facing)},{f(s)})")
    quills = []
    n = 36 if raised else 40
    for k in range(n):
        th = math.radians(165 - k * (140 / n))
        bx, by = 46 * math.cos(th), -20 - 33 * math.sin(th)
        if raised:
            ux, uy = math.cos(th) * 0.8 + rng.uniform(-0.25, 0.25), -math.sin(th) - 0.15 + rng.uniform(-0.2, 0.2)
            ln = rng.uniform(34, 52)
        else:
            ux, uy = -0.9 + 0.2 * math.cos(th), 0.25 + 0.3 * (1 - math.sin(th)) + rng.uniform(-0.08, 0.08)
            ln = rng.uniform(22, 34)
        m = math.hypot(ux, uy)
        ux, uy = ux / m, uy / m
        quills.append(f"M{f(bx)},{f(by)} L{f(bx + ux * ln)},{f(by + uy * ln)}")
    p.add(f'<path d="{" ".join(quills)}" stroke="{INK}" stroke-width="{f(1.1 / s)}" opacity="0.9" stroke-linecap="round"/>')
    body = "M-44,0 C-48,-26 -26,-50 4,-50 C28,-50 40,-36 46,-22 L60,-14 C60,-8 52,-4 46,0 Z"
    p.shape(body, (-50, -52, 62, 2), hatches=[(70, 3.2, 0.5, 0.8), (20, 4.2, 0.35, 0.7)], s=s, sw=2.0,
            wash=WASH["bone"] if bone else None, wash_op=0.35)
    # shorter quills lying over the back, and a hatched belly
    inner = []
    for ring in (0.92, 0.62):
        for k in range(22):
            th = math.radians(160 - k * (125 / 22) + rng.uniform(-2, 2))
            bx, by = 46 * ring * math.cos(th), -20 - 31 * ring * math.sin(th)
            if raised:
                ln = rng.uniform(10, 18)
                inner.append(f"M{f(bx)},{f(by)} L{f(bx + math.cos(th) * ln * 0.9)},{f(by - math.sin(th) * ln)}")
            else:
                ln = rng.uniform(22, 38)
                inner.append(f"M{f(bx)},{f(by)} q{f(-ln * 0.5)},{f(-2)} {f(-ln)},{f(ln * 0.3)}")
    p.add(f'<path d="{" ".join(inner)}" stroke="{INK}" stroke-width="{f(0.8 / s)}" opacity="0.6" stroke-linecap="round"/>')
    p.add(f'<path d="M-10,-4 Q10,-8 36,-3" stroke="{INK}" stroke-width="{f(1.2 / s)}" fill="none" opacity="0.7"/>')
    p.add(f'<circle cx="48" cy="-17" r="1.5" fill="{INK}"/><circle cx="60" cy="-14" r="2.4" fill="{INK}"/>')
    p.add(f'<path d="M-20,0 l0,2 M-8,0 l0,2 M26,0 l0,2 M38,0 l0,2" stroke="{INK}" stroke-width="{f(3 / s)}" stroke-linecap="round"/>')
    p.pop()


def porcupines(rng):
    p = Pen("p8", rng)
    slate = WASH["slate"]
    p.add(plate_open())
    hor = 560
    # slate sky, thinning toward the horizon, with etched lines
    p.wash(IX0 - 40, IY0 - 40, IX1 - IX0 + 80, hor - IY0 + 40, slate, 0.24, "mist")
    p.sky_lines(IY0, hor, 7, 0.26, 0.03)
    # far trees along the horizon
    for _ in range(46):
        x = rng.uniform(IX0 - 10, IX1 + 10)
        p.bare_tree(x, hor + rng.uniform(-2, 8), rng.uniform(16, 42), op=rng.uniform(0.35, 0.7))
    p.add(f'<path d="M{IX0},{hor} L{IX1},{hor + 2}" stroke="{INK}" stroke-width="0.8" opacity="0.6"/>')
    # snowfield: pale drifts, shadows in slate, hatching in low curves
    for y0, amp in [(600, 5), (660, 8), (730, 10), (820, 12), (930, 14), (1030, 16)]:
        p.add(f'<path d="M{IX0},{y0} C{IX0 + 150},{y0 - amp} {IX0 + 300},{y0 + amp} {IX1},{y0 - amp / 2}" fill="none" '
              f'stroke="{INK}" stroke-width="0.7" opacity="0.4"/>')
        p.add(f'<path d="M{IX0},{y0 + 6} C{IX0 + 160},{y0 - amp + 6} {IX0 + 320},{y0 + amp + 6} {IX1},{y0 - amp / 2 + 6}" fill="none" '
              f'stroke="{slate}" stroke-width="6" opacity="0.10"/>')
    p.scatter((IX0, hor + 12, IX1, IY1), 220, 14, 0.0, (0.2, 0.45), 0.7)
    # footprints between the animals
    pts = [(150, 1040), (190, 990), (250, 940), (290, 890), (320, 850)]
    for k in range(34):
        t = k / 33
        # quadratic through three of the points
        x = (1 - t) ** 2 * 120 + 2 * (1 - t) * t * 220 + t * t * 345
        y = (1 - t) ** 2 * 1060 + 2 * (1 - t) * t * 900 + t * t * 835
        off = 7 if k % 2 else -7
        sz = 4.4 - 2.2 * t
        p.add(f'<ellipse cx="{f(x + off)}" cy="{f(y)}" rx="{f(sz)}" ry="{f(sz * 0.5)}" fill="{slate}" opacity="0.35" stroke="{INK}" stroke-width="0.6"/>')
    # the ring of seven, seen from above, and the pair at the centre
    cx, cy, rx, ry = 340, 835, 200, 150
    animals = []
    for k in range(7):
        a = math.radians(-90 + k * 360 / 7 + 12)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        animals.append((y, x, False))
    animals.append((810, 306, True))
    animals.append((817, 380, True))
    animals.sort()
    for y, x, close in animals:
        s = 0.66 + 0.5 * (y - 660) / 330
        if close:
            left = x < 340
            porcupine(p, x, y, s * 1.02, facing=1 if left else -1, raised=True, rot=-7 if left else 2)
        else:
            porcupine(p, x, y, s, facing=1 if (x < 340) != (rng.random() < 0.3) else -1)
    p.add(aquatint(0.42))
    p.add(plate_close())
    return svg(p.done(), PESS_PAPER)


# ---------------------------------------------------------- IX shattered god

def shard(p, x, y, size, rot, light=True):
    """A smooth pale shard with one hatched face."""
    rng = p.rng
    n = rng.randint(4, 6)
    pts = []
    for k in range(n):
        a = k * 2 * math.pi / n + rng.uniform(-0.3, 0.3)
        r = size * (rng.uniform(0.55, 1.0) if k % 2 else rng.uniform(0.8, 1.35))
        pts.append((r * math.cos(a) * 1.3, r * math.sin(a) * 0.7))
    p.push(f"translate({f(x)},{f(y)}) rotate({rot})")
    p.shape(poly_d(pts), (-2 * size, -2 * size, 2 * size, 2 * size), fill=LIGHT,
            hatches=[(35, max(2.2, size / 6), 0.55, 0.7)], sw=1.4)
    p.pop()


def star(p, x, y, r):
    pts = []
    for k in range(8):
        a = k * math.pi / 4
        rr = r if k % 2 == 0 else r * 0.22
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    p.add(f'<path d="{poly_d(pts)}" fill="{LIGHT}" stroke="{INK}" stroke-width="0.5"/>')


def stone(p, x, y, r, rot=0):
    p.push(f"translate({f(x)},{f(y)}) rotate({rot})")
    d = f"M{-r},0 C{-r},{-r * 0.8} {-r * 0.4},{-r} {r * 0.3},{-r * 0.9} C{r},{-r * 0.8} {r * 1.1},{-r * 0.2} {r},0 C{r * 0.6},{r * 0.4} {-r * 0.6},{r * 0.4} {-r},0 Z"
    p.shape(d, (-r, -r, r, r), fill=LIGHT, hatches=[(60, 2.4, 0.6, 0.7), (-20, 3.4, 0.4, 0.6)], sw=1.4)
    p.pop()


def fish(p, x, y, size, rot=0):
    p.push(f"translate({f(x)},{f(y)}) rotate({rot}) scale({f(size / 40)})")
    d = "M-40,0 C-24,-18 10,-20 30,0 C10,20 -24,18 -40,0 Z"
    p.shape(d, (-42, -22, 32, 22), fill=LIGHT, hatches=[(80, 2.6, 0.5, 0.7)], sw=1.6, s=size / 40)
    p.shape("M30,0 L50,-14 L46,0 L50,14 Z", (28, -16, 52, 16), fill=LIGHT, hatches=[(0, 3, 0.5)], sw=1.4, s=size / 40)
    p.add(f'<circle cx="-26" cy="-3" r="2.2" fill="{INK}"/><path d="M-12,-8 Q-8,0 -12,8" stroke="{INK}" stroke-width="1.2" fill="none"/>')
    p.pop()


def bird(p, x, y, size, rot=0):
    p.push(f"translate({f(x)},{f(y)}) rotate({rot}) scale({f(size / 40)})")
    p.limb([(-40, -6), (-22, -18), (-6, -2)], 4.5, LIGHT, size / 40)
    p.limb([(40, -8), (22, -20), (6, -2)], 4.5, LIGHT, size / 40)
    p.shape("M-12,-2 C-6,-8 8,-8 14,-2 C10,6 -6,8 -12,-2 Z", (-14, -10, 16, 8), fill=LIGHT, hatches=[(60, 2.2, 0.5)], sw=1.6, s=size / 40)
    p.add(f'<path d="M12,-4 L22,-1 L12,0" fill="{INK}"/>')
    p.pop()


def tree(p, x, y, h):
    p.limb([(x, y), (x, y - h * 0.45)], h / 12, LIGHT)
    for dx, dy, rr in [(-0.2, 0.62, 0.22), (0.2, 0.64, 0.22), (0, 0.8, 0.26), (-0.08, 0.55, 0.2), (0.12, 0.5, 0.18)]:
        p.add(f'<circle cx="{f(x + dx * h)}" cy="{f(y - dy * h)}" r="{f(rr * h)}" fill="{LIGHT}" stroke="{INK}" stroke-width="1.3"/>')
    for dx, dy, rr in [(0, 0.8, 0.26), (-0.2, 0.62, 0.22), (0.2, 0.64, 0.22)]:
        p.add(f'<circle cx="{f(x + dx * h)}" cy="{f(y - dy * h)}" r="{f(rr * h * 0.82)}" fill="{LIGHT}"/>')
    d = " ".join(f"M{f(x - h * 0.4 + k * h * 0.07)},{f(y - h * 0.5)} q{f(h * 0.04)},{f(-h * 0.25)} {f(-h * 0.01)},{f(-h * 0.5)}" for k in range(12))
    p.add(f'<path d="{d}" stroke="{INK}" stroke-width="0.6" fill="none" opacity="0.5"/>')


def jagged(rng, x0, y0, x1, y1, steps=7, amp=14):
    pts = [(x0, y0)]
    for k in range(1, steps):
        t = k / steps
        pts.append((x0 + (x1 - x0) * t + rng.uniform(-amp, amp), y0 + (y1 - y0) * t + rng.uniform(-amp, amp)))
    pts.append((x1, y1))
    return pts


def shattered_god(rng):
    p = Pen("p9", rng)
    caput, bone = WASH["caput"], WASH["bone"]
    p.add(plate_open())
    # dark aquatint sky: ink grain doubled, hatched, tinted caput mortuum
    p.add(f'<rect x="{IX0}" y="{IY0}" width="{IX1 - IX0}" height="{IY1 - IY0}" fill="#cfc6b6"/>')
    p.wash(IX0 - 40, IY0 - 40, IX1 - IX0 + 80, 1000, caput, 0.55, "mist")
    p.add(f'<rect x="{IX0}" y="{IY0}" width="{IX1 - IX0}" height="880" fill="{INK}" opacity="0.28"/>')
    for ang, gap, op in [(0, 3.2, 0.42), (50, 4.4, 0.3), (-40, 5.5, 0.25)]:
        dd, rt = p.hatch_lines((IX0, IY0, IX1, 900), ang, gap)
        p.add(f'<clipPath id="p9sky{ang + 90}"><rect x="{IX0}" y="{IY0}" width="{IX1 - IX0}" height="830"/></clipPath>'
              f'<g clip-path="url(#p9sky{ang + 90})"><g transform="{rt}"><path d="{dd}" stroke="{INK}" stroke-width="0.8" opacity="{op}"/></g></g>')
    aquatint_rect(p, (IX0, IY0, IX1, 900), 0.9)
    aquatint_rect(p, (IX0, IY0, IX1, 900), 0.6)
    # landscape in the lower third: a dim ground with low hills, lighter than the sky
    horizon = "M70,900 C140,870 190,905 260,885 C330,862 380,900 450,880 C520,862 570,890 610,878 L610,1086 L70,1086 Z"
    p.shape(horizon, (IX0, 850, IX1, IY1), fill="#d9d0bf", hatches=[(0, 5, 0.35), (25, 7, 0.22)], sw=1.4, wash=caput, wash_op=0.18)
    p.scatter((IX0, 910, IX1, IY1), 160, 12, 0.0, (0.3, 0.5), 0.7)
    for y0 in (940, 990, 1040):
        p.add(f'<path d="M{IX0},{y0} C{IX0 + 150},{y0 - 8} {IX0 + 320},{y0 + 8} {IX1},{y0 - 4}" stroke="{INK}" stroke-width="0.7" fill="none" opacity="0.4"/>')
    # the sphere, larger than the plate: centre above the top edge
    cx, cy, r = 340, 200, 345
    sphere = ellipse_d(cx, cy, r, r)
    p.add(f'<path d="{sphere}" fill="{LIGHT}"/>')
    p.blot(cx - 70, cy + 230, 170, 70, bone, 0.5)
    # shading on the lower right limb: hatching under a radial mask
    p.add(f'<radialGradient id="p9g" cx="0.25" cy="0.15" r="1.15"><stop offset="0.62" stop-color="#000"/><stop offset="1" stop-color="#fff"/></radialGradient>'
          f'<mask id="p9m"><rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#p9g)"/></mask>')
    cid = "p9sph"
    p.add(f'<clipPath id="{cid}"><path d="{sphere}"/></clipPath><g clip-path="url(#{cid})"><g mask="url(#p9m)">')
    for ang, gap, op in [(65, 3.0, 0.7), (-25, 4.0, 0.5)]:
        dd, rt = p.hatch_lines((cx - r, cy - r, cx + r, cy + r), ang, gap)
        p.add(f'<g transform="{rt}"><path d="{dd}" stroke="{INK}" stroke-width="0.8" opacity="{op}"/></g>')
    p.add("</g>")
    # cracks: jagged lines running inward from the lower rim, some forking
    for k in range(30):
        a = math.radians(rng.uniform(20, 160))
        x0, y0 = cx + (r + 4) * math.cos(a), cy + (r + 4) * math.sin(a)
        ln = rng.uniform(60, 220)
        x1, y1 = x0 - ln * math.cos(a + rng.uniform(-0.35, 0.35)), y0 - ln * math.sin(a + rng.uniform(-0.35, 0.35))
        pts = jagged(rng, x0, y0, x1, y1, 6, 9)
        p.add(f'<path d="M' + " L".join(f"{f(a_)},{f(b_)}" for a_, b_ in pts) + f'" fill="none" stroke="{INK}" stroke-width="{rng.uniform(0.8, 1.6):.1f}" opacity="0.85"/>')
        if rng.random() < 0.6:
            bx, by = pts[3]
            bp = jagged(rng, bx, by, bx + rng.uniform(-70, 70), by - rng.uniform(10, 60), 4, 6)
            p.add(f'<path d="M' + " L".join(f"{f(a_)},{f(b_)}" for a_, b_ in bp) + f'" fill="none" stroke="{INK}" stroke-width="0.8" opacity="0.7"/>')
    p.add("</g>")
    p.add(f'<path d="{sphere}" fill="none" stroke="{INK}" stroke-width="2"/>')
    # fragments, fanning down: shards, then stars and stones, then the things of the world
    for k in range(34):
        t = rng.uniform(0.0, 0.26)
        x = 340 + rng.uniform(-1, 1) * (110 + t * 760)
        y = 545 + t * 1000 * (0.5 + 0.5 * rng.random())
        shard(p, x, y, 30 - t * 55 + rng.uniform(-4, 4), rng.randint(-50, 50))
    for k in range(40):
        star(p, rng.uniform(IX0 + 15, IX1 - 15), rng.uniform(620, 870), rng.uniform(5, 11))
    for x, y, r_ in [(190, 640, 15), (520, 620, 13), (120, 760, 11), (440, 740, 10), (560, 800, 12), (300, 820, 9), (230, 700, 8)]:
        stone(p, x, y, r_, rng.randint(-30, 30))
    fish(p, 470, 840, 40, -12)
    bird(p, 175, 830, 34, 8)
    tree(p, 135, 1000, 90)
    stone(p, 520, 1010, 14)
    stone(p, 440, 1050, 9)
    walker_back(p, 330, 1030, 54, tone=0.7)
    p.add(f'<path d="M300,1033 h60" stroke="{INK}" stroke-width="0.8" opacity="0.5"/>')
    return finish(p, 0.4, False)


# ------------------------------------------------------------- X the insomniac

def insomniac(rng):
    p = Pen("p10", rng)
    verd, bone = WASH["verdigris"], WASH["bone"]
    p.add(plate_open())
    # interior wall: light vertical hatching, darker toward the floor and the left
    p.add(f'<rect x="{IX0}" y="{IY0}" width="{IX1 - IX0}" height="{IY1 - IY0}" fill="#e9e2d2"/>')
    dd, rt = p.hatch_lines((IX0, IY0, IX1, IY1), 90, 6)
    p.add(f'<g transform="{rt}"><path d="{dd}" stroke="{INK}" stroke-width="0.6" opacity="0.28"/></g>')
    dd, rt = p.hatch_lines((IX0, 640, IX1, IY1), 70, 4.2)
    p.add(f'<linearGradient id="p10lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000"/><stop offset="0.5" stop-color="#555"/><stop offset="1" stop-color="#fff"/></linearGradient>'
          f'<mask id="p10fm"><rect x="{IX0}" y="640" width="{IX1 - IX0}" height="{IY1 - 640}" fill="url(#p10lg)"/></mask>'
          f'<g mask="url(#p10fm)"><g transform="{rt}"><path d="{dd}" stroke="{INK}" stroke-width="0.7" opacity="0.45"/></g></g>')
    # the window: night sky and a sleeping city
    wx0, wy0, wx1, wy1 = 362, 170, 590, 800
    win = f"M{wx0},{wy0} L{wx1},{wy0} L{wx1},{wy1} L{wx0},{wy1} Z"
    p.add(f'<path d="{win}" fill="#d4d6cc"/>')
    p.wash(wx0 - 20, wy0 - 20, wx1 - wx0 + 40, 700, verd, 0.55, "wash")
    p.add(f'<clipPath id="p10win"><path d="{win}"/></clipPath><g clip-path="url(#p10win)">')
    p.add(f'<rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}" fill="{verd}" opacity="0.35"/>')
    p.sky_lines(wy0, 560, 4, 0.55, 0.18, wx0, wx1)
    aquatint_rect(p, (wx0, wy0, wx1, 560), 0.9)
    for _ in range(14):
        star(p, rng.uniform(wx0 + 10, wx1 - 10), rng.uniform(wy0 + 15, 500), rng.uniform(2.2, 4.2))
    # street running into the distance, houses and roofs either side
    p.add(f'<path d="M452,560 L478,560 L520,{wy1} L420,{wy1} Z" fill="#cfd2c6" stroke="{INK}" stroke-width="0.8"/>')
    rows = [(570, 22, 14), (600, 30, 20), (640, 40, 27), (700, 56, 38), (780, 76, 52)]
    for yb, hw, hh in rows:
        spread = 8 + (yb - 570) * 0.34
        for side in (-1, 1):
            x = 465 + side * spread
            while wx0 - 50 < x < wx1 + 50:
                w = rng.uniform(0.8, 1.3) * hw
                hgt = rng.uniform(0.7, 1.2) * hh
                xl = x if side > 0 else x - w
                wall = poly_d([(xl, yb), (xl + w, yb), (xl + w, yb - hgt), (xl, yb - hgt)])
                p.shape(wall, (xl, yb - hgt, xl + w, yb), fill="#c6c9bc", hatches=[(80, 2.2, 0.55, 0.6)], sw=1.0)
                roof = poly_d([(xl - 3, yb - hgt), (xl + w + 3, yb - hgt), (xl + w / 2 + rng.uniform(-w * 0.15, w * 0.15), yb - hgt - w * 0.45)])
                p.shape(roof, (xl - 3, yb - hgt - w * 0.5, xl + w + 3, yb - hgt), fill="#b4baae", hatches=[(25, 2.0, 0.65, 0.6)], sw=1.1, wash=verd, wash_op=0.45)
                if rng.random() < 0.5:
                    cx_ = xl + w * rng.uniform(0.6, 0.85)
                    p.add(f'<path d="M{f(cx_)},{f(yb - hgt - w * 0.2)} v{f(-w * 0.45)}" stroke="{INK}" stroke-width="{f(max(1.2, w * 0.1))}"/>')
                x += side * (w + rng.uniform(1, 6) * (yb - 540) / 100)
    # lamp-post in the street: a dim bone point
    p.add(f'<path d="M472,{wy1 - 20} V{wy1 - 80}" stroke="{INK}" stroke-width="2"/><circle cx="472" cy="{wy1 - 84}" r="4" fill="{bone}" stroke="{INK}" stroke-width="1"/>')
    p.blot(472, wy1 - 84, 16, 14, bone, 0.5)
    p.add("</g>")
    # window frame, open sash and sill
    p.add(f'<path d="{win}" fill="none" stroke="{INK}" stroke-width="7"/><path d="{win}" fill="none" stroke="{FILL}" stroke-width="3.5"/>')
    p.shape(poly_d([(wx1, wy0), (wx1 + 18, wy0 + 24), (wx1 + 18, wy1 - 40), (wx1, wy1)]), (wx1, wy0, wx1 + 18, wy1), fill=FILL,
            hatches=[(80, 2.5, 0.5)], sw=1.6)
    p.shape(poly_d([(250, 800), (wx1 + 40, 800), (wx1 + 40, 826), (250, 826)]), (250, 800, wx1 + 40, 826), fill=FILL,
            hatches=[(0, 3, 0.5)], sw=2)
    # the table, books and lamp at the left
    p.shape(poly_d([(82, 850), (212, 850), (212, 866), (82, 866)]), (82, 850, 212, 866), fill=FILL, hatches=[(0, 3, 0.5)], sw=2)
    for lx in (90, 200):
        p.add(f'<path d="M{lx},866 V1010" stroke="{INK}" stroke-width="6"/><path d="M{lx},866 V1010" stroke="{FILL}" stroke-width="2.5"/>')
    for k, (bw, bh) in enumerate([(70, 14), (60, 12), (52, 12)]):
        by = 850 - sum(b[1] for b in [(70, 14), (60, 12), (52, 12)][:k + 1])
        p.shape(poly_d([(92 + k * 4, by), (92 + k * 4 + bw, by), (92 + k * 4 + bw, by + [(70, 14), (60, 12), (52, 12)][k][1]), (92 + k * 4, by + [(70, 14), (60, 12), (52, 12)][k][1])]),
                (92, by, 170, by + 14), fill=FILL, hatches=[(0, 2.5, 0.5)], sw=1.4)
    p.shape(poly_d([(166, 850), (200, 850), (196, 838), (170, 838)]), (166, 838, 200, 850), fill=FILL, hatches=[(80, 2, 0.5)], sw=1.4)
    p.shape(ellipse_d(183, 833, 16, 9), (167, 824, 199, 842), fill=LIGHT, sw=1.5)
    p.shape("M175,826 L175,796 C175,782 191,782 191,796 L191,826 Z", (175, 782, 191, 826), fill=LIGHT, sw=1.4)
    p.add(f'<path d="M183,826 C176,814 188,808 183,794 C180,806 190,812 183,826 Z" fill="{bone}" stroke="{INK}" stroke-width="0.8"/>')
    p.blot(183, 800, 70, 60, bone, 0.4, "mist")
    # chair and man in profile
    ox, oy = 296, 902
    p.push(f"translate({ox},{oy})")
    p.limb([(-52, -45), (-52, -190)], 5, FILL)
    p.limb([(-52, -45), (-52, 0)], 5, FILL)
    p.limb([(28, -45), (28, 0)], 5, FILL)
    p.shape("M-56,-42 L34,-42 L34,-34 L-56,-34 Z", (-56, -42, 34, -34), hatches=[(0, 2.5, 0.5)], sw=1.8)
    # legs: thigh forward, shin down, foot
    p.limb([(-18, -62), (34, -62), (38, -4)], 15, FILL)
    p.shape("M30,-2 L62,-2 L62,6 L30,6 Z", (30, -2, 62, 6), fill=INK, sw=1.2)
    # torso, shirtsleeves
    torso = "M-28,-60 C-34,-100 -30,-136 -18,-156 C-6,-168 12,-160 16,-146 C20,-114 12,-84 8,-60 Z"
    p.shape(torso, (-40, -170, 20, -58), fill=LIGHT, hatches=[(70, 3.4, 0.42, 0.7), (-20, 4.6, 0.25)], sw=2, wash=bone, wash_op=0.18)
    p.limb([(-6, -142), (8, -108), (10, -98)], 11, LIGHT)     # upper arm
    p.limb([(10, -98), (62, -101)], 10, LIGHT)                  # forearm on the sill
    p.shape(ellipse_d(68, -102, 9, 6), (58, -110, 78, -94), sw=1.4)
    p.limb([(-18, -156), (-6, -170)], 9, FILL)
    head(p, 4, -190, 17, nose=1, hair=True)
    p.add(f'<circle cx="11" cy="-192" r="2.4" fill="{LIGHT}" stroke="{INK}" stroke-width="0.8"/><circle cx="12" cy="-192" r="1.2" fill="{INK}"/>')
    p.add(f'<path d="M5,-200 L18,-203" stroke="{INK}" stroke-width="1.2"/>')
    p.pop()
    p.blot(310, 740, 60, 70, bone, 0.30)
    return finish(p, 0.4, True)


# ----------------------------------------------------------------- XI the stone

RIDGE = [(300, 70), (312, 200), (245, 400), (152, 560), (92, 700), (70, 780)]


def _ridge_x(y):
    for (xa, ya), (xb, yb) in zip(RIDGE, RIDGE[1:]):
        if ya <= y <= yb:
            return xa + (xb - xa) * (y - ya) / (yb - ya)
    return RIDGE[-1][0]


def boulder(p, cx, cy, r, moss=True):
    verd = WASH["verdigris"]
    p.blot(cx + 14, cy + r * 0.92, r * 1.15, r * 0.14, verd, 0.5)
    p.add(f'<path d="M{f(cx - r * 0.9)},{f(cy + r * 0.95)} h{f(r * 2.3)}" stroke="{INK}" stroke-width="0.8" opacity="0.5"/>')
    d = ellipse_d(cx, cy, r, r * 0.96)
    p.shape(d, (cx - r, cy - r, cx + r, cy + r), fill=LIGHT,
            hatches=[(70, 3.0, 0.5, 0.8), (-20, 4.2, 0.4, 0.7), (35, 3.5, 0.3, 0.7)], sw=2.4, wash=verd, wash_op=0.3)
    # a lit left side: paper-coloured wedge over the hatching
    cid = p.uid("c")
    p.add(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><ellipse cx="{f(cx - r * 0.42)}" cy="{f(cy - r * 0.3)}" rx="{f(r * 0.5)}" ry="{f(r * 0.45)}" '
          f'fill="{LIGHT}" opacity="0.85" clip-path="url(#{cid})" filter="url(#wash)"/>')
    for k in range(4):
        a = p.rng.uniform(0, 6.28)
        x0, y0 = cx + r * 0.2 * math.cos(a), cy + r * 0.2 * math.sin(a)
        pts = jagged(p.rng, x0, y0, cx + r * 0.95 * math.cos(a), cy + r * 0.95 * math.sin(a), 4, 5)
        p.add(f'<clipPath id="{cid}k{k}"><path d="{d}"/></clipPath><path d="M' + " L".join(f"{f(a_)},{f(b_)}" for a_, b_ in pts)
              + f'" fill="none" stroke="{INK}" stroke-width="1" opacity="0.7" clip-path="url(#{cid}k{k})"/>')


def stone_slope(rng):
    p = Pen("p11", rng)
    verd, slate = WASH["verdigris"], WASH["slate"]
    p.add(plate_open())
    # sky, with a touch of slate where it meets the ridge
    p.sky_lines(IY0, 700, 8, 0.2, 0.03, IX0, IX1)
    p.wash(IX0 - 30, 150, 260, 500, slate, 0.26, "mist")
    ridge = "M" + " L".join(f"{x},{y}" for x, y in RIDGE)
    mass = ridge + " L70,935 C250,925 450,960 610,1000 L610,70 L300,70 Z"
    box = (IX0, IY0, IX1, 1010)
    p.shape(mass, box, fill="#e6dfce",
            hatches=[(62, 4.2, 0.42, 0.8), (-28, 7, 0.28, 0.7)], sw=2.4, wash=verd, wash_op=0.2)
    # darker on the shaded right side of the mountain
    p.hatch(mass, (440, IY0, IX1, 1010), [(62, 3.0, 0.45, 0.8), (20, 5, 0.32, 0.7)])
    p.hatch(mass, (IX0, 560, 330, 940), [(-40, 4.0, 0.3, 0.7)])
    # mossy washes: heavier low on the slope
    p.blot(250, 800, 130, 100, verd, 0.34, "softwash")
    p.blot(420, 640, 120, 90, verd, 0.3, "softwash")
    p.blot(220, 560, 60, 60, verd, 0.25, "softwash")
    # the worn track
    track = [(500, 395), (445, 440), (490, 500), (390, 560), (440, 630), (330, 700), (375, 770), (260, 840), (305, 895), (255, 950)]
    d = f"M{track[0][0]},{track[0][1]}"
    for (xa, ya), (xb, yb) in zip(track, track[1:]):
        d += f" Q{xa},{(ya + yb) / 2:.0f} {(xa + xb) / 2:.0f},{(ya + yb) / 2:.0f}"
    d += f" L{track[-1][0]},{track[-1][1]}"
    p.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="12" opacity="0.5" stroke-linejoin="round" stroke-linecap="round"/>'
          f'<path d="{d}" fill="none" stroke="#e9e2d1" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>')
    # rock outcrops, avoiding the track
    spots = 0
    while spots < 34:
        y = rng.uniform(120, 960)
        x = rng.uniform(_ridge_x(y) + 15, IX1 - 10)
        foot = 935 + (x - 70) * 0.12
        if y > foot - 15:
            continue
        if any(abs(x - tx) < 34 and abs(y - ty) < 34 for tx, ty in track) or (400 < x < 560 and 260 < y < 460):
            continue
        w = rng.uniform(14, 38) * (0.7 + (y - 100) / 1400)
        pts = []
        for k in range(9):
            a = k * 2 * math.pi / 9
            rr = w * rng.uniform(0.6, 1.1)
            pts.append((x + rr * math.cos(a) * 1.2, y + rr * math.sin(a) * 0.65))
        p.shape(poly_d(pts), (x - w, y - w, x + w, y + w * 0.4), fill="#eee8db",
                hatches=[(70, 2.6, 0.55, 0.7)], sw=1.4, wash=verd, wash_op=0.35)
        spots += 1
    p.scatter((300, 100, IX1, 960), 260, 11, 0.5, (0.3, 0.6), 0.7)
    # level ground at the foot and the boulder at rest
    ground = "M70,935 C250,925 450,960 610,1000 L610,1086 L70,1086 Z"
    p.shape(ground, (IX0, 920, IX1, IY1), fill="#ece5d6", hatches=[(0, 5, 0.3), (14, 8, 0.2)], sw=1.8, wash=verd, wash_op=0.18)
    p.scatter((IX0, 960, IX1, IY1), 120, 12, 0.0, (0.3, 0.5), 0.7)
    boulder(p, 200, 975, 66)
    # Sisyphus, walking down the track, arms loose, no stone
    walker_profile(p, 482, 430, 150, facing=-1, kind="tunic", pose="walk", tone=0.55, wash=verd, wash_op=0.25, stride=0.9)
    return finish(p, 0.4, True)


# ------------------------------------------------------------- XII compassion

def lying_stranger(p, x, y, s):
    caput, bone = WASH["caput"], WASH["bone"]
    p.blot(x + 95 * s, y, 105 * s, 7 * s, caput, 0.4)
    p.push(f"translate({f(x)},{f(y)}) scale({f(s)})")
    p.add(f'<path d="M0,0 L12,0 L12,-9 Z M-0,-2 l14,0" fill="{INK}"/><path d="M4,-12 L18,-12 L18,0 L4,0 Z" fill="{INK}" opacity="0.85"/>')
    blanket = "M10,0 C10,-18 40,-26 80,-28 C120,-32 150,-32 176,-26 L182,0 Z"
    p.shape(blanket, (0, -34, 184, 2), fill=FILL, hatches=[(80, 3.0, 0.45, 0.8), (20, 5, 0.3)], sw=2.0, s=s, wash=bone, wash_op=0.5)
    p.add(f'<path d="M40,-4 C60,-14 90,-16 120,-12 M70,-20 C90,-24 120,-22 150,-22" stroke="{INK}" stroke-width="{f(1 / s)}" fill="none" opacity="0.7"/>')
    p.shape(ellipse_d(196, -12, 14, 11), (180, -24, 212, 0), fill=FILL, hatches=[(70, 3, 0.3)], sw=1.8, s=s)
    p.add(f'<path d="M184,-14 C190,-26 206,-26 210,-16 C204,-20 192,-20 184,-14 Z" fill="{INK}" opacity="0.8"/>')
    p.add(f'<path d="M203,-11 q4,-2 8,0 M206,-6 q3,2 6,0 M200,-16 q3,-1 6,0" stroke="{INK}" stroke-width="{f(1.1 / s)}" fill="none"/>')
    p.pop()


def kneeling_woman(p, x, y, s):
    caput = WASH["caput"]
    p.blot(x, y, 60 * s, 6 * s, caput, 0.4)
    p.push(f"translate({f(x)},{f(y)}) scale({f(s)})")
    skirt = "M-34,0 L40,0 C38,-14 28,-28 14,-36 L-6,-36 C-20,-26 -30,-14 -34,0 Z"
    torso = "M10,-38 C14,-52 4,-70 -10,-78 L-24,-70 C-18,-60 -14,-48 -16,-36 Z"
    p.shape(skirt, (-40, -40, 44, 2), fill="#d9ccc4", hatches=[(70, 2.6, 0.7, 0.8), (-20, 3.6, 0.5)], sw=2.2, s=s, wash=caput, wash_op=0.55)
    p.add(f'<path d="M-24,-4 C-20,-16 -16,-26 -10,-34 M-6,-2 C-6,-14 -4,-24 0,-34 M12,-2 C12,-14 12,-24 12,-34" stroke="{INK}" stroke-width="{f(1.1 / s)}" fill="none" opacity="0.8"/>')
    p.shape(torso, (-30, -80, 16, -34), fill="#d9ccc4", hatches=[(70, 2.6, 0.7, 0.8), (-20, 3.6, 0.5)], sw=2.2, s=s, wash=caput, wash_op=0.55)
    p.limb([(-16, -70), (-38, -50), (-46, -26)], 6, "#d9ccc4", s)
    p.shape(ellipse_d(-47, -22, 6, 4), (-54, -27, -40, -17), sw=1.4, s=s)
    head(p, -27, -86, 8.5, nose=-1, hair=True, s=s)
    p.add(f'<circle cx="-15" cy="-90" r="4.5" fill="{INK}" opacity="0.85"/>')
    p.pop()


def boy_crouching(p, x, y, s):
    bone = WASH["bone"]
    p.blot(x, y, 28 * s, 4 * s, WASH["caput"], 0.35)
    p.push(f"translate({f(x)},{f(y)}) scale({f(s)})")
    p.limb([(10, -16), (-12, -14), (-14, -1)], 7, FILL, s)
    p.add(f'<path d="M-24,0 L-8,0" stroke="{INK}" stroke-width="{f(3 / s)}" stroke-linecap="round"/>')
    body = "M-6,-14 C-10,-30 -4,-46 6,-52 C16,-54 24,-42 22,-26 C22,-14 18,-6 12,-4 Z"
    p.shape(body, (-14, -56, 26, 0), fill="#dcd3c3", hatches=[(65, 2.6, 0.6, 0.8), (-25, 3.6, 0.4)], sw=2.0, s=s, wash=WASH["slate"], wash_op=0.25)
    p.limb([(-2, -44), (-18, -32), (-26, -22)], 5, FILL, s)
    p.shape("M-36,-24 L-18,-24 C-18,-13 -36,-13 -36,-24 Z", (-38, -26, -16, -12), fill=FILL, wash=bone, wash_op=0.8, sw=1.6, s=s)
    p.add(f'<path d="M-35,-23 L-19,-23" stroke="{INK}" stroke-width="{f(1 / s)}"/><path d="M-34,-22.5 q8,2 15,0" stroke="{INK}" stroke-width="{f(0.6 / s)}" fill="#fff" opacity="0.6"/>')
    head(p, -6, -61, 8, nose=-1, hair=True, s=s)
    p.pop()


def dog_lying(p, x, y, s):
    p.blot(x + 8 * s, y, 50 * s, 4 * s, WASH["caput"], 0.35)
    p.push(f"translate({f(x)},{f(y)}) scale({f(s)})")
    p.add(f'<path d="M-30,-6 C-42,-8 -50,-14 -52,-24" stroke="{INK}" stroke-width="{f(2.6 / s)}" fill="none" stroke-linecap="round"/>')
    body = "M-32,0 C-34,-14 -16,-26 6,-25 C20,-24 28,-20 32,-14 L38,0 Z"
    p.shape(body, (-36, -28, 40, 2), fill="#e0d8c8", hatches=[(75, 2.6, 0.55, 0.8)], sw=1.9, s=s)
    p.add(f'<path d="M-6,-20 C-2,-12 -2,-6 -6,-1 M4,-21 C8,-12 8,-6 4,-1 M14,-20 C18,-12 18,-6 14,-1" stroke="{INK}" stroke-width="{f(1 / s)}" fill="none" opacity="0.7"/>')
    p.shape(ellipse_d(-14, -10, 14, 11), (-28, -22, 0, 2), fill="#e0d8c8", hatches=[(70, 3, 0.35)], sw=1.5, s=s)
    # raised head resting toward the boy, ear and snout
    p.limb([(26, -16), (40, -26)], 8, "#e0d8c8", s)
    p.shape(ellipse_d(46, -26, 10, 8), (36, -34, 58, -18), fill="#e0d8c8", hatches=[(60, 3, 0.35)], sw=1.7, s=s)
    p.shape("M52,-27 L66,-20 L56,-18 Z", (50, -30, 68, -16), fill="#e0d8c8", sw=1.5, s=s)
    p.add(f'<circle cx="65" cy="-21" r="1.8" fill="{INK}"/><circle cx="49" cy="-28" r="1.2" fill="{INK}"/>')
    p.shape("M38,-33 L44,-46 L49,-33 Z", (36, -48, 52, -32), fill="#cfc3b0", hatches=[(80, 2, 0.5)], sw=1.3, s=s)
    # the forelegs stretched forward, the near one in a plain bandage
    p.limb([(22, -6), (50, -4)], 6, "#e0d8c8", s)
    p.add(f'<rect x="38" y="-8.6" width="11" height="9" fill="{LIGHT}" stroke="{INK}" stroke-width="{f(1.3 / s)}"/>'
          f'<path d="M40,-8 l7,8 M44,-8 l5,6 M38,-4 l5,4" stroke="{INK}" stroke-width="{f(0.7 / s)}"/>')
    p.pop()


def compassion(rng):
    p = Pen("p12", rng)
    caput, bone = WASH["caput"], WASH["bone"]
    p.add(plate_open())
    hor = 600
    # dusk sky: caput mortuum wash thinning to white at the horizon
    p.wash(IX0 - 40, IY0 - 40, IX1 - IX0 + 80, 520, caput, 0.34, "mist")
    p.sky_lines(IY0, hor, 7, 0.34, 0.04)
    # distant land and the road
    p.add(f'<path d="M{IX0},{hor} C200,{hor - 8} 300,{hor + 6} {IX1},{hor - 4}" stroke="{INK}" stroke-width="1" fill="none" opacity="0.7"/>')
    for k in range(18):
        p.bare_tree(rng.uniform(IX0, IX1), hor + rng.uniform(0, 4), rng.uniform(8, 18), op=0.45)
        # verge in the foreground, then the road running down through it
    p.shape("M70,895 C200,884 400,910 610,890 L610,1086 L70,1086 Z", (IX0, 880, IX1, IY1), fill="#e8e1d1",
            hatches=[(0, 5, 0.3), (12, 8, 0.2)], sw=1.4, wash=caput, wash_op=0.14)
    p.scatter((IX0, 900, IX1, IY1), 360, 16, 1.4, (0.3, 0.6), 0.8)
    road = "M396,602 L408,602 C420,700 420,880 410,1086 L200,1086 C230,880 380,700 396,602 Z"
    for y0 in range(606, 900, 8):
        p.add(f'<path d="M{IX0},{y0} L{IX1},{y0}" stroke="{INK}" stroke-width="0.6" opacity="{0.18 + (y0 - 600) / 1000:.2f}"/>')
    p.add(f'<path d="M396,602 L408,602 C420,700 420,880 410,1086 L200,1086 C230,880 380,700 396,602 Z" fill="#efe9db"/>')
    p.add(f'<path d="{road}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    p.add(f'<path d="M402,640 C412,760 400,900 360,1086 M406,640 C420,780 430,900 420,1086" stroke="{INK}" stroke-width="0.8" fill="none" opacity="0.45"/>')
    p.scatter((260, 800, 430, 1080), 60, 9, 0.0, (0.3, 0.5), 0.7)
    # a bare tree at the left, a milestone at the right
    p.bare_tree(150, 880, 330, op=0.9, width=9)
    mile = "M526,846 L526,800 C526,786 556,786 556,800 L558,846 Z"
    p.shape(mile, (520, 784, 562, 850), fill="#e6dfce", hatches=[(70, 2.4, 0.5, 0.7)], sw=2.0, wash=caput, wash_op=0.25)
    # the two groups
    lying_stranger(p, 82, 968, 0.85)
    kneeling_woman(p, 312, 980, 1.7)
    dog_lying(p, 440, 988, 1.3)
    boy_crouching(p, 560, 992, 1.4)
    return finish(p, 0.4, True)


# ------------------------------------------------------------- XIII the broom

def broom_clump(p, x, y, s):
    """Spanish broom: many thin, nearly leafless stems, yellow flowers on the upper part."""
    rng = p.rng
    verd, bone = WASH["verdigris"], WASH["bone"]
    stems, flowers = [], []
    n = 18
    for k in range(n):
        a = math.radians(-62 + k * 124 / (n - 1) + rng.uniform(-5, 5))
        ln = rng.uniform(120, 190) * s
        bx = x + rng.uniform(-8, 8) * s
        ex, ey = bx + ln * math.sin(a), y - ln * math.cos(a) * 0.95
        mx, my = bx + ln * 0.45 * math.sin(a) * 0.8 + rng.uniform(-8, 8), y - ln * 0.55
        stems.append((bx, y, mx, my, ex, ey))
        for j in range(rng.randint(8, 12)):
            t_ = rng.uniform(0.38, 1.0)
            fx = (1 - t_) ** 2 * bx + 2 * (1 - t_) * t_ * mx + t_ * t_ * ex + rng.uniform(-5, 5) * s
            fy = (1 - t_) ** 2 * y + 2 * (1 - t_) * t_ * my + t_ * t_ * ey + rng.uniform(-5, 5) * s
            flowers.append((fx, fy, rng.uniform(2.6, 4.4) * (0.7 + 0.4 * s)))
    d = " ".join(f"M{f(a)},{f(b)} Q{f(c)},{f(d_)} {f(e)},{f(g)}" for a, b, c, d_, e, g in stems)
    p.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(3.4 * s)}" stroke-linecap="round"/>'
          f'<path d="{d}" fill="none" stroke="{verd}" stroke-width="{f(2.0 * s)}" stroke-linecap="round" opacity="0.9"/>')
    for fx, fy, r in flowers:
        p.add(f'<circle cx="{f(fx)}" cy="{f(fy)}" r="{f(r)}" fill="{LIGHT}" stroke="{INK}" stroke-width="0.5"/>'
              f'<circle cx="{f(fx)}" cy="{f(fy)}" r="{f(r * 0.9)}" fill="{bone}" opacity="0.92"/>')


def ruins(p, x, y, s):
    """Broken walls and columns of a small Roman town, half buried."""
    p.push(f"translate({f(x)},{f(y)}) scale({f(s)})")
    wall = "M0,0 L0,-30 L10,-34 L16,-26 L30,-30 L36,-22 L50,-24 L56,-14 L70,-16 L72,0 Z"
    p.shape(wall, (0, -36, 72, 2), fill="#e4dcc8", hatches=[(90, 3, 0.5, 0.8), (0, 6, 0.35)], sw=1.6, s=s)
    arch = "M18,0 L18,-12 C18,-24 36,-24 36,-12 L36,0 Z"
    p.add(f'<path d="{arch}" fill="{INK}" opacity="0.7"/>')
    for cx_, h in [(90, 44), (112, 30), (134, 12)]:
        p.shape(poly_d([(cx_ - 6, 0), (cx_ - 5, -h), (cx_ + 5, -h), (cx_ + 6, 0)]), (cx_ - 6, -h, cx_ + 6, 0),
                fill="#ece5d6", hatches=[(90, 2.2, 0.5, 0.7)], sw=1.5, s=s)
        p.shape(poly_d([(cx_ - 8, -h), (cx_ + 8, -h), (cx_ + 8, -h - 4), (cx_ - 8, -h - 4)]), (cx_ - 8, -h - 4, cx_ + 8, -h),
                fill="#ece5d6", sw=1.4, s=s)
    p.shape(poly_d([(150, 0), (150, -18), (162, -22), (176, -14), (180, 0)]), (150, -22, 180, 0), fill="#e4dcc8",
            hatches=[(90, 3, 0.5)], sw=1.5, s=s)
    p.pop()


def broom_scene(rng):
    p = Pen("p13", rng)
    bone, slate, verd = WASH["bone"], WASH["slate"], WASH["verdigris"]
    p.add(plate_open())
    # pale sky washed in bone, a few thin lines
    p.wash(IX0 - 40, IY0 - 40, IX1 - IX0 + 80, 560, bone, 0.5, "mist")
    p.sky_lines(IY0, 520, 9, 0.18, 0.03)
    # Vesuvius: truncated cone at upper right, thin plume
    cone = "M230,520 C300,495 360,450 410,380 L450,320 L478,284 L494,296 L504,276 C516,272 526,284 536,300 L570,350 C590,390 604,430 612,450 L612,520 Z"
    p.shape(cone, (230, 260, 612, 525), fill="#e8e0cc", hatches=[(62, 3.4, 0.4, 0.8), (-30, 6, 0.25)], sw=2.0, wash=bone, wash_op=0.35, outline=False)
    p.add(f'<path d="{cone[:cone.index(" L612,520")]}" fill="none" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
    p.hatch(cone, (500, 260, 612, 525), [(62, 2.4, 0.5, 0.8), (20, 4, 0.35)])
    p.add(f'<path d="M470,300 C440,360 400,420 360,470 M520,320 C540,380 570,430 590,480" stroke="{INK}" stroke-width="0.8" fill="none" opacity="0.45"/>')
    plume = "M490,282 C480,240 520,210 500,170 C480,130 440,120 430,80"
    p.add(f'<path d="{plume}" fill="none" stroke="{slate}" stroke-width="26" opacity="0.28" stroke-linecap="round" filter="url(#wash)"/>'
          f'<path d="{plume}" fill="none" stroke="{slate}" stroke-width="10" opacity="0.3" stroke-linecap="round" filter="url(#wash)"/>'
          f'<path d="M486,280 C474,240 512,214 492,172 C474,134 438,122 428,84 M498,278 C490,244 530,214 512,172 C496,140 460,126 448,90" fill="none" stroke="{INK}" stroke-width="0.8" opacity="0.55"/>')
    # the plain behind: ruined town at far left, ground lines
    plain = "M70,560 C200,548 330,540 470,520 L612,520 L612,760 L70,760 Z"
    p.shape(plain, (IX0, 520, IX1, 760), fill="#eee8db", hatches=[(0, 5, 0.3)], sw=1.0, outline=False, wash=bone, wash_op=0.15)
    p.add(f'<path d="M70,560 C200,548 330,540 470,520" stroke="{INK}" stroke-width="1" fill="none" opacity="0.6"/>')
    ruins(p, 84, 668, 1.0)
    ruins(p, 238, 630, 0.6)
    # the lava slope, black and cracked
    lava = "M70,700 C130,712 190,690 250,680 C330,664 380,600 450,566 C520,534 570,520 612,516 L612,1086 L70,1086 Z"
    p.add(f'<path d="{lava}" fill="{INK}" opacity="0.88"/>')
    p.add(f'<clipPath id="p13lava"><path d="{lava}"/></clipPath><g clip-path="url(#p13lava)">')
    # plates of cooled lava, lit on their upper edges
    for _ in range(46):
        cx_, cy_ = rng.uniform(IX0, IX1), rng.uniform(520, IY1)
        w = rng.uniform(26, 70) * (0.5 + (cy_ - 500) / 700)
        pts = [(cx_ + w * math.cos(a) * rng.uniform(0.7, 1.2), cy_ + w * 0.36 * math.sin(a) * rng.uniform(0.7, 1.2))
               for a in [k * 2 * math.pi / 7 for k in range(7)]]
        p.add(f'<path d="{poly_d(pts)}" fill="#2f2b27" stroke="#8d8576" stroke-width="1" opacity="0.9"/>')
        p.add(f'<path d="M{f(pts[4][0])},{f(pts[4][1])} L{f(pts[5][0])},{f(pts[5][1])} L{f(pts[6][0])},{f(pts[6][1])}" stroke="#cfc6b2" stroke-width="1" fill="none" opacity="0.55"/>')
    for _ in range(40):
        x0, y0 = rng.uniform(IX0, IX1), rng.uniform(530, IY1)
        pts = jagged(rng, x0, y0, x0 + rng.uniform(-90, 90), y0 + rng.uniform(5, 40), 5, 7)
        p.add('<path d="M' + " L".join(f"{f(a)},{f(b)}" for a, b in pts) + '" fill="none" stroke="#d9d0bb" stroke-width="1" opacity="0.55"/>')
    p.scatter((IX0, 540, IX1, IY1), 400, 8, 0.2, (0.4, 0.6), 0.8, ink="#cfc6b2")
    p.add("</g>")
    p.add(f'<path d="{lava}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    # broom clumps, large in the foreground
    clumps = [(110, 860, 0.55), (310, 880, 0.7), (565, 830, 0.5), (500, 960, 0.95), (180, 1010, 1.05), (350, 1070, 1.1)]
    for x, y, s in sorted(clumps, key=lambda c: c[1]):
        broom_clump(p, x, y, s)
    return finish(p, 0.4, True)


# ------------------------------------------------------------ XIV stilled wheel

def wheel(p, cx, cy, R, tilt=-6):
    rng = p.rng
    verd = WASH["verdigris"]
    p.push(f"translate({f(cx)},{f(cy)}) rotate({tilt}) scale(1,0.98)")
    r_in = R - 22
    # spokes, hub and rim
    for k in range(12):
        a = math.radians(k * 30 + 8)
        p.limb([(26 * math.cos(a), 26 * math.sin(a)), ((r_in + 4) * math.cos(a), (r_in + 4) * math.sin(a))], 7.5, FILL)
    p.shape(ellipse_d(0, 0, 30, 30), (-32, -32, 32, 32), fill=FILL, hatches=[(70, 2.6, 0.5)], sw=2.2)
    p.shape(ellipse_d(0, 0, 11, 11), (-12, -12, 12, 12), fill=INK, sw=1.4)
    ring = ellipse_d(0, 0, R, R) + f" M{f(-r_in)},0 A{f(r_in)},{f(r_in)} 0 1 1 {f(r_in)},0 A{f(r_in)},{f(r_in)} 0 1 1 {f(-r_in)},0 Z"
    p.shape(ring, (-R, -R, R, R), fill=FILL, hatches=[(80, 3, 0.42, 0.8), (-20, 4.5, 0.3)], sw=2.6)
    for k in range(12):
        a = math.radians(k * 30)
        p.add(f'<path d="M{f(r_in * math.cos(a))},{f(r_in * math.sin(a))} L{f(R * math.cos(a))},{f(R * math.sin(a))}" stroke="{INK}" stroke-width="1.4" opacity="0.85"/>')
    for rr in (R - 8, R - 15):
        p.add(f'<circle cx="0" cy="0" r="{rr}" fill="none" stroke="{INK}" stroke-width="0.7" opacity="0.5"/>')
    # ivy growing over the rim along the lower left
    vine = []
    for k in range(40):
        a = math.radians(95 + k * 3.9)
        rr = R - 11 + rng.uniform(-9, 9)
        vx, vy = rr * math.cos(a), rr * math.sin(a)
        vine.append((vx, vy))
        ang = math.degrees(a) + rng.uniform(-60, 60)
        p.push(f"translate({f(vx)},{f(vy)}) rotate({f(ang)})")
        p.add(f'<path d="M0,0 C4,-8 14,-8 18,0 C14,8 4,8 0,0 Z" fill="{verd}" opacity="0.62" stroke="{INK}" stroke-width="0.9"/>'
              f'<path d="M2,0 L16,0" stroke="{INK}" stroke-width="0.5"/>')
        p.pop()
    p.add('<path d="M' + " L".join(f"{f(a)},{f(b)}" for a, b in vine) + f'" fill="none" stroke="{INK}" stroke-width="1.2" opacity="0.8"/>')
    p.pop()


def seated_back(p, x, y, s):
    """A robed figure on a low stone, seen from behind."""
    p.blot(x + 6, y, 60 * s, 5 * s, WASH["verdigris"], 0.4)
    p.push(f"translate({f(x)},{f(y)}) scale({f(s)})")
    stone_ = "M-42,0 L-38,-34 C-20,-40 20,-40 40,-34 L46,0 Z"
    p.shape(stone_, (-46, -42, 48, 2), fill="#e2dac6", hatches=[(70, 3, 0.5, 0.8), (-20, 5, 0.3)], sw=2.2, s=s, wash=WASH["verdigris"], wash_op=0.25)
    robe = "M-20,-30 C-26,-56 -22,-88 -13,-104 C-6,-110 8,-110 14,-104 C23,-88 27,-56 21,-30 Z"
    p.shape(robe, (-28, -112, 28, -28), fill="#e6dfce", hatches=[(75, 2.8, 0.55, 0.8), (-20, 4, 0.35)], sw=2.2, s=s)
    p.add(f'<path d="M-6,-100 C-8,-80 -8,-60 -10,-34 M6,-100 C8,-80 9,-60 12,-34" stroke="{INK}" stroke-width="{f(1.1 / s)}" fill="none" opacity="0.8"/>')
    head(p, 1, -118, 10, nose=1, hair=True, s=s)
    p.pop()


def stilled_wheel(rng):
    p = Pen("p14", rng)
    slate, verd = WASH["slate"], WASH["verdigris"]
    p.add(plate_open())
    # open sky, a small touch of slate
    p.wash(IX0 - 40, IY0 - 40, IX1 - IX0 + 80, 420, slate, 0.16, "mist")
    p.sky_lines(IY0, 600, 10, 0.12, 0.02)
    # far hills and the valley floor
    for base, amp, op, gap in [(600, 22, 0.16, 7), (640, 30, 0.26, 6), (690, 26, 0.34, 5)]:
        pts, x = [], IX0 - 20
        d = f"M{IX0 - 20},{base + 80}"
        while x <= IX1 + 20:
            d += f" L{f(x)},{f(base - amp * math.sin(x / 70 + base) - rng.uniform(0, 8))}"
            x += 18
        d += f" L{IX1 + 20},{base + 100} Z"
        p.shape(d, (IX0, base - amp - 10, IX1, base + 100), fill="#ece6d6", hatches=[(15, gap, 0.38, 0.7)], sw=1.3, wash=verd, wash_op=op + 0.1)
    floor = "M70,725 C200,715 330,730 470,718 L612,712 L612,905 C500,915 400,895 300,885 C200,878 120,888 70,880 Z"
    p.shape(floor, (IX0, 710, IX1, 910), fill="#eee8db", sw=1.4, wash=verd, wash_op=0.2)
    for k, (x0, y0, w, h, ang) in enumerate([(100, 765, 70, 20, 4), (250, 740, 60, 14, -3), (440, 790, 75, 22, 5), (140, 835, 60, 18, -5),
                                               (320, 805, 55, 24, 2), (510, 745, 50, 14, -2), (230, 855, 50, 14, 3)]):
        p.push(f"rotate({ang} {x0} {y0})")
        p.shape(ellipse_d(x0, y0, w, h), (x0 - w, y0 - h, x0 + w, y0 + h), fill="#e9e3d2", hatches=[(10 + k * 17, 3.4 + k % 3, 0.3, 0.7)],
                sw=0.8, outline=False, wash=verd, wash_op=0.12 + 0.05 * (k % 3))
        p.pop()
    # the river, a pale ribbon winding into the distance
    river = [(520, 705), (470, 722), (440, 745), (462, 772), (420, 800), (372, 818), (368, 846), (410, 870), (396, 890)]
    rd = f"M{river[0][0]},{river[0][1]}"
    for (xa, ya), (xb, yb) in zip(river, river[1:]):
        rd += f" Q{xa},{(ya + yb) / 2:.0f} {(xa + xb) / 2:.0f},{(ya + yb) / 2:.0f}"
    rd += f" L{river[-1][0]},{river[-1][1]}"
    p.add(f'<path d="{rd}" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round" opacity="0.8"/>'
          f'<path d="{rd}" fill="none" stroke="{LIGHT}" stroke-width="7" stroke-linecap="round"/>')
    # grass terrace in the foreground
    ground = "M70,880 C150,872 300,885 400,908 C480,924 560,922 612,916 L612,1086 L70,1086 Z"
    p.shape(ground, (IX0, 870, IX1, IY1), fill="#e8e1d1", hatches=[(0, 6, 0.28), (12, 9, 0.2)], sw=1.6, wash=verd, wash_op=0.3)
    p.scatter((IX0, 890, IX1, IY1), 420, 18, 1.45, (0.35, 0.7), 0.8)
    wheel(p, 222, 785, 150)
    seated_back(p, 520, 945, 1.7)
    # long grass in front of both
    p.scatter((IX0, 930, IX1, IY1), 260, 34, 1.4, (0.4, 0.8), 0.9)
    p.scatter((130, 900, 330, 960), 120, 30, 1.4, (0.4, 0.8), 0.9)
    return finish(p, 0.4, True)


# -------------------------------------------------------------- XV last messiah

def last_messiah(rng):
    p = Pen("p15", rng)
    slate, caput = WASH["slate"], WASH["caput"]
    p.add(plate_open())
    hor = 610
    # wide pale sky, slate wash dominant, light etched lines
    p.wash(IX0 - 40, IY0 - 40, IX1 - IX0 + 80, 600, slate, 0.34, "mist")
    p.sky_lines(IY0, hor, 7, 0.3, 0.04)
    # the plain: distant hills, then ground lines thickening toward the viewer
    for base, amp, op in [(hor - 6, 7, 0.22), (hor + 8, 9, 0.18)]:
        d = f"M{IX0},{base + 30}"
        x = IX0
        while x <= IX1:
            d += f" L{f(x)},{f(base - amp * math.sin(x / 55 + base))}"
            x += 15
        d += f" L{IX1},{base + 30} Z"
        p.shape(d, (IX0, base - amp, IX1, base + 30), fill="#e9e3d3", hatches=[(0, 4, 0.2)], sw=1.0, wash=slate, wash_op=op + 0.1)
    p.add(f'<path d="M{IX0},{hor + 8} L{IX1},{hor + 6}" stroke="{INK}" stroke-width="0.9" opacity="0.7"/>')
    for k in range(70):
        y = hor + 12 + (k ** 1.55) * 1.4
        if y > IY1:
            break
        op = 0.16 + 0.22 * min(1, (y - hor) / 460)
        p.add(f'<path d="M{IX0},{f(y)} L{IX1},{f(y + rng.uniform(-1.2, 1.2))}" stroke="{INK}" stroke-width="0.7" opacity="{op:.2f}"/>')
    p.wash(IX0 - 20, hor + 10, IX1 - IX0 + 40, 500, slate, 0.12, "softwash")
    p.scatter((IX0, hor + 20, IX1, IY1), 300, 12, 0.0, (0.25, 0.5), 0.7)
    # the speaker's rise at left
    rise = "M70,790 C98,720 128,664 172,652 C214,646 252,706 296,764 C332,806 372,822 410,836 L410,860 L70,860 Z"
    p.shape(rise, (IX0, 640, 420, 862), fill="#ebe4d4", hatches=[(70, 4, 0.38, 0.8), (-20, 6, 0.26)], sw=2.0, wash=slate, wash_op=0.22)
    p.scatter((IX0, 680, 300, 850), 70, 10, 1.3, (0.3, 0.6), 0.8)
    # the crowd, rows receding up the plain; faces mostly away from the speaker
    rows = [(805, 4), (850, 5), (900, 6), (955, 6), (1015, 6)]
    people = []
    for yb, n in rows:
        for k in range(n):
            x = 300 + (k + rng.uniform(0.0, 0.7)) * (300 / n) + (yb - 800) * 0.05
            y = yb + rng.uniform(-8, 8)
            h = (38 + (y - 800) * 0.26) * rng.uniform(0.92, 1.06)
            people.append((y, x, h))
    people.sort()
    for y, x, h in people:
        r = rng.random()
        if r < 0.18:
            walker_back(p, x, y, h * 0.62, tone=0.6, child=True, stride=rng.uniform(-1, 1))
        elif r < 0.42:
            walker_back(p, x, y, h, skirt=rng.random() < 0.5, hat=rng.random() < 0.3, look=-1, tone=0.55, stride=rng.uniform(-1.5, 1.5))
        elif r < 0.7:
            walker_back(p, x, y, h, skirt=rng.random() < 0.4, hat=rng.random() < 0.3, tone=0.55, stride=rng.uniform(-1.5, 1.5))
        else:
            walker_profile(p, x, y, h, facing=1, kind=rng.choice(["man", "woman"]), pose="walk", tone=0.5, stride=rng.uniform(0.7, 1.2))
    # a few stragglers out on the empty plain
    for x, y, h in [(520, 706, 20), (566, 696, 18), (478, 718, 22)]:
        walker_back(p, x, y, h, tone=0.6)
    # the speaker: plain coat touched with caput mortuum, one hand open toward the crowd
    walker_profile(p, 176, 652, 96, facing=1, kind="man", pose="open", tone=0.6, wash=caput, wash_op=0.6)
    return finish(p, 0.4, True)


# Card id -> drawing function
CARDS = {"08": porcupines, "09": shattered_god, "10": insomniac, "11": stone_slope, "12": compassion,
         "13": broom_scene, "14": stilled_wheel, "15": last_messiah}
