"""Zen deck, minor series, suit of Water (wa01-wa15): feeling, relationship and the tea way.

Built on the pattern of zen_minor_earth, whose figure helpers (withdrawn, attending, acting,
engaged, ordinary), place() and props (bowl, floorboards and others) are imported rather than copied.

Pips wa01-wa10: zen_pip_open("water", n) draws the ensō with n spheres, then one small vignette of
the pip's Image paragraph is drawn in the lower inside of the ensō (ZEN_VIGNETTE), then
zen_pip_close(). Nothing round and filled is drawn near the emblem arc, so the sphere count stays
readable.

Ranks wa11-wa15 use the hanging-scroll frame with a fuller scene, and the same figure type as the
other suits for each rank: withdrawn (First), attending (Second), acting (Third), engaged (Fourth),
ordinary (Fifth). The setting and props are those of Water.

Helpers new to this module: water(), ripple(), rain(), chawan(), kettle(), tatami(), shoji(),
stone_row(), boat(), _sitter() and _bearer().
"""

import math

from .common import (GREY, INK, PALE, SCROLL_BOX, VERMILION, ZEN_VIGNETTE,
                     f, zen_pip_close, zen_pip_open, zen_rank_close, zen_rank_open)
from .zen_minor_earth import (STRAW, WOOD, _anchor, _arm, _smoke, acting, attending, bowl, cushion,
                              engaged, ordinary, place, withdrawn)
from .zen_transmission import GREYROBE, SKIN, ellipse, finish, head, path, tube
from .zen_way import grass, ground, hills, mist, rock, trunk

SX0, SY0, SX1, SY1 = SCROLL_BOX
SCX = (SX0 + SX1) / 2
VX0, VY0, VX1, VY1 = ZEN_VIGNETTE
VCX = (VX0 + VX1) / 2
FLOOR = 725
WATER, WATERD = "#c6cecd", "#a3b0af"
MAT = "#d9d0b2"


# ------------------------------------------------------------ new helpers

def water(x0, x1, y0, y1, op=0.6, col=WATER, edge=True):
    """A body of still water as a pale wash between y0 (far edge) and y1, with a faint line on the far edge."""
    out = [path(f"M{f(x0)},{f(y0)} L{f(x1)},{f(y0 + 2)} L{f(x1)},{f(y1)} L{f(x0)},{f(y1 + 2)} Z", fill=col, stroke=None, op=op, filt="softwash")]
    if edge:
        out.append(path(f"M{f(x0)},{f(y0)} Q{f((x0 + x1) / 2)},{f(y0 - 3)} {f(x1)},{f(y0 + 1)}", stroke=GREY, w=1.4, op=0.55, filt="brush"))
    return "".join(out)


def ripple(x, y, rx, n=3, op=0.8, col=GREY, w=1.5):
    """Concentric flattened rings spreading from (x, y)."""
    return "".join(ellipse(x, y, rx * (k + 1) / n, rx * 0.26 * (k + 1) / n, "none", stroke=col, w=w, op=op * (1 - k * 0.25))
                   for k in range(n))


def rain(rng, x0, x1, y0, y1, n, col=GREY, op=0.55):
    """Short slanted strokes of rain."""
    return "".join(path(f"M{f(x)},{f(y)} l-5,{rng.uniform(14, 24):.0f}", stroke=col, w=1.1, op=op * rng.uniform(0.6, 1.0))
                   for x, y in ((rng.uniform(x0, x1), rng.uniform(y0, y1)) for _ in range(n)))


def chawan(x, y, w, filled=None, rim=INK, col="#e4ded0", steam=False):
    """A tea bowl seen slightly from above, rim at y. filled is a surface colour (the bowl holds water) or None (empty)."""
    h = w * 0.55
    out = [path(f"M{f(x - w / 2)},{f(y)} C{f(x - w / 2)},{f(y + h * 0.9)} {f(x - w * 0.3)},{f(y + h)} {f(x)},{f(y + h)} "
                f"C{f(x + w * 0.3)},{f(y + h)} {f(x + w / 2)},{f(y + h * 0.9)} {f(x + w / 2)},{f(y)} Z",
                fill=col, stroke=INK, w=2.2, filt="brush"),
           ellipse(x, y, w / 2, w * 0.12, filled or "#8f877a", stroke=rim, w=1.9),
           path(f"M{f(x - w * 0.17)},{f(y + h)} l-1,4 h{f(w * 0.34 + 2)} l-1,-4", w=1.6)]
    if steam:
        out.append(path(f"M{f(x - 5)},{f(y - 8)} q-6,-10 0,-18 q6,-8 0,-16", stroke=PALE, w=1.4, op=0.8))
    return "".join(out)


def kettle(x, y, w, steam=True):
    """An iron kettle with a spout and a hooped handle, standing on the ground at y."""
    h = w * 0.72
    out = [path(f"M{f(x - w * 0.5)},{f(y - h * 0.35)} C{f(x - w * 0.55)},{f(y - h * 1.0)} {f(x + w * 0.55)},{f(y - h * 1.0)} {f(x + w * 0.5)},{f(y - h * 0.35)} "
                f"Q{f(x + w * 0.4)},{f(y)} {f(x)},{f(y)} Q{f(x - w * 0.4)},{f(y)} {f(x - w * 0.5)},{f(y - h * 0.35)} Z",
                fill=INK, stroke=INK, w=2, filt="brush"),
           path(f"M{f(x + w * 0.46)},{f(y - h * 0.5)} Q{f(x + w * 0.75)},{f(y - h * 0.6)} {f(x + w * 0.72)},{f(y - h * 0.95)}", stroke=INK, w=5),
           path(f"M{f(x - w * 0.44)},{f(y - h * 0.8)} Q{f(x)},{f(y - h * 1.7)} {f(x + w * 0.44)},{f(y - h * 0.8)}", stroke=INK, w=3),
           ellipse(x, y - h * 0.93, w * 0.1, w * 0.04, GREY),
           path(f"M{f(x - w * 0.3)},{f(y - h * 0.7)} Q{f(x - w * 0.2)},{f(y - h * 0.85)} {f(x - w * 0.05)},{f(y - h * 0.86)}", stroke=PALE, w=1.6, op=0.7)]
    if steam:
        out.append(_smoke(x + w * 0.72, y - h * 1.0, h * 1.1, 6))
        out.append(_smoke(x + w * 0.62, y - h * 1.0, h * 0.8, -6))
    return "".join(out)


