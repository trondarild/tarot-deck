"""Pessimist deck, minor series, suit of Sublimation (su01-su14): pain given a form.

Pips su01-su10: pess_pip_open("sublimation", n) draws the plate with a frieze of n burins; the scene of
the card's Image paragraph is drawn in the plate below the frieze (PESS_VIGNETTE), then
pess_pip_close(). Courts su11-su14: pess_court_open("sublimation", age) counts the age in burins at the
top, then a scene from the card's Figure paragraph with the matching age figure (child(), youth(),
adult(), elder()) as its main figure, then pess_court_close(). The scenes are mostly of making:
drawing, painting, writing, music and craft.

The drawing engine, helpers and figures come from pess_minor_isolation; the suit's colour is the
greyed copper green WASH["verdigris"], applied through the suit_colour decorator in the roles slate
plays in Isolation (washes, tints, sky gradients, night windows, dark underlays). The second colour is
bone, used only for lamp-glow and the glass of lit windows.

New helpers here: ribbon(), antler(), skull_profile(), sheet(), ruled(), staves(), easel(), brush(),
stool_fold(), shavings(), fruit pieces, violin(), tesserae rings and a few room pieces.
Everything uses the rng passed in; ids are prefixed by the card's tag so they stay unique in a document.
"""

import math

from . import pess_minor_isolation as iso
from .common import (PESS_PAPER, PESS_VIGNETTE, WASH, f, pess_court_close, pess_court_open, pess_pip_close,
                     pess_pip_open, svg)
from .pess_awakening import PAPER_FILL, ellipse_pts
from .pess_minor_isolation import (BONE, INK, IX0, IX1, IY0, IY1, VX0, VX1, VY0, VY1, Plate, adult, candle, cast,
                                   chair_side, child, curtain, elder, fade, floor_band, floor_shadow, glow,
                                   hand_dot, jar, lantern, mass, mix, rect, sky, slate, suit_colour,
                                   table_front, table_lamp, wall, window, wine_glass, youth, clip_open,
                                   clip_close, cloud_bank, vignette)

V = WASH["verdigris"]
suit = suit_colour(V)


# ------------------------------------------------------------------ plate helpers

def _pip(n, tag, rng):
    E = Plate(rng, tag)
    E.add(pess_pip_open("sublimation", n))
    return E


def _court(age, tag, rng):
    E = Plate(rng, tag)
    E.add(pess_court_open("sublimation", age))
    return E


def _end(E, close, **kw):
    return iso._end(E, close, **kw)


# ------------------------------------------------------------------ new helpers

