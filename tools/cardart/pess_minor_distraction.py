"""Pessimist deck, minor series, suit of Distraction (di01-di14): attention kept busy elsewhere.

Pips di01-di10: pess_pip_open("distraction", n) draws the plate with a frieze of n spinning tops; the
scene of the card's Image paragraph is drawn below the frieze (PESS_VIGNETTE), then pess_pip_close().
No spinning top is drawn in a scene, so the emblem count stays readable.

Courts di11-di14: pess_court_open("distraction", age) counts the age in emblems at the top, then a scene
from the card's Figure paragraph, then pess_court_close(). The main figure is child(), youth(), adult() or
elder() from the Isolation module.

Colour: bone ochre. WASH["bone"] is a light colour, so the suit colour OCHRE is the bone wash mixed deeply
toward a warm umber; shadows, tints, skies, night windows and the dark underlays all read as ochre and
umber. The one other colour is a small cold blue for screens (BLUE), used in di01 and di10.

Style, engine, figures and helpers are those of pess_minor_isolation, imported and not copied.
"""

import math
import re

from . import pess_minor_isolation as iso
from .common import PESS_PAPER, WASH, f, pess_court_close, pess_court_open, pess_pip_close, pess_pip_open, svg
from .pess_awakening import PAPER_FILL, ellipse_pts
from .pess_minor_isolation import (CONTRAST, IX0, IX1, IY0, IY1, INK, VX0, VX1, VY0, VY1, Plate, adult, arm_of_chair,
                                   armchair, book, candle, chair_side, child, clip_close, clip_open, cup, elder, fade,
                                   floor_band, floor_shadow, grass, hand_dot, jar, mass, mix, newspaper, rect, sky,
                                   suit_colour, table_front, wall, wall_clock, window, youth)

BONE = WASH["bone"]
OCHRE = mix(BONE, "#4a2c0a", 0.8)    # the suit colour: bone mixed deeply toward umber
BLUE = "#7fb0d6"                      # the second colour: the cold light of a screen
SCREEN = "#cfe6f5"
suit = suit_colour(OCHRE)


# ------------------------------------------------------------------ plate helpers

def _pip(n, tag, rng):
    E = Plate(rng, tag)
    E.add(pess_pip_open("distraction", n))
    return E


def _court(age, tag, rng):
    E = Plate(rng, tag)
    E.add(pess_court_open("distraction", age))
    return E


def _end(E, close, top=VY0, **kw):
    iso.vignette(E, top=top, **kw)
    return svg(E.done() + close, PESS_PAPER)


# ------------------------------------------------------------------ small pieces