def tatami(x0, x1, y0, y1, cols=3, fl=36):
    """A mat floor: pale straw wash, a far edge line and mat seams running toward the viewer, widening by fl each side."""
    out = [path(f"M{x0},{y0} L{x1},{y0} L{x1 + fl},{y1} L{x0 - fl},{y1} Z", fill=MAT, stroke=None, op=0.5, filt="softwash")]
    for k in range(cols + 1):
        t = k / cols
        out.append(path(f"M{f(x0 + (x1 - x0) * t)},{y0} L{f(x0 - fl + (x1 - x0 + 2 * fl) * t)},{y1}", stroke=GREY, w=1.3, op=0.45))
    out.append(path(f"M{x0},{y0} Q{f((x0 + x1) / 2)},{y0 - 3} {x1},{y0}", stroke=GREY, w=1.6, op=0.6, filt="brush"))
    return "".join(out)


def shoji(x0, y0, x1, y1, cols=3, rows=4, glow=0.55):
    """A paper screen: pale pane with a wooden lattice."""
    out = [path(f"M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z", fill="#f3eddc", stroke=INK, w=2.6, op=1, filt="brush")]
    out[0] = out[0].replace('/>', f' fill-opacity="{glow + 0.3:.2f}"/>', 1) if False else out[0]
    for k in range(1, cols):
        out.append(path(f"M{f(x0 + (x1 - x0) * k / cols)},{y0} L{f(x0 + (x1 - x0) * k / cols)},{y1}", stroke=INK, w=1.5, op=0.7))
    for k in range(1, rows):
        out.append(path(f"M{x0},{f(y0 + (y1 - y0) * k / rows)} L{x1},{f(y0 + (y1 - y0) * k / rows)}", stroke=INK, w=1.5, op=0.7))
    return "".join(out)


def stone_row(rng, x0, x1, y, n, size=11, col=GREY):
    """A line of small rounded stones from x0 to x1 along y."""
    return "".join(rock(rng, x0 + (x1 - x0) * k / max(1, n - 1) + rng.uniform(-3, 3), y + rng.uniform(-3, 3),
                        size * rng.uniform(0.8, 1.2), size * rng.uniform(0.6, 0.9), col) for k in range(n))


def boat(x, y, w, h=26):
    """A small flat boat, waterline at y, bow rising at both ends."""
    return (path(f"M{f(x - w / 2)},{f(y - h)} Q{f(x - w * 0.4)},{f(y + h * 0.3)} {f(x)},{f(y + h * 0.3)} Q{f(x + w * 0.4)},{f(y + h * 0.3)} {f(x + w / 2)},{f(y - h)} "
                 f"Q{f(x)},{f(y - h * 0.6)} {f(x - w / 2)},{f(y - h)} Z", fill="#b9a68a", stroke=INK, w=2.6, filt="brush")
            + path(f"M{f(x - w * 0.42)},{f(y - h * 0.5)} Q{f(x)},{f(y - h * 0.1)} {f(x + w * 0.42)},{f(y - h * 0.5)}", stroke=GREY, w=1.3, op=0.7))


def _sitter(x, y, s=1.0, flip=False, pose="sit", robe=GREYROBE):
    """A figure seated on a boat thwart, in profile facing +x. pose "flute": hands at a bamboo flute at the
    lips; "trail": leaning over the side with one arm hanging down. Origin is the seat. Returns (svg, anchors)."""
    o = [path("M-14,-4 L-11,-50 L11,-52 L15,-4 Z", fill=robe, stroke=INK, w=2.4, filt="brush"),
         path("M12,-6 L38,-6 L40,2", w=3.2)]
    if pose == "flute":
        o.append(head(1, -64, 10.5, look=1, hair=False))
        o.append(path("M7,-62 L46,-54", w=3.4, stroke="#8a7a52"))
        o.append(_arm((2, -46), (22, -36), (28, -56), SKIN, 4.6))
        o.append(_arm((0, -46), (14, -32), (38, -55), SKIN, 4.6))
        hand = (40, -2)
    else:
        o = [path("M-14,-4 Q-12,-30 -2,-50 L22,-50 L16,-4 Z", fill=robe, stroke=INK, w=2.4, filt="brush"),
             path("M12,-6 L34,-6 L36,2", w=3.2)]
        o.append(head(14, -62, 10.5, look=1, bowed=True, hair=False))
        o.append(_arm((16, -44), (38, -28), (48, 16), SKIN, 4.6))
        hand = (48, 16)
    return place(x, y, s, flip, "".join(o)), {"hand": _anchor(x, y, s, flip, hand)}


def _bearer(x, y, s=1.0, flip=False, robe=GREYROBE):
    """A figure walking with knees bent and both hands held out low in front, as when carrying a full bowl.
    Facing +x. Returns (svg, anchors) with the point where the hands meet under the load."""
    o = [path("M-3,-48 L-15,-26 L-12,0 M4,-48 L18,-30 L24,0", w=3.4),
         path("M-12,0 h-8 M22,0 h9", w=3),
         path("M-18,-42 Q-34,-44 -44,-54", w=3.4, stroke=GREY, op=0.7),
         path("M-14,-88 L14,-86 L18,-42 L-18,-40 Z", fill=robe, stroke=INK, w=2.4, filt="brush"),
         path("M-18,-56 L18,-58", w=2.2, stroke=GREY)]
    hand = (34, -50)
    o.append(_arm((6, -82), (24, -64), hand, SKIN, 4.8))
    o.append(_arm((0, -82), (18, -58), (28, -48), SKIN, 4.8))
    o.append(head(4, -100, 11, look=1, hair=False, bowed=True))
    return place(x, y, s, flip, "".join(o)), {"hand": _anchor(x, y, s, flip, hand)}


def _plank(x0, x1, y, h=14, op=0.55):
    """A wooden board seen edge on, top at y."""
    return path(f"M{x0},{y} Q{f((x0 + x1) / 2)},{y - 3} {x1},{y} L{x1},{y + h} L{x0},{y + h} Z", fill=WOOD, stroke=INK, w=2.2, op=op, filt="brush")


# ------------------------------------------------------------ pips wa01-wa10

