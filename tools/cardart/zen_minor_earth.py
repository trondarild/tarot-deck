"""Zen deck, minor series, suit of Earth (ea01-ea15): the body, sitting and daily work.

Pips ea01-ea10 follow the hybrid design: zen_pip_open("earth", n) draws the ensō with n gorintō
cubes, then one small vignette of the pip's Image paragraph is drawn in the lower inside of the
ensō (ZEN_VIGNETTE), then zen_pip_close(). The vignette is one object or figure with a little
ground, and draws no square shapes, so the cube count stays readable.

Ranks ea11-ea15 use the hanging-scroll frame with a fuller scene. Each rank has a figure type that
the other suits can repeat with their own scene and props:

    withdrawn()   First Rank   a seated figure, eyes closed, wrapped in a robe: still
    attending()   Second Rank  a figure leaning toward a small particular held in the hands
    acting()      Third Rank   a standing figure reaching out to work, one hand striking
    engaged()     Fourth Rank  a seated figure turned toward someone else, hand raised
    ordinary()    Fifth Rank   a stooped, plainly dressed figure at a chore

Each figure helper takes (x, y, s, flip, ...): x, y is the ground under the feet or seat, s scales
a figure about 100 units high, and flip mirrors it (figures face +x). It returns (svg, anchors);
anchors holds the hand points in page coordinates, so a caller can hang props on them.
"""

import math

from .common import (ENSO_CX, GREY, INK, PALE, SCROLL_BOX, VERMILION, ZEN_PAPER, ZEN_VIGNETTE,
                     f, zen_pip_close, zen_pip_open, zen_rank_close, zen_rank_open)
from .zen_transmission import GREYROBE, SKIN, ellipse, finish, head, path, tube
from .zen_way import grass, ground, herdsman, hills, mist, trunk

SX0, SY0, SX1, SY1 = SCROLL_BOX
SCX = (SX0 + SX1) / 2
VX0, VY0, VX1, VY1 = ZEN_VIGNETTE
VCX = (VX0 + VX1) / 2
FLOOR = 725          # ground line of the pip vignettes
WOOD, STRAW, CLAY = "#b9a68a", "#d6c7a1", "#a79e8f"


# ------------------------------------------------------------ figure helpers

def place(x, y, s, flip, inner):
    """Place local-unit drawing `inner` with its origin at (x, y), scaled by s, mirrored if flip.
    The whole-canvas brush filters used by finish() cannot sit inside a transformed group (their
    region is in local units), so inside the group the shared bounding-box filters are used."""
    inner = inner.replace("url(#brush)", "url(#fbrush)").replace("url(#dry)", "url(#fdry)")
    return f'<g transform="translate({f(x)},{f(y)}) scale({f(-s if flip else s)},{f(s)})">{inner}</g>'


def _anchor(x, y, s, flip, p):
    return (x + (-p[0] if flip else p[0]) * s, y + p[1] * s)


def _arm(sh, elbow, hand, robe=SKIN, w=5.0):
    """An arm as an inked tube from shoulder through elbow to hand, with a small hand."""
    d = f"M{f(sh[0])},{f(sh[1])} Q{f(elbow[0])},{f(elbow[1])} {f(hand[0])},{f(hand[1])}"
    return tube(d, w, robe) + ellipse(hand[0], hand[1], 3.4, 3.0, SKIN, stroke=INK, w=1.4)


def withdrawn(x, y, s=1.0, flip=False, robe=GREYROBE, view="front", eyes_closed=True):
    """First Rank figure: a cross-legged sitter, eyes closed, hands in the lap, robe drawn over the knees.
    view is "front", "side" (facing +x) or "back"; origin is the ground under the seat."""
    o = []
    if view == "side":
        o.append(path("M-50,-2 Q-40,-24 -6,-26 Q30,-26 48,-4 Q0,10 -50,-2 Z", fill=robe, stroke=INK, w=2.4, filt="brush"))
        o.append(tube("M-8,-20 Q-10,-40 -6,-60", 22, robe))
        o.append(_arm((-6, -56), (10, -38), (24, -22), robe))
        o.append(head(-1, -76, 12, look=1, bowed=eyes_closed, hair=False) +
                 (path("M5,-76 q3,2 6,0", w=1.4) if eyes_closed else ""))
    else:
        o.append(path("M-17,-60 Q-34,-28 -46,-3 Q0,10 46,-3 Q34,-28 17,-60 Q0,-67 -17,-60 Z",
                      fill=robe, stroke=INK, w=2.4, filt="brush"))
        o.append(path("M-46,-3 Q-30,-15 -12,-7 M46,-3 Q30,-15 12,-7", w=1.8))
        if view == "front":
            o.append(path("M-16,-58 Q-31,-34 -10,-17 M16,-58 Q31,-34 10,-17", stroke=INK, w=2.2))
            o.append(ellipse(0, -14, 11, 5, SKIN, stroke=INK, w=1.6))
        o.append(head(0, -75, 12, bowed=True))
        if view == "front":
            o.append(path("M-7,-74 q3,2.4 6,0 M2,-74 q3,2.4 6,0" if eyes_closed else "M-7,-75 h5 M2,-75 h5", w=1.4))
        elif view == "back":
            o.append(path("M-12,-78 Q0,-92 12,-78", w=3.5))
    return place(x, y, s, flip, "".join(o)), {"hands": [_anchor(x, y, s, flip, (0, -14))], "head": _anchor(x, y, s, flip, (0, -76))}