def glow(E, x, y, rx, ry, op=0.3, colour=None):
    """A blurred glow of light; the warm bone of the suit unless a colour is given."""
    E.add(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}" fill="{colour or BONE}" opacity="{op}" filter="url(#wash)"/>')


def screen(E, x, y, w, h, rot=0, op=0.9):
    """A lit screen or phone: dark case with a bright blue face, centred at (x, y)."""
    E.add(f'<g transform="rotate({rot} {f(x)} {f(y)})">')
    E.add(f'<rect x="{f(x - w / 2 - 3)}" y="{f(y - h / 2 - 3)}" width="{f(w + 6)}" height="{f(h + 6)}" rx="3" fill="{INK}"/>')
    E.add(f'<rect x="{f(x - w / 2)}" y="{f(y - h / 2)}" width="{f(w)}" height="{f(h)}" rx="2" fill="{SCREEN}" opacity="{op}"/>')
    E.add("</g>")


def blue_glow(E, x, y, rx, ry, op=0.4):
    glow(E, x, y, rx, ry, op, BLUE)


def lamp_pool(E, x, y, rx, ry, op=0.35):
    """Warm light pooled on a surface."""
    glow(E, x, y, rx, ry, op)


def antler_lines(cx, cy, s, sg):
    """Polylines of one side of a pair of antlers rising from (cx, cy); sg is -1 or +1."""
    beam = [(0, 0), (30, -30), (62, -48), (100, -52), (136, -78), (160, -126), (172, -172)]
    tines = [[(34, -34), (30, -90), (38, -140)], [(70, -50), (78, -110), (92, -156)],
             [(104, -54), (128, -50), (150, -64)], [(138, -82), (112, -118), (116, -162)],
             [(160, -126), (192, -134), (214, -126)], [(172, -172), (192, -198)]]
    out = [[(cx + sg * x * s, cy + y * s) for x, y in beam]]
    for t in tines:
        out.append([(cx + sg * x * s, cy + y * s) for x, y in t])
    return out


def antler_shadow(E, cx, cy, s, sx=1.0, sy=1.0, clip=(IX0, 340, IX1, 560)):
    """The shadow of the antlers: thick blurred strokes of the deep suit colour, stretched about (cx, cy)
    and kept inside the clip box."""
    cid = E.uid("q")
    E.add(f'<clipPath id="{cid}"><rect x="{clip[0]}" y="{clip[1]}" width="{clip[2] - clip[0]}" height="{clip[3] - clip[1]}"/></clipPath>'
          f'<g clip-path="url(#{cid})"><g transform="translate({f(cx)} {f(cy)}) scale({sx} {sy}) translate({f(-cx)} {f(-cy)})">')
    d = []
    for sg in (-1, 1):
        for pl in antler_lines(cx, cy, s, sg):
            d.append("M" + " L".join(f"{f(x)},{f(y)}" for x, y in pl))
    E.add(f'<path d="{" ".join(d)}" fill="none" stroke="{iso.DARK}" stroke-width="{f(16 * s)}" stroke-linecap="round" '
          f'stroke-linejoin="round" opacity="{min(0.8, 0.5 * CONTRAST):.2f}" filter="url(#wash)"/></g></g>')


def antlers(E, cx, cy, s):
    for sg in (-1, 1):
        for k, pl in enumerate(antler_lines(cx, cy, s, sg)):
            E.line(pl, w=(5.5 if k == 0 else 3.4) * s, smooth=False)
            E.line([(x + 1.5, y) for x, y in pl], w=1.2, op=0.6, smooth=False, color=PAPER_FILL)


def parcel(E, x, y, w, h, rot=0, ribbon=True, open_=False):
    """A wrapped parcel with its base-left at (x, y): box, ribbon cross, a bow."""
    E.add(f'<g transform="rotate({rot} {f(x + w / 2)} {f(y)})">')
    rect(E, x, y - h, x + w, y, hatches=[(70, 3.4, 0.28)], sw=1.8)
    if ribbon:
        rect(E, x + w / 2 - 4, y - h, x + w / 2 + 4, y, hatches=[(0, 2, 0.8)], sw=1.0)
        rect(E, x, y - h / 2 - 4, x + w, y - h / 2 + 4, hatches=[(80, 2, 0.8)], sw=1.0)
        E.shape(ellipse_pts(x + w / 2 - 9, y - h - 4, 9, 6, 10), sw=1.2)
        E.shape(ellipse_pts(x + w / 2 + 9, y - h - 4, 9, 6, 10), sw=1.2)
    E.add("</g>")


def shop_hat(E, x, y, s=1.0):
    """A hat on a stand, base at (x, y)."""
    E.line([(x, y), (x, y - 40 * s)], w=2.4, smooth=False)
    E.line([(x - 14 * s, y), (x + 14 * s, y)], w=2.6, smooth=False)
    E.shape(ellipse_pts(x, y - 52 * s, 30 * s, 8 * s, 14), hatches=[(0, 2.4, 0.5)], sw=1.6)
    E.shape([(x - 17 * s, y - 52 * s), (x - 14 * s, y - 76 * s), (x + 14 * s, y - 76 * s), (x + 17 * s, y - 52 * s)],
            smooth=False, hatches=[(70, 2.4, 0.6)], sw=1.6)


def dress_form(E, x, y, s=1.0):
    """A dressmaker's dummy on a stand, base at (x, y)."""
    E.line([(x, y), (x, y - 70 * s)], w=3, smooth=False)
    E.line([(x - 22 * s, y), (x + 22 * s, y)], w=3, smooth=False)
    E.shape([(x - 8 * s, y - 150 * s), (x + 8 * s, y - 150 * s), (x + 12 * s, y - 138 * s), (x + 26 * s, y - 132 * s),
             (x + 22 * s, y - 100 * s), (x + 28 * s, y - 70 * s), (x - 28 * s, y - 70 * s), (x - 22 * s, y - 100 * s),
             (x - 26 * s, y - 132 * s), (x - 12 * s, y - 138 * s)], hatches=[(70, 2.6, 0.5)], sw=1.8)
    E.shape(ellipse_pts(x, y - 156 * s, 4 * s, 7 * s, 8), sw=1.4)


def shoe_pair(E, x, y, s=1.0):
    E.shape([(x - 22 * s, y), (x - 22 * s, y - 14 * s), (x - 6 * s, y - 20 * s), (x + 14 * s, y - 10 * s), (x + 24 * s, y - 6 * s),
             (x + 24 * s, y)], smooth=False, hatches=[(70, 1.9, 0.85)], sw=1.4)


def pennants(E, pts, n, size=22, hang=1.0):
    """A string of blank pennant flags along the polyline pts (a sagging cord)."""
    E.line(pts, w=1.4)
    # sample the cord by linear interpolation along its length
    seg = [(a, b, math.hypot(b[0] - a[0], b[1] - a[1])) for a, b in zip(pts, pts[1:])]
    total = sum(s[2] for s in seg)
    for k in range(n):
        d = total * (k + 0.5) / n
        for a, b, ln in seg:
            if d <= ln:
                px, py = a[0] + (b[0] - a[0]) * d / ln, a[1] + (b[1] - a[1]) * d / ln
                break
            d -= ln
        E.shape([(px - size * 0.5, py), (px + size * 0.5, py), (px, py + size * 1.5 * hang)], smooth=False,
                hatches=[(70, 2.8, 0.5)] if k % 2 else [], sw=1.3)


# ------------------------------------------------------------------ pips

@suit
def di01(rng):
    """One: a woman at a kitchen table at night, lit from below by a bright rectangle in her hands; a
    hunting trophy of enormous antlers on the wall behind her, its shadow spread over the ceiling."""
    E = _pip(1, "a", rng)
    FL = 1010
    wall(E, 340, FL, op=0.16)
    fade(E, IX0, 340, IX1, 1000, op=0.7, side="t", reach=1.0)
    fade(E, IX0, 340, 260, FL, op=0.5, side="l", reach=1.0)
    fade(E, 480, 340, IX1, FL, op=0.5, side="r", reach=1.0)
    # the shadow of the antlers over the ceiling, thrown up by the light below
    antler_shadow(E, 350, 470, 1.2, sx=1.25, sy=0.62, clip=(IX0, 340, IX1, 470))
    window(E, 92, 560, 214, 800, tone=0.85, panes=(1, 2))
    # trophy plaque and head
    E.shape([(300, 545), (400, 545), (410, 600), (350, 650), (290, 600)], smooth=False, hatches=[(70, 3.4, 0.5)], sw=2.2)
    E.shape([(326, 520), (374, 520), (384, 560), (370, 612), (350, 628), (330, 612), (316, 560)],
            hatches=[(62, 2.6, 0.5), (-40, 3, 0.4)], sw=2)
    for sg in (-1, 1):
        E.shape([(350 + sg * 24, 524), (350 + sg * 58, 506), (350 + sg * 40, 540)], smooth=False, hatches=[(60, 2, 0.8)], sw=1.5)
        E.add(f'<circle cx="{350 + sg * 12}" cy="568" r="2.8" fill="{INK}"/>')
    E.shape(ellipse_pts(350, 612, 10, 7, 8), hatches=[(0, 1.8, 0.9)], sw=1.2)
    antlers(E, 350, 524, 1.0)
    floor_band(E, FL, 0.16)
    chair_side(E, 175, FL, seat=125, f_dir=1, back_h=210, w=110)
    top = 808
    w = adult(E, 210, FL, 500, pose="sit", facing=1, lean=0.24, tilt=12, wash_op=0.7, look=0.9,
              hands={"near": (330, 770), "far": (344, 776)})
    iso.cast(E, [(292, top + 24), (596, top + 24), (604, FL - 2), (286, FL - 2)], 0.6)
    iso.floor_shadow(E, 240, FL - 2, 150, 12, 0.6)
    table_front(E, 285, 595, top, FL, thick=18, legs=(0.08, 0.92))
    cup(E, 500, top, 1.2)
    E.shape([(430, top), (450, top - 16), (478, top - 16), (478, top)], smooth=False, hatches=[(0, 2, 0.5)], sw=1.4)
    hx, hy = w["hands"]["near"]
    screen(E, hx + 8, hy - 8, 20, 32, rot=-20)
    for hnd in w["hands"].values():
        hand_dot(E, hnd, 7)
    blue_glow(E, hx + 10, hy - 20, 110, 90, 0.5)
    return _end(E, pess_pip_close())


@suit
def di02(rng):
    """Two: an arcade of lit shop windows at dusk; a woman with parcels on both arms stops at the next
    window; behind her a parcel lies open on the pavement."""
    E = _pip(2, "b", rng)
    FL = 1000
    PIERS = (70, 250, 430, 610)
    # dusk over the arches, heaviest at the top
    sky(E, 340, 500, strongest=0.5, weakest=0.1, gap=5, tint=0.9)
    mass(E, [(70, 340), (610, 340), (610, 372), (70, 372)], solid=0.6, sw=2)
    for a, b in zip(PIERS, PIERS[1:]):
        cx = (a + b) / 2
        arch = [(a + 12, 500)] + [(cx + math.cos(math.pi * (1 - k / 12)) * ((b - a) / 2 - 12), 500 - math.sin(math.pi * (1 - k / 12)) * 88)
                                  for k in range(13)] + [(b - 12, 500)]
        E.shape(arch, smooth=False, hatches=[(0, 3, 0.3)], tone=0.0, sw=2)
        fade(E, a, 380, b, 500, op=0.8, side="t", reach=1.0, clip=arch)
    # lit windows
    for k, (a, b) in enumerate(zip(PIERS, PIERS[1:])):
        x0, x1 = a + 18, b - 18
        rect(E, x0, 510, x1, 930, hatches=[(0, 5, 0.12)], sw=2.2)
        glow(E, (x0 + x1) / 2, 760, 80, 140, 0.55)
        rect(E, x0, 780, x1, 790, hatches=[(0, 2, 0.6)], sw=1.5)
        rect(E, x0, 870, x1, 930, hatches=[(80, 3, 0.4)], sw=1.5)
        cx = (x0 + x1) / 2
        if k == 0:
            shop_hat(E, cx - 40, 780, 1.0)
            shop_hat(E, cx + 40, 780, 0.9)
            shop_hat(E, cx, 690, 0.8)
            rect(E, x0, 690 + 10, x1, 700 + 10, hatches=[(0, 2, 0.6)], sw=1.4)
        elif k == 1:
            dress_form(E, cx - 44, 870, 1.0)
            shoe_pair(E, cx + 20, 780, 1.0)
            shoe_pair(E, cx + 56, 780, 1.0)
            iso.lantern(E, cx + 28, 520, 0.6)
        else:
            for lx, ly in ((cx - 40, 780), (cx + 36, 780)):
                iso.table_lamp(E, lx, ly, 0.7, glow_=False)
            iso.wall_clock(E, cx, 640, 26)
        fade(E, x0, 510, x1, 930, op=0.4, side="t", reach=0.6)
    # piers
    for px in PIERS:
        rect(E, px - 12, 372, px + 12, FL, hatches=[(80, 2.8, 0.5)], sw=2)
        fade(E, px - 12, 372, px + 12, FL, op=0.5, side="l", reach=1.0)
        rect(E, px - 16, 372, px + 16, 388, hatches=[(0, 3, 0.5)], sw=1.8)
        rect(E, px - 16, FL - 14, px + 16, FL, hatches=[(0, 3, 0.5)], sw=1.8)
    floor_band(E, FL, 0.2, y1=1086)
    iso.floor_shadow(E, 480, FL + 4, 90, 12, 0.7)
    # the open parcel left on the pavement
    bx, by = 150, FL + 52
    E.shape([(bx - 50, by), (bx + 50, by), (bx + 56, by - 40), (bx - 44, by - 40)], smooth=False, hatches=[(70, 3, 0.4)], sw=1.8)
    E.shape([(bx - 50, by - 40), (bx - 70, by - 74), (bx - 20, by - 74), (bx - 4, by - 40)], smooth=False, hatches=[(0, 3, 0.3)], sw=1.5)
    for k in range(5):
        E.line([(bx - 40 + k * 18, by - 38), (bx - 30 + k * 16 + rng.uniform(-8, 8), by - 66 - rng.uniform(0, 14))], w=1.5, smooth=True)
    E.shape([(bx - 30, by - 38), (bx - 8, by - 62), (bx + 30, by - 50), (bx + 40, by - 38)], smooth=True, hatches=[(40, 2.6, 0.7)], sw=1.5)
    E.line([(bx + 42, by - 38), (bx + 80, by - 22), (bx + 112, by - 14)], w=1.6)
    # the woman, parcels on both arms
    w = adult(E, 468, FL + 20, 500, facing=1, lean=0.06, garment="dress", wash_op=0.8, look=0.9, stride=0.07,
              hands={"near": (540, 760), "far": (528, 790)})
    for (hx, hy), off in ((w["hands"]["near"], 0), (w["hands"]["far"], 30)):
        E.line([(hx, hy), (hx - 10, hy + 28)], w=1.2, smooth=False)
        parcel(E, hx - 40 - off * 0.2, hy + 98 + off * 0.3, 66 - off * 0.5, 64 - off * 0.3, rot=-3 if off else 2)
        hand_dot(E, (hx, hy), 7)
    return _end(E, pess_pip_close())


@suit
def di03(rng):
    """Three: a church hall after the service; women count coins into a tin at a trestle, a man on a ladder
    hangs bunting, and through the open door a priest stands alone in the nave looking at the altar."""
    E = _pip(3, "c", rng)
    FL = 1010
    wall(E, 340, FL, op=0.16)
    fade(E, IX0, 340, IX1, 560, op=0.55, side="t", reach=1.0)
    fade(E, IX0, 340, 230, FL, op=0.45, side="l", reach=1.0)
    # high windows with pointed heads
    for wx in (110, 505):
        E.shape([(wx - 34, 520), (wx - 34, 410), (wx, 366), (wx + 34, 410), (wx + 34, 520)], smooth=False,
                hatches=[(70, 3, 0.6), (-40, 3.4, 0.4)], tint=(iso.SLATE, 0.45), sw=2)
        E.line([(wx, 372), (wx, 520)], w=1.6, smooth=False)
    # the open door to the nave, with the priest
    dx0, dx1, dy0 = 292, 410, 470
    rect(E, dx0 - 12, dy0 - 12, dx1 + 12, FL, sw=2)
    E.shape([(dx0, FL), (dx0, dy0 + 30), ((dx0 + dx1) / 2, dy0), (dx1, dy0 + 30), (dx1, FL)], smooth=False,
            hatches=[(70, 3, 0.55), (-40, 3.4, 0.4)], tint=(iso.SLATE, 0.5), sw=2)
    clip_open(E, dx0, dy0, dx1, FL)
    E.add(f'<rect x="{dx0}" y="{dy0}" width="{dx1 - dx0}" height="{FL - dy0}" fill="{iso.DARK}" opacity="0.55"/>')
    glow(E, 351, 700, 56, 90, 0.5)
    # altar, steps and candles in the distance
    rect(E, 316, 690, 386, 740, hatches=[(0, 3, 0.4)], sw=1.8)
    rect(E, 306, 740, 396, 756, hatches=[(0, 3, 0.4)], sw=1.4)
    rect(E, 296, 756, 406, 772, hatches=[(0, 3, 0.4)], sw=1.4)
    for cx_ in (326, 376):
        rect(E, cx_ - 3, 666, cx_ + 3, 690, sw=1.2)
        iso.flame(E, cx_, 664, 0.6, 1.0)
    E.line([(351, 600), (351, 690)], w=3, smooth=False)
    E.line([(333, 625), (369, 625)], w=3, smooth=False)
    adult(E, 351, 900, 230, view="back", garment="long", hair="dark", wash_op=0.85, look=0.0, tilt=-6)
    E.line([(IX0, 900), (IX1, 900)], w=0.1, op=0, smooth=False)
    clip_close(E)
    E.add(f'<path d="M{dx0},{FL} V{dy0 + 30} L{(dx0 + dx1) / 2},{dy0} L{dx1},{dy0 + 30} V{FL}" fill="none" stroke="{INK}" stroke-width="2"/>')
    # bunting being hung, from the wall at left across to the man on the ladder
    pennants(E, [(70, 410), (170, 462), (300, 496), (440, 540)], 11, 20)
    floor_band(E, FL, 0.16)
    # ladder and the man hanging the bunting
    for lx in (498, 556):
        E.line([(lx, 470), (lx + (10 if lx > 520 else 0), FL)], w=5, smooth=False)
    for k in range(10):
        yy = 520 + k * 50
        E.line([(498, yy), (556 + 10 * (yy - 470) / 540, yy)], w=3.4, smooth=False)
    iso.floor_shadow(E, 530, FL - 2, 60, 8, 0.6)
    m = adult(E, 528, 770, 380, facing=-1, lean=0.04, garment="coat", hair="dark", wash_op=0.85, look=0.9, tilt=-12, stride=0.03,
              hands={"near": (470, 556), "far": (436, 540)})
    for hnd in m["hands"].values():
        hand_dot(E, hnd, 7)
    # trestle with the women and the coins
    TT = 820
    for who, wx, fc, hh in (("a", 112, 1, 440), ("b", 272, -1, 430)):
        adult(E, wx, 900, hh, pose="torso", facing=fc, garment="dress", hair="bun" if who == "a" else "dark", mouth=0.0,
              wash_op=0.8, look=0.9, tilt=14 if who == "a" else -10, lean=0.08,
              hands={"near": (wx + fc * 52, TT - 30), "far": (wx + fc * 76, TT - 24)})
    iso.cast(E, [(78, TT + 20), (306, TT + 20), (316, FL - 2), (70, FL - 2)], 0.6)
    E.shape([(70, TT), (320, TT), (322, TT + 14), (68, TT + 14)], smooth=False, hatches=[(2, 3, 0.3)], sw=1.8)
    E.shape([(76, TT + 14), (316, TT + 14), (326, TT + 130), (66, TT + 130)], smooth=False, hatches=[(90, 5, 0.3)], tone=0.1, sw=1.8)
    for k in range(1, 12):
        xx = 76 + 240 * k / 12
        E.line([(xx, TT + 18), (xx + 2, TT + 126)], w=0.8, op=0.45, smooth=False)
    fade(E, 66, TT + 14, 326, TT + 130, op=0.5, side="b", reach=1.0)
    for lx in (96, 290):
        rect(E, lx - 6, TT + 130, lx + 6, FL, hatches=[(80, 2.6, 0.5)], sw=1.5)
    E.shape([(170, TT - 2), (170, TT - 26), (208, TT - 26), (208, TT - 2)], smooth=False, hatches=[(70, 2.4, 0.45)], sw=1.6)
    rect(E, 164, TT - 32, 214, TT - 24, hatches=[(0, 2, 0.6)], sw=1.4)
    for k in range(5):
        iso.rect(E, 112 + k * 3, TT - 6 - k * 4, 140 + k * 3, TT - 2 - k * 4, tone=0.2, sw=1.0)
    for k in range(6):
        E.shape(ellipse_pts(236 + k * 12, TT - 4, 6, 3, 8), tone=0.1, sw=1.0)
    # cake stall in front
    ST = 930
    E.shape([(280, ST), (606, ST), (610, ST + 12), (276, ST + 12)], smooth=False, hatches=[(2, 3, 0.3)], sw=1.8)
    E.shape([(286, ST + 12), (602, ST + 12), (610, IY1 + 10), (278, IY1 + 10)], smooth=False, hatches=[(90, 5, 0.34)], tone=0.12, sw=1.8)
    for cx_, ch in ((330, 38), (408, 46), (490, 38), (566, 44)):
        rect(E, cx_ - 4, ST - 20, cx_ + 4, ST, sw=1.2)
        E.shape(ellipse_pts(cx_, ST - 22, 28, 6, 12), hatches=[(0, 2.4, 0.4)], sw=1.5)
        rect(E, cx_ - 22, ST - 22 - ch * 0.5, cx_ + 22, ST - 22, hatches=[(70, 2.4, 0.5)], sw=1.5)
        E.shape(ellipse_pts(cx_, ST - 22 - ch * 0.5, 22, 5, 10), sw=1.3)
        E.shape([(cx_ - 20, ST - 24 - ch * 0.5), (cx_ - 14, ST - 24 - ch), (cx_ + 14, ST - 24 - ch), (cx_ + 20, ST - 24 - ch * 0.5)],
                smooth=True, hatches=[(40, 3, 0.2)], sw=1.4)
    return _end(E, pess_pip_close())


@suit
def di04(rng):
    """Four: a crowd waits in the dark outside a shuttered shop, wrapped in coats, some on folding chairs; inside,
    a clerk sets a single object on a pedestal under a lamp; the clock in the square stands at midnight."""
    E = _pip(4, "d", rng)
    FL = 1010
    sky(E, 340, 700, strongest=0.55, weakest=0.1, gap=5, tint=0.95)
    fade(E, IX0, 340, IX1, FL, op=0.4, side="b", reach=1.0)
    # the clock tower in the square, left
    E.shape([(100, 330), (176, 330), (186, 760), (90, 760)], smooth=False, hatches=[(80, 3, 0.4), (-40, 3.6, 0.3)], sw=2)
    E.shape([(90, 760), (186, 760), (196, 1010), (80, 1010)], smooth=False, hatches=[(80, 3, 0.4)], sw=2)
    fade(E, 90, 330, 196, 1010, op=0.6, side="l", reach=1.0)
    cxk, cyk = 138, 480
    E.shape(ellipse_pts(cxk, cyk, 46, 46, 24), hatches=[(0, 3, 0.15)], sw=2.6)
    for k in range(12):
        a = k * math.pi / 6
        E.line([(cxk + 34 * math.sin(a), cyk - 34 * math.cos(a)), (cxk + 41 * math.sin(a), cyk - 41 * math.cos(a))], w=1.6, smooth=False)
    E.line([(cxk, cyk), (cxk, cyk - 26)], w=3.4, smooth=False)
    E.line([(cxk, cyk), (cxk, cyk - 36)], w=2.2, smooth=False)
    E.add(f'<circle cx="{cxk}" cy="{cyk}" r="3.6" fill="{INK}"/>')
    # the shop: dark front, shuttered door at left, lit window at right with the clerk and pedestal
    sx0, sx1, sy0 = 250, 610, 470
    mass(E, [(sx0, sy0), (sx1, sy0), (sx1, 1010), (sx0, 1010)], solid=0.5, wash=0.3, sw=2)
    rect(E, sx0 - 6, sy0 - 24, sx1 + 6, sy0, hatches=[(0, 3, 0.7)], sw=2)
    for k in range(14):                       # the roller shutter over the door
        E.line([(276, 700 + k * 22), (352, 700 + k * 22)], w=1.4, op=0.6, color=PAPER_FILL, smooth=False)
    rect(E, 270, 690, 358, 1010, fill=None, sw=2.2)
    wx0, wx1, wy0, wy1 = 388, 584, 530, 760
    rect(E, wx0 - 12, wy0 - 12, wx1 + 12, wy1 + 12, sw=2)
    rect(E, wx0, wy0, wx1, wy1, hatches=[(0, 5, 0.1)], sw=2)
    glow(E, 486, 670, 120, 110, 0.7)
    E.line([(486, wy0), (486, wy0 + 46)], w=1.6, smooth=False)
    E.shape([(458, wy0 + 76), (514, wy0 + 76), (500, wy0 + 46), (472, wy0 + 46)], smooth=False, hatches=[(70, 2.4, 0.6)], sw=1.8)
    glow(E, 486, wy0 + 96, 40, 30, 0.6)
    rect(E, 460, 690, 512, wy1, hatches=[(80, 3, 0.4)], sw=2)
    rect(E, 452, 680, 520, 692, hatches=[(0, 2.4, 0.5)], sw=1.8)
    E.shape(ellipse_pts(486, 652, 20, 22, 14), hatches=[(40, 3, 0.3)], sw=2)
    E.shape([(477, 634), (495, 634), (492, 622), (480, 622)], smooth=False, sw=1.4)
    clerk = adult(E, 566, wy1, 280, facing=-1, lean=0.14, garment="vest", hair="dark", wash_op=0.85, look=0.9,
                  hands={"near": (516, 650), "far": (520, 656)})
    hand_dot(E, clerk["hands"]["near"], 6, math.pi)
    floor_band(E, FL, 0.18)
    # the crowd outside, standing, backs to us
    crowd = [(226, "adult", 340, "top"), (322, "elder", 320, "bonnet"), (410, "adult", 350, "top"), (498, "youth", 330, None),
             (578, "elder", 310, "bonnet")]
    for x_, *_ in crowd:
        iso.floor_shadow(E, x_, FL + 4, 44, 7, 0.6)
    for x_, kd, hh, ht in crowd:
        fn = {"adult": adult, "elder": elder, "youth": youth}[kd]
        fn(E, x_, FL + 8, hh, view="back", garment="long" if kd == "elder" else "coat",
           hair="white" if kd == "elder" else "dark", hat=ht, wash_op=0.85)
    # folding chairs in front, with sitters
    for cx_, ht in ((130, "bonnet"), (310, "top")):
        chair_side(E, cx_, IY1 - 6, seat=80, f_dir=1, back_h=150, w=76)
        adult(E, cx_ - 2, IY1 - 6, 330, pose="sit", facing=1, lean=0.2, garment="long", hair="dark", wash_op=0.85,
              look=0.9, tilt=4, hat=ht)
    return _end(E, pess_pip_close())


def hourglass(E, x, y, s=1.0):
    """An upright hourglass standing with its base at (x, y): caps, two bulbs, sand."""
    rect(E, x - 20 * s, y - 6 * s, x + 20 * s, y, hatches=[(0, 2, 0.7)], sw=1.4)
    rect(E, x - 20 * s, y - 84 * s, x + 20 * s, y - 78 * s, hatches=[(0, 2, 0.7)], sw=1.4)
    for sg in (-1, 1):
        E.line([(x + sg * 18 * s, y - 6 * s), (x + sg * 18 * s, y - 78 * s)], w=2.2, smooth=False)
    E.shape([(x - 15 * s, y - 78 * s), (x + 15 * s, y - 78 * s), (x + 3 * s, y - 44 * s), (x - 3 * s, y - 44 * s)], smooth=False, sw=1.4)
    E.shape([(x - 3 * s, y - 40 * s), (x + 3 * s, y - 40 * s), (x + 15 * s, y - 8 * s), (x - 15 * s, y - 8 * s)], smooth=False, sw=1.4)
    E.shape([(x - 11 * s, y - 14 * s), (x + 11 * s, y - 14 * s), (x + 14 * s, y - 9 * s), (x - 14 * s, y - 9 * s), (x - 6 * s, y - 22 * s)],
            smooth=False, hatches=[(0, 1.9, 0.85)], sw=0.9)


def sheet(E, x, y, w=60, h=40, rot=0, lines=3, tone=0.0):
    """A loose sheet of paper lying flat, centred at (x, y), with ruled lines and no writing."""
    E.add(f'<g transform="rotate({rot} {f(x)} {f(y)})">')
    E.shape([(x - w / 2, y - h / 2 + 4), (x + w / 2, y - h / 2), (x + w / 2 + 4, y + h / 2 - 3), (x - w / 2 + 2, y + h / 2)],
            smooth=False, tone=tone, sw=1.2)
    for k in range(1, lines + 1):
        yy = y - h / 2 + h * k / (lines + 1)
        E.line([(x - w / 2 + 8, yy + 1), (x + w / 2 - 8, yy - 1)], w=0.6, op=0.5, smooth=False)
    E.add("</g>")


@suit
def di05(rng):
    """Five: a clerk at a desk heaped with papers that spill to the floor and climb the walls; a boy carries in
    another pile; on the sill, half hidden by a ledger, a small hourglass."""
    E = _pip(5, "e", rng)
    FL = 1010
    wall(E, 340, FL, op=0.16)
    fade(E, IX0, 340, IX1, 560, op=0.5, side="t", reach=1.0)
    fade(E, IX0, 340, 300, FL, op=0.55, side="l", reach=1.0)
    # window on the right, with ledger and hourglass on the sill
    window(E, 440, 400, 580, 640, tone=0.55, panes=(1, 2))
    hourglass(E, 540, 650, 1.0)
    book(E, 468, 650, 76, 16, hatch=(70, 2.6, 0.5), cover=0.6)
    book(E, 478, 634, 62, 14, hatch=(70, 2.6, 0.5), cover=0.4)
    # papers climbing the left wall: shelves heaped with stacks, sheets pinned between
    for sy in (500, 640, 780):
        rect(E, IX0, sy, 250, sy + 10, hatches=[(0, 3, 0.4)], sw=1.8)
        x = IX0 + 4
        while x < 240:
            hh = rng.uniform(40, 112)
            ww = rng.uniform(26, 44)
            iso.stack_of_papers(E, x, min(x + ww, 246), sy, max(2, int(hh / 17)), rng, 17)
            x += ww + rng.uniform(2, 8)
    for k in range(8):
        sheet(E, 290 + k * 16 % 100, 420 + k * 54 % 300, 54, 36, rot=rng.uniform(-8, 8))
    floor_band(E, FL, 0.16)
    # the clerk and the desk
    iso.floor_shadow(E, 330, FL - 2, 200, 12, 0.6)
    chair_side(E, 170, FL, seat=125, f_dir=1, back_h=200, w=100)
    cl = adult(E, 188, FL, 500, pose="sit", facing=1, lean=0.3, tilt=14, garment="coat", hair="dark", wash_op=0.8,
               hands={"near": (330, 760), "far": (306, 772)})
    px, py = cl["hands"]["near"]
    E.line([(px - 4, py + 4), (px + 24, py - 30)], w=2, smooth=False)
    TOP = 790
    iso.cast(E, [(250, TOP + 18), (500, TOP + 18), (506, FL - 2), (246, FL - 2)], 0.6)
    table_front(E, 245, 505, TOP, FL, thick=22, legs=(0.06, 0.94))
    # the heap on the desk: slabs of paper, out of true, and a lean-to of sheets sliding off the edge
    base = TOP
    for k in range(7):
        dx = rng.uniform(-12, 12)
        x0, x1 = 290 + dx, 470 + dx + rng.uniform(-10, 10)
        iso.rect(E, x0, base - 14, x1, base, hatches=[(0, 3.6, 0.12 + 0.08 * (k % 3))], sw=1.4)
        E.line([(x0 + 4, base - 7), (x1 - 4, base - 7)], w=0.7, op=0.6, smooth=False)
        base -= 14
    E.shape([(470, TOP - 70), (516, TOP - 2), (470, TOP - 2)], smooth=False, hatches=[(0, 3, 0.4)], sw=1.4)
    for k, (sx_, sy_) in enumerate(((528, FL - 20), (564, FL - 8), (486, FL - 8), (560, FL - 36), (300, FL + 24), (230, FL + 30))):
        sheet(E, sx_, sy_ + 6, 64, 40, rot=rng.uniform(-30, 30))
    iso.rect(E, 258, TOP - 4, 290, TOP, sw=1.0)
    hand_dot(E, (px, py), 7, -0.6)
    # the boy with another pile
    pile_x = 556
    b = child(E, 562, FL + 14, 330, facing=-1, garment="smock", wash_op=0.85, look=0.9, stride=0.06, tilt=-4,
              hands={"near": (pile_x - 44, 836), "far": (pile_x - 30, 826)})
    px_, py_ = b["hands"]["near"]
    ytop = py_ - 118
    for k in range(9):
        dx = rng.uniform(-4, 4)
        iso.rect(E, px_ - 6 + dx, py_ - 10 - k * 13, px_ + 56 + dx, py_ + 2 - k * 13, hatches=[(0, 3.6, 0.1 + 0.08 * (k % 3))], sw=1.3)
    for hnd in b["hands"].values():
        hand_dot(E, hnd, 6, math.pi)
    return _end(E, pess_pip_close())


@suit
def di06(rng):
    """Six: a man in a railway waiting room reads a newspaper, folds it, takes out another; a pendulum clock
    swings behind glass over his head, and the travellers on the benches do much the same."""
    E = _pip(6, "f", rng)
    FL = 1010
    wall(E, 340, FL, op=0.16)
    fade(E, IX0, 340, IX1, 600, op=0.55, side="t", reach=1.0)
    fade(E, IX0, 340, 200, FL, op=0.5, side="l", reach=1.0)
    fade(E, 450, 340, IX1, FL, op=0.5, side="r", reach=1.0)
    # dado: dark panelling below, rail above
    mass(E, [(IX0, 820), (IX1, 820), (IX1, FL), (IX0, FL)], solid=0.35, wash=0.3, sw=1.6)
    rect(E, IX0, 812, IX1, 824, hatches=[(0, 2.4, 0.5)], sw=1.8)
    # the clock case with a swinging pendulum behind glass
    cx = 212
    rect(E, cx - 52, 420, cx + 52, 640, hatches=[(80, 3, 0.4)], sw=2.4)
    E.shape([(cx - 60, 420), (cx - 44, 372), (cx + 44, 372), (cx + 60, 420)], smooth=False, hatches=[(0, 3, 0.4)], sw=2)
    E.shape(ellipse_pts(cx, 396, 36, 36, 22), hatches=[(60, 3, 0.18)], sw=2.2)
    for k in range(12):
        a = k * math.pi / 6
        E.line([(cx + 25 * math.sin(a), 396 - 25 * math.cos(a)), (cx + 31 * math.sin(a), 396 - 31 * math.cos(a))], w=1.4, smooth=False)
    E.line([(cx, 396), (cx + 8, 372)], w=2.6, smooth=False)
    E.line([(cx, 396), (cx - 14, 408)], w=2, smooth=False)
    rect(E, cx - 40, 446, cx + 40, 622, tint=(iso.SLATE, 0.5), tone=0.5, sw=1.8)
    iso.fade(E, cx - 40, 446, cx + 40, 622, op=0.9, side="t", reach=1.0, colour=iso.DARK, clip=[(cx - 40, 446), (cx + 40, 446), (cx + 40, 622), (cx - 40, 622)])
    E.line([(cx, 452), (cx + 26, 586)], w=2, smooth=False)
    E.shape(ellipse_pts(cx + 26, 598, 15, 15, 12), hatches=[(60, 2, 0.4)], sw=1.8)
    E.line([(cx - 36, 466), (cx - 30, 604)], w=2.6, op=0.4, color="#ffffff", smooth=False)
    # a notice board and a stove, quiet things on the wall
    rect(E, 420, 420, 592, 600, hatches=[(45, 5, 0.2)], sw=2.2)
    for r_ in range(2):
        for c_ in range(4):
            cx_, cy_ = 450 + c_ * 40, 460 + r_ * 70
            rect(E, cx_ - 14, cy_ - 22, cx_ + 14, cy_ + 22, sw=1.1)
            for k in range(1, 4):
                E.line([(cx_ - 9, cy_ - 22 + k * 11), (cx_ + 9, cy_ - 22 + k * 11)], w=0.7, op=0.55, smooth=False)
    floor_band(E, FL, 0.16)
    # the bench along the wall
    for lx in (110, 340, 570):
        rect(E, lx - 6, 905, lx + 6, FL, hatches=[(80, 2.6, 0.5)], sw=1.6)
    for yy in (700, 740, 780):
        rect(E, 84, yy, 600, yy + 22, hatches=[(0, 3, 0.4)], sw=1.5)
    for ux in (96, 340, 590):
        rect(E, ux - 5, 690, ux + 5, 815, hatches=[(80, 2.6, 0.5)], sw=1.5)
    # travellers further along, each with a paper
    for x_, fc, hh in ((402, 1, 400), (506, 1, 370)):
        t = adult(E, x_, FL - 20, hh, pose="sit", facing=fc, lean=0.18, garment="coat" if x_ < 450 else "dress",
                  hair="dark" if x_ < 450 else "bun", hat="top" if x_ < 450 else None, wash_op=0.8, look=0.6,
                  hands={"near": (x_ + 0.18 * hh, FL - 20 - 0.5 * hh), "far": (x_ + 0.17 * hh, FL - 20 - 0.45 * hh)})
        hx, hy = t["hands"]["near"]
        newspaper(E, hx + 18, hy - 14, 56, 76, rot=-6, cols=3, cover=0.1)
        for hnd in t["hands"].values():
            hand_dot(E, hnd, 6)
    rect(E, 84, 884, 600, 902, hatches=[(2, 3, 0.4)], sw=1.8)
    # the man himself: one paper open before him, a second held ready
    m = adult(E, 196, FL - 20, 520, pose="sit", facing=1, lean=0.2, garment="coat", hair="dark", wash_op=0.8, look=0.7, tilt=-6,
              hands={"near": (282, 770), "far": (270, 840)})
    hx, hy = m["hands"]["near"]
    newspaper(E, hx + 20, hy - 26, 70, 100, rot=-8, cols=4, cover=0.12)
    fx, fy = m["hands"]["far"]
    newspaper(E, fx + 24, fy + 8, 52, 32, rot=6, cols=2, cover=0.2)
    for hnd in m["hands"].values():
        hand_dot(E, hnd, 7)
    return _end(E, pess_pip_close())


def storm_bank(E, x0, x1, y, top, rng):
    """A bank of black cloud rising over the horizon: overlapping domes of dense cross-hatching."""
    for k in range(14):
        cx = x0 + (x1 - x0) * k / 13 + rng.uniform(-14, 14)
        r = rng.uniform(34, 64) * (1.2 - abs(k - 7) / 14)
        cy = y - r * 0.5 - rng.uniform(0, (y - top) * 0.7) * (1 - abs(k - 7) / 9)
        pts = ellipse_pts(cx, cy, r * 1.3, r, 16)
        mass(E, pts, solid=0.45, smooth=True, wash=0.3, sw=1.6)
    mass(E, [(x0, y), (x1, y), (x1, y - 30), (x0, y - 30)], solid=0.5, sw=1.2)


def striped(E, x0, y0, x1, y1, n):
    """A striped canvas panel: alternate stripes dark and paper."""
    w = (x1 - x0) / n
    for k in range(n):
        if k % 2:
            rect(E, x0 + k * w, y0, x0 + (k + 1) * w, y1, hatches=[(80, 3, 0.2)], sw=1.0)
        else:
            mass(E, [(x0 + k * w, y0), (x0 + (k + 1) * w, y0), (x0 + (k + 1) * w, y1), (x0 + k * w, y1)], solid=0.35, sw=1.0)


def ball(E, x, y, r):
    E.shape(ellipse_pts(x, y, r, r, 16), hatches=[(60, 3, 0.4, (x, y - r, x + r, y + r))], sw=2)
    for a in (0, 2.1, 4.2):
        E.line([(x + r * math.cos(a), y + r * math.sin(a)), (x + r * 0.3 * math.cos(a + 1.0), y + r * 0.3 * math.sin(a + 1.0))], w=1.3, smooth=False)


def radio(E, x, y, w=70, h=48, aerial=True):
    """A small portable radio standing with its base-left at (x, y): case, dial and grille, aerial."""
    rect(E, x, y - h, x + w, y, hatches=[(80, 3, 0.45)], sw=2)
    E.shape(ellipse_pts(x + w * 0.28, y - h * 0.5, h * 0.3, h * 0.3, 12), sw=1.4)
    for k in range(5):
        E.line([(x + w * 0.58, y - h + 10 + k * 7), (x + w * 0.9, y - h + 10 + k * 7)], w=1.0, op=0.8, smooth=False)
    if aerial:
        E.line([(x + w * 0.85, y - h), (x + w * 1.1, y - h - 56)], w=1.5, smooth=False)
    for k in (-1, 1):   # sound drawn as arcs, no letters
        E.line([(x + w * 1.12, y - h * 0.5 + k * 8), (x + w * 1.22, y - h * 0.5 + k * 16), (x + w * 1.1, y - h * 0.5 + k * 24)], w=1.1, op=0.7)


def deckchair(E, x, floor, fd=1):
    """A deck chair in profile, striped seat, front at +fd."""
    sx = x
    E.line([(sx - fd * 40, floor), (sx + fd * 10, floor - 90), (sx + fd * 40, floor)], w=3.2, smooth=False)
    E.shape([(sx - fd * 44, floor - 64), (sx + fd * 40, floor - 54), (sx + fd * 40, floor - 44), (sx - fd * 44, floor - 54)], smooth=False,
            hatches=[(90, 3, 0.5)], sw=1.8)
    E.shape([(sx - fd * 46, floor - 56), (sx - fd * 74, floor - 140), (sx - fd * 60, floor - 148), (sx - fd * 36, floor - 64)],
            smooth=False, hatches=[(90, 3, 0.5)], sw=1.8)


@suit
def di07(rng):
    """Seven: a family on a crowded beach under a striped awning, a radio playing, children shrieking at a
    ball; on the horizon a bank of black cloud over the water; only the lifeguard on his high chair has turned
    to look."""
    E = _pip(7, "g", rng)
    HOR = 560
    SAND = 690
    sky(E, 340, HOR, strongest=0.45, weakest=0.06, gap=6, tint=0.7)
    storm_bank(E, 70, 610, HOR, 430, rng)
    # sea
    E.shape([(IX0, HOR), (IX1, HOR), (IX1, SAND), (IX0, SAND)], smooth=False, hatches=[(1, 4.4, 0.28)], tone=0.2, outline=False)
    for k in range(7):
        yy = HOR + 10 + k * 18
        d = f"M{IX0},{f(yy)} " + " ".join(f"q{f(10 + k)},{f(-4 - k * 0.5)} {f(20 + 2 * k)},0" for _ in range(int(540 / (20 + 2 * k))))
        E.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="0.8" opacity="0.45"/>')
    fade(E, IX0, HOR, IX1, SAND, op=0.45, side="t", reach=1.0)
    E.line([(IX0, HOR), (IX1, HOR)], w=1.4, smooth=False)
    # sand, and the crowd: small figures and umbrellas along the shore
    gap, yy, d = 3.6, SAND + 4, []
    while yy < IY1 + 6:
        d.append(f"M{IX0},{f(yy)} L{IX1},{f(yy + rng.uniform(-0.8, 0.8))}")
        yy += gap
        gap *= 1.03
    E.add(f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width="0.6" opacity="0.35" fill="none"/>')
    fade(E, IX0, SAND, IX1, IY1, op=0.55, side="b", reach=1.0)
    for ux, uy in ((250, 740), (400, 720), (330, 760)):
        E.line([(ux, uy), (ux + 2, uy - 54)], w=1.6, smooth=False)
        E.shape([(ux - 34, uy - 46), (ux - 14, uy - 66), (ux + 18, uy - 66), (ux + 36, uy - 46)], smooth=False,
                hatches=[(80, 2.4, 0.6)], sw=1.4)
    for fx, fy, fk in ((290, 730, "adult"), (360, 740, "youth"), (440, 732, "child"), (205, 725, "adult")):
        {"adult": adult, "youth": youth, "child": child}[fk](E, fx, fy, 130, view="back", garment="dress", wash_op=0.8)
    # awning on the left: striped canopy on two poles, a family under it
    for px in (96, 322):
        E.line([(px, 640), (px + (4 if px > 200 else -4), 1020)], w=5, smooth=False)
    canopy = [(70, 668), (112, 600), (300, 600), (344, 668)]
    E.shape(canopy, smooth=False, hatches=[(80, 3, 0.15)], sw=2.2)
    cid = E.uid("q")
    E.add(f'<clipPath id="{cid}"><path d="{iso._poly(canopy)}"/></clipPath><g clip-path="url(#{cid})">')
    for k in range(0, 8, 2):
        x0 = 70 + k * 35
        mass(E, [(x0, 596), (x0 + 35, 596), (x0 + 35, 672), (x0, 672)], solid=0.4, sw=1.0)
    E.add("</g>")
    for k in range(7):
        x0 = 70 + k * 39
        E.shape([(x0, 668), (x0 + 39, 668), (x0 + 39, 678), (x0 + 19, 690), (x0, 678)], smooth=False,
                hatches=[(80, 3, 0.2)] if k % 2 else [(70, 1.9, 0.85)], sw=1.3)
    fade(E, 70, 600, 344, IY1, op=0.5, side="b", reach=1.0)
    FL = 1010
    iso.floor_shadow(E, 200, FL + 6, 150, 12, 0.6)
    deckchair(E, 170, FL, 1)
    mom = adult(E, 170, FL, 470, pose="sit", facing=1, lean=0.14, garment="dress", hair="bun", wash_op=0.7, look=0.9, tilt=-4,
                hands={"near": (200, 820), "far": (190, 830)})
    radio(E, 262, FL + 4, 72, 50)
    for hnd in mom["hands"].values():
        hand_dot(E, hnd, 6)
    # children and the ball
    for kx, fc, tl in ((388, -1, -10), (508, 1, 12)):
        c = child(E, kx, FL + 10, 270, facing=fc, garment="smock", wash_op=0.8, mouth=1.0, look=0.9, tilt=tl,
                  hands={"near": (kx + fc * 52, 790), "far": (kx + fc * 36, 780)})
        for hnd in c["hands"].values():
            hand_dot(E, hnd, 6)
    ball(E, 448, 770, 22)
    # lifeguard high chair, right
    for lx in (546, 596):
        E.line([(lx, 780), (lx + (-8 if lx < 570 else 8), IY1 - 20)], w=5, smooth=False)
    E.line([(540, 940), (604, 940)], w=3, smooth=False)
    rect(E, 530, 770, 612, 788, hatches=[(0, 3, 0.4)], sw=2)
    lg = adult(E, 574, 770, 270, view="back", pose="torso", garment="vest", hair="dark", hat="wide", wash_op=0.85, look=0.0, tilt=10)
    return _end(E, pess_pip_close())


def porcupine(E, x, y, s=1.0, fd=1, bowed=0.6):
    """A porcupine seated on its haunches, feet at (x, y), head bowed toward fd: round body bristling with
    quills, small face, forepaws."""
    cx, cy = x - fd * 8 * s, y - 40 * s
    # quills first, so the body sits over their roots
    for k in range(30):
        a = math.pi * (0.95 - 1.05 * k / 29) if fd == 1 else math.pi * (0.05 + 1.05 * k / 29)
        a = math.pi - a if fd == 1 else a
        ang = -math.pi / 2 + (k - 14.5) / 14.5 * 1.9
        ang = ang if fd == 1 else -math.pi - ang
        r0, r1 = 34 * s, (54 + (k % 3) * 8) * s
        sx, sy = cx - fd * 6 * s + math.cos(ang) * r0 * 0.9, cy + math.sin(ang) * r0 * 0.75
        ex, ey = cx - fd * 6 * s + math.cos(ang) * r1, cy + math.sin(ang) * r1 * 0.85
        if ey > y - 6 * s:
            continue
        E.line([(sx, sy), (ex, ey)], w=1.8, smooth=False, op=0.9)
    E.shape(ellipse_pts(cx, cy, 36 * s, 34 * s, 16), hatches=[(60, 2.4, 0.7), (-50, 2.8, 0.5)], sw=2)
    E.shape([(cx + fd * 26 * s, cy - 6 * s), (cx + fd * 60 * s, cy + 10 * s * bowed + 6 * s), (cx + fd * 58 * s, cy + 24 * s), (cx + fd * 28 * s, cy + 20 * s)],
            smooth=True, hatches=[(40, 3, 0.35)], sw=1.8)
    E.add(f'<circle cx="{f(cx + fd * 62 * s)}" cy="{f(cy + 18 * s)}" r="{f(3 * s)}" fill="{INK}"/>')
    E.add(f'<circle cx="{f(cx + fd * 46 * s)}" cy="{f(cy + 8 * s)}" r="{f(2.2 * s)}" fill="{INK}"/>')
    E.shape([(cx + fd * 6 * s, cy + 20 * s), (cx + fd * 40 * s, cy + 28 * s), (cx + fd * 38 * s, y - 4 * s), (cx + fd * 8 * s, y - 4 * s)],
            smooth=False, hatches=[(70, 2.4, 0.5)], sw=1.6)
    E.shape(ellipse_pts(cx + fd * 6 * s, y - 4 * s, 22 * s, 7 * s, 10), hatches=[(0, 2, 0.6)], sw=1.5)


@suit
def di08(rng):
    """Eight: a long table crowded with guests, every mouth open and every glass raised, each turned half toward a
    neighbour and half toward the next sound; at the far end two porcupines sit still on the cloth, eating from the
    same dish."""
    E = _pip(8, "h", rng)
    FL = 1010
    TOP = 840
    wall(E, 340, FL, op=0.18)
    fade(E, IX0, 340, IX1, 640, op=0.55, side="t", reach=1.0)
    fade(E, IX0, 340, 200, FL, op=0.45, side="l", reach=1.0)
    # garland of lamps across the room
    E.line([(IX0, 380), (200, 420), (340, 432), (480, 420), (IX1, 380)], w=1.4)
    for lx, ly in ((150, 412), (300, 430), (430, 428), (560, 396)):
        iso.lantern(E, lx, ly, 0.7)
    # second row of guests behind, smaller
    for x_, tl, lk in ((140, 8, 0.6), (236, -8, -0.6), (332, 8, 0.6), (428, -8, -0.6)):
        g = adult(E, x_, 880, 330, view="front", pose="torso", garment="coat", hair="dark", wash_op=0.9, mouth=0.9, tilt=tl, look=lk,
                  hands={"left": (x_ - 36, 640), "right": (x_ + 40, 760)})
        iso.hold_glass(E, g["hands"]["left"], 0.4, 0.5)
    # front row
    for x_, tl, lk, gm, hr in ((92, 10, 0.7, "dress", "bun"), (188, -12, -0.7, "coat", "dark"), (284, 14, 0.7, "dress", "dark"),
                               (380, -10, -0.7, "coat", "dark")):
        g = adult(E, x_, 930, 440, view="front", pose="torso", garment=gm, hair=hr, wash_op=0.78, mouth=1.0, tilt=tl, look=lk,
                  hands={"left": (x_ - 36, 706, -1), "right": (x_ + 38, 840)})
        iso.hold_glass(E, g["hands"]["left"], 0.52, 0.55)
        hand_dot(E, g["hands"]["right"], 6)
    # table top in perspective, and the cloth to the floor
    iso.cast(E, [(60, TOP + 20), (620, TOP + 20), (630, FL), (50, FL)], 0.55)
    E.shape([(66, TOP), (614, TOP), (632, TOP + 36), (48, TOP + 36)], smooth=False, hatches=[(0, 5, 0.22)], sw=1.8)
    E.shape([(48, TOP + 36), (632, TOP + 36), (640, 1070), (40, 1070)], smooth=False, hatches=[(90, 6, 0.38)], tone=0.12, sw=1.8)
    fade(E, 40, TOP + 36, 640, 1070, op=0.75, side="b", reach=1.0)
    for k in range(1, 22):
        xx = 48 + 584 * k / 22
        E.line([(xx, TOP + 40), (xx + (3 if k % 2 else -3), 1066)], w=0.8, op=0.5, smooth=False)
    # things on the table
    for px in (60, 140, 236, 332):
        E.shape(ellipse_pts(px, TOP + 16, 36, 7, 14), hatches=[(0, 2.6, 0.4)], sw=1.4)
    for px in (140, 236, 332):
        iso.wine_glass(E, px, TOP + 22, 0.7, fill=0.5)
    # the far end: two porcupines and the shared dish
    glow(E, 520, TOP - 20, 80, 60, 0.4)
    E.shape(ellipse_pts(516, TOP + 8, 34, 8, 14), hatches=[(0, 2.4, 0.4)], sw=1.8)
    E.shape([(496, TOP + 6), (499, TOP - 8), (533, TOP - 8), (536, TOP + 6)], smooth=False, hatches=[(70, 2.4, 0.5)], sw=1.6)
    porcupine(E, 458, TOP + 8, 0.64, 1)
    porcupine(E, 578, TOP + 8, 0.64, -1)
    return _end(E, pess_pip_close())


def china_shards(E, x0, y0, x1, y1, rng, tone, n=7):
    """n broken pieces of china lying in a tray, of one colour (tone) and several sizes."""
    for _ in range(n):
        cx = rng.uniform(x0 + 8, x1 - 8)
        cy = rng.uniform(y0 + 4, y1 - 4)
        r = rng.uniform(4, 9)
        pts = [(cx + math.cos(a) * r * rng.uniform(0.6, 1.2), cy + math.sin(a) * r * 0.6 * rng.uniform(0.6, 1.2))
               for a in sorted(rng.uniform(0, 2 * math.pi) for _ in range(4))]
        E.shape(pts, smooth=False, tone=tone, sw=1.0, hatches=[(30, 1.8, 0.8)] if tone > 0.4 else [])


def tray(E, x0, y0, x1, y1, rng, tone):
    """A shallow tray seen from above and in front, holding shards."""
    E.shape([(x0 + 6, y0), (x1 - 6, y0), (x1, y1), (x0, y1)], smooth=False, hatches=[(0, 3.4, 0.3)], sw=1.6)
    E.shape([(x0 + 12, y0 + 5), (x1 - 12, y0 + 5), (x1 - 6, y1 - 5), (x0 + 6, y1 - 5)], smooth=False, fill=PAPER_FILL, tone=0.18, sw=1.0)
    china_shards(E, x0 + 12, y0 + 5, x1 - 12, y1 - 5, rng, tone)


@suit
def di09(rng):
    """Nine: a man at a long workbench sorts broken china into shallow trays by colour and size; trays cover every
    surface; on the wall behind him hangs an empty frame."""
    E = _pip(9, "i", rng)
    FL = 1010
    wall(E, 340, FL, op=0.16)
    fade(E, IX0, 340, IX1, 600, op=0.5, side="t", reach=1.0)
    fade(E, IX0, 340, 160, FL, op=0.5, side="l", reach=1.0)
    fade(E, 520, 340, IX1, FL, op=0.45, side="r", reach=1.0)
    # the empty frame behind him
    fx0, fy0, fx1, fy1 = 200, 390, 480, 650
    E.line([(340, 340), (fx0 + 10, fy0 + 6), (340, 340), (fx1 - 10, fy0 + 6)], w=1.0, op=0.7, smooth=False)
    rect(E, fx0, fy0, fx1, fy1, hatches=[(45, 4, 0.5)], sw=2.6)
    rect(E, fx0 + 18, fy0 + 18, fx1 - 18, fy1 - 18, sw=2)
    rect(E, fx0 + 30, fy0 + 30, fx1 - 30, fy1 - 30, hatches=[(0, 9, 0.14)], sw=1.6)
    E.line([(fx0 + 30, fy1 - 30), (fx0 + 40, fy1 - 36)], w=1.2, smooth=False)
    # shelves of trays on the side walls
    for sx0, sx1 in ((IX0, 176), (506, IX1)):
        for sy in (470, 590, 710):
            rect(E, sx0, sy, sx1, sy + 8, hatches=[(0, 3, 0.4)], sw=1.6)
            x = sx0 + 6
            while x < sx1 - 30:
                rect(E, x, sy - 22, x + 36, sy, hatches=[(0, 3, 0.3)], sw=1.4)
                china_shards(E, x + 4, sy - 22, x + 32, sy - 8, rng, rng.choice((0.1, 0.35, 0.6)), 3)
                x += 40
    floor_band(E, FL, 0.16)
    # the bench: a long top covered with trays, front board, legs
    for lx in (96, 340, 584):
        rect(E, lx - 8, 968, lx + 8, FL, hatches=[(80, 2.6, 0.5)], sw=1.6)
    mass(E, [(70, 968), (610, 968), (610, FL), (70, FL)], solid=0.5, sw=1.4)
    man = adult(E, 340, 960, 600, view="front", pose="torso", garment="vest", hair="dark", wash_op=0.8, look=0.0, tilt=-4,
                hands={"left": (266, 884), "right": (414, 890)})
    E.shape([(70, 850), (610, 850), (630, 950), (50, 950)], smooth=False, hatches=[(2, 4, 0.2)], sw=2)
    E.shape([(50, 950), (630, 950), (630, 968), (50, 968)], smooth=False, hatches=[(0, 3, 0.4)], sw=2)
    tones = (0.08, 0.2, 0.35, 0.6, 0.8)
    k = 0
    for row, (y0, y1, wd, n) in enumerate(((858, 886, 76, 6), (894, 920, 100, 5), (924, 948, 110, 5))):
        gap = (540 - n * wd) / (n + 1)
        for c in range(n):
            x0 = 70 + gap + c * (wd + gap)
            tray(E, x0, y0, x0 + wd, y1, rng, tones[k % 5])
            k += 1
    for hnd in man["hands"].values():
        hand_dot(E, hnd, 7)
    # a china shard in each hand, held up for sorting
    for hx, hy in man["hands"].values():
        E.shape([(hx - 3, hy - 14), (hx + 10, hy - 10), (hx + 4, hy - 2)], smooth=False, tone=0.5, sw=1.2)
    return _end(E, pess_pip_close())


@suit
def di10(rng):
    """Ten: a man lies awake in bed in a small room, lit by the blue flicker of a screen held above his face; across
    the street another window glows blue, and beyond it a row of others."""
    E = _pip(10, "j", rng)
    FL = 1010
    wall(E, 340, FL, op=0.16)
    fade(E, IX0, 340, IX1, FL, op=0.8, side="t", reach=1.0)
    fade(E, IX0, 340, 330, FL, op=0.7, side="l", reach=1.0)
    fade(E, 330, 340, IX1, FL, op=0.45, side="l", reach=1.0)
    # the window onto the street: facade opposite, one blue window, others receding beyond it
    wx0, wy0, wx1, wy1 = 396, 400, 596, 780
    rect(E, wx0 - 10, wy0 - 10, wx1 + 10, wy1 + 10, sw=2)
    rect(E, wx0, wy0, wx1, wy1, hatches=[(0, 3, 0.1)], tint=(iso.SLATE, 0.5), tone=0.7, sw=1.8)
    iso.fade(E, wx0, wy0, wx1, wy1, op=0.9, side="t", reach=1.0, colour=iso.DARK, clip=[(wx0, wy0), (wx1, wy0), (wx1, wy1), (wx0, wy1)])
    clip_open(E, wx0, wy0, wx1, wy1)
    E.add(f'<rect x="{wx0}" y="{wy0 + 150}" width="{wx1 - wx0}" height="{wy1 - wy0 - 150}" fill="{iso.DARK}" opacity="0.75"/>')
    wins = [(412, 560, 84, 120), (520, 580, 64, 90), (586, 596, 46, 66)]
    for k, (x, y, w, h) in enumerate(wins):
        E.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER_FILL}" opacity="0.5"/>')
        rect(E, x, y, x + w, y + h, fill=None, sw=1.6)
        E.add(f'<rect x="{x + 3}" y="{y + 3}" width="{w - 6}" height="{h - 6}" fill="{BLUE}" opacity="{0.9 - 0.18 * k:.2f}"/>')
        E.line([(x + w / 2, y), (x + w / 2, y + h)], w=1.2, smooth=False)
        E.line([(x, y + h * 0.5), (x + w, y + h * 0.5)], w=1.2, smooth=False)
        glow(E, x + w / 2, y + h / 2, w, h * 0.8, 0.35, BLUE)
    for x, y in ((420, 450), (500, 470), (560, 440), (440, 720), (540, 700), (590, 740), (470, 680)):
        E.add(f'<rect x="{x}" y="{y}" width="30" height="42" fill="{INK}" opacity="0.5"/>')
        E.line([(x, y), (x + 30, y)], w=1.2, op=0.8, smooth=False)
    E.shape([(wx0 - 4, 640), (wx0 + 400, 624), (wx0 + 400, 650), (wx0 - 4, 660)], smooth=False, fill=None, tone=0.0, outline=False)
    clip_close(E)
    E.add(f'<rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}" fill="none" stroke="{INK}" stroke-width="2"/>')
    rect(E, wx0 - 22, wy1 + 10, wx1 + 22, wy1 + 22, hatches=[(0, 3, 0.3)], sw=1.8)
    floor_band(E, FL, 0.16)
    # the bed
    for lx in (96, 380):
        rect(E, lx - 8, 930, lx + 8, FL, hatches=[(80, 2.6, 0.5)], sw=1.6)
    rect(E, 70, 820, 94, 970, hatches=[(80, 3, 0.5)], sw=2)
    rect(E, 82, 870, 400, 930, hatches=[(0, 3.4, 0.35)], sw=2)
    iso.fade(E, 82, 870, 400, 930, op=0.6, side="b", reach=1.0)
    # pillow, the man's head turned up to the screen, the blanket over the rest of him
    E.shape(ellipse_pts(158, 860, 74, 22, 16), hatches=[(0, 3, 0.3)], sw=2)
    hcx, hcy, hr = 160, 810, 42
    E.add(f'<g transform="rotate(-78 {hcx} {hcy})">')
    iso._head_side(E, hcx, hcy, hr, 1, 0.0)
    iso._hair(E, hcx, hcy, hr, "dark", 1, "side")
    E.add("</g>")
    E.limb([(204, 868), (244, 856)], 30, tone=0.5)
    blanket = [(220, 858), (300, 836), (380, 842), (404, 880), (396, 928), (220, 928)]
    E.shape(blanket, smooth=True, hatches=[(70, 3.4, 0.4), (-45, 3.8, 0.3)], sw=2)
    for k in range(4):
        E.line([(250 + k * 36, 850 + k * 3), (254 + k * 36, 920)], w=0.9, op=0.5, smooth=False)
    # raised arm and the screen above his face
    E.limb([(240, 856), (262, 800), (214, 744)], 24, tone=0.5)
    hand_dot(E, (210, 736), 8, -2.4)
    screen(E, 192, 712, 34, 56, rot=14)
    blue_glow(E, 186, 750, 110, 90, 0.42)
    blue_glow(E, 170, 806, 52, 40, 0.3)
    return _end(E, pess_pip_close())


CARDS = {k: v for k, v in globals().items() if re.fullmatch(r'di\d\d', k)}
