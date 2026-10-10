"""Zen deck, minor series, suit of Fire (fi01-fi15): effort, doubt, embers and lamplight.

Built on the pattern of zen_minor_earth, whose figure helpers (withdrawn, attending, acting,
engaged, ordinary), place() and props are imported rather than copied.

Pips fi01-fi10: zen_pip_open("fire", n) draws the ensō with n pyramids, then one small vignette of
the pip's Image paragraph is drawn in the lower inside of the ensō (ZEN_VIGNETTE), then
zen_pip_close(). No dark triangle is drawn in a vignette, so the pyramid count stays readable;
tripods, roofs and stumps are drawn flat and wide.

Ranks fi11-fi15 use the hanging-scroll frame with a fuller scene, and the same figure type as the
other suits for each rank: withdrawn (First), attending (Second), acting (Third), engaged (Fourth),
ordinary (Fifth). The setting and props are those of Fire. Fire here is lamplight and embers, never
a blaze: each card has at most one vermilion accent besides the seal and rank emblems.

Helpers new to this module: flame(), brazier(), oil_lamp(), lantern(), kyosaku(), anvil(),
sparks(), hearth_ash(), _shadow() and _pillar().
"""

import math

from .common import (GREY, INK, PALE, SCROLL_BOX, VERMILION, ZEN_PAPER, ZEN_VIGNETTE,
                     f, zen_pip_close, zen_pip_open, zen_rank_close, zen_rank_open)
from .zen_minor_earth import (STRAW, WOOD, _anchor, _arm, _smoke, acting, attending, cushion,
                              engaged, floorboards, ordinary, place, withdrawn)
from .zen_minor_water import _bearer, kettle, tatami
from .zen_transmission import GREYROBE, SKIN, ellipse, finish, head, path, tube
from .zen_way import grass, ground, hills, mist, rock, trunk

SX0, SY0, SX1, SY1 = SCROLL_BOX
SCX = (SX0 + SX1) / 2
VX0, VY0, VX1, VY1 = ZEN_VIGNETTE
VCX = (VX0 + VX1) / 2
FLOOR = 725
IRON, ASH, CLAYRED = "#3b3834", "#cfcac0", "#a8958a"


# ------------------------------------------------------------ new helpers

def flame(x, y, r, bend=0.0, col=VERMILION):
    """A small teardrop flame with its base at (x, y); r is the half-width, bend leans the tip."""
    d = (f"M{f(x)},{f(y)} C{f(x - r)},{f(y - r * 0.5)} {f(x - r * 0.4 + bend * 0.4)},{f(y - r * 1.7)} {f(x + bend)},{f(y - r * 2.4)} "
         f"C{f(x + r * 0.5 + bend * 0.6)},{f(y - r * 1.5)} {f(x + r)},{f(y - r * 0.6)} {f(x)},{f(y)} Z")
    return f'<path d="{d}" fill="{col}" opacity="0.95"/>'


def hearth_ash(x, y, w, h=None, col=ASH):
    """A mound of grey ash, wide and low, resting on y."""
    h = h or w * 0.12
    return (path(f"M{f(x - w / 2)},{f(y)} Q{f(x - w * 0.25)},{f(y - h * 1.5)} {f(x)},{f(y - h)} Q{f(x + w * 0.25)},{f(y - h * 1.5)} {f(x + w / 2)},{f(y)} Z",
                 fill=col, stroke=GREY, w=1.6, filt="brush")
            + path(f"M{f(x - w * 0.3)},{f(y - h * 0.4)} q{f(w * 0.3)},{f(-h * 0.4)} {f(w * 0.55)},0", stroke="#ffffff", w=1.3, op=0.6))


def brazier(x, y, w, ash=ASH, ember=False, lit=None):
    """An iron brazier: a round pot on three short feet, standing on y, with ash in the mouth. ember adds a
    glowing red coal; lit is an optional vermilion colour for the coal."""
    h = w * 0.55
    out = [path(f"M{f(x - w * 0.36)},{f(y - h * 0.2)} l-4,{f(h * 0.2)} M{f(x + w * 0.36)},{f(y - h * 0.2)} l4,{f(h * 0.2)} M{f(x)},{f(y - h * 0.1)} l0,{f(h * 0.1)}", w=3.4),
           path(f"M{f(x - w / 2)},{f(y - h)} C{f(x - w * 0.58)},{f(y - h * 0.3)} {f(x - w * 0.3)},{f(y - h * 0.15)} {f(x)},{f(y - h * 0.15)} "
                f"C{f(x + w * 0.3)},{f(y - h * 0.15)} {f(x + w * 0.58)},{f(y - h * 0.3)} {f(x + w / 2)},{f(y - h)} Z",
                fill=IRON, stroke=INK, w=2.2, filt="brush"),
           ellipse(x, y - h, w / 2, w * 0.1, ash, stroke=INK, w=2)]
    if ember:
        out.append(ellipse(x + w * 0.05, y - h - 1, w * 0.1, w * 0.035, lit or VERMILION, op=0.95))
    return "".join(out)


def oil_lamp(x, y, s=1.0, lit=True, tip=VERMILION):
    """A dish lamp on a turned stem, standing on y; a small flame at the wick when lit."""
    out = [path(f"M{f(x - 16 * s)},{f(y)} L{f(x + 16 * s)},{f(y)}", w=3.6),
           path(f"M{f(x)},{f(y)} Q{f(x + 2 * s)},{f(y - 22 * s)} {f(x)},{f(y - 40 * s)}", w=3.6),
           path(f"M{f(x - 22 * s)},{f(y - 44 * s)} Q{f(x)},{f(y - 30 * s)} {f(x + 22 * s)},{f(y - 44 * s)} Z", fill=IRON, stroke=INK, w=2, filt="brush"),
           path(f"M{f(x + 18 * s)},{f(y - 44 * s)} l{f(6 * s)},{f(-4 * s)}", w=2.6)]
    if lit:
        out.append(ellipse(x + 22 * s, y - 56 * s, 22 * s, 24 * s, "#fff4d6", op=0.55, filt="wash"))
        out.append(flame(x + 24 * s, y - 48 * s, 3.8 * s, bend=1.5 * s, col=tip))
    return "".join(out)