def ribbon(pts, w0, w1):
    """A tapering band along a polyline: the outline polygon, wide w0 at the start and w1 at the end."""
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        w = (w0 + (w1 - w0) * i / max(1, n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def antler(E, x, y, s=1.0, d=1, shadow=None):
    """One great palmate antler (an extinct deer's) rising from the burr at (x, y), sweeping up and out to
    side d (+1 right, -1 left). Reach is about 175 s sideways and 370 s upward. shadow=(dx, dy) first
    casts a soft shadow of it on the wall behind."""
    def P(pts):
        return [(x + d * px * s, y + py * s) for px, py in pts]
    beam = P([(0, 0), (8, -60), (36, -120), (84, -158), (136, -172)])
    palm = P([(96, -172), (62, -206), (40, -250), (14, -296), (60, -276), (66, -330), (104, -290), (130, -352), (150, -292),
              (190, -338), (196, -280), (238, -300), (236, -244), (268, -250), (250, -200), (214, -166), (160, -150)])
    brow = P([(6, -30), (22, -70), (54, -94), (76, -92)])
    hs = [(70 if d > 0 else 110, 2.4, 0.5), (-30 if d > 0 else 30, 3.2, 0.35)]
    tips = ()
    bpoly, wpoly = ribbon(beam, 46 * s, 24 * s), ribbon(brow, 22 * s, 4 * s)
    tines = []
    if shadow:
        for poly in [bpoly, palm] + tines:
            cast(E, [(px + shadow[0], py + shadow[1]) for px, py in poly], 0.4)
    E.shape(wpoly, smooth=False, hatches=hs, sw=1.6)
    for poly in tines:
        E.shape(poly, smooth=False, hatches=hs, tone=0.2, sw=1.6)
    E.shape(bpoly, smooth=False, hatches=hs, tone=0.25, sw=1.8)
    E.shape(palm, smooth=False, hatches=hs, tone=0.2, sw=1.8)
    for k in range(4):
        E.line(P([(120 + 28 * k, -176), (128 + 32 * k, -262 - 6 * k)]), w=0.8, op=0.55, smooth=False)


def antler_lines(E, x, y, s, d=1, w=3.0, color=INK):
    """A child's antler, drawn as plain chalk strokes: a beam with a fan of tines."""
    def P(pts):
        return [(x + d * px * s, y + py * s) for px, py in pts]
    E.line(P([(0, 0), (20, -50), (50, -90), (92, -120)]), w=w, color=color)
    for tip in ((60, -150), (100, -165), (140, -140), (150, -105)):
        E.line(P([(92, -120), tip]), w=w * 0.8, color=color, smooth=False)


def skull_profile(E, x, y, s=1.0, d=1):
    """A great skull seen from the side, muzzle toward -d, base (jaw underside) at y; (x, y) is the centre
    of the cranium base."""
    def P(pts):
        return [(x + d * px * s, y + py * s) for px, py in pts]
    E.shape(P([(-30, -16), (-100, 2), (-120, 14), (-118, 30), (-30, 34)]), smooth=False,
            hatches=[(70, 2.6, 0.5), (-30, 3, 0.4)], tone=0.3, sw=1.8)
    E.shape(ellipse_pts(x, y - 20 * s, 44 * s, 36 * s, 16), hatches=[(64, 2.6, 0.45), (-30, 3, 0.35)], tone=0.2, sw=1.9)
    E.shape(ellipse_pts(x - d * 26 * s, y - 20 * s, 11 * s, 10 * s, 10), fill=INK, outline=False)
    E.line(P([(-104, 24), (-60, 24), (-30, 14)]), w=1.2, op=0.8, smooth=False)


def sheet(E, pts, hatches=(), tone=0.0, sw=1.5):
    """A sheet of paper as an etched quadrilateral."""
    E.shape(pts, smooth=False, hatches=list(hatches), tone=tone, sw=sw)


def ruled(E, x0, y0, x1, y1, n, frac=1.0, rng=None, gap_op=0.55):
    """Parallel hand-ruled lines of writing (no letters) across a box, covering the first frac of each line;
    lines are broken into short words by small gaps."""
    r = rng or E.rng
    for k in range(n):
        y = y0 + (y1 - y0) * (k + 0.5) / n
        xe = x0 + (x1 - x0) * frac * (0.82 + 0.18 * r.random())
        x = x0
        pieces = []
        while x < xe:
            ln = r.uniform(10, 26)
            pieces.append(f"M{f(x)},{f(y + r.uniform(-0.6, 0.6))} L{f(min(x + ln, xe))},{f(y + r.uniform(-0.6, 0.6))}")
            x += ln + r.uniform(4, 7)
        E.add(f'<path d="{" ".join(pieces)}" stroke="{INK}" stroke-width="0.9" opacity="{gap_op}" fill="none"/>')


def staves(E, x0, y0, x1, n=2, gap=5.0, rows=1, rng=None, notes=True):
    """Music staves (sets of five lines) with a scatter of note heads and stems, a few struck through."""
    r = rng or E.rng
    for k in range(n):
        yb = y0 + k * (gap * 4 + 11)
        d = " ".join(f"M{f(x0)},{f(yb + i * gap)} L{f(x1)},{f(yb + i * gap + r.uniform(-0.4, 0.4))}" for i in range(5))
        E.add(f'<path d="{d}" stroke="{INK}" stroke-width="0.8" opacity="0.7" fill="none"/>')
        if notes:
            x = x0 + 6
            while x < x1 - 6:
                ny = yb + r.randrange(0, 9) * gap / 2
                E.add(f'<ellipse cx="{f(x)}" cy="{f(ny)}" rx="2.6" ry="1.9" fill="{INK}" transform="rotate(-20 {f(x)} {f(ny)})"/>')
                E.add(f'<path d="M{f(x + 2.4)},{f(ny)} L{f(x + 2.4)},{f(ny - 13)}" stroke="{INK}" stroke-width="0.8"/>')
                x += r.uniform(8, 13)


def strike(E, x0, y0, x1, y1, w=1.6):
    """A heavy correcting stroke over a page."""
    E.line([(x0, y0), (x1, y1)], w=w, op=0.9, smooth=False)


def brush(E, p0, p1, w=3.0, tip=INK):
    """A painter's long brush from the hand at p0 to the tip at p1."""
    E.line([p0, p1], w=w, smooth=False)
    t = (p1[0] + (p1[0] - p0[0]) * 0.05, p1[1] + (p1[1] - p0[1]) * 0.05)
    E.add(f'<circle cx="{f(t[0])}" cy="{f(t[1])}" r="{f(w * 0.9)}" fill="{tip}"/>')


def easel(E, x, base, top, cw, ch, face=True):
    """A studio easel: three splayed legs and a ledge; the canvas box is (x - cw/2, top) to (x + cw/2, top + ch).
    Returns the canvas box."""
    x0, y0, x1, y1 = x - cw / 2, top, x + cw / 2, top + ch
    E.line([(x - cw * 0.5, y0 - 30), (x - cw * 0.8, base)], w=4.0, smooth=False)
    E.line([(x + cw * 0.5, y0 - 30), (x + cw * 0.8, base)], w=4.0, smooth=False)
    E.line([(x, y0 - 20), (x + cw * 0.15, base - 10)], w=3.0, op=0.8, smooth=False)
    rect(E, x0 - 14, y1 + 4, x1 + 14, y1 + 16, hatches=[(0, 2.6, 0.5)], sw=1.8)
    rect(E, x0, y0, x1, y1, sw=2.2)
    return x0, y0, x1, y1


def stool_fold(E, x, y, w=86):
    """A folding stool seen from the side: a seat at height y over crossed legs to the ground at y + 110."""
    base = y + 110
    for a, b in ((x - w * 0.4, x + w * 0.4), (x + w * 0.4, x - w * 0.4)):
        E.line([(a, y + 4), (b, base)], w=3.6, smooth=False)
    rect(E, x - w / 2, y - 3, x + w / 2, y + 7, hatches=[(0, 2.2, 0.6)], sw=1.8)


def shavings(E, x0, x1, y, n, rng):
    """Curled wood shavings strewn along a floor line."""
    for _ in range(n):
        x = rng.uniform(x0, x1)
        yy = y + rng.uniform(-6, 8)
        s = rng.uniform(0.8, 1.5)
        E.line([(x, yy), (x + 9 * s, yy - 9 * s), (x + 18 * s, yy - 3 * s), (x + 10 * s, yy + 5 * s), (x + 4 * s, yy - 1 * s)],
               w=1.3, smooth=True)


def peach(E, x, y, r=28, soft=False):
    """A peach with a cleft and a leaf-less stem; a soft one slumps and carries a bruise of hatching."""
    pts = ellipse_pts(x, y, r * (1.08 if soft else 1.0), r * (0.88 if soft else 0.95), 16)
    E.shape(pts, hatches=[(62, 3, 0.4, (x, y - r, x + r, y + r))], tone=0.3 if soft else 0.12, sw=1.8)
    E.line([(x - 2, y - r * 0.9), (x + 4, y - r * 0.2), (x + 2, y + r * 0.5)], w=1.0, op=0.6)
    if soft:
        E.shape(ellipse_pts(x + r * 0.35, y + r * 0.3, r * 0.34, r * 0.28, 10), hatches=[(40, 1.9, 0.8), (-30, 2.2, 0.6)],
                tone=0.6, outline=False)
    E.line([(x, y - r * 0.9), (x + 2, y - r * 1.2)], w=1.6, smooth=False)


def lemon(E, x, y, rx=34, ry=21, peeled=True):
    """A lemon on its side, half peeled; the peel hangs in a spiral from it."""
    E.shape(ellipse_pts(x, y, rx, ry, 16), hatches=[(20, 3, 0.4, (x - rx, y, x + rx, y + ry))], tone=0.15, sw=1.8)
    E.line([(x - rx, y), (x - rx - 6, y - 3)], w=1.8, smooth=False)
    E.line([(x + rx, y), (x + rx + 6, y + 2)], w=1.8, smooth=False)
    if peeled:
        E.line([(x + 6, y + ry - 2), (x + 20, y + ry + 18), (x + 6, y + ry + 34), (x + 22, y + ry + 50), (x + 10, y + ry + 64)],
               w=2.0)


def violin(E, x, y, s=1.0, rot=0):
    """A violin lying on its back, centred at (x, y), neck to the right before rotation."""
    E.add(f'<g transform="rotate({rot} {f(x)} {f(y)})">')
    body = [(-48, -8), (-42, -26), (-20, -32), (-6, -20), (-8, -10), (6, -4), (-8, 2), (-6, 14), (-20, 28), (-42, 24), (-48, 8)]
    E.shape([(x + px * s, y + py * s * 1.15) for px, py in [(a, b * 1.0) for a, b in body]], smooth=True,
            hatches=[(60, 2.4, 0.55)], tone=0.35, sw=1.8)
    E.line([(x - 4 * s, y), (x + 60 * s, y)], w=3.2 * s, smooth=False)
    E.shape(ellipse_pts(x + 68 * s, y - 2 * s, 7 * s, 5 * s, 10), hatches=[(40, 2, 0.8)], tone=0.5, sw=1.4)
    for k in (-1, 0, 1):
        E.line([(x - 40 * s, y + k * 2 * s), (x + 60 * s, y + k * 1.2 * s)], w=0.7, op=0.8, smooth=False)
    E.add("</g>")


def pen_hand(E, p, ang=0.0, ln=20):
    """A pen held by the hand at p, pointing along ang (radians): a short shaft and a dark nib."""
    q = (p[0] + math.cos(ang) * ln, p[1] + math.sin(ang) * ln)
    E.line([p, q], w=2.0, smooth=False)
    E.add(f'<circle cx="{f(q[0])}" cy="{f(q[1])}" r="1.8" fill="{INK}"/>')


def tile_ring(E, cx, cy, rx, ry, u0, u1, size, cols, skip, rng):
    """One ring of mosaic tesserae in a flattened circle (perspective), from radius fraction u0 to u1.
    cols is a list of fills used round the ring; skip(angle) says where the ring is still unlaid."""
    n = max(8, int(2 * math.pi * (u0 + u1) / 2 * rx / size))
    out = []
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 0.86) / n
        if skip(a0):
            continue
        pts = [(u0, a0), (u1, a0), (u1, a1), (u0, a1)]
        d = "M" + " L".join(f"{f(cx + u * rx * math.cos(a))},{f(cy + u * ry * math.sin(a))}" for u, a in pts) + " Z"
        out.append(f'<path d="{d}" fill="{cols[i % len(cols)]}" stroke="{INK}" stroke-width="0.6" stroke-opacity="0.85"/>')
    E.add("".join(out))


def pebble_heap(E, x, y, rng, n=14, spread=60):
    """A heap of loose stones on the ground."""
    for _ in range(n):
        px = x + rng.uniform(-spread, spread)
        py = y - rng.uniform(0, spread * 0.5) * (1 - abs(px - x) / (spread * 1.2))
        r = rng.uniform(7, 13)
        E.shape(ellipse_pts(px, py, r * 1.2, r, 8, rot=rng.uniform(0, 3)), hatches=[(60, 2.6, 0.5)], tone=rng.uniform(0.1, 0.5),
                sw=1.2)


def window_town(E, x0, y0, x1, y1, rng, tone=0.85, spire=True):
    """A night window onto roofs: the glass, then dark roof masses and a few lit panes in bone."""
    window(E, x0, y0, x1, y1, tone=tone, panes=(1, 1))
    clip_open(E, x0, y0, x1, y1)
    base = y1
    xs = x0
    while xs < x1:
        w = rng.uniform(26, 48)
        h = rng.uniform(40, 90)
        E.shape([(xs, base), (xs, base - h), (xs + w / 2, base - h - 20), (xs + w, base - h), (xs + w, base)], smooth=False,
                hatches=[(80, 2.0, 0.8), (-40, 2.4, 0.6)], tone=0.8, sw=1.3)
        if rng.random() < 0.5:
            E.add(f'<rect x="{f(xs + w * 0.3)}" y="{f(base - h * 0.6)}" width="6" height="8" fill="{BONE}" opacity="0.9"/>')
        xs += w + 2
    if spire:
        sx = x0 + (x1 - x0) * 0.62
        E.shape([(sx - 10, base), (sx - 10, base - 130), (sx, base - 190), (sx + 10, base - 130), (sx + 10, base)], smooth=False,
                hatches=[(80, 2.0, 0.8), (-40, 2.4, 0.6)], tone=0.85, sw=1.3)
    clip_close(E)


# ------------------------------------------------------------------ pips

@suit
def su01(rng):
    """One: a draughtsman at a table in a museum store-room draws a vast antler from a skull on a trestle."""
    E = _pip(1, "a", rng)
    FL = 1010
    wall(E, 340, FL, op=0.16)
    # store-room shelving on the wall: crates and long bones
    for sy in (470, 600):
        rect(E, 84, sy, 330, sy + 11, hatches=[(0, 3, 0.4)], sw=1.8)
    for bx, bw, bh in ((98, 70, 62), (180, 72, 44), (262, 60, 58)):
        rect(E, bx, 470 - bh, bx + bw, 470, hatches=[(80, 3.4, 0.35)], tone=0.2, sw=1.8)
        E.line([(bx + 8, 470 - bh / 2), (bx + bw - 8, 470 - bh / 2)], w=0.9, op=0.6, smooth=False)
    for bx in (104, 150, 196, 242, 288):
        rect(E, bx, 538, bx + 14, 600, hatches=[(80, 2.4, 0.5)], tone=0.2, sw=1.4)
    for k in range(3):
        E.shape([(110 + k * 80, 596), (150 + k * 80, 596), (146 + k * 80, 586), (114 + k * 80, 586)], smooth=False, sw=1.2, tone=0.25)
    fade(E, IX0, 340, 360, FL, op=0.6, side="l", reach=1.0)
    fade(E, 70, 340, IX1, 470, op=0.45, side="t", reach=1.0)
    floor_band(E, FL, 0.16)
    # the skull on its trestle, the great antler above it, with a shadow on the wall
    SX, SY = 478, 796
    antler(E, SX + 8, SY - 44, 1.08, -1, shadow=(-36, 14))
    floor_shadow(E, 480, FL - 2, 120, 10, 0.6)
    for lx0, lx1 in ((408, 392), (556, 574)):
        E.line([(lx0, 836), (lx1, FL)], w=5, smooth=False)
    E.line([(408, 920), (556, 920)], w=3, smooth=False)
    rect(E, 386, 826, 580, 840, hatches=[(0, 2.6, 0.5)], sw=2)
    skull_profile(E, SX, SY, 1.0, d=-1)
    # chair, the draughtsman, and the table with the drawing board
    chair_side(E, 125, FL, seat=125, f_dir=1, back_h=200, w=100)
    cast(E, [(204, 826), (352, 826), (360, FL - 2), (200, FL - 2)], 0.6)
    adult(E, 125, FL, 500, pose="sit", facing=1, lean=0.2, wash_op=0.7, garment="coat", hair="dark",
          hands={"near": (245, 782), "far": (270, 800)})
    table_front(E, 205, 350, 806, FL, thick=16, legs=(0.08, 0.92))
    board = [(222, 806), (340, 806), (338, 664), (232, 656)]
    sheet(E, board, hatches=[(0, 3, 0.2)], sw=2.2)
    paper = [(232, 796), (330, 796), (328, 674), (240, 668)]
    sheet(E, paper, hatches=[(70, 2.0, 0.6), (-30, 2.4, 0.45), (12, 2.6, 0.35)], tone=0.35, sw=1.2)
    antler_lines(E, 252, 782, 0.24, 1, w=2.0, color=PAPER_FILL)
    E.line([(262, 700), (316, 704)], w=1.0, op=0.6, smooth=False)
    brush(E, (252, 784), (240, 774), w=2.0)
    hand_dot(E, (248, 786), 7, -0.6)
    return _end(E, pess_pip_close())


@suit
def su02(rng):
    """Two: a painter at an easel before a table of peaches, a half-peeled lemon and a glass; the soft peach
    is at the centre of the canvas."""
    E = _pip(2, "b", rng)
    FL = 1010
    wall(E, 340, FL, op=0.14)
    fade(E, IX0, 340, 330, FL, op=0.5, side="l", reach=1.0)
    window(E, 100, 400, 240, 650, tone=0.2, panes=(1, 2), glow=BONE)
    curtain(E, 400, 600, 330, 800, drawn=1.0, side="right", op=0.55)
    floor_band(E, FL, 0.14)
    # table with fruit
    TOP = 800
    rect(E, 404, TOP, 606, TOP + 14, hatches=[(0, 3, 0.4)], sw=2)
    table_front(E, 412, 598, TOP + 14, FL, cloth=170, wash_op=0.15)
    cast(E, [(404, TOP + 14), (606, TOP + 14), (616, FL - 2), (396, FL - 2)], 0.45)
    peach(E, 448, TOP - 26, 26)
    peach(E, 496, TOP - 22, 25, soft=True)
    peach(E, 470, TOP - 62, 22)
    lemon(E, 538, TOP - 18)
    wine_glass(E, 584, TOP, 0.82, fill=0.3)
    # the easel with the painting: a still life, the soft peach in the middle
    x0, y0, x1, y1 = easel(E, 292, FL, 560, 150, 210)
    E.shape([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], smooth=False, tone=0.08, hatches=[(0, 3.4, 0.2)], sw=2.2)
    rect(E, x0 + 6, y0 + 6, x1 - 6, y1 - 6, tint=(V, 0.16), hatches=[(60, 3.6, 0.28)], sw=1.0)
    E.line([(x0 + 6, y0 + 140), (x1 - 6, y0 + 140)], w=1.2, smooth=False, op=0.7)
    E.shape(ellipse_pts(292, y0 + 100, 24, 21, 14), hatches=[(40, 2, 0.7), (-30, 2.4, 0.5)], tone=0.45, sw=1.3)
    E.shape(ellipse_pts(256, y0 + 118, 15, 13, 12), hatches=[(60, 3, 0.4)], tone=0.12, sw=1.1)
    E.shape(ellipse_pts(330, y0 + 120, 13, 12, 12), hatches=[(60, 3, 0.4)], tone=0.12, sw=1.1)
    E.shape(ellipse_pts(300, y0 + 128, 20, 8, 12), hatches=[(0, 2.6, 0.4)], sw=1.0)
    E.shape([(272, y0 + 74), (290, y0 + 68), (306, y0 + 74)], smooth=False, fill=None, sw=0.01, outline=False)
    # the painter, a brush at the canvas, a palette on the other hand
    painter = adult(E, 112, FL, 520, facing=1, lean=0.1, garment="long", hair="dark", wash_op=0.8, look=0.9,
                    hands={"near": (216, 704), "far": (178, 760)})
    hx, hy = painter["hands"]["near"]
    brush(E, (hx - 4, hy + 6), (hx + 26, hy - 14), w=2.4)
    px, py = painter["hands"]["far"]
    E.shape(ellipse_pts(px + 6, py + 4, 34, 18, 14), hatches=[(0, 3, 0.4)], tone=0.15, sw=1.8)
    for k, c in enumerate((V, BONE, V)):
        E.add(f'<circle cx="{f(px - 12 + k * 14)}" cy="{f(py + 4)}" r="4.5" fill="{c}" opacity="0.85"/>')
    hand_dot(E, (px, py), 7)
    hand_dot(E, (hx, hy), 7, 0.0)
    return _end(E, pess_pip_close())


@suit
def su03(rng):
    """Three: a small choir in a stone nave sings from one score under one lamp; the vault above is dark and empty."""
    E = _pip(3, "c", rng)
    FL = 1010
    wall(E, 360, FL, op=0.2, gap=6)
    # stone: columns and the dark vault
    for cx in (108, 590):
        rect(E, cx - 24, 440, cx + 24, FL, hatches=[(80, 3, 0.45)], tone=0.15, sw=2)
        rect(E, cx - 34, 420, cx + 34, 446, hatches=[(0, 2.4, 0.55)], sw=1.8)
        rect(E, cx - 32, 986, cx + 32, FL, hatches=[(0, 2.4, 0.55)], sw=1.8)
    mass(E, [(IX0, 340), (IX1, 340), (IX1, 470), (590, 436), (340, 560), (108, 436), (IX0, 470)], solid=0.7, wash=0.4, sw=2)
    for k in range(5):
        E.line([(340, 560), (340 + (k - 2) * 120, 345)], w=1.0, op=0.45, smooth=False)
    fade(E, IX0, 560, 300, FL, op=0.5, side="l", reach=1.0)
    fade(E, 420, 560, IX1, FL, op=0.5, side="r", reach=1.0)
    floor_band(E, 940, 0.2)
    # lectern with the one score, and the lamp hanging over it
    cast(E, [(430, 940), (600, 940), (630, FL), (400, FL)], 0.35)
    E.line([(522, 345), (522, 600)], w=1.4, smooth=False)
    lantern(E, 522, 600, 0.8)
    rect(E, 514, 740, 530, FL - 30, hatches=[(80, 2.6, 0.5)], sw=1.8)
    E.shape(ellipse_pts(522, FL - 24, 34, 8, 12), hatches=[(0, 2.4, 0.5)], sw=1.8)
    desk = [(464, 706), (578, 696), (584, 738), (470, 750)]
    sheet(E, desk, hatches=[(0, 3, 0.35)], sw=2)
    score = [(472, 716), (572, 708), (576, 736), (476, 744)]
    sheet(E, score, sw=1.0)
    staves(E, 482, 718, 566, n=1, gap=3.4, rng=rng)
    # the choir in profile, faces lifted to the vault
    singers = ((425, "adult", 470, "long"), (338, "elder", 480, "long"), (252, "adult", 450, "dress"), (166, "elder", 440, "long"))
    for k, (sx, kind, h, gar) in enumerate(singers):
        fn = {"adult": adult, "elder": elder}[kind]
        near = (482, 740) if k == 0 else (sx + 70, 780 - k * 6) if k == 1 else None
        hands = {"near": near, "far": (near[0] - 22, near[1] + 6)} if near else {"near": (sx + 48, 760), "far": (sx + 40, 772)}
        floor_shadow(E, sx + 8, FL - 2, 52, 8, 0.6)
        fn(E, sx, FL, h, facing=1, lean=0.04, garment=gar, hair="dark" if k % 2 else "white", mouth=0.9, look=0.9, tilt=-20,
           wash_op=0.8 - 0.1 * (k % 2), hands=hands)
    return _end(E, pess_pip_close())


@suit
def su04(rng):
    """Four: a restorer in a smock on a scaffold fills a patch of missing sky in a flaking fresco, a bucket of
    lime and a ladder beside her."""
    E = _pip(4, "d", rng)
    FL = 1010
    PL = 790
    wall(E, 340, FL, op=0.2, gap=6)
    fade(E, IX0, 340, 300, FL, op=0.5, side="l", reach=1.0)
    # the fresco: an arched panel of painted sky and hills, cracked, with patches gone
    fx0, fx1, fy0, fy1 = 130, 560, 390, 760
    arch = [(fx0, fy1), (fx0, fy0 + 90)] + [(fx0 + (fx1 - fx0) / 2 - math.cos(a) * (fx1 - fx0) / 2, fy0 + 90 - math.sin(a) * 90)
                                         for a in [k * math.pi / 14 for k in range(1, 14)]] + [(fx1, fy0 + 90), (fx1, fy1)]
    E.shape(arch, smooth=False, hatches=[(0, 12, 0.15)], tone=0.0, sw=2.4)
    clip = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in arch) + " Z"
    cid = E.uid("w")
    E.add(f'<clipPath id="{cid}"><path d="{clip}"/></clipPath><g clip-path="url(#{cid})">')
    sky(E, fy0, 650, strongest=0.4, weakest=0.05, gap=5, x0=fx0, x1=fx1, tint=0.7)
    E.shape([(fx0, 700), (230, 640), (340, 690), (450, 630), (fx1, 680), (fx1, fy1), (fx0, fy1)], smooth=False,
            hatches=[(62, 2.2, 0.75), (-38, 2.6, 0.55)], tone=0.55, sw=1.4)
    E.shape([(fx0, fy1), (fx0, 740), (260, 716), (400, 740), (fx1, 720), (fx1, fy1)], smooth=False,
            hatches=[(10, 3, 0.5), (-40, 3, 0.4)], tone=0.4, sw=1.2)
    # flaked-away patches, showing bare plaster
    for pts in ([(250, 470), (300, 450), (340, 484), (320, 530), (268, 520)],
                [(430, 430), (500, 440), (520, 500), (470, 520), (440, 480)],
                [(160, 600), (214, 584), (230, 640), (176, 650)]):
        E.shape(pts, smooth=False, hatches=[(0, 3, 0.5), (50, 4, 0.4)], tone=0.35, sw=1.6)
    E.add("</g>")
    # the patch in hand: half filled with fresh sky
    E.shape([(340, 396), (420, 392), (432, 452), (372, 470), (336, 440)], smooth=False, fill=PAPER_FILL, sw=1.6,
            hatches=[(0, 2.6, 0.45), (0, 4.8, 0.3, (340, 396, 386, 470))], tint=(V, 0.3))
    for pts in ([(190, 380), (210, 450), (186, 520), (210, 600)], [(480, 380), (460, 430), (490, 500)], [(380, 520), (400, 600), (370, 700)]):
        E.line(pts, w=1.1, op=0.8, smooth=False)
    floor_band(E, FL - 8, 0.18)
    for k in range(7):
        fxp = rng.uniform(150, 540)
        E.shape([(fxp, FL + 6), (fxp + 14, FL - 2), (fxp + 22, FL + 10), (fxp + 6, FL + 14)], smooth=False, sw=1.0, tone=0.2)
    # scaffold: poles, planking, braces, a rail
    for px in (120, 480):
        rect(E, px - 6, 560, px + 6, FL, hatches=[(80, 2.6, 0.5)], sw=1.8)
    E.line([(120, 810), (480, 1000)], w=3.2, smooth=False)
    E.line([(480, 810), (120, 1000)], w=3.2, smooth=False)
    E.line([(120, 700), (480, 700)], w=3.4, smooth=False)
    rect(E, 100, PL, 510, PL + 16, hatches=[(0, 3, 0.4)], sw=2)
    for gx in range(106, 506, 40):
        E.line([(gx, PL), (gx, PL + 16)], w=0.9, op=0.6, smooth=False)
    cast(E, [(104, PL + 16), (508, PL + 16), (520, PL + 60), (96, PL + 60)], 0.4)
    # lime bucket on the planks
    E.shape([(160, PL), (166, PL - 50), (222, PL - 50), (228, PL)], smooth=False, hatches=[(80, 3, 0.45)], sw=1.8)
    E.shape(ellipse_pts(194, PL - 50, 28, 6, 12), fill=BONE, sw=1.6)
    E.line([(166, PL - 50), (194, PL - 94), (222, PL - 50)], w=1.4)
    # ladder
    for lx in (518, 566):
        E.line([(lx - 6 * (1 if lx < 540 else 0.4), PL + 6), (lx + 18, FL)], w=4, smooth=False)
    for k in range(7):
        t = k / 6
        yy = PL + 30 + t * (FL - PL - 40)
        E.line([(520 + 18 * t * 0.8, yy), (568 + 14 * t * 0.8, yy)], w=3, smooth=False)
    # the restorer, from behind, brush to the sky
    adult(E, 292, PL, 390, view="back", garment="smock", hair="bun", wash_op=0.5,
          hands={"right": (350, 440, -1), "left": (254, PL - 190)})
    E.line([(350, 438), (364, 424)], w=2.2, smooth=False)
    return _end(E, pess_pip_close())


