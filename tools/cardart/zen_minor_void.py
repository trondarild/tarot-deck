"""Zen deck, minor series, suit of Void (vo01-vo15): awareness itself.

Built on the pattern of zen_minor_earth, whose figure helpers (withdrawn, acting, ordinary), place() and props are imported rather
than copied, with a few props from the Water, Fire and Wind modules.

Void is the sparse suit: each card leaves most of the paper bare and shows one recognisable object
or figure, with a little ground. Light, shadow, rings and reflections stand for awareness.

Pips vo01-vo10: zen_pip_open("void", n) draws the ensō with n outlined jewels, then one small
vignette of the pip's Image paragraph is drawn in the lower inside of the ensō (ZEN_VIGNETTE), then
zen_pip_close(). No drop or teardrop outline is drawn in a vignette, so the jewel count stays
readable: the lamp flame is small and filled, the maple leaf is a lobed star, ripples are ellipses.

Ranks vo11-vo15 use the hanging-scroll frame with a fuller scene, and the same figure type as the
other suits for each rank: withdrawn (First), attending (Second, as _attending_up), acting (Third), engaged (Fourth, as
_ferryman), ordinary (Fifth). The setting and props are those of Void: bare rooms, a wide river, a shrine
stair. Each card has at most one small vermilion accent besides the seal and rank emblems.

Helpers new to this module: window_frame(), light_beam(), footprints(), bell(), grasping_hand(), motes(),
sheet_with_circle(), brush_and_stone(), maple(), stool(), bedstead(), awning_stall(), and variants of
the Second and Fourth Rank figures, _attending_up() and _ferryman(), plus _sitter_front() for passengers.
"""

import math

from .common import (GREY, INK, PALE, SCROLL_BOX, VERMILION, ZEN_PAPER, ZEN_VIGNETTE,
                     f, zen_pip_close, zen_pip_open, zen_rank_close, zen_rank_open)
from .zen_minor_earth import (STRAW, WOOD, _anchor, _arm, acting, floorboards, ordinary, place,
                              withdrawn)
from .zen_minor_fire import lantern, oil_lamp
from .zen_minor_water import boat, chawan, rain, ripple, water
from .zen_transmission import GREYROBE, SKIN, ellipse, finish, head, hut, path, standing, tube
from .zen_way import coil, grass, ground, herdsman, mist, ox, rock, rope

SX0, SY0, SX1, SY1 = SCROLL_BOX
SCX = (SX0 + SX1) / 2
VX0, VY0, VX1, VY1 = ZEN_VIGNETTE
VCX = (VX0 + VX1) / 2
FLOOR = 725
PAPERWHITE, WALL, SKY = "#faf6ea", "#d9d3c6", "#c9d0d1"


# ------------------------------------------------------------ new helpers

def window_frame(x0, y0, x1, y1, bars=(1, 1), sky=None, w=3.4):
    """A rectangular window: optional pale pane, a heavy frame and a lattice of bars (cols, rows)."""
    o = []
    if sky:
        o.append(path(f"M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z", fill=sky, stroke=None, op=0.7, filt="softwash"))
    for k in range(1, bars[0] + 1):
        if k < bars[0] + 1 and bars[0] > 1:
            x = x0 + (x1 - x0) * k / bars[0]
            if k < bars[0]:
                o.append(path(f"M{f(x)},{y0} Q{f(x + 2)},{f((y0 + y1) / 2)} {f(x)},{y1}", w=w * 0.6, op=0.85))
    for k in range(1, bars[1]):
        y = y0 + (y1 - y0) * k / bars[1]
        o.append(path(f"M{x0},{f(y)} Q{f((x0 + x1) / 2)},{f(y + 2)} {x1},{f(y)}", w=w * 0.6, op=0.85))
    o.append(path(f"M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z", w=w, filt="brush"))
    return "".join(o)


def light_beam(poly, op=0.2, edge=True):
    """A slanted shaft of light as a pale grey wash with two faint edge lines. poly is four points."""
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in poly) + " Z"
    out = [path(d, fill=GREY, stroke=None, op=op, filt="softwash")]
    if edge:
        out.append(path(f"M{f(poly[0][0])},{f(poly[0][1])} L{f(poly[3][0])},{f(poly[3][1])} "
                        f"M{f(poly[1][0])},{f(poly[1][1])} L{f(poly[2][0])},{f(poly[2][1])}", stroke=PALE, w=1.1, op=0.6))
    return "".join(out)


def footprints(pts, s=1.0, rng=None):
    """Bare footprints pressed into sand: a soft grey sole narrowing at the arch, with a short row of
    toes joined to it; no ink outline, so they read as hollows. pts are (x, y, size, angle, side),
    toes toward local -y, side -1 for a left foot and 1 for a right foot."""
    out = []
    for x, y, sz, ang, side in pts:
        sole = "M-7,-18 C-9,-8 -6,2 -5,8 C-5,16 -4,22 0,22 C5,22 7,16 6,8 C6,0 9,-8 8,-17 C6,-24 -5,-25 -7,-18 Z"
        g = [path(sole, fill=GREY, stroke=None, op=0.5, filt="softwash"),
             path(sole, fill=GREY, stroke=None, op=0.35)]
        for tx, ty, tr in ((-5.5, -24, 2.4), (-1.5, -26.5, 2.2), (2.5, -26.5, 2.0), (6, -24.5, 1.8)):
            g.append(f'<circle cx="{tx}" cy="{ty}" r="{tr}" fill="{GREY}" opacity="0.55"/>')
        mirror = -1 if side < 0 else 1
        # foreshortened: prints on level ground seen from above at a low angle
        out.append(f'<g transform="translate({f(x)},{f(y)}) scale(1,0.55) rotate({ang}) scale({f(mirror * sz)},{f(sz * 0.8)})">{"".join(g)}</g>')
    return "".join(out)


def bell(x, y, w, h):
    """A temple bell hanging from its cap at (x, y), mouth flaring to the width w."""
    d = (f"M{f(x - w * 0.22)},{f(y + 8)} C{f(x - w * 0.24)},{f(y + h * 0.5)} {f(x - w * 0.5)},{f(y + h * 0.7)} {f(x - w * 0.5)},{f(y + h)} "
         f"L{f(x + w * 0.5)},{f(y + h)} C{f(x + w * 0.5)},{f(y + h * 0.7)} {f(x + w * 0.24)},{f(y + h * 0.5)} {f(x + w * 0.22)},{f(y + 8)} Z")
    return (path(f"M{f(x)},{f(y - 40)} L{f(x)},{f(y + 4)}", w=3.4)
            + path(d, fill="#6e6a63", stroke=INK, w=2.6, filt="brush")
            + ellipse(x, y + h, w * 0.5, w * 0.08, "#4a4742", stroke=INK, w=2)
            + path(f"M{f(x - w * 0.3)},{f(y + h * 0.45)} h{f(w * 0.6)} M{f(x - w * 0.4)},{f(y + h * 0.62)} h{f(w * 0.8)}", stroke=PALE, w=1.4, op=0.8))


def grasping_hand(x, y, rot=15, s=1.0):
    """A right hand closing loosely on something, seen from the back, the four fingers slightly curled
    and spread so that what lies behind shows between them, and the thumb along the index finger.
    The wrist is at (x, y) and the fingers point along -x before rot (degrees, clockwise)."""
    o = []
    for k, (yk, tip, ln) in enumerate([(-19, -27, 40), (-6.5, -10, 46), (6.5, 8, 41), (19, 25, 33)]):
        kx = -56
        d = f"M{kx},{yk} Q{f(kx - ln * 0.55)},{f(yk + (tip - yk) * 0.25 - 2)} {f(kx - ln)},{f(tip + 5)}"
        o.append(tube(d, 8.4, SKIN))
        o.append(ellipse(kx - ln + 2.5, tip + 3.2, 2.6, 3.2, PAPERWHITE, stroke=INK, w=0.9))  # nail
    o.append(path("M0,-12 C-18,-16 -38,-19 -57,-22 C-62,-9 -62,9 -57,22 C-38,19 -18,15 0,13 Z", fill=SKIN, stroke=INK, w=1.8))
    for yk in (-19, -6.5, 6.5, 19):
        o.append(path(f"M-52,{f(yk - 3)} q-4,3 0,6", stroke=PALE, w=1.1, op=0.8))  # knuckles
    o.append(path("M-4,-9 C-22,-13 -34,-14 -48,-15", stroke=PALE, w=1.1, op=0.7))
    o.append(tube("M-8,-12 Q-30,-38 -60,-39 Q-72,-39 -78,-32", 8.6, SKIN))  # thumb
    o.append(path("M-52,-40 q4,-1 7,1", stroke=PALE, w=1.0, op=0.8))
    return f'<g transform="translate({f(x)},{f(y)}) rotate({rot}) scale({s})">{"".join(o)}</g>'