def attending(x, y, s=1.0, flip=False, seat=36, lean=22, reach=(50, -42), robe=GREYROBE, tied=True):
    """Second Rank figure: seated (seat > 26, on a stool) or kneeling (seat <= 26), the torso leaning
    forward and the head bowed over the hands, which hold at `reach` (local units) a small particular.
    The sleeves are tied back and the face is turned down, so the whole figure points at its hands."""
    hip = (-8, -seat)
    sh = (hip[0] + lean, hip[1] - 38)
    o = []
    if seat > 26:
        knee, foot = (hip[0] + 26, hip[1] + 1), (hip[0] + 24, 0)
        o.append(path(f"M{f(hip[0])},{f(hip[1])} L{f(knee[0])},{f(knee[1])} L{f(foot[0])},{f(foot[1])}", w=3.2))
        o.append(path(f"M{f(foot[0] - 3)},{f(foot[1])} h12", w=3))
        o.append(tube(f"M{f(hip[0])},{f(hip[1])} L{f(knee[0] - 4)},{f(knee[1])}", 15, robe))
    else:
        o.append(path(f"M{f(hip[0] - 22)},-2 Q{f(hip[0])},-14 {f(hip[0] + 30)},-3 Q{f(hip[0])},5 {f(hip[0] - 22)},-2 Z",
                      fill=robe, stroke=INK, w=2.2, filt="brush"))
    o.append(tube(f"M{f(hip[0])},{f(hip[1])} Q{f(hip[0] + lean * 0.2)},{f(hip[1] - 20)} {f(sh[0])},{f(sh[1])}", 22, robe))
    o.append(_arm(sh, (sh[0] + 14, sh[1] + 16), reach, SKIN))
    o.append(head(sh[0] + 10, sh[1] - 8, 11, bowed=True, hair=False))
    o.append(path(f"M{f(sh[0] + 2)},{f(sh[1] - 15)} q8,-6 16,0", w=3.2))
    return place(x, y, s, flip, "".join(o)), {"hands": [_anchor(x, y, s, flip, reach)]}


def acting(x, y, s=1.0, flip=False, reach=(46, -64), strike=True, robe=GREYROBE):
    """Third Rank figure: a standing worker leaning into the task, one hand steadying the work at
    `reach`, the other raised with a mallet (strike) or on the work too. Head turned to the joint,
    sleeves tied back, sash at the waist."""
    hip, sh = (-4, -50), (6, -86)
    o = []
    o.append(path("M-4,-50 L12,-26 L16,0 M-4,-50 L-18,-24 L-26,0", w=3.4))
    o.append(path("M13,0 h10 M-27,0 h-9", w=3))
    o.append(path("M-14,-84 L16,-82 L20,-34 L-24,-32 Z", fill=robe, stroke=INK, w=2.4, filt="brush"))
    o.append(path("M-22,-46 L18,-48", w=2.4, stroke=GREY))
    o.append(_arm(sh, (30, -80), reach, SKIN))
    hand2 = (24, -122) if strike else (36, -70)
    o.append(_arm((2, -84), (20, -108) if strike else (22, -76), hand2, SKIN))
    if strike:
        o.append(path("M24,-122 L32,-134", w=3.4, stroke=INK))
        o.append(path("M24,-136 L40,-130", w=7, stroke=INK))
    o.append(head(10, -100, 11, look=1, hair=False))
    o.append(path("M-1,-103 Q10,-114 21,-103", w=3.2))
    return place(x, y, s, flip, "".join(o)), {"hands": [_anchor(x, y, s, flip, reach), _anchor(x, y, s, flip, hand2)]}


def engaged(x, y, s=1.0, flip=False, robe=GREYROBE, hat=True, tool="hoe", seat="stump"):
    """Fourth Rank figure: seated, turned toward someone else, one hand raised open in greeting,
    the other resting on a tool (hoe, or None). Facing +x.
    seat="stump" draws a stump to sit on; seat="floor" kneels on the floor (seiza), for indoor scenes."""
    o = []
    if seat == "stump":
        o += [path("M-24,-30 L24,-30 L20,0 L-20,0 Z", fill="#cfc6b6", stroke=INK, w=2.2, filt="brush"),
              ellipse(0, -30, 24, 6, "#e4ded0", stroke=INK, w=1.8)]
    o.append(path("M-14,-32 L-18,-62 L8,-62 L12,-32 Z", fill=robe, stroke=INK, w=2.2))  # robe over the lap
    if seat == "stump":
        o.append(path("M-6,-34 L18,-26 L22,0 M-12,-34 L-4,-24 L-8,0", w=3.2))
    else:  # legs folded under: the robe spreads on the floor
        o.append(path("M-26,-30 Q-4,-42 22,-32 L26,-30 Q0,-24 -26,-30 Z", fill=robe, stroke=INK, w=2.2, filt="brush"))
    o.append(path("M-18,-92 Q0,-100 14,-90 L16,-36 L-18,-34 Z", fill=robe, stroke=INK, w=2.4, filt="brush"))
    if tool == "hoe":
        o.append(path("M-30,-4 L-34,-130 M-34,-130 l16,6", w=3.4, stroke="#6b5a45"))
        o.append(path("M-38,-132 l22,8 l-3,8 z", fill=INK, stroke=INK, w=1.5))
        o.append(_arm((-12, -86), (-30, -70), (-31, -62), SKIN))
    else:
        o.append(_arm((-12, -86), (-20, -62), (-8, -48), SKIN))
    o.append(_arm((12, -88), (36, -96), (38, -118), SKIN))  # raised hand
    o.append(head(2, -106, 11, look=1, hair=False, hat=hat, mouth="smile"))
    # kneeling sits the body about 30 units lower than sitting on the stump
    dy = 0 if seat == "stump" else 30
    inner = "".join(o) if dy == 0 else f'<g transform="translate(0,{dy})">{"".join(o)}</g>'
    return place(x, y, s, flip, inner), {"hands": [_anchor(x, y, s, flip, (38, -118 + dy))]}