def lantern(x, y, w, h, lit=True, tip=VERMILION):
    """A paper lantern hanging with its top at y: pale oval with ribs and an inner flame."""
    out = [ellipse(x, y + h / 2, w * 1.5, h * 0.8, "#fff4d6", op=0.5, filt="wash") if lit else "",
           ellipse(x, y + h / 2, w / 2, h / 2, "#f1e8cf", stroke=INK, w=2.2, filt="brush")]
    for k in (-0.55, -0.15, 0.25, 0.6):
        out.append(path(f"M{f(x - w / 2 * (1 - abs(k) ** 2 * 0.6))},{f(y + h / 2 + k * h * 0.4)} Q{f(x)},{f(y + h / 2 + k * h * 0.4 + 5)} {f(x + w / 2 * (1 - abs(k) ** 2 * 0.6))},{f(y + h / 2 + k * h * 0.4)}", stroke=GREY, w=1.2, op=0.8))
    out.append(path(f"M{f(x - w * 0.2)},{f(y)} h{f(w * 0.4)} M{f(x - w * 0.2)},{f(y + h)} h{f(w * 0.4)}", w=3))
    if lit:
        out.append(flame(x, y + h * 0.72, w * 0.1, bend=1.0, col=tip))
    return "".join(out)


def kyosaku(x0, y0, x1, y1, w=6):
    """The long flat stick of the monastery hall as a plain stroke with a darker blade end at (x1, y1)."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return (path(f"M{f(x0)},{f(y0)} L{f(x1)},{f(y1)}", stroke=INK, w=w + 2.2)
            + path(f"M{f(x0)},{f(y0)} L{f(x1)},{f(y1)}", stroke="#8a6f4a", w=w)
            + path(f"M{f(mx)},{f(my)} L{f(x1)},{f(y1)}", stroke="#6b5230", w=w - 1))


def anvil(x, y, w):
    """A smith's anvil on a log, seen from the side: a flat block with a horn to the right, top at y."""
    h = w * 0.3
    return (path(f"M{f(x - w * 0.5)},{f(y + 4)} L{f(x - w * 0.5)},{f(y + h * 0.35)} L{f(x - w * 0.28)},{f(y + h * 0.55)} L{f(x - w * 0.22)},{f(y + h * 1.5)} "
                 f"L{f(x + w * 0.22)},{f(y + h * 1.5)} L{f(x + w * 0.2)},{f(y + h * 0.55)} L{f(x + w * 0.5)},{f(y + h * 0.35)} Q{f(x + w * 0.7)},{f(y + h * 0.2)} {f(x + w * 0.75)},{f(y)} "
                 f"L{f(x - w * 0.5)},{f(y)} Z", fill=IRON, stroke=INK, w=2.4)
            + path(f"M{f(x - w * 0.45)},{f(y + 3)} L{f(x + w * 0.5)},{f(y + 3)}", stroke=GREY, w=1.5, op=0.7)
            + path(f"M{f(x - w * 0.3)},{f(y + h * 1.5)} L{f(x - w * 0.36)},{f(y + h * 4)} L{f(x + w * 0.36)},{f(y + h * 4)} L{f(x + w * 0.3)},{f(y + h * 1.5)}",
                   fill=WOOD, stroke=INK, w=2.2, op=0.9, filt="brush"))


def sparks(x, y, n, rng, span=110, rise=70, col=VERMILION):
    """A clean arc of small sparks leaving (x, y) toward the upper right."""
    out = []
    for k in range(n):
        t = (k + 1) / (n + 1)
        a = -0.2 - 1.2 * t
        r = span * (0.5 + rng.uniform(0, 0.5))
        px, py = x + r * math.cos(a) * 0.8, y + r * math.sin(a) * rise / span
        out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{rng.uniform(1.6, 2.8):.1f}" fill="{col}" opacity="{rng.uniform(0.7, 1):.2f}"/>')
        out.append(path(f"M{f(px)},{f(py)} l{f(-6 * math.cos(a))},{f(-6 * math.sin(a) * 0.6)}", stroke=col, w=1.2, op=0.6))
    return "".join(out)


def _shadow(inner, op=0.2):
    """Wrap drawing in a group of reduced opacity: a figure seen as a shadow."""
    return f'<g opacity="{op}">{inner}</g>'


def _pillar(x, y0, y1, w, op=0.35):
    """A temple pillar in grey wash with a base, tapering not at all."""
    return (path(f"M{f(x - w / 2)},{f(y0)} L{f(x + w / 2)},{f(y0)} L{f(x + w / 2)},{f(y1)} L{f(x - w / 2)},{f(y1)} Z", fill=GREY, stroke=None, op=op, filt="softwash")
            + path(f"M{f(x - w / 2)},{f(y0)} Q{f(x - w / 2 - 1)},{f((y0 + y1) / 2)} {f(x - w / 2)},{f(y1)}", stroke=GREY, w=1.4, op=0.5, filt="brush"))


# ------------------------------------------------------------ pips fi01-fi10

def fi01(rng):
    """One of Fire: a lone figure in a dark hall walks between pillars with one lit taper, the flame bent in the draught."""
    o = [zen_pip_open("fire", 1), floorboards(FLOOR - 36, FLOOR + 44, VCX - 190, VCX + 190, col="#8a8174")]
    for px, op in ((VX0 + 24, 0.5), (VX0 + 120, 0.32), (VX1 - 110, 0.32), (VX1 - 24, 0.5)):
        o.append(_pillar(px, FLOOR - 250, FLOOR - 30, 36 if op > 0.4 else 28, op))
    fig, a = _bearer(VCX - 10, FLOOR + 6, 2.2)
    o.append(fig)
    hx, hy = a["hand"]
    o.append(path(f"M{f(hx)},{f(hy)} L{f(hx + 1)},{f(hy - 34)}", stroke="#efe7cf", w=5))
    o.append(path(f"M{f(hx)},{f(hy)} L{f(hx + 1)},{f(hy - 34)}", stroke=INK, w=1.2, op=0.5))
    o.append(ellipse(hx + 8, hy - 52, 46, 50, "#fff4d6", op=0.55, filt="wash"))
    o.append(flame(hx + 1, hy - 34, 6.5, bend=14))
    for k in range(3):  # the draught
        o.append(path(f"M{f(hx + 54 + k * 12)},{f(hy - 70 + k * 18)} q22,-4 44,2", stroke=PALE, w=1.4, op=0.85))
    return finish(o + [zen_pip_close()])


