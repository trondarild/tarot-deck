"""Zen deck, The Way: cards I-X (Kuoan's ox-herding pictures), drawn inside the ensō."""

import math

from .common import (ENSO_CX, ENSO_CY, ENSO_R, GREY, INK, PALE, VERMILION, ZEN_PAPER,
                     enso_close, enso_open, enso_stroke, f, seal, svg)


def zen_searching(rng):
    ink, grey, pale, verm = INK, GREY, PALE, VERMILION
    cx, cy, r = ENSO_CX, ENSO_CY, ENSO_R
    out = [enso_open()]

    # Distant mountains: two layers of soft wash, ridge lines barely inked
    for layer, (base, amp, col, op) in enumerate([(470, 110, pale, 0.32), (530, 60, grey, 0.26)]):
        pts = []
        x = cx - r - 20
        while x < cx + r + 40:
            pts.append((x, base - amp * abs(math.sin(x / (90 + 40 * layer) + layer)) - rng.uniform(0, 18)))
            x += 18
        d = f"M{f(pts[0][0])},{base + 25} " + " ".join(f"L{f(a)},{f(b)}" for a, b in pts) + f" L{f(pts[-1][0])},{base + 25} Z"
        out.append(f'<path d="{d}" fill="{col}" opacity="{op}" filter="url(#softwash)"/>')
        ridge = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts)
        out.append(f'<path d="{ridge}" fill="none" stroke="{grey}" stroke-width="1.6" opacity="{0.35 + 0.2 * layer}" filter="url(#brush)"/>')

    # Plain: a faint ground wash below the hills
    out.append(f'<rect x="{cx - r}" y="575" width="{2 * r}" height="{r}" fill="#cfc6b6" opacity="0.12" filter="url(#wash)"/>')

    # Stream winding across the middle ground, left to lower right
    stream = "M 40,640 C 160,610 240,690 330,672 S 470,640 560,700 S 650,760 700,750"
    out.append(f'<path d="{stream}" fill="none" stroke="#e9e3d6" stroke-width="26" stroke-linecap="round"/>')
    out.append(f'<path d="{stream}" fill="none" stroke="{grey}" stroke-width="1.4" opacity="0.7" transform="translate(0,-12)" filter="url(#brush)"/>')
    out.append(f'<path d="{stream}" fill="none" stroke="{grey}" stroke-width="1.2" opacity="0.5" transform="translate(4,13)" filter="url(#brush)"/>')

    # Maples at the right edge: trunks, branches, ink-blot leaf clusters
    for tx, th, tw in [(560, 360, 9), (612, 420, 12), (520, 300, 6)]:
        base_y = 700
        top = base_y - th
        out.append(f'<path d="M{tx},{base_y} C{tx - 8},{base_y - th * 0.4} {tx + 10},{base_y - th * 0.7} {tx - 4},{top}" '
                   f'fill="none" stroke="{ink}" stroke-width="{tw}" stroke-linecap="round" filter="url(#dry)"/>')
        for _ in range(7):
            by = rng.uniform(top + 20, base_y - th * 0.35)
            bx = tx + rng.uniform(-6, 6)
            ex = bx + rng.choice([-1, 1]) * rng.uniform(40, 90)
            ey = by - rng.uniform(20, 60)
            out.append(f'<path d="M{f(bx)},{f(by)} Q{f((bx + ex) / 2)},{f(by - 10)} {f(ex)},{f(ey)}" fill="none" '
                       f'stroke="{ink}" stroke-width="{rng.uniform(1.5, 3.5):.1f}" stroke-linecap="round" filter="url(#brush)"/>')
            for _ in range(9):
                lx, ly = ex + rng.gauss(0, 18), ey + rng.gauss(0, 14)
                s = rng.uniform(4, 9)
                out.append(f'<path d="M{f(lx)},{f(ly)} l{f(s)},{f(-s * 0.4)} l{f(-s * 0.3)},{f(s)} z" fill="{rng.choice([ink, grey, grey])}" '
                           f'opacity="{rng.uniform(0.5, 0.9):.2f}" transform="rotate({rng.uniform(0, 360):.0f} {f(lx)} {f(ly)})"/>')

    # Tall wild grass across the foreground
    for _ in range(420):
        gx = rng.uniform(cx - r, cx + r)
        gy = rng.uniform(700, 900)
        h = rng.uniform(25, 85) * (0.6 + (gy - 700) / 300)
        lean = rng.uniform(-18, 22)
        col = rng.choice([ink, grey, grey, pale])
        out.append(f'<path d="M{f(gx)},{f(gy)} q{f(lean * 0.3)},{f(-h * 0.6)} {f(lean)},{f(-h)}" fill="none" stroke="{col}" '
                   f'stroke-width="{rng.uniform(0.6, 1.8):.1f}" stroke-linecap="round" opacity="{rng.uniform(0.45, 0.95):.2f}"/>')

    # The herdsman: small, left of centre, shading his eyes, rope in hand
    hx, hy = 255, 668  # feet
    fig = [
        # legs and sandals
        f'<path d="M{hx - 6},{hy} L{hx - 3},{hy - 30} M{hx + 7},{hy} L{hx + 4},{hy - 30}" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>',
        # short robe, tied at the waist
        f'<path d="M{hx - 15},{hy - 26} Q{hx},{hy - 34} {hx + 15},{hy - 26} L{hx + 10},{hy - 62} Q{hx},{hy - 68} {hx - 10},{hy - 62} Z" '
        f'fill="#f1ece2" stroke="{ink}" stroke-width="2.2" filter="url(#brush)"/>',
        f'<path d="M{hx - 11},{hy - 44} L{hx + 11},{hy - 44}" stroke="{ink}" stroke-width="2"/>',
        # head, turned slightly left
        f'<circle cx="{hx - 1}" cy="{hy - 75}" r="8" fill="#f1ece2" stroke="{ink}" stroke-width="2"/>',
        f'<path d="M{hx - 8},{hy - 79} Q{hx - 1},{hy - 87} {hx + 7},{hy - 80}" stroke="{ink}" stroke-width="3" fill="none"/>',
        # right arm raised, hand shading the eyes
        f'<path d="M{hx + 8},{hy - 60} Q{hx + 14},{hy - 74} {hx - 4},{hy - 80}" stroke="{ink}" stroke-width="2.6" fill="none" stroke-linecap="round"/>',
        # left arm down, holding the coiled rope
        f'<path d="M{hx - 8},{hy - 60} Q{hx - 18},{hy - 46} {hx - 20},{hy - 36}" stroke="{ink}" stroke-width="2.6" fill="none" stroke-linecap="round"/>',
    ]
    for k in range(3):
        fig.append(f'<ellipse cx="{hx - 22}" cy="{hy - 30 + k * 2}" rx="{9 - k}" ry="{5 - k * 0.6:.1f}" fill="none" stroke="{verm}" stroke-width="2"/>')
    out += fig
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


# ------------------------------------------------------------ shared figures