def ordinary(x, y, s=1.0, flip=False, robe="#b8b2a6", tool="broom", hair="#8f8a82"):
    """Fifth Rank figure: a stooped, plainly dressed elder at a chore (broom, or None), head bowed
    under a kerchief. Nothing about the pose suggests practice. Facing +x."""
    o = []
    o.append(path("M-2,-44 L4,-22 L8,0 M-8,-44 L-12,-22 L-16,0", w=3.2))
    o.append(path("M5,0 h8 M-17,0 h-8", w=3))
    o.append(path("M-14,-70 Q-6,-80 14,-72 L20,-30 L-20,-24 Z", fill=robe, stroke=INK, w=2.4, filt="brush"))
    if tool == "broom":
        o.append(path("M48,-6 L20,-86", w=3, stroke="#6b5a45"))
        for k in range(9):
            o.append(path(f"M{f(47 + k * 2)},-6 l{f(-3 - k * 1.2)},{f(10 + (k % 3))}", w=1.6, stroke=GREY))
        o.append(path("M52,-8 l-12,-6 l-4,8 z", fill=STRAW, stroke=INK, w=1.4))
        o.append(_arm((6, -70), (24, -62), (30, -58), SKIN, 4.5))
        o.append(_arm((4, -66), (12, -48), (24, -34), SKIN, 4.5))
    o.append(head(16, -78, 10, look=1, hair=False, bowed=True))
    o.append(path("M6,-80 Q16,-94 27,-80 Q16,-84 6,-80 Z", fill=hair, stroke=INK, w=1.4))
    o.append(ellipse(5, -86, 5, 4, hair, stroke=INK, w=1.2))  # bun
    return place(x, y, s, flip, "".join(o)), {"hands": [_anchor(x, y, s, flip, (30, -58))]}


# ------------------------------------------------------------ small objects

def cushion(x, y, w, dent=0.0, col=INK, op=1.0):
    """A round zafu seen from the side, resting on the ground at y; dent > 0 hollows the top."""
    h = w * 0.36
    d = (f"M{f(x - w / 2)},{f(y)} C{f(x - w / 2)},{f(y - h * 1.1)} {f(x - w * 0.3)},{f(y - h)} {f(x)},{f(y - h)} "
         f"C{f(x + w * 0.3)},{f(y - h)} {f(x + w / 2)},{f(y - h * 1.1)} {f(x + w / 2)},{f(y)} Q{f(x)},{f(y + h * 0.28)} {f(x - w / 2)},{f(y)} Z")
    out = [path(d, fill=col, stroke=INK, w=2.4, op=op, filt="brush")]
    if dent:
        out.append(ellipse(x, y - h * 0.92, w * 0.26, h * 0.2, INK, op=0.75, filt="wash"))
        out.append(path(f"M{f(x - w * 0.24)},{f(y - h * 0.9)} Q{f(x)},{f(y - h * 0.62)} {f(x + w * 0.24)},{f(y - h * 0.9)}", stroke=PALE, w=1.6, op=0.8))
    out.append(path(f"M{f(x - w * 0.4)},{f(y - h * 0.3)} Q{f(x)},{f(y - h * 0.05)} {f(x + w * 0.4)},{f(y - h * 0.3)}", stroke=PALE, w=1.3, op=0.7))
    return "".join(out)


def bowl(x, y, w, col="#e4ded0", rim=INK, steam=False):
    """A small bowl on a foot, rim at y."""
    h = w * 0.45
    out = [path(f"M{f(x - w / 2)},{f(y)} Q{f(x - w * 0.42)},{f(y + h)} {f(x)},{f(y + h)} Q{f(x + w * 0.42)},{f(y + h)} {f(x + w / 2)},{f(y)} Z",
                fill=col, stroke=INK, w=2.2, filt="brush"),
           ellipse(x, y, w / 2, w * 0.1, "#d4cbb8", stroke=rim, w=1.8),
           path(f"M{f(x - w * 0.15)},{f(y + h)} l-2,4 h{f(w * 0.3 + 4)} l-2,-4", w=1.6)]
    if steam:
        out.append(path(f"M{f(x - 4)},{f(y - 8)} q-6,-10 0,-18 q6,-8 0,-16", stroke=PALE, w=1.4, op=0.8))
    return "".join(out)


def floorboards(y0, y1, x0=VX0, x1=VX1, rows=4, col=WOOD):
    """A wooden floor seen at a shallow angle: pale wash with plank lines running away from the viewer."""
    out = [path(f"M{x0},{y0} L{x1},{y0} L{x1 + 30},{y1} L{x0 - 30},{y1} Z", fill=col, stroke=None, op=0.28, filt="softwash")]
    for k in range(rows + 1):
        t = k / rows
        xt, xb = x0 + (x1 - x0) * t, x0 - 30 + (x1 - x0 + 60) * t
        out.append(path(f"M{f(xt)},{f(y0)} L{f(xb)},{f(y1)}", stroke=GREY, w=1.1, op=0.4))
    out.append(path(f"M{x0},{y0} Q{f((x0 + x1) / 2)},{y0 - 5} {x1},{y0}", stroke=GREY, w=1.6, op=0.6, filt="brush"))
    return "".join(out)


def _sandals(x, y, s=1.0, flip=False):
    d = -1 if flip else 1
    out = []
    for k, dx in enumerate((0, 22)):
        px = x + dx * d * s
        out.append(path(f"M{f(px)},{f(y)} q{f(2 * d)},{f(-17 * s)} {f(13 * d * s)},{f(-18 * s)} q{f(2 * d)},{f(16 * s)} {f(-13 * d * s)},{f(18 * s)} Z",
                        fill=STRAW, stroke=INK, w=1.8))
        out.append(path(f"M{f(px + 2 * d * s)},{f(y - 12 * s)} l{f(7 * d * s)},{f(-2 * s)}", w=1.4, stroke=GREY))
    return "".join(out)


def _pine_crown(rng, x, y, w, layers=3):
    """Dry-brush pine pads with needle fringes; (x, y) is the top of the trunk."""
    out = []
    for k in range(layers):
        px, py, pw = x + (k % 2 * 2 - 1) * 12 * (k > 0), y + k * 34, w - k * 6
        out.append(ellipse(px, py, pw, 17, INK, op=0.85, filt="dry"))
        for _ in range(26):
            nx = px + rng.uniform(-pw, pw)
            out.append(path(f"M{f(nx)},{f(py + 6)} l{rng.uniform(-6, 6):.1f},{rng.uniform(10, 20):.1f}", stroke=GREY, w=1, op=0.7))
    return "".join(out)