def fi02(rng):
    """Two of Fire: two small braziers on a wooden floor, one with a live coal, one with grey ash and a thread of smoke; a blank scroll lies open."""
    o = [zen_pip_open("fire", 2), floorboards(FLOOR - 40, FLOOR + 50, VCX - 190, VCX + 190, rows=5)]
    o.append(brazier(VCX - 150, FLOOR + 6, 90, ash="#e4ded0", ember=True))
    o.append(brazier(VCX - 20, FLOOR + 6, 90, ash=ASH))
    o.append(_smoke(VCX - 20, FLOOR - 56, 120, 7, PALE, 1.8))
    o.append(_smoke(VCX - 150, FLOOR - 56, 40, 4, PALE, 1.4))
    bx, by = VCX + 120, FLOOR + 22
    o.append(path(f"M{bx - 70},{by - 14} L{bx + 70},{by - 18} L{bx + 74},{by + 24} L{bx - 66},{by + 28} Z", fill="#ebe4d3", stroke=INK, w=2.2, filt="brush"))
    for xx in (bx - 78, bx + 80):  # the rolled ends
        o.append(ellipse(xx, by + 5, 9, 25, "#d9d0b8", stroke=INK, w=2))
    return finish(o + [zen_pip_close()])


def fi03(rng):
    """Three of Fire: a red-hot iron ball on an anvil in a bare smithy, a smith's two hands holding it with tongs; the rest grey."""
    o = [zen_pip_open("fire", 3), ground(FLOOR + 10, VX0 + 10, VX1 - 10, op=0.16)]
    ax, ay = VCX - 40, FLOOR - 34
    bx, by, br = ax - 10, ay - 26, 21
    o.append(anvil(ax, ay, 150))
    o.append(ellipse(bx, by - 6, br * 3.0, br * 2.0, "#fff0d0", op=0.5, filt="wash"))
    o.append(f'<circle cx="{f(bx)}" cy="{f(by)}" r="{br}" fill="{VERMILION}" stroke="{INK}" stroke-width="1.4"/>')
    o.append(ellipse(bx - 6, by - 7, 7, 5, "#f3a98d", op=0.7, filt="wash"))
    # two tongs from the right, gripped by two hands
    for dy in (-10, 12):
        o.append(path(f"M{bx + br - 6},{by + dy * 0.6} L{bx + 128},{by + dy * 1.3 - 6}", stroke=INK, w=5))
    # the smith's forearms reach in from the right edge to the tong handles
    for k, (hx, hy) in enumerate(((bx + 128, by - 16), (bx + 128, by + 8))):
        sx0, sy0 = VX1 + 10, hy - 40 + k * 46
        sleeve = f"M{sx0 + 30},{sy0 + 10} Q{hx + 70},{hy - 18 + k * 20} {hx + 26},{hy}"
        o.append(path(sleeve, stroke=INK, w=30, op=0.9))
        o.append(path(sleeve, stroke="#8f877a", w=25))
        o.append(path(f"M{hx + 30},{hy - 13} l-4,26", stroke=INK, w=2.2))  # cuff
        # the hand closing on the tong handle
        o.append(ellipse(hx + 12, hy, 15, 12, SKIN, stroke=INK, w=2))
        o.append(path(f"M{hx + 4},{hy - 8} q-6,8 0,16", stroke=INK, w=1.4, op=0.7))
    o.append(path(f"M{VX0 + 10},{FLOOR + 6} Q{VCX},{FLOOR + 2} {VX1 - 10},{FLOOR + 6}", stroke=GREY, w=1.5, op=0.5, filt="brush"))
    return finish(o + [zen_pip_close()])


def fi04(rng):
    """Four of Fire: a figure kneels on a cushion with a long stick across the lap while a lamp burns ahead; behind, a second shadow lifts the stick."""
    o = [zen_pip_open("fire", 4), floorboards(FLOOR - 24, FLOOR + 46, VCX - 190, VCX + 190, col="#9a907f")]
    sh, _ = acting(VCX - 150, FLOOR - 4, 2.0, flip=False, strike=True, reach=(40, -70), robe=GREY)
    o.append(_shadow(sh, 0.2))
    o.append(cushion(VCX - 20, FLOOR + 8, 190))
    fig, a = withdrawn(VCX - 20, FLOOR - 24, 2.0, view="side", eyes_closed=False)
    o.append(fig)
    o.append(kyosaku(VCX - 60, FLOOR - 50, VCX + 70, FLOOR - 78, 6))
    o.append(oil_lamp(VCX + 150, FLOOR + 22, 1.5))
    return finish(o + [zen_pip_close()])


def fi05(rng):
    """Five of Fire: a kitchen hearth at dusk, a kettle on a hook over a small fire; a monk crouches to lay a split log, dried radishes hang above in grey."""
    o = [zen_pip_open("fire", 5), ground(FLOOR + 6, VX0 + 6, VX1 - 6, op=0.16)]
    hx, hy = VCX + 90, FLOOR + 14
    o.append(path(f"M{hx - 90},{hy} L{hx + 90},{hy} L{hx + 100},{hy + 26} L{hx - 100},{hy + 26} Z", fill=WOOD, stroke=INK, w=2.4, op=0.55, filt="brush"))
    o.append(path(f"M{hx - 70},{hy - 10} L{hx + 70},{hy - 10} L{hx + 84},{hy + 8} L{hx - 84},{hy + 8} Z", fill=IRON, stroke=INK, w=2.4, filt="brush"))
    o.append(path(f"M{hx - 40},{hy - 12} Q{hx},{hy - 22} {hx + 40},{hy - 12}", stroke=GREY, w=5, op=0.8))
    o.append(flame(hx + 4, hy - 8, 8, bend=3))
    o.append(path(f"M{hx},{FLOOR - 250} L{hx},{FLOOR - 134}", stroke="#6b5a45", w=3))  # the pot hook
    o.append(kettle(hx, hy - 60, 76, steam=True))
    # radishes strung from the beam in grey wash
    bx0, bx1, by = VX0 + 30, VCX + 40, FLOOR - 270
    o.append(path(f"M{bx0},{by} Q{(bx0 + bx1) / 2},{by + 22} {bx1},{by + 2}", stroke=INK, w=2.2, op=0.7))
    for k in range(7):
        rx = bx0 + 12 + k * ((bx1 - bx0 - 24) / 6)
        ry = by + 12 + 20 * math.sin(math.pi * (k + 0.5) / 7)
        o.append(path(f"M{f(rx)},{f(ry)} l0,{f(10)}", stroke=GREY, w=1.4, op=0.6))
        o.append(ellipse(rx, ry + 24, 5.5, 14, GREY, op=0.45, stroke=INK, w=1))
    fig, a = attending(VCX - 70, FLOOR + 10, 2.1, flip=False, seat=18, lean=34, reach=(52, -10), robe=GREYROBE)
    o.append(fig)
    hx2, hy2 = a["hands"][0]
    o.append(path(f"M{f(hx2 - 36)},{f(hy2 + 4)} L{f(hx2 + 40)},{f(hy2 - 6)}", stroke="#8a6f4a", w=9))
    o.append(path(f"M{f(hx2 + 40)},{f(hy2 - 6)} L{f(hx2 + 40)},{f(hy2 + 4)}", stroke=PALE, w=2))
    return finish(o + [zen_pip_close()])