@suit
def su05(rng):
    """Five: an old man at a plain desk writes on a long roll that falls over the edge and coils on the floor;
    a candle burns beside him and the roll's shadow crosses the wall."""
    E = _pip(5, "e", rng)
    FL = 1010
    TOP = 794
    wall(E, 340, FL, op=0.16)
    fade(E, IX0, 340, 300, FL, op=0.6, side="l", reach=1.0)
    fade(E, 70, 340, IX1, 470, op=0.5, side="t", reach=1.0)
    window(E, 440, 370, 570, 620, tone=0.75, panes=(1, 2))
    floor_band(E, FL, 0.16)
    # the shadow of the roll on the wall: a long, sagging swath from the desk toward the upper left
    cast(E, [(300, TOP - 6), (400, TOP - 8), (330, 600), (190, 480), (110, 430), (100, 500), (210, 620)], 0.55)
    glow(E, 548, TOP - 74, 80, 70, 0.34)
    chair_side(E, 150, FL, seat=120, f_dir=1, back_h=210, w=100)
    cast(E, [(262, TOP + 16), (600, TOP + 16), (610, FL - 2), (254, FL - 2)], 0.55)
    # the roll, coiling on the floor
    for k, (rx, ry) in enumerate(((78, 15), (58, 11), (38, 8), (20, 5))):
        E.shape(ellipse_pts(456 - k * 3, FL - 18 + k * 2, rx, ry, 18), hatches=[(0, 3, 0.2)], tone=0.04 * k, sw=1.5)
    E.shape([(300, FL - 6), (350, FL - 14), (390, FL - 12), (330, FL + 2)], smooth=False, sw=1.2)
    hold = el = elder(E, 150, FL, 480, pose="sit", facing=1, lean=0.28, wash_op=0.8, garment="long", hair="white", look=0.9,
                      tilt=6, hands={"near": (306, TOP - 10), "far": (290, TOP - 4)})
    # the desk, its top and front
    rect(E, 262, TOP, 606, TOP + 16, hatches=[(2, 3, 0.4)], sw=2)
    rect(E, 276, TOP + 16, 596, TOP + 70, hatches=[(80, 4, 0.3)], tone=0.12, sw=1.8)
    for lx in (284, 586):
        rect(E, lx - 7, TOP + 70, lx + 7, FL, hatches=[(80, 2.6, 0.5)], sw=1.6)
    # the roll lying along the desk and over its front edge
    E.shape([(298, TOP - 6), (500, TOP - 6), (512, TOP + 2), (290, TOP + 2)], smooth=False, hatches=[(0, 3, 0.18)], sw=1.5)
    ruled(E, 306, TOP - 5, 500, TOP + 1, 1, 0.8, rng)
    band = ribbon([(468, TOP + 6), (470, TOP + 60), (462, TOP + 120), (474, TOP + 170), (466, FL - 30)], 40, 40)
    E.shape(band, smooth=False, hatches=[(0, 3, 0.14)], sw=1.6)
    ruled(E, 452, TOP + 24, 486, TOP + 190, 1, 1.0, rng)
    for k in range(6):
        ruled(E, 452, TOP + 26 + k * 30, 486, TOP + 40 + k * 30, 1, 0.9, rng)
    hx, hy = el["hands"]["near"]
    pen_hand(E, (hx + 2, hy), -0.5, 20)
    hand_dot(E, (hx, hy), 7, 0.1)
    candle(E, 548, TOP, 70, 1.0)
    # a handful of stacked books on the shelf end
    return _end(E, pess_pip_close())