def wa01(rng):
    """One of Water: an empty tea bowl on a veranda in light rain; a path runs down through mist to a river. No figure."""
    o = [zen_pip_open("water", 1)]
    o.append(water(VX0 + 10, VX1 - 10, FLOOR - 160, FLOOR - 110, op=0.7))
    o.append(path(f"M{VCX + 20},{FLOOR - 112} Q{VCX + 60},{FLOOR - 70} {VCX + 20},{FLOOR - 30} L{VCX + 150},{FLOOR - 30} Q{VCX + 100},{FLOOR - 70} {VCX + 70},{FLOOR - 112} Z",
                  fill="#cfc6b6", stroke=None, op=0.5, filt="softwash"))
    o.append(path(f"M{VCX + 20},{FLOOR - 112} Q{VCX + 60},{FLOOR - 70} {VCX + 20},{FLOOR - 30} M{VCX + 70},{FLOOR - 112} Q{VCX + 100},{FLOOR - 70} {VCX + 150},{FLOOR - 30}", stroke=GREY, w=1.5, op=0.7, filt="brush"))
    o.append(mist(VCX + 40, FLOOR - 120, 190, 22, 0.85))
    o.append(_plank(VX0 + 10, VX1 - 10, FLOOR - 2, 18))
    for k in range(4):
        o.append(path(f"M{VX0 + 60 + k * 100},{FLOOR - 1} l-8,18", stroke=GREY, w=1.2, op=0.6))
    o.append(chawan(VCX - 70, FLOOR - 36, 96))
    o.append(rain(rng, VX0 + 10, VX1 - 10, FLOOR - 190, FLOOR - 20, 46))
    return finish(o + [zen_pip_close()])


def wa02(rng):
    """Two of Water: wet footprints across a dry stone step into a tea room; a ripple spreads across a stone basin outside."""
    o = [zen_pip_open("water", 2)]
    # tea room doorway at left
    dx0, dx1 = VX0 + 10, VX0 + 130
    o.append(path(f"M{dx0},{FLOOR - 150} L{dx1},{FLOOR - 150} L{dx1},{FLOOR - 26} L{dx0},{FLOOR - 26} Z", fill="#8f877a", stroke=INK, w=3, op=0.55, filt="brush"))
    o.append(path(f"M{dx0 - 8},{FLOOR - 26} L{dx1 + 8},{FLOOR - 26} M{dx0 - 8},{FLOOR - 152} L{dx1 + 8},{FLOOR - 152}", stroke=INK, w=5, filt="brush"))
    o.append(path(f"M{dx0 + 20},{FLOOR - 26} L{dx0 + 20},{FLOOR - 120} M{dx1 - 20},{FLOOR - 26} L{dx1 - 20},{FLOOR - 120}", stroke=GREY, w=1.4, op=0.5))
    # the stone step: a flat slab in perspective, then a lower garden ground
    o.append(path(f"M{VX0 + 10},{FLOOR - 24} L{VX1 - 10},{FLOOR - 24} L{VX1 + 20},{FLOOR + 30} L{VX0 - 10},{FLOOR + 30} Z", fill="#cfc9bc", stroke=INK, w=2.4, op=0.7, filt="brush"))
    # footprints, wet and dark, coming in from the right and fading as they dry
    for k in range(5):
        px, py = VX0 + 270 - k * 44, FLOOR + 8 + (k % 2) * 14
        o.append(ellipse(px, py, 10, 17, INK, op=0.8 - k * 0.1, filt="brush"))
        o.append(ellipse(px - 6, py - 21, 4.5, 6, INK, op=0.65 - k * 0.08))
    # basin on a stone at the right
    bx, by = VX1 - 70, FLOOR - 18
    o.append(path(f"M{bx - 40},{by - 40} L{bx + 40},{by - 40} L{bx + 34},{by + 28} L{bx - 34},{by + 28} Z", fill="#a79e8f", stroke=INK, w=2.6, op=0.85, filt="brush"))
    o.append(ellipse(bx, by - 40, 44, 12, WATER, stroke=INK, w=2.2))
    o.append(ripple(bx, by - 40, 30, 3, 0.9))
    return finish(o + [zen_pip_close()])


def wa03(rng):
    """Three of Water: moonlight lies in a bowl of still water on a low table; a hand hovers above, the surface unbroken."""
    o = [zen_pip_open("water", 3), ground(FLOOR + 22, VX0 + 10, VX1 - 10, op=0.12)]
    tx, ty = VCX - 20, FLOOR - 30
    o.append(path(f"M{tx - 150},{ty - 100} L{tx - 100},{ty - 100} L{tx + 90},{ty + 10} L{tx + 20},{ty + 10} Z", fill="#fff8e4", stroke=None, op=0.8, filt="softwash"))  # a slant of moonlight
    o.append(path(f"M{tx - 110},{ty} L{tx + 110},{ty} L{tx + 100},{ty + 10} L{tx - 100},{ty + 10} Z", fill=WOOD, stroke=INK, w=2.6, filt="brush"))
    o.append(path(f"M{tx - 96},{ty + 10} L{tx - 100},{ty + 70} M{tx + 96},{ty + 10} L{tx + 100},{ty + 70}", stroke=INK, w=5))
    o.append(path(f"M{tx - 96},{ty + 44} L{tx + 96},{ty + 44}", stroke=GREY, w=2.4, op=0.7))
    cx, cy, w = tx, ty - 6, 150
    o.append(path(f"M{cx - w / 2},{cy - 40} C{cx - w / 2},{cy} {cx - w * 0.3},{cy + 2} {cx},{cy + 2} C{cx + w * 0.3},{cy + 2} {cx + w / 2},{cy} {cx + w / 2},{cy - 40} Z", fill="#e4ded0", stroke=INK, w=2.4, filt="brush"))
    o.append(ellipse(cx, cy - 40, w / 2, 17, "#8fa0a1", stroke=INK, w=2))
    o.append(ellipse(cx - 6, cy - 40, 15, 5, "#fff8e4", op=0.95, filt="wash"))  # the moon lying in the water
    o.append(ellipse(cx - 6, cy - 40, 15, 5, "none", stroke="#fff8e4", w=1.5))
    # the hand, flat above the bowl, arm coming from the upper right
    hx, hy = cx + 10, cy - 120
    arm = f"M{hx + 150},{hy - 70} Q{hx + 80},{hy - 60} {hx + 26},{hy - 12}"
    o.append(tube(arm, 11, GREYROBE))
    o.append(ellipse(hx, hy - 4, 28, 8, SKIN, stroke=INK, w=2))
    for k in range(4):
        o.append(path(f"M{hx - 20 + k * 11},{hy - 2} q-3,8 -6,14", stroke=INK, w=3, cap="round"))
    return finish(o + [zen_pip_close()])