def fi06(rng):
    """Six of Fire: a figure walks a path at dusk with a paper lantern on a pole, the flame steady, eyes on the ground ahead."""
    o = [zen_pip_open("fire", 6), ground(FLOOR - 10, VX0 + 6, VX1 - 6, op=0.18)]
    o.append(path(f"M{VX0 + 10},{FLOOR + 40} Q{VCX - 60},{FLOOR + 8} {VX1 - 20},{FLOOR - 4}", stroke="#cfc6b6", w=34, op=0.5, filt="softwash"))
    fig, a = _bearer(VCX - 40, FLOOR + 8, 2.2)
    o.append(fig)
    hx, hy = a["hand"]
    # the pole rises from the near hand to the lantern at its tip
    px, py = hx + 24, hy - 150
    o.append(path(f"M{f(hx - 4)},{f(hy + 4)} L{f(px)},{f(py)}", stroke="#6b5a45", w=4))
    o.append(lantern(px, py, 46, 60))
    for k in range(5):  # light on the ground ahead
        o.append(ellipse(VCX + 130 + k * 10, FLOOR + 14 + k * 6, 60 - k * 6, 9, "#fff4d6", op=0.22, filt="wash"))
    return finish(o + [zen_pip_close()])


def fi07(rng):
    """Seven of Fire: an empty iron stand on a cold hearth in a bare room, a few embers under the ash; through the open door a figure sits in sunlight on the veranda."""
    o = [zen_pip_open("fire", 7), floorboards(FLOOR - 40, FLOOR + 50, VX0 + 10, VCX + 50, rows=3, col="#9a907f")]
    # the door at the right: posts and a bright veranda beyond
    dx0, dx1 = VCX + 70, VX1 - 10
    o.append(path(f"M{dx0},{FLOOR - 190} L{dx1},{FLOOR - 190} L{dx1},{FLOOR - 36} L{dx0},{FLOOR - 36} Z", fill="#fff8e4", stroke=INK, w=3, op=0.9, filt="brush"))
    o.append(ellipse((dx0 + dx1) / 2, FLOOR - 20, 90, 18, "#fff4c9", op=0.8, filt="wash"))
    o.append(path(f"M{dx0},{FLOOR - 26} L{dx1},{FLOOR - 26}", stroke=GREY, w=2, op=0.7, filt="brush"))
    fig, _ = withdrawn((dx0 + dx1) / 2 + 4, FLOOR - 26, 1.15, view="back", robe="#b3ad9f")
    o.append(fig)
    # the cold hearth and the empty stand (a ring on short legs, low and wide)
    cx, cy = VX0 + 120, FLOOR + 20
    o.append(path(f"M{cx - 100},{cy - 8} L{cx + 100},{cy - 8} L{cx + 112},{cy + 24} L{cx - 112},{cy + 24} Z", fill=IRON, stroke=INK, w=2.6, filt="brush"))
    o.append(path(f"M{cx - 82},{cy - 4} L{cx + 82},{cy - 4} L{cx + 94},{cy + 14} L{cx - 94},{cy + 14} Z", fill="#8a867e", stroke=None))
    o.append(hearth_ash(cx, cy + 10, 150, 12, col=ASH))
    for lx in (-52, 0, 52):
        o.append(path(f"M{cx + lx * 0.9},{cy - 56} L{cx + lx},{cy + 2}", stroke=INK, w=4))
    o.append(ellipse(cx, cy - 56, 68, 8, "none", stroke=INK, w=4.4))
    o.append(path(f"M{cx - 66},{cy - 56} Q{cx},{cy - 50} {cx + 66},{cy - 56}", stroke=GREY, w=1.5, op=0.7))
    for k in range(3):  # a few embers in the ash
        o.append(f'<circle cx="{f(cx - 14 + k * 16)}" cy="{f(cy + 4 + (k % 2) * 3)}" r="2.8" fill="{VERMILION}" opacity="0.9"/>')
    return finish(o + [zen_pip_close()])


def fi08(rng):
    """Eight of Fire: a bare hearth drawn as an empty ring of ash on blank paper; one thin grey thread of smoke leaves the centre and dissolves."""
    o = [zen_pip_open("fire", 8)]
    cx, cy = VCX, FLOOR - 4
    o.append(ellipse(cx, cy, 150, 36, "none", stroke=GREY, w=10, op=0.75, filt="dry"))
    o.append(ellipse(cx, cy, 150, 36, "none", stroke=ASH, w=5, op=0.9))
    o.append(ellipse(cx, cy + 4, 124, 26, "#e4ded0", op=0.5, filt="softwash"))
    o.append(path(f"M{cx},{cy} C{cx + 14},{cy - 50} {cx - 16},{cy - 100} {cx + 8},{cy - 150} C{cx + 18},{cy - 176} {cx - 4},{cy - 196} {cx + 6},{cy - 214}", stroke=GREY, w=2, op=0.75))
    return finish(o + [zen_pip_close()])


