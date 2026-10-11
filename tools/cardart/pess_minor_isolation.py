"""Pessimist deck, minor series, suit of Isolation (is01-is14): dismissal of the surplus of awareness.

Pips is01-is10: pess_pip_open("isolation", n) draws the plate with a frieze of n closed shutters;
the scene of the card's Image paragraph is drawn in the plate below the frieze (PESS_VIGNETTE),
then pess_pip_close(). No slatted rectangle is drawn in the scene, so the shutter count stays
readable.

Courts is11-is14: pess_court_open("isolation", age) counts the age in emblems at the top, then a
scene from the card's Figure paragraph, then pess_court_close(). The four ages use the same kind of
person at four stages, drawn by the reusable helpers child(), youth(), adult() and elder().

Style: etched line on bare paper, as in the major cards. Objects, figures, walls and floors are paper;
tone comes only from hatching and cross-hatching (the Etch hatching of pess_awakening, same gaps and
weights), and the slate wash appears as a thin tint on a few areas (sky, a window, a shadow). Plate is
an Etch whose shape(), line() and limb() add a gentle wobble and a doubled outline of varying weight,
and which turns a mid-grey fill or a wash into hatching, so any helper drawn through it is etched.

Reusable figure engine (import these from other suits; build the plate with Plate(rng, tag)):
  figure()  one person: side, front or back view; standing, seated or torso only; arms placed by
            the hand target with two-bone joints (shoulder, elbow, wrist, hand). wash_op is the
            tone of the garment (hatch density), not a wash.
  child(), youth(), adult(), elder()  the four ages, built on figure().
  mix(), rect(), slate(), sky(), wall(), floor_band(), window(), table_front(), chair_side(), jar(),
  cup(), book(), table_lamp(), curtain(), hand_dot()  small scene pieces.
Tone is set by one module constant, CONTRAST: it scales the hatch density of every Plate shape, the slate
washes (slate(), sky(), fade(), cast(), mass(), window(), floor_band(), vignette) and the figure garments, so
other suits can import the module and set CONTRAST once.
Everything uses the rng passed in; ids are prefixed by the card's tag so they stay unique in a document.
"""

import math

from .common import (ETCH_INK, IMAGE_BOX, PESS_PAPER, PESS_VIGNETTE, WASH, f,
                     pess_court_close, pess_court_open, pess_pip_close, pess_pip_open, svg)
from .pess_awakening import (Etch, PAPER_FILL, _bbox, _poly_d, _smooth_d, draw_hat, ellipse_pts, head)
from .pess_world import Pen

INK = ETCH_INK
SLATE = WASH["slate"]
BONE = WASH["bone"]
IX0, IY0, IX1, IY1 = IMAGE_BOX
VX0, VY0, VX1, VY1 = PESS_VIGNETTE
CONTRAST = 1.0   # global: scales the slate shadow washes and the hatch density (0 = pale, 1 = default, 1.3 = heavy)


def _boost():
    """Hatch strength factor from CONTRAST (1.3 at the default)."""
    return 0.75 + 0.55 * CONTRAST


# ------------------------------------------------------------------ colour helpers