def wa04(rng):
    """Four of Water: a figure crosses a wooden bridge in wind, both hands under a full bowl, knees bent; the water trembles at the rim."""
    o = [zen_pip_open("water", 4)]
    o.append(water(VX0 + 10, VX1 - 10, FLOOR + 6, FLOOR + 60, op=0.55))
    o.append(path(f"M{VX0 + 14},{FLOOR - 4} Q{VCX},{FLOOR - 52} {VX1 - 14},{FLOOR - 4}", stroke=INK, w=9, filt="brush"))
    o.append(path(f"M{VX0 + 14},{FLOOR + 6} Q{VCX},{FLOOR - 40} {VX1 - 14},{FLOOR + 6}", stroke=WOOD, w=6))
    for k in range(6):
        px = VX0 + 40 + k * 64
        py = FLOOR - 4 - 48 * (1 - ((px - VCX) / (VCX - VX0 - 14)) ** 2) * 0.78
        o.append(path(f"M{px},{py + 4} L{px},{py + 30}", stroke=INK, w=3.4, op=0.8))
    for k in range(5):
        o.append(path(f"M{VX0 + 12 + k * 20},{FLOOR + 12 + k * 6} l{14 + k * 4},0", stroke=PALE, w=1.3, op=0.8))
    fig, a = _bearer(VCX - 20, FLOOR - 38, 1.9)
    o.append(fig)
    hx, hy = a["hand"]
    o.append(chawan(hx + 4, hy - 4, 44, filled=WATER))
    for k in range(3):  # the water trembling at the rim
        o.append(path(f"M{f(hx - 14 + k * 14)},{f(hy - 14 - k % 2 * 4)} q4,-8 8,0", stroke=GREY, w=1.5, op=0.9))
    for k in range(6):  # wind
        wy = FLOOR - 190 + k * 34
        o.append(path(f"M{VX1 - 30 - k * 8},{wy} q-60,-10 -120,{rng.uniform(-6, 6):.0f}", stroke=PALE, w=1.6, op=0.85))
    return finish(o + [zen_pip_close()])


def wa05(rng):
    """Five of Water: a channel runs through a garden between two lines of stones; a figure kneels and clears a fallen leaf from the gate where it enters."""
    o = [zen_pip_open("water", 5), ground(FLOOR - 70, VX0 + 10, VX1 - 10, op=0.12)]
    cy0, cy1 = FLOOR + 6, FLOOR + 40
    o.append(path(f"M{VX0 + 60},{cy0} L{VX1 - 10},{cy0 - 2} L{VX1 - 10},{cy1} L{VX0 + 60},{cy1} Z", fill=WATER, stroke=None, op=0.8, filt="softwash"))
    for k in range(4):
        o.append(path(f"M{VX0 + 120 + k * 80},{cy0 + 10 + (k % 2) * 12} q22,-4 46,0", stroke=PALE, w=1.4, op=0.9))
    o.append(stone_row(rng, VX0 + 70, VX1 - 20, cy0 - 4, 9, 13))
    o.append(stone_row(rng, VX0 + 60, VX1 - 20, cy1 + 8, 9, 14))
    # the gate where the water enters: two posts and a slatted board
    gx = VX0 + 52
    o.append(path(f"M{gx},{cy0 - 56} L{gx},{cy1 + 6} M{gx + 30},{cy0 - 56} L{gx + 30},{cy1 + 6}", stroke=INK, w=6, filt="brush"))
    o.append(path(f"M{gx - 4},{cy0 - 50} L{gx + 34},{cy0 - 50}", stroke=INK, w=5))
    for k in range(4):
        o.append(path(f"M{gx + 5 + k * 7},{cy0 - 20} L{gx + 5 + k * 7},{cy1 + 4}", stroke=GREY, w=2))
    o.append(f'<path d="M{gx + 10},{cy0 - 6} q7,-9 15,0 q-7,7 -15,0 z" fill="{VERMILION}" opacity="0.9"/>')  # the fallen leaf
    fig, a = attending(302, FLOOR - 20, 1.9, flip=True, seat=18, lean=32, reach=(46, 10))
    o.append(fig)
    o.append(grass(rng, VX0 + 100, VX1 - 20, FLOOR - 50, FLOOR - 24, 16, 8, 22))
    return finish(o + [zen_pip_close()])


def wa06(rng):
    """Six of Water: two people drift in a small boat on a wide river at dusk; one plays a bamboo flute, the other trails a hand in the water; the far bank is a faint line."""
    o = [zen_pip_open("water", 6)]
    o.append(water(VX0 - 10, VX1 + 10, FLOOR - 150, FLOOR + 70, op=0.5, edge=False))
    o.append(path(f"M{VX0 - 10},{FLOOR - 150} Q{VCX},{FLOOR - 156} {VX1 + 10},{FLOOR - 148}", stroke=GREY, w=1.6, op=0.4, filt="brush"))
    o.append(hills(rng, [(FLOOR - 150, 26, PALE, 0.3, 70)], VX0 - 10, VX1 + 10))
    o.append(mist(VCX, FLOOR - 140, 200, 14, 0.7))
    bx, by = VCX, FLOOR + 22
    o.append(boat(bx, by, 290, 28))
    f1, _ = _sitter(bx - 75, by - 22, 1.5, pose="flute")
    f2, a2 = _sitter(bx + 50, by - 22, 1.5, pose="trail")
    o.append(f1 + f2)
    hx, hy = a2["hand"]
    o.append(ripple(hx, by + 8, 34, 3))
    o.append(path(f"M{bx - 120},{by + 14} q-30,6 -70,2 M{bx + 120},{by + 14} q30,6 70,2", stroke=PALE, w=1.5, op=0.8))
    o.append(path(f"M{VX0 + 20},{FLOOR + 56} q60,-5 120,0 M{VX1 - 150},{FLOOR + 50} q60,-5 120,0", stroke=PALE, w=1.4, op=0.7))
    return finish(o + [zen_pip_close()])


def wa07(rng):
    """Seven of Water: a tea room late in the afternoon; utensils at rest on the tatami, one figure looking at the kettle, the door open to the garden."""
    o = [zen_pip_open("water", 7), tatami(VX0 + 10, VX1 - 10, FLOOR - 36, FLOOR + 50, 4)]
    dx0, dx1 = VX0 + 14, VX0 + 118
    o.append(path(f"M{dx0},{FLOOR - 176} L{dx1},{FLOOR - 176} L{dx1},{FLOOR - 36} L{dx0},{FLOOR - 36} Z", fill="#cdd3c4", stroke=INK, w=3, op=0.8, filt="brush"))
    o.append(path(f"M{dx0 + 20},{FLOOR - 40} Q{dx0 + 40},{FLOOR - 110} {dx0 + 80},{FLOOR - 150} M{dx0 + 80},{FLOOR - 150} q14,-4 22,4", stroke=INK, w=3, op=0.75, filt="brush"))
    o.append(path(f"M{VX1 - 12},{FLOOR - 176} L{VX1 - 12},{FLOOR - 36}", stroke=INK, w=4, filt="brush"))
    o.append(ellipse(VCX - 10, FLOOR - 40, 160, 24, "#fff4d6", op=0.5, filt="wash"))  # late light
    fig, _ = withdrawn(VCX + 24, FLOOR + 12, 2.2, view="side", eyes_closed=False)
    o.append(fig)
    o.append(kettle(VCX + 150, FLOOR + 22, 64, steam=True))
    o.append(path(f"M{VCX + 108},{FLOOR + 24} L{VCX + 192},{FLOOR + 24}", stroke=INK, w=3))
    # utensils at rest: a bowl, a whisk laid down, a scoop, a lidded caddy
    o.append(chawan(VCX - 110, FLOOR + 14, 48))
    o.append(path(f"M{VCX - 56},{FLOOR + 40} l34,-6", stroke="#8a7a52", w=3))
    o.append(path(f"M{VCX - 30},{FLOOR + 22} q10,6 18,0 l-4,14 h-10 z", fill=STRAW, stroke=INK, w=1.6))
    o.append(path(f"M{VCX - 100},{FLOOR + 56} l60,-4", stroke="#8a7a52", w=2.6))
    return finish(o + [zen_pip_close()])