def _smoke(x, y, h, sway=8, col=PALE, w=1.6):
    return path(f"M{f(x)},{f(y)} C{f(x + sway)},{f(y - h * 0.3)} {f(x - sway)},{f(y - h * 0.6)} {f(x + sway * 0.5)},{f(y - h)}", stroke=col, w=w, op=0.85)


def _wipe_streaks(x0, x1, y, n, rng):
    return "".join(path(f"M{f(x0)},{f(y + k * 7)} Q{f((x0 + x1) / 2)},{f(y + k * 7 - 4)} {f(x1 + rng.uniform(-10, 10))},{f(y + k * 7 + 1)}",
                        stroke=PALE, w=1.6, op=0.9) for k in range(n))


# ------------------------------------------------------------ pips ea01-ea10

def ea01(rng):
    """One of Earth: a round black cushion on a bare floor, straw sandals at the threshold."""
    o = [zen_pip_open("earth", 1), floorboards(FLOOR - 30, FLOOR + 40, VCX - 170, VCX + 170),
         cushion(VCX + 30, FLOOR + 8, 230),
         _sandals(VCX - 170, FLOOR + 40, 1.9)]
    o.append(path(f"M{VCX - 190},{FLOOR - 30} q{rng.uniform(-4, 4):.1f},-70 -2,-110", stroke=INK, w=3.5, op=0.6, filt="brush"))  # door post
    o.append(grass(rng, VX0, VX0 + 40, FLOOR - 36, FLOOR - 26, 8, 14, 30))
    return finish(o + [zen_pip_close()])


def ea02(rng):
    """Two of Earth: a worn cushion with a deep hollow, an open manual with crossed legs drawn on it."""
    o = [zen_pip_open("earth", 2), floorboards(FLOOR - 24, FLOOR + 44, VCX - 190, VCX + 190)]
    o.append(cushion(VCX - 85, FLOOR + 10, 190, dent=1.0, col="#6e6a63"))
    bx, by = VCX + 105, FLOOR + 20
    # open book: two pages as parallelograms, a gutter, and a crossed-leg drawing on the left page
    o.append(path(f"M{bx - 88},{by - 20} L{bx - 4},{by - 30} L{bx - 4},{by + 38} L{bx - 94},{by + 44} Z", fill="#ebe4d3", stroke=INK, w=2.2, filt="brush"))
    o.append(path(f"M{bx + 4},{by - 30} L{bx + 88},{by - 20} L{bx + 92},{by + 44} L{bx + 4},{by + 38} Z", fill="#ebe4d3", stroke=INK, w=2.2, filt="brush"))
    for k in range(4):
        o.append(path(f"M{bx + 14},{by - 14 + k * 12} L{bx + 76},{by - 8 + k * 12}", stroke=GREY, w=1.2, op=0.7))
    fx, fy = bx - 48, by + 20
    o.append(path(f"M{fx - 22},{fy} Q{fx},{fy - 7} {fx + 22},{fy} Q{fx},{fy + 8} {fx - 22},{fy} Z M{fx},{fy - 4} L{fx},{fy - 26} M{fx},{fy - 26} m-3,-5 a5,5 0 1 0 6,0 a5,5 0 1 0 -6,0", w=1.8, stroke=INK))
    return finish(o + [zen_pip_close()])


def ea03(rng):
    """Three of Earth: a figure seated in profile at dusk, shoulders level, hands in the lap, a slant of last light on the knees."""
    o = [zen_pip_open("earth", 3), ground(FLOOR, VX0 + 20, VX1 - 20, op=0.16)]
    o.append(ellipse(VCX - 90, FLOOR + 12, 190, 16, GREY, op=0.28, filt="wash"))  # long shadow: low light from the right
    fig, _ = withdrawn(VCX + 20, FLOOR - 2, 2.5, flip=False, view="side", eyes_closed=False)
    o.append(fig)
    o.append(path(f"M{VCX + 20},{FLOOR - 50} Q{VCX + 60},{FLOOR - 62} {VCX + 110},{FLOOR - 40}", stroke="#fff8e4", w=9, op=0.9, filt="wash"))  # last light on the knees
    return finish(o + [zen_pip_close()])


def ea04(rng):
    """Four of Earth: a man seated before dawn, breath visible, an incense stick half burned (the one ember), a lantern at the door."""
    o = [zen_pip_open("earth", 4), floorboards(FLOOR - 24, FLOOR + 44, VCX - 190, VCX + 190, col="#9a907f")]
    fig, a = withdrawn(VCX + 40, FLOOR - 2, 2.3, flip=False, view="side", eyes_closed=True)
    o.append(fig)
    hx, hy = VCX + 40 + 14 * 2.3, FLOOR - 2 - 76 * 2.3
    for k in range(3):
        o.append(path(f"M{f(hx + 22 + k * 11)},{f(hy + 10 - k * 3)} q6,-4 12,0", stroke=PALE, w=1.5, op=0.9 - k * 0.2))
    o.append(path(f"M{VCX - 60},{FLOOR - 4} l2,-70", stroke=INK, w=3.6))
    o.append(path(f"M{VCX - 58},{FLOOR - 74} l1,-36", stroke=GREY, w=3.2, op=0.6))
    o.append(f'<circle cx="{VCX - 57}" cy="{FLOOR - 76}" r="3.4" fill="{VERMILION}"/>')
    o.append(_smoke(VCX - 57, FLOOR - 82, 100))
    o.append(ellipse(VCX - 59, FLOOR - 2, 22, 5, GREY, op=0.6))
    lx = VX0 + 40  # lantern: a paper ellipse on a cord
    o.append(path(f"M{lx},{FLOOR - 270} Q{lx + 3},{FLOOR - 230} {lx},{FLOOR - 190}", stroke=INK, w=2.4))
    o.append(ellipse(lx, FLOOR - 160, 26, 36, "#efe7cf", stroke=INK, w=2.4, filt="brush"))
    o.append(path(f"M{lx - 24},{FLOOR - 170} Q{lx},{FLOOR - 160} {lx + 24},{FLOOR - 170} M{lx - 22},{FLOOR - 148} Q{lx},{FLOOR - 138} {lx + 22},{FLOOR - 148}", stroke=GREY, w=1.4))
    return finish(o + [zen_pip_close()])


