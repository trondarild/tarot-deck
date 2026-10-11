"""Pessimist deck, minor series, suit of Anchoring (an01-an14): the fixing of a point to hold the mind.

Same engine, line and hatching as the Isolation suit (imported from pess_minor_isolation); the wash,
sky, shadow and dark-mass colour is caput mortuum (WASH["caput"], a violet-brown) in place of slate,
set for each card by the suit_colour decorator.

Pips an01-an10: pess_pip_open("anchoring", n) draws the plate with a frieze of n anchors; the scene of the
card's Image paragraph is drawn below it. No anchor is drawn in a scene, so the count stays readable.
Courts an11-an14: pess_court_open("anchoring", age) counts the age in anchors, then the scene of the
Figure paragraph, with child(), youth(), adult() or elder() as the main figure.

New helpers in this module: ground(), rope(), tag_card(), stag(), banner(), pew_row(), notice_wall(),
gilt_frame(), shard() and chain().
"""

import math

from . import pess_minor_isolation as iso
from .common import (IMAGE_BOX, PESS_PAPER, PESS_VIGNETTE, WASH, f, pess_court_close, pess_court_open,
                     pess_pip_close, pess_pip_open, svg)
from .pess_awakening import PAPER_FILL, ellipse_pts
from .pess_minor_isolation import (BONE, CONTRAST, INK, Plate, adult, book, candle, cast, chair_side, child,
                                   clip_close, clip_open, cup, curtain, elder, fade, floor_band, floor_shadow,
                                   glow, grass, hand_dot, mass, rect, sky, slate, suit_colour, table_front,
                                   table_lamp, vignette, wall, window, youth, _boost)

CAPUT = WASH["caput"]
IX0, IY0, IX1, IY1 = IMAGE_BOX
VX0, VY0, VX1, VY1 = PESS_VIGNETTE
suit = suit_colour(CAPUT)


def _pip(n, tag, rng):
    E = Plate(rng, tag)
    E.add(pess_pip_open("anchoring", n))
    return E


def _court(age, tag, rng):
    E = Plate(rng, tag)
    E.add(pess_court_open("anchoring", age))
    return E


def _end(E, close, vig=True, top=VY0, **kw):
    if vig:
        vignette(E, top=top, **kw)
    return svg(E.done() + close, PESS_PAPER)


# ------------------------------------------------------------------ new helpers