def wa08(rng):
    """Eight of Water: a plain bowl in the centre of an empty tatami room, with a ring of damp beneath it; the screens are closed and the light even."""
    o = [zen_pip_open("water", 8)]
    wall_y = FLOOR - 70
    for k in range(3):
        sx = VX0 + 10 + k * 127
        o.append(shoji(sx, wall_y - 130, sx + 127, wall_y, 3, 5))
    o.append(tatami(VX0 + 10, VX1 - 10, wall_y, FLOOR + 60, 4, 56))
    o.append(path(f"M{VX0 + 10},{wall_y} L{VX1 - 10},{wall_y}", stroke=INK, w=3))
    cx, cy = VCX, FLOOR - 4
    o.append(ellipse(cx, cy + 22, 52, 13, "#8f877a", op=0.5, filt="wash"))
    o.append(ellipse(cx, cy + 22, 52, 13, "none", stroke=GREY, w=1.6, op=0.8))
    o.append(chawan(cx, cy - 14, 58))
    return finish(o + [zen_pip_close()])


def wa09(rng):
    """Nine of Water: an iron kettle simmers on a charcoal hearth in an empty tea room; through the open shoji a stream runs past red maples. No figure."""
    o = [zen_pip_open("water", 9)]
    wall_y = FLOOR - 36
    top = wall_y - 190
    ox0, ox1 = VCX - 20, VX1 - 10
    o.append(shoji(VX0 + 10, top, ox0, wall_y, 2, 5))
    # the opening onto the garden
    o.append(path(f"M{ox0},{top} L{ox1},{top} L{ox1},{wall_y} L{ox0},{wall_y} Z", fill="#dfe3d6", stroke=INK, w=3, op=0.9, filt="brush"))
    o.append(path(f"M{ox0 + 4},{wall_y - 40} C{ox0 + 50},{wall_y - 70} {ox0 + 100},{wall_y - 18} {ox1 - 4},{wall_y - 52}", stroke=WATER, w=32, op=0.95, filt="softwash"))
    o.append(path(f"M{ox0 + 4},{wall_y - 54} C{ox0 + 50},{wall_y - 84} {ox0 + 100},{wall_y - 32} {ox1 - 4},{wall_y - 66}", stroke=GREY, w=1.3, op=0.6))
    bough = f"M{ox1},{top + 14} C{ox1 - 40},{top + 24} {ox0 + 60},{top + 44} {ox0 + 20},{top + 84}"
    o.append(path(bough, stroke=INK, w=4, filt="brush"))
    for _ in range(11):
        t = rng.uniform(0.1, 0.95)
        lx = ox1 - (ox1 - ox0 - 20) * t + rng.uniform(-8, 8)
        ly = top + 14 + (70 * t) + rng.uniform(-6, 24)
        o.append(f'<path d="M{f(lx)},{f(ly)} l10,-3 l-3,10 z" fill="{VERMILION}" opacity="0.9" transform="rotate({rng.uniform(0, 360):.0f} {f(lx)} {f(ly)})"/>')
    o.append(path(f"M{VX0 + 6},{wall_y} L{VX1 - 6},{wall_y}", stroke=INK, w=3.4))
    o.append(tatami(VX0 + 10, VX1 - 10, wall_y, FLOOR + 60, 4, 50))
    # the hearth: a sunken frame of dark wood with charcoal, and the kettle above it
    hx, hy = VCX - 70, FLOOR + 36
    o.append(path(f"M{hx - 90},{hy - 10} L{hx + 90},{hy - 10} L{hx + 104},{hy + 18} L{hx - 104},{hy + 18} Z", fill=INK, stroke=INK, w=3, op=0.9, filt="brush"))
    o.append(path(f"M{hx - 72},{hy - 4} L{hx + 72},{hy - 4} L{hx + 82},{hy + 10} L{hx - 82},{hy + 10} Z", fill="#59544c", stroke=None))
    for _ in range(14):
        o.append(path(f"M{f(hx + rng.uniform(-64, 64))},{f(hy + rng.uniform(-2, 8))} l{rng.uniform(-5, 5):.0f},{rng.uniform(-3, 2):.0f}", stroke=PALE, w=2.2, op=0.6))
    o.append(kettle(hx, hy - 6, 96, steam=True))
    return finish(o + [zen_pip_close()])