def ea05(rng):
    """Five of Earth: a monk kneeling to wipe the boards in long strokes beside a bucket, wet grain showing."""
    o = [zen_pip_open("earth", 5), floorboards(FLOOR - 40, FLOOR + 50, VCX - 190, VCX + 190, rows=5)]
    o.append(_wipe_streaks(VCX - 130, VCX + 90, FLOOR - 4, 3, rng))
    fig, a = attending(VCX - 50, FLOOR + 6, 2.2, flip=False, seat=18, lean=34, reach=(46, -2), robe=GREYROBE)
    o.append(fig)
    bx, by = VCX + 130, FLOOR + 6
    o.append(path(f"M{bx - 36},{by - 62} L{bx + 36},{by - 62} L{bx + 28},{by} L{bx - 28},{by} Z", fill="#a79e8f", stroke=INK, w=2.4, filt="brush"))
    o.append(ellipse(bx, by - 62, 36, 7, "#cfc9bc", stroke=INK, w=2))
    o.append(path(f"M{bx - 36},{by - 62} Q{bx},{by - 118} {bx + 36},{by - 62}", stroke=INK, w=2))
    o.append(path(f"M{bx - 20},{by - 20} h40 M{bx - 22},{by - 40} h44", stroke=GREY, w=1.4, op=0.7))
    return finish(o + [zen_pip_close()])


def ea06(rng):
    """Six of Earth: a monk under a pine in the evening, eyes half open, a flute across his lap (the one accent)."""
    o = [zen_pip_open("earth", 6), ground(FLOOR, VX0 + 20, VX1 - 20, op=0.16)]
    px = VCX + 140
    o.append(path(f"M{px},{FLOOR + 6} C{px - 10},{FLOOR - 60} {px + 10},{FLOOR - 110} {px - 4},{FLOOR - 165}", stroke=INK, w=16, filt="dry"))
    o.append(_pine_crown(rng, px - 10, FLOOR - 168, 78, 2))
    fig, _ = withdrawn(VCX - 20, FLOOR - 2, 2.3, flip=False, view="front", eyes_closed=False)
    o.append(fig)
    o.append(path(f"M{VCX - 100},{FLOOR - 50} L{VCX + 60},{FLOOR - 40}", stroke=VERMILION, w=6))
    o.append(grass(rng, VX0 + 20, VX1 - 20, FLOOR - 4, FLOOR + 40, 40, 10, 34))
    return finish(o + [zen_pip_close()])


def ea07(rng):
    """Seven of Earth: a man seen from behind on a veranda, sipping from a bowl; a rope coil hangs unused on a nail (the one accent)."""
    o = [zen_pip_open("earth", 7)]
    o.append(path(f"M{VX0 + 10},{FLOOR - 4} Q{VCX},{FLOOR - 10} {VX1 - 10},{FLOOR - 4} L{VX1 - 10},{FLOOR + 14} L{VX0 + 10},{FLOOR + 14} Z", fill=WOOD, stroke=INK, w=2.2, op=0.5, filt="brush"))
    px = VCX - 130
    o.append(path(f"M{px},{FLOOR - 4} Q{px + 5},{FLOOR - 120} {px},{FLOOR - 230}", stroke=INK, w=10, filt="dry"))
    o.append(path(f"M{px + 5},{FLOOR - 196} l16,-3", stroke=INK, w=3))
    for k in range(3):
        o.append(f'<ellipse cx="{px + 24}" cy="{FLOOR - 176 + k * 5}" rx="{15 - k * 2}" ry="{9 - k}" fill="none" stroke="{VERMILION}" stroke-width="2.4"/>')
    fig, _ = withdrawn(VCX + 50, FLOOR - 6, 2.3, flip=False, view="back")
    o.append(fig)
    bx, by = VCX + 50 + 40, FLOOR - 6 - 190
    arm = f"M{VCX + 50 + 16},{FLOOR - 6 - 135} Q{bx + 4},{by + 60} {bx - 6},{by + 8}"
    o.append(path(arm, stroke=INK, w=11))
    o.append(path(arm, stroke=GREYROBE, w=8))
    o.append(bowl(bx, by, 32, steam=True))
    return finish(o + [zen_pip_close()])


def ea08(rng):
    """Eight of Earth: an empty hall, one undented cushion at the centre of a wide circle of pale light on the floor. No figure."""
    o = [zen_pip_open("earth", 8), floorboards(FLOOR - 70, FLOOR + 50, VCX - 190, VCX + 190, rows=6, col="#a79e8f")]
    o.append(ellipse(VCX, FLOOR - 4, 175, 46, "#f9f3e0", op=0.95, filt="wash"))
    o.append(ellipse(VCX, FLOOR - 4, 168, 40, "none", stroke=PALE, w=1.6, op=0.7, filt="brush"))
    o.append(cushion(VCX, FLOOR + 2, 120, col="#6e6a63"))
    return finish(o + [zen_pip_close()])