def fi09(rng):
    """Nine of Fire: a mountain stream under a rising sun, fresh red maples on the bank in faint wash, a burnt stump in front with a green shoot."""
    o = [zen_pip_open("fire", 9)]
    hy = FLOOR - 120
    o.append(ellipse(VCX + 60, hy - 6, 62, 62, "#f6e2c4", op=0.8, filt="wash"))
    o.append(ellipse(VCX + 60, hy - 6, 40, 40, "#f1d3ae", op=0.9, filt="wash"))
    o.append(hills(rng, [(hy + 6, 22, PALE, 0.35, 80), (hy + 30, 16, GREY, 0.18, 60)], VX0 + 6, VX1 - 6))
    o.append(path(f"M{VX0 + 6},{hy + 24} Q{VCX},{hy + 18} {VX1 - 6},{hy + 24} L{VX1 - 6},{FLOOR + 60} L{VX0 + 6},{FLOOR + 60} Z", fill="#d9e0df", stroke=None, op=0.0))
    # the stream: two dry-brush banks narrowing toward the hills, unpainted water between them
    left = f"M{VCX - 6},{hy + 30} C{VCX + 40},{hy + 80} {VCX - 90},{FLOOR - 30} {VCX - 50},{FLOOR + 52}"
    right = f"M{VCX + 18},{hy + 30} C{VCX + 80},{hy + 80} {VCX + 40},{FLOOR - 30} {VCX + 100},{FLOOR + 52}"
    o.append(path(left + f" L{VCX + 100},{FLOOR + 52} C{VCX + 40},{FLOOR - 30} {VCX + 80},{hy + 80} {VCX + 18},{hy + 30} Z",
                  fill="#c9d2d2", stroke=None, op=0.55, filt="softwash"))
    o.append(path(left, stroke=INK, w=2.2, op=0.75, filt="dry"))
    o.append(path(right, stroke=INK, w=2.2, op=0.75, filt="dry"))
    for k in range(5):  # flow lines, longer as the stream comes nearer
        y_ = hy + 60 + k * 26
        o.append(path(f"M{VCX - 20 + k * 3},{y_} q{14 + k * 6},-3 {28 + k * 12},1", stroke=GREY, w=1.3, op=0.6, filt="brush"))
    # maple on the right bank
    mx = VX1 - 110
    o.append(path(f"M{mx},{hy + 40} Q{mx - 6},{hy - 10} {mx + 8},{hy - 70}", stroke=INK, w=5, filt="brush"))
    o.append(path(f"M{mx + 4},{hy - 20} q30,-20 60,-24 M{mx + 2},{hy - 40} q-30,-16 -50,-20", stroke=INK, w=3, filt="brush"))
    for _ in range(14):
        lx, ly = mx + rng.uniform(-60, 70), hy - 20 - rng.uniform(0, 90)
        o.append(f'<path d="M{f(lx)},{f(ly)} l9,-3 l-3,9 z" fill="{VERMILION}" opacity="0.55" transform="rotate({rng.uniform(0, 360):.0f} {f(lx)} {f(ly)})"/>')
    o.append(ground(FLOOR + 6, VX0 + 6, VX1 - 6, op=0.12))
    # burnt stump at the left, with a green shoot
    sx, sy = VX0 + 100, FLOOR + 30
    o.append(path(f"M{sx - 34},{sy} L{sx - 28},{sy - 52} L{sx - 14},{sy - 44} L{sx - 6},{sy - 66} L{sx + 8},{sy - 50} L{sx + 20},{sy - 60} L{sx + 32},{sy - 40} L{sx + 38},{sy} Z",
                  fill=IRON, stroke=INK, w=2.4, filt="brush"))
    o.append(path(f"M{sx - 20},{sy - 20} l2,-18 M{sx + 14},{sy - 12} l-2,-22", stroke=GREY, w=1.5, op=0.6))
    o.append(path(f"M{sx + 4},{sy - 62} Q{sx + 2},{sy - 90} {sx + 14},{sy - 108}", stroke="#7e9a62", w=3))
    o.append(path(f"M{sx + 12},{sy - 104} q20,-14 30,2 q-14,10 -30,-2 Z M{sx + 6},{sy - 90} q-20,-12 -28,2 q14,10 28,-2 Z", fill="#9db384", stroke="#6b8751", w=1.4))
    o.append(grass(rng, VX0 + 20, VX1 - 20, FLOOR + 30, FLOOR + 56, 22, 8, 22))
    return finish(o + [zen_pip_close()])


def fi10(rng):
    """Ten of Fire: a village street at night with a charcoal seller's brazier at a corner; a stranger in a worn robe warms both palms beside a labourer and a child."""
    o = [zen_pip_open("fire", 10), ground(FLOOR - 4, VX0 + 6, VX1 - 6, op=0.2)]
    wy = FLOOR - 150
    o.append(path(f"M{VX0 + 6},{wy - 48} L{VX1 - 6},{wy - 48} L{VX1 - 6},{FLOOR - 6} L{VX0 + 6},{FLOOR - 6} Z", fill=GREY, stroke=None, op=0.28, filt="softwash"))
    o.append(path(f"M{VX0 + 6},{wy - 48} L{VX1 - 6},{wy - 48}", stroke=INK, w=4, op=0.7, filt="brush"))
    for k in range(6):
        o.append(path(f"M{VX0 + 30 + k * 66},{wy - 44} l0,{f(60)}", stroke=GREY, w=1.5, op=0.5))
    bx, by = VCX + 10, FLOOR + 14
    o.append(ellipse(bx, by - 30, 96, 52, "#fff0d0", op=0.45, filt="wash"))
    o.append(brazier(bx, by, 96, ash="#59544c", ember=True))
    # stranger at left, both hands held over the coals
    fig, a = acting(bx - 100, FLOOR - 4, 1.7, flip=False, strike=False, reach=(60, -40), robe=SKIN)
    o.append(fig)
    lab, _ = ordinary(bx + 160, FLOOR - 4, 1.75, flip=True, tool=None, robe="#a9a398")
    o.append(lab)
    kid, _ = ordinary(bx + 84, FLOOR + 8, 1.1, flip=True, tool=None, robe="#c9c4ba")
    o.append(kid)
    # a basket of charcoal at the corner
    o.append(path(f"M{VX0 + 14},{FLOOR - 40} L{VX0 + 80},{FLOOR - 40} L{VX0 + 70},{FLOOR + 14} L{VX0 + 24},{FLOOR + 14} Z", fill=STRAW, stroke=INK, w=2.2, filt="brush"))
    for k in range(5):
        o.append(ellipse(VX0 + 28 + k * 11, FLOOR - 44 + (k % 2) * 3, 7, 5, IRON))
    return finish(o + [zen_pip_close()])