@suit
def su06(rng):
    """Six: a woman at a pianoforte in a bare room, a metronome beside the score; a pendulum shadow sweeps the
    wall and the score is covered with corrections."""
    E = _pip(6, "f", rng)
    FL = 1010
    wall(E, 340, FL, op=0.14)
    fade(E, IX0, 340, 300, FL, op=0.55, side="l", reach=1.0)
    fade(E, 70, 340, IX1, 470, op=0.4, side="t", reach=1.0)
    # the pendulum's shadow: a rod and a bob, with faint arcs of the swing
    px, py = 190, 380
    for k, a in enumerate((-0.5, -0.25, 0.25, 0.5)):
        E.line([(px, py), (px + 340 * math.sin(a), py + 340 * math.cos(a))], w=0.8, op=0.3, smooth=False, dash="4 7")
    rod = ribbon([(px, py), (px - 30, py + 160), (px - 62, py + 320)], 16, 9)
    cast(E, rod, 1.0)
    cast(E, ellipse_pts(px - 66, py + 340, 30, 34, 14), 1.0)
    floor_band(E, FL, 0.14)
    # the pianoforte: tall case, key bed, music desk with the score, metronome on top
    cast(E, [(350, FL - 8), (620, FL - 8), (620, FL + 30), (340, FL + 30)], 0.4)
    rect(E, 340, 560, 606, FL, hatches=[(80, 5, 0.3), (-40, 6, 0.2)], tone=0.2, sw=2.2)
    rect(E, 330, 548, 606, 568, hatches=[(0, 3, 0.4)], sw=2)
    fade(E, 340, 560, 606, FL, op=0.6, side="r", reach=1.0)
    rect(E, 318, 806, 380, 822, hatches=[(0, 2.6, 0.5)], sw=1.8)
    E.shape([(300, 786), (380, 786), (380, 806), (300, 806)], smooth=False, sw=1.8)
    for k in range(7):
        E.line([(306 + k * 11, 788), (306 + k * 11, 805)], w=0.9, smooth=False)
    sheet(E, [(344, 650), (420, 640), (426, 764), (348, 774)], sw=2.0)
    staves(E, 354, 656, 416, n=3, gap=3.4, rng=rng)
    for (a, b, c, d) in ((366, 700, 410, 690), (358, 740, 404, 732), (374, 664, 396, 676)):
        strike(E, a, b, c, d, 1.8)
    # the metronome
    E.shape([(500, 548), (540, 548), (528, 450), (512, 450)], smooth=False, hatches=[(80, 2.4, 0.6)], tone=0.3, sw=2)
    E.line([(520, 540), (544, 436)], w=1.6, smooth=False)
    rect(E, 538, 464, 552, 476, hatches=[(0, 2, 0.6)], tone=0.6, sw=1.2)
    # the woman on the stool
    rect(E, 150, 884, 232, 896, hatches=[(0, 2.4, 0.5)], sw=1.8)
    E.line([(170, 896), (162, FL)], w=4, smooth=False)
    E.line([(212, 896), (222, FL)], w=4, smooth=False)
    floor_shadow(E, 190, FL - 2, 90, 9, 0.6)
    adult(E, 188, FL, 500, pose="sit", facing=1, lean=0.14, wash_op=0.75, garment="dress", hair="bun", look=0.9, tilt=4,
          hands={"near": (306, 770), "far": (296, 778)})
    return _end(E, pess_pip_close())