def motes(rng, poly, n, rise=0.0):
    """Specks of dust unevenly spread inside the quadrilateral poly (top-left, top-right, bottom-right, bottom-left)."""
    out = []
    for _ in range(n):
        t, u = rng.random() ** 1.3, rng.random()
        lx0 = poly[0][0] + (poly[3][0] - poly[0][0]) * t
        lx1 = poly[1][0] + (poly[2][0] - poly[1][0]) * t
        y = poly[0][1] + (poly[3][1] - poly[0][1]) * t
        out.append(f'<circle cx="{f(lx0 + (lx1 - lx0) * u)}" cy="{f(y)}" r="{rng.uniform(1.0, 2.3):.1f}" fill="{GREY}" opacity="{rng.uniform(0.35, 0.8):.2f}"/>')
    return "".join(out)


def sheet_with_circle(x, y, w, h, gap=70):
    """A sheet of paper lying on a table (seen from above at a slant) with one brushed circle, open at
    the lower edge. (x, y) is the centre of the sheet."""
    o = [path(f"M{f(x - w / 2 + 14)},{f(y - h / 2)} L{f(x + w / 2 - 10)},{f(y - h / 2)} L{f(x + w / 2 + 14)},{f(y + h / 2)} L{f(x - w / 2 - 12)},{f(y + h / 2)} Z",
              fill=PAPERWHITE, stroke=INK, w=2, filt="brush")]
    rx, ry = w * 0.33, h * 0.38
    pts = []
    for k in range(0, 47):
        a = math.radians(90 + gap / 2 + (360 - gap) * k / 46)
        pts.append((x + rx * math.cos(a), y + 2 + ry * math.sin(a)))
    o.append(path("M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts), stroke=INK, w=7.5, filt="brush"))
    o.append(path("M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts[:6]), stroke=INK, w=3, filt="dry", op=0.8))
    return "".join(o)


def brush_and_stone(x, y, s=1.0):
    """An ink stone with a pool of ink; (x, y) is its centre. The brush is drawn by the caller."""
    o = [path(f"M{f(x - 34 * s)},{f(y - 6 * s)} L{f(x + 34 * s)},{f(y - 8 * s)} L{f(x + 40 * s)},{f(y + 16 * s)} L{f(x - 40 * s)},{f(y + 18 * s)} Z",
              fill="#3f3c38", stroke=INK, w=2, filt="brush"),
         ellipse(x + 2 * s, y + 4 * s, 22 * s, 6 * s, INK, op=0.95)]
    return "".join(o)


def maple(x, y, r=12, ang=0.0, fill=VERMILION):
    """A small five-lobed maple leaf (a star, never a drop), centred at (x, y)."""
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * 0.5
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts) + " Z"
    return (f'<g transform="translate({f(x)},{f(y)}) rotate({f(ang)})"><path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>'
            f'<path d="M0,0 L0,{f(r * 1.4)}" stroke="{INK}" stroke-width="1.3"/></g>')


def stool(x, y, w=70, h=40):
    """A small three-legged stool seen from the side, standing on y, seat at y - h."""
    return (path(f"M{f(x - w / 2 + 6)},{f(y - h + 4)} L{f(x - w / 2)},{f(y)} M{f(x + w / 2 - 6)},{f(y - h + 4)} L{f(x + w / 2)},{f(y)}", w=4, stroke="#6b5a45")
            + path(f"M{f(x - w / 2 - 4)},{f(y - h)} L{f(x + w / 2 + 4)},{f(y - h)}", w=7, stroke="#6b5a45"))


def bedstead(x0, x1, top, drop=70):
    """A low bed seen from the side: mattress edge at `top`, a frame and two feet. Returns the drawing."""
    return (path(f"M{x0},{top} L{x1},{top} L{x1},{top + 24} L{x0},{top + 24} Z", fill="#cfc6b6", stroke=INK, w=2.6, filt="brush")
            + path(f"M{x0 + 10},{top + 24} L{x0 + 10},{top + drop} M{x1 - 10},{top + 24} L{x1 - 10},{top + drop}", w=5, stroke="#6b5a45"))


def awning_stall(x, y, w, h, tone=GREY, goods=4, rng=None):
    """A market stall in fine line: striped awning, two posts, a counter and a row of small wares; y is the ground."""
    top = y - h
    o = [path(f"M{x - 6},{top + 24} L{x + w * 0.1},{top} L{x + w * 0.9},{top} L{x + w + 6},{top + 24} Z", fill=tone, stroke=INK, w=1.4, op=0.28),
         path(f"M{x - 6},{top + 24} L{x + w * 0.1},{top} L{x + w * 0.9},{top} L{x + w + 6},{top + 24} Z", stroke=INK, w=1.4, op=0.7)]
    for k in range(1, 7):
        t = k / 7
        o.append(path(f"M{f(x - 6 + (w + 12) * t)},{top + 24} L{f(x + w * 0.1 + w * 0.8 * t)},{top}", stroke=GREY, w=1, op=0.6))
    o.append(path(f"M{x + 2},{top + 24} L{x + 2},{y} M{x + w - 2},{top + 24} L{x + w - 2},{y}", w=1.8, op=0.7))
    o.append(path(f"M{x},{y - 30} L{x + w},{y - 30}", w=1.8, op=0.8))
    for k in range(goods):
        gx = x + w * (k + 0.5) / goods
        o.append(f'<circle cx="{f(gx)}" cy="{y - 36}" r="5" fill="none" stroke="{GREY}" stroke-width="1.2"/>')
        o.append(path(f"M{f(gx - 6)},{y - 22} h12", stroke=GREY, w=1.2, op=0.7))
    return "".join(o)


def _big_arm(sh, elbow, hand, robe=GREYROBE, w=10):
    """An arm as a tube from shoulder to hand with a hand sized for a figure drawn at about 2x."""
    d = f"M{f(sh[0])},{f(sh[1])} Q{f(elbow[0])},{f(elbow[1])} {f(hand[0])},{f(hand[1])}"
    return tube(d, w, robe) + ellipse(hand[0], hand[1], 7.5, 6.5, SKIN, stroke=INK, w=1.8)


def _ox(x, y, s, pose, flip=False):
    """The water ox with its brush filters swapped for the shared bounding-box ones, which work inside its transformed group."""
    svg, anchors = ox(x, y, s, pose, flip)
    return svg.replace("url(#brush)", "url(#fbrush)").replace("url(#dry)", "url(#fdry)"), anchors


def _wall(x0, x1, y0, y1, op=0.16, col=WALL):
    return path(f"M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z", fill=col, stroke=None, op=op, filt="softwash")


def _attending_up(x, y, s=1.0, flip=False, seat=36, lean=8, reach=(54, -56), robe=GREYROBE):
    """Variant of attending() for a face that shows: the same seated, forward-leaning body and reaching
    arm, but the head is raised on a short neck, the eyes wide and the brows lifted, looking at the hands."""
    hip = (-8, -seat)
    sh = (hip[0] + lean, hip[1] - 38)
    o = []
    knee, foot = (hip[0] + 26, hip[1] + 1), (hip[0] + 24, 0)
    o.append(path(f"M{f(hip[0])},{f(hip[1])} L{f(knee[0])},{f(knee[1])} L{f(foot[0])},{f(foot[1])}", w=3.2))
    o.append(path(f"M{f(foot[0] - 3)},{f(foot[1])} h12", w=3))
    o.append(tube(f"M{f(hip[0])},{f(hip[1])} L{f(knee[0] - 4)},{f(knee[1])}", 15, robe))
    o.append(tube(f"M{f(hip[0])},{f(hip[1])} Q{f(hip[0] + lean * 0.2)},{f(hip[1] - 20)} {f(sh[0])},{f(sh[1])}", 22, robe))
    o.append(_arm(sh, (sh[0] + 14, sh[1] + 16), reach, SKIN))
    hx, hy, r = sh[0] + 7, sh[1] - 25, 11.5
    o.append(path(f"M{f(sh[0] + 2)},{f(sh[1] - 4)} L{f(hx - 1)},{f(hy + r - 2)}", stroke=INK, w=8))
    o.append(path(f"M{f(sh[0] + 2)},{f(sh[1] - 4)} L{f(hx - 1)},{f(hy + r - 2)}", stroke=SKIN, w=5.2))
    o.append(ellipse(hx - r * 0.85, hy - r * 0.55, r * 0.5, r * 0.4, INK))  # hair knot at the back
    o.append(head(hx, hy, r, look=1, wide=True, mouth="shut"))
    o.append(path(f"M{f(hx - r)},{f(hy - r * 0.1)} Q{f(hx - r * 0.9)},{f(hy - r * 1.2)} {f(hx + r * 0.2)},{f(hy - r * 1.1)} Q{f(hx - r * 0.5)},{f(hy - r * 0.75)} {f(hx - r * 0.55)},{f(hy - r * 0.1)}",
                  fill=INK, stroke=INK, w=1))
    for sx in (-1, 1):  # eyebrows lifted high above the eyes
        px = hx + r * 0.32 + sx * r * 0.36
        o.append(path(f"M{f(px - r * 0.24)},{f(hy - r * 0.5)} Q{f(px)},{f(hy - r * 0.78)} {f(px + r * 0.24)},{f(hy - r * 0.5)}", w=1.5))
    return place(x, y, s, flip, "".join(o)), {"hands": [_anchor(x, y, s, flip, reach)]}


def _sitter_front(x, y, s, robe, hk, lean=0.0, tilt=0.0, arms=(), hands=(), sash=None, hat=False):
    """A cross-legged passenger seen from the front, seat at (x, y), about 72 high before scaling.
    lean tips the whole upper body, tilt tips the head alone; arms are tube paths and hands are points."""
    o = [path("M-38,0 C-42,-12 -24,-18 -15,-50 Q0,-60 15,-50 C24,-18 42,-12 38,0 Q0,5 -38,0 Z", fill=robe, w=2.2, filt="fbrush"),
         path("M-30,-6 Q0,-14 30,-6", w=1.5, op=0.6)]
    ub = []
    if sash:
        ub.append(path("M-16,-30 Q0,-24 16,-30", stroke=sash, w=4.5))
    for d, w in arms:
        ub.append(tube(d, w, robe=robe))
    for hx, hy in hands:
        ub.append(ellipse(hx, hy, 3.8, 3.4, SKIN, stroke=INK, w=1.4))
    ub.append(f'<g transform="rotate({f(tilt)} 0 -56)">{head(0, -64, 9, **hk)}</g>')
    o.append(f'<g transform="rotate({f(lean)} 0 -10)">{"".join(ub)}</g>')
    return place(x, y, s, False, "".join(o))


def _ferryman(x, y, s, pole_hand):
    """The ferryman standing at the stern in a wide stance, in the Fourth Rank manner of engaged(): turned
    toward the passengers with one hand raised open, the other on the pole. Feet at (x, y)."""
    legs = path("M-6,-28 L-20,-14 L-32,0 M6,-28 L14,-12 L26,0", w=3)
    feet = path("M-38,0 h10 M22,0 h10", w=3)
    over = (ellipse(pole_hand[0], pole_hand[1], 4, 3.6, SKIN, stroke=INK, w=1.5)
            + ellipse(38, -114, 4, 3.8, SKIN, stroke=INK, w=1.5))
    arms = [(f"M-13,-80 Q-26,-86 {pole_hand[0]},{pole_hand[1]}", 6), ("M13,-84 Q36,-90 38,-112", 6)]
    fig = standing(robe="#c2bcb0", arms=arms, legs=None, sash="#8f8a82",
                   headkw={"look": 1, "hat": True, "mouth": "smile"}, over=over)
    return place(x, y, s, False, legs + feet + fig)


# ------------------------------------------------------------ pips vo01-vo10

def vo01(rng):
    """One of Void: a figure sits in a bare room holding a lantern at arm's length; its light fans over floor and wall, the shadow falls behind."""
    o = [zen_pip_open("void", 1), _wall(VCX - 200, VCX + 200, 530, FLOOR - 30),
         floorboards(FLOOR - 30, FLOOR + 50, VCX - 190, VCX + 190, rows=5)]
    o.append(path(f"M{VCX + 175},{FLOOR - 34} Q{VCX + 178},{FLOOR - 140} {VCX + 174},{FLOOR - 190}", stroke=GREY, w=2, op=0.5, filt="brush"))  # room corner
    px, py, s = VCX - 95, FLOOR - 2, 2.55
    o.append(ellipse(px - 70, FLOOR + 14, 120, 13, GREY, op=0.3, filt="wash"))  # the shadow, behind and to the left
    fig, _ = withdrawn(px, py, s, view="side", eyes_closed=False)
    o.append(fig)
    sh = (px - 6 * s, py - 56 * s)
    hand = (px + 92, py - 176)
    lx, ly = hand
    # light from the lantern: rays to floor and wall
    for tx, ty in [(VCX + 175, FLOOR - 34), (VCX + 120, FLOOR + 26), (VCX + 40, FLOOR + 40), (VCX - 40, FLOOR + 36), (VCX + 170, FLOOR - 120)]:
        o.append(path(f"M{f(lx)},{f(ly + 50)} L{f(tx)},{f(ty)}", stroke=PALE, w=1.1, op=0.5))
    o.append(_big_arm(sh, (px + 32, py - 142), hand, GREYROBE, 13))
    o.append(path(f"M{f(lx)},{f(ly + 6)} L{f(lx)},{f(ly + 16)}", w=2.2))
    o.append(lantern(lx, ly + 16, 62, 84))
    return finish(o + [zen_pip_close()])


def vo02(rng):
    """Two of Void: fresh footprints cross smooth sand and stop at the edge of a still pool that holds the sky; no one is near."""
    px, py = VCX + 80, FLOOR - 28
    # the horizon sits above the pool's far edge, so the pool lies in the sand
    o = [zen_pip_open("void", 2), ground(py - 62, VX0 + 10, VX1 - 10, op=0.2)]
    o.append(ellipse(px, py, 120, 46, SKY, op=0.6, filt="softwash"))
    o.append(ellipse(px, py, 120, 46, "none", stroke=GREY, w=1.8, op=0.75, filt="brush"))
    for k, (dx, dy, wd) in enumerate([(-44, -8, 44), (28, 6, 52), (-10, 15, 32)]):  # clouds in the sky reflected
        o.append(path(f"M{f(px + dx - wd / 2)},{f(py + dy)} Q{f(px + dx)},{f(py + dy - 8)} {f(px + dx + wd / 2)},{f(py + dy)}", stroke=PALE, w=2.4, op=0.7))
    o.append(ripple(px + 36, py + 4, 20, 2, op=0.5))
    # a trail of paired prints, left and right feet either side of the line of walking, toes toward the pool
    (x0, y0), (x1, y1) = (VX0 + 30, FLOOR + 62), (px - 118, py + 12)
    n, ang = 6, 40
    ux, uy = x1 - x0, y1 - y0
    ln = math.hypot(ux, uy)
    nx, ny = -uy / ln, ux / ln  # to the walker's right
    pts = []
    for k in range(n):
        t = k / (n - 1)
        side = -1 if k % 2 == 0 else 1
        pts.append((x0 + ux * t + nx * 15 * side, y0 + uy * t + ny * 15 * side, 1.25 - 0.3 * t, ang, side))
    o.append(footprints(pts))
    for _ in range(26):  # sand grain
        o.append(f'<circle cx="{f(rng.uniform(VX0 + 10, VX1 - 10))}" cy="{f(rng.uniform(FLOOR - 4, FLOOR + 80))}" r="1.1" fill="{PALE}" opacity="0.6"/>')
    o.append(grass(rng, px + 80, px + 118, py - 20, py - 14, 8, 20, 48))
    return finish(o + [zen_pip_close()])


def vo03(rng):
    """Three of Void: a bell has just been struck; widening rings cross a quiet courtyard while a monk on the veranda turns his head."""
    G = FLOOR + 10
    o = [zen_pip_open("void", 3), ground(G, VX0 + 10, VX1 - 10, op=0.14)]
    bx, beam = VCX - 105, 552
    o.append(path(f"M{bx - 86},{G} Q{bx - 84},{(G + beam) // 2} {bx - 86},{beam}", stroke=INK, w=9, filt="dry"))
    o.append(path(f"M{bx + 86},{G} Q{bx + 88},{(G + beam) // 2} {bx + 86},{beam}", stroke=INK, w=9, filt="dry"))
    for r, op in ((26, 0.8), (52, 0.6), (78, 0.4)):  # the sound, widening from the bell's mouth
        o.append(f'<circle cx="{bx}" cy="654" r="{r}" fill="none" stroke="{GREY}" stroke-width="2.4" opacity="{op}"/>')
    o.append(path(f"M{bx - 102},{beam} L{bx + 102},{beam - 2}", w=10, filt="brush"))
    o.append(bell(bx, 592, 56, 62))
    o.append(path(f"M{bx + 58},{beam + 2} L{bx + 66},{650}", stroke=GREY, w=1.8))  # the striker hangs on a cord, swung back
    o.append(path(f"M{bx + 36},{672} L{bx + 100},{646}", stroke=INK, w=9, filt="brush"))
    for k in range(4):  # raked gravel
        o.append(path(f"M{VX0 + 36},{G + 14 + k * 14} Q{VCX - 40},{G + 8 + k * 14} {VCX + 70},{G + 14 + k * 14}", stroke=PALE, w=1.3, op=0.6))
    vx = VCX + 130
    o.append(path(f"M{vx - 90},{G - 24} L{vx + 68},{G - 24} L{vx + 68},{G + 6} L{vx - 90},{G + 6} Z", fill=WOOD, stroke=INK, w=2.4, op=0.55, filt="brush"))
    monk = place(vx - 10, G - 24, 1.8, True,
                 standing(robe=GREYROBE, arms="down", long=True, barefoot=True, headkw={"look": 1, "hair": False}))
    o.append(monk)
    return finish(o + [zen_pip_close()])


def vo04(rng):
    """Four of Void: a hand closes around a shaft of light from a window; the light spills through the fingers, dust moves unevenly."""
    o = [zen_pip_open("void", 4), _wall(VCX - 200, VCX + 200, 535, FLOOR - 20, op=0.14)]
    o.append(window_frame(VCX - 170, 545, VCX - 60, 665, bars=(2, 2), sky="#e3e6e4"))
    o.append(path(f"M{VCX - 190},{FLOOR - 20} Q{VCX},{FLOOR - 26} {VCX + 190},{FLOOR - 20}", stroke=GREY, w=1.6, op=0.5, filt="brush"))
    poly = [(VCX - 170, 665), (VCX - 60, 665), (VCX + 55, 770), (VCX - 75, 770)]
    o.append(light_beam(poly, op=0.34))
    o.append(motes(rng, poly, 18))
    o.append(path(f"M{VCX + 20},{FLOOR + 38} Q{VCX + 80},{FLOOR + 30} {VCX + 130},{FLOOR + 40}", stroke=GREY, w=14, op=0.12, filt="softwash"))  # light on the floor
    wx, wy = VCX + 32, 722
    # the forearm comes in from the edge of the circle: a sleeve, then the bare wrist
    o.append(tube(f"M{VCX + 250},{FLOOR + 88} Q{VCX + 160},{FLOOR + 50} {wx + 62},{wy + 17}", 28, GREYROBE))
    o.append(tube(f"M{wx + 66},{wy + 18} L{wx + 4},{wy + 1}", 12, SKIN))
    o.append(closed_hand(wx - 8, wy, 1.15))
    # light from the beam spills over the knuckles
    o.append(ellipse(wx - 30, wy - 14, 34, 16, "#fff6dc", op=0.55, filt="wash"))
    return finish(o + [zen_pip_close()])


def closed_hand(x, y, s=1.0):
    """A right hand loosely closed, seen from the side, knuckles up: the back of the hand, four folded
    fingers as a row of rounded knuckles, and the thumb folded across. The wrist is at (x, y), the
    fingers toward -x."""
    k = s
    back = (f"M{f(x)},{f(y - 13 * k)} C{f(x - 18 * k)},{f(y - 20 * k)} {f(x - 40 * k)},{f(y - 22 * k)} {f(x - 52 * k)},{f(y - 14 * k)} "
            f"C{f(x - 62 * k)},{f(y - 6 * k)} {f(x - 62 * k)},{f(y + 12 * k)} {f(x - 50 * k)},{f(y + 18 * k)} "
            f"C{f(x - 34 * k)},{f(y + 22 * k)} {f(x - 14 * k)},{f(y + 16 * k)} {f(x)},{f(y + 12 * k)} Z")
    o = [path(back, fill=SKIN, stroke=INK, w=2.0)]
    for j in range(4):  # knuckles of the folded fingers along the front
        cx_ = x - (50 - j * 1.5) * k
        cy_ = y + (-9 + j * 7.5) * k
        o.append(f'<path d="M{f(cx_ + 4 * k)},{f(cy_ - 3.5 * k)} q{f(-8 * k)},{f(1 * k)} {f(-8 * k)},{f(3.5 * k)} q0,{f(3 * k)} {f(8 * k)},{f(3.5 * k)}" '
                 f'fill="none" stroke="{INK}" stroke-width="1.3" opacity="0.75"/>')
    # the thumb folded across the fingers
    o.append(path(f"M{f(x - 14 * k)},{f(y + 8 * k)} C{f(x - 26 * k)},{f(y + 14 * k)} {f(x - 40 * k)},{f(y + 12 * k)} {f(x - 46 * k)},{f(y + 4 * k)}",
                  stroke=INK, w=2.0))
    o.append(path(f"M{f(x - 30 * k)},{f(y - 17 * k)} q{f(-6 * k)},{f(4 * k)} {f(-12 * k)},{f(3 * k)}", stroke=INK, w=1.1, op=0.5))  # a crease on the back
    return "".join(o)


def vo05(rng):
    """Five of Void: a herdsman walks a path through tall grass with a loose cord trailing; the ox wanders a little way off. The sky is empty."""
    o = [zen_pip_open("void", 5), ground(FLOOR - 4, VX0 + 10, VX1 - 10, op=0.16)]
    o.append(path(f"M{VX0 + 10},{FLOOR + 44} Q{VCX - 40},{FLOOR + 20} {VX1 - 20},{FLOOR - 2}", stroke="#cfc6b6", w=30, op=0.45, filt="softwash"))
    o.append(grass(rng, VX0 + 20, VX1 - 20, FLOOR + 14, FLOOR + 70, 40, 20, 52))
    ox_, oa = _ox(VCX + 100, FLOOR + 6, 0.85, "walk")
    o.append(ox_)
    fig, a = herdsman(VCX - 130, FLOOR + 26, 2.0, "walk")
    o.append(fig)
    hand, nose = a["hands"][0], oa["neck"]
    o.append(rope(hand, (nose[0] - 16, nose[1] + 4), sag=44, col=GREY, w=2))
    o.append(grass(rng, VX0 + 20, VX1 - 20, FLOOR + 30, FLOOR + 86, 30, 24, 60))
    return finish(o + [zen_pip_close()])


def vo06(rng):
    """Six of Void: a boy rides sideways on an ox along a river at dusk, playing a flute; the far bank is a pale line, no mountains."""
    o = [zen_pip_open("void", 6)]
    o.append(water(VX0 - 20, VX1 + 20, FLOOR - 78, FLOOR + 22, op=0.5, col=SKY))
    o.append(path(f"M{VX0},{FLOOR - 82} Q{VCX},{FLOOR - 88} {VX1},{FLOOR - 80}", stroke=PALE, w=2.2, op=0.7, filt="brush"))
    o.append(ground(FLOOR + 40, VX0 + 10, VX1 - 10, op=0.16))
    o.append(ripple(VCX - 100, FLOOR - 30, 70, 2, op=0.45))
    o.append(ripple(VCX + 130, FLOOR - 50, 50, 2, op=0.45))
    ox_, oa = _ox(VCX - 10, FLOOR + 54, 1.3, "ride")
    o.append(ox_)
    nose = oa["nose"]
    o.append(path(f"M{f(nose[0])},{f(nose[1])} q-5,38 -24,52", stroke=GREY, w=2.2))
    back = oa["back"]
    fig, a = herdsman(back[0] + 19, back[1] + 49, 2.0, "ride", pale_legs=True)
    o.append(fig)
    hd = a["head"]
    m = (hd[0] + 8, hd[1] + 11)
    o.append(path(f"M{f(m[0] - 27)},{f(m[1] + 4)} L{f(m[0] + 69)},{f(m[1] - 10)}", stroke=VERMILION, w=4.6))
    o.append(grass(rng, VX0 + 40, VX1 - 40, FLOOR + 50, FLOOR + 62, 24, 14, 26))
    return finish(o + [zen_pip_close()])


def vo07(rng):
    """Seven of Void: a man sits eyes closed on the veranda of a thatched hut, a rope coiled in the dust (the accent) and an empty stall behind; the sky is wide and plain."""
    o = [zen_pip_open("void", 7), ground(FLOOR, VX0 + 10, VX1 - 10, op=0.14)]
    o.append(hut(VCX + 66, FLOOR - 108, 130, 108))
    for sx in (VCX - 185, VCX - 120):  # the empty stall
        o.append(path(f"M{sx},{FLOOR} Q{sx + 3},{FLOOR - 55} {sx},{FLOOR - 110}", stroke=INK, w=6, filt="dry"))
    o.append(path(f"M{VCX - 188},{FLOOR - 104} L{VCX - 117},{FLOOR - 106} M{VCX - 188},{FLOOR - 60} L{VCX - 117},{FLOOR - 62}", stroke="#6b5a45", w=4))
    o.append(path(f"M{VCX - 180},{FLOOR + 2} L{VCX - 125},{FLOOR + 2}", stroke=WOOD, w=8, op=0.6))
    o.append(path(f"M{VCX - 90},{FLOOR - 16} L{VCX + 195},{FLOOR - 16} L{VCX + 195},{FLOOR + 8} L{VCX - 90},{FLOOR + 8} Z", fill=WOOD, stroke=INK, w=2.4, op=0.7, filt="brush"))
    fig, _ = withdrawn(VCX - 10, FLOOR - 14, 1.95, view="side", eyes_closed=True)
    o.append(fig)
    o.append(coil(VCX - 60, FLOOR + 42, VERMILION, 1.9))
    o.append(grass(rng, VX0 + 20, VX1 - 20, FLOOR + 30, FLOOR + 60, 14, 8, 20))
    return finish(o + [zen_pip_close()])


def vo08(rng):
    """Eight of Void: on a low table a sheet of paper bears one brushed circle open at the lower edge; a brush rests by the ink stone."""
    o = [zen_pip_open("void", 8)]
    o.append(path(f"M{VX0 + 6},{FLOOR - 40} L{VX1 - 6},{FLOOR - 40} L{VX1 + 20},{FLOOR + 50} L{VX0 - 20},{FLOOR + 50} Z", fill=WOOD, stroke=None, op=0.3, filt="softwash"))
    o.append(path(f"M{VX0 + 6},{FLOOR - 40} Q{VCX},{FLOOR - 46} {VX1 - 6},{FLOOR - 40}", stroke=GREY, w=1.8, op=0.6, filt="brush"))
    o.append(sheet_with_circle(VCX + 30, FLOOR - 8, 250, 140))
    o.append(brush_and_stone(VX0 + 50, FLOOR - 4, 0.8))
    o.append(path(f"M{VX0 + 36},{FLOOR + 50} L{VX0 + 122},{FLOOR + 32}", stroke=INK, w=7))
    o.append(path(f"M{VX0 + 36},{FLOOR + 50} L{VX0 + 122},{FLOOR + 32}", stroke="#8a7a52", w=4.6))
    o.append(path(f"M{VX0 + 122},{FLOOR + 32} L{VX0 + 148},{FLOOR + 27}", stroke=INK, w=5))
    return finish(o + [zen_pip_close()])


def vo09(rng):
    """Nine of Void: an open window in an empty room looks out on a wet garden; a bowl on the sill holds the grey sky and a maple leaf (the accent) drifts across. No one is drawn."""
    o = [zen_pip_open("void", 9), _wall(VCX - 200, VCX + 200, 530, FLOOR + 20, op=0.12)]
    x0, x1, y0, y1 = VCX - 135, VCX + 135, 540, FLOOR - 55
    o.append(path(f"M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z", fill="#e8ebe8", stroke=None, op=0.8, filt="softwash"))
    o.append(path(f"M{x0 + 4},{y1 - 62} Q{VCX},{y1 - 72} {x1 - 4},{y1 - 60}", stroke=GREY, w=1.6, op=0.5, filt="brush"))  # garden wall line
    o.append(rock(rng, VCX - 70, y1 - 8, 28, 13, op=0.45))
    o.append(rock(rng, VCX + 60, y1 - 4, 20, 10, op=0.4))
    o.append(grass(rng, x0 + 10, x1 - 10, y1 - 44, y1 - 6, 16, 10, 24))
    o.append(rain(rng, x0 + 10, x1 - 10, y0 + 8, y1 - 60, 16, op=0.5))
    o.append(maple(VCX + 50, y0 + 80, 14, ang=28))
    o.append(path(f"M{VCX + 110},{y0 + 44} Q{VCX + 80},{y0 + 50} {VCX + 56},{y0 + 66}", stroke=PALE, w=1.2, op=0.6))
    o.append(window_frame(x0, y0, x1, y1, bars=(1, 1), w=4.4))
    o.append(path(f"M{x0 - 18},{y1 + 6} L{x1 + 18},{y1 + 6} L{x1 + 18},{y1 + 22} L{x0 - 18},{y1 + 22} Z", fill=WOOD, stroke=INK, w=2.4, op=0.8, filt="brush"))
    o.append(chawan(VCX - 60, y1 - 22, 76, filled="#a9aeb0"))
    o.append(path(f"M{VCX - 84},{y1 - 22} q12,-4 24,0 M{VCX - 70},{y1 - 15} q12,-4 26,0", stroke=PAPERWHITE, w=2, op=0.9))  # sky in the bowl
    o.append(path(f"M{VCX - 190},{FLOOR + 40} Q{VCX},{FLOOR + 32} {VCX + 190},{FLOOR + 40}", stroke=GREY, w=1.6, op=0.5, filt="brush"))
    return finish(o + [zen_pip_close()])


def vo10(rng):
    """Ten of Void: a barefoot man in a market street holds a door for a woman with a heavy basket while a child looks up at him; the stalls are drawn in fine detail, the man in few lines."""
    G = FLOOR + 26
    o = [zen_pip_open("void", 10), ground(G, VX0 + 10, VX1 - 10, op=0.14)]
    for k, (sx, sw, sh_) in enumerate([(152, 82, 150), (236, 74, 138), (316, 88, 150), (410, 70, 140)]):
        o.append(awning_stall(sx, G - 6, sw, sh_, goods=4 + k % 2))
    mx = 398
    dx = mx + 56  # the door posts and the leaf standing open
    o.append(path(f"M{dx},{G + 4} L{dx},{G - 205} M{dx + 62},{G + 4} L{dx + 62},{G - 205} M{dx - 6},{G - 205} L{dx + 68},{G - 205}", stroke=INK, w=7, filt="brush"))
    o.append(path(f"M{dx + 6},{G - 200} L{dx + 46},{G - 184} L{dx + 46},{G - 6} L{dx + 6},{G + 2} Z", fill="#cfc6b6", stroke=INK, w=2.6, op=0.85, filt="brush"))
    man = place(mx, G, 2.2, True,
                standing(robe=GREYROBE, arms="down", long=True, barefoot=True, headkw={"look": 1, "hair": False, "mouth": "smile"},
                         extra_arms=[("M-13,-80 Q-30,-82 -44,-76", 6)]))
    o.append(man)
    wx, ws = 188, 1.9
    wf, wa = ordinary(wx, G, ws, flip=False, tool=None)
    o.append(wf)
    sh = (wx + 6 * ws, G - 70 * ws)
    bx, by = wx + 34 * ws, G - 34 * ws
    o.append(_arm(sh, (sh[0] + 28, sh[1] + 40), (bx - 28, by - 8), SKIN, 6))
    o.append(path(f"M{bx - 44},{by - 10} Q{bx},{by - 28} {bx + 44},{by - 10} L{bx + 34},{by + 48} Q{bx},{by + 58} {bx - 34},{by + 48} Z", fill=STRAW, stroke=INK, w=2.4, filt="brush"))
    for k in range(3):
        o.append(path(f"M{bx - 36 + k * 5},{by + k * 15 + 6} Q{bx},{by + k * 15 + 13} {bx + 36 - k * 5},{by + k * 15 + 6}", stroke=GREY, w=1.3, op=0.7))
    cf = place(334, G, 1.25, False, standing(robe="#c9c4ba", arms="down", headkw={"look": 1, "hair": True}))
    o.append(cf)
    return finish(o + [zen_pip_close()])


# ------------------------------------------------------------ ranks vo11-vo15

def vo11(rng):
    """First Rank of Void: a sitter in a bare room before a blank wall, hands in the cosmic mudra, the window shuttered; a closed letter lies in dust on the floor."""
    o = [zen_rank_open("void", 1)]
    base = SY1 - 150
    o.append(_wall(SX0, SX1, 300, base, op=0.2))
    o.append(floorboards(base, base + 120, SX0 + 20, SX1 - 20, rows=6, col="#a79e8f"))
    wx0, wy0, wx1, wy1 = SX0 + 50, 380, SX0 + 170, 640
    o.append(path(f"M{wx0},{wy0} L{wx1},{wy0} L{wx1},{wy1} L{wx0},{wy1} Z", fill="#cfc6b6", stroke=None, op=0.8, filt="softwash"))
    for k in range(1, 14):
        yy = wy0 + (wy1 - wy0) * k / 14
        o.append(path(f"M{wx0},{f(yy)} L{wx1},{f(yy + 4)}", stroke=GREY, w=1.5, op=0.7))
    o.append(path(f"M{wx0},{wy0} L{wx1},{wy0} L{wx1},{wy1} L{wx0},{wy1} Z", w=4, filt="brush"))
    fig, a = withdrawn(SCX + 50, base + 60, 3.0, view="front", robe="#b3ad9f")
    o.append(fig)
    lx, ly = SCX - 150, base + 76
    o.append(path(f"M{lx - 36},{ly} L{lx + 40},{ly - 6} L{lx + 52},{ly + 20} L{lx - 28},{ly + 26} Z", fill=PAPERWHITE, stroke=INK, w=2, filt="brush"))
    o.append(path(f"M{lx - 36},{ly} L{lx + 8},{ly + 14} L{lx + 40},{ly - 6}", stroke=GREY, w=1.4, op=0.8))
    o.append(f'<rect x="{lx - 2}" y="{ly + 8}" width="9" height="9" fill="{VERMILION}" opacity="0.9"/>')
    o.append(ellipse(lx + 8, ly + 12, 54, 13, GREY, op=0.22, filt="wash"))
    for _ in range(22):  # dust
        o.append(f'<circle cx="{f(lx + rng.gauss(0, 24))}" cy="{f(ly + 10 + rng.gauss(0, 7))}" r="{rng.uniform(0.8, 1.8):.1f}" fill="{PALE}" opacity="0.7"/>')
    return finish(o + [zen_rank_close()])


def vo12(rng):
    """Second Rank of Void: a woman at a kitchen table has stopped peeling an orange (the accent); window light falls on the long spiral of peel."""
    o = [zen_rank_open("void", 2)]
    base = SY1 - 150
    s = 3.0
    gy = base + 16  # the ground under the stool and the table legs
    o.append(_wall(SX0, SX1, 330, base, op=0.18))
    o.append(floorboards(base, base + 110, SX0 + 20, SX1 - 20, rows=6, col="#a79e8f"))
    o.append(window_frame(SX0 + 40, 400, SX0 + 170, 620, bars=(2, 3), sky="#dfe4e3", w=4))
    px = SCX - 130
    hx, ty = px + 54 * s, gy - 54 * s
    tx0, tx1 = hx - 40, SX1 - 24
    o.append(path(f"M{tx0 + 20},{ty} L{tx0 + 40},{gy + 6} M{tx1 - 30},{ty} L{tx1 - 22},{gy + 6}", stroke="#6b5a45", w=7))
    o.append(path(f"M{tx0},{ty} L{tx1},{ty} L{tx1 + 10},{ty + 16} L{tx0 - 10},{ty + 16} Z", fill=WOOD, stroke=INK, w=2.6, op=0.85, filt="brush"))
    o.append(light_beam([(SX0 + 60, 600), (SX0 + 160, 610), (hx + 120, ty), (hx + 20, ty)], op=0.1, edge=False))
    o.append(ellipse(hx + 70, ty + 1, 70, 7, PAPERWHITE, op=0.85, filt="wash"))
    o.append(stool(px - 8, gy, 100, 36 * s - 8))
    fig, a = _attending_up(px, gy, s, False, seat=36, lean=8, reach=(54, -56), robe="#b8b2a6")
    o.append(fig)
    hx_, hy_ = a["hands"][0]
    ox_, oy = hx_ + 16, ty - 17
    o.append(f'<circle cx="{f(ox_)}" cy="{f(oy)}" r="17" fill="{VERMILION}" opacity="0.92" stroke="{INK}" stroke-width="1.4"/>')
    o.append(path(f"M{f(ox_ + 6)},{f(oy + 14)} Q{f(ox_ + 30)},{f(oy + 30)} {f(ox_ + 44)},{f(oy + 10)} Q{f(ox_ + 62)},{f(oy - 4)} {f(ox_ + 76)},{f(oy + 14)} "
                  f"Q{f(ox_ + 88)},{f(oy + 24)} {f(ox_ + 98)},{f(oy + 14)}", stroke="#d99a7a", w=3.2))
    return finish(o + [zen_rank_close()])


def _patient(hand_x, top, x1):
    """A patient lying on his back on a bed whose mattress top is at `top` and right end at x1: head in
    profile on the pillow, eyes closed; body under a blanket with a turned-down fold; the near arm on
    top of the blanket, wrist and hand toward hand_x, where a carer's hand can rest on the wrist."""
    o = []
    hcx, hcy = x1 - 52, top - 26  # head centre
    o.append(path(f"M{x1 - 104},{top} Q{x1 - 100},{top - 22} {x1 - 66},{top - 22} L{x1 - 14},{top - 20} Q{x1 - 4},{top - 10} {x1 - 10},{top} Z",
                  fill="#ebe4d3", stroke=INK, w=2))  # pillow
    # the body under the blanket: shoulders high at the pillow, falling to the feet at the far end
    feet = hand_x - 40
    body = (f"M{x1 - 84},{top} C{x1 - 88},{top - 40} {x1 - 120},{top - 46} {x1 - 160},{top - 40} "
            f"C{x1 - 220},{top - 32} {feet + 70},{top - 28} {feet + 30},{top - 34} "
            f"C{feet + 10},{top - 38} {feet},{top - 22} {feet},{top} Z")
    o.append(path(body, fill="#d9d2c2", stroke=INK, w=2.4))
    o.append(path(f"M{x1 - 94},{top - 30} Q{x1 - 128},{top - 22} {x1 - 160},{top - 32}", stroke=INK, w=1.6, op=0.6))  # the turned-down fold
    o.append(path(f"M{feet + 40},{top - 30} q-8,10 -6,26", stroke=GREY, w=1.4, op=0.6))  # the feet beneath
    # the head in profile, facing up: skull, closed eye, nose, ear, a little hair
    o.append(ellipse(hcx, hcy, 21, 18, SKIN, stroke=INK, w=2))
    o.append(path(f"M{hcx - 18},{hcy - 6} q2,-4 6,-5", stroke=INK, w=1.6))  # nose
    o.append(path(f"M{hcx - 9},{hcy - 9} q4,2 8,0", stroke=INK, w=1.4))     # closed eye
    o.append(ellipse(hcx + 6, hcy + 2, 4, 5, SKIN, stroke=INK, w=1.3))      # ear
    o.append(path(f"M{hcx + 2},{hcy - 17} Q{hcx + 20},{hcy - 16} {hcx + 20},{hcy + 6}", stroke=GREY, w=4, op=0.8))  # hair on the pillow
    # the near arm on top of the blanket: shoulder, elbow, wrist, hand
    sh = (x1 - 98, top - 30)
    el = (x1 - 168, top - 28)
    wr = (hand_x + 18, top - 22)
    o.append(path(f"M{sh[0]},{sh[1]} Q{(sh[0] + el[0]) / 2},{sh[1] - 6} {el[0]},{el[1]}", stroke=INK, w=14))
    o.append(path(f"M{sh[0]},{sh[1]} Q{(sh[0] + el[0]) / 2},{sh[1] - 6} {el[0]},{el[1]}", stroke="#ebe4d3", w=10))  # nightshirt sleeve
    o.append(path(f"M{el[0]},{el[1]} L{wr[0]},{wr[1]}", stroke=INK, w=11))
    o.append(path(f"M{el[0]},{el[1]} L{wr[0]},{wr[1]}", stroke=SKIN, w=7.5))   # bare forearm
    o.append(path(f"M{el[0] + 2},{el[1] - 5} l0,10", stroke=INK, w=1.6))       # cuff
    o.append(ellipse(wr[0] - 10, wr[1] + 1, 11, 7, SKIN, stroke=INK, w=1.6))   # the open hand, palm down
    o.append(path(f"M{wr[0] - 18},{wr[1] - 2} l-6,2 M{wr[0] - 18},{wr[1] + 3} l-6,2", stroke=INK, w=1.2, op=0.7))  # fingers
    return "".join(o)


def vo13(rng):
    """Third Rank of Void: a nurse stands by a bed at night under a shaded lamp, one hand lightly on the patient's wrist; the window behind is a dark rectangle."""
    o = [zen_rank_open("void", 3)]
    base = SY1 - 150
    s = 2.6
    gy = base + 16
    o.append(_wall(SX0, SX1, 320, base, op=0.2))
    o.append(floorboards(base, base + 110, SX0 + 20, SX1 - 20, rows=6, col="#9a907f"))
    o.append(path(f"M{SCX + 10},400 L{SCX + 130},400 L{SCX + 130},590 L{SCX + 10},590 Z", fill=INK, stroke=None, op=0.5, filt="softwash"))
    o.append(window_frame(SCX + 10, 400, SCX + 130, 590, bars=(2, 2), w=4))
    nx = SCX - 90
    hx, hy = nx + 46 * s, gy - 60 * s
    top = hy + 20
    o.append(bedstead(hx - 70, SX1 - 6, top, gy - top + 6))
    # the patient, scaled up about the bed's right end, his wrist kept under the nurse's hand
    k, x1 = 1.5, SX1 - 6
    o.append(f'<g transform="translate({x1},{top}) scale({k}) translate({-x1},{-top})">'
             + _patient(x1 + (hx - x1) / k, top, x1) + '</g>')
    lx = SX0 + 50  # an oil lamp on a small low table at the left
    o.append(path(f"M{lx - 32},{base - 130} L{lx + 32},{base - 130}", w=8, stroke="#6b5a45"))
    o.append(path(f"M{lx - 24},{base - 128} L{lx - 27},{base + 12} M{lx + 24},{base - 128} L{lx + 27},{base + 12}", stroke="#6b5a45", w=5))
    o.append(oil_lamp(lx, base - 134, 1.8))
    fig, a = acting(nx, gy, s, False, strike=False, reach=(46, -60), robe="#d8d1c1")
    o.append(fig)
    return finish(o + [zen_rank_close()])


def vo14(rng):
    """Fourth Rank of Void: a ferryman poles a crowded boat over a wide river in morning mist, answering a passenger while he keeps his line; the far shore is not yet visible."""
    o = [zen_rank_open("void", 4)]
    wl = SY1 - 300
    o.append(water(SX0, SX1, wl - 130, wl + 220, op=0.45, col=SKY))
    o.append(ripple(SCX - 140, wl + 80, 110, 3, op=0.45))
    o.append(ripple(SCX + 120, wl + 130, 90, 3, op=0.4))
    o.append(boat(SCX, wl, 440, 36))
    fx = SX0 + 120
    gy = wl - 8
    px0, py0 = fx - 38, wl - 340  # the pole slants from above his head down into the water behind the stern
    px1, py1 = fx - 112, wl + 170
    o.append(path(f"M{px0},{py0} L{px1},{py1}", stroke=INK, w=9))
    o.append(path(f"M{px0},{py0} L{px1},{py1}", stroke="#8a7a52", w=5.4))
    o.append(path(f"M{px1 + 3},{py1 - 6} L{px1},{py1}", stroke=PALE, w=3))
    t = (gy - 144 - py0) / (py1 - py0)
    grip = (px0 + (px1 - px0) * t, gy - 144)
    o.append(_ferryman(fx, gy, 2.0, ((grip[0] - fx) / 2.0, (grip[1] - gy) / 2.0)))
    # three passengers: a talker, one who answers him, and one dozing with his head tipped to the side
    o.append(_sitter_front(SCX - 20, gy, 1.3, "#b3ad9f", {"look": 1, "hair": True, "knot": True, "mouth": "open"},
                           arms=[("M-13,-52 Q-30,-32 -7,-20", 6), ("M13,-50 Q38,-58 36,-80", 6)], hands=[(36, -82)], sash="#8f8a82"))
    o.append(_sitter_front(SCX + 78, gy, 1.3, "#d8d2c5", {"look": -1, "band": True},
                           arms=[("M-13,-52 Q-34,-52 -32,-72", 6), ("M13,-52 Q30,-32 7,-20", 6)], hands=[(-32, -74)], sash=GREY))
    o.append(_sitter_front(SCX + 176, gy, 1.3, "#9d9689", {"hat": True}, lean=7, tilt=22,
                           arms=[("M-13,-52 Q-30,-32 -7,-20", 6), ("M13,-52 Q30,-32 7,-20", 6)]))
    o.append(path(f"M{SCX + 188},{gy - 122} q4,3 8,0 M{SCX + 202},{gy - 120} q4,3 8,0", w=1.3, op=0.9))  # closed eyes of the sleeper
    o.append(boat(SCX, wl, 440, 36))
    o.append(mist(SX1 - 40, wl - 150, 230, 80, 0.95))
    o.append(mist(SCX, wl + 190, 280, 40, 0.8))
    o.append(mist(SX0 + 50, wl - 190, 150, 40, 0.7))
    return finish(o + [zen_rank_close()])


def vo15(rng):
    """Fifth Rank of Void: an old man sweeps the steps of a small shrine at dawn in a plain robe; a few leaves lie on the stone. Nothing draws the eye."""
    o = [zen_rank_open("void", 5)]
    base = SY1 - 150
    MOSS = "#8a9170"
    j = lambda a=2.0: rng.uniform(-a, a)
    o.append(mist(SCX, base - 120, 300, 36, 0.6))
    # four stone steps: each a riser and a tread, narrowing a little as they rise
    n, rise, depth, y0, hw0, dec = 4, 32, 26, base + 40, 168, 8
    tops = []
    for k in range(n):
        yb = y0 - k * (rise + depth)
        yt, ybk = yb - rise, yb - rise - depth
        hw, hwb = hw0 - k * dec, hw0 - (k + 1) * dec
        o.append(path(f"M{f(SCX - hw + j())},{f(yb + j(1))} L{f(SCX + hw + j())},{f(yb + j(1))} L{f(SCX + hw + j())},{f(yt + j(1))} L{f(SCX - hw + j())},{f(yt + j(1))} Z",
                      fill="#bdb6a8", stroke=INK, w=2.2, op=0.9, filt="brush"))
        o.append(path(f"M{f(SCX - hw + j())},{f(yt)} L{f(SCX + hw + j())},{f(yt)} L{f(SCX + hwb + j())},{f(ybk + j(1))} L{f(SCX - hwb + j())},{f(ybk + j(1))} Z",
                      fill="#e4ded0", stroke=INK, w=2, op=0.95, filt="brush"))
        o.append(path(f"M{f(SCX - hw + 4)},{f(yt + 3)} L{f(SCX + hw - 4)},{f(yt + 3)}", stroke=PAPERWHITE, w=2, op=0.8))
        for _ in range(3):  # joints in the riser and a crack or two in the tread
            jx = SCX + rng.uniform(-hw + 20, hw - 20)
            o.append(path(f"M{f(jx)},{f(yt + 3)} L{f(jx + j(3))},{f(yb - 2)}", stroke=GREY, w=1.2, op=0.5))
        cx_ = SCX + rng.uniform(-hw * 0.6, hw * 0.6)
        o.append(path(f"M{f(cx_)},{f(yt - 3)} l{f(rng.uniform(8, 18))},{f(-rng.uniform(4, 9))}", stroke=GREY, w=1.1, op=0.5))
        for sx in (-1, 1):  # moss where the stone is damp: the corners and the foot of the riser
            o.append(ellipse(SCX + sx * (hw - 6), yb - 4, 15, 5, MOSS, op=0.6, filt="wash"))
            o.append(ellipse(SCX + sx * (hw - 20), yt + 2, 9, 3, MOSS, op=0.5, filt="wash"))
        for _ in range(2):
            mx = SCX + rng.uniform(-hw + 30, hw - 30)
            o.append(ellipse(mx, yb - 2, rng.uniform(8, 16), 3.2, MOSS, op=0.45, filt="wash"))
        tops.append(ybk)
    ly = tops[-1]  # the landing
    hwl = hw0 - n * dec
    o.append(path(f"M{SCX - hwl},{ly} L{SCX + hwl},{ly} L{SCX + hwl - 6},{ly - 16} L{SCX - hwl + 6},{ly - 16} Z", fill="#d8d2c4", stroke=INK, w=1.8, op=0.9, filt="brush"))
    # the shrine: a stone plinth, a small timber box with a lattice door, a heavy hipped roof with crossed finials
    sx0, sx1 = SCX - 58, SCX + 58
    o.append(path(f"M{sx0 - 10},{ly - 12} L{sx1 + 10},{ly - 12} L{sx1 + 10},{ly - 28} L{sx0 - 10},{ly - 28} Z", fill="#bdb6a8", stroke=INK, w=2.2, filt="brush"))
    wt = ly - 112
    o.append(path(f"M{sx0},{ly - 28} L{sx1},{ly - 28} L{sx1},{wt} L{sx0},{wt} Z", fill="#e8e1d0", stroke=INK, w=2.4, filt="brush"))
    o.append(path(f"M{SCX - 24},{ly - 30} L{SCX + 24},{ly - 30} L{SCX + 24},{wt + 8} L{SCX - 24},{wt + 8} Z", fill=INK, stroke=INK, w=1.6, op=0.62))
    for k in range(1, 4):
        o.append(path(f"M{SCX - 24 + k * 12},{ly - 30} L{SCX - 24 + k * 12},{wt + 8}", stroke="#cfc6b6", w=1.4, op=0.8))
    for k in range(1, 3):
        o.append(path(f"M{SCX - 24},{wt + 8 + k * 20} L{SCX + 24},{wt + 8 + k * 20}", stroke="#cfc6b6", w=1.2, op=0.7))
    for px in (sx0 + 4, sx1 - 4):
        o.append(path(f"M{px},{ly - 28} L{px},{wt}", stroke="#6b5a45", w=6))
    rt = wt - 58
    o.append(path(f"M{sx0 - 40},{wt + 6} Q{sx0 - 24},{wt + 2} {sx0 - 10},{wt - 10} L{SCX - 26},{rt} L{SCX + 26},{rt} L{sx1 + 10},{wt - 10} Q{sx1 + 24},{wt + 2} {sx1 + 40},{wt + 6} "
                  f"Q{SCX},{wt - 6} {sx0 - 40},{wt + 6} Z", fill="#6e6a63", stroke=INK, w=2.6, op=0.95, filt="brush"))
    o.append(path(f"M{SCX - 26},{rt} L{SCX + 26},{rt}", stroke=INK, w=5))
    o.append(path(f"M{SCX - 16},{rt - 14} L{SCX + 6},{rt + 1} M{SCX + 16},{rt - 14} L{SCX - 6},{rt + 1}", w=2.4))
    for k in range(1, 6):  # roof tiles
        t = k / 6
        o.append(path(f"M{f(SCX - 26 + (sx0 - 10 - SCX + 26) * t)},{f(rt + (wt - 10 - rt) * t)} L{f(SCX + 26 + (sx1 + 10 - SCX - 26) * t)},{f(rt + (wt - 10 - rt) * t)}", stroke=PALE, w=1.1, op=0.45))
    o.append(ground(base + 40, SX0, SX1, op=0.2))
    fig, a = ordinary(SCX - 70, base + 64, 2.6, flip=False)
    o.append(fig)
    for hx_, hy_ in [(SX0 + 100, base + 70), (SCX + 90, base + 100), (SX1 - 90, base + 60)]:
        for _ in range(4):
            lx, ly2 = hx_ + rng.gauss(0, 14), hy_ + rng.gauss(0, 5)
            sz = rng.uniform(5, 8)
            o.append(f'<path d="M{f(lx)},{f(ly2)} l{f(sz)},{f(-sz * 0.4)} l{f(-sz * 0.3)},{f(sz)} z" fill="{rng.choice([GREY, PALE, INK])}" opacity="{rng.uniform(0.5, 0.85):.2f}"/>')
    for k in range(3):  # a few leaves on the treads
        yy = y0 - (k + 1) * (rise + depth) + 8
        lx = SCX + rng.uniform(-90, 90)
        o.append(f'<path d="M{f(lx)},{f(yy)} l7,-3 l-2,7 z" fill="{GREY}" opacity="0.7"/>')
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 140, base + 175, 12, 6, 14))
    return finish(o + [zen_rank_close()])

CARDS = {"vo01": vo01, "vo02": vo02, "vo03": vo03, "vo04": vo04, "vo05": vo05,
         "vo06": vo06, "vo07": vo07, "vo08": vo08, "vo09": vo09, "vo10": vo10,
         "vo11": vo11, "vo12": vo12, "vo13": vo13, "vo14": vo14, "vo15": vo15}