# ------------------------------------------------------------ ranks fi11-fi15

def fi11(rng):
    """First Rank of Fire: a seated monk beside a dead fire, hands in his sleeves, face turned from it; grey ash and one cooled ember at the foot."""
    o = [zen_rank_open("fire", 1)]
    base = SY1 - 160
    wy = base - 620
    o.append(path(f"M{SX0},{wy} L{SX1},{wy} L{SX1},{base + 30} L{SX0},{base + 30} Z", fill="#e4ded0", stroke=None, op=0.4, filt="softwash"))
    # a ceiling beam, and a tall window at the right with a lattice
    o.append(path(f"M{SX0 + 4},{wy + 20} L{SX1 - 4},{wy + 22}", stroke=INK, w=9, op=0.7, filt="brush"))
    wx0, wx1, wyt, wyb = SX1 - 200, SX1 - 70, wy + 140, wy + 360
    o.append(path(f"M{wx0},{wyt} L{wx1},{wyt} L{wx1},{wyb} L{wx0},{wyb} Z", fill="#f3eddc", stroke=INK, w=3.2, filt="brush"))
    for k in (1, 2):
        o.append(path(f"M{wx0 + (wx1 - wx0) * k / 3},{wyt} L{wx0 + (wx1 - wx0) * k / 3},{wyb}", stroke=INK, w=1.6, op=0.7))
    for k in (1, 2, 3):
        o.append(path(f"M{wx0},{wyt + (wyb - wyt) * k / 4} L{wx1},{wyt + (wyb - wyt) * k / 4}", stroke=INK, w=1.6, op=0.7))
    o.append(floorboards(base - 30, base + 130, SX0 + 20, SX1 - 20, rows=5, col="#a79e8f"))
    # the dead hearth at left: a sunken square of grey ash under an empty hook on a long chain
    hx, hy = SCX - 110, base + 60
    o.append(path(f"M{hx - 100},{hy - 16} L{hx + 100},{hy - 16} L{hx + 120},{hy + 30} L{hx - 120},{hy + 30} Z", fill=IRON, stroke=INK, w=3, filt="brush"))
    o.append(path(f"M{hx - 80},{hy - 8} L{hx + 80},{hy - 8} L{hx + 98},{hy + 20} L{hx - 98},{hy + 20} Z", fill=ASH, stroke=GREY, w=1.5, op=0.95))
    o.append(hearth_ash(hx, hy + 8, 120, 14, col="#bdb8ae"))
    o.append(path(f"M{hx + 8},{wy + 24} L{hx + 8},{hy - 150} q12,10 -2,24", stroke=GREY, w=3, op=0.75))
    for k in range(3):
        o.append(path(f"M{hx - 50 + k * 40},{hy + 18} q10,-4 22,0", stroke="#ffffff", w=1.4, op=0.6))
    # the cooled ember at the foot of the hearth
    o.append(f'<ellipse cx="{f(hx + 130)}" cy="{f(hy + 40)}" rx="8" ry="5.5" fill="{VERMILION}" opacity="0.88"/>')
    # the monk, turned away from the fire, facing right, hands tucked into his sleeves
    fig, a = withdrawn(SCX + 110, base + 60, 3.0, view="side", robe="#b3ad9f")
    o.append(fig)
    return finish(o + [zen_rank_close()])


def fi12(rng):
    """Second Rank of Fire: a cook in an apron crouched at a stove, his face lit by a small fire; utensils hang on the wall in loose ink, the flame the only colour."""
    o = [zen_rank_open("fire", 2)]
    base = SY1 - 140
    wy = base - 520
    o.append(path(f"M{SX0},{wy - 40} L{SX1},{wy - 40} L{SX1},{base + 20} L{SX0},{base + 20} Z", fill="#e4ded0", stroke=None, op=0.45, filt="softwash"))
    # a rail with hanging utensils in loose ink, drawn in local units from the rail's left end
    u = [path("M0,0 L300,2", stroke=INK, w=4, op=0.8, filt="brush")]
    ux = 36
    for kind in ("ladle", "pan", "whisk", "spoon", "pot"):
        u.append(path(f"M{ux},0 l0,22", stroke=GREY, w=2))
        if kind == "ladle":
            u.append(path(f"M{ux},22 l0,70", stroke=INK, w=3, op=0.8))
            u.append(f'<path d="M{ux - 14},92 q14,22 28,0 z" fill="{GREY}" stroke="{INK}" stroke-width="2" opacity="0.8"/>')
        elif kind == "pan":
            u.append(path(f"M{ux},22 l0,40", stroke=INK, w=3, op=0.8))
            u.append(ellipse(ux, 90, 26, 28, GREY, stroke=INK, w=2.2, op=0.75, filt="brush"))
        elif kind == "whisk":
            u.append(path(f"M{ux},22 l0,36", stroke=INK, w=3, op=0.8))
            for k in range(-2, 3):
                u.append(path(f"M{ux},58 q{k * 6},18 {k * 9},44", stroke=GREY, w=1.5))
        elif kind == "spoon":
            u.append(path(f"M{ux},22 l0,84", stroke=INK, w=3, op=0.8))
            u.append(ellipse(ux, 114, 8, 14, GREY, stroke=INK, w=2, op=0.8))
        else:
            u.append(path(f"M{ux - 24},22 Q{ux},8 {ux + 24},22", stroke=INK, w=2, op=0.7))
            u.append(path(f"M{ux - 22},58 L{ux - 18},112 L{ux + 18},112 L{ux + 22},58 Z", fill=GREY, stroke=INK, w=2.2, op=0.75, filt="brush"))
        ux += 56
    o.append(place(SX0 + 36, wy + 16, 1.4, False, "".join(u)))
    o.append(floorboards(base - 10, base + 130, SX0 + 20, SX1 - 20, rows=5, col="#a79e8f"))
    # stove: a clay block with a mouth, kettle on top, small fire inside (local units, scaled)
    sx, sy, k = SCX + 60, base + 36, 1.25
    st = [path("M-90,-100 L90,-100 L100,26 L-100,26 Z", fill=CLAYRED, stroke=INK, w=3, filt="brush"),
          path("M-100,-100 L100,-100", stroke=INK, w=5, filt="brush"),
          path("M-46,22 L-46,-34 Q0,-70 46,-34 L46,22 Z", fill=IRON, stroke=INK, w=2.6, filt="brush"),
          ellipse(0, -6, 70, 40, "#fff0d0", op=0.35, filt="wash"),
          flame(0, 12, 11, bend=4),
          path("M-26,14 L28,8", stroke="#8a6f4a", w=6),
          kettle(0, -100, 84, steam=True)]
    o.append(place(sx, sy, k, False, "".join(st)))
    # the cook, crouched, face to the fire, in an apron
    cx, cy, cs = sx - 170, base + 36, 2.7
    fig, a = attending(cx, cy, cs, flip=False, seat=18, lean=28, reach=(62, -30), robe=GREYROBE)
    o.append(fig)
    o.append(path(f"M{cx + 10},{cy - 30 * cs * 0.55} L{cx + 62 * cs * 0.85},{cy - 24 * cs * 0.55} L{cx + 58 * cs * 0.85},{cy - 4} L{cx + 6},{cy - 6} Z", fill="#e9e2d0", stroke=INK, w=1.8, op=0.0))
    o.append(path(f"M{SX0 + 14},{base + 24} Q{SCX},{base + 18} {SX1 - 14},{base + 26}", stroke=GREY, w=1.5, op=0.6, filt="brush"))
    return finish(o + [zen_rank_close()])