def wa10(rng):
    """Ten of Water: a roadside stall under a straw awning; a barefoot man ladles water into a bowl for a weary porter, others wait, children play in a puddle."""
    o = [zen_pip_open("water", 10), ground(FLOOR - 4, VX0 + 10, VX1 - 10, op=0.16)]
    # awning on two posts
    for px in (VX0 + 20, VCX + 20):
        o.append(path(f"M{px},{FLOOR - 6} Q{px + 3},{FLOOR - 100} {px},{FLOOR - 190}", stroke=INK, w=6, filt="brush"))
    o.append(path(f"M{VX0 - 6},{FLOOR - 184} L{VCX + 100},{FLOOR - 184} L{VCX + 70},{FLOOR - 236} L{VX0 + 24},{FLOOR - 236} Z", fill=STRAW, stroke=INK, w=2.6, filt="brush"))
    for k in range(9):
        o.append(path(f"M{VX0 + 28 + k * 12},{FLOOR - 236 + (k > 6) * 0} L{VX0 + 6 + k * 13},{FLOOR - 184}", stroke=GREY, w=1.2, op=0.7))
    # counter and bucket
    o.append(path(f"M{VX0 + 6},{FLOOR - 50} L{VCX + 60},{FLOOR - 50} L{VCX + 60},{FLOOR - 36} L{VX0 + 6},{FLOOR - 36} Z", fill=WOOD, stroke=INK, w=2.4, filt="brush"))
    o.append(path(f"M{VX0 + 20},{FLOOR - 36} L{VX0 + 20},{FLOOR - 6} M{VCX + 40},{FLOOR - 36} L{VCX + 40},{FLOOR - 6}", stroke=INK, w=4))
    bx = VCX - 10
    o.append(path(f"M{bx - 26},{FLOOR - 92} L{bx + 26},{FLOOR - 92} L{bx + 21},{FLOOR - 50} L{bx - 21},{FLOOR - 50} Z", fill=WOOD, stroke=INK, w=2.2, filt="brush"))
    o.append(ellipse(bx, FLOOR - 92, 26, 5, WATER, stroke=INK, w=1.8))
    o.append(path(f"M{bx - 26},{FLOOR - 82} h52 M{bx - 24},{FLOOR - 64} h48", stroke=GREY, w=1.4, op=0.7))
    # the barefoot man at the counter, ladle out to the porter's bowl
    fig, a = acting(VX0 + 90, FLOOR - 2, 1.65, strike=False, reach=(52, -66), robe=SKIN)
    o.append(fig)
    hx, hy = a["hands"][0]
    # porter and the one waiting
    por, pa = ordinary(VCX + 140, FLOOR - 2, 1.7, flip=True, tool=None, robe="#a9a398")
    o.append(por)
    ph = (VCX + 140 - 30 * 1.7, FLOOR - 2 - 62 * 1.7)
    o.append(tube(f"M{VCX + 140 - 6 * 1.7},{FLOOR - 2 - 66 * 1.7} Q{ph[0] + 8},{ph[1] + 30} {ph[0]},{ph[1]}", 4.4, SKIN))
    o.append(chawan(ph[0] - 2, ph[1] - 4, 34, filled=WATER))
    o.append(path(f"M{hx},{hy} L{ph[0] + 14},{ph[1] - 18}", stroke="#6b5a45", w=3))  # the ladle
    wf, _ = ordinary(VX1 - 20, FLOOR - 2, 1.25, flip=True, tool=None, robe="#c9c4ba")
    o.append(wf)
    # puddle and children
    px, py = VCX - 20, FLOOR + 44
    o.append(ellipse(px, py, 80, 14, WATER, stroke=GREY, w=1.5, op=0.85))
    o.append(ripple(px + 20, py, 30, 2, 0.9))
    for cx0, dirn in ((px - 30, 1), (px + 46, -1)):
        o.append(path(f"M{cx0},{py + 4} l-2,-26 M{cx0},{py - 22} l{12 * dirn},-10 M{cx0},{py - 22} l{-10 * dirn},-8", stroke=INK, w=2.6))
        o.append(f'<circle cx="{cx0}" cy="{py - 30}" r="6" fill="{SKIN}" stroke="{INK}" stroke-width="1.6"/>')
    return finish(o + [zen_pip_close()])


# ------------------------------------------------------------ ranks wa11-wa15

def wa11(rng):
    """First Rank of Water: a hermit beside a mountain pool in late autumn, the water clear, no leaf moving on it."""
    o = [zen_rank_open("water", 1)]
    base = SY1 - 150
    ridge = [(SX0 + 4, 540), (170, 490), (220, 420), (262, 360), (300, 326), (340, 290), (382, 332), (420, 380), (470, 440), (520, 490), (SX1 - 4, 520)]
    mass = "M" + " L".join(f"{a},{b}" for a, b in ridge + [(SX1 - 4, 680), (SX0 + 4, 680)]) + " Z"
    # the mountain fades downward into the mist, with no hard lower edge
    o.append('<defs><linearGradient id="wa11fade" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="0.62" stop-color="#fff" stop-opacity="0.85"/>'
             '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             f'<mask id="wa11mask" maskUnits="userSpaceOnUse" x="{SX0}" y="280" width="{SX1 - SX0}" height="420">'
             f'<rect x="{SX0}" y="280" width="{SX1 - SX0}" height="400" fill="url(#wa11fade)"/></mask></defs>')
    o.append(f'<g mask="url(#wa11mask)">{path(mass, fill="#a39d90", stroke=None, op=0.4, filt="softwash")}</g>')
    o.append(path("M" + " L".join(f"{a},{b}" for a, b in ridge), stroke=INK, w=3, op=0.7, filt="brush"))
    o.append(mist(SCX, 650, 250, 34, 0.75))

    # pool: a flat ellipse in perspective, still water in a soft wash, the mountain reflected upside down
    pcx, pcy, prx, pry = SCX + 25, base - 10, 172, 70
    o.append(f'<defs><clipPath id="wa11pond"><ellipse cx="{pcx}" cy="{pcy}" rx="{prx}" ry="{pry}"/></clipPath>'
             f'<radialGradient id="wa11still" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="{WATER}" stop-opacity="0.25"/>'
             f'<stop offset="1" stop-color="{WATER}" stop-opacity="0.85"/></radialGradient></defs>')
    o.append(f'<ellipse cx="{pcx}" cy="{pcy}" rx="{prx}" ry="{pry}" fill="url(#wa11still)" filter="url(#softwash)"/>')
    pond = []
    # reflection: the ridge mirrored about the far bank and squashed, in pale wash
    far = pcy - pry + 6
    refl = [(pcx + (x - SCX) * 0.8, far + (520 - y) * 0.42) for x, y in ridge]
    rpath = f"M{refl[0][0]},{far} " + " ".join(f"L{f(x)},{f(y)}" for x, y in refl) + f" L{refl[-1][0]},{far} Z"
    pond.append(path(rpath, fill="#8f8a82", stroke=None, op=0.38, filt="softwash"))
    # horizontal strokes breaking the reflection: the sign of still water in ink painting
    for k in range(9):
        yy = far + 12 + k * 13 + rng.uniform(-3, 3)
        xx = pcx + rng.uniform(-150, 90)
        ln = rng.uniform(40, 110)
        pond.append(path(f"M{f(xx)},{f(yy)} l{f(ln)},{f(rng.uniform(-1, 1))}", stroke=rng.choice([GREY, PALE]), w=rng.uniform(1.0, 2.2), op=0.55, filt="brush"))
    o.append(f'<g clip-path="url(#wa11pond)">{"".join(pond)}</g>')
    # rim: broken dry-brush arcs, heavier at the near edge, open in places
    for a0, a1, w_, op_ in [(195, 250, 2.4, 0.7), (265, 330, 1.6, 0.5), (345, 400, 2.6, 0.75), (20, 160, 3.6, 0.9)]:
        pts = [(pcx + prx * math.cos(math.radians(a)), pcy + pry * math.sin(math.radians(a))) for a in range(a0, a1 + 1, 6)]
        o.append(path("M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts), stroke=INK, w=w_, op=op_, filt="dry"))
    # reeds and a stone at the far right edge of the pool
    for k in range(7):
        rx_ = pcx + prx - 52 + k * 7 + rng.uniform(-3, 3)
        rh = rng.uniform(40, 80)
        o.append(path(f"M{f(rx_)},{f(pcy - 20)} q{f(rng.uniform(-4, 4))},{f(-rh * 0.6)} {f(rng.uniform(-8, 8))},{f(-rh)}", stroke=INK, w=1.4, op=0.75))
    o.append(rock(rng, pcx + 90, pcy + 18, 18, 9, op=0.45))
    # bank at left with the hermit
    o.append(ellipse(SX0 + 100, base - 38, 120, 36, "#8f877a", stroke=INK, w=2.4, op=0.7, filt="brush"))
    fig, a = withdrawn(SX0 + 110, base - 50, 2.0, view="side", robe="#b3ad9f")
    o.append(fig)
    o.append(rock(rng, SX0 + 40, base - 8, 26, 16))
    for _ in range(9):  # fallen leaves lie on the bank, none on the water
        lx, ly = SX0 + rng.uniform(20, 190), base - rng.uniform(26, 50)
        o.append(f'<path d="M{f(lx)},{f(ly)} l8,-3 l-3,8 z" fill="{rng.choice([GREY, PALE, "#a79e8f"])}" opacity="0.8"/>')
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 120, base + 160, 24, 8, 20))
    return finish(o + [zen_rank_close()])