@suit
def su07(rng):
    """Seven: a painter on a stony beach, on a folding stool, works at a panel in the wind before a sea under a
    heavy sky and one small sail."""
    E = _pip(7, "g", rng)
    HOR = 650
    sky(E, 340, HOR, strongest=0.42, weakest=0.06, gap=6, tint=0.95)
    for x, y, w, h, op in ((90, 420, 300, 46, 0.34), (320, 500, 280, 40, 0.3), (110, 590, 240, 28, 0.26), (380, 380, 230, 34, 0.3)):
        cloud_bank(E, x, y, w, h, op)
    E.line([(IX0, HOR), (IX1, HOR)], w=1.2, smooth=False)
    slate(E, IX0, HOR, IX1, 900, 0.55)
    d = []
    for k in range(12):
        yy = HOR + 14 + k * 20
        x = IX0 + rng.uniform(0, 14)
        d.append(f"M{f(x)},{f(yy)} " + " ".join("q9,-5 18,0" for _ in range(31)))
    E.add(f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width="0.8" opacity="0.45" fill="none"/>')
    # the small sail
    E.shape([(468, HOR - 2), (468, HOR - 42), (490, HOR - 6)], smooth=False, hatches=[(80, 2.2, 0.6)], tone=0.3, sw=1.4)
    E.line([(458, HOR), (498, HOR)], w=2.4, smooth=False)
    # beach: shingle with stones
    E.shape([(IX0, 880), (IX1, 870), (IX1, IY1 + 6), (IX0, IY1 + 6)], smooth=False, hatches=[(2, 5, 0.2)], sw=0.01, outline=False)
    fade(E, IX0, 880, IX1, IY1 + 6, op=0.7, side="b", reach=1.0)
    for _ in range(70):
        sx, sy = rng.uniform(80, 600), rng.uniform(900, 1078)
        r = 4 + (sy - 900) / 178 * 12 * rng.uniform(0.6, 1.1)
        E.shape(ellipse_pts(sx, sy, r * 1.3, r, 8, rot=rng.uniform(0, 3)), hatches=[(60, 2.6, 0.5)], tone=rng.uniform(0.0, 0.35), sw=1.0)
    FLP = 1000
    stool_fold(E, 190, 890)
    floor_shadow(E, 200, FLP + 4, 110, 9, 0.6)
    # field easel with the panel
    for lx in (300, 372):
        E.line([(lx, 760), (lx + (lx - 336) * 0.5, FLP)], w=3.6, smooth=False)
    E.line([(336, 740), (346, FLP + 6)], w=3, op=0.8, smooth=False)
    rect(E, 290, 690, 384, 776, hatches=[(0, 3, 0.2)], sw=2.2)
    rect(E, 298, 698, 376, 768, tint=(V, 0.25), hatches=[(0, 3, 0.35)], sw=1.0)
    E.line([(298, 730), (376, 730)], w=1.0, op=0.8, smooth=False)
    E.line([(342, 736), (352, 728)], w=1.4, smooth=False)
    rect(E, 280, 776, 394, 784, hatches=[(0, 2.4, 0.5)], sw=1.6)
    pa = adult(E, 190, FLP, 450, pose="sit", facing=1, lean=0.2, wash_op=0.8, garment="coat", hair="dark", hat="wide", look=0.9,
               hands={"near": (284, 736), "far": (270, 780)})
    hx, hy = pa["hands"]["near"]
    brush(E, (hx, hy), (hx + 22, hy - 8), w=2.2)
    hand_dot(E, (hx, hy), 7, 0.0)
    # wind: streaks and a scarf end
    for _ in range(14):
        wx, wy = rng.uniform(80, 560), rng.uniform(420, 860)
        E.line([(wx, wy), (wx + rng.uniform(30, 60), wy + rng.uniform(-2, 4))], w=0.8, op=0.5, smooth=False)
    E.line([(160, 650), (130, 656), (106, 650), (88, 660)], w=2.4)
    return _end(E, pess_pip_close())


def _room(E, y0, y1, rng, village, tag, lamp_x=200):
    """One of the two rooms of su08: a box with wall hatching, window on the right with a road, a desk with a
    lamp, a half-written sheet and a chair. village picks the window view."""
    x0, x1 = 84, 560
    FL = y1 - 54
    rect(E, x0, y0, x1, y1, hatches=[(80, 6, 0.14)], sw=2.4)
    clip_open(E, x0, y0, x1, y1)
    fade(E, x0, y0, x1, y1, op=0.55, side="l", reach=1.0)
    fade(E, x0, y0, x1, y0 + 120, op=0.4, side="t", reach=1.0)
    # window on the right with the road through it
    wx0, wx1, wy0, wy1 = 430, 534, y0 + 40, y0 + 190
    window(E, wx0, wy0, wx1, wy1, tone=0.35, panes=(1, 2), glow=BONE)
    clip_open(E, wx0, wy0, wx1, wy1)
    hz = wy0 + 94
    E.line([(wx0, hz), (wx1, hz)], w=1.0, smooth=False)
    if village == 0:   # roofs and a spire
        for rx, rw, rh in ((wx0 + 2, 26, 22), (wx0 + 32, 20, 32), (wx1 - 30, 28, 24)):
            E.shape([(rx, hz), (rx, hz - rh), (rx + rw / 2, hz - rh - 12), (rx + rw, hz - rh), (rx + rw, hz)], smooth=False, tone=0.5,
                    hatches=[(80, 2, 0.7)], sw=1.0)
    else:              # chimneys and a mill
        for rx, rw, rh in ((wx0 + 4, 30, 18), (wx1 - 36, 34, 28)):
            E.shape([(rx, hz), (rx, hz - rh), (rx + rw, hz - rh), (rx + rw, hz)], smooth=False, tone=0.5, hatches=[(80, 2, 0.7)], sw=1.0)
        E.shape([(wx0 + 50, hz), (wx0 + 56, hz - 34), (wx0 + 64, hz - 34), (wx0 + 70, hz)], smooth=False, tone=0.6, hatches=[(80, 2, 0.7)], sw=1.0)
    E.line([(wx0 + 20, wy1), (wx0 + 54, hz + 2)], w=1.3, smooth=False, op=0.9)
    E.line([(wx0 + 70, wy1), (wx0 + 58, hz + 2)], w=1.3, smooth=False, op=0.9)
    clip_close(E)
    # desk and lamp
    cast(E, [(120, FL - 6), (360, FL - 6), (370, FL + 20), (112, FL + 20)], 0.5)
    DT = FL - 130
    rect(E, 116, DT, 366, DT + 14, hatches=[(2, 3, 0.4)], sw=2)
    for lx in (128, 354):
        rect(E, lx - 6, DT + 14, lx + 6, FL, hatches=[(80, 2.6, 0.5)], sw=1.6)
    table_lamp(E, lamp_x, DT, 0.62)
    # the half-written sheet, in perspective, and a pen
    sh = [(228, DT - 2), (332, DT - 2), (340, DT + 8), (220, DT + 8)]
    sheet(E, sh, sw=1.4)
    ruled(E, 236, DT - 1, 330, DT + 7, 1, 0.5, rng)
    sheet(E, [(262, DT - 40), (326, DT - 44), (332, DT - 2), (258, DT - 1)], hatches=[(0, 3, 0.06)], sw=1.4)
    ruled(E, 268, DT - 38, 322, DT - 6, 5, 0.55, rng)
    E.line([(340, DT - 6), (366, DT - 22)], w=2.2, smooth=False)
    # a chair drawn up
    chair_side(E, 296, FL, seat=70, f_dir=-1, back_h=110, w=70)
    E.line([(x0, FL), (x1, FL)], w=1.6, smooth=False)
    clip_close(E)


@suit
def su08(rng):
    """Eight: two desks in two rooms of different towns, each with a lamp and a half-written sheet; a faint road
    through each window joins them."""
    E = _pip(8, "h", rng)
    _room(E, 346, 690, rng, 0, "u", lamp_x=190)
    _room(E, 732, 1076, rng, 1, "v", lamp_x=170)
    # the road, drawn faintly down the margin from the window of one room to the other
    E.line([(488, 480), (560, 520), (590, 600), (592, 690), (590, 728), (576, 780), (560, 820), (506, 850), (488, 870)], w=1.4, op=0.5, dash="6 5")
    E.line([(500, 480), (574, 520), (604, 600), (606, 690), (604, 728), (590, 780), (574, 820), (516, 850), (500, 870)], w=1.4, op=0.5, dash="6 5")
    return _end(E, pess_pip_close(), top=346)


@suit
def su09(rng):
    """Nine: a mason kneels on a floor setting tesserae into a wide circular pattern with a trowel; the circle is
    nearly done, a few gaps remain, loose stones heaped beside him."""
    E = _pip(9, "i", rng)
    FL = 1010
    wall(E, 340, 560, op=0.18)
    mass(E, [(150, 560), (150, 440), (190, 396), (250, 380), (310, 396), (350, 440), (350, 560)], solid=0.6, wash=0.35, sw=2)
    rect(E, 420, 420, 540, 560, hatches=[(80, 4, 0.3)], tone=0.12, sw=1.8)
    fade(E, IX0, 340, 360, 560, op=0.45, side="l", reach=1.0)
    floor_band(E, 560, 0.2)
    cx, cy, rx, ry = 384, 836, 222, 94
    E.shape(ellipse_pts(cx, cy + 8, rx + 12, ry + 6, 40), hatches=[(0, 3, 0.2)], tone=0.2, sw=2)
    E.shape(ellipse_pts(cx, cy, rx + 3, ry + 2, 40), fill=PAPER_FILL, hatches=[(5, 4, 0.14)], sw=1.4)
    light = "#E7E0CE"
    mid = mix(PAPER_FILL, V, 0.5)
    deep = mix(INK, V, 0.5)
    gap = lambda a: 1.75 < a < 2.65 or 5.0 < a < 5.35                    # the open sector, to the left
    rings = [(0.08, 0.2, (deep, light)), (0.2, 0.34, (mid, light, mid, deep)), (0.34, 0.46, (light, deep)),
             (0.46, 0.6, (mid, mid, light)), (0.6, 0.72, (deep, light, light)), (0.72, 0.86, (mid, deep, mid, light)),
             (0.86, 0.98, (light, mid))]
    for k, (u0, u1, cols) in enumerate(rings):
        sk = gap if k >= 3 else (lambda a: False)
        tile_ring(E, cx, cy, rx, ry, u0, u1, 11, cols, sk, rng)
    for _ in range(14):
        a = rng.uniform(0, 2 * math.pi)
        u = rng.uniform(0.15, 0.9)
        qx, qy = cx + u * rx * math.cos(a), cy + u * ry * math.sin(a)
        E.add(f'<ellipse cx="{f(qx)}" cy="{f(qy)}" rx="5" ry="3" fill="{PAPER_FILL}" stroke="{INK}" stroke-width="0.5"/>')
    E.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx * 0.07)}" ry="{f(ry * 0.07)}" fill="{iso.DARK}"/>')
    fade(E, 70, 560, IX1, IY1, op=0.5, side="b", reach=1.0)
    pebble_heap(E, 540, 1008, rng, n=16, spread=62)
    pebble_heap(E, 190, 1040, rng, n=6, spread=24)
    # the mason kneeling: thigh upright, shin along the floor, torso bent to the work
    X, HIP, KN = 212, 862, 996
    floor_shadow(E, X - 40, KN + 12, 130, 9, 0.6)
    E.limb([(X - 6, HIP), (X + 18, KN - 8)], 30, tone=0.3)
    E.limb([(X + 18, KN - 8), (X - 128, KN + 2)], 24, tone=0.3)
    iso._shoe(E, X - 128, KN + 6, -1, 500)
    m = adult(E, X, HIP, 500, pose="torso", facing=1, lean=0.8, garment="vest", hair="dark", wash_op=0.8, look=0.9, tilt=12,
              hands={"near": (292, 918), "far": (268, 934)})
    hx, hy = m["hands"]["near"]
    E.shape([(hx + 4, hy - 4), (hx + 34, hy - 18), (hx + 42, hy - 8), (hx + 10, hy + 4)], smooth=False, hatches=[(40, 2, 0.8)], tone=0.5, sw=1.4)
    E.line([(hx - 4, hy + 2), (hx + 8, hy - 2)], w=3.4, smooth=False)
    hand_dot(E, (hx, hy), 7, 0.1)
    return _end(E, pess_pip_close())