def ground(E, hor, op=0.6, x0=IX0, x1=IX1, y1=IY1, gap=4.0, grow=1.04):
    """Open ground below a horizon: fine horizontal lines widening toward the viewer under a graded wash."""
    r = E.rng
    d, yy, g = [], hor + 6, gap
    while yy < y1 + 10:
        d.append(f"M{x0},{f(yy)} L{x1},{f(yy + r.uniform(-1, 1))}")
        yy += g
        g *= grow
    E.add(f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width="0.6" opacity="0.4" fill="none"/>')
    fade(E, x0, hor, x1, y1, op=op, side="b", reach=1.0)
    E.line([(x0, hor), (x1, hor)], w=1.2, smooth=False, op=0.8)


def rope(E, p0, p1, sag=18, w=1.6, n=14, op=1.0):
    """A cord from p0 to p1 hanging in a shallow curve; returns the points along it."""
    pts = []
    for k in range(n + 1):
        t = k / n
        pts.append((p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t + sag * 4 * t * (1 - t)))
    E.line(pts, w=w, op=op)
    return pts


def tag_card(E, x, y, w=14, h=20, rot=0, tone=0.0):
    """A small paper tag hung from (x, y) with a string hole, no writing."""
    E.add(f'<g transform="rotate({rot} {f(x)} {f(y)})">')
    E.shape([(x - w / 2, y + 4), (x + w / 2, y + 4), (x + w / 2, y + h), (x - w / 2, y + h)], smooth=False, tone=tone, sw=1.2)
    E.add(f'<circle cx="{f(x)}" cy="{f(y + 8)}" r="1.6" fill="{INK}"/>')
    E.line([(x, y), (x, y + 4)], w=0.9, smooth=False)
    E.add("</g>")


def stag(E, x, base, s=1.0, fd=-1):
    """A stag in profile, head raised toward fd. Returns the antler points (tips and tine ends) for ribbons."""
    for lx, tone in ((x + 62 * s, 0.35), (x - 70 * s, 0.35), (x + 40 * s, 0.1), (x - 90 * s, 0.1)):
        E.limb([(lx, base - 140 * s), (lx + 5 * s, base - 72 * s), (lx - 2 * s, base - 8 * s)], 15 * s, tone=tone, taper=True)
        E.shape([(lx - 9 * s, base - 12 * s), (lx + 9 * s, base - 12 * s), (lx + 10 * s, base), (lx - 10 * s, base)],
                smooth=False, hatches=[(80, 1.9, 0.85)], sw=1.2)
    body = ellipse_pts(x, base - 172 * s, 98 * s, 46 * s, 22)
    E.shape(body, hatches=[(70, 3.4, 0.4), (-45, 4, 0.3, (x, base - 235 * s, x + 120 * s, base - 120 * s))], sw=2)
    fade(E, x - 98 * s, base - 220 * s, x + 98 * s, base - 126 * s, op=0.55, side="r" if fd == -1 else "l", reach=1.0, clip=body)
    E.shape([(x - fd * 94 * s, base - 192 * s), (x - fd * 118 * s, base - 206 * s), (x - fd * 110 * s, base - 168 * s)], smooth=False, sw=1.3)
    hx, hy = x + fd * 124 * s, base - 336 * s
    neck = [(x + fd * 30 * s, base - 214 * s), (hx - fd * 16 * s, hy - 6 * s), (hx + fd * 12 * s, hy + 26 * s),
            (x + fd * 84 * s, base - 150 * s), (x + fd * 40 * s, base - 140 * s)]
    E.shape(neck, smooth=False, hatches=[(70, 3.2, 0.42), (-48, 3.8, 0.3)], sw=1.9)
    head = [(hx - fd * 16 * s, hy - 16 * s), (hx + fd * 22 * s, hy - 18 * s), (hx + fd * 58 * s, hy + 20 * s),
            (hx + fd * 56 * s, hy + 38 * s), (hx + fd * 22 * s, hy + 34 * s), (hx - fd * 12 * s, hy + 20 * s)]
    E.shape(head, hatches=[(60, 3, 0.4)], sw=1.8)
    E.shape(ellipse_pts(hx + fd * 54 * s, hy + 30 * s, 5 * s, 4 * s, 8), fill=INK, outline=False)
    E.add(f'<circle cx="{f(hx + fd * 14 * s)}" cy="{f(hy + 2 * s)}" r="{f(3 * s)}" fill="{INK}"/>')
    E.shape([(hx - fd * 8 * s, hy - 14 * s), (hx - fd * 30 * s, hy - 30 * s), (hx - fd * 20 * s, hy)], smooth=False, sw=1.2)
    pts = []
    for off in (0, 16):
        ox, oy = hx - fd * (2 + off) * s, hy - 16 * s - off * 0.25 * s
        beam = [(ox, oy), (ox - fd * 18 * s, oy - 52 * s), (ox - fd * 26 * s, oy - 112 * s), (ox - fd * 18 * s, oy - 176 * s)]
        E.line(beam, w=5.5 * s, smooth=True)
        E.line(beam, w=1.6, smooth=True, op=0.9, color=PAPER_FILL)
        for k, (bx, by) in enumerate(beam[1:], start=1):
            tx, ty = bx + fd * (26 - 4 * k) * s, by - (30 - 4 * k) * s
            E.line([(bx, by), (tx, ty)], w=3.6 * s, smooth=False)
            pts.append((tx, ty))
        pts.append(beam[-1])
    return pts


def kneeler(E, x, yb, s, hair, tone=0.6, shawl=False):
    """A kneeling person seen from behind, head bowed between the shoulders; yb is the pew line."""
    sh = [(x - 38 * s, yb), (x - 36 * s, yb - 56 * s), (x - 22 * s, yb - 74 * s), (x + 22 * s, yb - 74 * s), (x + 36 * s, yb - 56 * s),
          (x + 38 * s, yb)]
    E.shape(sh, smooth=False, hatches=[(70, 3.4 - 1.2 * tone, 0.4 + 0.3 * tone), (-48, 3.8, 0.3 + 0.3 * tone)], sw=1.8)
    fade(E, x - 38 * s, yb - 74 * s, x + 38 * s, yb, op=0.4 + 0.4 * tone, side="l", reach=0.95, clip=sh)
    if shawl:
        E.shape([(x - 34 * s, yb - 60 * s), (x, yb - 40 * s), (x + 34 * s, yb - 60 * s), (x + 22 * s, yb - 74 * s), (x - 22 * s, yb - 74 * s)],
                smooth=False, hatches=[(20, 2.6, 0.5)], sw=1.3)
    hd = ellipse_pts(x, yb - 88 * s, 21 * s, 23 * s, 14)
    dark = hair != "white"
    E.shape(hd, fill=iso.DARK if dark else PAPER_FILL, hatches=[(62, 1.9, 0.85), (-38, 2.2, 0.65)] if dark else [(70, 3.4, 0.35)], sw=1.6)


def board(E, x0, x1, top, h, tone=0.2):
    """The top board of a pew, a hatched slab with an edge line, graded darker toward the floor."""
    rect(E, x0, top, x1, top + h, hatches=[(0, 3.2, 0.38)], tone=tone, sw=2)
    fade(E, x0, top, x1, top + h, op=0.55, side="b", reach=1.0)
    E.line([(x0, top + 5), (x1, top + 5)], w=1.0, smooth=False, op=0.6)


# ------------------------------------------------------------------ pips

@suit
def an01(rng):
    """One: a stag in a farmyard with ribbons and tags wound through its antlers, knotted to a fence post; a
    child reaches up to tie on one more tag. The sky is wide and empty, the ground trodden bare in a circle."""
    E = _pip(1, "a", rng)
    HOR, BASE = 780, 980
    sky(E, 340, HOR, strongest=0.38, weakest=0.04, gap=6, tint=0.7)
    E.shape([(70, HOR), (70, HOR - 26), (200, HOR - 40), (330, HOR - 22), (430, HOR)], smooth=True, hatches=[(0, 3.4, 0.3)], sw=1.4)
    rect(E, 96, HOR - 56, 170, HOR, hatches=[(80, 3.4, 0.4)], sw=1.8)
    E.shape([(88, HOR - 56), (133, HOR - 88), (178, HOR - 56)], smooth=False, hatches=[(30, 3.4, 0.5)], sw=1.8)
    ground(E, HOR, op=0.55)
    for ry in (HOR + 52, HOR + 86):
        E.line([(IX0, ry), (IX1, ry)], w=2.0, smooth=False)
    for px in (140, 250, 440):
        rect(E, px - 6, HOR + 30, px + 6, HOR + 110, hatches=[(80, 2.6, 0.5)], sw=1.5)
    E.shape(ellipse_pts(340, BASE + 4, 280, 46, 28), fill=None, hatches=[(0, 3.2, 0.34)], tone=0.18, sw=1.2)
    grass(E, BASE + 40, IY1, 110)
    post_x = 570
    rect(E, post_x - 16, 470, post_x + 16, BASE + 4, hatches=[(80, 2.6, 0.55)], sw=2.2)
    E.shape([(post_x - 20, 470), (post_x, 450), (post_x + 20, 470)], smooth=False, hatches=[(30, 3, 0.5)], sw=1.8)
    fade(E, post_x - 16, 470, post_x + 16, BASE, op=0.6, side="r", reach=1.0)
    floor_shadow(E, 340, BASE + 4, 210, 14, 0.6)
    floor_shadow(E, post_x, BASE + 4, 36, 7, 0.6)
    pts = stag(E, 400, BASE, 1.0, fd=-1)
    # ribbons from the antlers to the post, hung with tags
    pts = sorted(pts, key=lambda p: -p[0])
    for k, (tx, ty) in enumerate(pts[:6]):
        py = 500 + k * 18
        rp = rope(E, (tx, ty), (post_x - 14, py), sag=26 + 8 * k, w=1.5 if k % 2 else 2.2)
        for m in (4, 8, 11):
            px_, py_ = rp[m]
            tag_card(E, px_, py_, 12, 18, rot=rng.uniform(-10, 10))
        E.add(f'<circle cx="{f(post_x - 14)}" cy="{f(py)}" r="3.2" fill="{INK}"/>')
    # the child, tying one more tag to a ribbon hanging from the antlers
    hx0, hy0 = 252, 640
    j = child(E, 130, BASE, 350, facing=1, lean=0.1, tilt=-14, wash_op=0.7, look=0.9, stride=0.02,
              hands={"near": (232, 670), "far": (206, 700)})
    hx, hy = j["hands"]["near"]
    ribbon = rope(E, (hx0 + 16, 520), (hx + 4, hy - 2), sag=-12, w=1.8, n=8)
    tag_card(E, hx + 2, hy - 4, 14, 22, rot=6)
    hand_dot(E, (hx, hy), 7, -0.6)
    return _end(E, pess_pip_close())


@suit
def an02(rng):
    """Two: a family close around a kitchen table under one lamp, figures overlapping; through the window a
    crowd of strangers passes in the dark street."""
    E = _pip(2, "b", rng)
    FL, TOP = 1010, 826
    wall(E, 340, FL, op=0.16)
    fade(E, IX0, 340, 220, FL, op=0.6, side="l", reach=1.0)
    fade(E, 460, 340, IX1, FL, op=0.6, side="r", reach=1.0)
    fade(E, IX0, 340, IX1, 470, op=0.5, side="t", reach=1.0)
    # window onto the street: a dark sheet, a crowd of pale faces over dark bodies
    wx0, wy0, wx1, wy1 = 196, 372, 484, 560
    window(E, wx0, wy0, wx1, wy1, tone=0.8, panes=(2, 1))
    clip_open(E, wx0, wy0, wx1, wy1)
    for yb, hh, n, ph in ((566, 150, 7, 0), (566, 118, 8, 20)):
        for k in range(n):
            x = wx0 + 22 + ph + k * (wx1 - wx0 - 44 - ph) / (n - 1) + rng.uniform(-5, 5)
            hr = hh * 0.1
            E.add(f'<path d="M{f(x - hr * 1.9)},{f(yb)} L{f(x - hr * 1.5)},{f(yb - hh + hr * 2.6)} L{f(x + hr * 1.5)},{f(yb - hh + hr * 2.6)} L{f(x + hr * 1.9)},{f(yb)} Z" fill="{iso.DARK}" opacity="0.92" stroke="{INK}" stroke-width="1"/>')
            E.shape(ellipse_pts(x, yb - hh + hr * 1.2, hr, hr * 1.2, 10), sw=1.2, tone=0.15)
    clip_close(E)
    # hanging lamp over the table, bone glow
    E.line([(340, 330), (340, 590)], w=1.4, smooth=False)
    glow(E, 340, 660, 200, 120, 0.34)
    E.shape([(340 - 20, 590), (340 + 20, 590), (340 + 56, 650), (340 - 56, 650)], smooth=False, hatches=[(75, 3, 0.35)], sw=2)
    E.shape(ellipse_pts(340, 652, 14, 5, 10), sw=1.4)
    floor_band(E, FL, 0.14)
    people = ((200, 890, "elder", 450, "long", 0.5, "white"), (484, 890, "adult", 470, "coat", 0.7, "dark"),
              (316, 900, "adult", 480, "dress", 0.55, "bun"), (410, 910, "child", 380, "smock", 0.6, "dark"),
              (256, 934, "child", 320, "smock", 0.5, "dark"))
    for fx, fy, kd, h, g, w, hr in people:
        fn = {"adult": adult, "elder": elder, "child": child}[kd]
        fn(E, fx, fy, h, view="front", pose="torso", garment=g, hair=hr, wash_op=w, mouth=0.0, look=0.0,
           hands={"left": (fx - 40, TOP - 6), "right": (fx + 40, TOP - 6)})
    E.shape([(100, TOP - 6), (580, TOP - 6), (590, TOP + 12), (90, TOP + 12)], smooth=False, hatches=[(0, 5, 0.25)], sw=1.8)
    E.shape([(90, TOP + 12), (590, TOP + 12), (598, 1004), (82, 1004)], smooth=False, hatches=[(90, 6, 0.4)], tone=0.1, sw=1.8)
    fade(E, 90, TOP + 12, 590, 1004, op=0.7, side="b", reach=1.0)
    for k in range(1, 16):
        xx = 90 + 500 * k / 16
        E.line([(xx, TOP + 16), (xx + (3 if k % 2 else -3), 1000)], w=0.8, op=0.5, smooth=False)
    for bx in (170, 250, 430, 510):
        iso.bowl(E, bx, TOP + 2, 30, 14)
    iso.tureen(E, 340, TOP + 4, 0.9)
    return _end(E, pess_pip_close())


def arch(x0, x1, yb, ya, n=18):
    """A pointed arch from x0 to x1 springing at yb with its crown at ya, closed along the base."""
    cx = (x0 + x1) / 2
    left = [(x0 + (cx - x0) * (k / n), yb - (yb - ya) * (k / n) ** 0.55) for k in range(n + 1)]
    right = [(2 * cx - x, y) for x, y in reversed(left[:-1])]
    return left + right


@suit
def an03(rng):
    """Three: a village congregation kneels in rows in a stone church, heads bowed; the vault is painted with
    a sky. One figure at the back looks up through a broken window pane at the real one."""
    E = _pip(3, "c", rng)
    SPR = 530
    wall(E, 340, 740, op=0.2)
    fade(E, IX0, 340, IX1, 740, op=0.4, side="t", reach=1.0)
    # the painted vault: a sky of hatching and stars inside nested ribs
    outer = arch(80, 600, SPR, 350)
    E.shape(outer, smooth=False, tone=0.2, hatches=[(0, 4.0, 0.32)], tint=(CAPUT, 0.4), sw=2.4)
    for k in range(18):
        sx, sy = rng.uniform(150, 530), rng.uniform(390, SPR - 30)
        E.line([(sx - 5, sy), (sx + 5, sy)], w=1.2, smooth=False)
        E.line([(sx, sy - 5), (sx, sy + 5)], w=1.2, smooth=False)
    iso.cloud_bank(E, 140, 470, 150, 22, 0.4)
    iso.cloud_bank(E, 360, 430, 130, 20, 0.4)
    for x0, x1, ya in ((130, 550, 410), (190, 490, 462)):
        E.shape(arch(x0, x1, SPR, ya), smooth=False, fill=None, sw=2.2, hatches=[])
    mass(E, [(IX0, SPR), (IX1, SPR), (IX1, SPR + 14), (IX0, SPR + 14)], solid=0.4, wash=0.3, sw=1.6)
    # columns at the springing points and the real window between the right column and the aisle
    for cx_ in (96, 584):
        rect(E, cx_ - 18, SPR + 14, cx_ + 18, 740, hatches=[(80, 3, 0.5)], sw=2)
    wx0, wx1, wy0, wy1 = 456, 560, 596, 714
    pointed = arch(wx0, wx1, wy1, wy0 - 20) 
    E.shape(pointed, smooth=False, tone=0.12, hatches=[(0, 2.6, 0.4)], tint=(CAPUT, 0.2), sw=2)
    wm = (wx0 + wx1) / 2
    E.line([(wm, wy0 - 12), (wm, wy1)], w=1.5, smooth=False)
    E.line([(wx0, (wy0 + wy1) / 2 + 8), (wx1, (wy0 + wy1) / 2 + 8)], w=1.5, smooth=False)
    E.shape([(wx0 + 8, (wy0 + wy1) / 2 + 14), (wm - 4, (wy0 + wy1) / 2 + 12), (wm - 2, wy1 - 6), (wx0 + 8, wy1 - 6)],
            smooth=False, fill=PAPER_FILL, tone=0.0, sw=1.0)
    for a in (200, 250, 300, 340, 20, 60):
        E.line([(wx0 + 34, wy1 - 52), (wx0 + 34 + 26 * math.cos(math.radians(a)), wy1 - 52 + 26 * math.sin(math.radians(a)))], w=1.0, smooth=False)
    rect(E, wx0 - 10, wy1 + 4, wx1 + 10, wy1 + 14, hatches=[(0, 3, 0.3)], sw=1.8)
    floor_band(E, 740, 0.12)
    # rows of kneeling people from far to near, each hidden to the waist by the pew behind it
    for yb, s, n, tone in ((808, 0.6, 8, 0.5), (890, 0.8, 6, 0.6), (996, 1.05, 4, 0.7)):
        step = (452 - 80) / n
        for i in range(n):
            kneeler(E, 80 + step * (i + 0.5), yb, s, rng.choice(("dark", "white", "dark", "dark")), tone, shawl=rng.random() < 0.3)
        board(E, 70, 470, yb, 36 * s, 0.2)
    # the one who looks up, in the aisle at the back
    adult(E, 534, 1050, 340, facing=1, lean=0.0, tilt=-24, garment="long", wash_op=0.85, look=0.9, stride=0.02)
    return _end(E, pess_pip_close())


def banner(E, x, top, w, h, device, tone=0.2):
    """A banner cloth hung from the pole top at (x, top): width w, height h, a device on it (no text)."""
    x0, y0, x1, y1 = x + 2, top + 4, x + 2 + w, top + 4 + h
    E.shape([(x0, y0), ((x0 + x1) / 2, y0 + 3), (x1, y0), (x1 - 3, (y0 + y1) / 2), (x1, y1), ((x0 + x1) / 2, y1 - 4), (x0, y1)],
            smooth=False, hatches=[(0, 4, 0.3)], tone=tone, sw=1.8)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = min(w, h) * 0.26
    if device == "sun":
        E.shape(ellipse_pts(cx, cy, r, r, 14), fill=None, tone=0.5, sw=1.6)
        for a in range(0, 360, 45):
            E.line([(cx + r * 1.2 * math.cos(math.radians(a)), cy + r * 1.2 * math.sin(math.radians(a))),
                    (cx + r * 1.8 * math.cos(math.radians(a)), cy + r * 1.8 * math.sin(math.radians(a)))], w=1.6, smooth=False)
    elif device == "cross":
        rect(E, cx - r * 0.3, cy - r * 1.5, cx + r * 0.3, cy + r * 1.5, tone=0.6, sw=1.4)
        rect(E, cx - r * 1.4, cy - r * 0.3, cx + r * 1.4, cy + r * 0.3, tone=0.6, sw=1.4)
    elif device == "tri":
        E.shape([(cx, cy - r * 1.4), (cx + r * 1.4, cy + r), (cx - r * 1.4, cy + r)], smooth=False, tone=0.6, sw=1.5)
    elif device == "stripes":
        for k in range(-2, 3):
            E.line([(x0 + 6, cy + k * r * 0.7), (x1 - 6, cy + k * r * 0.7)], w=3.2 if k % 2 else 1.6, smooth=False)
    elif device == "star":
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = r * 1.6 if k % 2 == 0 else r * 0.7
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        E.shape(pts, smooth=False, tone=0.6, sw=1.4)
    elif device == "wheel":
        E.shape(ellipse_pts(cx, cy, r * 1.3, r * 1.3, 16), fill=None, sw=1.6)
        for a in range(0, 180, 45):
            E.line([(cx - r * 1.3 * math.cos(math.radians(a)), cy - r * 1.3 * math.sin(math.radians(a))),
                    (cx + r * 1.3 * math.cos(math.radians(a)), cy + r * 1.3 * math.sin(math.radians(a)))], w=1.3, smooth=False)
    else:
        for k in (-1, 0, 1):
            E.line([(cx - r * 1.4, cy + k * r * 0.9), (cx, cy + k * r * 0.9 + r * 0.8), (cx + r * 1.4, cy + k * r * 0.9)], w=2.2, smooth=False)


@suit
def an04(rng):
    """Four: a column of marchers carries banners, each with a different device, through a town square; the
    leaders hold theirs high. A woman at the roadside holds up a child. The road narrows into haze."""
    E = _pip(4, "d", rng)
    VP = (340, 640)
    TOPY, BOTY, XE = 350, 940, 276    # the facades run from the plate edge to x=XE, then dissolve in haze
    sky(E, 340, VP[1], strongest=0.3, weakest=0.04, gap=6, tint=0.6)

    def lerp_wall(side, u, v):
        """Point on a facade: u from the near edge (0) to the far end (1), v from the eave (0) to the base (1)."""
        xe = IX0 if side < 0 else IX1
        xf = XE if side < 0 else IX1 - (XE - IX0)
        x = xe + (xf - xe) * u
        t = abs(x - xe) / abs(VP[0] - xe)
        top = TOPY + (VP[1] - TOPY) * t
        bot = BOTY + (VP[1] - BOTY) * t
        return (x, top + (bot - top) * v)

    # haze at the end of the road
    E.add(f'<ellipse cx="{VP[0]}" cy="{VP[1] - 40}" rx="170" ry="140" fill="{BONE}" opacity="0.5" filter="url(#mist)"/>')
    for side in (-1, 1):
        poly = [lerp_wall(side, 0, 0), lerp_wall(side, 1, 0), lerp_wall(side, 1, 1), lerp_wall(side, 0, 1)]
        E.shape(poly, smooth=False, hatches=[(80, 4, 0.28), (-45, 5, 0.2)], tone=0.2, sw=2)
        fade(E, min(p[0] for p in poly), TOPY, max(p[0] for p in poly), BOTY, op=0.5, side="l" if side < 0 else "r", reach=1.0, clip=poly)
        for u0, u1 in ((0.07, 0.2), (0.3, 0.42), (0.52, 0.62), (0.72, 0.8)):
            for v0, v1 in ((0.12, 0.3), (0.4, 0.58)):
                E.shape([lerp_wall(side, u0, v0), lerp_wall(side, u1, v0), lerp_wall(side, u1, v1), lerp_wall(side, u0, v1)],
                        smooth=False, hatches=[(60, 2.4, 0.7)], sw=1.2)
    # the square: paving converging on the haze
    sq = [lerp_wall(-1, 1, 1), lerp_wall(1, 1, 1), (IX1, IY1), (IX0, IY1)]
    E.shape([(IX0, BOTY - 0), lerp_wall(-1, 1, 1), lerp_wall(1, 1, 1), (IX1, BOTY), (IX1, IY1), (IX0, IY1)], smooth=False,
            hatches=[(0, 5, 0.2)], sw=0)
    for k in range(-9, 10):
        E.line([(VP[0] + k * 12, VP[1] + 40), (VP[0] + k * 95, IY1)], w=0.7, op=0.4, smooth=False)
    fade(E, IX0, VP[1], IX1, IY1, op=0.6, side="b", reach=1.0)
    # the column: rows from the haze to the near edge; each row's banners are drawn before the figures
    devices = ["sun", "cross", "tri", "stripes", "star", "wheel", "chev"]
    rows = ((VP[1] + 70, 120, (VP[0] - 70, VP[0] - 4, VP[0] + 62), 1.9), (VP[1] + 135, 170, (VP[0] - 112, VP[0] - 22, VP[0] + 76), 1.75),
            (VP[1] + 240, 250, (VP[0] - 160, VP[0] - 28, VP[0] + 104), 1.6), (VP[1] + 395, 360, (VP[0] - 150, VP[0] + 40), 1.4))
    di = 0
    for yb, hh, xs, up in rows:
        info = []
        for k, x in enumerate(xs):
            px = x + hh * 0.12
            hand = (px, yb - hh * 0.72)
            ptop = yb - hh * up
            E.line([(px, yb - hh * 0.3), (px, ptop)], w=2.4 + hh * 0.004, smooth=False)
            E.shape(ellipse_pts(px, ptop - 4, 3 + hh * 0.01, 3 + hh * 0.01, 8), fill=INK, outline=False)
            banner(E, px, ptop, hh * 0.34, hh * 0.4, devices[di % 7], tone=0.08 + 0.05 * (di % 3))
            info.append((x, k, hand))
            di += 1
        for x, k, hand in info:
            (adult, youth, adult)[k % 3](E, x, yb, hh, view="back", garment=("coat", "dress", "coat")[k % 3],
                                          hat=("top", None, "wide")[k % 3], wash_op=0.8, stride=0.03,
                                          hands={"right": (hand[0], hand[1], -1), "left": (x - hh * 0.1, yb - hh * 0.52)})
    # the woman and child at the roadside, right
    wx, wb = 566, 1010
    wh = 400
    w = adult(E, wx, wb, wh, facing=-1, lean=0.04, garment="dress", wash_op=0.8, look=-0.9, stride=0.02,
              hands={"near": (wx - 66, wb - 0.52 * wh), "far": (wx - 40, wb - 0.62 * wh)})
    hy = w["hands"]["near"][1]
    ch = child(E, wx - 60, hy + 6, 190, view="front", pose="torso", garment="smock", wash_op=0.5, look=-0.4,
               hands={"left": (wx - 104, hy - 62), "right": (wx - 22, hy - 58)})
    hand_dot(E, w["hands"]["near"], 7, -2.6)
    return _end(E, pess_pip_close())


def clerk_desk(E, x, FL, s, rng, tone=0.8):
    """A clerk on a high stool at a tall sloping desk, writing in a ledger; s scales the whole group, x is the
    stool centre and FL the floor line. Every clerk is drawn alike. Returns the clerk's joints."""
    h = 470 * s
    base = FL - 70 * s
    sy = base - 0.25 * h
    # stool: seat, legs, footrest ring
    for lx in (x - 34 * s, x + 34 * s):
        rect(E, lx - 4 * s, sy + 10 * s, lx + 4 * s, FL, hatches=[(80, 2.4, 0.5)], sw=1.4)
    rect(E, x - 42 * s, base - 4 * s, x + 42 * s, base + 4 * s, sw=1.2)
    rect(E, x - 46 * s, sy, x + 46 * s, sy + 12 * s, hatches=[(4, 3, 0.4)], sw=1.8)
    dx0, dx1 = x + 66 * s, x + 296 * s
    topy = FL - 236 * s
    # desk body, then clerk, then the sloping top and ledger over his lap and hands
    mass(E, [(dx0 + 8 * s, topy + 20 * s), (dx1, topy + 20 * s), (dx1, FL), (dx0 + 8 * s, FL)], solid=0.35, wash=0.3, sw=1.8)
    for k in range(2):
        rect(E, dx0 + (20 + k * 100) * s, topy + 44 * s, dx0 + (100 + k * 100) * s, topy + 104 * s, sw=1.2)
        E.shape(ellipse_pts(dx0 + (60 + k * 100) * s, topy + 74 * s, 4 * s, 4 * s, 8), fill=INK, outline=False)
    c = adult(E, x, base, h, pose="sit", facing=1, lean=0.24, tilt=10, garment="coat", hair="dark", wash_op=tone,
              hands={"near": (dx0 + 74 * s, topy - 6 * s), "far": (dx0 + 52 * s, topy - 2 * s)}, stride=0.02)
    E.shape([(dx0 - 6 * s, topy - 30 * s), (dx1 + 8 * s, topy + 4 * s), (dx1 + 8 * s, topy + 24 * s), (dx0 - 6 * s, topy + 20 * s)],
            smooth=False, hatches=[(10, 4, 0.26)], sw=2)
    # ledger lying open on the slope
    E.shape([(dx0 + 20 * s, topy - 22 * s), (dx0 + 190 * s, topy - 4 * s), (dx0 + 188 * s, topy + 4 * s), (dx0 + 18 * s, topy - 14 * s)],
            smooth=False, sw=1.3)
    E.line([(dx0 + 104 * s, topy - 16 * s), (dx0 + 102 * s, topy + 2 * s)], w=1.0, smooth=False)
    for hnd in c["hands"].values():
        hand_dot(E, hnd, 7 * s)
    px, py = c["hands"]["near"]
    E.line([(px - 2 * s, py + 2 * s), (px + 22 * s, py - 30 * s)], w=2, smooth=False)
    return c


@suit
def an05(rng):
    """Five: a clerk at a tall desk in a room of identical desks writes in a ledger, a framed certificate above him;
    through the open door a corridor of offices recedes; on the windowsill a candle burns down in daylight."""
    E = _pip(5, "e", rng)
    WB = 790
    wall(E, 340, WB, op=0.16)
    fade(E, IX0, 340, 240, WB, op=0.5, side="l", reach=1.0)
    fade(E, IX0, 340, IX1, 470, op=0.4, side="t", reach=1.0)
    # the open door and the corridor of offices
    dx0, dy0, dx1 = 462, 392, 590
    rect(E, dx0 - 12, dy0 - 12, dx1 + 12, WB, sw=2)
    clip_open(E, dx0, dy0, dx1, WB)
    E.add(f'<rect x="{dx0}" y="{dy0}" width="{dx1 - dx0}" height="{WB - dy0}" fill="{PAPER_FILL}"/>')
    vp = (526, 600)
    E.shape([(dx0, dy0), (vp[0] - 22, vp[1] - 24), (vp[0] - 22, vp[1] + 40), (dx0, WB)], smooth=False, hatches=[(80, 3.2, 0.4), (-48, 3.8, 0.3)], sw=1.4)
    E.shape([(dx1, dy0), (vp[0] + 22, vp[1] - 24), (vp[0] + 22, vp[1] + 40), (dx1, WB)], smooth=False, hatches=[(100, 3.2, 0.4), (48, 3.8, 0.3)], sw=1.4)
    E.shape([(dx0, dy0), (dx1, dy0), (vp[0] + 22, vp[1] - 24), (vp[0] - 22, vp[1] - 24)], smooth=False, hatches=[(0, 3, 0.35)], sw=1.4)
    E.shape([(dx0, WB), (dx1, WB), (vp[0] + 22, vp[1] + 40), (vp[0] - 22, vp[1] + 40)], smooth=False, hatches=[(0, 3.4, 0.28)], sw=1.4)
    for side in (-1, 1):
        for t0, t1 in ((0.12, 0.32), (0.4, 0.55), (0.62, 0.72), (0.78, 0.84)):
            def pt(t, v):
                xe = dx0 if side < 0 else dx1
                xf = vp[0] - 22 if side < 0 else vp[0] + 22
                x = xe + (xf - xe) * t
                yt = dy0 + (vp[1] - 24 - dy0) * t
                yb = WB + (vp[1] + 40 - WB) * t
                return (x, yt + (yb - yt) * v)
            E.shape([pt(t0, 0.28), pt(t1, 0.28), pt(t1, 0.97), pt(t0, 0.97)], smooth=False, hatches=[(60, 2.4, 0.7)], sw=1.1)
    E.add(f'<ellipse cx="{vp[0]}" cy="{vp[1]}" rx="30" ry="40" fill="{BONE}" opacity="0.5" filter="url(#wash)"/>')
    clip_close(E)
    E.add(f'<rect x="{dx0}" y="{dy0}" width="{dx1 - dx0}" height="{WB - dy0}" fill="none" stroke="{INK}" stroke-width="2"/>')
    mass(E, [(dx0, dy0), (dx0 + 30, dy0 + 14), (dx0 + 30, WB - 20), (dx0, WB)], solid=0.5, sw=1.8)
    # the window with the candle on its sill, in daylight
    wx0, wy0, wx1, wy1 = 284, 420, 394, 610
    window(E, wx0, wy0, wx1, wy1, tone=0.08, panes=(1, 2))
    candle(E, 340, wy1 + 10, 52, 0.8)
    # the framed certificate
    cx0, cy0 = 96, 408
    rect(E, cx0, cy0, cx0 + 128, cy0 + 100, hatches=[(45, 3, 0.4)], sw=2.2)
    rect(E, cx0 + 10, cy0 + 10, cx0 + 118, cy0 + 90, sw=1.3)
    for k in range(3):
        E.line([(cx0 + 24, cy0 + 28 + k * 14), (cx0 + 104, cy0 + 28 + k * 14)], w=0.9, op=0.6, smooth=False)
    E.shape(ellipse_pts(cx0 + 64, cy0 + 74, 9, 9, 10), tone=0.5, sw=1.2)
    floor_band(E, WB, 0.14)
    # identical desks, nearest last
    clerk_desk(E, 440, 856, 0.5, rng, 0.8)
    clerk_desk(E, 270, 920, 0.72, rng, 0.8)
    clerk_desk(E, 96, 1010, 1.02, rng, 0.85)
    return _end(E, pess_pip_close())


@suit
def an06(rng):
    """Six: a man walks the same towpath along a canal at dusk; the lamplighter, the baker and a woman at a window
    stand where they stood the day before; the clock on the tower has no hands."""
    E = _pip(6, "f", rng)
    HOR, QUAY = 690, 868
    sky(E, 340, HOR, strongest=0.45, weakest=0.06, gap=6, tint=0.9)
    # tower with a handless clock
    tx0, tx1 = 408, 488
    rect(E, tx0, 400, tx1, HOR + 10, hatches=[(80, 4, 0.3)], sw=2)
    E.shape([(tx0 - 6, 400), ((tx0 + tx1) / 2, 350), (tx1 + 6, 400)], smooth=False, hatches=[(30, 3.4, 0.5)], sw=2)
    E.shape(ellipse_pts(448, 446, 26, 26, 20), hatches=[(60, 3, 0.2)], sw=2.2)
    E.shape(ellipse_pts(448, 446, 21, 21, 20), sw=1.1)
    for k in range(12):
        a = k * math.pi / 6
        E.line([(448 + 15 * math.sin(a), 446 - 15 * math.cos(a)), (448 + 19 * math.sin(a), 446 - 19 * math.cos(a))], w=1.3, smooth=False)
    E.shape(ellipse_pts(448, 446, 2.6, 2.6, 8), fill=INK, outline=False)
    rect(E, 436, 500, 460, 540, tone=0.7, sw=1.4)
    # houses with lit windows, one with the woman at an upper window
    for hx, hw, hh in ((70, 150, 250), (220, 110, 300), (330, 80, 200), (500, 110, 270)):
        rect(E, hx, HOR - hh, hx + hw, HOR + 10, hatches=[(80, 4, 0.3), (-45, 5, 0.2)], sw=1.8)
        E.shape([(hx - 5, HOR - hh), (hx + hw / 2, HOR - hh - 36), (hx + hw + 5, HOR - hh)], smooth=False, hatches=[(30, 4, 0.45)], sw=1.8)
        for wy in range(int(HOR - hh + 36), int(HOR - 110), 60):
            for wxx in (hx + hw * 0.18, hx + hw * 0.58):
                rect(E, wxx, wy, wxx + hw * 0.22, wy + 34, hatches=[(60, 2.4, 0.7)], sw=1.2)
    for gx, gy in ((246, 480), (110, 560)):
        glow(E, gx, gy, 24, 20, 0.5)
        rect(E, gx - 13, gy - 18, gx + 13, gy + 18, tone=0.06, sw=1.4)
    clip_open(E, 233, 462, 259, 498)
    adult(E, 246, 520, 130, view="front", pose="torso", garment="dress", wash_op=0.5, look=0.0, hands={"left": (233, 504), "right": (259, 504)})
    clip_close(E)
    rect(E, 233, 462, 259, 498, fill=None, sw=1.6)
    # the baker in a doorway
    rect(E, 142, 620, 196, HOR + 10, hatches=[(80, 2.4, 0.8)], tone=0.7, sw=2)
    adult(E, 170, HOR + 8, 190, view="front", garment="long", hair="white", wash_op=0.4, hands={"left": (150, HOR - 70), "right": (190, HOR - 70)})
    # towpath, quay, canal
    ground(E, HOR, op=0.5, y1=QUAY)
    rect(E, IX0, QUAY, IX1, QUAY + 24, hatches=[(0, 5, 0.3)], sw=2)
    for k in range(9):
        xx = IX0 + 20 + k * 70
        E.line([(xx, QUAY), (xx, QUAY + 24)], w=0.8, op=0.5, smooth=False)
    slate(E, IX0, QUAY + 24, IX1, IY1 + 20, 0.7)
    d = []
    for k in range(10):
        yy = QUAY + 40 + k * 20
        d.append(f"M{IX0},{yy} " + " ".join("q10,-4 20,0" for _ in range(27)))
    E.add(f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width="0.8" opacity="0.5" fill="none"/>')
    rv = []
    for hx, hw in ((100, 120), (260, 80), (420, 60), (520, 90)):
        rv.append(f"M{hx},{QUAY + 30} l0,150 M{hx + hw // 2},{QUAY + 30} l0,150 M{hx + hw},{QUAY + 30} l0,150")
    E.add(f'<path d="{" ".join(rv)}" stroke="{INK}" stroke-width="0.8" opacity="0.18" fill="none"/>')
    E.add(f'<path d="M{IX0},{QUAY + 120} h{IX1 - IX0}" stroke="{INK}" opacity="0.0"/>')
    # worn groove of the towpath
    E.add(f'<path d="M{IX0},{QUAY - 22} L{IX1},{QUAY - 30}" stroke="{INK}" stroke-width="3" opacity="0.2" stroke-dasharray="14 10" fill="none"/>')
    # lamp post with the lamplighter
    lx = 354
    E.line([(lx, HOR + 80), (lx, 500)], w=3.0, smooth=False)
    glow(E, lx, 484, 36, 36, 0.42)
    E.shape([(lx - 12, 500), (lx + 12, 500), (lx + 9, 468), (lx - 9, 468)], smooth=False, tone=0.1, sw=1.8)
    E.shape([(lx - 14, 468), (lx, 456), (lx + 14, 468)], smooth=False, hatches=[(30, 2.4, 0.7)], sw=1.5)
    j = adult(E, lx + 44, HOR + 90, 270, facing=-1, lean=0.06, garment="coat", hair="dark", hat="top", wash_op=0.85, stride=0.04,
              hands={"near": (lx + 12, HOR - 30), "far": (lx + 22, HOR - 6)})
    E.line([(lx + 8, HOR - 36), (lx - 6, 470)], w=2, smooth=False)
    hand_dot(E, j["hands"]["near"], 6, math.pi)
    # the man who walks the path
    m = adult(E, 224, 846, 420, facing=1, lean=0.1, garment="coat", hair="dark", hat="top", wash_op=0.9, stride=0.08,
              hands={"near": (258, 700), "far": (206, 712)})
    floor_shadow(E, 236, 848, 70, 7, 0.6)
    return _end(E, pess_pip_close())


CARDS = {f"an{n:02d}": globals()[f"an{n:02d}"] for n in range(1, 15) if f"an{n:02d}" in globals()}