def ea09(rng):
    """Nine of Earth: a bell-topped window onto a river and a red maple bough, a bowl on the sill, a broom against the wall. No person."""
    o = [zen_pip_open("earth", 9)]
    wx, wy0, wy1, ww = VCX - 40, FLOOR - 250, FLOOR - 50, 74
    frame = (f"M{wx - ww},{wy1} L{wx - ww},{wy0 + 70} C{wx - ww},{wy0 + 20} {wx - 30},{wy0 + 20} {wx},{wy0} "
             f"C{wx + 30},{wy0 + 20} {wx + ww},{wy0 + 20} {wx + ww},{wy0 + 70} L{wx + ww},{wy1} Z")
    o.append(path(frame, fill="#e9e3d6", stroke=INK, w=3.4, filt="brush"))
    o.append(path(f"M{wx - ww + 6},{wy1 - 70} C{wx - 30},{wy1 - 96} {wx + 30},{wy1 - 60} {wx + ww - 6},{wy1 - 84}", stroke="#cfc9bc", w=22, op=0.8, filt="softwash"))
    o.append(path(f"M{wx + ww},{wy0 + 90} C{wx + 30},{wy0 + 96} {wx - 10},{wy0 + 120} {wx - 40},{wy0 + 150}", stroke=INK, w=4, filt="brush"))
    for _ in range(9):
        lx, ly = wx + rng.uniform(-30, ww - 10), wy0 + rng.uniform(96, 160)
        o.append(f'<path d="M{f(lx)},{f(ly)} l9,-3 l-3,9 z" fill="{VERMILION}" opacity="0.85" transform="rotate({rng.uniform(0, 360):.0f} {f(lx)} {f(ly)})"/>')
    o.append(path(f"M{wx - ww - 16},{wy1} Q{wx},{wy1 - 4} {wx + ww + 16},{wy1} L{wx + ww + 16},{wy1 + 10} L{wx - ww - 16},{wy1 + 10} Z", fill=WOOD, stroke=INK, w=2.4, op=0.8))
    o.append(bowl(wx - 30, wy1 - 18, 40))
    o.append(path(f"M{VX0 + 10},{FLOOR + 14} Q{VCX},{FLOOR + 8} {VX1 - 10},{FLOOR + 14}", stroke=GREY, w=1.8, op=0.6, filt="brush"))
    # broom leaning on the wall to the right of the window
    bx = wx + ww + 70
    o.append(path(f"M{bx},{FLOOR - 150} L{bx - 36},{FLOOR + 10}", stroke="#6b5a45", w=4))
    for k in range(10):
        o.append(path(f"M{f(bx - 36 + k * 1.8 - 9)},{FLOOR + 10} l{f(-7 + k * 0.5)},{f(-26 - (k % 3) * 3)}", stroke=GREY, w=1.8))
    o.append(path(f"M{bx - 44},{FLOOR - 16} q12,-6 22,2", stroke=INK, w=3))
    return finish(o + [zen_pip_close()])


def ea10(rng):
    """Ten of Earth: a barefoot cook with sleeves tied back, handing out a bowl of rice; a basket of radishes (the one accent) at his feet."""
    o = [zen_pip_open("earth", 10), ground(FLOOR, VX0 + 20, VX1 - 20, op=0.16)]
    fig, a = acting(VCX - 60, FLOOR - 2, 2.1, flip=False, strike=False, reach=(50, -66), robe=SKIN)
    o.append(fig)
    hx, hy = a["hands"][0]
    o.append(bowl(hx + 6, hy - 4, 34, steam=True))
    bx, by = VCX + 120, FLOOR + 20
    o.append(path(f"M{bx - 44},{by - 34} Q{bx},{by - 50} {bx + 44},{by - 34} L{bx + 34},{by + 14} Q{bx},{by + 24} {bx - 34},{by + 14} Z", fill=STRAW, stroke=INK, w=2.2, filt="brush"))
    for k in range(5):
        rx = bx - 30 + k * 15
        o.append(f'<ellipse cx="{rx}" cy="{by - 42 + (k % 2) * 4}" rx="7.5" ry="9" fill="{VERMILION}" opacity="0.9" stroke="{INK}" stroke-width="1.2"/>')
        o.append(path(f"M{rx},{by - 50} q{rng.uniform(-4, 4):.0f},-8 {rng.uniform(-5, 5):.0f},-14", stroke=GREY, w=2))
    o.append(grass(rng, VX0 + 20, VX1 - 20, FLOOR - 2, FLOOR + 40, 40, 8, 26))
    return finish(o + [zen_pip_close()])


# ------------------------------------------------------------ ranks ea11-ea15

def _scroll_haze(rng, y=330):
    """Soft mountain wash and mist in the upper part of a scroll, leaving most of the paper bare."""
    return hills(rng, [(y + 40, 60, PALE, 0.22, 90)], SX0 + 4, SX1 - 4) + mist(SCX, y + 50, 240, 24, 0.7)


def ea11(rng):
    """First Rank of Earth: a recluse seated in a mountain hollow, eyes closed, moss over his knees; rock and sitter share one outline."""
    o = [zen_rank_open("earth", 1)]
    base = SY1 - 120
    ridge = [(SX0, 560), (150, 500), (200, 440), (232, 410), (262, 350), (300, 318), (322, 282), (350, 262), (374, 296), (410, 330), (440, 392), (480, 430), (520, 486), (SX1, 520)]
    peak = ridge + [(SX1, base + 40), (SX0, base + 40)]
    mass = "M" + " L".join(f"{a},{b}" for a, b in peak) + " Z"
    o.append(path(mass, fill="#a39d90", stroke=None, op=0.5))
    o.append(path("M" + " L".join(f"{a},{b}" for a, b in ridge), stroke=INK, w=3, op=0.75, filt="brush"))
    for _ in range(26):
        x, y = rng.uniform(SX0 + 20, SX1 - 20), rng.uniform(420, base - 20)
        o.append(path(f"M{f(x)},{f(y)} l{rng.uniform(-10, 10):.0f},{rng.uniform(20, 56):.0f}", stroke=GREY, w=rng.uniform(1.2, 3), op=rng.uniform(0.25, 0.5), filt="dry"))
    hollow = f"M{SCX - 130},{base + 40} C{SCX - 140},{base - 200} {SCX - 60},{base - 270} {SCX},{base - 270} C{SCX + 60},{base - 270} {SCX + 140},{base - 200} {SCX + 130},{base + 40} Z"
    o.append(path(hollow, fill="#6e6a63", stroke=INK, w=3, op=0.85, filt="brush"))
    fig, a = withdrawn(SCX, base + 2, 1.9, flip=False, view="front", robe="#b3ad9f")
    o.append(fig)
    for _ in range(46):  # moss on the knees and the rock
        mx = SCX + rng.gauss(0, 40)
        my = base - rng.uniform(0, 26)
        o.append(f'<circle cx="{f(mx)}" cy="{f(my)}" r="{rng.uniform(1.2, 3.2):.1f}" fill="{GREY}" opacity="{rng.uniform(0.45, 0.85):.2f}"/>')
    for _ in range(30):
        mx, my = rng.uniform(SX0 + 30, SX1 - 30), rng.uniform(560, base)
        o.append(f'<circle cx="{f(mx)}" cy="{f(my)}" r="{rng.uniform(1, 2.6):.1f}" fill="{GREY}" opacity="0.5"/>')
    o.append(ground(base + 38, SX0, SX1, op=0.2))
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 50, base + 110, 40, 8, 22))
    o.append(mist(SCX, 560, 250, 20, 0.6))
    return finish(o + [zen_rank_close()])


