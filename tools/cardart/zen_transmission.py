"""Zen deck, card 0 (Mu, inside the ensō) and the Transmission strand, cards XI-XVII (hanging-scroll frame)."""

import math

from .common import (ENSO_CX, ENSO_CY, GREY, INK, PALE, SCROLL_BOX, VERMILION, ZEN_PAPER,
                     enso_close, enso_open, f, scroll_close, scroll_open, svg)

SKIN = "#f1ece2"
GREYROBE = "#c9c4ba"
SX0, SY0, SX1, SY1 = SCROLL_BOX

# Copies of the shared brush and dry filters whose region is the whole canvas. The shared ones size
# their region from each shape's bounding box, which clips thick strokes on thin or straight shapes.
TFILTERS = """
<filter id="tbrush" filterUnits="userSpaceOnUse" x="0" y="0" width="680" height="1156">
  <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="7" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="5" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="tdry" filterUnits="userSpaceOnUse" x="0" y="0" width="680" height="1156">
  <feTurbulence type="fractalNoise" baseFrequency="0.9 0.08" numOctaves="2" seed="11" result="t"/>
  <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 1.5" result="gaps"/>
  <feComposite in="SourceGraphic" in2="gaps" operator="in" result="cut"/>
  <feDisplacementMap in="cut" in2="t" scale="4" xChannelSelector="R" yChannelSelector="G"/>
</filter>
"""


def finish(out):
    body = "".join(out).replace("url(#brush)", "url(#tbrush)").replace("url(#dry)", "url(#tdry)")
    body = body.replace("url(#fbrush)", "url(#brush)").replace("url(#fdry)", "url(#dry)")
    return svg(f"<defs>{TFILTERS}</defs>" + body, ZEN_PAPER)


# ------------------------------------------------------------ small helpers

def path(d, fill="none", stroke=INK, w=2.0, op=1.0, filt=None, cap="round", extra=""):
    s = f'<path d="{d}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round"'
    if op != 1.0:
        s += f' opacity="{op}"'
    if filt:
        s += f' filter="url(#{filt})"'
    return s + f' {extra}/>'


def vline(x, y0, y1, w, bow=3, **kw):
    """A near-vertical stroke with a slight bow: a perfectly straight line has no bounding box width, so SVG filters drop it."""
    return path(f"M{f(x)},{f(y0)} Q{f(x + bow)},{f((y0 + y1) / 2)} {f(x)},{f(y1)}", w=w, **kw)


def ellipse(cx, cy, rx, ry, fill, stroke=None, w=1.5, op=1.0, filt=None):
    s = f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{w}"'
    if op != 1.0:
        s += f' opacity="{op}"'
    if filt:
        s += f' filter="url(#{filt})"'
    return s + "/>"


def mist(cx, cy, w, h, op=0.85):
    """A band of mist: paper-coloured blur laid over the picture."""
    return ellipse(cx, cy, w / 2, h / 2, ZEN_PAPER, op=op, filt="mist")


def wash(cx, cy, w, h, col=GREY, op=0.2):
    return ellipse(cx, cy, w / 2, h / 2, col, op=op, filt="softwash")