ROBE = "#f1ece2"   # the herdsman's robe and skin, as in card I
OX = "#2b2926"     # the water ox: one colour on every card
OX_HORN = "#55514b"


def _pt(x, y, s, flip, lx, ly):
    return (x + (-lx if flip else lx) * s, y + ly * s)


# Poses in local units (feet at 0,0, facing +x, about 100 high): hip, shoulder,
# legs as (knee, foot), arms as (elbow, hand), optional head offset.
HERDSMAN_POSES = {
    "stand": dict(hip=(0, -48), sh=(0, -82),
                  legs=[((-3, -25), (-7, 0)), ((3, -25), (8, 0))],
                  arms=[((-8, -65), (-12, -50)), ((8, -65), (12, -50))]),
    "crouch": dict(hip=(-6, -34), sh=(12, -56), head=(26, -58),
                   legs=[((10, -38), (-2, 0)), ((16, -28), (14, 0))],
                   arms=[((24, -38), (34, -16)), ((4, -40), (0, -26))]),
    "surprise": dict(hip=(0, -48), sh=(1, -82),
                     legs=[((-3, -25), (-7, 0)), ((4, -25), (9, 0))],
                     arms=[((-9, -64), (-14, -46)), ((13, -88), (15, -108))]),
    "pull": dict(hip=(2, -48), sh=(-16, -80),
                 legs=[((10, -26), (18, 0)), ((-12, -28), (-24, 0))],
                 arms=[((-2, -72), (12, -64)), ((2, -66), (16, -58))]),
    "walk": dict(hip=(0, -48), sh=(3, -82),
                 legs=[((8, -26), (16, 0)), ((-5, -26), (-14, -2))],
                 arms=[((12, -66), (17, -52)), ((-6, -64), (-12, -48))]),
    "ride": dict(hip=(0, -28), sh=(-2, -62),
                 legs=[((9, -26), (6, 0)), ((14, -30), (15, -2))],
                 arms=[((10, -56), (14, -70)), ((14, -62), (26, -68))]),
    "sit": dict(hip=(0, -12), sh=(0, -50), lap=34,
                legs=[((-26, -6), (8, -2)), ((26, -6), (-8, -2))],
                arms=[((-14, -32), (-4, -18)), ((14, -32), (4, -18))]),
}


def herdsman(x, y, s=1.0, pose="stand", flip=False, pale_legs=False):
    """The young herdsman. Returns (svg, anchors); anchors holds hand and head points."""
    p = HERDSMAN_POSES[pose]
    P = lambda q: _pt(x, y, s, flip, q[0], q[1])
    hip, sh = P(p["hip"]), P(p["sh"])
    ax, ay = sh[0] - hip[0], sh[1] - hip[1]
    n = math.hypot(ax, ay)
    ux, uy = ax / n, ay / n          # up the torso
    nx, ny = -uy, ux
    hd = P(p["head"]) if "head" in p else (sh[0] + ux * 15 * s, sh[1] + uy * 15 * s)
    out = []
    sw = lambda w: f"{w * max(s, 0.6):.1f}"
    for knee, foot in p["legs"]:
        k, ft = P(knee), P(foot)
        out.append(f'<path d="M{f(hip[0])},{f(hip[1])} L{f(k[0])},{f(k[1])} L{f(ft[0])},{f(ft[1])}" fill="none" '
                   f'stroke="{INK}" stroke-width="{sw(3)}" stroke-linecap="round" stroke-linejoin="round"/>')
        if pale_legs:
            out.append(f'<path d="M{f(hip[0])},{f(hip[1])} L{f(k[0])},{f(k[1])} L{f(ft[0])},{f(ft[1])}" fill="none" '
                       f'stroke="{ROBE}" stroke-width="{sw(1.4)}" stroke-linecap="round" stroke-linejoin="round"/>')
        d = -1 if flip else 1
        out.append(f'<path d="M{f(ft[0] - 3 * d * s)},{f(ft[1] + 1.5 * s)} L{f(ft[0] + 8 * d * s)},{f(ft[1] + 1.5 * s)}" '
                   f'stroke="{INK}" stroke-width="{sw(2.6)}" stroke-linecap="round"/>')
    hem = (hip[0] - ux * 16 * s, hip[1] - uy * 16 * s)
    a = (sh[0] + nx * 11 * s, sh[1] + ny * 11 * s)
    b = (sh[0] - nx * 11 * s, sh[1] - ny * 11 * s)
    c = (hem[0] - nx * 16 * s, hem[1] - ny * 16 * s)
    e = (hem[0] + nx * 16 * s, hem[1] + ny * 16 * s)
    out.append(f'<path d="M{f(a[0])},{f(a[1])} L{f(b[0])},{f(b[1])} L{f(c[0])},{f(c[1])} L{f(e[0])},{f(e[1])} Z" '
               f'fill="{ROBE}" stroke="{INK}" stroke-width="{sw(2.2)}" stroke-linejoin="round" filter="url(#brush)"/>')
    if "lap" in p:
        l1, l2, l3 = P((-p["lap"], -3)), P((p["lap"], -3)), P((0, -30))
        out.append(f'<path d="M{f(l1[0])},{f(l1[1])} Q{f(l3[0])},{f(l3[1])} {f(l2[0])},{f(l2[1])} Q{f(P((0, 6))[0])},{f(P((0, 6))[1])} {f(l1[0])},{f(l1[1])} Z" '
                   f'fill="{ROBE}" stroke="{INK}" stroke-width="{sw(2.2)}" stroke-linejoin="round" filter="url(#brush)"/>')
    w1 = (hip[0] + nx * 13 * s, hip[1] + ny * 13 * s)
    w2 = (hip[0] - nx * 13 * s, hip[1] - ny * 13 * s)
    out.append(f'<path d="M{f(w1[0])},{f(w1[1])} L{f(w2[0])},{f(w2[1])}" stroke="{INK}" stroke-width="{sw(2)}"/>')
    hands = []
    for elbow, hand in p["arms"]:
        el, hn = P(elbow), P(hand)
        hands.append(hn)
        out.append(f'<path d="M{f(sh[0])},{f(sh[1])} Q{f(el[0])},{f(el[1])} {f(hn[0])},{f(hn[1])}" fill="none" '
                   f'stroke="{INK}" stroke-width="{sw(2.6)}" stroke-linecap="round"/>')
    out.append(f'<circle cx="{f(hd[0])}" cy="{f(hd[1])}" r="{f(8.5 * s)}" fill="{ROBE}" stroke="{INK}" stroke-width="{sw(2)}"/>')
    hx, hy = hd
    r = 8.5 * s
    out.append(f'<path d="M{f(hx - r)},{f(hy - r * 0.2)} Q{f(hx - r * 0.1)},{f(hy - r * 1.6)} {f(hx + r)},{f(hy - r * 0.3)}" '
               f'stroke="{INK}" stroke-width="{sw(3.2)}" fill="none" stroke-linecap="round"/>')
    return "".join(out), {"hands": hands, "head": hd, "hip": hip, "sh": sh}