def ea12(rng):
    """Second Rank of Earth: a potter at the wheel, hands wet with clay, looking at one bowl; shelves of pieces behind, each a little different."""
    o = [zen_rank_open("earth", 2)]
    base = SY1 - 130
    wy = base - 330
    # back wall, shelves with varied bowls
    o.append(path(f"M{SX0},{wy - 70} L{SX1},{wy - 70} L{SX1},{base + 20} L{SX0},{base + 20} Z", fill="#e4ded0", stroke=None, op=0.45, filt="softwash"))
    for k, sy in enumerate((wy - 10, wy + 110)):
        o.append(path(f"M{SX0 + 20},{sy} Q{SCX},{sy - 4} {SX1 - 20},{sy + 2}", stroke=INK, w=3, op=0.8, filt="brush"))
        x = SX0 + 40
        while x < SX1 - 50:
            w = rng.uniform(28, 52)
            h = rng.uniform(18, 40)
            kind = rng.choice(["bowl", "jar", "cup"])
            if kind == "bowl":
                d = f"M{f(x)},{f(sy - h * 0.7)} Q{f(x + w * 0.1)},{f(sy)} {f(x + w / 2)},{f(sy)} Q{f(x + w * 0.9)},{f(sy)} {f(x + w)},{f(sy - h * 0.7)} Z"
            elif kind == "jar":
                d = f"M{f(x + w * 0.3)},{f(sy - h * 1.5)} Q{f(x - w * 0.1)},{f(sy - h * 0.5)} {f(x + w * 0.2)},{f(sy)} L{f(x + w * 0.8)},{f(sy)} Q{f(x + w * 1.1)},{f(sy - h * 0.5)} {f(x + w * 0.7)},{f(sy - h * 1.5)} Z"
            else:
                d = f"M{f(x + w * 0.15)},{f(sy - h)} L{f(x + w * 0.25)},{f(sy)} L{f(x + w * 0.75)},{f(sy)} L{f(x + w * 0.85)},{f(sy - h)} Z"
            o.append(path(d, fill=rng.choice(["#cfc6b6", "#bdb4a3", "#dcd5c4"]), stroke=INK, w=1.8, op=0.9, filt="brush"))
            x += w + rng.uniform(14, 30)
    # the wheel: a low table and a spinning disc
    wx = SCX + 30
    o.append(path(f"M{wx - 70},{base - 78} L{wx + 70},{base - 78} L{wx + 56},{base + 6} L{wx - 56},{base + 6} Z", fill="#b9a68a", stroke=INK, w=2.6, op=0.85, filt="brush"))
    o.append(ellipse(wx, base - 78, 78, 16, "#a79e8f", stroke=INK, w=2.4))
    fig, a = attending(wx - 140, base + 4, 2.3, flip=False, seat=44, lean=18, reach=(60, -56), robe=GREYROBE)
    o.append(fig)
    hx, hy = a["hands"][0]
    o.append(path(f"M{wx - 30},{base - 84} Q{wx - 34},{base - 128} {wx},{base - 130} Q{wx + 34},{base - 128} {wx + 30},{base - 84} Z", fill="#c9bfa9", stroke=INK, w=2.6, filt="brush"))
    o.append(path(f"M{wx - 28},{base - 112} Q{wx},{base - 104} {wx + 28},{base - 112}", stroke=VERMILION, w=3.2))
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 10, base + 60, 14, 6, 16))
    o.append(path(f"M{SX0},{base + 8} Q{SCX},{base + 2} {SX1},{base + 10}", stroke=GREY, w=1.6, op=0.6, filt="brush"))
    return finish(o + [zen_rank_close()])


def ea13(rng):
    """Third Rank of Earth: a builder on a half-finished roof, mallet raised, fitting a beam; scaffold and tools in order, villagers below hold the ropes."""
    o = [zen_rank_open("earth", 3)]
    base = SY1 - 130
    top = base - 360
    # frame of the building: two posts and a half-laid roof
    for px in (SX0 + 90, SX1 - 90):
        o.append(path(f"M{px},{base} Q{px + 4},{(base + top) / 2} {px},{top + 70}", stroke=INK, w=10, filt="dry"))
    o.append(path(f"M{SX0 + 60},{top + 70} L{SCX},{top - 10} L{SX1 - 60},{top + 70}", stroke=INK, w=8, filt="brush"))
    o.append(path(f"M{SX0 + 90},{top + 100} L{SX1 - 90},{top + 100}", stroke=INK, w=6, filt="brush"))
    for k in range(6):  # rafters, left half only
        x = SX0 + 70 + k * 36
        o.append(path(f"M{x},{top + 70 - (x - SX0 - 60) * 0.35 + 6} L{x + 6},{top + 104}", stroke=GREY, w=3, op=0.8))
    # scaffold on the right
    for px in (SX1 - 40, SX1 - 120):
        o.append(path(f"M{px},{base} Q{px + 3},{base - 100} {px},{base - 210}", stroke="#6b5a45", w=6))
    for yy in (base - 60, base - 130, base - 205):
        o.append(path(f"M{SX1 - 130},{yy} Q{SX1 - 80},{yy - 3} {SX1 - 30},{yy}", stroke="#6b5a45", w=5))
    # builder on the cross-beam, steadying the new beam
    by = top + 100
    fig, a = acting(SCX - 80, by, 1.9, flip=False, reach=(48, -62), strike=True)
    o.append(fig)
    h1 = a["hands"][0]
    o.append(path(f"M{f(h1[0] - 50)},{f(h1[1] + 8)} L{f(h1[0] + 130)},{f(h1[1] - 14)}", stroke="#6b5a45", w=10, filt="brush"))
    o.append(path(f"M{SCX - 40},{by - 8} L{SCX + 40},{by - 4}", stroke=GREY, w=4, op=0.5))
    # tools laid in order on the ground at left, villagers at the ropes below
    for k in range(4):
        tx = SX0 + 50 + k * 22
        o.append(path(f"M{tx},{base + 30} L{tx + 4},{base + 80}", stroke=INK if k % 2 else GREY, w=3))
    o.append(ground(base + 20, SX0, SX1, op=0.2))
    for k, vx in enumerate((SCX - 70, SCX + 20)):
        vf, va = ordinary(vx, base + 60, 1.4, flip=False, tool=None, robe=rng.choice(["#b8b2a6", "#c9c4ba"]))
        o.append(vf)
        o.append(path(f"M{vx + 20},{base - 20} L{vx + 30},{base + 6}", stroke=INK, w=2))
    o.append(path(f"M{SCX + 32},{base + 30} Q{SCX + 90},{(by + base) / 2} {f(h1[0] + 126)},{f(h1[1] - 14)}", stroke=VERMILION, w=3))
    o.append(path(f"M{SCX - 42},{base + 30} Q{SCX - 20},{(by + base) / 2} {SCX - 28},{by - 2}", stroke=GREY, w=2.4))
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 70, base + 110, 30, 8, 22))
    return finish(o + [zen_rank_close()])