def fi13(rng):
    """Third Rank of Fire: a smith at the moment of striking, face calm and arm loose, sparks leaving the anvil in a clean arc; a bare forge behind."""
    o = [zen_rank_open("fire", 3)]
    base = SY1 - 140
    top = base - 600
    o.append(path(f"M{SX0},{top} L{SX1},{top} L{SX1},{base + 30} L{SX0},{base + 30} Z", fill="#d8d2c6", stroke=None, op=0.4, filt="softwash"))
    # the forge: a stone hearth block at left with a chimney drawn as flat blocks
    fx, fy = SX0 + 100, base
    o.append(path(f"M{fx - 80},{fy - 130} L{fx + 80},{fy - 130} L{fx + 80},{fy + 30} L{fx - 80},{fy + 30} Z", fill="#8f877a", stroke=INK, w=3, op=0.75, filt="brush"))
    o.append(path(f"M{fx - 56},{fy - 118} L{fx + 56},{fy - 118} L{fx + 56},{fy - 30} L{fx - 56},{fy - 30} Z", fill=IRON, stroke=INK, w=2.4, op=0.9, filt="brush"))
    o.append(path(f"M{fx - 34},{top + 40} L{fx + 34},{top + 40} L{fx + 34},{fy - 130} L{fx - 34},{fy - 130} Z", fill="#8f877a", stroke=INK, w=3, op=0.5, filt="brush"))
    o.append(path(f"M{fx - 44},{top + 40} L{fx + 44},{top + 40}", stroke=INK, w=5, filt="brush"))
    o.append(path(f"M{fx - 90},{fy - 76} l180,0", stroke=GREY, w=1.6, op=0.5))
    # tools on the wall: hanging tongs and hammers as plain strokes
    for k, tx in enumerate((SCX + 30, SCX + 90, SCX + 150)):
        o.append(path(f"M{tx},{top + 80} l0,{110 - k * 14}", stroke=INK, w=3, op=0.6))
        o.append(path(f"M{tx - 16},{top + 190 - k * 14} l32,0", stroke=INK, w=6, op=0.6))
    o.append(ground(base + 28, SX0, SX1, op=0.22))
    sx, ss = SCX - 30, 3.0
    fig, a = acting(sx, base + 30, ss, flip=False, strike=True, reach=(46, -64), robe=SKIN)
    o.append(fig)
    hx, hy = a["hands"][0]
    ax, ay = hx + 8, hy + 22
    o.append(ellipse(ax + 10, ay - 20, 70, 36, "#fff0d0", op=0.4, filt="wash"))
    o.append(anvil(ax, ay, 118))
    o.append(path(f"M{f(hx - 6)},{f(ay - 5)} L{f(ax + 40)},{f(ay - 5)}", stroke=IRON, w=8))
    o.append(path(f"M{f(hx - 6)},{f(ay - 5)} L{f(hx - 60)},{f(ay - 24)}", stroke=INK, w=5))  # tongs
    o.append(sparks(ax + 30, ay - 12, 10, rng, 100, 110))
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 60, base + 110, 22, 8, 22))
    return finish(o + [zen_rank_close()])