def coil(x, y, col=VERMILION, s=1.0):
    return "".join(f'<ellipse cx="{f(x)}" cy="{f(y + k * 2 * s)}" rx="{f((9 - k) * s)}" ry="{f((5 - k * 0.6) * s)}" '
                   f'fill="none" stroke="{col}" stroke-width="{f(2 * s)}"/>' for k in range(3))


def rope(a, b, sag=0.0, col=VERMILION, w=2.4):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + sag
    return (f'<path d="M{f(a[0])},{f(a[1])} Q{f(mx)},{f(my)} {f(b[0])},{f(b[1])}" fill="none" stroke="{col}" '
            f'stroke-width="{w}" stroke-linecap="round"/>')


OX_POSES = {
    "stand": dict(hc=(120, -68), ang=38, legs=[(-58, 2, 0), (56, -2, 0), (-72, 0, 0), (64, 2, 0)]),
    "walk": dict(hc=(120, -66), ang=38, legs=[(-58, 14, 0), (56, -14, 4), (-72, -14, 8), (64, 16, 0)]),
    "pull": dict(hc=(116, -42), ang=64, legs=[(-58, -8, 0), (56, 26, 0), (-72, -14, 0), (64, 30, 0)]),
    "ride": dict(hc=(118, -56), ang=50, legs=[(-58, 14, 0), (56, -14, 4), (-72, -14, 8), (64, 16, 0)]),
}


def ox(x, y, s=1.0, pose="stand", flip=False, head=True):
    """The dark water ox, facing +x (or -x when flipped); y is the ground under it.
    Returns (svg, anchors) with nose, neck and back points."""
    p = OX_POSES[pose]
    P = lambda lx, ly: _pt(x, y, s, flip, lx, ly)
    g = []
    d = -1 if flip else 1
    # far legs first, then body, then near legs
    def leg(hx, dx, lift):
        kx, ky = hx + dx * 0.4, -34
        fx, fy = hx + dx, -lift
        return (f'<path d="M{hx},-62 L{kx},{ky}" stroke="{OX}" stroke-width="15" stroke-linecap="round"/>'
                f'<path d="M{kx},{ky} L{fx},{fy - 3}" stroke="{OX}" stroke-width="9" stroke-linecap="round"/>'
                f'<path d="M{fx - 5},{fy} L{fx + 5},{fy}" stroke="{OX}" stroke-width="5" stroke-linecap="round"/>')
    legs = p["legs"]
    g.append(leg(*legs[0]) + leg(*legs[1]))
    g.append(f'<path d="M-90,-78 C-92,-100 -55,-106 -15,-102 C20,-100 42,-112 68,-102 L86,-70 C80,-52 50,-50 20,-50 '
             f'C-20,-48 -60,-50 -78,-56 C-90,-60 -92,-70 -90,-78 Z" fill="{OX}" filter="url(#brush)"/>')
    g.append(f'<path d="M-80,-98 C-40,-106 10,-100 40,-106" fill="none" stroke="{OX_HORN}" stroke-width="2.2" '
             f'opacity="0.7" filter="url(#dry)"/>')
    g.append(f'<path d="M-88,-84 C-102,-70 -104,-46 -98,-30" fill="none" stroke="{OX}" stroke-width="4" stroke-linecap="round"/>'
             f'<ellipse cx="-98" cy="-24" rx="4" ry="9" fill="{OX}"/>')
    g.append(leg(*legs[2]) + leg(*legs[3]))
    anchors = {"back": P(0, -104), "neck": P(88, -80)}
    if head:
        hx, hy = p["hc"]
        ang = p["ang"]
        g.append(f'<path d="M62,-88 L{hx - 6},{hy}" stroke="{OX}" stroke-width="44" stroke-linecap="round"/>')
        horn = f'M-8,-10 C-18,-28 -42,-30 -54,-12'
        g.append(f'<g transform="translate({hx},{hy}) rotate({ang})">'
                 f'<path d="{horn}" fill="none" stroke="{OX_HORN}" stroke-width="7" stroke-linecap="round"/>'
                 f'<path d="M-12,-4 C-26,-6 -30,-14 -24,-22 C-16,-18 -12,-12 -12,-4 Z" fill="{OX}"/>'
                 f'<ellipse cx="0" cy="0" rx="27" ry="15" fill="{OX}"/>'
                 f'<ellipse cx="26" cy="3" rx="11" ry="10" fill="{OX}"/>'
                 f'<circle cx="7" cy="-4" r="1.8" fill="{ZEN_PAPER}"/></g>')
        a = math.radians(ang)
        nx_ = hx + 34 * math.cos(a) - 8 * math.sin(a)
        ny_ = hy + 34 * math.sin(a) + 8 * math.cos(a)
        anchors["nose"] = P(nx_, ny_)
        anchors["neck"] = P(hx - 34, hy + 8 if ang > 45 else hy + 4)
    return f'<g transform="translate({f(x)},{f(y)}) scale({f(d * s)},{f(s)})">' + "".join(g) + "</g>", anchors


# ------------------------------------------------------------ shared scenery

def hills(rng, layers, x0=40, x1=640):
    """layers: (base, amp, colour, opacity, period) soft wash hills with a faint ridge line."""
    out = []
    for layer, (base, amp, col, op, per) in enumerate(layers):
        pts, x = [], x0
        while x < x1:
            pts.append((x, base - amp * abs(math.sin(x / per + layer * 1.7)) - rng.uniform(0, 12)))
            x += 18
        d = f"M{f(pts[0][0])},{base + 25} " + " ".join(f"L{f(a)},{f(b)}" for a, b in pts) + f" L{f(pts[-1][0])},{base + 25} Z"
        out.append(f'<path d="{d}" fill="{col}" opacity="{op}" filter="url(#softwash)"/>')
        out.append(f'<path d="M{" L".join(f"{f(a)},{f(b)}" for a, b in pts)}" fill="none" stroke="{GREY}" stroke-width="1.4" '
                   f'opacity="{0.25 + 0.1 * layer}" filter="url(#brush)"/>')
    return "".join(out)


def grass(rng, x0, x1, y0, y1, n, hmin=20, hmax=70, tall=True):
    out = []
    for _ in range(n):
        gx, gy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        h = rng.uniform(hmin, hmax) * (0.7 + 0.5 * (gy - y0) / max(1, y1 - y0))
        lean = rng.uniform(-14, 16)
        col = rng.choice([INK, GREY, GREY, PALE])
        out.append(f'<path d="M{f(gx)},{f(gy)} q{f(lean * 0.3)},{f(-h * 0.6)} {f(lean)},{f(-h)}" fill="none" stroke="{col}" '
                   f'stroke-width="{rng.uniform(0.6, 1.7):.1f}" stroke-linecap="round" opacity="{rng.uniform(0.45, 0.95):.2f}"/>')
    return "".join(out)