def pine_branch(rng, x0, y0, x1, y1, droop=25, clusters=4, size=1.0):
    """A pine branch from (x0,y0) to (x1,y1) with fans of needles."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - droop * 0.6
    out = [path(f"M{f(x0)},{f(y0)} Q{f(mx)},{f(my)} {f(x1)},{f(y1)}", w=6.5 * size, filt="brush")]
    for i in range(clusters):
        t = 0.35 + 0.65 * i / max(1, clusters - 1)
        px = (1 - t) ** 2 * x0 + 2 * t * (1 - t) * mx + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * t * (1 - t) * my + t * t * y1
        py -= 4
        for _ in range(16):
            a = math.radians(rng.uniform(-170, -10))
            ln = rng.uniform(16, 34) * size
            ex, ey = px + ln * math.cos(a), py + ln * math.sin(a) * 0.55 + ln * 0.35
            out.append(path(f"M{f(px)},{f(py)} L{f(ex)},{f(ey)}", w=1.3, op=rng.uniform(0.55, 0.95)))
    return "".join(out)


def rock(rng, pts, fill=GREY, op=0.3, jitter=6, hatch=0.0, hatch_dir=(0.2, 1.0)):
    """A rock mass: soft wash polygon, inked outline, optional dry hatching."""
    jp = [(x + rng.uniform(-jitter, jitter), y + rng.uniform(-jitter, jitter)) for x, y in pts]
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in jp) + " Z"
    out = [path(d, fill=fill, stroke=None, op=op, filt="softwash"),
           path("M" + " L".join(f"{f(x)},{f(y)}" for x, y in jp), w=3.5, op=0.85, filt="brush")]
    if hatch:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        n = int(hatch)
        for _ in range(n):
            x = rng.uniform(min(xs), max(xs))
            y = rng.uniform(min(ys), max(ys))
            ln = rng.uniform(20, 60)
            out.append(path(f"M{f(x)},{f(y)} l{f(hatch_dir[0] * ln)},{f(hatch_dir[1] * ln)}", stroke=GREY,
                            w=rng.uniform(0.8, 2.2), op=rng.uniform(0.2, 0.5), filt="dry"))
    return "".join(out)


def rock_texture(rng, x0, y0, x1, y1, n, vertical=True):
    """Angular fissures and broad dry strokes over a rock face."""
    out = []
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        pts = [(x, y)]
        for _ in range(rng.randint(2, 4)):
            dx = rng.uniform(-14, 14) if vertical else rng.uniform(20, 60)
            dy = rng.uniform(20, 60) if vertical else rng.uniform(-10, 10)
            x, y = x + dx, y + dy
            pts.append((x, y))
        d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts)
        out.append(path(d, stroke=INK, w=rng.uniform(1.5, 4.5), op=rng.uniform(0.2, 0.6), filt="brush"))
    for _ in range(n // 2):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        out.append(path(f"M{f(x)},{f(y)} q{f(rng.uniform(20, 50))},{f(rng.uniform(-6, 6))} {f(rng.uniform(60, 140))},{f(rng.uniform(-8, 8))}",
                        stroke=GREY, w=rng.uniform(10, 24), op=rng.uniform(0.1, 0.22), filt="wash"))
    return "".join(out)


def grass_tufts(rng, x0, x1, y0, y1, n):
    out = []
    for _ in range(n):
        gx, gy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        h = rng.uniform(8, 22)
        lean = rng.uniform(-6, 6)
        out.append(path(f"M{f(gx)},{f(gy)} q{f(lean * 0.3)},{f(-h * 0.6)} {f(lean)},{f(-h)}", stroke=rng.choice([INK, GREY, PALE]),
                        w=rng.uniform(0.7, 1.5), op=rng.uniform(0.4, 0.9)))
    return "".join(out)


# ------------------------------------------------------------ figures
# All figures are drawn in local units about 100 tall with the feet (or seat) at the origin,
# then placed with a translate/scale. Stroke widths scale with the figure.

def tube(d, w=6.0, robe=SKIN, rob_op=1.0):
    """A sleeve or limb: an inked outline with a filled core."""
    return path(d, stroke=INK, w=w + 2.4) + path(d, stroke=robe, w=w, op=rob_op)


def head(cx, cy, r, look=0, hair=False, knot=False, brows=0.0, beard=False, mouth=None,
         band=False, bowed=False, jaw=False, eyes=True, wide=False, hat=False, ears=False):
    """Head drawn at (cx,cy). look: -1 left, 0 front, 1 right. mouth: None, 'smile', 'open', 'shut'."""
    o = []
    if jaw:
        o.append(f'<rect x="{f(cx - r * 0.95)}" y="{f(cy - r)}" width="{f(r * 1.9)}" height="{f(r * 2.1)}" rx="{f(r * 0.45)}" '
                 f'fill="{SKIN}" stroke="{INK}" stroke-width="2"/>')
    else:
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{SKIN}" stroke="{INK}" stroke-width="2"/>')
    if ears:
        for sx in (-1, 1):
            o.append(ellipse(cx + sx * r * 0.98, cy + r * 0.45, r * 0.16, r * 0.55, SKIN, stroke=INK, w=1.4))
    if hair:
        o.append(path(f"M{f(cx - r)},{f(cy - r * 0.15)} Q{f(cx - r * 0.9)},{f(cy - r * 1.25)} {f(cx)},{f(cy - r * 1.2)} "
                      f"Q{f(cx + r * 0.9)},{f(cy - r * 1.25)} {f(cx + r)},{f(cy - r * 0.15)} Q{f(cx)},{f(cy - r * 0.55)} {f(cx - r)},{f(cy - r * 0.15)} Z",
                      fill=INK, stroke=INK, w=1))
    if knot:
        o.append(ellipse(cx, cy - r * 1.15, r * 0.4, r * 0.3, INK))
    if band:
        o.append(path(f"M{f(cx - r)},{f(cy - r * 0.35)} Q{f(cx)},{f(cy - r * 0.8)} {f(cx + r)},{f(cy - r * 0.35)}", stroke=GREY, w=r * 0.55))
        o.append(path(f"M{f(cx + r * 0.9)},{f(cy - r * 0.4)} q{f(r * 0.7)},{f(r * 0.3)} {f(r * 0.5)},{f(r * 1.0)}", stroke=GREY, w=r * 0.3))
    if hat:
        o.append(path(f"M{f(cx - r * 1.1)},{f(cy - r * 0.5)} L{f(cx - r * 0.8)},{f(cy - r * 1.7)} L{f(cx + r * 0.8)},{f(cy - r * 1.7)} L{f(cx + r * 1.1)},{f(cy - r * 0.5)} Z",
                      fill=INK, stroke=INK, w=1.5))
    if bowed:
        return "".join(o)
    ex = look * r * 0.32
    if eyes:
        for sx in (-1, 1):
            px = cx + ex + sx * r * 0.36
            if wide:
                o.append(f'<circle cx="{f(px)}" cy="{f(cy - r * 0.1)}" r="{f(r * 0.2)}" fill="{SKIN}" stroke="{INK}" stroke-width="1.2"/>'
                         f'<circle cx="{f(px)}" cy="{f(cy - r * 0.1)}" r="{f(r * 0.07)}" fill="{INK}"/>')
            else:
                o.append(path(f"M{f(px - r * 0.14)},{f(cy - r * 0.08)} L{f(px + r * 0.14)},{f(cy - r * 0.08)}", w=1.6))
    if brows:
        for sx in (-1, 1):
            px = cx + ex + sx * r * 0.36
            o.append(path(f"M{f(px - r * 0.25)},{f(cy - r * 0.32 - sx * brows * 0.1 * r)} L{f(px + r * 0.25)},{f(cy - r * 0.32 + sx * brows * 0.1 * r)}",
                          w=1.5 + 2.2 * brows))
    if beard:
        o.append(path(f"M{f(cx - r * 0.9)},{f(cy + r * 0.1)} Q{f(cx - r * 0.7)},{f(cy + r * 1.5)} {f(cx + ex)},{f(cy + r * 1.6)} "
                      f"Q{f(cx + r * 0.7)},{f(cy + r * 1.5)} {f(cx + r * 0.9)},{f(cy + r * 0.1)} Q{f(cx)},{f(cy + r * 0.55)} {f(cx - r * 0.9)},{f(cy + r * 0.1)} Z",
                      fill=INK, stroke=INK, w=1, op=0.85))
    if mouth == "smile":
        o.append(path(f"M{f(cx + ex - r * 0.3)},{f(cy + r * 0.45)} Q{f(cx + ex)},{f(cy + r * 0.7)} {f(cx + ex + r * 0.3)},{f(cy + r * 0.45)}", w=1.4))
    elif mouth == "open":
        o.append(ellipse(cx + ex, cy + r * 0.55, r * 0.34, r * 0.38, INK))
    elif mouth == "shut":
        o.append(path(f"M{f(cx + ex - r * 0.22)},{f(cy + r * 0.5)} L{f(cx + ex + r * 0.22)},{f(cy + r * 0.5)}", w=1.4))
    return "".join(o)


def place(inner, x, y, s=1.0, rot=0.0, flip=False, op=1.0):
    t = f"translate({f(x)},{f(y)}) scale({-s if flip else s},{s})"
    if rot:
        t += f" rotate({f(rot)})"
    extra = f' opacity="{op}"' if op != 1.0 else ""
    return f'<g transform="{t}"{extra}>{inner}</g>'


ARMS = {
    "palms": [("M-12,-80 Q-24,-60 -3,-62", 6), ("M12,-80 Q24,-60 3,-62", 6)],
    "down": [("M-13,-80 Q-22,-55 -19,-38", 6), ("M13,-80 Q22,-55 19,-38", 6)],
    "lap": [("M-13,-52 Q-30,-32 -7,-20", 6), ("M13,-52 Q30,-32 7,-20", 6)],
}


def standing(robe=SKIN, arms="down", bow=0.0, long=False, barefoot=False, sandals=False,
             legs="straight", headkw=None, extra_arms=(), sash=None, over=""):
    """A standing figure, feet at the origin, about 100 high. bow tilts the upper body (degrees)."""
    o = []
    hem = -5 if long else -27
    # legs
    if legs == "straight":
        o.append(path("M-6,0 L-4,-30 M6,0 L4,-30", w=3))
    elif legs == "buckle":
        o.append(path("M-4,0 L-16,-14 L-6,-32 M8,0 L2,-12 L8,-32", w=3))
    if sandals:
        o.append(path("M-10,1 L-1,1 M2,1 L11,1", w=2.4))
    # upper body
    ub = []
    wid = 21 if long else 19
    ub.append(path(f"M-14,-84 Q0,-90 14,-84 L{wid},{hem} Q0,{hem + 6} {-wid},{hem} Z", fill=robe, w=2.2, filt="fbrush"))
    ub.append(path("M-6,-84 Q0,-70 6,-84", w=1.6))
    if sash:
        ub.append(path("M-15,-50 Q0,-45 15,-50", stroke=sash, w=4.5))
        ub.append(path("M8,-48 q4,16 2,26", stroke=sash, w=3.2))
    else:
        ub.append(path("M-14,-48 Q0,-43 14,-48", w=2))
    spec = ARMS[arms] if isinstance(arms, str) else arms
    for d, w in list(spec) + list(extra_arms):
        ub.append(tube(d, w, robe=robe))
    hk = dict(headkw or {})
    ub.append(head(0, -95, 9, **hk))
    ub.append(over)
    if bow:
        o.append(f'<g transform="rotate({f(bow)} 0 -42)">{"".join(ub)}</g>')
    else:
        o += ub
    return "".join(o)


def seated(robe=SKIN, arms="lap", headkw=None, extra_arms=(), over="", lean=0.0, bow=0.0):
    """A cross-legged figure seen from the front, seat at the origin, about 72 high."""
    o = [path("M-38,0 C-42,-12 -24,-18 -15,-50 Q0,-60 15,-50 C24,-18 42,-12 38,0 Q0,5 -38,0 Z", fill=robe, w=2.2, filt="fbrush"),
         path("M-30,-6 Q0,-14 30,-6", w=1.5, op=0.6)]
    ub = []
    spec = ARMS[arms] if isinstance(arms, str) else arms
    for d, w in list(spec) + list(extra_arms):
        ub.append(tube(d, w, robe=robe))
    hk = dict(headkw or {})
    ub.append(head(0, -64, 9, **hk))
    ub.append(over)
    if lean or bow:
        o.append(f'<g transform="rotate({f(lean + bow)} 0 -10)">{"".join(ub)}</g>')
    else:
        o += ub
    return "".join(o)


def bodhidharma_back(vermilion=True):
    """Bodhidharma seen from behind, seated, in a hooded red robe; seat at the origin, about 85 high.
    Only the edge of the brow and beard shows at the left of the hood."""
    col = VERMILION if vermilion else GREYROBE
    o = [path("M-42,0 C-48,-16 -34,-30 -24,-56 C-18,-70 18,-70 24,-56 C34,-30 48,-16 42,0 Q0,8 -42,0 Z",
              fill=col, stroke=INK, w=2.6, op=0.92, filt="fbrush"),
         # hood
         path("M-22,-56 C-26,-84 -10,-98 2,-98 C16,-98 26,-84 22,-56 Q0,-48 -22,-56 Z", fill=col, stroke=INK, w=2.6, op=0.95, filt="fbrush"),
         # broad fold strokes down the back
         path("M-8,-52 C-10,-30 -16,-14 -22,-2", stroke=INK, w=3, op=0.55, filt="fdry"),
         path("M8,-52 C10,-30 18,-14 24,-2", stroke=INK, w=3, op=0.55, filt="fdry"),
         path("M0,-54 C2,-34 0,-16 -2,-2", stroke=INK, w=2, op=0.4, filt="fdry"),
         path("M-34,-8 Q0,-18 34,-8", stroke=INK, w=2, op=0.4, filt="fdry"),
         # brow and beard visible at the near edge of the hood
         path("M-22,-82 q-5,-1 -7,2", stroke=INK, w=3.4),
         path("M-23,-70 q-8,4 -5,12 q4,-2 7,-6", fill=INK, stroke=INK, w=1.2)]
    return "".join(o)


# ------------------------------------------------------------ card 0

def gate(x, y_top, y_base, half=55):
    """An open gateway: two posts and one straight crossbeam, no door and no wall.
    Kept plain on purpose: an upswept double beam would read as a Shinto torii."""
    o = []
    for sx in (-1, 1):
        px = x + sx * half
        o.append(vline(px, y_top - 6, y_base, 15, filt="brush"))
    o.append(path(f"M{x - half - 22},{y_top} L{x + half + 22},{y_top - 2}", w=14, filt="brush"))
    for sx in (-1, 1):
        px = x + sx * half
        o.append(ellipse(px, y_base + 3, 16, 4, GREY, op=0.35, filt="wash"))
    return "".join(o)


def dog(sit_x, sit_y, s=1.0):
    """A small dark dog sitting, seen from the side, looking up to the right."""
    o = [path("M-14,0 C-18,-14 -8,-26 4,-26 C12,-26 14,-12 12,0 Z", fill=INK, stroke=INK, w=2, filt="fbrush"),
         path("M-14,-4 C-24,-6 -26,2 -18,2", stroke=INK, w=3.5),
         ellipse(8, -30, 6.5, 6, INK),
         path("M10,-31 L19,-37 L14,-27 Z", fill=INK, stroke=INK, w=1.5),
         path("M2,-36 L0,-44 L7,-37 Z", fill=INK, stroke=INK, w=1.5),
         path("M6,0 L8,-12", stroke=INK, w=3)]
    return place("".join(o), sit_x, sit_y, s)


def mu(rng):
    cx, cy = ENSO_CX, ENSO_CY
    out = [enso_open()]
    ground = 690
    # Faint far hills behind the gate, mostly empty paper above
    out.append(path(f"M60,560 Q150,500 230,540 T400,525 T620,555 L620,600 L60,600 Z", fill=PALE, stroke=None, op=0.2, filt="softwash"))
    out.append(mist(cx, 590, 560, 70, 0.8))
    out.append(wash(cx, ground + 40, 560, 110, col="#cfc6b6", op=0.35))
    # Pine branch from the upper left
    out.append(pine_branch(rng, 75, 370, 285, 315, droop=-30, clusters=4, size=1.8))
        # The gateway
    out.append(gate(cx, 380, 670, half=62))
    out.append(grass_tufts(rng, 100, 580, ground - 4, ground + 90, 80))
    # Master on a flat stone, right
    out.append(ellipse(470, ground + 4, 62, 14, GREY, op=0.55, filt="brush"))
    out.append(ellipse(470, ground - 2, 56, 10, "#cfc6b6", op=0.8))
    palm = [("M-13,-52 Q-24,-34 -6,-24", 6), ("M13,-52 Q40,-52 52,-72", 6)]
    out.append(place(seated(robe=VERMILION, arms=[("M-13,-52 Q-24,-34 -6,-24", 6), ("M13,-52 Q28,-50 36,-62", 6)],
                            headkw=dict(look=-1, brows=0.8, beard=False, mouth="shut"),
                            over=ellipse(37, -64, 5, 3.4, SKIN, stroke=INK, w=1.4)),
                     470, ground - 2, 1.5))
    # Dog between them
    out.append(dog(340, ground + 18, 1.4))
    # Young monk (the herdsman), bowing slightly toward the master
    out.append(place(standing(arms="palms", bow=9, sandals=True, headkw=dict(look=1, hair=True)), 225, ground + 22, 1.6))
    out.append(enso_close(rng))
    return finish(out)


# ------------------------------------------------------------ card XI

def flower_xi(rng):
    out = [scroll_open()]
    # Rocky ledge at upper right and mist
    out.append(rock(rng, [(330, 360), (400, 350), (570, 330), (570, 560), (500, 520), (420, 470), (350, 420)],
                    GREY, 0.3, hatch=26, hatch_dir=(-0.2, 1.0)))
    out.append(wash(480, 430, 300, 80, op=0.25))
    # Pines and mist, upper left
    out.append(pine_branch(rng, 110, 130, 330, 215, droop=-30, clusters=4, size=1.2))
    out.append(pine_branch(rng, 110, 260, 250, 300, droop=-20, clusters=2, size=0.9))
    out.append(wash(250, 330, 300, 90, col=PALE, op=0.3))
    out.append(mist(330, 480, 520, 110, 0.9))
    # The Buddha: plain grey robe, topknot, long earlobes, no halo
    bud = seated(robe=GREYROBE,
                 arms=[("M-13,-52 Q-34,-44 -26,-66", 6), ("M13,-52 Q30,-40 8,-26", 6)],
                 headkw=dict(look=-1, mouth="shut", ears=True))
    bud += ellipse(0, -77, 3.2, 3.2, INK)  # topknot
    for k in range(-3, 4):
        bud += ellipse(k * 2.4, -73.5 - abs(k) * 0.2, 1.3, 1.5, INK)  # tight curls
    bud += ellipse(-9.4, -58, 1.5, 5, SKIN, stroke=INK, w=1)  # long earlobe, left
    bud += ellipse(9.4, -58, 1.5, 5, SKIN, stroke=INK, w=1)
    bud += path("M-26,-67 L-27,-80", stroke=INK, w=1.8)  # short stem
    petals = "".join(ellipse(-27 + 4.8 * math.cos(a), -85 + 3.8 * math.sin(a) , 3.2, 2.4, VERMILION) for a in
                     [i * 2 * math.pi / 5 for i in range(5)]) + f'<circle cx="-27" cy="-85" r="2" fill="{VERMILION}"/>'
    bud += petals
    out.append(place(bud, 450, 395, 1.6))
    # Assembly of five seated monks, heads bowed and still
    spots = [(265, 700, 1.0), (340, 725, 1.0), (305, 650, 0.9), (395, 690, 0.95)]
    for x, y, s in spots:
        out.append(place(seated(robe=GREYROBE, headkw=dict(bowed=True)), x, y, s))
    # The smiling monk, apart in front, head lifted
    out.append(place(seated(robe=GREYROBE, headkw=dict(look=1, mouth="smile")), 205, 790, 1.3))
    out.append(wash(300, 830, 320, 50, col="#cfc6b6", op=0.35))
    out.append(grass_tufts(rng, 130, 470, 820, 880, 40))
    out.append(scroll_close())
    return finish(out)


# ------------------------------------------------------------ card XII

def bare_branch(rng, x, y, dx, dy, depth=3, w=4.0):
    out = [path(f"M{f(x)},{f(y)} q{f(dx * 0.3)},{f(dy * 0.2)} {f(dx)},{f(dy)}", w=w, filt="brush")]
    if depth > 0:
        for _ in range(2):
            a = rng.uniform(-0.7, 0.7)
            ndx = (dx * math.cos(a) - dy * math.sin(a)) * 0.65
            ndy = (dx * math.sin(a) + dy * math.cos(a)) * 0.65
            out.append(bare_branch(rng, x + dx, y + dy, ndx, ndy, depth - 1, w * 0.62))
    return "".join(out)


def facing_wall(rng):
    out = [scroll_open()]
    # The blank cliff: a heavy mass of grey dry-brush rock
    wall = [(SX0 - 10, 250), (190, 215), (300, 240), (400, 205), (SX1 + 10, 235), (SX1 + 10, 940), (SX0 - 10, 940)]
    out.append(rock(rng, wall, GREY, 0.42, jitter=8, hatch=0))
    out.append(rock_texture(rng, SX0, 260, SX1 - 20, 880, 60))
    # lighter planes and a ledge so the wall reads as rock
    out.append(wash(190, 480, 200, 140, col=PALE, op=0.3))
    out.append(wash(500, 410, 180, 150, col=PALE, op=0.3))
    # shallow cave: a darker arch behind him
    out.append(path("M215,930 C205,740 260,630 340,625 C420,630 475,740 465,930 Z", fill=INK, stroke=None, op=0.35, filt="softwash"))
    out.append(path("M215,930 C205,740 260,630 340,625 C420,630 475,740 465,930", w=3, op=0.6, filt="dry"))
    # ground, moss at the base of the seat, litter
    out.append(wash(340, 945, 420, 60, col=INK, op=0.25))
    out.append(ellipse(340, 925, 110, 16, "#cfc6b6", stroke=INK, w=1.5, op=0.95, filt="brush"))
    for _ in range(70):
        mx = 340 + rng.gauss(0, 55)
        my = 928 + rng.uniform(-2, 12)
        out.append(ellipse(mx, my, rng.uniform(2, 5), rng.uniform(1.2, 2.5), INK if rng.random() < 0.5 else GREY, op=rng.uniform(0.4, 0.8)))
    for _ in range(26):
        lx, ly = rng.uniform(150, 530), rng.uniform(960, 1040)
        out.append(path(f"M{f(lx)},{f(ly)} q5,-4 10,0 q-5,3 -10,0 Z", fill=GREY, stroke=None, op=0.6,
                        extra=f'transform="rotate({rng.uniform(0, 180):.0f} {f(lx)} {f(ly)})"'))
    # Bodhidharma, from behind
    out.append(place(bodhidharma_back(), 340, 924, 2.0))
    # Bare branches above and a sliver of mist along the cliff top
    out.append(bare_branch(rng, 120, 200, 120, -50, depth=3, w=9))
    out.append(bare_branch(rng, 565, 130, -110, 50, depth=3, w=8))
    out.append(mist(340, 240, 640, 36, 0.7))
    out.append(scroll_close())
    return finish(out)


# ------------------------------------------------------------ card XIII

def pacifying(rng):
    out = [scroll_open()]
    # Cliff on the right with an overhang over a shallow cave
    cliff = [(430, 150), (570, 120), (SX1 + 10, 120), (SX1 + 10, 960), (330, 960), (330, 560), (290, 530), (340, 495),
             (370, 440), (410, 300)]
    out.append(rock(rng, cliff, GREY, 0.42, jitter=7))
    out.append(rock_texture(rng, 345, 150, 565, 520, 40))
    # sharp cliff lines on the left edge
    out.append(path("M110,780 L170,700 L195,730 L250,640", w=2.5, op=0.6, filt="dry"))
    out.append(path("M110,620 L150,560 L175,590", w=2, op=0.4, filt="dry"))
    # cave
    out.append(path("M350,960 L350,600 Q380,545 470,545 Q560,545 575,620 L575,960 Z", fill=INK, stroke=None, op=0.38, filt="softwash"))
    out.append(path("M350,960 L350,600 Q380,545 470,545", w=3.2, op=0.65, filt="dry"))
    # snowy ground
    out.append(wash(340, 965, 520, 50, col="#cfc6b6", op=0.45))
    out.append(path("M110,962 Q250,950 350,962 T570,960", w=2, op=0.4, filt="brush"))
    # twisted bare pine at the left
    out.append(path("M150,962 C130,880 190,820 150,740 C120,680 175,620 150,540 C140,500 170,470 190,440", w=11, filt="dry"))
    out.append(path("M158,760 C190,740 215,730 245,700", w=5, filt="dry"))
    out.append(path("M150,600 C120,580 110,560 112,530", w=4, filt="dry"))
    out.append(pine_branch(rng, 190, 440, 270, 420, droop=-10, clusters=2, size=0.8))
    out.append(pine_branch(rng, 245, 700, 300, 690, droop=-8, clusters=1, size=0.7))
    # Bodhidharma, back to us, in the cave
    out.append(place(bodhidharma_back(), 470, 955, 1.9))
    # Huike in the snow: bowed, left sleeve empty, a small white bundle held forward
    sleeve = path("M-12,-82 L-20,-78 Q-30,-55 -25,-30 L-15,-31 Q-14,-55 -9,-70 Z", fill=GREYROBE, stroke=INK, w=2)
    sleeve += path("M-25,-30 L-15,-31", w=3)
    bundle = ellipse(44, -64, 9, 7.5, "#fbf8f1", stroke=INK, w=1.8)
    bundle += path("M38,-66 Q44,-60 50,-66 M44,-71 l0,-4", w=1.2)
    huike = sleeve + standing(arms=[("M12,-80 Q30,-70 40,-65", 6)], bow=10,
                              headkw=dict(bowed=True, hair=False), over="") + bundle
    out.append(place(huike, 225, 962, 1.85))
    # snow at his ankles and a few flecks in the air
    out.append(ellipse(225, 962, 62, 9, "#fbf8f1", op=0.9, filt="brush"))
    out.append(path("M190,962 Q235,950 280,962", w=2, op=0.5, filt="brush"))
    for _ in range(90):
        sx, sy = rng.uniform(SX0, SX1), rng.uniform(80, 940)
        out.append(f'<circle cx="{f(sx)}" cy="{f(sy)}" r="{rng.uniform(1.2, 2.8):.1f}" fill="{PALE}" opacity="{rng.uniform(0.35, 0.8):.2f}"/>')
    out.append(scroll_close())
    return finish(out)


# ------------------------------------------------------------ card XIV

def bamboo(rng, x, y0, y1, lean=0.0):
    out = [path(f"M{x},{y1} q{lean + 4},{(y0 - y1) / 2} {lean * 1.5},{y0 - y1}", w=9, filt="brush")]
    for k in range(5):
        ny = y1 + (y0 - y1) * (k + 1) / 6
        out.append(path(f"M{x - 5 + lean * (k / 6)},{ny} l10,0", w=2))
    for _ in range(7):
        lx, ly = x + lean * 1.5 + rng.uniform(-6, 6), y0 + rng.uniform(0, 90)
        sx = rng.choice([-1, 1])
        out.append(path(f"M{f(lx)},{f(ly)} q{f(sx * 18)},{f(10)} {f(sx * 46)},{f(rng.uniform(26, 44))}", stroke=INK, w=3,
                        op=rng.uniform(0.6, 0.9), filt="brush", extra=""))
    return "".join(out)


def scribble_marks(rng, x0, y0, cols, rows, dx, dy, length, wobble, w, sloppy):
    """Abstract brush marks laid in a grid. No glyph is ever formed: each mark is one wavering stroke."""
    out = []
    for c in range(cols):
        for r in range(rows):
            x = x0 + c * dx + rng.uniform(-sloppy, sloppy)
            y = y0 + r * dy + rng.uniform(-sloppy, sloppy)
            L = length * rng.uniform(0.6, 1.2)
            a = rng.uniform(-0.5, 0.5)
            ex, ey = x + L * math.cos(a), y + L * math.sin(a)
            out.append(path(f"M{f(x)},{f(y)} Q{f((x + ex) / 2)},{f((y + ey) / 2 + rng.uniform(-wobble, wobble))} {f(ex)},{f(ey)}",
                            w=w * rng.uniform(0.7, 1.5), op=rng.uniform(0.6, 0.9), filt="brush"))
    return "".join(out)


def no_mirror(rng):
    out = [scroll_open()]
    out.append(bamboo(rng, 150, 70, 330, lean=14))
    out.append(bamboo(rng, 200, 100, 330, lean=-8))
    out.append(bamboo(rng, 520, 80, 330, lean=-10))
    # tiled roof edge
    out.append(path("M105,300 Q340,330 575,300 L575,372 L105,372 Z", fill=GREY, stroke=INK, w=2.5, op=0.85, filt="brush"))
    for k in range(24):
        x = 112 + k * 20
        out.append(path(f"M{x},304 q8,16 0,64", stroke=ZEN_PAPER, w=1.6, op=0.55))
    out.append(path("M105,372 Q340,386 575,372", w=5, filt="dry"))
    # wall of pale plaster with timber posts and a plinth
    out.append(f'<rect x="135" y="378" width="410" height="430" fill="#e8dfcd" filter="url(#brush)"/>')
    out.append(wash(340, 560, 380, 300, col="#fff", op=0.18))
    for px in (135, 545):
        out.append(vline(px, 372, 815, 12, filt="brush"))
    out.append(path("M135,740 Q340,744 545,740", w=3, op=0.6, filt="brush"))
    out.append(path("M135,812 Q340,816 545,812", w=8, op=0.8, filt="brush"))
    out.append(f'<rect x="135" y="745" width="410" height="66" fill="{GREY}" opacity="0.22" filter="url(#wash)"/>')
    # lantern under the eaves
    out.append(path("M340,386 L340,420", w=1.6))
    out.append(ellipse(340, 440, 15, 21, "#f1ece2", stroke=INK, w=2.2))
    out.append(path("M326,433 L354,433 M326,447 L354,447", w=1.2, op=0.7))
    out.append(path("M330,419 L350,419 M333,461 L347,461", w=3))
    # the two verses: one neat and even, one larger and looser; no characters
    out.append(scribble_marks(rng, 185, 470, 5, 6, 22, 24, 15, 3, 2.2, 0.8))
    out.append(scribble_marks(rng, 345, 480, 3, 4, 52, 50, 42, 9, 4.4, 7))
    # courtyard ground
    out.append(wash(340, 880, 460, 70, col="#cfc6b6", op=0.4))
    out.append(grass_tufts(rng, 120, 560, 860, 960, 50))
    # Huineng, the rice-pounder: barefoot, headcloth, short rough robe, pole on his shoulder
    pole = path("M-52,-12 L52,-128", stroke=INK, w=4.5, filt="fbrush") + ellipse(-52, -12, 4, 4, GREY, stroke=INK, w=1.5)
    hui = standing(robe=GREYROBE, arms=[("M-13,-80 Q-24,-66 -10,-62", 6), ("M13,-80 Q36,-96 38,-110", 6)],
                   headkw=dict(look=1, band=True, mouth="shut"), sash=VERMILION)
    out.append(place(pole + hui, 200, 872, 1.85))
    # the official with his brush
    off = standing(robe="#ddd7cc", arms=[("M13,-80 Q22,-60 6,-56", 6), ("M-13,-80 Q-30,-98 -42,-102", 6)],
                   long=True, headkw=dict(look=-1, hat=True, mouth="shut"))
    off += path("M-42,-102 L-52,-124", w=2.4) + path("M-52,-124 l-2,-6", stroke=INK, w=3.2)
    out.append(place(off, 480, 880, 1.9))
    out.append(scroll_close())
    return finish(out)


# ------------------------------------------------------------ card XV

def hut(x, y, w, h):
    """A small thatched hut, front on."""
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e8dfcd" stroke="{INK}" stroke-width="2.4" filter="url(#brush)"/>',
         path(f"M{x - 22},{y + 8} L{x + w / 2},{y - 62} L{x + w + 22},{y + 8} Z", fill=GREY, stroke=INK, w=3, op=0.9, filt="brush")]
    for k in range(9):
        t = k / 8
        o.append(path(f"M{f(x - 18 + t * (w + 36))},{y + 6} L{f(x + w / 2 + (t - 0.5) * 20)},{y - 56}", stroke=INK, w=1.4, op=0.4, filt="dry"))
    o.append(f'<rect x="{x + w / 2 - 14}" y="{y + 20}" width="28" height="{h - 20}" fill="{INK}" opacity="0.7"/>')
    return "".join(o)


def ordinary(rng):
    out = [scroll_open(), '<g transform="translate(0,-90)">']
    # distant hills and thin mist, blank sky above
    out.append(path("M105,460 Q180,380 260,430 T400,400 T575,440 L575,520 L105,520 Z", fill=PALE, stroke=None, op=0.3, filt="softwash"))
    out.append(path("M105,500 Q220,450 330,490 T575,480 L575,540 L105,540 Z", fill=GREY, stroke=None, op=0.2, filt="softwash"))
    out.append(mist(340, 520, 520, 70, 0.85))
    # hut, broom and bucket
    out.append(wash(445, 705, 260, 40, col="#cfc6b6", op=0.4))
    out.append(hut(380, 600, 130, 100))
    out.append(path("M372,705 L392,610", w=3, filt="brush"))
    for k in range(7):
        out.append(path(f"M{372 - 6 + k * 3},706 L{366 + k * 3},{724}", w=1.6, op=0.8))
    out.append(path("M362,706 Q372,698 382,706", w=3, op=0.8))
    out.append(path("M520,690 L526,716 L552,716 L558,690 Z", fill="#e1d8c5", stroke=INK, w=2))
    out.append(path("M522,690 Q540,672 556,690", w=1.8))
    # a stone path winding down
    for _ in range(18):
        ty = rng.uniform(850, 1060)
        sx, sy = 330 + 50 * math.sin(ty / 60) + rng.gauss(0, 30), ty
        out.append(ellipse(sx, sy, rng.uniform(8, 16), rng.uniform(3, 6), "#cfc6b6", stroke=GREY, w=1, op=0.7))
    out.append(grass_tufts(rng, 120, 560, 725, 760, 40))
    out.append(grass_tufts(rng, 120, 300, 800, 1000, 50))
    # the flat stone with the tea bowl between the two
    out.append(ellipse(325, 800, 36, 9, GREY, op=0.55, filt="brush"))
    out.append(ellipse(325, 796, 32, 7, "#d9d1c0", stroke=INK, w=1.4))
    out.append(path("M309,780 Q310,794 325,795 Q340,794 341,780 Z", fill="#f1ece2", stroke=INK, w=2))
    out.append(ellipse(325, 780, 16, 3.8, SKIN, stroke=VERMILION, w=2.6))
    # the old teacher on a low stool, staff beside him
    out.append(path("M410,790 L406,806 M470,790 L474,806", w=3))
    out.append(path("M404,788 L476,788", w=6, filt="brush"))
    out.append(vline(512, 690, 806, 5, bow=5, filt="brush"))
    out.append(place(seated(robe=GREYROBE, arms=[("M-13,-52 Q-34,-38 -28,-18", 6), ("M13,-52 Q34,-38 28,-18", 6)],
                            headkw=dict(look=-1, brows=0.2, mouth="shut"),
                            over=ellipse(-28, -17, 4, 3, SKIN, stroke=INK, w=1.2) + ellipse(28, -17, 4, 3, SKIN, stroke=INK, w=1.2)),
                     443, 790, 1.6))
    # the younger monk, palms together, leaning to ask
    out.append(place(standing(arms="palms", long=True, bow=9, robe="#e0dacd", headkw=dict(look=1, mouth="shut", hair=False)), 232, 805, 1.55))
    out.append(wash(340, 820, 440, 40, col=GREY, op=0.15))
    out.append("</g>")
    out.append(scroll_close())
    return finish(out)


# ------------------------------------------------------------ card XVI

def wild_fox(rng):
    out = [scroll_open()]
    # steep misty mountain
    out.append(path("M100,700 L190,420 L240,300 L300,170 L360,260 L410,200 L470,360 L575,520 L575,720 Z", fill=GREY, stroke=None, op=0.33, filt="softwash"))
    out.append(rock_texture(rng, 220, 200, 480, 560, 30))
    out.append(path("M110,690 L190,430 L240,310 L300,172 L360,262 L410,205 L470,362 L570,520", w=2.8, op=0.75, filt="dry"))
    out.append(path("M410,205 L400,340 L440,440", w=2, stroke=GREY, op=0.45, filt="dry"))
    out.append(mist(340, 420, 520, 90, 0.9))
    out.append(mist(300, 590, 560, 100, 0.92))
    # pines above
    out.append(pine_branch(rng, 575, 130, 400, 215, droop=-25, clusters=4, size=1.1))
    out.append(pine_branch(rng, 110, 250, 220, 290, droop=-15, clusters=2, size=0.9))
    # clearing
    out.append(wash(340, 900, 440, 150, col="#cfc6b6", op=0.45))
    out.append(grass_tufts(rng, 130, 560, 880, 1000, 60))
    # smoke, one curl rising from the pyre
    smoke = "M388,805 C410,760 350,720 385,680 C415,640 360,590 392,540 C410,500 380,470 398,420"
    for w, op in ((16, 0.22), (9, 0.3), (3, 0.45)):
        out.append(path(smoke, stroke=GREY, w=w, op=op, filt="wash" if w > 5 else "brush"))
    out.append('<g transform="translate(340,880) scale(1.4) translate(-340,-880)">')
    # pyre: stacked logs, one small flame
    for ax, ay, bx, by in ((360, 860, 420, 838), (356, 842, 424, 860), (364, 826, 416, 828), (370, 852, 412, 806)):
        out.append(path(f"M{ax},{ay} L{bx},{by}", w=6, filt="dry"))
    out.append(path("M383,812 C372,796 388,786 390,770 C400,786 410,798 398,812 Z", fill=VERMILION, stroke=None, op=0.92, filt="brush"))
    out.append(path("M392,812 C388,800 394,796 396,788 C402,798 404,806 398,812 Z", fill=ZEN_PAPER, stroke=None, op=0.35))
    # the fox on a board before the pyre, wrapped in a robe: ears and tail show
    out.append(path("M268,930 L268,950 M372,930 L372,950", w=4))
    out.append(path("M262,930 L378,930", w=7, filt="dry"))
    out.append(path("M276,928 C276,904 312,896 340,906 C364,912 372,922 372,928 Z", fill=GREYROBE, stroke=INK, w=2.4, filt="brush"))
    out.append(path("M296,912 Q320,918 350,912 M304,922 Q326,926 358,920", w=1.4, op=0.6))
    out.append(path("M278,908 L272,888 L288,900 Z", fill=INK, stroke=INK, w=1.8))
    out.append(path("M290,902 L292,884 L302,899 Z", fill=INK, stroke=INK, w=1.8))
    out.append(path("M372,924 C392,918 410,926 424,912 C420,932 396,940 372,932 Z", fill=INK, stroke=INK, w=2, filt="brush"))
    out.append('</g>')
    # monks standing in a half circle, heads bowed, palms together
    for x, y, s in ((235, 890, 1.3), (285, 835, 1.25), (475, 835, 1.25), (525, 890, 1.3)):
        out.append(place(standing(robe=GREYROBE, arms="palms", long=True, bow=6 if x < 340 else -6, headkw=dict(bowed=True)), x, y, s))
    # the old man, faint pale wash at the left, bowing toward them
    out.append(place(standing(robe="#d8d3c8", arms=[("M-12,-80 Q-18,-62 -6,-62", 5), ("M12,-80 Q18,-62 6,-62", 5)], long=True, bow=16,
                              headkw=dict(bowed=True)), 165, 800, 1.3, op=0.4))
    out.append(wash(165, 760, 70, 160, col="#ffffff", op=0.12))
    out.append(scroll_close())
    return finish(out)


# ------------------------------------------------------------ card XVII

def the_shout(rng):
    out = [scroll_open()]
    # leaning pine at upper left
    out.append(path("M150,520 C145,400 125,300 175,200", w=10, filt="dry"))
    out.append(pine_branch(rng, 172, 220, 320, 190, droop=-20, clusters=3, size=1.1))
    out.append(pine_branch(rng, 165, 300, 112, 330, droop=10, clusters=2, size=0.8))
    out.append(path("M150,520 C140,560 110,590 108,620", w=7, filt="dry"))
    # bare ground
    out.append(wash(340, 925, 500, 70, col="#cfc6b6", op=0.5))
    out.append(path("M110,920 Q250,905 400,918 T570,912", w=2, op=0.5, filt="brush"))
    out.append(grass_tufts(rng, 110, 570, 925, 1010, 50))
    # the chair: plain frame, back posts and crossbar
    out.append(path("M378,610 Q383,770 376,905", w=9, filt="brush") + path("M556,610 Q551,770 558,905", w=9, filt="brush"))
    out.append(path("M378,670 Q470,674 556,670 M378,640 Q470,644 556,640", w=5, filt="brush"))
    out.append(path("M364,840 Q460,844 572,840", w=10, filt="brush"))
    # Linji: bold strokes, leaning forward, fist on the knee, mouth open, square jaw
    patch = f'<rect x="-22" y="-44" width="10" height="13" fill="{VERMILION}" opacity="0.92" filter="url(#fbrush)"/>'
    linji = seated(robe=GREYROBE, arms=[("M-13,-50 Q-36,-34 -32,-20", 7), ("M13,-50 Q34,-34 22,-14", 7)],
                   headkw=dict(look=-1, jaw=True, brows=1.0, mouth="open", beard=False, wide=False), lean=-6,
                   over=patch + ellipse(-32, -18, 6, 5, SKIN, stroke=INK, w=1.8))
    out.append(place(linji, 466, 840, 2.2))
    # the young monk, thrown backwards: arms flung up, knees buckling, robe whipped aside, mouth shut and eyes wide
    flap = path("M12,-82 Q40,-90 52,-66 Q36,-62 16,-50", fill="#e8e2d6", stroke=INK, w=2, op=0.95)
    young = standing(robe="#f1ece2", arms=[("M-13,-80 Q-36,-100 -34,-124", 6), ("M13,-80 Q34,-106 46,-124", 6)],
                     bow=-24, legs="buckle", sandals=True,
                     headkw=dict(look=1, hair=True, wide=True, mouth="shut", jaw=False), over=flap)
    out.append(place(young, 245, 900, 1.9))
    # the shout: one violent diagonal stroke of ink between them, with spatter
    stroke_poly = "M262,850 C280,780 316,712 336,650 C348,616 360,590 368,556 C376,606 364,652 350,700 C334,752 316,806 296,858 Z"
    out.append(path(stroke_poly, fill=INK, stroke=INK, w=6, op=0.92, filt="dry"))
    out.append(path("M274,830 C304,760 334,690 366,566", stroke=INK, w=14, op=0.8, filt="brush"))
    out.append(path("M280,860 C288,820 318,790 330,750", stroke=GREY, w=9, op=0.5, filt="dry"))
    for _ in range(46):
        t = rng.uniform(0, 1)
        bx = 262 + 110 * t + rng.gauss(0, 38)
        by = 850 - 290 * t + rng.gauss(0, 34)
        out.append(f'<circle cx="{f(bx)}" cy="{f(by)}" r="{rng.uniform(1.2, 5.5):.1f}" fill="{INK}" opacity="{rng.uniform(0.5, 0.9):.2f}"/>')
    out.append(scroll_close())
    return finish(out)


# Card id -> drawing function
CARDS = {
    "00": mu,
    "11": flower_xi,
    "12": facing_wall,
    "13": pacifying,
    "14": no_mirror,
    "15": ordinary,
    "16": wild_fox,
    "17": the_shout,
}