def fi14(rng):
    """Fourth Rank of Fire: a woman at a pottery kiln tends the firebox with a long iron rake while a child hands her wood; smoke rises into a pale sky; a thin red line marks the glow."""
    o = [zen_rank_open("fire", 4)]
    base = SY1 - 140
    hor = base - 470
    o.append(hills(rng, [(hor + 10, 40, PALE, 0.25, 80)], SX0 + 4, SX1 - 4))
    o.append(ground(base - 20, SX0, SX1, op=0.18))
    # the kiln: a long low dome with a chimney and a firebox mouth at the front (local units, scaled)
    kx, ky, k = SX0 + 150, base + 10, 1.1
    kn = [path("M-130,0 C-130,-160 110,-160 110,0 Z", fill=CLAYRED, stroke=INK, w=3, op=0.9, filt="brush")]
    for j in range(4):
        kn.append(path(f"M{-110 + j * 8},{-40 - j * 28} Q-10,{-62 - j * 28} {90 - j * 8},{-40 - j * 28}", stroke=GREY, w=1.4, op=0.55))
    kn.append(path("M64,-130 L94,-130 L94,-40 L64,-40 Z", fill=CLAYRED, stroke=INK, w=2.6, filt="brush"))
    kn.append(path("M58,-134 L100,-134", stroke=INK, w=5))
    kn.append(path("M-70,0 L-70,-44 Q-40,-66 -10,-44 L-10,0 Z", fill=IRON, stroke=INK, w=2.6, filt="brush"))
    kn.append(path("M-62,-10 L-18,-10", stroke=VERMILION, w=3.4))
    o.append(place(kx, ky, k, False, "".join(kn)))
    for j in range(3):
        o.append(_smoke(kx + (80 + j * 6) * k, ky - (140 + j * 10) * k, 420 - j * 60, 18 if j % 2 else -18, PALE, 2.8))
    # the woman on a stump, turned toward the child, rake laid back toward the firebox
    ws, wx, wb = 2.3, SCX + 30, base + 40
    fig, a = engaged(wx, wb, ws, flip=False, hat=False, tool=None, seat="stump")
    o.append(fig)
    lx, ly = wx - 8 * ws, wb - 48 * ws
    fx, fy = kx - 30 * k, ky - 6 * k
    o.append(path(f"M{f(lx)},{f(ly)} L{f(fx)},{f(fy)}", stroke=IRON, w=4))
    o.append(path(f"M{f(fx)},{f(fy)} l-16,-12 M{f(fx)},{f(fy)} l-8,-18 M{f(fx)},{f(fy)} l-20,-2", stroke=IRON, w=3))
    # the child offering a split log
    hx, hy = a["hands"][0]
    kid, ka = ordinary(hx + 56, wb, 1.4, flip=True, tool=None, robe="#c9c4ba")
    o.append(kid)
    kh = (hx + 56 - 22 * 1.4, wb - 58 * 1.4)
    o.append(tube(f"M{f(hx + 56 - 4 * 1.4)},{f(wb - 66 * 1.4)} Q{f(kh[0] + 4)},{f(kh[1] + 20)} {f(kh[0])},{f(kh[1])}", 5, SKIN))
    # a short split log held out, with a gap before the woman's hand
    lgx, lgy = kh[0] - 4, kh[1] + 2
    o.append(path(f"M{f(lgx)},{f(lgy)} L{f(lgx - 46)},{f(lgy - 10)}", stroke="#8a6f4a", w=11))
    o.append(ellipse(lgx - 46, lgy - 10, 5, 6, "#c9b894", stroke=INK, w=1.2))
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 60, base + 120, 26, 8, 22))
    return finish(o + [zen_rank_close()])


def fi15(rng):
    """Fifth Rank of Fire: an old woman sweeping a temple yard in the evening, a small fire of fallen leaves glowing beside her, its smoke a thin grey line."""
    o = [zen_rank_open("fire", 5)]
    base = SY1 - 140
    o.append(mist(SCX, base - 420, 340, 40, 0.5))
    # the temple hall in wash: a flat wall with eaves, posts and a dark doorway
    wy = base - 150
    o.append(path(f"M{SX0 + 20},{wy - 260} L{SX1 - 20},{wy - 260} L{SX1 - 20},{wy} L{SX0 + 20},{wy} Z", fill="#d8d2c6", stroke=None, op=0.4, filt="softwash"))
    o.append(path(f"M{SX0 + 10},{wy - 264} L{SX1 - 10},{wy - 264}", stroke=INK, w=6, op=0.6, filt="brush"))
    o.append(path(f"M{SX0 + 30},{wy - 300} L{SX1 - 30},{wy - 300}", stroke=GREY, w=3, op=0.4, filt="brush"))
    for px in (SX0 + 50, SX0 + 160, SCX + 30, SX1 - 130, SX1 - 50):
        o.append(path(f"M{px},{wy - 260} Q{px + 2},{wy - 130} {px},{wy}", stroke=INK, w=6, op=0.55, filt="dry"))
    o.append(path(f"M{SX0 + 20},{wy} Q{SCX},{wy - 6} {SX1 - 20},{wy + 2}", stroke=GREY, w=1.8, op=0.6, filt="brush"))
    o.append(trunk(rng, SX1 - 60, base - 20, base - 520, 14, -10, leafy=3))
    o.append(ground(base - 50, SX0, SX1, op=0.2))
    fig, a = ordinary(SCX - 80, base + 50, 3.0, flip=False)
    o.append(fig)
    # the small fire of leaves, a low heap with one ember glow and a thread of smoke
    fx, fy = SCX + 130, base + 80
    o.append(hearth_ash(fx, fy, 110, 16, col="#bdb8ae"))
    for _ in range(18):
        lx, ly = fx + rng.gauss(0, 22), fy - rng.uniform(2, 14)
        sz = rng.uniform(5, 8)
        o.append(f'<path d="M{f(lx)},{f(ly)} l{f(sz)},{f(-sz * 0.4)} l{f(-sz * 0.3)},{f(sz)} z" fill="{rng.choice([GREY, PALE, INK])}" opacity="{rng.uniform(0.5, 0.85):.2f}"/>')
    o.append(ellipse(fx, fy - 8, 34, 14, "#fff0d0", op=0.45, filt="wash"))
    o.append(flame(fx + 2, fy - 8, 8, bend=2))
    o.append(path(f"M{fx + 4},{fy - 34} C{fx + 20},{fy - 100} {fx - 14},{fy - 160} {fx + 8},{fy - 250} C{fx + 18},{fy - 300} {fx - 4},{fy - 340} {fx + 10},{fy - 400}", stroke=GREY, w=2.4, op=0.75))
    for hx, hy, n in [(SX0 + 80, base + 70, 8), (SX0 + 170, base + 130, 6), (SX1 - 80, base + 130, 5)]:
        for _ in range(n):
            lx, ly = hx + rng.gauss(0, 14), hy + rng.gauss(0, 4)
            sz = rng.uniform(5, 8)
            o.append(f'<path d="M{f(lx)},{f(ly)} l{f(sz)},{f(-sz * 0.4)} l{f(-sz * 0.3)},{f(sz)} z" fill="{rng.choice([GREY, PALE, INK])}" opacity="{rng.uniform(0.5, 0.85):.2f}"/>')
    o.append(grass(rng, SX0 + 10, SX1 - 10, base + 150, base + 190, 14, 6, 14))
    return finish(o + [zen_rank_close()])


CARDS = {"fi01": fi01, "fi02": fi02, "fi03": fi03, "fi04": fi04, "fi05": fi05,
         "fi06": fi06, "fi07": fi07, "fi08": fi08, "fi09": fi09, "fi10": fi10,
         "fi11": fi11, "fi12": fi12, "fi13": fi13, "fi14": fi14, "fi15": fi15}