def trunk(rng, x, base, top, w, lean=0.0, col=INK, leafy=0):
    """A tree trunk in dry brush, with a few bark lines and optional bare branches."""
    out = [f'<path d="M{x},{base} C{x - 8 + lean * 0.3},{base - (base - top) * 0.4} {x + 8 + lean * 0.7},{base - (base - top) * 0.7} '
           f'{x + lean},{top}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" filter="url(#dry)"/>']
    for _ in range(int(w)):
        yy = rng.uniform(top + 20, base - 10)
        xx = x + lean * (base - yy) / (base - top) + rng.uniform(-w / 3, w / 3)
        out.append(f'<path d="M{f(xx)},{f(yy)} l{rng.uniform(-1, 1):.1f},{f(rng.uniform(10, 26))}" stroke="{PALE}" stroke-width="1" opacity="0.6"/>')
    for _ in range(leafy):
        by = rng.uniform(top, top + (base - top) * 0.45)
        bx = x + lean * (base - by) / (base - top)
        ex, ey = bx + rng.choice([-1, 1]) * rng.uniform(30, 70), by - rng.uniform(15, 45)
        out.append(f'<path d="M{f(bx)},{f(by)} Q{f((bx + ex) / 2)},{f(by - 8)} {f(ex)},{f(ey)}" fill="none" stroke="{col}" '
                   f'stroke-width="{rng.uniform(1.5, 3.2):.1f}" stroke-linecap="round" filter="url(#brush)"/>')
        for _ in range(7):
            lx, ly = ex + rng.gauss(0, 14), ey + rng.gauss(0, 10)
            sz = rng.uniform(4, 8)
            out.append(f'<path d="M{f(lx)},{f(ly)} l{f(sz)},{f(-sz * 0.4)} l{f(-sz * 0.3)},{f(sz)} z" fill="{rng.choice([INK, GREY])}" '
                       f'opacity="{rng.uniform(0.5, 0.85):.2f}"/>')
    return "".join(out)


def willow(rng, x, base, top, w, lean=0.0, fronds=26, spread=70):
    out = [trunk(rng, x, base, top, w, lean)]
    tx = x + lean
    for _ in range(fronds):
        t = rng.uniform(0.0, 1.0)
        sx = tx + rng.uniform(-spread, spread) * 0.5
        sy = top + rng.uniform(0, 30)
        ex = sx + rng.uniform(-spread, spread) * 0.8
        ey = sy - rng.uniform(5, 25)
        out.append(f'<path d="M{f(tx)},{f(top + 15)} Q{f((tx + sx) / 2)},{f(top - 20)} {f(sx)},{f(sy)}" fill="none" stroke="{INK}" '
                   f'stroke-width="{rng.uniform(1.2, 2.4):.1f}" opacity="0.75" stroke-linecap="round"/>')
        L = rng.uniform(70, 150)
        sway = rng.uniform(-10, 10)
        out.append(f'<path d="M{f(sx)},{f(sy)} q{f(sway)},{f(L * 0.5)} {f(sway * 0.4)},{f(L)}" fill="none" '
                   f'stroke="{rng.choice([GREY, PALE, GREY])}" stroke-width="{rng.uniform(0.8, 1.6):.1f}" opacity="{rng.uniform(0.5, 0.9):.2f}"/>')
    return "".join(out)


def mist(x, y, w, h, op=0.8):
    return f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{h}" fill="{ZEN_PAPER}" opacity="{op}" filter="url(#mist)"/>'


def rock(rng, x, y, w, h, col=GREY, op=0.55):
    pts = []
    for k in range(9):
        a = math.pi * k / 8
        pts.append((x + w * math.cos(a) * rng.uniform(0.85, 1.05), y - h * math.sin(a) * rng.uniform(0.8, 1.05)))
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts) + " Z"
    return (f'<path d="{d}" fill="{col}" opacity="{op}" filter="url(#brush)"/>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.6" opacity="0.8" filter="url(#brush)"/>')


def ground(y, x0=40, x1=640, col="#cfc6b6", op=0.18, wob=0):
    return (f'<path d="M{x0},{y} Q{(x0 + x1) / 2},{y - 10 + wob} {x1},{y + 4} L{x1},{y + 260} L{x0},{y + 260} Z" '
            f'fill="{col}" opacity="{op}" filter="url(#wash)"/>'
            f'<path d="M{x0},{y} Q{(x0 + x1) / 2},{y - 10 + wob} {x1},{y + 4}" fill="none" stroke="{GREY}" stroke-width="1.6" '
            f'opacity="0.6" filter="url(#brush)"/>')