@suit
def su10(rng):
    """Ten: a narrow room at night with one window, a pale sky in it; a man writes at a desk with a stack of
    finished pages at his elbow, the bed behind him made."""
    E = _pip(10, "j", rng)
    FL = 1010
    TOP = 800
    wall(E, 340, FL, op=0.18)
    fade(E, IX0, 340, 400, FL, op=0.75, side="l", reach=1.0)
    fade(E, 70, 340, IX1, 520, op=0.65, side="t", reach=1.0)
    window(E, 430, 380, 566, 690, tone=0.1, panes=(1, 2), glow=BONE)
    sky(E, 392, 560, strongest=0.18, weakest=0.04, gap=6, x0=432, x1=564, tint=0.25)
    floor_band(E, FL, 0.2)
    # the made bed behind him
    rect(E, 80, 740, 100, 900, hatches=[(80, 2.4, 0.55)], tone=0.3, sw=1.8)
    rect(E, 90, 880, 270, 926, hatches=[(0, 2.6, 0.4)], tone=0.4, sw=1.8)
    E.shape([(100, 860), (262, 860), (270, 892), (92, 892)], smooth=False, hatches=[(60, 3, 0.35), (-30, 3.6, 0.3)], tone=0.4, sw=1.8)
    E.shape(ellipse_pts(132, 846, 34, 16, 14), hatches=[(0, 3, 0.3)], tone=0.2, sw=1.6)
    for lx in (96, 266):
        E.line([(lx, 926), (lx, FL)], w=4, smooth=False)
    fade(E, 80, 740, 270, FL, op=0.7, side="l", reach=1.0)
    chair_side(E, 300, FL, seat=125, f_dir=1, back_h=200, w=96)
    cast(E, [(354, TOP + 16), (606, TOP + 16), (616, FL - 2), (346, FL - 2)], 0.6)
    ma = adult(E, 292, FL, 490, pose="sit", facing=1, lean=0.3, tilt=8, garment="coat", hair="dark", wash_op=0.85, look=0.9,
               hands={"near": (384, TOP - 12), "far": (360, TOP - 6)})
    rect(E, 350, TOP, 606, TOP + 16, hatches=[(2, 3, 0.4)], sw=2)
    rect(E, 362, TOP + 16, 596, TOP + 66, hatches=[(80, 4, 0.3)], tone=0.12, sw=1.8)
    for lx in (370, 590):
        rect(E, lx - 7, TOP + 66, lx + 7, FL, hatches=[(80, 2.6, 0.5)], sw=1.6)
    # finished pages, squared neatly, and the page being written
    for k in range(10):
        rect(E, 452, TOP - 4 - k * 4, 528, TOP - k * 4, hatches=[(0, 3, 0.1 + 0.02 * k)], sw=1.0)
    E.shape([(360, TOP - 4), (440, TOP - 4), (448, TOP + 4), (352, TOP + 4)], smooth=False, sw=1.3)
    ruled(E, 366, TOP - 3, 436, TOP + 3, 1, 0.55, rng)
    hx, hy = ma["hands"]["near"]
    pen_hand(E, (hx + 2, hy + 2), -0.4, 18)
    hand_dot(E, (hx, hy), 7, 0.1)
    table_lamp(E, 566, TOP, 0.7)
    return _end(E, pess_pip_close())