def mix(c1, c2, t):
    """Blend two #rrggbb colours; t=0 gives c1, t=1 gives c2."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02x}" for p, q in zip(a, b))


def _lum(c):
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


_PAPER_LUM = _lum(PAPER_FILL)
DARK = mix(INK, SLATE, 0.22)   # the near-black of the solid underlays


def suit_colour(colour):
    """Decorator for a card function: while it draws, the shadow washes, tints, sky gradients and
    dark underlays use `colour` in place of slate. Each suit passes its own WASH colour, so the
    suits can be told apart; Isolation keeps slate. Restores the previous colour afterwards."""
    def deco(fn):
        def wrapped(rng):
            global SLATE, DARK
            saved = SLATE, DARK
            SLATE, DARK = colour, mix(INK, colour, 0.22)
            try:
                return fn(rng)
            finally:
                SLATE, DARK = saved
        wrapped.__name__, wrapped.__doc__ = fn.__name__, fn.__doc__
        return wrapped
    return deco


def _poly(pts):
    return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + " Z"


# ------------------------------------------------------------------ the plate: an Etch with a hand

class Plate(Etch):
    """Etch with a hand-etched line: gentle wobble, doubled outlines of varying weight, hatched tone.

    shape(): fills are paper; a mid-grey fill or a wash becomes hatching of the same tone (tone= gives
    it directly); tint=(colour, opacity) is the one real wash. Very dark fills (ink details, shoes)
    stay solid. line() and limb() wobble as well."""

    # -- wobble
    def _wob(self, pts, smooth, amp=None, step=34):
        r = self.rng
        x0, y0, x1, y1 = _bbox(pts, 0)
        size = math.hypot(x1 - x0, y1 - y0)
        if amp is None:
            amp = 0.3 if size < 50 else 0.7 if size < 250 else 1.0
        if smooth:
            return [(x + r.uniform(-amp, amp) * 0.6, y + r.uniform(-amp, amp) * 0.6) for x, y in pts]
        out, n = [], len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            out.append((a[0] + r.uniform(-amp, amp) * 0.4, a[1] + r.uniform(-amp, amp) * 0.4))
            k = int(math.hypot(b[0] - a[0], b[1] - a[1]) // step)
            for j in range(1, k + 1):
                t = j / (k + 1)
                out.append((a[0] + (b[0] - a[0]) * t + r.uniform(-amp, amp), a[1] + (b[1] - a[1]) * t + r.uniform(-amp, amp)))
        return out

    def _wob_open(self, pts, amp=0.7, step=30):
        r = self.rng
        out = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            k = int(math.hypot(b[0] - a[0], b[1] - a[1]) // step)
            for j in range(1, k + 1):
                t = j / (k + 1)
                out.append((a[0] + (b[0] - a[0]) * t + r.uniform(-amp, amp), a[1] + (b[1] - a[1]) * t + r.uniform(-amp, amp)))
            out.append((b[0] + r.uniform(-amp, amp) * 0.4, b[1] + r.uniform(-amp, amp) * 0.4))
        return out

    # -- tone
    def hatch_d(self, d, bbox, angle, gap, op=0.6, w=0.7, sub=None, color=INK, jitter=0.6):
        """Parallel pen lines clipped to path d (as Etch.hatch_d) with a slight bow, uneven spacing and
        three line weights."""
        r = self.rng
        x0, y0, x1, y1 = sub or bbox
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        R = math.hypot(x1 - x0, y1 - y0) / 2 + 4
        buckets = ([], [], [])
        y, i = cy - R, 0
        while y < cy + R:
            if r.random() > 0.05:
                buckets[i % 3].append(f"M{f(cx - R)},{f(y)} Q{f(cx)},{f(y + r.uniform(-1.4, 1.4))} {f(cx + R)},{f(y + r.uniform(-jitter, jitter))}")
            y += gap * r.uniform(0.86, 1.14)
            i += 1
        cid = self.uid("h")
        s = f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">'
        if sub:
            sid = self.uid("s")
            s += f'<clipPath id="{sid}"><rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}"/></clipPath><g clip-path="url(#{sid})">'
        s += f'<g transform="rotate({angle} {f(cx)} {f(cy)})" fill="none" stroke="{color}" opacity="{op}">'
        for ws, b in zip((w * 0.85, w * 1.15, w * 0.7), buckets):
            if b:
                s += f'<path d="{" ".join(b)}" stroke-width="{f(ws)}"/>'
        s += "</g>" + ("</g>" if sub else "") + "</g>"
        self.add(s)

    def _tone(self, t, pts, angle=64):
        """Hatches of tone t (0 to 1): a single set when light, crossed on the shadow half, then fully."""
        if t <= 0:
            return []
        t = min(t * _boost(), 0.9)
        x0, y0, x1, y1 = _bbox(pts, 0)
        g = max(2.1, 4.8 - 3.4 * t)
        hs = [(angle, g, min(0.85, 0.28 + 0.6 * t))]
        if t > 0.26:
            sub = ((x0 + x1) / 2, y0, x1, y1) if t < 0.55 else None
            hs.append((angle - 112, g * 1.2, min(0.75, 0.2 + 0.55 * t), sub))
        if t > 0.7:
            hs.append((angle + 38, g * 1.1, 0.55))
        return hs

    @staticmethod
    def _dense(hatches):
        """Scale explicit hatches by CONTRAST: closer lines, stronger ink."""
        b = _boost()
        out = []
        for h in hatches:
            a, g, op = h[:3]
            out.append((a, max(1.7, g / (0.5 + 0.5 * b)), min(0.92, op * b)) + tuple(h[3:]))
        return out

    @staticmethod
    def _fill(fill):
        if not fill or fill[0] != "#" or len(fill) != 7:
            return fill, 0.0
        q = _lum(fill) / _PAPER_LUM
        if q < 0.42:
            return fill, 0.0
        t = 1.0 - q
        return PAPER_FILL, (t if t >= 0.1 else 0.0)

    # -- drawing
    def shape(self, pts, smooth=True, fill=PAPER_FILL, wash=None, wash_op=0.3, hatches=(), sw=1.8,
              outline=True, grain=0.0, tone=0.0, tint=None):
        p1 = self._wob(pts, smooth)
        fl, t = self._fill(fill)
        t = max(t, tone)
        if wash:
            t = max(t, min(0.7, wash_op * 0.9))
        hs = self._dense(hatches) + self._tone(t, p1)
        d = Etch.shape(self, p1, smooth=smooth, fill=fl, wash=tint[0] if tint else None,
                       wash_op=tint[1] if tint else 0.3, hatches=hs, sw=sw, outline=False, grain=grain)
        if outline and sw > 0:
            self.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(sw * 0.85)}" stroke-linejoin="round"/>')
            if sw >= 1.2:
                p2 = self._wob(pts, smooth, amp=0.9)
                d2 = _smooth_d(p2) if smooth else _poly_d(p2)
                self.add(f'<path d="{d2}" fill="none" stroke="{INK}" stroke-width="{f(sw * 0.5)}" opacity="0.6" stroke-linejoin="round"/>')
        return d

    def line(self, pts, w=1.5, op=1.0, smooth=True, dash=None, color=INK, cap="round"):
        p = self._wob_open(list(pts))
        Etch.line(self, p, w, op, smooth and len(pts) > 2, dash, color, cap)
        if w >= 1.6 and color == INK and not dash:
            Etch.line(self, self._wob_open(list(pts), 1.0), w * 0.45, op * 0.55, smooth and len(pts) > 2, None, color, cap)

    def limb(self, pts, w, fill=PAPER_FILL, taper=False, tone=None):
        """A limb: an etched capsule per segment (so the joints show), lightly hatched."""
        t = self._fill(fill)[1] if tone is None else tone
        for k, (a, b) in enumerate(zip(pts, pts[1:])):
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            r0, r1 = (w + 2) / 2, (w + 2) / 2 * (0.82 if taper else 1.0)
            cap = []
            for j in range(7):
                th = -math.pi / 2 + math.pi * j / 6
                cap.append((b[0] + r1 * math.cos(ang + th), b[1] + r1 * math.sin(ang + th)))
            for j in range(7):
                th = math.pi / 2 + math.pi * j / 6
                cap.append((a[0] + r0 * math.cos(ang + th), a[1] + r0 * math.sin(ang + th)))
            hs = [(math.degrees(ang) + 62, 2.8, 0.3 + 0.3 * t)] if w > 8 else []
            self.shape(cap, smooth=False, fill=PAPER_FILL, hatches=hs, tone=max(0.0, t - 0.2), sw=1.5)


def rect(E, x0, y0, x1, y1, **kw):
    """An etched rectangle. kw as Plate.shape."""
    return E.shape([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], smooth=False, **kw)


def hand_dot(E, p, r=7, ang=0.0):
    """A hand: a small palm along ang (radians) with a thumb. Also redraws a hand over a prop it holds."""
    x, y = p
    E.shape(ellipse_pts(x + math.cos(ang) * r * 0.2, y + math.sin(ang) * r * 0.2, r * 1.05, r * 0.75, 10, rot=ang), sw=1.3)
    th = ang + 0.95
    E.line([(x + math.cos(th) * r * 0.2, y + math.sin(th) * r * 0.2), (x + math.cos(th - 0.3) * r * 1.2, y + math.sin(th - 0.3) * r * 1.2)],
           w=1.3, smooth=False)


# ------------------------------------------------------------------ atmosphere and ground

def slate(E, x0, y0, x1, y1, op=0.2, filt="softwash"):
    """A slate tint over a rectangle with soft edges (use for a sea, a shadow, a window)."""
    E.add(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{SLATE}" opacity="{min(0.85, op * CONTRAST):.3f}" filter="url(#{filt})"/>')


def fade(E, x0, y0, x1, y1, op=0.3, side="l", clip=None, reach=1.0, colour=None):
    """A graded slate tint over a box, strongest at the given side (l, r, t or b) and fading to nothing
    across reach (0 to 1) of the box; clip is an optional polygon. This is the shadow side of a room, a
    figure, a floor."""
    colour = colour or SLATE
    op = min(0.9, op * CONTRAST * 0.78)
    gid = E.uid("g")
    xa, xb, ya, yb = {"l": (0, 1, 0, 0), "r": (1, 0, 0, 0), "t": (0, 0, 0, 1), "b": (0, 0, 1, 0)}[side]
    E.add(f'<linearGradient id="{gid}" x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}">'
          f'<stop offset="0" stop-color="{colour}" stop-opacity="{op:.3f}"/>'
          f'<stop offset="{0.5 * reach:.2f}" stop-color="{colour}" stop-opacity="{op * 0.45:.3f}"/>'
          f'<stop offset="{reach:.2f}" stop-color="{colour}" stop-opacity="0"/></linearGradient>')
    if clip:
        cid = E.uid("q")
        E.add(f'<clipPath id="{cid}"><path d="{_poly(clip)}"/></clipPath><g clip-path="url(#{cid})">')
    E.add(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" fill="url(#{gid})"/>')
    if clip:
        E.add("</g>")


def cast(E, pts, op=0.4):
    """A soft slate shadow with blurred edges: under a table, behind a figure, on the floor."""
    E.add(f'<path d="{_poly(pts)}" fill="{SLATE}" opacity="{min(0.85, op * CONTRAST):.3f}" filter="url(#wash)"/>')


def floor_shadow(E, cx, cy, rx, ry, op=0.4):
    """A soft elliptical contact shadow on the floor."""
    E.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{SLATE}" opacity="{min(0.85, op * CONTRAST):.3f}" filter="url(#wash)"/>')


def mass(E, pts, solid=0.3, smooth=False, sw=1.6, wash=0.25):
    """A dark mass: dense three-way cross-hatching under a slate tint and a deep underlay (solid sets the
    near-black underlay, 0 to 0.6); the etched lines stay visible through it."""
    d = E.shape(pts, smooth=smooth, hatches=[(62, 2.0, 0.8), (-38, 2.2, 0.7), (12, 2.4, 0.55)],
                tint=(SLATE, min(0.7, wash * CONTRAST)), sw=sw)
    if solid:
        E.add(f'<path d="{d}" fill="{DARK}" opacity="{min(0.8, solid * CONTRAST):.2f}"/>')
    return d


def vignette(E, top=VY0, cx=(VX0 + VX1) / 2, cy=800, op=0.32, r=520):
    """A radial slate fall-off over the plate, clear in the middle and deepening to the corners."""
    gid = E.uid("v")
    o = min(0.85, op * CONTRAST)
    E.add(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{f(cx)}" cy="{f(cy)}" r="{r}">'
          f'<stop offset="0.5" stop-color="{SLATE}" stop-opacity="0"/>'
          f'<stop offset="0.8" stop-color="{SLATE}" stop-opacity="{o * 0.45:.3f}"/>'
          f'<stop offset="1" stop-color="{DARK}" stop-opacity="{o:.3f}"/></radialGradient>'
          f'<rect x="{VX0}" y="{top}" width="{VX1 - VX0}" height="{VY1 - top}" fill="url(#{gid})"/>')


def sky(E, y0, y1, strongest=0.5, weakest=0.05, gap=6.0, x0=IX0, x1=IX1, tint=0.0, w=0.7):
    """Horizontal etched lines that thin from y0 to y1 (as in the major cards' skies), over a slate
    gradient: tint is the opacity at the top, fading toward the horizon, so it reads as sky."""
    r = E.rng
    b = _boost()
    if tint:
        gid = E.uid("g")
        o = min(0.85, tint * CONTRAST)
        E.add(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
              f'<stop offset="0" stop-color="{DARK}" stop-opacity="{o:.3f}"/>'
              f'<stop offset="0.45" stop-color="{SLATE}" stop-opacity="{o * 0.55:.3f}"/>'
              f'<stop offset="0.85" stop-color="{SLATE}" stop-opacity="{o * 0.14:.3f}"/>'
              f'<stop offset="1" stop-color="{SLATE}" stop-opacity="0"/></linearGradient>'
              f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#{gid})"/>')
    buckets = {}
    n = int((y1 - y0) / gap)
    for k in range(n):
        y = y0 + k * gap + r.uniform(-0.8, 0.8)
        op = round(min(0.9, (strongest + (weakest - strongest) * k / max(1, n - 1)) * b) * 20) / 20
        buckets.setdefault(op, []).append(f"M{x0},{f(y)} Q{f((x0 + x1) / 2)},{f(y + r.uniform(-1.4, 1.4))} {x1},{f(y + r.uniform(-1, 1))}")
    for op, ds in buckets.items():
        E.add(f'<path d="{" ".join(ds)}" fill="none" stroke="{INK}" stroke-width="{w}" opacity="{op:.2f}"/>')


def wall(E, y0, y1, x0=IX0, x1=IX1, gap=7.0, op=0.2, w=0.7):
    """Wall hatching: broken vertical pen lines, open at the top and closing toward the floor."""
    r = E.rng
    d = []
    x = x0 + r.uniform(0, gap)
    while x < x1:
        ya = y0 + r.uniform(0, 0.55) * (y1 - y0)
        yb = y1 - r.uniform(0, 24)
        d.append(f"M{f(x)},{f(ya)} Q{f(x + r.uniform(-1.2, 1.2))},{f((ya + yb) / 2)} {f(x + r.uniform(-1, 1))},{f(yb)}")
        x += gap * r.uniform(0.8, 1.25)
    E.add(f'<path d="{" ".join(d)}" fill="none" stroke="{INK}" stroke-width="{w}" opacity="{min(0.6, op * _boost() * 1.3):.2f}"/>')


def floor_band(E, y, op=0.28, x0=IX0, x1=IX1, y1=IY1):
    """Floor: horizontal etched lines opening toward the viewer, a few receding board lines, the skirting
    line, and a slate tint that deepens toward the viewer with a dark contact band under the wall."""
    r = E.rng
    b = _boost()
    gid = E.uid("g")
    E.add(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="{DARK}" stop-opacity="{min(0.8, 0.5 * CONTRAST):.3f}"/>'
          f'<stop offset="0.35" stop-color="{SLATE}" stop-opacity="{min(0.8, 0.3 * CONTRAST):.3f}"/>'
          f'<stop offset="1" stop-color="{SLATE}" stop-opacity="{min(0.8, 0.46 * CONTRAST):.3f}"/></linearGradient>')
    E.add(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{y1 - y}" fill="url(#{gid})"/>')
    d, yy, gap = [], y + 5, 3.6
    while yy < y1 + 10:
        d.append(f"M{x0 - 10},{f(yy)} Q{f((x0 + x1) / 2)},{f(yy + r.uniform(-1, 1))} {x1 + 10},{f(yy + r.uniform(-0.8, 0.8))}")
        yy += gap
        gap *= 1.07
    E.add(f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width="0.7" opacity="{min(0.8, 0.4 * b):.2f}" fill="none"/>')
    bd = [f"M{f(340 + k * 20)},{f(y)} L{f(340 + k * 95)},{f(y1)}" for k in range(-6, 8)]
    E.add(f'<path d="{" ".join(bd)}" stroke="{INK}" stroke-width="0.6" opacity="{min(0.7, (op + 0.1) * b):.2f}" fill="none"/>')
    dk = [f"M{x0 - 10},{f(y + 3 + k * 2.6)} L{x1 + 10},{f(y + 3 + k * 2.6 + r.uniform(-0.6, 0.6))}" for k in range(9)]
    E.add(f'<path d="{" ".join(dk)}" stroke="{INK}" stroke-width="0.9" opacity="{min(0.85, 0.5 * CONTRAST):.2f}" fill="none"/>')
    E.line([(x0, y), (x1, y)], w=1.9, smooth=False)


def glow(E, x, y, rx, ry, op=0.3, colour=BONE):
    """A small blurred glow of the second colour (bone) around a light."""
    E.add(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}" fill="{colour}" opacity="{op}" filter="url(#wash)"/>')


def clip_open(E, x0, y0, x1, y1):
    """Open a group clipped to a rectangle (for a figure seen through a window); close with clip_close()."""
    cid = E.uid("w")
    E.add(f'<clipPath id="{cid}"><rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}"/></clipPath>'
          f'<g clip-path="url(#{cid})">')


def clip_close(E):
    E.add("</g>")


def window(E, x0, y0, x1, y1, tone=0.55, panes=(2, 2), glow=None):
    """A window with sill and muntins; tone is the darkness of the glass (night), as hatch density, a
    graded slate tint and, for dark panes, a deep underlay."""
    rect(E, x0 - 10, y0 - 10, x1 + 10, y1 + 10, sw=2)
    rect(E, x0, y0, x1, y1, tint=(SLATE, min(0.6, (0.1 + 0.4 * tone) * CONTRAST)), tone=tone, sw=1.8)
    if tone > 0.3:
        fade(E, x0, y0, x1, y1, op=0.9 * tone, side="t", reach=1.0, colour=DARK, clip=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
    if glow:
        E.add(f'<ellipse cx="{f((x0 + x1) / 2)}" cy="{f(y1 - 40)}" rx="{f((x1 - x0) / 2.3)}" ry="40" fill="{glow}" opacity="0.3" filter="url(#wash)"/>')
    nx, ny = panes
    for i in range(1, nx):
        xx = x0 + (x1 - x0) * i / nx
        rect(E, xx - 3, y0, xx + 3, y1, sw=1.3)
    for j in range(1, ny):
        yy = y0 + (y1 - y0) * j / ny
        rect(E, x0, yy - 3, x1, yy + 3, sw=1.3)
    rect(E, x0 - 22, y1 + 10, x1 + 22, y1 + 22, hatches=[(0, 3, 0.3)], sw=1.8)


# ------------------------------------------------------------------ furniture and props

def table_front(E, x0, x1, top, floor, thick=16, legs=(0.07, 0.93), cloth=None, wash_op=0.0):
    """A table seen from the side or front: slab, two legs to the floor, optional hanging cloth."""
    if cloth:
        d = [(x0 - 6, top), (x1 + 6, top), (x1 + 14, top + cloth), (x0 - 14, top + cloth)]
        E.shape(d, smooth=False, hatches=[(90, 5, 0.4)], tone=wash_op, sw=1.8)
        for k in range(1, 9):
            xx = x0 + (x1 - x0) * k / 9
            E.line([(xx, top + 4), (xx + 3, top + cloth - 3)], w=0.8, op=0.5, smooth=False)
        return
    for t in legs:
        lx = x0 + (x1 - x0) * t
        rect(E, lx - 7, top + thick, lx + 7, floor, hatches=[(80, 2.6, 0.5)], sw=1.6)
    rect(E, x0, top, x1, top + thick, hatches=[(3, 3.4, 0.35)], sw=1.8)


def chair_side(E, x, floor, seat=125, f_dir=1, back_h=190, w=100):
    """A plain chair in profile, back at -f_dir side of the seat; x is the seat centre."""
    sx0, sx1 = x - w / 2, x + w / 2
    sy = floor - seat
    b = x - f_dir * w / 2
    for lx in (sx0 + 6, sx1 - 6):
        rect(E, lx - 5, sy + 12, lx + 5, floor, hatches=[(80, 2.6, 0.5)], sw=1.5)
    rect(E, min(sx0, sx1), sy, max(sx0, sx1), sy + 14, hatches=[(4, 3, 0.4)], sw=1.8)
    rect(E, b - 6, sy - back_h, b + 6, sy + 12, hatches=[(80, 2.6, 0.5)], sw=1.6)
    rect(E, b - 9, sy - back_h - 8, b + 9, sy - back_h + 14, sw=1.5)


def jar(E, x, y, w, h, lid=True, tone=0.18):
    """A glass jar standing with its base at (x, y); returns the box (x0, y0, x1, y1) of the glass."""
    x0, x1 = x - w / 2, x + w / 2
    top = y - h
    body = [(x0 + 6, top), (x1 - 6, top), (x1, top + 14), (x1, y - 12), (x1 - 10, y), (x0 + 10, y), (x0, y - 12), (x0, top + 14)]
    E.shape(body, smooth=False, tone=tone * 0.7, hatches=[(78, 5.5, 0.16, (x0 + w * 0.55, top, x1, y))], sw=2)
    E.line([(x0 + 10, top + 24), (x0 + 10, y - 26)], w=2, op=0.8, color="#ffffff", smooth=False)
    if lid:
        rect(E, x0 + 2, top - 10, x1 - 2, top + 2, hatches=[(80, 2, 0.6)], sw=1.8)
    return (x0, top, x1, y)


def cup(E, x, y, s=1.0, tilt=0):
    """A small cup with a handle, base centre at (x, y)."""
    E.add(f'<g transform="rotate({tilt} {f(x)} {f(y)})">')
    pts = [(x - 20 * s, y - 34 * s), (x + 20 * s, y - 34 * s), (x + 15 * s, y - 4 * s), (x - 15 * s, y - 4 * s)]
    E.shape(pts, hatches=[(70, 3, 0.4, (x, y - 34 * s, x + 20 * s, y))], sw=1.8)
    E.shape(ellipse_pts(x + 24 * s, y - 20 * s, 9 * s, 10 * s, 12), fill=None, sw=3.0)
    E.line([(x - 17 * s, y - 33 * s), (x + 17 * s, y - 33 * s)], w=1.0, smooth=False)
    E.add("</g>")


def book(E, x, y, w, h, hatch=(70, 2.6, 0.5), cover=0.4):
    """A closed book lying flat, seen from the side: spine block with page edge. (x, y) is its base-left."""
    rect(E, x, y - h, x + w, y, hatches=[hatch], tone=cover * 0.6, sw=1.8)
    rect(E, x + 4, y - h + 4, x + w - 3, y - 4, hatches=[(0, 3.4, 0.3)], sw=0.9)


def table_lamp(E, x, y, s=1.0, glow_=True):
    """A table lamp, base at (x, y). Returns the shade centre. One small bone glow."""
    if glow_:
        glow(E, x, y - 92 * s, 78 * s, 66 * s, 0.34)
    rect(E, x - 4 * s, y - 62 * s, x + 4 * s, y - 8 * s, hatches=[(80, 2, 0.6)], sw=1.5)
    E.shape(ellipse_pts(x, y - 6 * s, 26 * s, 7 * s, 14), hatches=[(0, 2, 0.5)], sw=1.6)
    E.shape([(x - 16 * s, y - 110 * s), (x + 16 * s, y - 110 * s), (x + 34 * s, y - 62 * s), (x - 34 * s, y - 62 * s)],
            smooth=False, hatches=[(75, 3, 0.35)], sw=1.8)
    return x, y - 86 * s


def curtain(E, x0, x1, y0, y1, drawn=1.0, side="right", op=0.4):
    """A hanging curtain of vertical folds along the wall from x0 to x1; drawn is the fraction closed."""
    wdt = (x1 - x0) * drawn
    xa, xb = (x0, x0 + wdt) if side == "left" else (x1 - wdt, x1)
    folds = max(3, int(wdt / 22))
    pts_top = [(xa + wdt * k / folds, y0) for k in range(folds + 1)]
    bottom = [(xa + wdt * k / folds + (7 if k % 2 else -7), y1) for k in range(folds, -1, -1)]
    E.shape(pts_top + bottom, smooth=False, hatches=[(88, 4, 0.45)], tone=op * 0.7, sw=1.8)
    for k in range(1, folds):
        xx = xa + wdt * k / folds
        E.line([(xx, y0 + 4), (xx + (6 if k % 2 else -6), y1 - 4)], w=1.0, op=0.7, smooth=False)
    E.line([(x0 - 6, y0), (x1 + 6, y0)], w=3.0, smooth=False)


# ------------------------------------------------------------------ figures

# Proportions as fractions of the standing height h.
_KIND = {
    "child": dict(r=0.105, leg=0.43, torso=0.30, upper=0.19, fore=0.17, thigh=0.23, shin=0.23, build=1.2,
                  garment="smock", hair="dark", lean=0.0, headfwd=0.0),
    "youth": dict(r=0.08, leg=0.50, torso=0.31, upper=0.17, fore=0.16, thigh=0.24, shin=0.25, build=0.95,
                  garment="coat", hair="dark", lean=0.0, headfwd=0.0),
    "adult": dict(r=0.077, leg=0.50, torso=0.31, upper=0.17, fore=0.16, thigh=0.24, shin=0.25, build=1.0,
                  garment="dress", hair="bun", lean=0.04, headfwd=0.0),
    "elder": dict(r=0.077, leg=0.50, torso=0.31, upper=0.17, fore=0.16, thigh=0.24, shin=0.25, build=0.95,
                  garment="long", hair="white", lean=0.30, headfwd=0.28),
}


def _rot(p, a):
    x, y = p
    return (x * math.cos(a) - y * math.sin(a), y * math.cos(a) + x * math.sin(a))


def _two_bone(sh, tgt, l1, l2, bend):
    """Elbow and hand for a shoulder, a hand target and the two bone lengths; the target is
    pulled in if out of reach. bend=+1 bends the elbow below/behind for a figure facing right."""
    dx, dy = tgt[0] - sh[0], tgt[1] - sh[1]
    dist = math.hypot(dx, dy) or 1e-6
    d = min(max(dist, abs(l1 - l2) + 1.0), l1 + l2 - 1.0)
    ux, uy = dx / dist, dy / dist
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    hh = math.sqrt(max(l1 * l1 - a * a, 0))
    mx, my = sh[0] + ux * a, sh[1] + uy * a
    return (mx - bend * uy * hh, my + bend * ux * hh), (sh[0] + ux * d, sh[1] + uy * d)


def _arm(E, sh, tgt, l1, l2, bend, w, tone):
    """Draw an arm: sleeve from shoulder to elbow and on toward the wrist, bare wrist, hand.
    Returns the hand centre."""
    elbow, hand = _two_bone(sh, tgt, l1, l2, bend)
    E.limb([sh, elbow], w, tone=tone)
    ex, ey = elbow
    vx, vy = hand[0] - ex, hand[1] - ey
    wrist = (ex + vx * 0.8, ey + vy * 0.8)
    E.limb([elbow, wrist], w * 0.84, tone=tone)
    E.limb([wrist, (ex + vx * 0.94, ey + vy * 0.94)], w * 0.5, tone=0.0)
    hp = (ex + vx * 0.97, ey + vy * 0.97)
    hand_dot(E, hp, w * 0.62, math.atan2(vy, vx))
    return hp


def _hair(E, cx, cy, r, style, fd, view):
    """Hair over the skull, etched in dense cross-hatching (dark) or a few light lines (white)."""
    if not style:
        return
    dark = style in ("dark", "bun")
    hatch = [(62, 1.9, 0.85), (-38, 2.2, 0.65)] if dark else [(70, 3.4, 0.3)]
    fill = DARK if dark else PAPER_FILL
    if view == "side":
        pts = [(cx - fd * 0.95 * r, cy + 0.5 * r), (cx - fd * 1.0 * r, cy - 0.25 * r), (cx - fd * 0.6 * r, cy - 0.95 * r),
               (cx + fd * 0.1 * r, cy - 1.14 * r), (cx + fd * 0.7 * r, cy - 0.88 * r), (cx + fd * 0.84 * r, cy - 0.4 * r),
               (cx + fd * 0.3 * r, cy - 0.6 * r), (cx - fd * 0.3 * r, cy - 0.35 * r), (cx - fd * 0.62 * r, cy + 0.15 * r)]
        E.shape(pts, hatches=hatch, fill=fill, sw=1.3)
        if style == "bun":
            E.shape(ellipse_pts(cx - fd * 1.05 * r, cy - 0.15 * r, 0.42 * r, 0.4 * r, 12), hatches=hatch, fill=fill, sw=1.3)
        if dark:   # a thin highlight along the crown keeps the mass etched
            E.line([(cx - fd * 0.45 * r, cy - 0.98 * r), (cx + fd * 0.1 * r, cy - 1.02 * r), (cx + fd * 0.5 * r, cy - 0.85 * r)],
                   w=0.9, op=0.5, color=mix(SLATE, PAPER_FILL, 0.55), smooth=False)
    elif view == "front":
        pts = [(cx - 0.9 * r, cy + 0.05 * r), (cx - 0.88 * r, cy - 0.7 * r), (cx, cy - 1.14 * r), (cx + 0.88 * r, cy - 0.7 * r),
               (cx + 0.9 * r, cy + 0.05 * r), (cx + 0.5 * r, cy - 0.5 * r), (cx, cy - 0.6 * r), (cx - 0.5 * r, cy - 0.5 * r)]
        E.shape(pts, hatches=hatch, fill=fill, sw=1.3)
        if dark:
            E.line([(cx - 0.45 * r, cy - 0.98 * r), (cx + 0.05 * r, cy - 1.04 * r), (cx + 0.45 * r, cy - 0.92 * r)],
                   w=0.9, op=0.5, color=mix(SLATE, PAPER_FILL, 0.55), smooth=False)


def _head_side(E, cx, cy, r, fd, mouth):
    """A small profile head: the nose is a slight bump in the outline, one eye, a brow and a tick of mouth."""
    prof = [(0.0, -1.0), (0.55, -0.84), (0.8, -0.5), (0.88, -0.22), (0.99, 0.08), (0.88, 0.2), (0.9, 0.38), (0.8, 0.58),
            (0.62, 0.82), (0.2, 0.98), (-0.35, 0.9), (-0.78, 0.55), (-0.92, 0.05), (-0.8, -0.55), (-0.45, -0.9)]
    pts = [(cx + fd * x * r, cy + y * r) for x, y in prof]
    E.shape(pts, hatches=[(62, 3, 0.42, (min(cx - r, cx - fd * 0.1 * r), cy - r, max(cx - r, cx - fd * 0.1 * r), cy + r))], sw=1.6)
    ex, ey = cx + fd * 0.5 * r, cy - 0.12 * r
    E.add(f'<circle cx="{f(ex)}" cy="{f(ey)}" r="{f(max(1.1, r * 0.06))}" fill="{INK}"/>')
    E.line([(ex - fd * 0.14 * r, ey - 0.16 * r), (ex + fd * 0.16 * r, ey - 0.2 * r)], w=1.1, smooth=False)
    my = cy + 0.5 * r
    if mouth > 0:
        E.add(f'<ellipse cx="{f(cx + fd * 0.72 * r)}" cy="{f(my)}" rx="{f(0.1 * r)}" ry="{f(max(1.2, 0.13 * r * mouth))}" fill="{INK}"/>')
    else:
        E.line([(cx + fd * 0.62 * r, my + 0.02 * r), (cx + fd * 0.84 * r, my - 0.02 * r)], w=1.1, smooth=False)
    E.line([(cx - fd * 0.1 * r, cy - 0.02 * r), (cx - fd * 0.2 * r, cy + 0.2 * r), (cx - fd * 0.05 * r, cy + 0.26 * r)], w=0.9, smooth=True)


def _head(E, c, cx, cy, r, view, fd, look, mouth, tilt, hat, hair):
    E.add(f'<g transform="rotate({tilt} {f(cx)} {f(cy)})">' if tilt else "<g>")
    if view == "back":
        head(E, cx, cy, r, face="back", f_dir=fd)
    elif view == "front":
        head(E, cx, cy, r, face="front", look=look, mouth=mouth, f_dir=fd)
        _hair(E, cx, cy, r, hair, fd, view)
    else:
        _head_side(E, cx, cy, r, fd, mouth)
        _hair(E, cx, cy, r, hair, fd, view)
    if hat:
        draw_hat(E, hat, cx, cy, r, fd)
    E.add("</g>")


_HEM = {"dress": (None, 0.125), "coat": (0.27, 0.098), "smock": (0.22, 0.14), "long": (None, 0.11),
        "vest": (0.07, 0.085)}


def _outline(c, g, view, h, T, lean, fd, hip, short):
    """Garment outline of the torso (leaned about the hip) and the skirt or coat below it.
    short=True ends the garment at the hip (seated or torso-only figures). Returns the outline and the
    two hem points (front, back), or None for a short garment."""
    b = c["build"]
    hx, hy = hip
    if view == "side":
        fr = [(0.012, 1.012), (0.056, 1.0), (0.082, 0.74), (0.07, 0.35), (0.082, 0.0)]
        bk = [(-0.088, 0.0), (-0.076, 0.35), (-0.092, 0.74), (-0.062, 1.0)]

        def up(p):
            q = _rot((p[0] * h * b, -p[1] * T), lean)
            return (hx + fd * q[0], hy + q[1])
        upper_f, upper_b = [up(p) for p in fr], [up(p) for p in bk]
        sgn = fd
    else:
        fr = [(0.0, 1.012), (0.062, 1.0), (0.078, 0.78), (0.066, 0.38), (0.076, 0.0)]
        bk = [(-0.076, 0.0), (-0.066, 0.38), (-0.078, 0.78), (-0.062, 1.0)]
        upper_f = [(hx + p[0] * h * b, hy - p[1] * T) for p in fr]
        upper_b = [(hx + p[0] * h * b, hy - p[1] * T) for p in bk]
        sgn = 1
    if short:
        low_f, low_b = [(0.08, 0.02)], [(-0.085, 0.03)]
    else:
        hem, flare = _HEM[g]
        if hem is None:
            hem = c["leg"] - (0.07 if g == "dress" else 0.05)
        if g == "vest":
            low_f, low_b = [(0.08, hem)], [(-0.085, hem)]
        else:
            low_f = [(0.085, 0.14), (flare, hem)]
            low_b = [(-flare - 0.012, hem), (-0.095, 0.14)]
    if view != "side":
        low_b = [(-x, y) for x, y in reversed(low_f)]
    lo_f = [(hx + sgn * x * h * b, hy + y * h) for x, y in low_f]
    lo_b = [(hx + sgn * x * h * b, hy + y * h) for x, y in low_b]
    return upper_f + lo_f + lo_b + upper_b, (None if short else (lo_f[-1], lo_b[0]))


def _shoe(E, x, base, fd, h, w=1.0):
    """A small shoe in profile, crosshatched dark."""
    s = h * w
    pts = [(x - fd * 0.014 * s, base - 0.05 * s), (x + fd * 0.03 * s, base - 0.05 * s), (x + fd * 0.065 * s, base - 0.022 * s),
           (x + fd * 0.085 * s, base - 0.012 * s), (x + fd * 0.085 * s, base), (x - fd * 0.016 * s, base)]
    E.shape(pts, smooth=False, hatches=[(80, 1.9, 0.85), (-40, 2.2, 0.6)], sw=1.3)


def figure(E, kind, x, base, h, view="side", facing=1, pose="stand", lean=None, look=None, tilt=0, hands=None,
           garment=None, hair=None, hat=None, cloth=PAPER_FILL, wash_op=0.4, mouth=0.0, stride=0.05):
    """Draw one person and return a dict of joints for attaching props.

    kind    child | youth | adult | elder: sets proportions, default garment, hair and stoop.
    x, base centre x and ground line; with pose "torso" base is the hip line and no legs are drawn
            (for people behind a table or in a bed).
    h       standing height in pixels (an elder's stoop makes the figure look shorter).
    view    side (facing -1 left or +1 right), front, or back. Front and back are standing or torso.
    pose    stand | sit (side view, seat height equals shin length) | torso.
    hands   {"near": (x, y), "far": (x, y)} in side view, {"left": .., "right": ..} (screen sides) in
            front and back view. Each arm is placed by two-bone IK from the shoulder, so it has a
            visible shoulder, elbow, wrist and hand, and stops at full reach if the target is too far.
            A third value (x, y, bend) with bend +1 or -1 flips which way the elbow points; raised
            arms usually need the opposite sign to hanging ones.
    garment smock | coat | dress | long | vest; hair dark | bun | white | None; hat as head() in pess_awakening.
    wash_op the tone of the garment (0 to 0.7): hatch density, with the cross-hatch on the shadow side.
            cloth is accepted for compatibility; garments are always paper.
    Returns {"head": (x, y, r), "shoulder": (x, y), "hip": (x, y), "hands": {key: (x, y)}, "feet": (x, y)}.
    """
    t0 = min(wash_op, 0.7)                  # limbs; Plate.shape applies CONTRAST to these
    t = min(wash_op * _boost(), 0.85)       # garment: CONTRAST applied here
    c = _KIND[kind]
    g = garment or c["garment"]
    fd = facing
    r, T, leg = c["r"] * h, c["torso"] * h, c["leg"] * h
    lean = c["lean"] if lean is None else lean
    hair = c["hair"] if hair is None else (hair or None)
    if view != "side":
        lean = 0.0
    seated = pose == "sit"
    hip = (x, base - c["shin"] * h) if seated else (x, base - leg) if pose == "stand" else (x, base)
    lw = 0.052 * h * c["build"]
    aw = max(5.0, 0.034 * h * c["build"])
    out = {"hands": {}}

    if view == "side":
        sh = (hip[0] + fd * T * math.sin(lean), hip[1] - T * math.cos(lean))
        hf = lean + c["headfwd"] + 0.05
        dist = r + 0.03 * h
        hc = (sh[0] + fd * math.sin(hf) * dist, sh[1] - math.cos(hf) * dist)
        sh_far = (sh[0] - fd * 0.014 * h, sh[1])
        keys = ("far", "near")
        shoulders = {"far": sh_far, "near": sh}
        bends = {"far": fd, "near": fd}
    else:
        sh = (hip[0], hip[1] - T)
        hc = (sh[0], sh[1] - r - 0.03 * h)
        sw = 0.058 * h * c["build"]
        keys = ("left", "right")
        shoulders = {"left": (sh[0] - sw, sh[1] + 0.015 * h), "right": (sh[0] + sw, sh[1] + 0.015 * h)}
        bends = {"left": 1, "right": -1}
    out.update(head=(hc[0], hc[1], r), shoulder=sh, hip=hip, feet=(x, base))

    default = {}
    for k in keys:
        s = shoulders[k]
        if view == "side" and seated or pose == "torso" and view == "side":
            default[k] = (hip[0] + fd * (0.19 if k == "near" else 0.2) * h, hip[1] - 0.03 * h)
        else:
            default[k] = (s[0] + (0.0 if view == "side" else (-1 if k == "left" else 1) * 0.02 * h), s[1] + 0.34 * h)
    tgt = dict(default)
    if hands:
        tgt.update({k: v for k, v in hands.items() if v is not None})
    l1, l2 = c["upper"] * h, c["fore"] * h

    def arm(k):
        v = tgt[k]
        bend = v[2] if len(v) > 2 else bends[k]
        out["hands"][k] = _arm(E, shoulders[k], v[:2], l1, l2, bend, aw, t0 * 0.8)

    if view == "side":
        arm("far")

    # legs and shoes
    if pose in ("stand", "sit"):
        if view == "side" and pose == "stand":
            for k, sgn in (("far", -1), ("near", 1)):
                ax = x + fd * sgn * stride * h
                kn = ((hip[0] + ax) / 2 + fd * 0.02 * h, (hip[1] + base) / 2)
                lt = 0.34 if k == "far" else 0.12
                E.limb([(hip[0] + fd * sgn * 0.01 * h, hip[1]), kn], lw, tone=lt)
                E.limb([kn, (ax, base - 0.03 * h)], lw * 0.82, tone=lt)
                _shoe(E, ax, base, fd, h)
        elif view == "side":
            for k, off in (("far", 0.035), ("near", 0.0)):
                kx = hip[0] + fd * (c["thigh"] * h + off * h)
                ky = hip[1] - 0.005 * h
                lt = 0.34 if k == "far" else 0.12
                E.limb([(hip[0], hip[1]), (kx, ky)], lw * 1.05, tone=lt)
                E.limb([(kx, ky), (kx - fd * 0.01 * h, base - 0.03 * h)], lw * 0.82, tone=lt)
                _shoe(E, kx - fd * 0.012 * h, base, fd, h)
        else:
            for sg in (-1, 1):
                ax = x + sg * 0.05 * h
                E.limb([(x + sg * 0.03 * h, hip[1]), (ax, base - 0.03 * h)], lw * 0.82, tone=0.15)
                _shoe(E, ax - sg * 0.01 * h, base, sg, h, 0.9)

    # neck, then garment
    E.limb([(sh[0], sh[1] + 0.01 * h), hc], max(5.0, r * 0.62), tone=0.25)
    outline, hem = _outline(c, g, view, h, T, lean, fd, hip, seated or pose == "torso")
    xs = [p[0] for p in outline]
    ys = [p[1] for p in outline]
    shade = (min(xs), min(ys), (min(xs) + max(xs)) / 2, max(ys)) if (view == "side" and fd == 1) or view == "back" else \
            ((min(xs) + max(xs)) / 2, min(ys), max(xs), max(ys))
    shade_left = shade[0] == min(xs)
    gh = [(70, 3.6 - 1.6 * t0, 0.4 + 0.35 * t0), (-48, 3.8 - 1.2 * t0, 0.3 + 0.4 * t0, shade)]
    if t0 > 0.55:
        gh.append((18, 3.4, 0.3 + 0.2 * t0, shade))
    E.shape(outline, smooth=False, hatches=gh, sw=1.9)
    # the shadow side of the garment: a graded slate tint, strongest at the far edge; the lit side stays paper
    fade(E, min(xs), min(ys), max(xs), max(ys), op=0.18 + 0.5 * t, side="l" if shade_left else "r", reach=0.95, clip=outline)
    if hem:
        (fx, fy), (bx, by) = hem
        for u in (0.3, 0.55, 0.8):
            E.line([(hip[0] + (u - 0.5) * 0.13 * h, hip[1] + 0.09 * h), ((bx + (fx - bx) * u + hip[0] + (u - 0.5) * 0.13 * h) / 2, (fy + hip[1]) / 2),
                    (bx + (fx - bx) * u, fy - 5)], w=0.9, op=0.45)
    if seated and g in ("dress", "smock", "long"):
        kx = hip[0] + fd * c["thigh"] * h
        drape = [(hip[0] - fd * 0.09 * h, hip[1] - 0.03 * h), (kx, hip[1] - 0.06 * h), (kx + fd * 0.05 * h, hip[1] + 0.0),
                 (kx + fd * 0.05 * h, base - 0.08 * h), (kx - fd * 0.05 * h, base - 0.07 * h), (kx - fd * 0.06 * h, hip[1] + 0.07 * h),
                 (hip[0] - fd * 0.05 * h, hip[1] + 0.07 * h)]
        E.shape(drape, hatches=[(80, 3.2, 0.3 + 0.3 * t), (-40, 3.8, 0.2 + 0.3 * t)], sw=1.8)
    _head(E, c, hc[0], hc[1], r, view, fd, (look if look is not None else fd * 0.85) if view == "side" else (look or 0.0),
          mouth, tilt, hat, hair)
    if view == "side":
        arm("near")
    else:
        arm("left")
        arm("right")
    return out


def child(E, x, base, h=300, **kw):
    """A child of about seven: large head, short smock, bare knees, dark hair. h is the standing
    height; pass pose="sit" for the seated child. Same arguments and return value as figure()."""
    return figure(E, "child", x, base, h, **kw)


def youth(E, x, base, h=470, **kw):
    """A young person of about twenty: slim, upright, a travelling coat to the knee, dark hair and
    a straight back that leans forward into the day. Same arguments as figure()."""
    return figure(E, "youth", x, base, h, **kw)


def adult(E, x, base, h=500, **kw):
    """A person in the forties: full height, sensible long dress, hair pinned in a bun, a slight
    forward stoop of the busy. Same arguments as figure()."""
    return figure(E, "adult", x, base, h, **kw)


def elder(E, x, base, h=480, **kw):
    """An old person: long robe or coat, white hair, head and trunk bowed forward (lean 0.3). Same
    arguments as figure(); props such as a stick or shawl are drawn by the scene."""
    return figure(E, "elder", x, base, h, **kw)


# ------------------------------------------------------------------ plate helpers

def _pip(n, tag, rng):
    E = Plate(rng, tag)
    E.add(pess_pip_open("isolation", n))
    return E


def _court(age, tag, rng):
    E = Plate(rng, tag)
    E.add(pess_court_open("isolation", age))
    return E


def _end(E, close, vig=True, top=VY0, **kw):
    """Close the plate: a radial slate fall-off over the scene (clear in the middle), then the plate."""
    if vig:
        vignette(E, top=top, **kw)
    return svg(E.done() + close, PESS_PAPER)


def grass(E, y0, y1, n=420):
    """Ground texture: short etched grass strokes between y0 and y1."""
    E.strokes(IX0, y0, IX1, y1, n, 5, 16, w=0.8, lean=6)


def flame(E, fx, fy, fs, sw=1.2):
    E.add(f'<path d="M{f(fx)},{f(fy - 24 * fs)} C{f(fx + 8 * fs)},{f(fy - 8 * fs)} {f(fx + 6 * fs)},{f(fy)} {f(fx)},{f(fy)} '
          f'C{f(fx - 6 * fs)},{f(fy)} {f(fx - 8 * fs)},{f(fy - 8 * fs)} {f(fx)},{f(fy - 24 * fs)} Z" fill="{PAPER_FILL}" stroke="{INK}" stroke-width="{sw}"/>')


# ------------------------------------------------------------------ pips

def is01(rng):
    """One: a woman at a kitchen table lays a lid on a jar holding an antlered shadow."""
    E = _pip(1, "a", rng)
    FL = 1010
    wall(E, 340, FL, op=0.16)
    window(E, 350, 400, 570, 690, tone=0.7, panes=(2, 2))
    # shelf with pots on the wall, left
    rect(E, 90, 560, 320, 572, hatches=[(0, 3, 0.4)], sw=1.8)
    for px, pr in ((135, 34), (205, 28), (268, 32)):
        E.shape(ellipse_pts(px, 560 - pr, pr, pr * 0.95, 16), hatches=[(60, 3, 0.45, (px, 560 - 2 * pr, px + pr, 560))], sw=1.8)
        rect(E, px - pr * 0.6, 560 - pr * 2 - 6, px + pr * 0.6, 560 - pr * 2 + 6, hatches=[(0, 2, 0.5)], sw=1.5)
    fade(E, IX0, 340, 350, FL, op=0.6, side="l", reach=1.0)
    fade(E, 70, 340, IX1, 470, op=0.45, side="t", reach=1.0)
    floor_band(E, FL, 0.16)
    chair_side(E, 160, FL, seat=125, f_dir=1, back_h=210, w=110)
    top = 810
    cup(E, 350, 770, 1.3, tilt=-8)
    j = adult(E, 215, FL, 500, pose="sit", facing=1, lean=0.2, wash_op=0.7,
              hands={"near": (326, 744), "far": (418, top - 150 - 14)})
    # the table (drawn after the figure so the forearm and lap pass behind it)
    cast(E, [(292, top + 24), (596, top + 24), (604, FL - 2), (286, FL - 2)], 0.6)
    floor_shadow(E, 230, FL - 2, 150, 12, 0.6)
    table_front(E, 285, 595, top, FL, thick=18, legs=(0.08, 0.92))
    jar(E, 440, top, 104, 150)
    # the antlered shadow pressing the glass: a soft hatched shape, no silhouette fill
    sx, sy = 425, top - 56
    mass(E, [(sx - 18, sy + 32), (sx - 20, sy - 6), (sx - 8, sy - 24), (sx + 10, sy - 26), (sx + 24, sy - 8), (sx + 20, sy + 32)],
         solid=0.4, smooth=True, sw=1.3)
    for sg in (-1, 1):
        ax = sx + sg * 6
        E.line([(ax, sy - 22), (ax + sg * 14, sy - 50), (ax + sg * 8, sy - 74)], w=2.2, smooth=False)
        E.line([(ax + sg * 12, sy - 46), (ax + sg * 28, sy - 58)], w=1.8, smooth=False)
        E.line([(ax + sg * 10, sy - 62), (ax + sg * 24, sy - 78)], w=1.6, smooth=False)
    E.add(f'<circle cx="{f(sx + 12)}" cy="{f(sy - 8)}" r="2.4" fill="{PAPER_FILL}"/>')
    # lid held above the jar by the far hand, and the cup in the near hand
    hx, hy = j["hands"]["far"]
    E.shape(ellipse_pts(hx + 6, hy + 10, 56, 11, 16), hatches=[(0, 2.4, 0.5)], sw=1.8)
    return _end(E, pess_pip_close())


def lantern(E, x, y, s=1.0):
    """A paper lantern hanging from (x, y) with ribs, caps and a tassel; a small bone glow behind."""
    glow(E, x, y + 46 * s, 62 * s, 62 * s, 0.3)
    E.line([(x, y), (x, y + 10 * s)], w=1.5, smooth=False)
    rect(E, x - 12 * s, y + 8 * s, x + 12 * s, y + 18 * s, hatches=[(0, 2, 0.6)], sw=1.4)
    E.shape(ellipse_pts(x, y + 52 * s, 34 * s, 36 * s, 18), hatches=[(90, 5, 0.25)], sw=1.8)
    for k in (-0.55, 0, 0.55):
        E.line([(x, y + 18 * s), (x + k * 34 * s * 1.5, y + 52 * s), (x, y + 88 * s)], w=0.9, op=0.7)
    rect(E, x - 12 * s, y + 86 * s, x + 12 * s, y + 94 * s, hatches=[(0, 2, 0.6)], sw=1.4)
    E.line([(x, y + 94 * s), (x, y + 112 * s)], w=1.4, smooth=False)
    E.line([(x - 5 * s, y + 112 * s), (x + 5 * s, y + 112 * s)], w=3, smooth=False)


def wine_glass(E, x, y, s=1.0, fill=0.0):
    """A wine glass standing on (x, y); returns the centre of the bowl."""
    bowl = [(x - 24 * s, y - 100 * s), (x + 24 * s, y - 100 * s), (x + 22 * s, y - 66 * s), (x + 8 * s, y - 50 * s),
            (x - 8 * s, y - 50 * s), (x - 22 * s, y - 66 * s)]
    E.shape(bowl, tone=0.08, sw=1.8)
    if fill:
        E.shape([(x - 23 * s, y - 100 * s + fill * 60 * s), (x + 23 * s, y - 100 * s + fill * 60 * s), (x + 22 * s, y - 66 * s),
                 (x + 8 * s, y - 50 * s), (x - 8 * s, y - 50 * s), (x - 22 * s, y - 66 * s)], smooth=False,
                hatches=[(0, 2.6, 0.5)], outline=False)
    E.line([(x, y - 50 * s), (x, y - 6 * s)], w=2.4, smooth=False)
    E.line([(x - 18 * s, y - 4 * s), (x + 18 * s, y - 4 * s)], w=2.4, smooth=False)
    return x, y - 76 * s


def hold_glass(E, hand, s=0.6, fill=0.5):
    """A wine glass held by the hand at `hand` (stem in the fist); redraws the hand over the stem."""
    wine_glass(E, hand[0], hand[1] + 8 * s * 2, s, fill=fill)
    hand_dot(E, hand, 7)


def candle(E, x, y, hgt, flame_=1.0):
    """A candle in a holder with base at (x, y); the flame scales from 0 (out) to 1."""
    rect(E, x - 8, y - hgt, x + 8, y - 10, hatches=[(80, 3, 0.35)], sw=1.5)
    rect(E, x - 16, y - 10, x + 16, y, hatches=[(0, 2, 0.6)], sw=1.5)
    if flame_ > 0:
        flame(E, x, y - hgt - 6, flame_, 1.3)


def newspaper(E, x, y, w, h, rot=0, cols=3, cover=0.15):
    """A folded newspaper sheet lying flat (a rectangle with column rules, no text) centred at (x, y)."""
    E.add(f'<g transform="rotate({rot} {f(x)} {f(y)})">')
    rect(E, x - w / 2, y - h / 2, x + w / 2, y + h / 2, tone=cover, sw=1.5)
    for k in range(1, cols):
        xx = x - w / 2 + w * k / cols
        E.line([(xx, y - h / 2 + 5), (xx, y + h / 2 - 5)], w=0.7, op=0.6, smooth=False)
    E.line([(x - w / 2 + 6, y - h / 2 + 8), (x + w / 2 - 6, y - h / 2 + 8)], w=2.0, smooth=False, op=0.7)
    E.add("</g>")


def is02(rng):
    """Two: a banquet under lanterns; one diner looks into his glass where the flames shrink."""
    E = _pip(2, "b", rng)
    wall(E, 340, 900, op=0.14)
    fade(E, IX0, 340, IX1, 600, op=0.6, side="t", reach=1.0)
    fade(E, IX0, 340, 240, 900, op=0.5, side="l", reach=1.0)
    fade(E, 440, 340, IX1, 900, op=0.55, side="r", reach=1.0)
    # string of lanterns, sagging across the room
    E.line([(IX0, 372), (200, 408), (340, 422), (480, 408), (IX1, 372)], w=1.4)
    for lx, ly in ((150, 402), (280, 418), (410, 418), (540, 402)):
        lantern(E, lx, ly, 0.85)
    TOP = 790
    # servant behind the end diner, leaning in over the dessert
    sv = youth(E, 553, 986, 535, pose="stand", facing=-1, lean=0.22, wash_op=0.8,
               hair="dark", garment="coat", hands={"near": (498, TOP - 36), "far": (462, TOP - 52)})
    # guests, in profile
    g1 = adult(E, 100, 880, 500, pose="torso", facing=1, garment="coat", hair="dark", mouth=0.9, look=0.9, tilt=-8,
               wash_op=0.75, hands={"near": (196, 640), "far": (160, TOP - 20)})
    g2 = adult(E, 272, 880, 500, pose="torso", facing=-1, mouth=0.8, tilt=6, wash_op=0.3,
               hands={"near": (210, 716), "far": (322, TOP - 20)})
    g3 = elder(E, 442, 862, 500, pose="torso", facing=-1, lean=0.3, tilt=-22, hair="dark", garment="coat",
               wash_op=0.8, hands={"near": (385, TOP - 30), "far": (480, TOP - 20)})
    # table: top surface in slight perspective, hanging cloth
    E.shape([(78, TOP - 8), (602, TOP - 8), (614, TOP + 14), (66, TOP + 14)], smooth=False, hatches=[(0, 5, 0.25)], sw=1.8)
    E.shape([(66, TOP + 14), (614, TOP + 14), (622, 1004), (58, 1004)], smooth=False, hatches=[(90, 6, 0.4)], tone=0.12, sw=1.8)
    fade(E, 66, TOP + 14, 622, 1004, op=0.7, side="b", reach=1.0)
    for k in range(1, 18):
        xx = 66 + 548 * k / 18
        E.line([(xx, TOP + 18), (xx + (3 if k % 2 else -3), 1000)], w=0.8, op=0.5, smooth=False)
    hold_glass(E, g1["hands"]["near"], 0.62)
    # things on the table
    for px in (130, 240):
        E.shape(ellipse_pts(px, TOP + 2, 52, 9, 18), hatches=[(0, 2.6, 0.4)], sw=1.5)
    candle(E, 305, TOP + 8, 60, 0.35)
    bx, by = wine_glass(E, 360, TOP + 12, 0.95, fill=0.5)
    for k, fs in enumerate((1.15, 0.75, 0.42)):
        flame(E, bx - 15 + k * 15, by + 6, fs)
    # dessert under a cloth held by the servant
    E.shape(ellipse_pts(480, TOP + 4, 46, 9, 16), hatches=[(0, 3, 0.4)], sw=1.6)
    E.shape([(436, TOP - 2), (440, TOP - 40), (462, TOP - 62), (498, TOP - 62), (520, TOP - 40), (524, TOP - 2)],
            hatches=[(60, 3, 0.4)], sw=1.8)
    hx, hy = sv["hands"]["near"]
    gx, gy = sv["hands"]["far"]
    cloth_pts = [(gx - 6, gy - 10), (hx + 10, hy - 14), (hx + 28, hy + 16), (hx + 6, TOP - 20), (gx - 18, TOP - 18), (gx - 22, gy + 8)]
    E.shape(cloth_pts, hatches=[(80, 5, 0.35)], sw=1.6)
    for hnd in (sv["hands"]["near"], sv["hands"]["far"]):
        hand_dot(E, hnd, 7)
    return _end(E, pess_pip_close())


def is03(rng):
    """Three: mourners at a graveside watch the priest's raised hand; a child is turned to the road."""
    E = _pip(3, "c", rng)
    P = Pen("p3", rng)
    HOR = 610
    LINE = 930   # the line the standing figures' feet are on
    sky(E, 340, HOR, strongest=0.4, weakest=0.05, gap=6, tint=0.8)
    E.line([(IX0, HOR), (IX1, HOR)], w=1.2, smooth=False, op=0.8)
    # ground: fine horizontal lines, wider toward the viewer
    yy, gap, d = HOR + 6, 4.0, []
    while yy < IY1 + 10:
        d.append(f"M{IX0},{f(yy)} L{IX1},{f(yy + rng.uniform(-1, 1))}")
        yy += gap
        gap *= 1.04
    E.add(f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width="0.6" opacity="0.4" fill="none"/>')
    fade(E, IX0, HOR, IX1, IY1, op=0.6, side="b", reach=1.0)
    fade(E, 330, HOR, IX1, IY1, op=0.35, side="r", reach=1.0)
    for sx_ in (215, 350, 445, 535):
        floor_shadow(E, sx_ + 6, LINE + 2, 56, 9, 0.7)
    # road running from the left foreground to the horizon
    E.shape([(150, HOR), (172, HOR), (225, 1100), (70, 1100), (70, 900)], smooth=False, hatches=[(20, 6, 0.2)], sw=1.4)
    for tx, th in ((235, 150), (330, 120), (560, 130)):
        P.bare_tree(tx, HOR + 4, th, op=0.7)
    E.add(P.done())
    for sx, sy, sh in ((250, 720, 70), (330, 700, 56), (440, 690, 50), (560, 700, 56)):
        E.shape([(sx - 18, sy), (sx - 18, sy - sh * 0.7), (sx, sy - sh), (sx + 18, sy - sh * 0.7), (sx + 18, sy)],
                hatches=[(60, 3, 0.4, (sx, sy - sh, sx + 18, sy))], sw=1.6)
    # back row of mourners, small
    for mx in (395, 485, 575):
        adult(E, mx, 880, 235, view="back", garment="coat", hat="top", wash_op=0.75)
    # priest, hand raised to the sky
    elder(E, 215, LINE, 400, facing=1, lean=0.1, garment="long", wash_op=0.8, look=0.9, tilt=-22,
          hands={"near": (305, 590), "far": (255, 800)})
    # front row of mourners, faces turned up to the hand
    for mx, kd, ht, ln in ((350, "adult", "top", 0.05), (445, "elder", "top", 0.2), (535, "adult", "bonnet", 0.05)):
        fn = {"elder": elder, "adult": adult}[kd]
        fn(E, mx, LINE, 330, facing=-1, garment="long", hair="dark", hat=ht, look=-0.9, tilt=18, wash_op=0.8, lean=ln)
    # grave in the foreground: spoil heap and open pit, the pit shaded by dense hatching
    E.shape([(188, 1050), (215, 1005), (260, 988), (310, 1005), (330, 1050)], hatches=[(40, 3, 0.5), (-30, 4, 0.4)], tone=0.4, sw=1.8)
    E.shape([(305, 975), (545, 975), (585, 1066), (270, 1066)], smooth=False, hatches=[(20, 5, 0.2)], sw=2)
    mass(E, [(322, 988), (532, 988), (562, 1050), (294, 1050)], solid=0.55, wash=0.35, sw=1.8)
    # child at the left edge, back turned, facing the road
    child(E, 112, 1030, 250, view="back", garment="coat", wash_op=0.8, hands={"left": (92, 960), "right": (132, 960)})
    return _end(E, pess_pip_close())


def scissors(E, x, y, ang=0, ln=44):
    """A pair of scissors, open a little, pivot at (x, y); the blades point along ang (degrees)."""
    E.add(f'<g transform="rotate({ang} {f(x)} {f(y)})">')
    for sg in (-1, 1):
        E.line([(x, y), (x + ln, y + sg * 7)], w=3.0, smooth=False)
        E.line([(x, y), (x - ln * 0.5, y - sg * 9)], w=2.4, smooth=False)
        E.shape(ellipse_pts(x - ln * 0.5 - 8, y - sg * 12, 10, 7, 12), fill=None, sw=2.2)
    E.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="2.8" fill="{INK}"/></g>')


def stack_of_papers(E, x0, x1, base, n, rng, thick=16):
    """A pile of folded newspapers: n slabs, each a little out of true, with page edges."""
    y = base
    for k in range(n):
        dx = rng.uniform(-5, 5)
        rect(E, x0 + dx, y - thick, x1 + dx, y, hatches=[(0, 3.6, 0.12 + 0.08 * (k % 3))], sw=1.4)
        E.line([(x0 + dx + 4, y - thick / 2), (x1 + dx - 4, y - thick / 2)], w=0.7, op=0.6, smooth=False)
        y -= thick


def is04(rng):
    """Four: a man among newspapers cuts columns; the doorway shows a railway cutting to a smoking horizon."""
    E = _pip(4, "d", rng)
    FL = 1010
    wall(E, 340, FL, op=0.14)
    fade(E, IX0, 340, 340, FL, op=0.55, side="l", reach=1.0)
    fade(E, IX0, 340, IX1, 480, op=0.4, side="t", reach=1.0)
    # pinboard with neat rows of clippings
    rect(E, 88, 380, 322, 560, hatches=[(45, 5, 0.22)], sw=2.2)
    for r_ in range(3):
        for c_ in range(5):
            cx_, cy_ = 118 + c_ * 46, 410 + r_ * 54
            rect(E, cx_ - 15, cy_ - 20, cx_ + 15, cy_ + 20, sw=1.2)
            for k in range(1, 4):
                E.line([(cx_ - 10, cy_ - 20 + k * 9), (cx_ + 10, cy_ - 20 + k * 9)], w=0.7, op=0.55, smooth=False)
            E.add(f'<circle cx="{f(cx_)}" cy="{f(cy_ - 17)}" r="2.4" fill="{INK}"/>')
    # doorway to the railway cutting
    ox0, oy0, ox1 = 410, 390, 592
    rect(E, ox0 - 12, oy0 - 12, ox1 + 12, FL, sw=2)
    VP = (500, 730)
    clip_open(E, ox0, oy0, ox1, FL)
    E.add(f'<rect x="{ox0}" y="{oy0}" width="{ox1 - ox0}" height="{FL - oy0}" fill="{PAPER_FILL}"/>')
    sky(E, oy0, VP[1], strongest=0.45, weakest=0.06, gap=5, x0=ox0, x1=ox1, tint=0.8)
    E.shape([(ox0 - 4, FL + 4), (ox0 - 4, VP[1] + 40), (VP[0] - 4, VP[1]), (VP[0] - 70, FL + 4)], smooth=False,
            hatches=[(70, 3.2, 0.5), (-50, 3.6, 0.35)], sw=1.4)
    E.shape([(ox1 + 4, FL + 4), (ox1 + 4, VP[1] + 40), (VP[0] + 4, VP[1]), (VP[0] + 70, FL + 4)], smooth=False,
            hatches=[(110, 3.2, 0.5), (50, 3.6, 0.35)], sw=1.4)
    hs = [f"M{ox0 + k * 14},{FL} L{VP[0] + k * 1.2},{VP[1]}" for k in range(-9, 10)]
    E.add(f'<path d="{" ".join(hs)}" stroke="{INK}" stroke-width="0.6" opacity="0.3" fill="none"/>')
    E.line([(VP[0] - 28, FL), (VP[0] - 2, VP[1])], w=2.2, smooth=False)
    E.line([(VP[0] + 28, FL), (VP[0] + 2, VP[1])], w=2.2, smooth=False)
    for k in range(10):
        t = (k / 10) ** 1.6
        yy = FL - (FL - VP[1]) * t
        wd = 28 * (1 - t) + 2
        E.line([(VP[0] - wd - 6 * (1 - t), yy), (VP[0] + wd + 6 * (1 - t), yy)], w=2.2 * (1 - t) + 0.6, smooth=False)
    # smoke plume on the horizon: thin hatched puffs over a faint wash
    for k in range(9):
        t = k / 8
        cx_ = VP[0] + 14 + t * 60 + math.sin(t * 5) * 8
        cy_ = VP[1] - 8 - t * 230
        rr = 16 + t * 34
        E.add(f'<ellipse cx="{f(cx_)}" cy="{f(cy_)}" rx="{f(rr * 1.2)}" ry="{f(rr)}" fill="{SLATE}" opacity="{0.16 - 0.08 * t:.2f}" filter="url(#wash)"/>')
        E.shape(ellipse_pts(cx_, cy_, rr * 1.1, rr * 0.9, 12), fill=None, hatches=[(20, 3.2, 0.35)], sw=0.9, outline=False)
    E.add(f'<path d="M{VP[0] - 3},{VP[1]} l0,-12 l8,0 l0,12" fill="{INK}"/>')
    clip_close(E)
    E.add(f'<rect x="{ox0}" y="{oy0}" width="{ox1 - ox0}" height="{FL - oy0}" fill="none" stroke="{INK}" stroke-width="2"/>')
    # open door leaf, in perspective
    mass(E, [(ox0, oy0), (ox0 + 38, oy0 + 16), (ox0 + 38, FL - 24), (ox0, FL)], solid=0.55, sw=2)
    # stacks of newspapers
    stack_of_papers(E, 345, 396, FL, 13, rng, 17)
    stack_of_papers(E, 84, 160, FL, 9, rng, 17)
    stack_of_papers(E, 96, 150, FL - 9 * 17, 3, rng, 17)
    floor_band(E, FL, 0.14)
    fade(E, 345, FL - 13 * 17, 396, FL, op=0.6, side="l", reach=1.0)
    fade(E, 84, FL - 9 * 17, 160, FL, op=0.6, side="l", reach=1.0)
    floor_shadow(E, 300, FL - 2, 130, 12, 0.6)
    # stool and basket of cuttings
    rect(E, 108, 862, 172, 874, hatches=[(2, 3, 0.4)], sw=1.8)
    for lx in (116, 164):
        rect(E, lx - 3, 874, lx + 3, FL, sw=1.4)
    mass(E, [(100, 800), (180, 800), (170, 860), (110, 860)], solid=0.45, sw=2)
    for k in range(7):
        sx_ = 108 + k * 10
        E.line([(sx_, 800), (sx_ + rng.uniform(-10, 10), 786 - rng.uniform(0, 10))], w=2.2, smooth=False)
    chair_side(E, 300, FL, seat=125, f_dir=-1, back_h=200, w=96)
    m = adult(E, 292, FL, 480, pose="sit", facing=-1, lean=0.22, tilt=-14, garment="vest", hair="dark",
              wash_op=0.8, hands={"near": (160, 772), "far": (192, 748)})
    hx, hy = m["hands"]["far"]
    E.shape([(hx - 6, hy - 40), (hx - 52, hy - 34), (hx - 46, hy + 52), (hx + 6, hy + 40)], smooth=False, sw=1.6)
    for k in range(1, 4):
        xx = hx - 6 - 13 * k
        E.line([(xx, hy - 30), (xx - 1, hy + 40)], w=0.7, op=0.5, smooth=False)
    hand_dot(E, (hx, hy), 7, math.pi)
    nx, ny = m["hands"]["near"]
    scissors(E, nx - 14, ny + 2, ang=172)
    hand_dot(E, (nx, ny), 7, math.pi)
    return _end(E, pess_pip_close())


def hourglass_lying(E, x, y, s=1.0):
    """An hourglass laid on its side on a shelf: caps at both ends, two cone bulbs, a little sand."""
    for sg in (-1, 1):
        E.shape([(x + sg * 38 * s, y - 28 * s), (x + sg * 4 * s, y - 18 * s), (x + sg * 4 * s, y - 10 * s), (x + sg * 38 * s, y)],
                smooth=False, sw=1.6)
        rect(E, x + sg * 42 * s - 4, y - 32 * s, x + sg * 42 * s + 4, y + 3 * s, hatches=[(0, 2, 0.6)], sw=1.4)
    E.shape([(x - 36 * s, y - 2 * s), (x - 12 * s, y - 2 * s), (x - 4 * s, y - 10 * s), (x - 36 * s, y - 10 * s)],
            smooth=False, fill=BONE, outline=False)


def margin_skull(E, cx, cy, s=1.0):
    """A skull inked in a ledger margin, large enough to read at card size, half scratched out."""
    E.shape(ellipse_pts(cx, cy, 27 * s, 27 * s, 16), hatches=[(60, 3, 0.4, (cx, cy - 27 * s, cx + 27 * s, cy + 27 * s))], sw=1.8)
    E.shape([(cx - 14 * s, cy + 18 * s), (cx + 14 * s, cy + 18 * s), (cx + 12 * s, cy + 36 * s), (cx - 12 * s, cy + 36 * s)],
            smooth=False, sw=1.6)
    for k in range(-1, 2):
        E.line([(cx + k * 6 * s, cy + 25 * s), (cx + k * 6 * s, cy + 36 * s)], w=1.0, smooth=False)
    for sg in (-1, 1):
        E.shape(ellipse_pts(cx + sg * 10 * s, cy - 2 * s, 7 * s, 8 * s, 10), hatches=[(60, 1.8, 0.9), (-40, 2, 0.8)], sw=1.3)
    E.shape([(cx, cy + 8 * s), (cx - 4 * s, cy + 16 * s), (cx + 4 * s, cy + 16 * s)], smooth=False, hatches=[(60, 1.8, 0.9)], sw=1.0)
    for k in range(7):  # scratching out, over the lower half
        E.line([(cx - 28 * s + k * 5, cy + 36 * s), (cx - 2 * s + k * 5, cy - 14 * s)], w=1.7, op=0.85, smooth=False)


def is05(rng):
    """Five: a clerk writes steadily in a ledger; a skull inked in the margin is half scratched out."""
    E = _pip(5, "e", rng)
    FL = 1010
    wall(E, 340, FL, op=0.14)
    fade(E, 300, 340, IX1, FL, op=0.6, side="r", reach=1.0)
    fade(E, IX0, 340, IX1, 470, op=0.4, side="t", reach=1.0)
    window(E, 96, 420, 232, 700, tone=0.55, panes=(1, 2))
    # shelf of hourglasses laid on their sides
    rect(E, 300, 520, 598, 534, hatches=[(0, 3, 0.4)], sw=1.8)
    for bx in (350, 440, 530):
        hourglass_lying(E, bx, 520, 0.95)
    for bx in (320, 580):
        E.line([(bx, 534), (bx, 566)], w=3, smooth=False)
    floor_band(E, FL, 0.14)
    # high desk: body, sloping top seen from above, drawers
    mass(E, [(262, 742), (592, 742), (592, FL), (262, FL)], solid=0.4, sw=2)
    for dx in (280, 440):
        rect(E, dx, 780, dx + 140, 860, sw=1.6)
        E.shape(ellipse_pts(dx + 70, 820, 6, 6, 8), fill=INK, outline=False)
    E.shape([(300, 596), (592, 596), (592, 742), (262, 742)], smooth=False, hatches=[(10, 5, 0.25)], sw=2)
    # open ledger, large enough for the skull
    lp = [(284, 616), (428, 614), (424, 730), (276, 734)]
    rp = [(428, 614), (572, 616), (576, 734), (424, 730)]
    E.shape(lp, smooth=False, sw=1.6)
    E.shape(rp, smooth=False, sw=1.6)
    for k in range(1, 8):
        t = k / 8
        E.line([(284 - 8 * t + 8, 616 + 116 * t), (424, 614 + 114 * t)], w=0.6, op=0.4, smooth=False)
        E.line([(428, 614 + 114 * t), (572 + 4 * t, 616 + 116 * t)], w=0.6, op=0.4, smooth=False)
    E.line([(526, 618), (530, 732)], w=0.9, op=0.7, smooth=False)
    margin_skull(E, 534, 668, 1.25)
    cl = adult(E, 212, FL, 520, facing=1, lean=0.3, tilt=14, garment="coat", hair="dark", wash_op=0.8,
               hands={"near": (330, 706), "far": (292, 736)}, stride=0.03)
    # pen in the writing hand
    px, py = cl["hands"]["near"]
    E.line([(px - 4, py + 4), (px + 26, py - 34)], w=2, smooth=False)
    hand_dot(E, (px, py), 7, -0.6)
    return _end(E, pess_pip_close())


def armchair(E, x, floor, f_dir=1, seat=125):
    """Back part of an armchair for a seated figure: tall back and wing. Draw arm_of_chair() after the figure."""
    sy = floor - seat
    b = x - f_dir * 70
    E.shape([(b - 14, sy - 300), (b + f_dir * 90, sy - 310), (b + f_dir * 96, sy + 10), (b - 14, sy + 10)], smooth=False,
            hatches=[(70, 3.2, 0.4), (-45, 3.8, 0.3)], sw=2)
    E.shape([(b - 14, sy - 300), (b + f_dir * 90, sy - 310), (b + f_dir * 100, sy - 270), (b + f_dir * 10, sy - 262), (b - 14, sy - 268)],
            smooth=False, hatches=[(0, 3, 0.4)], sw=1.8)
    fade(E, b - 14, sy - 310, b + f_dir * 96, sy + 10, op=0.7, side="l" if f_dir == 1 else "r", reach=1.0,
         clip=[(b - 14, sy - 300), (b + f_dir * 90, sy - 310), (b + f_dir * 96, sy + 10), (b - 14, sy + 10)])
    E.shape([(x - 80, sy), (x + 90, sy), (x + 90, sy + 40), (x - 80, sy + 40)], smooth=False, hatches=[(0, 4, 0.35)], sw=2)
    for lx in (x - 70, x + 70):
        rect(E, lx - 6, sy + 40, lx + 6, floor, hatches=[(80, 2.6, 0.5)], sw=1.6)


def arm_of_chair(E, x, floor, f_dir=1, seat=125):
    """The near arm of an armchair, drawn over the seated figure's thigh side."""
    sy = floor - seat
    E.shape([(x - 78, sy - 46), (x + 82, sy - 46), (x + 90, sy - 28), (x + 82, sy + 40), (x - 78, sy + 40)], smooth=False,
            hatches=[(0, 4, 0.35), (60, 5, 0.3)], sw=2)
    E.shape(ellipse_pts(x + 84 * f_dir, sy - 40, 14, 12, 12), hatches=[(40, 3, 0.4)], sw=1.8)


def is06(rng):
    """Six: a man in an armchair at dusk, coat on, watches a clock whose pendulum is behind a curtain."""
    E = _pip(6, "f", rng)
    FL = 1010
    wall(E, 340, FL, op=0.14)
    fade(E, IX0, 340, 330, FL, op=0.6, side="l", reach=1.0)
    window(E, 98, 410, 238, 650, tone=0.75, panes=(1, 2))
    # chimney breast and mantel
    E.shape([(380, 360), (592, 360), (592, 640), (380, 640)], smooth=False, hatches=[(70, 6, 0.22)], sw=1.8)
    rect(E, 358, 640, 612, 668, hatches=[(0, 4, 0.35)], sw=2)
    E.shape([(380, 668), (592, 668), (592, 1010), (380, 1010)], smooth=False, hatches=[(75, 6, 0.26)], sw=1.8)
    fade(E, 380, 360, 592, 1010, op=0.55, side="r", reach=1.0)
    mass(E, [(446, 1010), (446, 820), (478, 796), (526, 796), (558, 820), (558, 1010)], solid=0.65, wash=0.35, sw=2.2)
    E.shape([(446, 1010), (446, 975), (558, 975), (558, 1010)], smooth=False, hatches=[(80, 4, 0.5)], sw=1.8)
    # the clock
    cx_ = 490
    E.shape([(cx_ - 58, 640), (cx_ - 58, 540), (cx_ - 44, 500), (cx_, 476), (cx_ + 44, 500), (cx_ + 58, 540), (cx_ + 58, 640)],
            smooth=False, hatches=[(70, 3, 0.35)], sw=2.2)
    E.shape(ellipse_pts(cx_, 540, 40, 40, 24), sw=2)
    for k in range(12):
        a = k * math.pi / 6
        E.line([(cx_ + 33 * math.sin(a), 540 - 33 * math.cos(a)), (cx_ + 38 * math.sin(a), 540 - 38 * math.cos(a))], w=1.6, smooth=False)
    E.line([(cx_, 540), (cx_ + 6, 512)], w=2.6, smooth=False)
    E.line([(cx_, 540), (cx_ - 20, 548)], w=2.2, smooth=False)
    E.shape(ellipse_pts(cx_, 540, 3, 3, 8), fill=INK, outline=False)
    rect(E, cx_ - 24, 590, cx_ + 24, 636, tone=0.5, sw=1.8)
    curtain(E, cx_ - 24, cx_ + 24, 590, 636, drawn=1.0, op=0.55)
    floor_band(E, FL, 0.14)
    # tea table with a cold tray
    E.shape(ellipse_pts(405, 842, 64, 11, 18), hatches=[(0, 3, 0.4)], sw=2)
    rect(E, 401, 852, 409, 1000, sw=1.6)
    floor_shadow(E, 405, 1004, 70, 9, 0.6)
    E.shape(ellipse_pts(405, 1002, 40, 8, 14), hatches=[(0, 3, 0.4)], sw=1.6)
    E.shape(ellipse_pts(405, 836, 50, 8, 16), hatches=[(0, 2.4, 0.5)], sw=1.5)
    E.shape([(384, 834), (384, 800), (398, 786), (424, 786), (436, 800), (436, 834)], hatches=[(70, 3, 0.4)], sw=1.8)
    E.line([(436, 806), (458, 790), (462, 796)], w=2.4, smooth=False)
    E.line([(384, 806), (370, 806), (370, 822), (384, 824)], w=2.2, smooth=False)
    cup(E, 356, 836, 0.9)
    # the man
    armchair(E, 190, FL, f_dir=1)
    adult(E, 190, FL, 470, pose="sit", facing=1, lean=0.06, tilt=-10, garment="coat", hair="dark", wash_op=0.85,
          hands={"near": (272, 830), "far": (246, 836)})
    arm_of_chair(E, 190, FL, f_dir=1)
    return _end(E, pess_pip_close())


def storm_window(E, rng, x0, y0, x1, y1):
    """A window onto a storm: a sky of dense hatching and rain, a rough sea, a wrecked boat on the shore, and
    a giantess of cloud with her back turned. Draws the frame and sill too."""
    rect(E, x0 - 10, y0 - 10, x1 + 10, y1 + 10, sw=2)
    hz = y0 + (y1 - y0) * 0.62
    clip_open(E, x0, y0, x1, y1)
    E.add(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{PAPER_FILL}"/>')
    sky(E, y0, hz, strongest=0.75, weakest=0.3, gap=3.4, x0=x0, x1=x1, tint=0.9, w=0.7)
    # sea: wave lines
    for k in range(9):
        yy = hz + 6 + k * 14
        d = f"M{x0},{f(yy)} " + " ".join(f"q{f(14 - k * 0.8)},{f(-8 - k * 0.6)} {f(28 - k * 1.6)},0" for _ in range(int((x1 - x0) / 20)))
        E.add(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="0.9" opacity="0.6"/>')
    E.shape([(x0 - 4, hz), (x1 + 4, hz), (x1 + 4, y1 + 4), (x0 - 4, y1 + 4)], smooth=False, fill=None, hatches=[(2, 5, 0.3)], outline=False)
    # giantess: a cloud that has turned away, hair streaming off to the right
    gx, gy = x0 + (x1 - x0) * 0.62, y0 + 110
    body = [(gx, gy + 50, 34), (gx - 36, gy + 56, 26), (gx + 36, gy + 58, 26), (gx - 6, gy + 96, 36), (gx - 40, gy + 110, 28),
            (gx + 34, gy + 108, 30), (gx - 54, gy + 70, 16), (gx + 62, gy + 66, 18), (gx + 86, gy + 62, 12)]
    for cx_, cy_, rr in body:
        E.add(f'<circle cx="{f(cx_)}" cy="{f(cy_)}" r="{f(rr)}" fill="{PAPER_FILL}" stroke="{INK}" stroke-width="1.8"/>')
    for cx_, cy_, rr in body:
        E.add(f'<circle cx="{f(cx_)}" cy="{f(cy_)}" r="{f(rr - 1.1)}" fill="{PAPER_FILL}"/>')
    cd = " ".join(f"M{f(cx_ - rr)},{f(cy_)} a{f(rr)},{f(rr)} 0 1 0 {f(2 * rr)},0 a{f(rr)},{f(rr)} 0 1 0 {f(-2 * rr)},0 Z" for cx_, cy_, rr in body)
    E.hatch_d(cd, (gx - 90, gy, gx + 100, gy + 140), 70, 4.5, 0.32, 0.7, sub=(gx - 90, gy + 60, gx + 100, gy + 140))
    E.shape(ellipse_pts(gx + 4, gy, 25, 25, 16), sw=1.8)
    for k in range(6):
        E.line([(gx + 20, gy - 14 + k * 5), (gx + 56 + k * 6, gy - 22 + k * 8), (gx + 90 + k * 10, gy - 20 + k * 9)], w=1.0, op=0.7)
    # wrecked boat on the shore and broken mast
    bx, by = x1 - 70, y1 - 24
    E.add(f'<g transform="rotate(-14 {f(bx)} {f(by)})">')
    E.shape([(bx - 50, by - 4), (bx - 20, by + 14), (bx + 56, by - 18), (bx + 50, by - 30), (bx - 44, by - 22)],
            hatches=[(0, 2.2, 0.8), (50, 2.6, 0.6)], sw=1.8)
    E.add("</g>")
    E.add(f'<path d="M{f(bx - 6)},{f(by - 24)} L{f(bx + 4)},{f(by - 80)} l10,-8 M{f(bx + 8)},{f(by - 60)} l26,4" fill="none" stroke="{INK}" stroke-width="2.6"/>')
    # rain
    d = []
    for _ in range(80):
        rx, ry = rng.uniform(x0, x1), rng.uniform(y0, y1)
        d.append(f"M{f(rx)},{f(ry)} l{f(-9)},{f(rng.uniform(22, 38))}")
    E.add(f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width="0.8" opacity="0.4"/>')
    clip_close(E)
    E.add(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="{INK}" stroke-width="2"/>')
    rect(E, x0 - 22, y1 + 10, x1 + 22, y1 + 22, hatches=[(0, 3, 0.3)], sw=1.8)


def tureen(E, x, y, s=1.0):
    """A soup tureen with a domed lid and knob, base at (x, y); thin steam rises."""
    E.shape([(x - 54 * s, y - 36 * s), (x + 54 * s, y - 36 * s), (x + 44 * s, y - 4 * s), (x - 44 * s, y - 4 * s)],
            hatches=[(70, 3, 0.4)], sw=2)
    E.shape([(x - 52 * s, y - 36 * s), (x - 40 * s, y - 62 * s), (x - 14 * s, y - 76 * s), (x + 14 * s, y - 76 * s), (x + 40 * s, y - 62 * s),
             (x + 52 * s, y - 36 * s)], hatches=[(60, 3, 0.3)], sw=2)
    E.shape(ellipse_pts(x, y - 82 * s, 8 * s, 6 * s, 10), fill=INK, outline=False)
    E.shape(ellipse_pts(x, y - 2 * s, 46 * s, 5 * s, 14), hatches=[(0, 2, 0.5)], sw=1.5)
    for k in range(3):
        E.line([(x - 12 * s + k * 12 * s, y - 90 * s), (x - 18 * s + k * 12 * s, y - 104 * s), (x - 8 * s + k * 12 * s, y - 118 * s)],
               w=1.0, op=0.45)


def bowl(E, x, y, rx=34, depth=18):
    """A soup bowl seen from the side with its rim, base centre (x, y)."""
    E.shape([(x - rx, y - depth), (x + rx, y - depth), (x + rx * 0.6, y), (x - rx * 0.6, y)], hatches=[(70, 3, 0.35)], sw=1.8)
    E.shape(ellipse_pts(x, y - depth, rx, 6, 14), tone=0.3, sw=1.6)


def is07(rng):
    """Seven: a family at lamplit supper while a storm wrecks the shore; the mother draws the curtain."""
    E = _pip(7, "g", rng)
    FL = 1010
    TOP = 770
    wall(E, 340, FL, op=0.14)
    fade(E, 420, 340, IX1, FL, op=0.6, side="r", reach=1.0)
    fade(E, IX0, 340, 160, FL, op=0.4, side="l", reach=1.0)
    storm_window(E, rng, 336, 372, 590, 700)
    # curtain on the room side of the window, partly drawn from the left
    curtain(E, 326, 600, 356, 712, drawn=0.3, side="left", op=0.45)
    # hanging lamp over the table
    E.line([(228, 330), (228, 520)], w=1.4, smooth=False)
    glow(E, 228, 560, 96, 70, 0.32)
    E.shape([(228 - 16, 520), (228 + 16, 520), (228 + 46, 566), (228 - 46, 566)], smooth=False, hatches=[(75, 3, 0.35)], sw=2)
    E.shape(ellipse_pts(228, 568, 12, 5, 10), sw=1.4)
    floor_band(E, FL, 0.14)
    # the mother, standing: one hand on the curtain, the other with the ladle over the tureen
    mo = adult(E, 338, FL - 26, 530, facing=1, lean=0.14, tilt=-6, garment="dress", wash_op=0.8,
               hands={"near": (402, TOP - 40), "far": (400, 590)}, stride=0.03)
    # the family, seated, facing us
    for fx, fy, kind, h_, g_ in ((112, 836, "adult", 500, "vest"), (214, 856, "child", 380, "smock")):
        fn = {"adult": adult, "child": child}[kind]
        fn(E, fx, fy, h_, view="front", pose="torso", garment=g_, hair="dark", wash_op=0.7, mouth=0.0,
           hands={"left": (fx - 32, TOP - 4), "right": (fx + 32, TOP - 4)})
    # table with cloth
    E.shape([(70, TOP - 6), (610, TOP - 6), (618, TOP + 12), (62, TOP + 12)], smooth=False, hatches=[(0, 5, 0.25)], sw=1.8)
    E.shape([(62, TOP + 12), (618, TOP + 12), (624, 1004), (56, 1004)], smooth=False, hatches=[(90, 6, 0.4)], tone=0.1, sw=1.8)
    fade(E, 62, TOP + 12, 624, 1004, op=0.7, side="b", reach=1.0)
    for k in range(1, 18):
        xx = 62 + 556 * k / 18
        E.line([(xx, TOP + 16), (xx + (3 if k % 2 else -3), 1000)], w=0.8, op=0.5, smooth=False)
    for bx in (112, 214, 272):
        bowl(E, bx, TOP + 4, 32, 16)
    tureen(E, 380, TOP + 6, 1.0)
    # the ladle in the mother's near hand
    lx, ly = mo["hands"]["near"]
    E.line([(lx, ly), (lx - 10, ly + 26)], w=3.0, smooth=False)
    E.shape(ellipse_pts(lx - 12, ly + 32, 11, 7, 10), hatches=[(0, 2, 0.5)], sw=1.6)
    hand_dot(E, (lx, ly), 7, 0.6)
    return _end(E, pess_pip_close())


def open_book(E, cx, cy, w=64, h=76, rot=-14):
    """An open book held up to read: two pages with a spine, tilted by rot degrees."""
    E.add(f'<g transform="rotate({rot} {f(cx)} {f(cy)})">')
    rect(E, cx - w / 2 - 3, cy - h / 2 - 3, cx + w / 2 + 3, cy + h / 2 + 3, hatches=[(70, 2.4, 0.6)], sw=1.8)
    for sg in (-1, 1):
        E.shape([(cx, cy - h / 2), (cx + sg * w / 2, cy - h / 2 + 2), (cx + sg * w / 2, cy + h / 2 - 2), (cx, cy + h / 2)],
                smooth=False, sw=1.3)
        for k in range(1, 5):
            yy = cy - h / 2 + k * h / 5
            E.line([(cx + sg * 6, yy), (cx + sg * (w / 2 - 6), yy + 1)], w=0.6, op=0.4, smooth=False)
    E.add("</g>")


def is08(rng):
    """Eight: two relatives at either end of a long sofa, each reading; a door ajar on darkness behind."""
    E = _pip(8, "h", rng)
    FL = 1010
    wall(E, 340, FL, op=0.14)
    fade(E, IX0, 340, 200, FL, op=0.5, side="l", reach=1.0)
    fade(E, 480, 340, IX1, FL, op=0.5, side="r", reach=1.0)
    fade(E, IX0, 340, IX1, 450, op=0.4, side="t", reach=1.0)
    # framed pictures, blank, either side
    for fx in (96, 468):
        rect(E, fx, 420, fx + 80, 540, hatches=[(90, 4, 0.2)], sw=2)
        rect(E, fx + 8, 428, fx + 72, 532, hatches=[(50, 4.4, 0.3)], sw=1.2)
    # the door, ajar on darkness; nobody looks at it
    rect(E, 284, 424, 396, 760, sw=2.2)
    mass(E, [(294, 434), (386, 434), (386, 760), (294, 760)], solid=0.7, wash=0.4, sw=1.6)
    E.shape([(294, 434), (338, 452), (338, 760), (294, 760)], smooth=False, hatches=[(80, 3, 0.4)], sw=2)
    rect(E, 304, 470, 328, 560, fill=None, sw=1.2)
    E.shape(ellipse_pts(330, 620, 3.4, 3.4, 8), fill=INK, outline=False)
    floor_band(E, FL, 0.14)
    # sofa: back, seat, arms, short legs
    SY = 918
    E.shape([(84, 738), (596, 738), (596, SY), (84, SY)], smooth=False, hatches=[(70, 4, 0.4), (-50, 5, 0.3)], sw=2.2)
    for k in range(4):
        x0_ = 130 + k * 108
        E.shape([(x0_, 752), (x0_ + 100, 752), (x0_ + 100, SY - 6), (x0_, SY - 6)], smooth=False, hatches=[(80, 6, 0.2)], sw=1.4)
    for ax in (70, 562):
        E.shape([(ax, SY - 38), (ax + 48, SY - 38), (ax + 48, SY + 38), (ax, SY + 38)], smooth=False, hatches=[(0, 4, 0.4)], sw=2)
    E.shape([(84, SY), (596, SY), (596, SY + 40), (84, SY + 40)], smooth=False, hatches=[(0, 4, 0.35)], sw=2.2)
    cast(E, [(84, SY + 40), (596, SY + 40), (604, FL - 2), (76, FL - 2)], 0.65)
    for lx in (96, 580):
        rect(E, lx - 6, SY + 40, lx + 6, FL, hatches=[(80, 2.6, 0.5)], sw=1.6)
    fade(E, 84, 738, 596, SY, op=0.5, side="t", reach=0.8)
    # readers
    open_book(E, 238, 806, 60, 72, -12)
    open_book(E, 442, 806, 60, 72, 12)
    adult(E, 150, FL, 430, pose="sit", facing=1, lean=0.12, tilt=20, wash_op=0.75,
          hands={"near": (232, 826), "far": (252, 800)})
    elder(E, 530, FL, 430, pose="sit", facing=-1, lean=0.2, tilt=-20, garment="coat", hair="white", wash_op=0.8,
          hands={"near": (448, 826), "far": (430, 800)})
    # low table between them: lamp and a covered dish
    TT = 985
    rect(E, 276, TT, 404, TT + 12, hatches=[(0, 3, 0.4)], sw=1.8)
    for lx in (284, 396):
        rect(E, lx - 4, TT + 12, lx + 4, FL, sw=1.5)
    table_lamp(E, 312, TT, 0.85)
    E.shape(ellipse_pts(366, TT - 3, 28, 5, 12), hatches=[(0, 2, 0.5)], sw=1.5)
    E.shape([(340, TT - 5), (342, TT - 22), (354, TT - 34), (378, TT - 34), (390, TT - 22), (392, TT - 5)],
            hatches=[(60, 3, 0.3)], sw=1.8)
    E.shape(ellipse_pts(366, TT - 38, 5, 4, 8), fill=INK, outline=False)
    return _end(E, pess_pip_close())


def shard_sphere(E, cx, cy, r, rng, n=8):
    """Pieces of broken china lying in the shape of a sphere: n curved shards with thin gaps."""
    angs = sorted(rng.uniform(0, 2 * math.pi) for _ in range(n))
    for i in range(n):
        a0, a1 = angs[i], angs[(i + 1) % n] + (2 * math.pi if i == n - 1 else 0)
        mid = (a0 + a1) / 2
        gx_, gy_ = math.cos(mid) * 2.2, math.sin(mid) * 2.2
        inner = rng.uniform(0.0, 0.35)
        pts = [(cx + math.cos(mid) * r * inner + gx_, cy + math.sin(mid) * r * inner + gy_)]
        for k in range(6):
            a = a0 + (a1 - a0) * k / 5
            rr = r * (1 + rng.uniform(-0.03, 0.03))
            pts.append((cx + math.cos(a) * rr + gx_, cy + math.sin(a) * rr + gy_))
        light = mid > math.pi * 1.1 and mid < math.pi * 1.9
        E.shape(pts, smooth=False, hatches=[] if light else [(40 + i * 25, 3.2, 0.45)], sw=1.5)
    E.line([(cx - r * 0.55, cy - r * 0.45), (cx - r * 0.1, cy - r * 0.75)], w=2, op=0.8, color="#ffffff")


def crate(E, x0, y0, x1, y1):
    """A packing crate with cross braces."""
    rect(E, x0, y0, x1, y1, hatches=[(80, 4, 0.3)], sw=2)
    rect(E, x0 + 8, y0 + 8, x1 - 8, y1 - 8, fill=None, sw=1.2)
    E.line([(x0 + 8, y0 + 8), (x1 - 8, y1 - 8)], w=1.4, smooth=False, op=0.8)
    E.line([(x1 - 8, y0 + 8), (x0 + 8, y1 - 8)], w=1.4, smooth=False, op=0.8)


def is09(rng):
    """Nine: in a house being cleared a woman wraps china; a cracked tureen lies in pieces on a chair."""
    E = _pip(9, "i", rng)
    FL = 1010
    wall(E, 340, FL, op=0.17)
    fade(E, IX0, 340, 330, FL, op=0.6, side="l", reach=1.0)
    fade(E, 500, 340, IX1, FL, op=0.55, side="r", reach=1.0)
    window(E, 372, 400, 540, 650, tone=0.06, panes=(2, 2))
    # the pale patch where a picture hung, and its hook: the wall hatching stops at the patch
    rect(E, 110, 420, 210, 540, sw=0.9)
    E.add(f'<circle cx="160" cy="432" r="3" fill="{INK}"/>')
    # crates against the back wall
    crate(E, 540, 860, 606, 1010)
    crate(E, 548, 770, 604, 860)
    E.shape([(562, 600), (598, 600), (598, 770), (562, 770)], smooth=False, hatches=[(80, 3.4, 0.4)], sw=1.6)
    floor_band(E, FL, 0.14)
    fade(E, 540, 770, 606, 1010, op=0.65, side="l", reach=1.0)
    floor_shadow(E, 135, FL - 2, 90, 9, 0.6)
    # the chair with the broken tureen, behind her
    chair_side(E, 132, FL, seat=125, f_dir=1, back_h=200, w=104)
    shard_sphere(E, 140, 885 - 52, 50, rng)
    TOP = 800
    # table with newspaper and wrapped parcels
    cast(E, [(306, TOP + 22), (590, TOP + 22), (600, FL - 2), (298, FL - 2)], 0.65)
    floor_shadow(E, 236, FL - 2, 120, 10, 0.6)
    table_front(E, 300, 590, TOP, FL, thick=18, legs=(0.05, 0.95))
    newspaper(E, 380, TOP - 4, 90, 14, rot=0, cols=1)
    newspaper(E, 480, TOP - 6, 84, 14, rot=0, cols=1)
    for bx_ in (450, 500, 548):
        E.shape(ellipse_pts(bx_, TOP - 34, 26, 30, 14), hatches=[(45, 3.2, 0.35), (-45, 4, 0.3)], sw=1.8)
    w_ = adult(E, 236, FL, 500, facing=1, lean=0.2, tilt=16, garment="dress", wash_op=0.8, mouth=0,
               hands={"near": (330, TOP - 50), "far": (312, TOP - 70)}, stride=0.03)
    hx, hy = w_["hands"]["near"]
    E.shape(ellipse_pts(hx - 6, hy - 14, 34, 34, 16), hatches=[(80, 5, 0.22)], sw=1.8)
    E.shape([(hx - 40, hy - 4), (hx + 30, hy - 8), (hx + 36, hy + 24), (hx - 36, hy + 28)], smooth=False, hatches=[(0, 5, 0.3)], sw=1.5)
    for hnd in (w_["hands"]["near"], w_["hands"]["far"]):
        hand_dot(E, hnd, 7)
    return _end(E, pess_pip_close())


def head_shadow(E, cx, cy, s=1.0):
    """The shadow of a head and shoulders on a wall, soft: nested shapes of hatching that thin outward,
    no outline and no fill, over a faint blurred tint."""
    E.add(f'<ellipse cx="{f(cx + 20 * s)}" cy="{f(cy + 90 * s)}" rx="{f(150 * s)}" ry="{f(190 * s)}" fill="{SLATE}" opacity="{min(0.6, 0.34 * CONTRAST):.2f}" filter="url(#mist)"/>')
    layers = ((1.0, 5.0, 0.3, None), (0.85, 3.8, 0.4, None), (0.7, 3.0, 0.5, -52), (0.55, 2.4, 0.6, -30), (0.4, 2.0, 0.7, 20))
    for k, gap, op, cross in layers:
        op = min(0.92, op * (0.75 + 0.25 * _boost()))
        head_ = ellipse_pts(cx, cy, 76 * s * k, 92 * s * k, 18, rot=0.45)
        body = [(cx - 76 * s * k, cy + 120 * s), (cx - 44 * s * k, cy + 52 * s), (cx + 50 * s * k, cy + 46 * s),
                (cx + 154 * s * k, cy + 132 * s), (cx + 176 * s * k, cy + 380 * s), (cx - 86 * s * k, cy + 380 * s)]
        for pts in (head_, body):
            d = _smooth_d(pts) if pts is head_ else _poly_d(pts)
            bb = _bbox(pts)
            E.hatch_d(d, bb, 62, gap, op, 0.7)
            if cross is not None:
                E.hatch_d(d, bb, cross, gap * 1.1, op * 0.8, 0.7)


def is10(rng):
    """Ten: a man sits up in bed with the lamp lit; his head's shadow leans over him on the wall."""
    E = _pip(10, "j", rng)
    FL = 1010
    wall(E, 340, FL, op=0.12)
    fade(E, IX0, 340, 360, FL, op=0.6, side="l", reach=1.0)
    fade(E, IX0, 340, IX1, 500, op=0.45, side="t", reach=1.0)
    head_shadow(E, 176, 520)
    # window with the grey of early morning
    window(E, 440, 400, 584, 660, tone=0.12, panes=(1, 2), glow=None)
    floor_band(E, FL, 0.14)
    # bedside table: lamp, glass of water, closed book
    TT = 800
    rect(E, 440, TT, 606, TT + 16, hatches=[(0, 3, 0.35)], sw=1.8)
    for lx in (454, 592):
        rect(E, lx - 5, TT + 16, lx + 5, FL, hatches=[(80, 2.6, 0.5)], sw=1.5)
    table_lamp(E, 476, TT, 0.95)
    gx_ = 530
    E.shape([(gx_ - 17, TT - 54), (gx_ + 17, TT - 54), (gx_ + 14, TT), (gx_ - 14, TT)], smooth=False, tone=0.08, sw=1.8)
    E.shape([(gx_ - 16, TT - 30), (gx_ + 16, TT - 30), (gx_ + 14, TT), (gx_ - 14, TT)], smooth=False, hatches=[(0, 2.6, 0.45)], outline=False)
    book(E, 552, TT, 54, 16)
    # bed: headboard, footboard, pillow, frame
    mass(E, [(78, 640), (116, 640), (116, FL), (78, FL)], solid=0.55, sw=2)
    E.shape(ellipse_pts(97, 636, 24, 12, 12), hatches=[(0, 2.4, 0.5)], sw=1.8)
    rect(E, 426, 836, 456, FL, hatches=[(80, 3, 0.5)], sw=2)
    E.shape([(116, 746), (206, 740), (216, 880), (116, 884)], hatches=[(30, 6, 0.22)], sw=1.8)
    m = adult(E, 232, 904, 500, pose="torso", facing=1, lean=0.02, tilt=2, garment="vest", hair="dark", wash_op=0.5,
              hands={"near": (306, 868), "far": (290, 872)}, look=0.5)
    # blanket over his legs; its edge rises over the foot of the shadow
    E.shape([(150, 888), (214, 868), (260, 872), (310, 840), (372, 818), (430, 846), (446, 960), (150, 970)],
            hatches=[(20, 4, 0.4), (-60, 6, 0.3)], tone=0.45, sw=2)
    for fx_, fy_ in ((260, 880), (330, 850), (390, 840)):
        E.line([(fx_, fy_), (fx_ + 10, fy_ + 80)], w=1.1, op=0.7)
    rect(E, 116, 936, 446, 972, hatches=[(0, 4, 0.3)], sw=2)
    cast(E, [(110, 972), (456, 972), (466, FL - 2), (100, FL - 2)], 0.7)
    hand_dot(E, m["hands"]["near"], 7)
    return _end(E, pess_pip_close(), op=0.55, cx=470, cy=700)


# ------------------------------------------------------------------ court cards

def snail(E, x, y, s=1.0, facing=-1):
    """A garden snail on the ground at (x, y): spiral shell, body, two eyestalks, head toward `facing`."""
    fd = facing
    E.shape([(x - fd * 52 * s, y), (x - fd * 30 * s, y - 12 * s), (x + fd * 20 * s, y - 14 * s), (x + fd * 46 * s, y - 26 * s),
             (x + fd * 58 * s, y - 20 * s), (x + fd * 50 * s, y)], hatches=[(10, 3, 0.4)], sw=1.8)
    E.line([(x + fd * 52 * s, y - 24 * s), (x + fd * 58 * s, y - 46 * s)], w=1.8, smooth=False)
    E.line([(x + fd * 44 * s, y - 24 * s), (x + fd * 44 * s, y - 46 * s)], w=1.8, smooth=False)
    cx_, cy_ = x - fd * 12 * s, y - 34 * s
    E.shape(ellipse_pts(cx_, cy_, 34 * s, 32 * s, 18), tone=0.3, hatches=[(50, 3, 0.4)], sw=2)
    pts = []
    for k in range(40):
        a = k * 0.42
        rr = 2 + k * 0.7
        pts.append((cx_ + math.cos(a) * rr * s, cy_ + math.sin(a) * rr * s))
    E.line(pts, w=1.5, op=0.9)


def is11(rng):
    """Child: a girl of seven on a garden step beside a dead bird under a leaf, watching a snail; an adult
    watches from a window and does not come out."""
    E = _court(1, "k", rng)
    FL = 1010
    STEP = 910   # top of the step; the seated girl's hip is a shin's length above the ground
    # house wall: clapboards as fine horizontal lines, thinning downward
    sky(E, 210, STEP, strongest=0.32, weakest=0.05, gap=6, tint=0.7)
    window(E, 340, 250, 570, 560, tone=0.78, panes=(1, 1))
    clip_open(E, 340, 250, 570, 560)
    adult(E, 456, 720, 560, view="front", pose="torso", garment="dress", hair="bun", wash_op=0.85, look=-0.15, tilt=-3,
          hands={"left": (386, 500, -1), "right": (540, 650)})
    clip_close(E)
    E.line([(366, 282), (440, 520)], w=9, op=0.5, color=PAPER_FILL, smooth=False)
    E.line([(400, 270), (470, 520)], w=4, op=0.5, color=PAPER_FILL, smooth=False)
    mass(E, [(90, 340), (262, 340), (262, STEP), (90, STEP)], solid=0.35, wash=0.3, sw=2.2)
    rect(E, 108, 362, 244, 560, fill=None, sw=1.4)
    rect(E, 108, 584, 244, STEP - 20, fill=None, sw=1.4)
    E.shape(ellipse_pts(230, 740, 6, 6, 8), fill=INK, outline=False)
    grass(E, FL - 4, IY1, 520)
    fade(E, IX0, FL - 4, IX1, IY1 + 10, op=0.75, side="b", reach=1.0)
    E.line([(IX0, FL), (IX1, FL)], w=1.2, op=0.7)
    # step
    rect(E, 70, STEP, 450, FL, hatches=[(80, 4, 0.34), (0, 8, 0.2)], sw=2.2)
    fade(E, 70, STEP, 450, FL, op=0.6, side="b", reach=1.0)
    rect(E, 70, STEP - 14, 450, STEP, hatches=[(0, 3.6, 0.2)], sw=2)
    # shoebox with the bird under a leaf
    bx0, bx1 = 330, 450
    rect(E, bx0, STEP - 40, bx1, STEP - 14, hatches=[(70, 3, 0.4)], sw=2)
    E.shape([(bx0 - 6, STEP - 50), (bx1 + 6, STEP - 50), (bx1, STEP - 36), (bx0, STEP - 36)], smooth=False, hatches=[(0, 3.4, 0.25)], sw=1.8)
    leaf = [(bx0 + 18, STEP - 50), (bx0 + 48, STEP - 72), (bx1 - 24, STEP - 72), (bx1, STEP - 52), (bx1 - 28, STEP - 44), (bx0 + 44, STEP - 44)]
    E.shape(leaf, tone=0.3, hatches=[(30, 3, 0.4)], sw=1.8)
    E.line([(bx0 + 24, STEP - 53), (bx1 - 4, STEP - 55)], w=1.2, op=0.8, smooth=False)
    E.line([(bx1 + 2, STEP - 54), (bx1 + 24, STEP - 50), (bx1 + 20, STEP - 44)], w=1.6, smooth=False)  # a tail feather
    E.line([(bx1 + 2, STEP - 54), (bx1 + 22, STEP - 60)], w=1.4, smooth=False)
    # the girl, leaning to look at the snail
    child(E, 205, FL, 430, pose="sit", facing=1, lean=0.36, tilt=24, wash_op=0.75, look=0.6,
          hands={"near": (320, STEP - 24), "far": (292, STEP - 18)})
    floor_shadow(E, 520, FL - 2, 70, 7, 0.6)
    snail(E, 520, FL - 4, 1.2, facing=-1)
    # hollyhocks
    for sx, sh in ((582, 400), (554, 300)):
        E.line([(sx, FL), (sx - 4, FL - sh)], w=2.4, smooth=False)
        for k in range(6):
            yy = FL - 70 - k * (sh - 100) / 5
            E.shape(ellipse_pts(sx + (-1) ** k * 12 - 2, yy, 12, 11, 10), hatches=[(40, 3, 0.45)], sw=1.4)
    return _end(E, pess_court_close(), top=196, cy=700)


def bollard(E, x, y, s=1.0):
    """A short quay bollard with a coil of rope, base at (x, y)."""
    E.shape([(x - 14 * s, y), (x - 11 * s, y - 52 * s), (x + 11 * s, y - 52 * s), (x + 14 * s, y)], smooth=False,
            hatches=[(80, 3, 0.55)], sw=1.8)
    E.shape(ellipse_pts(x, y - 56 * s, 16 * s, 6 * s, 12), hatches=[(0, 2, 0.5)], sw=1.8)
    for k in range(3):
        E.shape(ellipse_pts(x, y - 18 * s - k * 8 * s, 18 * s, 5 * s, 12), fill=None, sw=2.0)


def ship(E, x, y, s=1.0):
    """A sailing ship at its berth, seen from the side: hull, two masts with furled sails and rigging."""
    hull = [(x - 100 * s, y - 40 * s), (x + 110 * s, y - 52 * s), (x + 90 * s, y + 6 * s), (x - 70 * s, y + 6 * s)]
    E.shape(hull, smooth=False, hatches=[(0, 3, 0.6), (60, 5, 0.4)], sw=2)
    E.line([(x - 100 * s, y - 40 * s), (x + 110 * s, y - 52 * s)], w=2.6, smooth=False)
    for mx, mh in ((x - 36 * s, 430), (x + 52 * s, 520)):
        E.line([(mx, y - 44 * s), (mx, y - mh * s)], w=3.6, smooth=False)
        for yy in (0.5, 0.72, 0.9):
            hy = y - mh * s * yy
            E.line([(mx - 40 * s, hy), (mx + 40 * s, hy)], w=2.6, smooth=False)
            E.shape([(mx - 38 * s, hy + 3), (mx + 38 * s, hy + 3), (mx + 30 * s, hy + 26 * s), (mx - 30 * s, hy + 26 * s)],
                    smooth=False, hatches=[(90, 4.4, 0.34)], sw=1.4)
    E.line([(x - 100 * s, y - 40 * s), (x - 36 * s, y - 430 * s), (x + 52 * s, y - 520 * s), (x + 110 * s, y - 52 * s)],
           w=0.9, op=0.7, smooth=False)
    E.line([(x - 36 * s, y - 420 * s), (x + 52 * s, y - 56 * s)], w=0.8, op=0.6, smooth=False)


def cloud_bank(E, x, y, w, h, op=0.3):
    """A long low cloud: a lens of hatching with an uneven underside, no outline."""
    pts = [(x, y), (x + w * 0.25, y - h * 0.8), (x + w * 0.6, y - h), (x + w * 0.9, y - h * 0.4), (x + w, y),
           (x + w * 0.7, y + h * 0.35), (x + w * 0.3, y + h * 0.3)]
    d = _smooth_d(pts)
    op = min(0.9, op * _boost())
    E.hatch_d(d, _bbox(pts), -2, 3.6, op, 0.7)
    E.hatch_d(d, _bbox(pts), 28, 4.2, op * 0.8, 0.6, sub=(x + w * 0.4, y - h, x + w, y + h))


def is12(rng):
    """Youth: a young man in a travelling coat stands on a quay with his trunk, back turned on older relatives;
    an old woman raises a hand to ask a question she does not put."""
    E = _court(2, "l", rng)
    LINE = 960
    HOR = 720
    EDGE = 484
    # a sky of etched lines over a thin slate tint, with cloud banks and gulls
    sky(E, 210, HOR, strongest=0.42, weakest=0.04, gap=6, tint=0.85)
    cloud_bank(E, 90, 330, 260, 36, 0.3)
    cloud_bank(E, 360, 440, 230, 30, 0.28)
    cloud_bank(E, 120, 560, 200, 24, 0.24)
    for gx, gy in ((380, 300), (430, 338), (330, 360)):
        E.line([(gx - 14, gy + 4), (gx - 6, gy - 4), (gx, gy + 2), (gx + 6, gy - 4), (gx + 14, gy + 4)], w=1.3)
    # sea and ship
    slate(E, EDGE, HOR, VX1 + 20, IY1 + 20, 0.6)
    E.line([(IX0, HOR), (IX1, HOR)], w=1.0, smooth=False, op=0.6)
    d = []
    for k in range(18):
        yy = HOR + 14 + k * 20
        d.append(f"M{EDGE},{yy} " + " ".join("q8,-6 16,0" for _ in range(11)))
    E.add(f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width="0.8" opacity="0.5" fill="none"/>')
    ship(E, 548, 900, 0.56)
    # warehouses behind the relatives
    for wx, ww, wh in ((72, 120, 240), (196, 96, 170), (300, 130, 290), (440, 40, 130)):
        rect(E, wx, HOR - wh, wx + ww, HOR + 14, hatches=[(80, 4, 0.26)], tone=0.3, sw=1.8)
        E.shape([(wx - 6, HOR - wh), (wx + ww / 2, HOR - wh - 40), (wx + ww + 6, HOR - wh)], smooth=False,
                hatches=[(30, 4, 0.45)], sw=1.8)
        for k in range(2):
            rect(E, wx + 14 + k * (ww - 44), HOR - wh + 36, wx + 30 + k * (ww - 44), HOR - wh + 66, hatches=[(60, 2.4, 0.7)], sw=1.2)
    # the quay: stone top and face
    E.shape([(70, LINE), (EDGE, LINE), (EDGE, IY1 + 10), (70, IY1 + 10)], smooth=False, hatches=[(0, 16, 0.18)], sw=2)
    for k in range(4):
        yy = LINE + 22 + k * 26
        E.line([(70, yy), (EDGE, yy)], w=0.7, op=0.5, smooth=False)
        for xx in range(80 + (k % 2) * 40, EDGE, 80):
            E.line([(xx, yy), (xx, yy + 26)], w=0.7, op=0.5, smooth=False)
    E.line([(70, LINE), (EDGE, LINE)], w=2, smooth=False)
    fade(E, 70, LINE, EDGE, IY1 + 10, op=0.8, side="b", reach=1.0)
    for fx_ in (116, 196, 416):
        floor_shadow(E, fx_ + 8, LINE + 3, 70, 8, 0.7)
    bollard(E, EDGE - 22, LINE, 1.1)
    # trunk, between the relatives and the youth
    tx0, tx1 = 258, 342
    E.shape([(tx0, LINE), (tx0, LINE - 66), (tx0 + 14, LINE - 88), (tx1 - 14, LINE - 88), (tx1, LINE - 66), (tx1, LINE)],
            smooth=False, hatches=[(60, 3, 0.4)], sw=2)
    E.line([(tx0, LINE - 66), (tx1, LINE - 66)], w=1.6, smooth=False)
    for sx in (tx0 + 20, tx1 - 20):
        E.line([(sx, LINE - 88), (sx, LINE)], w=4.5, smooth=False)
    E.shape(ellipse_pts((tx0 + tx1) / 2, LINE - 38, 5, 5, 8), fill=INK, outline=False)
    # relatives behind him: the old woman asks, without asking
    adult(E, 116, LINE, 480, facing=1, lean=0.08, garment="dress", mouth=0.7, wash_op=0.8, look=0.9,
          hands={"near": (184, LINE - 330), "far": (134, LINE - 230)})
    elder(E, 196, LINE, 450, facing=1, lean=0.22, garment="long", hair="white", wash_op=0.85, look=0.9, tilt=-4,
          hands={"near": (284, LINE - 340), "far": (214, LINE - 200)})
    # the youth, facing the sea
    youth(E, 416, LINE, 540, facing=1, lean=0.05, hat="wide", garment="coat", wash_op=0.85, look=0.9,
          hands={"near": (456, LINE - 270), "far": (412, LINE - 280)})
    return _end(E, pess_court_close(), top=196, cy=700)


def envelope(E, x, y, w=96, h=60, rot=0, tone=0.0):
    """A sealed envelope: rectangle, flap lines, a small stamp square; centred at (x, y)."""
    E.add(f'<g transform="rotate({rot} {f(x)} {f(y)})">')
    rect(E, x - w / 2, y - h / 2, x + w / 2, y + h / 2, tone=tone, sw=1.6)
    E.line([(x - w / 2, y - h / 2), (x, y + h * 0.1), (x + w / 2, y - h / 2)], w=1.2, smooth=False)
    rect(E, x + w / 2 - 22, y - h / 2 + 5, x + w / 2 - 6, y - h / 2 + 22, fill=None, sw=1.0)
    E.line([(x - w / 2 + 10, y + h * 0.3), (x - 4, y + h * 0.3)], w=0.8, smooth=False, op=0.6)
    E.add("</g>")


def wall_phone(E, x, y):
    """A wall telephone with two bells, a handset on its hook and a coiled cord; (x, y) is the box top-left."""
    rect(E, x, y, x + 62, y + 100, hatches=[(80, 3, 0.45)], sw=2.2)
    for bx in (x + 16, x + 46):
        E.shape(ellipse_pts(bx, y + 14, 11, 11, 12), sw=1.8)
    E.shape(ellipse_pts(x + 31, y + 56, 14, 14, 12), hatches=[(0, 2.4, 0.5)], sw=1.6)
    rect(E, x + 62, y + 20, x + 76, y + 72, hatches=[(80, 1.9, 0.85), (-40, 2.2, 0.6)], sw=1.6)
    E.shape(ellipse_pts(x + 69, y + 18, 11, 8, 10), hatches=[(0, 1.9, 0.85)], sw=1.4)
    E.shape(ellipse_pts(x + 69, y + 76, 11, 8, 10), hatches=[(0, 1.9, 0.85)], sw=1.4)
    pts = [(x + 69, y + 84)]
    for k in range(14):
        pts.append((x + 69 + (6 if k % 2 else -6), y + 90 + k * 6))
    E.line(pts, w=1.5, smooth=False)


def wall_clock(E, cx, cy, r=34):
    """A round wall clock: ring, ticks and two hands; no figures."""
    E.shape(ellipse_pts(cx, cy, r, r, 20), hatches=[(60, 3, 0.3, (cx, cy - r, cx + r, cy + r))], sw=2.2)
    E.shape(ellipse_pts(cx, cy, r * 0.8, r * 0.8, 20), sw=1.2)
    for k in range(12):
        a = k * math.pi / 6
        E.line([(cx + r * 0.62 * math.sin(a), cy - r * 0.62 * math.cos(a)), (cx + r * 0.74 * math.sin(a), cy - r * 0.74 * math.cos(a))], w=1.3, smooth=False)
    E.line([(cx, cy), (cx + r * 0.22, cy - r * 0.46)], w=2.2, smooth=False)
    E.line([(cx, cy), (cx - r * 0.5, cy + r * 0.12)], w=1.8, smooth=False)


def is13(rng):
    """Adult: a woman in her forties at the kitchen counter after work, reading a jar's label closely; unopened
    letters beside her, a note by the wall telephone turned face down."""
    E = _court(3, "m", rng)
    FL = 1010
    TOP = 764
    # the room above the counter: a ceiling beam, plaster hatched toward the corners, a clock
    wall(E, 210, FL, op=0.2, gap=6.5)
    fade(E, IX0, 232, 260, FL, op=0.55, side="l", reach=1.0)
    fade(E, IX0, 232, IX1, 420, op=0.45, side="t", reach=1.0)
    mass(E, [(IX0 - 10, 196), (IX1 + 10, 196), (IX1 + 10, 232), (IX0 - 10, 232)], solid=0.6, sw=2)
    for bx in (150, 330, 510):
        E.line([(bx, 232), (bx + 18, 262)], w=1.4, op=0.6)
    wall_clock(E, 340, 330, 32)
    # pendant lamp, unlit
    E.line([(236, 232), (236, 250)], w=1.4, smooth=False)
    mass(E, [(214, 250), (258, 250), (282, 290), (190, 290)], solid=0.55, sw=2)
    window(E, 430, 270, 580, 500, tone=0.8, panes=(1, 2))
    # shelf of jars over the counter
    rect(E, 470, 640, 604, 652, hatches=[(0, 3, 0.4)], sw=1.8)
    for jx, jh in ((500, 64), (550, 52), (590, 70)):
        jar(E, jx, 640, 36, jh, tone=0.22)
    # telephone and the note beneath it, turned face down
    wall_phone(E, 96, 330)
    E.shape([(108, 520), (178, 512), (184, 580), (114, 588)], smooth=False, hatches=[(70, 4, 0.26)], sw=1.6)
    E.shape([(184, 580), (168, 570), (176, 586)], smooth=False, hatches=[(0, 2, 0.5)], sw=1.2)
    E.add('<circle cx="144" cy="517" r="3.4" fill="#2a2622"/>')
    floor_band(E, FL, 0.14)
    # counter with cupboard doors
    rect(E, 340, TOP, 612, FL, hatches=[(80, 5, 0.22)], sw=2)
    for dx in (352, 484):
        rect(E, dx, TOP + 28, dx + 120, FL - 24, sw=1.6)
        E.shape(ellipse_pts(dx + 104, TOP + 120, 4, 4, 8), fill=INK, outline=False)
    fade(E, 340, TOP, 612, FL, op=0.7, side="b", reach=1.0)
    rect(E, 332, TOP - 14, 612, TOP, hatches=[(0, 3, 0.35)], sw=2)
    for k, (ex, ey, rt) in enumerate(((524, TOP - 26, -3), (530, TOP - 38, 4), (520, TOP - 50, -5), (528, TOP - 62, 2),
                                      (524, TOP - 74, -2))):
        envelope(E, ex, ey, 104, 54, rt, tone=0.04 * k)
    E.shape([(372, TOP - 14), (364, TOP - 54), (384, TOP - 76), (422, TOP - 76), (442, TOP - 54), (434, TOP - 14)],
            hatches=[(60, 3, 0.45)], sw=2)
    E.line([(434, TOP - 50), (464, TOP - 70)], w=3, smooth=False)
    E.line([(378, TOP - 70), (403, TOP - 96), (428, TOP - 70)], w=3, smooth=False)
    # the woman, the jar before her eyes
    jx, jy = 400, 590
    w_ = adult(E, 262, FL, 590, facing=1, lean=0.12, tilt=14, garment="dress", wash_op=0.85, look=0.9,
               hands={"near": (jx - 8, jy + 40), "far": (jx - 30, jy + 28)})
    jar(E, jx + 4, jy + 62, 62, 104, tone=0.16)
    rect(E, jx - 24, jy + 12, jx + 32, jy + 44, sw=1.4)
    rect(E, jx - 19, jy + 17, jx + 27, jy + 39, fill=None, sw=0.8)
    for hnd in w_["hands"].values():
        hand_dot(E, hnd)
    return _end(E, pess_court_close(), top=196, cy=700)


def is14(rng):
    """Elder: an old man in a garden chair, shawl over his knees, eyes on a shut gate; beside him a bundle of
    letters tied with string, one end untied, and a pair of reading glasses."""
    E = _court(4, "n", rng)
    P = Pen("p14", rng)
    FL = 1010
    sky(E, 210, 724, strongest=0.4, weakest=0.05, gap=6, tint=0.85)
    # bare trees overhead fill the sky
    P.bare_tree(120, 740, 520, op=0.7, width=14)
    P.bare_tree(560, 720, 430, op=0.6, width=11)
    E.add(P.done())
    # hedge behind, gate in it: leaf loops in dense hatching
    mass(E, [(70, 740), (610, 724), (610, FL), (70, FL)], solid=0.4, wash=0.3, sw=1.4)
    for _ in range(90):
        hx, hy = rng.uniform(78, 604), rng.uniform(750, 990)
        E.shape(ellipse_pts(hx, hy, rng.uniform(8, 14), rng.uniform(5, 9), 8, rot=rng.uniform(0, 3)), fill=None, sw=0.8)
    gx0, gx1, gy0 = 484, 584, 760
    for px in (gx0 - 24, gx1 + 2):
        rect(E, px, gy0 - 40, px + 22, FL, hatches=[(80, 3, 0.5)], sw=2)
        rect(E, px - 4, gy0 - 50, px + 26, gy0 - 38, hatches=[(0, 2, 0.5)], sw=1.8)
    for ry in (gy0 + 16, gy0 + 112, 970):
        rect(E, gx0, ry - 12, gx1, ry + 12, hatches=[(0, 3, 0.4)], sw=2)
    for bx in (gx0 + 8, gx1 - 20):
        rect(E, bx, gy0 + 4, bx + 12, 982, hatches=[(80, 3, 0.4)], sw=2)
    E.line([(gx0 + 14, 970), (gx1 - 14, gy0 + 112)], w=7, smooth=False)
    E.line([(gx0 + 14, 970), (gx1 - 14, gy0 + 112)], w=3, smooth=False, color=PAPER_FILL)
    rect(E, gx0 + 30, gy0 + 44, gx0 + 44, gy0 + 72, hatches=[(80, 1.9, 0.85)], sw=1.4)  # latch
    E.line([(gx0 + 30, gy0 + 58), (gx0 + 58, gy0 + 58)], w=3, smooth=False)
    # path to the gate and grass
    E.shape([(gx0 + 6, FL), (gx1 - 6, FL), (590, IY1 + 10), (300, IY1 + 10)], smooth=False, hatches=[(15, 6, 0.2)], sw=1.4)
    grass(E, FL, IY1, 380)
    fade(E, IX0, FL, IX1, IY1 + 10, op=0.7, side="b", reach=1.0)
    floor_shadow(E, 170, FL - 2, 120, 9, 0.7)
    # garden chair and the old man
    chair_side(E, 170, FL, seat=135, f_dir=1, back_h=240, w=130)
    sit = elder(E, 150, FL, 560, pose="sit", facing=1, lean=0.3, garment="long", hair="white", wash_op=0.85, look=0.9, tilt=4,
                hands={"near": (262, 856), "far": (276, 860)})
    hip = sit["hip"]
    kx = hip[0] + 0.24 * 560
    shawl = [(hip[0] - 16, hip[1] - 26), (kx - 24, hip[1] - 40), (kx + 44, hip[1] - 14), (kx + 56, FL - 80), (kx + 16, FL - 74),
             (kx - 34, hip[1] + 70), (hip[0] - 22, hip[1] + 22)]
    mass(E, shawl, solid=0.35, sw=2)
    for k in range(5):
        E.line([(kx + 56 - k * 9, FL - 80), (kx + 56 - k * 9, FL - 64)], w=1.0, smooth=False)
    for hnd in sit["hands"].values():
        hand_dot(E, hnd)
    # table with the bundle of letters and the glasses
    TT = 800
    E.shape(ellipse_pts(380, TT, 76, 13, 20), hatches=[(0, 3, 0.4)], sw=2)
    rect(E, 374, TT + 8, 386, FL - 8, sw=1.6)
    E.shape(ellipse_pts(380, FL - 6, 46, 8, 14), hatches=[(0, 3, 0.4)], sw=1.6)
    for k, rt in enumerate((-3, 2, -1, 3, -2)):
        E.add(f'<g transform="rotate({rt} 350 {TT - 14})">')
        rect(E, 306, TT - 10 - k * 10, 394, TT - 1 - k * 10, tone=0.05 * k, sw=1.4)
        E.add("</g>")
    E.line([(340, TT - 56), (340, TT - 2)], w=2.2, smooth=False)
    E.line([(306, TT - 30), (394, TT - 30)], w=2.2, smooth=False)
    E.shape(ellipse_pts(340, TT - 30, 5, 5, 8), fill=INK, outline=False)
    E.line([(394, TT - 30), (414, TT - 12), (410, TT + 18), (422, TT + 40)], w=2.2)   # the untied end
    gx_, gy_ = 372, TT - 62
    for dx in (-16, 16):
        E.shape(ellipse_pts(gx_ + dx, gy_ + 2, 15, 13, 12), tone=0.08, sw=2)
    E.line([(gx_ - 1, gy_ - 2), (gx_ + 1, gy_ - 2)], w=2, smooth=False)
    E.line([(gx_ + 31, gy_ - 6), (gx_ + 52, gy_ - 8), (gx_ + 64, gy_ + 4)], w=1.8, smooth=False)
    E.line([(gx_ - 31, gy_ - 6), (gx_ - 52, gy_ - 8), (gx_ - 64, gy_ + 4)], w=1.8, smooth=False)
    return _end(E, pess_court_close(), top=196, cy=700)


CARDS = {f"is{n:02d}": fn for n, fn in enumerate(
    (is01, is02, is03, is04, is05, is06, is07, is08, is09, is10, is11, is12, is13, is14), start=1)}