def moon(x, y, r):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e6dfd0" opacity="0.7" filter="url(#wash)"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{PALE}" stroke-width="2" opacity="0.8" filter="url(#brush)"/>')


# ------------------------------------------------------------ cards II-X

def hoofprint(x, y, s, ang):
    half = "M-3.5,-15 C-13,-9 -14,8 -6,14 C-4,6 -3.5,-4 -3.5,-15 Z"
    return (f'<g transform="translate({f(x)},{f(y)}) scale(1,0.72) rotate({ang}) scale({f(s)})">'
            f'<ellipse cx="0" cy="0" rx="14" ry="17" fill="{GREY}" opacity="0.22" filter="url(#wash)"/>'
            f'<path d="{half}" fill="{INK}" opacity="0.85"/><path d="{half}" fill="{INK}" opacity="0.85" transform="scale(-1,1)"/></g>')


def zen_traces(rng):
    out = [enso_open()]
    out.append(hills(rng, [(470, 80, PALE, 0.28, 110)]))
    # stream behind the bank
    stream = "M40,620 C190,585 360,650 650,575"
    out.append(f'<path d="{stream}" fill="none" stroke="#e4ded0" stroke-width="44" stroke-linecap="round"/>')
    out.append(f'<path d="{stream}" fill="none" stroke="{GREY}" stroke-width="1.4" opacity="0.7" transform="translate(0,-22)" filter="url(#brush)"/>')
    out.append(f'<path d="{stream}" fill="none" stroke="{GREY}" stroke-width="1.2" opacity="0.5" transform="translate(0,24)" filter="url(#brush)"/>')
    for _ in range(14):
        sx = rng.uniform(80, 600)
        out.append(f'<path d="M{f(sx)},{f(rng.uniform(595, 625))} q10,-3 22,0" stroke="{PALE}" stroke-width="1.2" fill="none" opacity="0.8"/>')
    # trunks behind
    out.append(trunk(rng, 110, 670, 250, 34, 8, leafy=5))
    out.append(trunk(rng, 215, 640, 300, 22, -6, leafy=3))
    out.append(trunk(rng, 575, 620, 250, 28, 10, leafy=4))
    out.append(ground(660))
    # mud along the diagonal
    out.append(f'<path d="M190,790 L520,660" stroke="#a79e8f" stroke-width="60" stroke-linecap="round" opacity="0.28" filter="url(#softwash)"/>')
    pts = [(250, 790), (292, 763), (330, 741), (366, 722), (400, 706), (432, 693), (462, 682), (488, 673)]
    for i, (px, py) in enumerate(pts):
        sc = 1.6 - 0.09 * i
        off = 7 if i % 2 else -7
        out.append(hoofprint(px + off * 0.5, py + off, sc, 52))
    out.append(grass(rng, 40, 640, 770, 840, 70, 25, 60))
    # figure, crouching at the bank and looking down at the first prints
    fig, a = herdsman(200, 745, 1.55, "crouch")
    out.append(fig)
    hnd = a["hands"][1]
    out.append(coil(hnd[0] - 4, hnd[1] + 8, VERMILION, 1.1))
    out.append(rope(hnd, (hnd[0] - 30, hnd[1] + 30), 6))
    # tall grass swallows the prints at the right
    out.append(grass(rng, 470, 620, 650, 700, 150, 45, 110))
    out.append(grass(rng, 40, 120, 680, 720, 30, 30, 70))
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


def zen_seeing(rng):
    out = [enso_open()]
    out.append(hills(rng, [(480, 90, PALE, 0.28, 120), (540, 40, GREY, 0.2, 80)]))
    # a stream down the middle, between the two banks
    left = "M345,560 C310,640 345,730 270,845"
    right = "M372,560 C360,640 450,730 470,845"
    out.append(f'<path d="{left} L470,845 C450,730 360,640 372,560 Z" fill="#ddd7c9" opacity="0.8"/>')
    out.append(f'<path d="{left}" fill="none" stroke="{GREY}" stroke-width="1.6" opacity="0.7" filter="url(#brush)"/>')
    out.append(f'<path d="{right}" fill="none" stroke="{GREY}" stroke-width="1.6" opacity="0.7" filter="url(#brush)"/>')
    for k in range(16):
        t = k / 15
        yy = 580 + 250 * t
        cxm = 358 + (-8 + 20 * t) * t * 6 + rng.uniform(-6, 6)
        out.append(f'<path d="M{f(cxm - 14 - 24 * t)},{f(yy)} q{f(12 + 10 * t)},-4 {f(26 + 30 * t)},0" stroke="{GREY}" stroke-width="1.2" fill="none" opacity="0.6"/>')
    # far bank: ox behind willow trunks
    o, oa = ox(500, 700, 0.95, "stand", flip=False, head=False)
    out.append(ground(700, 385, 640))
    out.append(mist(500, 700, 150, 22, 0.7))
    out.append(mist(360, 590, 200, 24, 0.8))
    out.append(o)
    out.append(willow(rng, 575, 725, 360, 24, -12, 30, 110))
    out.append(willow(rng, 440, 705, 390, 16, 10, 22, 80))
    # bird on a branch
    bx, by = 470, 447
    out.append(f'<path d="M{bx - 40},{by + 9} L{bx + 30},{by + 6}" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
    out.append(f'<ellipse cx="{bx}" cy="{by}" rx="9" ry="6" fill="{INK}"/><circle cx="{bx + 8}" cy="{by - 4}" r="4" fill="{INK}"/>'
               f'<path d="M{bx - 8},{by} L{bx - 24},{by + 6}" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
               f'<path d="M{bx + 11},{by - 4} l6,1" stroke="{INK}" stroke-width="1.6"/>')
    # near bank, left
    out.append(ground(720, 40, 300))
    out.append(grass(rng, 60, 300, 735, 830, 120, 25, 70))
    fig, a = herdsman(175, 740, 1.5, "surprise")
    out.append(fig)
    hn = a["hands"][0]
    out.append(coil(hn[0] - 2, hn[1] + 8, VERMILION, 1.1))
    out.append(grass(rng, 380, 620, 770, 835, 50, 25, 60))
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


def zen_catching(rng):
    out = [enso_open()]
    out.append(f'<path d="M80,470 Q300,445 620,480" stroke="{PALE}" stroke-width="40" stroke-linecap="round" opacity="0.22" filter="url(#mist)"/>')
    out.append(hills(rng, [(560, 50, PALE, 0.22, 100)]))
    # windswept tree, leaning away from the wind to the right
    out.append(trunk(rng, 255, 735, 460, 14, 40, leafy=0))
    for k in range(7):
        bx = 255 + 40 * (735 - (520 + k * 28)) / 275
        by = 520 + k * 28
        out.append(f'<path d="M{f(bx)},{f(by)} q40,{-8 - k} {70 + k * 6},{-16 + k * 4}" stroke="{INK}" stroke-width="{3 - k * 0.25:.1f}" '
                   f'fill="none" stroke-linecap="round" filter="url(#brush)"/>')
    out.append(ground(735, 40, 640, col="#b8ae9c", op=0.28))
    # the ox, braced, facing the man
    o, oa = ox(480, 745, 1.15, "pull", flip=True)
    out.append(o)
    fig, a = herdsman(205, 745, 1.6, "pull")
    out.append(fig)
    h1, h2 = a["hands"]
    neck = oa["neck"]
    out.append(f'<ellipse cx="{f(neck[0])}" cy="{f(neck[1] - 4)}" rx="12" ry="26" fill="none" stroke="{VERMILION}" stroke-width="3.2" '
               f'transform="rotate(-16 {f(neck[0])} {f(neck[1])})"/>')
    tgt = (neck[0] - 10, neck[1] - 8)
    out.append(rope(h1, tgt, 8, w=3))
    out.append(rope(h2, (h2[0] - 40, h2[1] + 52), 12, w=3))
    # rocks and rough ground
    for rx, ry, rw, rh in [(130, 760, 26, 14), (300, 778, 20, 10), (420, 790, 34, 16), (560, 770, 24, 12)]:
        out.append(rock(rng, rx, ry, rw, rh))
    out.append(grass(rng, 60, 620, 780, 830, 60, 12, 40))
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


def zen_herding(rng):
    out = [enso_open()]
    out.append(hills(rng, [(560, 70, PALE, 0.3, 130)], 40, 640))
    # a large pine on the left
    out.append(f'<path d="M150,730 C140,640 175,560 160,420" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round" filter="url(#dry)"/>')
    for px, py, pw in [(160, 410, 90), (120, 470, 80), (205, 490, 85), (140, 560, 70)]:
        out.append(f'<ellipse cx="{px}" cy="{py}" rx="{pw}" ry="22" fill="{INK}" opacity="0.85" filter="url(#dry)"/>')
        for _ in range(30):
            nx_ = px + rng.uniform(-pw, pw)
            out.append(f'<path d="M{f(nx_)},{f(py + 6)} l{rng.uniform(-8, 8):.1f},{rng.uniform(12, 24):.1f}" stroke="{GREY}" stroke-width="1" opacity="0.7"/>')
    out.append(ground(715, 40, 640))
    o, oa = ox(320, 710, 1.0, "walk")
    out.append(o)
    fig, a = herdsman(480, 740, 1.5, "walk")
    out.append(fig)
    h_rope, h_whip = a["hands"]
    nose = oa["nose"]
    out.append(rope(h_rope, (nose[0] - 2, nose[1] + 3), 26, w=2.6))
    out.append(f'<path d="M{f(h_whip[0])},{f(h_whip[1])} L{f(h_whip[0] - 22)},{f(h_whip[1] + 6)} Q{f(h_whip[0] - 40)},{f(h_whip[1] + 18)} {f(h_whip[0] - 56)},{f(h_whip[1] + 40)}" '
               f'fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
    out.append(grass(rng, 50, 620, 735, 830, 150, 15, 55))
    out.append(grass(rng, 220, 330, 705, 715, 20, 10, 30))
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


def zen_riding(rng):
    out = [enso_open()]
    out.append(moon(470, 410, 44))
    out.append(hills(rng, [(560, 110, PALE, 0.3, 100), (620, 60, GREY, 0.22, 80)]))
    out.append(mist(340, 600, 280, 34, 0.9))
    out.append(mist(340, 660, 260, 26, 0.7))
    out.append(ground(715, 40, 640))
    # bent willow over the path at the left
    out.append(willow(rng, 130, 730, 470, 20, 70, 28, 90))
    o, oa = ox(335, 705, 1.05, "ride")
    out.append(o)
    # loose rope hanging from the nose ring, grey so the flute carries the accent
    nose = oa["nose"]
    out.append(f'<path d="M{f(nose[0])},{f(nose[1])} q-4,34 -22,46" fill="none" stroke="{GREY}" stroke-width="2" stroke-linecap="round"/>')
    back = oa["back"]
    fig, a = herdsman(back[0] + 20, back[1] + 30 * 1.2, 1.2, "ride", pale_legs=True)
    out.append(fig)
    hd = a["head"]
    m = (hd[0] + 4, hd[1] + 6)
    out.append(f'<path d="M{f(m[0] - 18)},{f(m[1] + 3)} L{f(m[0] + 48)},{f(m[1] - 6)}" stroke="{VERMILION}" stroke-width="3.6" stroke-linecap="round"/>')
    out.append(grass(rng, 50, 620, 730, 820, 110, 15, 50))
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


def zen_alone(rng):
    out = [enso_open()]
    out.append(moon(470, 410, 78))
    out.append(hills(rng, [(580, 70, PALE, 0.2, 120)]))
    out.append(ground(700, 40, 640))
    # thatched hut
    hx, hy = 200, 700
    out.append(f'<rect x="{hx - 55}" y="{hy - 50}" width="110" height="50" fill="#e4ded0" stroke="{INK}" stroke-width="2.4" filter="url(#brush)"/>')
    out.append(f'<rect x="{hx - 12}" y="{hy - 38}" width="30" height="38" fill="{INK}" opacity="0.8"/>')
    out.append(f'<path d="M{hx - 85},{hy - 44} L{hx - 40},{hy - 112} L{hx + 40},{hy - 112} L{hx + 85},{hy - 44} Z" fill="{GREY}" '
               f'stroke="{INK}" stroke-width="2.6" stroke-linejoin="round" filter="url(#dry)"/>')
    for k in range(22):
        t = k / 21
        out.append(f'<path d="M{f(hx - 85 + 45 * t * 0 + 170 * t * 0.9 - 10)},{hy - 46} L{f(hx - 38 + 76 * t)},{hy - 110}" stroke="{INK}" stroke-width="1" opacity="0.5"/>')
    out.append(f'<path d="M{hx - 88},{hy - 42} q40,12 176,0" stroke="{INK}" stroke-width="3" fill="none" filter="url(#dry)"/>')
    # mat, figure
    mx, my = 330, 716
    out.append(f'<path d="M{mx - 52},{my + 4} L{mx + 52},{my + 4} L{mx + 64},{my + 18} L{mx - 64},{my + 18} Z" fill="#cfc6b6" stroke="{INK}" stroke-width="1.6" filter="url(#brush)"/>')
    fig, a = herdsman(mx, my + 2, 1.5, "sit")
    out.append(fig)
    hd = a["head"]
    out.append(f'<path d="M{f(hd[0] - 6)},{f(hd[1] + 1)} q3,2 6,0 M{f(hd[0] + 1)},{f(hd[1] + 1)} q3,2 6,0" stroke="{INK}" stroke-width="1.2" fill="none"/>')
    # whip and coiled rope laid down
    out.append(f'<path d="M{mx + 78},{my + 22} L{mx + 130},{my + 12} Q{mx + 150},{my + 14} {mx + 168},{my + 26}" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
    out.append(coil(mx + 106, my + 30, VERMILION, 1.4))
    # reeds
    for rx in (90, 110, 560, 585):
        out.append(grass(rng, rx - 10, rx + 10, 740, 780, 14, 40, 90))
    out.append(grass(rng, 400, 560, 725, 790, 40, 15, 40))
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


def zen_empty(rng):
    """Ox and herdsman both gone: an empty clearing, sparse ground cover, a few trees at the side.
    No figure and no ox; the seal is the only vermilion."""
    out = [enso_open()]
    out.append(hills(rng, [(560, 50, PALE, 0.16, 130)]))
    out.append(mist(330, 600, 260, 40, 0.7))
    out.append(ground(705, 40, 640, op=0.12))
    # a few trees at the right side, kept small so the clearing dominates
    out.append(trunk(rng, 500, 708, 470, 7, lean=-6, leafy=4))
    out.append(trunk(rng, 548, 712, 430, 9, lean=4, leafy=5))
    out.append(trunk(rng, 462, 704, 560, 4, lean=-3, leafy=2))
    # sparse vegetation: scattered low tufts, thinning toward the centre
    for cx_, cy_, n in [(110, 745, 16), (180, 800, 10), (300, 765, 6), (410, 805, 8), (440, 735, 12), (250, 840, 8), (530, 760, 14), (580, 800, 10)]:
        out.append(grass(rng, cx_ - 18, cx_ + 18, cy_ - 6, cy_ + 6, n, 12, 34))
    for _ in range(14):
        out.append(grass(rng, 80, 600, 720, 860, 1, 5, 12))
    out.append(rock(rng, 380, 772, 16, 7, op=0.35))
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


def zen_source(rng):
    out = [enso_open()]
    out.append(hills(rng, [(470, 120, PALE, 0.32, 110), (530, 60, GREY, 0.24, 90)]))
    # stream from upper right to lower left
    cl = [(640, 500), (520, 585), (400, 665), (270, 750), (120, 840)]
    d = "M" + " L".join(f"{a},{b}" for a, b in cl)
    out.append(f'<path d="M640,500 C520,560 440,650 330,710 S170,800 100,850" fill="none" stroke="#e4ded0" stroke-width="80" stroke-linecap="round"/>')
    for off, op in ((-38, 0.6), (40, 0.5)):
        out.append(f'<path d="M640,500 C520,560 440,650 330,710 S170,800 100,850" fill="none" stroke="{GREY}" stroke-width="1.4" '
                   f'opacity="{op}" transform="translate({-off * 0.4},{off})" filter="url(#brush)"/>')
    for k in range(40):
        t = rng.uniform(0, 1)
        out.append(f'<path d="M{f(600 - 470 * t + rng.uniform(-14, 14))},{f(520 + 320 * t * 0.95 + rng.uniform(-12, 12))} l{-30 - 40 * t:.0f},{14 + 10 * t:.0f}" stroke="{GREY}" stroke-width="1" opacity="0.4"/>')
    for k in range(10):
        t = k / 9
        out.append(f'<path d="M{f(560 - 400 * t + rng.uniform(-10, 10))},{f(540 + 270 * t + rng.uniform(-8, 8))} q12,-4 26,0" stroke="{PALE}" stroke-width="1.2" fill="none"/>')
    # hut among bamboo on the far bank
    out.append(f'<rect x="466" y="522" width="44" height="26" fill="#e4ded0" stroke="{INK}" stroke-width="1.8"/>')
    out.append(f'<path d="M458,524 L478,498 L500,498 L518,524 Z" fill="{GREY}" stroke="{INK}" stroke-width="1.8" filter="url(#dry)"/>')
    for bx in (545, 560, 440, 428):
        out.append(f'<path d="M{bx},560 L{bx + 3},{470 - (bx % 5) * 6}" stroke="{INK}" stroke-width="2.2" opacity="0.8" filter="url(#brush)"/>')
        for j in range(3):
            yy = 500 + j * 18 - (bx % 5) * 6
            out.append(f'<path d="M{bx + 2},{yy} l16,-8 M{bx + 2},{yy} l-14,-9" stroke="{INK}" stroke-width="1.6" opacity="0.7"/>')
    # rocky bank, left
    out.append(f'<path d="M60,700 C120,672 200,690 270,716 C230,780 150,820 60,810 Z" fill="#cfc6b6" opacity="0.4" filter="url(#softwash)"/>')
    out.append(f'<path d="M70,712 C130,680 210,696 272,720" fill="none" stroke="{GREY}" stroke-width="1.6" opacity="0.7" filter="url(#brush)"/>')
    out.append(rock(rng, 330, 745, 34, 20))
    out.append(rock(rng, 262, 770, 26, 14))
    out.append(rock(rng, 410, 690, 22, 12))
    out.append(rock(rng, 110, 740, 40, 22))
    out.append(rock(rng, 200, 726, 28, 14, op=0.4))
    # plum tree
    out.append(f'<path d="M170,730 C150,650 205,590 168,500 C160,470 175,440 160,400" fill="none" stroke="{INK}" stroke-width="20" stroke-linecap="round" filter="url(#dry)"/>')
    branches = [(168, 520, 70, 480), (165, 560, 260, 520), (175, 480, 100, 380), (162, 430, 225, 380), (160, 410, 150, 335), (170, 600, 90, 560), (172, 460, 270, 440)]
    for bx, by, ex, ey in branches:
        out.append(f'<path d="M{bx},{by} Q{(bx + ex) / 2},{(by + ey) / 2 - 24} {ex},{ey}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" filter="url(#brush)"/>')
        for sub in range(3):
            t = 0.45 + 0.25 * sub
            sx, sy = bx + (ex - bx) * t, by + (ey - by) * t - 10
            out.append(f'<path d="M{f(sx)},{f(sy)} l{rng.uniform(-30, 30):.0f},{rng.uniform(-30, -8):.0f}" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
        for _ in range(26):
            t = rng.uniform(0.3, 1.0)
            fx = bx + (ex - bx) * t + rng.gauss(0, 12)
            fy = by + (ey - by) * t - 12 * t + rng.gauss(0, 12)
            out.append(f'<circle cx="{f(fx)}" cy="{f(fy)}" r="{rng.uniform(2.2, 4.6):.1f}" fill="{VERMILION}" opacity="{rng.uniform(0.6, 0.95):.2f}"/>')
    out.append(grass(rng, 60, 290, 790, 830, 50, 15, 40))
    out.append(grass(rng, 480, 620, 790, 830, 30, 15, 40))
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


def _budai(x, y, s):
    """The herdsman grown old: barefoot, round-bellied, laughing, in the manner of Budai."""
    P = lambda lx, ly: (x + lx * s, y + ly * s)
    out = []
    A = lambda pts: " ".join(f"{f(P(*q)[0])},{f(P(*q)[1])}" for q in pts)
    # staff with a wine gourd, left side
    top = P(-72, -126)
    out.append(f'<path d="M{f(P(-72, 0)[0])},{f(P(-72, 0)[1])} L{f(top[0])},{f(top[1])}" stroke="{INK}" stroke-width="{3.4 * s:.1f}" stroke-linecap="round"/>')
    g1, g2 = P(-64, -112), P(-64, -92)
    out.append(f'<path d="M{f(top[0])},{f(top[1] + 4)} L{f(g1[0])},{f(g1[1])}" stroke="{INK}" stroke-width="1.5"/>')
    out.append(f'<ellipse cx="{f(g1[0])}" cy="{f(g1[1] + 7 * s)}" rx="{7 * s:.1f}" ry="{9 * s:.1f}" fill="{GREY}" stroke="{INK}" stroke-width="1.8"/>'
               f'<ellipse cx="{f(g2[0] + 1)}" cy="{f(g2[1] + 6 * s)}" rx="{11 * s:.1f}" ry="{12 * s:.1f}" fill="{GREY}" stroke="{INK}" stroke-width="1.8"/>')
    # bare feet and legs
    for lx, fx in ((-12, -18), (12, 20)):
        a, b = P(lx, -34), P(fx, 0)
        out.append(f'<path d="M{f(a[0])},{f(a[1])} L{f(b[0])},{f(b[1])}" stroke="{INK}" stroke-width="{4 * s:.1f}" stroke-linecap="round"/>')
        out.append(f'<path d="M{f(b[0] - 3 * s)},{f(b[1] + 1)} l{14 * s:.1f},0" stroke="{INK}" stroke-width="{3 * s:.1f}" stroke-linecap="round"/>')
    # sack over the shoulder, hanging at the back: the vermilion accent
    sk = P(-30, -50)
    out.append(f'<path d="M{f(P(-18, -92)[0])},{f(P(-18, -92)[1])} Q{f(P(-44, -80)[0])},{f(P(-44, -80)[1])} {f(sk[0])},{f(sk[1] - 24 * s)}" fill="none" stroke="{INK}" stroke-width="{2.2 * s:.1f}"/>')
    out.append(f'<path d="M{f(sk[0])},{f(sk[1] - 26 * s)} C{f(sk[0] - 22 * s)},{f(sk[1] - 8 * s)} {f(sk[0] - 20 * s)},{f(sk[1] + 34 * s)} {f(sk[0] + 2 * s)},{f(sk[1] + 38 * s)} '
               f'C{f(sk[0] + 22 * s)},{f(sk[1] + 32 * s)} {f(sk[0] + 20 * s)},{f(sk[1] - 8 * s)} {f(sk[0])},{f(sk[1] - 26 * s)} Z" '
               f'fill="{VERMILION}" stroke="{INK}" stroke-width="{2.2 * s:.1f}" filter="url(#brush)"/>')
    # open robe: two ragged panels, belly bare and round
    out.append(f'<path d="M{A([(-24, -92), (-30, -60), (-26, -30), (-14, -24), (-8, -60), (-6, -88)])}" fill="{ROBE}" stroke="{INK}" stroke-width="{2.2 * s:.1f}" stroke-linejoin="round" filter="url(#brush)"/>')
    out.append(f'<path d="M{A([(24, -92), (32, -60), (28, -28), (16, -22), (10, -60), (6, -88)])}" fill="{ROBE}" stroke="{INK}" stroke-width="{2.2 * s:.1f}" stroke-linejoin="round" filter="url(#brush)"/>')
    bc = P(0, -52)
    out.append(f'<ellipse cx="{f(bc[0])}" cy="{f(bc[1])}" rx="{19 * s:.1f}" ry="{27 * s:.1f}" fill="{ROBE}" stroke="{INK}" stroke-width="{2 * s:.1f}"/>')
    out.append(f'<path d="M{f(bc[0] - 2 * s)},{f(bc[1] - 2 * s)} q3,3 6,0" stroke="{INK}" stroke-width="1.4" fill="none"/>')
    # staff arm, and the open hand held out toward the traveller
    sh1, sh2 = P(-18, -90), P(18, -90)
    hn = P(-72, -74)
    out.append(f'<path d="M{f(sh1[0])},{f(sh1[1])} Q{f(P(-50, -64)[0])},{f(P(-50, -64)[1])} {f(hn[0])},{f(hn[1])}" fill="none" stroke="{INK}" stroke-width="{3 * s:.1f}" stroke-linecap="round"/>')
    e, h = P(50, -80), P(76, -88)
    out.append(f'<path d="M{f(sh2[0])},{f(sh2[1])} Q{f(e[0])},{f(e[1])} {f(h[0])},{f(h[1])}" fill="none" stroke="{INK}" stroke-width="{3 * s:.1f}" stroke-linecap="round"/>')
    for dx, dy in ((4, -5), (8, -2), (7, 2), (3, 4)):
        out.append(f'<path d="M{f(h[0])},{f(h[1])} l{dx * s:.1f},{dy * s:.1f}" stroke="{INK}" stroke-width="{1.8 * s:.1f}" stroke-linecap="round"/>')
    # head, laughing
    hd = P(0, -112)
    out.append(f'<circle cx="{f(hd[0])}" cy="{f(hd[1])}" r="{17 * s:.1f}" fill="{ROBE}" stroke="{INK}" stroke-width="{2.2 * s:.1f}"/>')
    out.append(f'<path d="M{f(hd[0] - 10 * s)},{f(hd[1] + 3 * s)} Q{f(hd[0])},{f(hd[1] + 18 * s)} {f(hd[0] + 10 * s)},{f(hd[1] + 3 * s)} Z" fill="{INK}"/>')
    out.append(f'<path d="M{f(hd[0] - 9 * s)},{f(hd[1] - 5 * s)} q{4 * s:.1f},{-5 * s:.1f} {8 * s:.1f},0 M{f(hd[0] + 2 * s)},{f(hd[1] - 5 * s)} q{4 * s:.1f},{-5 * s:.1f} {8 * s:.1f},0" stroke="{INK}" stroke-width="1.8" fill="none"/>')
    out.append(f'<path d="M{f(hd[0] - 17 * s)},{f(hd[1] - 2 * s)} q-6,6 0,10" stroke="{INK}" stroke-width="1.6" fill="none"/>')
    return "".join(out), {"hand": h}


def zen_market(rng):
    out = [enso_open()]
    out.append(hills(rng, [(500, 70, PALE, 0.22, 120)]))
    # village sketched in light grey: roofs, an awning
    for rx, ry, rw, rh in [(130, 600, 80, 44), (250, 585, 70, 38), (430, 600, 90, 42), (545, 590, 60, 34)]:
        out.append(f'<path d="M{rx - rw},{ry} L{rx - rw * 0.55},{ry - rh} L{rx + rw * 0.55},{ry - rh} L{rx + rw},{ry} Z" fill="{PALE}" opacity="0.5" stroke="{GREY}" stroke-width="1.4" filter="url(#brush)"/>')
        out.append(f'<rect x="{rx - rw * 0.7}" y="{ry}" width="{rw * 1.4}" height="34" fill="#e4ded0" opacity="0.7" stroke="{GREY}" stroke-width="1.2"/>')
    out.append(f'<path d="M330,612 L440,612 L460,640 L310,640 Z" fill="{GREY}" opacity="0.4" stroke="{GREY}" stroke-width="1.4"/>')
    out.append(f'<path d="M325,640 L325,690 M445,640 L445,690" stroke="{GREY}" stroke-width="2" opacity="0.7"/>')
    # bare tree about to flower, pale buds only
    out.append(trunk(rng, 560, 720, 450, 12, -8, col=GREY, leafy=0))
    for bx, by, ex, ey in [(556, 560, 500, 510), (552, 520, 600, 470), (558, 610, 610, 570), (554, 480, 520, 440)]:
        out.append(f'<path d="M{bx},{by} Q{(bx + ex) / 2},{(by + ey) / 2 - 12} {ex},{ey}" fill="none" stroke="{GREY}" stroke-width="3" stroke-linecap="round" filter="url(#brush)"/>')
        for _ in range(5):
            t = rng.uniform(0.4, 1)
            out.append(f'<circle cx="{f(bx + (ex - bx) * t)}" cy="{f(by + (ey - by) * t - 6)}" r="{rng.uniform(2, 3.6):.1f}" fill="{ZEN_PAPER}" stroke="{GREY}" stroke-width="1.2"/>')
    # dirt path
    out.append(f'<path d="M40,740 C200,700 360,740 640,700 L640,840 L40,840 Z" fill="#cfc6b6" opacity="0.3" filter="url(#softwash)"/>')
    out.append(f'<path d="M40,740 C200,700 360,740 640,700" fill="none" stroke="{GREY}" stroke-width="1.5" opacity="0.6" filter="url(#brush)"/>')
    sx, sy, ss = 250, 760, 1.55
    fig, ah = _budai(sx, sy, ss)
    out.append(fig)
    # the young traveller with a coiled rope, at the right, facing him
    tr, ta = herdsman(500, 745, 1.15, "stand", flip=True)
    out.append(tr)
    hn = ta["hands"][0]
    out.append(coil(hn[0] + 4, hn[1] + 8, GREY, 1.0))
    out.append(grass(rng, 60, 620, 780, 840, 60, 12, 36))
    out.append(enso_close(rng))
    return svg("".join(out), ZEN_PAPER)


# Card id -> drawing function
CARDS = {"01": zen_searching, "02": zen_traces, "03": zen_seeing, "04": zen_catching,
         "05": zen_herding, "06": zen_riding, "07": zen_alone, "08": zen_empty,
         "09": zen_source, "10": zen_market}