def wa12(rng):
    """Second Rank of Water: a tea host in a small room cleaning a worn bowl with a white cloth; light from the window falls on the steam."""
    o = [zen_rank_open("water", 2)]
    base = SY1 - 130
    wy = base - 330
    o.append(path(f"M{SX0},{wy - 60} L{SX1},{wy - 60} L{SX1},{base + 20} L{SX0},{base + 20} Z", fill="#e4ded0", stroke=None, op=0.4, filt="softwash"))
    # latticed window at the upper right, with a slant of light
    wx0, wx1, wyt, wyb = SCX + 20, SX1 - 36, wy, wy + 150
    o.append(path(f"M{wx0},{wyt} L{wx1},{wyt} L{wx1},{wyb} L{wx0},{wyb} Z", fill="#f6f0dc", stroke=INK, w=3.2, filt="brush"))
    for k in range(1, 4):
        o.append(path(f"M{wx0 + (wx1 - wx0) * k / 4},{wyt} L{wx0 + (wx1 - wx0) * k / 4},{wyb}", stroke=INK, w=1.6, op=0.7))
    o.append(path(f"M{wx0},{wyt + 75} L{wx1},{wyt + 75}", stroke=INK, w=1.6, op=0.7))
    o.append(path(f"M{wx0},{wyb} L{wx0 - 130},{base - 40} L{wx0 - 40},{base - 40} L{wx1},{wyb} Z", fill="#fff8e4", stroke=None, op=0.55, filt="softwash"))
    o.append(tatami(SX0 + 14, SX1 - 14, base - 40, base + 120, 3, 40))
    # the host kneeling, holding the bowl and the cloth
    fig, a = attending(SCX - 90, base + 20, 2.3, flip=False, seat=18, lean=24, reach=(60, -52))
    o.append(fig)
    hx, hy = a["hands"][0]
    o.append(chawan(hx + 8, hy - 2, 70, col="#d8cfbd"))
    o.append(path(f"M{hx - 22},{hy - 6} q18,-14 42,-4 q-10,14 -34,14 z", fill="#fffdf6", stroke=INK, w=1.8))  # the white cloth
    for k, dx in enumerate((-18, 4, 26)):  # steam catching the light
        o.append(path(f"M{hx + 8 + dx},{hy - 20} C{hx + 20 + dx},{hy - 60} {hx - 6 + dx},{hy - 90} {hx + 14 + dx},{hy - 130 - k * 12}", stroke=PALE, w=2.6, op=0.95))
    # kettle and a water jar at the side
    o.append(kettle(SCX + 150, base + 40, 70, steam=False))
    o.append(path(f"M{SCX - 200},{base + 40} q-20,-30 0,-56 h44 q20,26 0,56 z", fill="#cfc6b6", stroke=INK, w=2.2, filt="brush"))
    return finish(o + [zen_rank_close()])


def wa13(rng):
    """Third Rank of Water: a ferryman at a river crossing, pole in hand, a hurried traveller arriving at dusk; the boat small and the current strong."""
    o = [zen_rank_open("water", 3)]
    base = SY1 - 150
    hor = base - 330
    o.append(ellipse(SCX + 90, hor - 40, 52, 52, "#e6dfd0", op=0.6, filt="wash"))
    o.append(hills(rng, [(hor + 10, 44, PALE, 0.28, 80)], SX0 + 4, SX1 - 4))
    o.append(water(SX0 + 4, SX1 - 4, hor + 10, base + 40, op=0.5))
    for k in range(18):  # strong current: long streaks, all leaning one way
        yy = hor + 40 + k * 22
        xx = rng.uniform(SX0 + 20, SX1 - 120)
        o.append(path(f"M{f(xx)},{f(yy)} q40,-7 {rng.uniform(70, 110):.0f},{rng.uniform(-3, 3):.0f}", stroke=GREY if k % 2 else PALE, w=1.6, op=0.7))
    # near bank at the right, with the traveller
    o.append(path(f"M{SX1 - 4},{base - 80} Q{SX1 - 90},{base - 70} {SX1 - 150},{base + 10} Q{SX1 - 100},{base + 60} {SX1 - 4},{base + 70} Z", fill="#cfc6b6", stroke=INK, w=2.2, op=0.7, filt="brush"))
    trav, _ = ordinary(SX1 - 70, base - 8, 1.35, flip=True, tool=None, robe="#a9a398")
    o.append(trav)
    # the ferryman standing in the boat with the pole planted
    bx, by = SCX - 80, base - 80
    o.append(boat(bx, by, 250, 30))
    fig, a = acting(bx - 20, by - 10, 1.8, flip=False, strike=False, reach=(34, -48))
    o.append(fig)
    px, py = a["hands"][0]
    o.append(path(f"M{px + 10},{py - 190} L{px + 52},{by + 90}", stroke="#6b5a45", w=6))
    o.append(path(f"M{bx - 120},{by + 14} q-40,8 -90,0 M{bx + 120},{by + 14} q40,8 90,0", stroke=PALE, w=1.6, op=0.9))
    o.append(ripple(px + 52, by + 90, 36, 3))
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 90, base + 150, 20, 8, 20))
    return finish(o + [zen_rank_close()])