def ea14(rng):
    """Fourth Rank of Earth: a farmer with a hoe, sitting on a stump at the field's edge at dusk, raising a hand to a neighbour; crop rows run to the horizon."""
    o = [zen_rank_open("earth", 4)]
    base = SY1 - 160
    hor = base - 330
    o.append(ellipse(SCX - 60, hor - 60, 56, 56, "#e6dfd0", op=0.7, filt="wash"))  # low sun
    o.append(hills(rng, [(hor + 10, 40, PALE, 0.25, 80)], SX0 + 4, SX1 - 4))
    o.append(path(f"M{SX0},{hor + 8} Q{SCX},{hor + 2} {SX1},{hor + 10}", stroke=GREY, w=1.5, op=0.6, filt="brush"))
    # converging crop rows
    vp = (SCX - 20, hor + 8)
    for k in range(-5, 7):
        bx = SCX - 20 + k * 90
        o.append(path(f"M{vp[0]},{vp[1]} L{f(bx)},{base + 80}", stroke=GREY, w=1.6, op=0.55))
        for j in range(1, 7):
            t = (j / 7) ** 1.6
            px, py = vp[0] + (bx - vp[0]) * t, vp[1] + (base + 80 - vp[1]) * t
            o.append(path(f"M{f(px)},{f(py)} l{rng.uniform(-3, 3):.1f},{f(-6 - 12 * t)}", stroke=INK, w=1.2 + t, op=0.6))
    o.append(path(f"M{SCX - 90},{hor + 8} Q{SCX - 40},{base - 80} {SCX + 20},{base + 90}", stroke="#cfc6b6", w=30, op=0.5, filt="softwash"))
    # a neighbour coming up the path, small
    nb, _ = herdsman(SCX - 110, hor + 170, 1.0, "walk")
    o.append(nb)
    fig, a = engaged(SCX + 90, base + 30, 2.2, flip=True, hat=False)
    o.append(fig)
    o.append(ground(base + 40, SX0, SX1, op=0.18))
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 40, base + 110, 40, 8, 26))
    return finish(o + [zen_rank_close()])


def ea15(rng):
    """Fifth Rank of Earth: an old woman sweeping a yard in early morning, straw broom, bent back; leaves in small heaps. Nothing else."""
    o = [zen_rank_open("earth", 5)]
    base = SY1 - 150
    o.append(mist(SCX, base - 300, 340, 40, 0.5))
    o.append(path(f"M{SX0},{base - 120} Q{SCX},{base - 130} {SX1},{base - 118}", stroke=GREY, w=2, op=0.5, filt="brush"))  # yard wall
    o.append(path(f"M{SX0},{base - 118} Q{SCX},{base - 128} {SX1},{base - 116} L{SX1},{base - 90} L{SX0},{base - 90} Z", fill="#cfc6b6", op=0.3, filt="softwash"))
    o.append(trunk(rng, SX1 - 70, base - 100, base - 380, 12, -10, leafy=3))
    o.append(ground(base - 60, SX0, SX1, op=0.2))
    fig, a = ordinary(SCX - 20, base + 30, 2.4, flip=False)
    o.append(fig)
    for hx, hy, n in [(SX0 + 90, base + 60, 9), (SCX + 90, base + 90, 7), (SX0 + 160, base + 130, 5), (SX1 - 80, base + 40, 6)]:
        for _ in range(n):
            lx, ly = hx + rng.gauss(0, 16), hy + rng.gauss(0, 5)
            sz = rng.uniform(5, 9)
            o.append(f'<path d="M{f(lx)},{f(ly)} l{f(sz)},{f(-sz * 0.4)} l{f(-sz * 0.3)},{f(sz)} z" fill="{rng.choice([GREY, PALE, INK])}" opacity="{rng.uniform(0.5, 0.85):.2f}"/>')
    o.append(path(f"M{SCX + 20},{base + 28} q-30,6 -70,0 M{SCX + 30},{base + 40} q-40,6 -80,2", stroke=PALE, w=1.4, op=0.8))  # broom marks
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 150, base + 190, 14, 6, 14))
    return finish(o + [zen_rank_close()])


CARDS = {"ea01": ea01, "ea02": ea02, "ea03": ea03, "ea04": ea04, "ea05": ea05,
         "ea06": ea06, "ea07": ea07, "ea08": ea08, "ea09": ea09, "ea10": ea10,
         "ea11": ea11, "ea12": ea12, "ea13": ea13, "ea14": ea14, "ea15": ea15}