# ------------------------------------------------------------------ courts

@suit
def su11(rng):
    """Child: a child sits on the floor drawing on a large sheet with a stub of chalk: a house, a sun and a very
    large animal with antlers. Nobody is watching."""
    E = _court(1, "k", rng)
    FL = 1030
    wall(E, 212, 640, op=0.16)
    fade(E, IX0, 212, 300, 640, op=0.5, side="l", reach=1.0)
    window(E, 380, 300, 560, 540, tone=0.18, panes=(2, 2), glow=BONE)
    # shelf with toys: a block house, a wooden horse
    rect(E, 90, 560, 300, 572, hatches=[(0, 3, 0.4)], sw=1.8)
    rect(E, 112, 520, 150, 560, hatches=[(80, 3, 0.4)], tone=0.2, sw=1.6)
    E.shape([(106, 520), (131, 496), (156, 520)], smooth=False, hatches=[(30, 3, 0.5)], sw=1.6)
    E.shape(ellipse_pts(222, 536, 30, 14, 12), hatches=[(60, 3, 0.4)], tone=0.2, sw=1.6)
    for lx in (200, 214, 232, 244):
        E.line([(lx, 546), (lx, 560)], w=3, smooth=False)
    E.shape(ellipse_pts(250, 516, 9, 8, 10), sw=1.5)
    E.line([(240, 526), (248, 520)], w=3, smooth=False)
    floor_band(E, 640, 0.2)
    # the big sheet on the floor, in perspective, and the drawing on it
    sheet(E, [(262, 790), (590, 784), (614, 1048), (216, 1056)], hatches=[(0, 4, 0.1)], sw=2.2)
    E.line([(270, 800), (582, 796), (602, 1038), (226, 1046), (270, 800)], w=0.7, op=0.5, smooth=False)
    # house, sun, and the great animal
    E.shape([(316, 930), (316, 876), (366, 876), (366, 930)], smooth=False, fill=None, sw=2.6)
    E.line([(308, 876), (341, 842), (374, 876), (308, 876)], w=2.6, smooth=False)
    E.shape([(332, 930), (332, 900), (350, 900), (350, 930)], smooth=False, fill=None, sw=2.0)
    E.shape(ellipse_pts(552, 838, 24, 22, 14), fill=None, sw=2.6)
    for k in range(10):
        a = k * math.pi / 5
        E.line([(552 + 30 * math.cos(a), 838 + 28 * math.sin(a)), (552 + 44 * math.cos(a), 838 + 41 * math.sin(a))], w=2.2, smooth=False)
    E.shape(ellipse_pts(470, 962, 82, 42, 16), fill=None, sw=2.8)
    for lx, ly in ((410, 1000), (440, 1004), (500, 1004), (530, 1000)):
        E.line([(lx, ly), (lx - 2, ly + 40)], w=3.0, smooth=False)
    E.line([(540, 940), (580, 896), (596, 912)], w=2.8)
    E.shape(ellipse_pts(590, 906, 15, 11, 10), fill=None, sw=2.4)
    antler_lines(E, 582, 898, 0.28, 1, w=2.4)
    antler_lines(E, 590, 898, 0.2, -1, w=2.0)
    E.line([(392, 962), (378, 984)], w=2.6, smooth=False)
    # lap, shoes, and the child leaning over her work
    X, HIP = 164, 984
    floor_shadow(E, 170, 1030, 110, 9, 0.6)
    E.shape(ellipse_pts(X + 60, 1010, 96, 26, 16), hatches=[(78, 3, 0.4), (-40, 3.8, 0.3)], tone=0.3, sw=1.8)
    for sx_ in (X + 118, X + 142):
        E.shape(ellipse_pts(sx_, 1018, 14, 8, 10), hatches=[(60, 1.9, 0.85)], tone=0.7, sw=1.2)
    k_ = child(E, X, HIP, 400, pose="torso", facing=1, lean=0.55, tilt=14, wash_op=0.75, look=0.9,
               hands={"near": (330, 948), "far": (300, 960)})
    hx, hy = k_["hands"]["near"]
    E.line([(hx - 2, hy + 3), (hx + 8, hy + 8)], w=4.0, smooth=False, color=INK)
    hand_dot(E, (hx, hy), 7, 0.4)
    return _end(E, pess_court_close(), top=196, cy=700)


@suit
def su12(rng):
    """Youth: a young person in an attic room writes by lamplight; loose pages on the floor, a violin on the bed,
    the window open on a town below."""
    E = _court(2, "l", rng)
    FL = 1030
    TOP = 800
    wall(E, 212, FL, op=0.18)
    # the sloping roof of the attic
    mass(E, [(IX0, 205), (390, 205), (IX0, 590)], solid=0.6, wash=0.38, sw=2)
    for k in range(4):
        E.line([(IX0 + k * 14, 600 - k * 100), (IX0 + 200 + k * 54, 205)], w=1.0, op=0.45, smooth=False)
    E.line([(IX0, 590), (390, 205)], w=3, smooth=False)
    mass(E, [(IX1 + 10, 205), (560, 205), (IX1 + 10, 300)], solid=0.55, wash=0.35, sw=2)
    fade(E, 70, 212, 330, FL, op=0.55, side="l", reach=1.0)
    # the dormer window, open on the town, the casement swung in
    window_town(E, 400, 340, 566, 660, rng)
    E.shape([(400, 340), (352, 362), (352, 640), (400, 660)], smooth=False, hatches=[(80, 3, 0.4)], tone=0.2, sw=2)
    E.line([(352, 500), (400, 500)], w=1.6, smooth=False)
    floor_band(E, FL - 24, 0.2)
    # the bed in the corner, a violin on its cover
    rect(E, 78, 770, 94, 1000, hatches=[(80, 2.4, 0.55)], tone=0.3, sw=1.8)
    E.shape([(88, 880), (250, 880), (258, 934), (84, 934)], smooth=False, hatches=[(60, 3, 0.35), (-30, 3.6, 0.3)], tone=0.35, sw=1.8)
    E.shape(ellipse_pts(124, 866, 32, 15, 14), hatches=[(0, 3, 0.3)], tone=0.2, sw=1.6)
    for lx in (92, 250):
        E.line([(lx, 934), (lx, FL - 20)], w=4, smooth=False)
    violin(E, 188, 898, 0.85, rot=-8)
    fade(E, 78, 770, 258, FL - 20, op=0.5, side="l", reach=1.0)
    # the desk, the lamp, the young writer
    chair_side(E, 266, FL, seat=118, f_dir=1, back_h=160, w=84)
    cast(E, [(346, TOP + 16), (606, TOP + 16), (616, FL - 2), (338, FL - 2)], 0.55)
    yw = youth(E, 262, FL, 470, pose="sit", facing=1, lean=0.3, tilt=10, garment="coat", hair="dark", wash_op=0.8, look=0.9,
               hands={"near": (372, TOP - 10), "far": (350, TOP - 4)})
    rect(E, 340, TOP, 606, TOP + 16, hatches=[(2, 3, 0.4)], sw=2)
    rect(E, 352, TOP + 16, 596, TOP + 62, hatches=[(80, 4, 0.3)], tone=0.12, sw=1.8)
    for lx in (360, 590):
        rect(E, lx - 7, TOP + 62, lx + 7, FL, hatches=[(80, 2.6, 0.5)], sw=1.6)
    E.shape([(354, TOP - 4), (440, TOP - 4), (448, TOP + 4), (346, TOP + 4)], smooth=False, sw=1.3)
    ruled(E, 360, TOP - 3, 436, TOP + 3, 1, 0.5, rng)
    for k in range(5):
        rect(E, 470, TOP - 4 - k * 4, 540, TOP - k * 4, hatches=[(0, 3, 0.1)], sw=1.0)
    table_lamp(E, 566, TOP, 0.72)
    hx, hy = yw["hands"]["near"]
    pen_hand(E, (hx + 2, hy + 2), -0.4, 18)
    hand_dot(E, (hx, hy), 7, 0.1)
    # loose pages on the floor
    for px, py, rt in ((200, 1004, -12), (292, 1014, 8), (150, 1020, 20), (330, 1000, -20), (240, 1022, 4), (470, 1006, 14)):
        E.add(f'<g transform="rotate({rt} {px} {py})">')
        rect(E, px - 26, py - 12, px + 26, py + 12, sw=1.3)
        ruled(E, px - 20, py - 8, px + 20, py + 8, 2, 0.8, rng)
        E.add("</g>")
    return _end(E, pess_court_close(), top=196, cy=700)