def wa14(rng):
    """Fourth Rank of Water: a tea master and a guest kneel across a hearth, steam rising between them from a single bowl; the room plain and warm."""
    o = [zen_rank_open("water", 4)]
    base = SY1 - 150
    wy = base - 330
    o.append(path(f"M{SX0},{wy} L{SX1},{wy} L{SX1},{base} L{SX0},{base} Z", fill="#e4ded0", stroke=None, op=0.4, filt="softwash"))
    o.append(shoji(SX0 + 40, wy + 20, SCX - 20, wy + 200, 3, 5))
    o.append(path(f"M{SCX + 40},{wy + 20} L{SX1 - 40},{wy + 20} L{SX1 - 40},{wy + 200} L{SCX + 40},{wy + 200} Z", fill="#ddd5c0", stroke=INK, w=2.6, op=0.7, filt="brush"))
    o.append(path(f"M{SCX + 52},{wy + 40} l50,0 M{SCX + 52},{wy + 170} l90,0", stroke=GREY, w=2, op=0.5))
    o.append(tatami(SX0 + 14, SX1 - 14, wy + 200, base + 120, 4, 60))
    hx, hy = SCX, base + 60
    o.append(ellipse(hx, hy, 130, 28, "#fff4d6", op=0.6, filt="wash"))  # warmth of the fire
    o.append(path(f"M{hx - 66},{hy - 14} L{hx + 66},{hy - 14} L{hx + 84},{hy + 22} L{hx - 84},{hy + 22} Z", fill=INK, stroke=INK, w=3, op=0.88, filt="brush"))
    o.append(path(f"M{hx - 50},{hy - 6} L{hx + 50},{hy - 6} L{hx + 64},{hy + 14} L{hx - 64},{hy + 14} Z", fill="#59544c", stroke=None))
    o.append(chawan(hx, hy - 4, 56))
    for dx in (-14, 0, 14):
        o.append(_smoke(hx + dx, hy - 30, 150 - abs(dx) * 3, 8 if dx else -8, PALE, 2.6))
    gf, _ = withdrawn(SCX - 140, base + 80, 1.7, view="side", robe="#b3ad9f", eyes_closed=False)
    o.append(gf)
    mf, _ = engaged(SCX + 150, base + 60, 1.7, flip=True, hat=False, tool=None, seat="floor")
    o.append(mf)
    return finish(o + [zen_rank_close()])


def wa15(rng):
    """Fifth Rank of Water: an old woman at a village well in the early morning, lowering a wooden bucket, nodding to a neighbour as she goes on."""
    o = [zen_rank_open("water", 5)]
    base = SY1 - 150
    o.append(mist(SCX, base - 300, 340, 40, 0.5))
    o.append(path(f"M{SX0},{base - 100} Q{SCX},{base - 110} {SX1},{base - 98} L{SX1},{base - 70} L{SX0},{base - 70} Z", fill="#cfc6b6", op=0.3, filt="softwash"))
    o.append(path(f"M{SX0},{base - 100} Q{SCX},{base - 110} {SX1},{base - 98}", stroke=GREY, w=2, op=0.5, filt="brush"))
    o.append(ground(base - 50, SX0, SX1, op=0.2))
    # the well: a stone ring, two posts, a cross-beam and rope
    wx, wy = SCX + 80, base + 40
    o.append(path(f"M{wx - 70},{wy - 40} L{wx + 70},{wy - 40} L{wx + 62},{wy + 30} L{wx - 62},{wy + 30} Z", fill="#a79e8f", stroke=INK, w=2.8, filt="brush"))
    o.append(ellipse(wx, wy - 40, 70, 14, "#6e6a63", stroke=INK, w=2.4))
    for k in range(3):
        o.append(path(f"M{wx - 62 + k * 22},{wy - 26} l0,40", stroke=GREY, w=1.2, op=0.6))
    for dx in (-60, 60):
        o.append(path(f"M{wx + dx},{wy - 40} Q{wx + dx + 3},{wy - 140} {wx + dx},{wy - 230}", stroke=INK, w=9, filt="dry"))
    o.append(path(f"M{wx - 76},{wy - 230} L{wx + 76},{wy - 232}", stroke=INK, w=8, filt="brush"))
    rope_top = (wx - 30, wy - 226)
    # the old woman at the rim, hands on the rope
    fig, a = ordinary(wx - 150, base + 40, 2.3, flip=False, tool=None)
    o.append(fig)
    s = 2.3
    sh = (wx - 150 + 6 * s, base + 40 - 70 * s)
    hand = (wx - 150 + 38 * s, base + 40 - 58 * s)
    o.append(tube(f"M{f(sh[0])},{f(sh[1])} Q{f(sh[0] + 28)},{f(sh[1] + 36)} {f(hand[0])},{f(hand[1])}", 10, SKIN))
    o.append(ellipse(hand[0], hand[1], 6, 5.5, SKIN, stroke=INK, w=1.6))
    o.append(path(f"M{f(rope_top[0])},{f(rope_top[1])} L{f(hand[0])},{f(hand[1])}", stroke="#6b5a45", w=2.4))
    # the bucket going down into the well
    o.append(path(f"M{wx - 30},{wy - 226} L{wx - 30},{wy - 128}", stroke="#6b5a45", w=2.4))
    o.append(path(f"M{wx - 48},{wy - 128} L{wx - 12},{wy - 128} L{wx - 17},{wy - 84} L{wx - 43},{wy - 84} Z", fill=WOOD, stroke=INK, w=2.2, filt="brush"))
    o.append(path(f"M{wx - 48},{wy - 128} Q{wx - 30},{wy - 148} {wx - 12},{wy - 128}", stroke=INK, w=2))
    # a neighbour passing on the road, small
    nb, _ = ordinary(SX0 + 110, base + 130, 1.15, flip=False, tool=None, robe="#c9c4ba")
    o.append(nb)
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 150, base + 190, 14, 6, 14))
    return finish(o + [zen_rank_close()])


CARDS = {"wa01": wa01, "wa02": wa02, "wa03": wa03, "wa04": wa04, "wa05": wa05,
         "wa06": wa06, "wa07": wa07, "wa08": wa08, "wa09": wa09, "wa10": wa10,
         "wa11": wa11, "wa12": wa12, "wa13": wa13, "wa14": wa14, "wa15": wa15}