@suit
def su13(rng):
    """Adult: a middle-aged woman at a workbench after the day's labour carves a small figure from wood; a coat on
    a nail, supper dishes on a shelf, shavings on the floor."""
    E = _court(3, "m", rng)
    FL = 1030
    TOP = 790
    wall(E, 212, FL, op=0.2, gap=6.5)
    fade(E, IX0, 212, 280, FL, op=0.55, side="l", reach=1.0)
    fade(E, IX0, 212, IX1, 420, op=0.5, side="t", reach=1.0)
    # shelf with the supper dishes: plates on edge, bowls, a jug
    rect(E, 90, 420, 330, 432, hatches=[(0, 3, 0.4)], sw=1.8)
    for px in (120, 152, 184):
        E.shape(ellipse_pts(px, 396, 12, 24, 12), hatches=[(60, 3, 0.4, (px, 372, px + 12, 420))], tone=0.1, sw=1.6)
    for bx in (232, 288):
        E.shape([(bx - 28, 392), (bx + 28, 392), (bx + 20, 420), (bx - 20, 420)], smooth=False, hatches=[(70, 3, 0.4)], sw=1.8)
        E.shape(ellipse_pts(bx, 392, 28, 5, 12), sw=1.4)
    # coat on a nail
    E.add('<circle cx="110" cy="480" r="4" fill="#2a2622"/>')
    coat = [(98, 486), (128, 486), (144, 520), (150, 700), (138, 780), (86, 780), (74, 700), (82, 520)]
    mass(E, coat, solid=0.3, smooth=False, wash=0.3, sw=2)
    E.line([(112, 492), (112, 780)], w=1.2, op=0.6, smooth=False)
    fade(E, IX0, 400, 330, FL, op=0.4, side="l", reach=1.0)
    # pendant lamp over the bench
    E.line([(470, 212), (470, 400)], w=1.4, smooth=False)
    glow(E, 470, 470, 120, 90, 0.4)
    E.shape([(446, 400), (494, 400), (528, 450), (412, 450)], smooth=False, hatches=[(75, 2.8, 0.5)], tone=0.35, sw=2)
    # tool rack
    rect(E, 420, 560, 600, 574, hatches=[(0, 2.6, 0.5)], sw=1.8)
    for k in range(6):
        tx = 434 + k * 28
        E.line([(tx, 574), (tx, 600 + (k % 3) * 12)], w=3.4, smooth=False)
        rect(E, tx - 4, 574, tx + 4, 590, hatches=[(80, 1.9, 0.85)], sw=1.0)
    floor_band(E, FL - 24, 0.2)
    # bench with a vise
    cast(E, [(320, TOP + 20), (600, TOP + 20), (620, FL), (312, FL)], 0.55)
    wm = adult(E, 224, FL - 18, 540, facing=1, lean=0.24, tilt=16, garment="dress", hair="bun", wash_op=0.85, look=0.9,
               hands={"near": (352, TOP - 40), "far": (338, TOP - 32)})
    rect(E, 310, TOP, 606, TOP + 22, hatches=[(2, 3, 0.4)], sw=2)
    rect(E, 322, TOP + 22, 596, TOP + 66, hatches=[(80, 4, 0.3)], tone=0.15, sw=1.8)
    for lx in (334, 584):
        rect(E, lx - 8, TOP + 66, lx + 8, FL - 18, hatches=[(80, 2.6, 0.5)], sw=1.6)
    rect(E, 330, TOP + 34, 590, TOP + 44, hatches=[(0, 3, 0.4)], sw=1.4)
    rect(E, 560, TOP - 26, 600, TOP, hatches=[(80, 2.4, 0.7)], tone=0.4, sw=1.8)
    # the small carved figure and the knife, drawn over her hands
    fx, fy = 366, TOP - 54
    E.shape([(fx - 9, fy + 40), (fx - 12, fy + 4), (fx - 5, fy - 8), (fx + 5, fy - 8), (fx + 12, fy + 4), (fx + 9, fy + 40)], smooth=False,
            hatches=[(70, 2.2, 0.5)], tone=0.25, sw=1.6)
    E.shape(ellipse_pts(fx, fy - 22, 11, 13, 12), hatches=[(60, 2.6, 0.45)], tone=0.2, sw=1.6)
    hx, hy = wm["hands"]["near"]
    E.line([(hx - 2, hy + 4), (hx - 30, hy + 20)], w=3.2, smooth=False)
    E.line([(hx + 8, hy - 2), (hx + 36, hy - 12)], w=1.6, smooth=False)
    hand_dot(E, (hx, hy), 7, 0.2)
    hand_dot(E, wm["hands"]["far"], 7, 0.0)
    shavings(E, 250, 560, FL - 8, 12, rng)
    shavings(E, 340, 400, TOP - 6, 3, rng)
    return _end(E, pess_court_close(), top=196, cy=700)


@suit
def su14(rng):
    """Elder: an old man sits in a garden with a sketchbook on his knee; a young apprentice stands at his shoulder
    holding a roll of paper, and the old man points to a place on the page."""
    E = _court(4, "n", rng)
    FL = 1010
    sky(E, 210, 720, strongest=0.38, weakest=0.04, gap=6, tint=0.8)
    # a leafy tree
    E.shape([(486, 760), (490, 580), (480, 480), (512, 480), (516, 580), (524, 760)], smooth=False, hatches=[(80, 3, 0.5)], tone=0.3, sw=1.8)
    for cx_, cy_, rr in ((500, 420, 80), (440, 450, 60), (566, 450, 60), (500, 360, 58), (470, 350, 40), (540, 340, 44)):
        E.shape(ellipse_pts(cx_, cy_, rr * 1.15, rr, 18), hatches=[(62, 2.6, 0.55), (-38, 3, 0.4)], tone=0.35, sw=1.6)
    # the hedge, and beds laid out in rows
    mass(E, [(70, 740), (610, 724), (610, 800), (70, 810)], solid=0.4, wash=0.3, sw=1.4)
    for _ in range(50):
        hx, hy = rng.uniform(78, 604), rng.uniform(742, 800)
        E.shape(ellipse_pts(hx, hy, rng.uniform(8, 13), rng.uniform(5, 8), 8, rot=rng.uniform(0, 3)), fill=None, sw=0.8)
    E.shape([(70, 810), (610, 800), (610, FL), (70, FL)], smooth=False, hatches=[(2, 6, 0.16)], sw=0.01, outline=False)
    fade(E, 70, 800, IX1, IY1 + 10, op=0.55, side="b", reach=1.0)
    for row in range(3):
        yy = 826 + row * 54
        for k in range(8):
            bx = 100 + k * 66 + (row % 2) * 20
            rr = 14 + row * 3
            E.shape(ellipse_pts(bx, yy, rr * 1.4, rr, 10), hatches=[(62, 2.8, 0.5)], tone=0.3, sw=1.2)
            E.line([(bx, yy - rr), (bx - 4, yy - rr - 12)], w=1.2, smooth=False)
    E.shape([(280, FL), (330, FL), (420, IY1 + 10), (200, IY1 + 10)], smooth=False, hatches=[(15, 6, 0.2)], sw=1.4)
    iso.grass(E, FL, IY1, 300)
    floor_shadow(E, 220, FL - 2, 150, 9, 0.7)
    # the apprentice, standing at the old man's shoulder with a roll of paper
    ap = youth(E, 96, FL, 520, facing=1, lean=0.16, tilt=12, garment="coat", hair="dark", wash_op=0.85, look=0.9,
               hands={"near": (216, 640), "far": (176, 700)})
    E.shape([(196, 668), (254, 628), (262, 644), (204, 684)], smooth=False, hatches=[(40, 2.4, 0.4)], tone=0.12, sw=1.6)
    E.shape(ellipse_pts(258, 636, 6, 9, 8, rot=0.5), fill=None, sw=1.3)
    hand_dot(E, ap["hands"]["near"], 7, 0.3)
    # bench and the old man
    chair_side(E, 250, FL, seat=130, f_dir=1, back_h=210, w=170)
    el = elder(E, 240, FL, 520, pose="sit", facing=1, lean=0.3, garment="long", hair="white", wash_op=0.85, look=0.9, tilt=6,
               hands={"near": (350, 800), "far": (372, 836)})
    # the sketchbook on his knee, the page showing a garden plan
    E.add('<g transform="rotate(-14 392 812)">')
    sheet(E, [(344, 764), (440, 764), (440, 860), (344, 860)], hatches=[(0, 4, 0.08)], sw=2)
    for (x0, y0, x1, y1) in ((356, 776, 392, 798), (404, 776, 430, 798), (356, 812, 430, 826), (356, 838, 392, 852)):
        rect(E, x0, y0, x1, y1, fill=None, hatches=[(30, 3.2, 0.3)], sw=1.0)
    E.line([(398, 800), (398, 852)], w=0.9, op=0.7, smooth=False)
    E.add("</g>")
    hx, hy = el["hands"]["near"]
    E.line([(hx, hy), (hx + 22, hy - 6), (hx + 38, hy - 22)], w=2.6, smooth=False)
    hand_dot(E, (hx, hy), 7, 0.0)
    hand_dot(E, el["hands"]["far"], 7, 0.0)
    return _end(E, pess_court_close(), top=196, cy=700)


CARDS = {f"su{n:02d}": fn for n, fn in enumerate(
    (su01, su02, su03, su04, su05, su06, su07, su08, su09, su10, su11, su12, su13, su14), start=1)}
