"""Zen deck, minor series, suit of Wind (wi01-wi15): breath, movement and speech.

Built on the pattern of zen_minor_earth, whose figure helpers (withdrawn, attending, acting,
engaged, ordinary), place() and props are imported rather than copied, with a few props from the
Water and Fire modules.

Wind cannot be drawn, so every card shows it through what it moves: grass, cloth, a flame, a leaf,
smoke, a wind chime, a kite.

Pips wi01-wi10: zen_pip_open("wind", n) draws the ensō with n black half-moons, then one small
vignette of the pip's Image paragraph is drawn in the lower inside of the ensō (ZEN_VIGNETTE), then
zen_pip_close(). No solid dark half-round shape is drawn in a vignette, so the half-moon count stays
readable: cushions, bells, hats and gourds are drawn pale or in outline.

Ranks wi11-wi15 use the hanging-scroll frame with a fuller scene, and the same figure type as the
other suits for each rank: withdrawn (First), attending (Second), acting (Third), engaged (Fourth),
ordinary (Fifth). The setting and props are those of Wind. Each card has at most one vermilion
accent besides the seal and rank emblems.

Helpers new to this module: wind_grass(), cloth(), balloon_sleeve(), fan(), chime(), kite(),
bent_smoke(), leaf(), scatter_leaves(), windwalker(), kinhin().
"""

import math

from .common import (GREY, INK, PALE, SCROLL_BOX, VERMILION, ZEN_PAPER, ZEN_VIGNETTE,
                     f, zen_pip_close, zen_pip_open, zen_rank_close, zen_rank_open)
from .zen_minor_earth import (STRAW, WOOD, _anchor, _arm, acting, attending, cushion, engaged,
                              floorboards, ordinary, place, withdrawn, _smoke)
from .zen_minor_fire import flame, lantern, oil_lamp
from .zen_minor_water import boat, ripple, shoji, stone_row, water
from .zen_transmission import GREYROBE, SKIN, ellipse, finish, head, path, tube
from .zen_way import grass, ground, hills, mist, rock, trunk

SX0, SY0, SX1, SY1 = SCROLL_BOX
SCX = (SX0 + SX1) / 2
VX0, VY0, VX1, VY1 = ZEN_VIGNETTE
VCX = (VX0 + VX1) / 2
FLOOR = 725
CLOTH, SAND, BAMBOO = "#ece6d6", "#d9d0b2", "#8a7a52"


# ------------------------------------------------------------ new helpers

def wind_grass(rng, x0, x1, y0, y1, n, hmin=20, hmax=50, dirn=1, bend=0.6):
    """Blades of grass bent by a steady wind: dirn is +1 (toward +x) or -1, bend 0 (upright) to 1 (flat)."""
    out = []
    for _ in range(n):
        gx, gy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        h = rng.uniform(hmin, hmax) * (0.75 + 0.5 * (gy - y0) / max(1, y1 - y0))
        b = min(0.95, max(0.05, bend * rng.uniform(0.8, 1.1)))
        tx, ty = gx + dirn * h * b, gy - h * (1 - b * 0.7)
        cx, cy = gx + dirn * h * b * 0.12, gy - h * 0.75 * (1 - b * 0.4)
        col = rng.choice([INK, GREY, GREY, PALE])
        out.append(path(f"M{f(gx)},{f(gy)} Q{f(cx)},{f(cy)} {f(tx)},{f(ty)}", stroke=col,
                        w=rng.uniform(0.7, 1.8), op=rng.uniform(0.5, 0.95)))
    return "".join(out)


def cloth(x0, x1, y, length, shift, amp=8, fill=CLOTH, n=3, phase=0, op=1.0):
    """A cloth hung from the line y between x0 and x1, blown sideways by `shift` at its lower edge,
    with a wavy hem (amp) and two fold lines. shift 0 hangs straight."""
    yb = y + length
    xs = [x1 + shift - (x1 - x0) * i / n for i in range(n + 1)]
    d = f"M{f(x0)},{f(y)} L{f(x1)},{f(y)} Q{f(x1 + shift * 0.2)},{f(y + length * 0.5)} {f(xs[0])},{f(yb)}"
    for i in range(n):
        d += f" Q{f((xs[i] + xs[i + 1]) / 2)},{f(yb + amp * (1 if (i + phase) % 2 else -1))} {f(xs[i + 1])},{f(yb)}"
    d += f" Q{f(x0 + shift * 0.2)},{f(y + length * 0.5)} {f(x0)},{f(y)} Z"
    out = [path(d, fill=fill, stroke=INK, w=2, op=op, filt="brush")]
    for k in range(1, 3):
        t = k / 3
        out.append(path(f"M{f(x0 + (x1 - x0) * t)},{f(y + 4)} Q{f(x0 + (x1 - x0) * t + shift * 0.3)},{f(y + length * 0.5)} "
                        f"{f(x0 + (x1 - x0) * t + shift * 0.9)},{f(yb - 3)}", stroke=GREY, w=1.2, op=0.6 * op))
    return "".join(out)


def balloon_sleeve(e, h, flare=24, side=1, fill=GREYROBE):
    """A wide sleeve filled with wind, drawn from the hand h back toward the elbow e (page coordinates);
    the cloth bulges to `side` (+1 right, -1 left) of the forearm."""
    dx, dy = e[0] - h[0], e[1] - h[1]
    n = math.hypot(dx, dy) or 1
    px, py = -dy / n * side, dx / n * side
    ex, ey = e[0] + dx * 0.25, e[1] + dy * 0.25
    mx, my = (h[0] + ex) / 2 + px * flare * 1.5, (h[1] + ey) / 2 + py * flare * 1.5
    d = (f"M{f(h[0] - px * 3)},{f(h[1] - py * 3)} Q{f(mx)},{f(my)} {f(ex + px * flare)},{f(ey + py * flare)} "
         f"Q{f(ex + px * flare * 0.5 + dx * 0.1)},{f(ey + py * flare * 0.5 + dy * 0.1 + 6)} {f(ex - px * 4)},{f(ey - py * 4)} "
         f"Q{f((h[0] + ex) / 2 - px * 2)},{f((h[1] + ey) / 2 - py * 2)} {f(h[0] - px * 3)},{f(h[1] - py * 3)} Z")
    folds = path(f"M{f(h[0] + px * 2)},{f(h[1] + py * 2)} Q{f(mx * 0.9 + (h[0] + ex) * 0.05)},{f(my * 0.9 + (h[1] + ey) * 0.05)} "
                 f"{f(ex + px * flare * 0.7)},{f(ey + py * flare * 0.7)}", stroke=GREY, w=1.2, op=0.7)
    return path(d, fill=fill, stroke=INK, w=2.2, filt="brush") + folds


def streamer(x, y, length, dirn=1, droop=0.0, w0=12, w1=3, fill=CLOTH, amp=5):
    """A strip of cloth (a sleeve end or hem) blown out from (x, y) toward dirn (+1 or -1), tapering
    from width w0 to w1, with a gentle wave and a droop at the free end."""
    up, dn = [], []
    for k in range(17):
        t = k / 16
        cx = x + dirn * length * t
        cy = y + droop * t * t + amp * math.sin(t * 6.0) * t
        hw = (w0 * (1 - t) + w1 * t) / 2
        up.append((cx, cy - hw))
        dn.append((cx, cy + hw))
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in up + dn[::-1]) + " Z"
    mid = "M" + " L".join(f"{f(a)},{f((b + c) / 2)}" for (a, b), (_, c) in list(zip(up, dn))[1:12])
    return path(d, fill=fill, stroke=INK, w=1.8, filt="brush") + path(mid, stroke=GREY, w=1.1, op=0.6)


def fan(x, y, r, rot=0.0, accent=False):
    """A round hand fan (uchiwa): pale disc with ribs and a bamboo handle; (x, y) is the disc centre."""
    o = [path(f"M{f(x)},{f(y + r * 0.9)} L{f(x)},{f(y + r * 1.9)}", stroke=INK, w=6.4),
         path(f"M{f(x)},{f(y + r * 0.9)} L{f(x)},{f(y + r * 1.9)}", stroke=BAMBOO, w=4),
         ellipse(x, y, r, r, "#efe7cf", stroke=INK, w=2.2)]
    for k in range(-2, 3):
        a = math.radians(90 + k * 17)
        o.append(path(f"M{f(x)},{f(y + r * 0.8)} L{f(x + r * 0.9 * math.cos(math.radians(270 + k * 20)))},{f(y + r * 0.9 * math.sin(math.radians(270 + k * 20)))}",
                      stroke=GREY, w=1.2, op=0.7))
    if accent:
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * 0.28)}" fill="{VERMILION}" opacity="0.9"/>')
    return f'<g transform="rotate({f(rot)} {f(x)} {f(y)})">{"".join(o)}</g>'


def chime(x, y, drop=26, swing=14, w=26):
    """A wind chime (furin) hung from (x, y): cord, a pale glass bell in outline, and a paper strip
    blown out sideways by `swing`."""
    by = y + drop
    o = [path(f"M{f(x)},{f(y)} L{f(x)},{f(by)}", stroke=INK, w=1.8),
         path(f"M{f(x - w / 2)},{f(by + w * 0.6)} Q{f(x - w / 2)},{f(by)} {f(x)},{f(by)} Q{f(x + w / 2)},{f(by)} {f(x + w / 2)},{f(by + w * 0.6)} Z",
              fill="#e9efee", stroke=INK, w=2, filt="brush"),
         path(f"M{f(x - w / 2 - 2)},{f(by + w * 0.6)} h{f(w + 4)}", stroke=INK, w=2.2),
         path(f"M{f(x)},{f(by + w * 0.3)} L{f(x + swing * 0.1)},{f(by + w * 0.9)}", stroke=GREY, w=1.2),
         path(f"M{f(x)},{f(by + w * 0.6)} Q{f(x + swing * 0.2)},{f(by + w * 1.2)} {f(x + swing * 0.5)},{f(by + w * 1.8)}", stroke=INK, w=1.6),
         path(f"M{f(x + swing * 0.5 - 4)},{f(by + w * 1.8)} L{f(x + swing * 0.5 + 4)},{f(by + w * 1.8 + 1)} "
              f"L{f(x + swing + 8)},{f(by + w * 2.8)} L{f(x + swing - 1)},{f(by + w * 2.9)} Z", fill=CLOTH, stroke=INK, w=1.5)]
    return "".join(o)


def kite(x, y, s=1.0, rot=0.0, col=VERMILION, tail=3):
    """A diamond kite centred at (x, y), tilted by rot degrees, with a bowed tail."""
    o = [path(f"M0,{f(-42 * s)} L{f(26 * s)},0 L0,{f(54 * s)} L{f(-26 * s)},0 Z", fill=col, stroke=INK, w=2, op=0.92),
         path(f"M0,{f(-42 * s)} L0,{f(54 * s)} M{f(-26 * s)},0 L{f(26 * s)},0", stroke=INK, w=1.2, op=0.7)]
    ty = 54 * s
    d = f"M0,{f(ty)}"
    for k in range(tail * 2):
        d += f" q{f((-9 if k % 2 else 9) * s)},{f(10 * s)} 0,{f(20 * s)}"
    o.append(path(d, stroke=INK, w=1.6))
    for k in range(tail):
        o.append(path(f"M{f(-7 * s)},{f(ty + 40 * s * k + 14 * s)} l{f(14 * s)},{f(5 * s)} l0,{f(-8 * s)} l{f(-14 * s)},{f(5 * s)} Z",
                      fill=col, stroke=INK, w=1.2))
    return f'<g transform="translate({f(x)},{f(y)}) rotate({f(rot)})">{"".join(o)}</g>'


def bent_smoke(x, y, h, bend, w=1.8, col=GREY, steps=24, wob=4):
    """A thread of smoke rising from (x, y) to height h, drifting by `bend` at the top, fading and
    fraying toward its end."""
    pts = []
    for k in range(steps + 1):
        t = k / steps
        pts.append((x + bend * t ** 2 + wob * math.sin(t * 7) * t, y - h * t))
    out = []
    for part, op in ((slice(0, 9), 0.9), (slice(8, 17), 0.65), (slice(16, 25), 0.4)):
        seg = pts[part]
        out.append(path("M" + " L".join(f"{f(a)},{f(b)}" for a, b in seg), stroke=col, w=w, op=op))
    ex, ey = pts[-1]
    for k in range(3):
        out.append(path(f"M{f(ex + 6 + k * 9)},{f(ey - 4 - k * 3)} q5,-3 10,1", stroke=col, w=w * 0.8, op=0.4 - k * 0.1))
    return "".join(out)


def leaf(x, y, ang=0.0, length=44, fill=VERMILION, op=1.0, veins=True, outline=INK):
    """A leaf hanging from the stalk end (x, y) (the leaf extends downward, rotated by ang degrees),
    with serrated edge, midrib and side veins."""
    L = length
    o = [path(f"M0,0 C{f(L * 0.55)},{f(L * 0.2)} {f(L * 0.5)},{f(L * 0.75)} 0,{f(L)} C{f(-L * 0.5)},{f(L * 0.75)} {f(-L * 0.55)},{f(L * 0.2)} 0,0 Z",
              fill=fill, stroke=outline, w=1.8, op=op)]
    if veins:
        o.append(path(f"M0,{f(-L * 0.18)} L0,{f(L * 0.96)}", stroke=outline, w=1.6, op=0.9 * op))
        for k in range(1, 6):
            yy = L * (0.1 + 0.15 * k)
            o.append(path(f"M0,{f(yy + 4)} L{f(L * 0.22)},{f(yy - 5)} M0,{f(yy + 4)} L{f(-L * 0.22)},{f(yy - 5)}", stroke=outline, w=1.0, op=0.7 * op))
    return f'<g transform="translate({f(x)},{f(y)}) rotate({f(ang)})">{"".join(o)}</g>'


def scatter_leaves(rng, pts, size=(5, 9), cols=(GREY, PALE, INK), op=(0.5, 0.85)):
    """Small dry leaves lying or flying at the given points, each turned a different way."""
    out = []
    for lx, ly in pts:
        sz = rng.uniform(*size)
        out.append(f'<path d="M0,0 l{f(sz)},{f(-sz * 0.4)} l{f(-sz * 0.3)},{f(sz)} z" fill="{rng.choice(cols)}" '
                   f'opacity="{rng.uniform(*op):.2f}" transform="translate({f(lx)},{f(ly)}) rotate({rng.uniform(0, 360):.0f})"/>')
    return "".join(out)


def windwalker(x, y, s=1.0, flip=False, mode="gale", robe=GREYROBE):
    """A walking figure facing +x, origin on the ground, about 105 units high.
    mode "gale": leaning into a headwind, robe hem and sleeve streaming back, one hand on a straw hat;
    "breeze": upright, a flute held loosely in one hand, the other sleeve lifted forward;
    "speak": upright with a staff and a gourd, the free hand open in speech, hem lifting forward.
    Returns (svg, anchors)."""
    o = []
    if mode == "gale":
        o.append(path("M0,-42 L22,-24 L30,0 M-2,-42 L-16,-22 L-28,-2", w=3.4))
        o.append(path("M26,0 h12 M-32,-2 h-10", w=3))
        o.append(path("M6,-80 Q-18,-80 -44,-92 L-36,-80 L-54,-76 L-36,-68 Q-18,-66 4,-70 Z", fill=robe, stroke=INK, w=2, filt="brush"))
        o.append(path("M-4,-88 Q14,-92 24,-82 L20,-54 L15,-32 Q-14,-30 -60,-42 L-44,-36 L-64,-28 L-44,-22 L-58,-12 "
                      "Q-30,-14 -8,-18 L-14,-60 Z", fill=robe, stroke=INK, w=2.4, filt="brush"))
        o.append(path("M-14,-52 Q4,-50 20,-52", w=2.2, stroke=GREY))
        o.append(head(20, -100, 10.5, look=1, hair=False, bowed=True))
        o.append(path("M2,-107 Q22,-140 48,-106 Q26,-100 2,-107 Z", fill=STRAW, stroke=INK, w=2.2))
        o.append(_arm((16, -84), (40, -94), (30, -110), SKIN, 4.6))
        hand = (30, -110)
    else:
        o.append(path("M0,-44 L10,-22 L14,0 M-2,-44 L-12,-22 L-18,0", w=3.4))
        o.append(path("M10,0 h10 M-22,0 h-8", w=3) if mode == "breeze" else path("M10,0 h8 M-22,0 h-6", w=2))
        if mode == "speak":
            o.append(path("M24,0 L26,-128", stroke=INK, w=6.4))
            o.append(path("M24,0 L26,-128", stroke="#6b5a45", w=4))
        o.append(path("M-14,-84 Q0,-90 14,-84 L18,-36 L-20,-34 Z", fill=robe, stroke=INK, w=2.4, filt="brush"))
        o.append(path("M18,-36 Q30,-36 38,-42 Q34,-32 18,-28 Z", fill=robe, stroke=INK, w=2, filt="brush"))
        o.append(path("M-18,-56 L18,-58", w=2.2, stroke=GREY))
        if mode == "breeze":
            o.append(tube("M-6,-80 Q-10,-64 -8,-50", 5.5, robe))
            o.append(path("M26,-62 Q34,-74 46,-70 Q40,-62 30,-52 Z", fill=robe, stroke=INK, w=1.8, filt="brush"))
            o.append(_arm((8, -80), (22, -66), (30, -54), SKIN, 4.6))
            o.append(path("M16,-52 L70,-62", stroke=INK, w=4.6))
            o.append(path("M16,-52 L70,-62", stroke=BAMBOO, w=2.6))
            o.append(head(2, -98, 10.5, look=1, hair=False))
            hand = (30, -54)
        else:
            o.append(_arm((-4, -80), (8, -64), (24, -62), SKIN, 4.6))
            o.append(path("M26,-124 L40,-122", stroke=INK, w=1.8))
            o.append(ellipse(41, -116, 5, 6, STRAW, stroke=INK, w=1.6))
            o.append(ellipse(41, -102, 9.5, 11, STRAW, stroke=INK, w=1.8))
            o.append(_arm((8, -82), (28, -84), (46, -96), SKIN, 4.6))
            o.append(head(4, -98, 10.5, look=1, hair=False, mouth="open"))
            hand = (46, -96)
    return place(x, y, s, flip, "".join(o)), {"hand": _anchor(x, y, s, flip, hand)}


def kinhin(x, y, s=1.0, flip=False, robe=GREYROBE):
    """A monk walking slowly, facing +x, hands folded at the chest, head a little bowed. Origin on the ground."""
    o = [path("M-6,-10 L-8,0 M8,-10 L16,0", w=3.2), path("M-12,0 h-4 M14,0 h10", w=3),
         path("M-13,-84 Q0,-90 13,-84 L19,-8 L-19,-8 Z", fill=robe, stroke=INK, w=2.4, filt="brush"),
         path("M-17,-50 L17,-52", w=2.2, stroke=GREY),
         path("M-6,-8 Q0,-4 6,-8", w=1.6, stroke=GREY),
         tube("M-9,-80 Q-12,-62 6,-68", 5, robe), tube("M9,-80 Q14,-62 2,-68", 5, robe),
         ellipse(4, -68, 5, 4, SKIN, stroke=INK, w=1.4),
         head(2, -98, 10.5, look=1, hair=False, bowed=True)]
    return place(x, y, s, flip, "".join(o)), {"hand": _anchor(x, y, s, flip, (4, -68))}


def _pole(x, y0, y1, w=7, col="#6b5a45"):
    return path(f"M{f(x)},{f(y0)} L{f(x + 2)},{f(y1)}", stroke=INK, w=w + 2) + path(f"M{f(x)},{f(y0)} L{f(x + 2)},{f(y1)}", stroke=col, w=w)


def _needles(rng, x, y, n, r, tilt=0.5, col=INK):
    """A fan of fine pine needles from (x, y), swept toward +x by the wind (tilt)."""
    out = []
    for _ in range(n):
        a = math.radians(rng.uniform(-170, -10))
        ln = r * rng.uniform(0.55, 1.0)
        ex, ey = x + math.cos(a) * ln + tilt * ln * 0.6, y + math.sin(a) * ln * 0.8
        out.append(path(f"M{f(x)},{f(y)} L{f(ex)},{f(ey)}", stroke=rng.choice([col, GREY]), w=rng.uniform(0.7, 1.1), op=rng.uniform(0.55, 0.95)))
    return "".join(out)


def _basket(x, y, w, h):
    return (path(f"M{f(x - w / 2)},{f(y - h)} L{f(x + w / 2)},{f(y - h)} L{f(x + w * 0.4)},{f(y)} L{f(x - w * 0.4)},{f(y)} Z",
                 fill=STRAW, stroke=INK, w=2.2, filt="brush")
            + path(f"M{f(x - w * 0.46)},{f(y - h * 0.66)} h{f(w * 0.92)} M{f(x - w * 0.43)},{f(y - h * 0.33)} h{f(w * 0.86)}", stroke=GREY, w=1.2, op=0.7)
            + ellipse(x, y - h, w / 2, w * 0.08, "#c9bd98", stroke=INK, w=1.8))


# ------------------------------------------------------------ pips wi01-wi10

def wi01(rng):
    """One of Wind: a figure seen from behind on a cushion at dusk beside an open door; the breath rises as a thin vapour that frays toward the trees outside."""
    o = [zen_pip_open("wind", 1), floorboards(FLOOR - 30, FLOOR + 40, VCX - 170, VCX + 170)]
    # the open door at the right, trees beyond in wash
    dx0, dx1, dt = VCX + 70, VCX + 190, FLOOR - 250
    o.append(path(f"M{dx0},{dt} L{dx1},{dt} L{dx1},{FLOOR - 28} L{dx0},{FLOOR - 28} Z", fill="#d9d3c6", stroke=None, op=0.55, filt="softwash"))
    for tx, th in ((dx0 + 26, 150), (dx0 + 66, 190), (dx0 + 102, 130)):
        o.append(path(f"M{tx},{FLOOR - 30} Q{tx + 3},{FLOOR - 30 - th / 2} {tx},{FLOOR - 30 - th}", stroke=GREY, w=5, op=0.55, filt="dry"))
        o.append(ellipse(tx + 8, FLOOR - 30 - th, 22, 30, GREY, op=0.28, filt="wash"))
    o.append(path(f"M{dx0},{FLOOR - 28} L{dx0},{dt} L{dx1},{dt} L{dx1},{FLOOR - 28}", stroke=INK, w=6, filt="brush"))
    cx = VCX - 70
    o.append(cushion(cx, FLOOR + 6, 150, col="#b3ad9f"))
    fig, a = withdrawn(cx, FLOOR - 34, 2.2, view="back", robe="#9c968a")
    o.append(fig)
    hx, hy = a["head"]
    o.append(bent_smoke(hx + 20, hy - 24, 70, 190, 2.8, col=INK, wob=6))
    o.append(bent_smoke(hx + 26, hy - 18, 54, 150, 2.2, wob=5))
    o.append(bent_smoke(hx + 14, hy - 30, 90, 150, 1.8, wob=7))
    return finish(o + [zen_pip_close()])


def wi02(rng):
    """Two of Wind: an open hand held before a paper window where a lamp flame leans and recovers; bamboo shadows sway on the paper."""
    o = [zen_pip_open("wind", 2), floorboards(FLOOR - 24, FLOOR + 44, VCX - 190, VCX + 190)]
    x0, y0, x1, y1 = VCX - 50, FLOOR - 205, VCX + 125, FLOOR - 24
    o.append(shoji(x0, y0, x1, y1, cols=3, rows=5))
    cid = "wi02win"
    sh = [f'<clipPath id="{cid}"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/></clipPath><g clip-path="url(#{cid})">']
    for bx, lean in ((x0 + 60, 26), (x0 + 112, -22), (x0 + 160, 30)):
        sh.append(path(f"M{bx},{y1 + 10} Q{bx + lean * 0.3},{(y0 + y1) / 2} {bx + lean},{y0 - 10}", stroke=GREY, w=5, op=0.4))
        for k in range(1, 4):
            ny = y1 - k * 44
            nx = bx + lean * (y1 - ny) / (y1 - y0 + 20)
            sh.append(path(f"M{f(nx - 4)},{f(ny)} h8", stroke=GREY, w=2, op=0.5))
            for sgn in (-1, 1):
                sh.append(path(f"M{f(nx)},{f(ny)} q{f(sgn * 16 + lean * 0.5)},{f(-4)} {f(sgn * 34 + lean)},{f(-14 + k)}", stroke=GREY, w=1.6, op=0.45))
    sh.append("</g>")
    o.append("".join(sh))
    o.append(path(f"M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z", stroke=INK, w=2.4, op=0.9))
    lx, ly, ls = VCX - 4, FLOOR + 8, 1.9
    o.append(oil_lamp(lx, ly, ls, lit=False))
    fx, fy = lx + 24 * ls, ly - 48 * ls
    o.append(ellipse(fx + 6, fy - 14, 44, 42, "#fff4d6", op=0.55, filt="wash"))
    o.append(flame(fx - 10, fy, 12, bend=-18, col=PALE))
    o.append(flame(fx, fy, 12, bend=18))
    # the open hand, held toward the flame
    hx, hy = VCX - 92, FLOOR - 86
    arm = f"M{VX0 - 70},{hy + 52} Q{VX0 + 40},{hy + 30} {hx},{hy}"  # enters from the circle's edge
    o.append(path(arm, stroke=INK, w=26))
    o.append(path(arm, stroke=GREYROBE, w=22))
    o.append(path(f"M{hx - 20},{hy - 12} l-6,24", stroke=INK, w=2.2))
    for k in range(4):
        o.append(tube(f"M{hx + 4},{hy - 8 + k * 6} l{18 + (k % 2) * 3},{-6 + k * 1.5}", 4.4, SKIN))
    o.append(tube(f"M{hx + 2},{hy + 8} l14,10", 4.6, SKIN))
    o.append(ellipse(hx + 2, hy + 1, 10, 13, SKIN, stroke=INK, w=1.8))
    return finish(o + [zen_pip_close()])


def wi03(rng):
    """Three of Wind: a bare winter branch, one leaf turning on its stalk in a gust; mountains behind as pale wash. Only the leaf is drawn in detail."""
    o = [zen_pip_open("wind", 3)]
    o.append(hills(rng, [(FLOOR - 40, 70, PALE, 0.3, 90), (FLOOR - 4, 40, PALE, 0.22, 70)], VX0 + 10, VX1 - 10))
    o.append(ground(FLOOR + 20, VX0 + 20, VX1 - 20, op=0.1))
    p0, c1, c2 = (VX0 - 10, FLOOR - 160), (VCX - 120, FLOOR - 210), (VCX - 20, FLOOR - 150)
    bx, by = VCX + 70, FLOOR - 190

    def bez(t):
        u = 1 - t
        return (u ** 3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * bx,
                u ** 3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * by)
    br = f"M{p0[0]},{p0[1]} C{c1[0]},{c1[1]} {c2[0]},{c2[1]} {bx},{by}"
    o.append(path(br, stroke=INK, w=9, filt="dry"))
    o.append(path(br, stroke=INK, w=4))
    for t, dx, dy in ((0.22, 26, -62), (0.42, 38, -60), (0.6, 20, 52), (0.78, 28, -66)):
        tx, ty = bez(t)
        ex, ey = tx + dx, ty + dy
        o.append(path(f"M{f(tx)},{f(ty)} Q{f(tx + dx * 0.3 - 4)},{f(ty + dy * 0.6)} {f(ex)},{f(ey)}", stroke=INK, w=3, filt="brush"))
        o.append(path(f"M{f(ex)},{f(ey)} l{f(dx * 0.3)},{f(dy * 0.3)}", stroke=INK, w=1.8))
    o.append(path(f"M{bx},{by} Q{bx + 10},{by + 16} {bx + 6},{by + 34}", stroke=INK, w=2.4))
    sx, sy = bx + 6, by + 34
    o.append(leaf(sx, sy, -75, 46, fill="none", op=0.4, veins=False, outline=GREY))
    o.append(leaf(sx, sy, 70, 46, fill="none", op=0.4, veins=False, outline=GREY))
    o.append(leaf(sx, sy, 10, 52))
    return finish(o + [zen_pip_close()])


def wi04(rng):
    """Four of Wind: a figure leaning into a hard crosswind on a ridge, robe pressed flat, one hand clutching a hat; the grass lies almost horizontal."""
    o = [zen_pip_open("wind", 4)]
    o.append(hills(rng, [(FLOOR - 70, 50, PALE, 0.28, 100)], VX0 + 10, VX1 - 10))
    o.append(ground(FLOOR, VX0 + 6, VX1 - 6, op=0.2))
    fig, _ = windwalker(VCX + 10, FLOOR - 2, 2.0, mode="gale")
    o.append(fig)
    o.append(wind_grass(rng, VX0 + 8, VX1 - 8, FLOOR - 4, FLOOR + 44, 70, 24, 52, dirn=-1, bend=0.85))
    return finish(o + [zen_pip_close()])


def wi05(rng):
    """Five of Wind: a line of monks walking slowly in a corridor, hands folded at the chest; light through slatted windows lies on the floorboards; one sandal at the far end."""
    o = [zen_pip_open("wind", 5), floorboards(FLOOR - 40, FLOOR + 50, VCX - 190, VCX + 190, rows=5, col="#a79e8f")]
    wy0, wy1 = FLOOR - 215, FLOOR - 40
    o.append(path(f"M{VX0 + 6},{wy0} L{VX1 - 6},{wy0} L{VX1 - 6},{wy1} L{VX0 + 6},{wy1} Z", fill=GREY, stroke=None, op=0.2, filt="softwash"))
    o.append(path(f"M{VX0 + 6},{wy0} L{VX1 - 6},{wy0}", stroke=INK, w=4, op=0.7, filt="brush"))
    for k in range(3):  # slatted windows
        wx = VX0 + 30 + k * 125
        o.append(path(f"M{wx},{wy0 + 22} L{wx + 82},{wy0 + 22} L{wx + 82},{wy0 + 82} L{wx},{wy0 + 82} Z", fill="#f3eddc", stroke=INK, w=2.2, filt="brush"))
        for j in range(1, 6):
            o.append(path(f"M{wx + j * 82 / 6:.0f},{wy0 + 22} l0,60", stroke=INK, w=1.6, op=0.8))
        o.append(path(f"M{wx + 4},{wy0 + 84} L{wx + 86},{wy0 + 84} L{wx + 128},{FLOOR + 32} L{wx + 44},{FLOOR + 32} Z", fill="#fff4d6", stroke=None, op=0.4, filt="softwash"))
    for k, (mx, my, ms) in enumerate(((VCX - 110, FLOOR + 22, 1.85), (VCX - 8, FLOOR + 8, 1.6), (VCX + 80, FLOOR - 4, 1.4))):
        fig, _ = kinhin(mx, my, ms, robe=("#b3ad9f", "#a9a398", "#b8b2a6")[k])
        o.append(fig)
    sx, sy = VX1 - 36, FLOOR - 8
    o.append(path(f"M{sx},{sy} q2,-10 11,-11 q2,9 -11,11 Z", fill=STRAW, stroke=INK, w=1.6))
    return finish(o + [zen_pip_close()])


def wi06(rng):
    """Six of Wind: a traveller on a straight, empty country road at evening, a flute loose in one hand, sleeves lifted by a breeze; the reeds along the verge bend the way he walks."""
    o = [zen_pip_open("wind", 6)]
    hy = FLOOR - 120
    o.append(ellipse(VCX + 20, hy - 4, 44, 44, "#f6e2c4", op=0.8, filt="wash"))
    o.append(hills(rng, [(hy + 8, 28, PALE, 0.3, 80)], VX0 + 6, VX1 - 6))
    o.append(path(f"M{VCX - 4},{hy + 10} L{VCX + 150},{FLOOR + 50} L{VCX - 170},{FLOOR + 50} Z", fill="#cfc6b6", stroke=None, op=0.5, filt="softwash"))
    o.append(path(f"M{VCX - 4},{hy + 10} L{VCX - 170},{FLOOR + 50} M{VCX - 4},{hy + 10} L{VCX + 150},{FLOOR + 50}", stroke=GREY, w=1.6, op=0.6, filt="brush"))
    for side in (-1, 1):  # reeds on both verges, all bent to +x
        for _ in range(16):
            rx = VCX + side * rng.uniform(95, 200)
            ry = rng.uniform(hy + 80, FLOOR + 40)
            h = rng.uniform(40, 90) * (0.5 + (ry - hy) / 300)
            tx, ty = rx + h * 0.55, ry - h * 0.8
            o.append(path(f"M{f(rx)},{f(ry)} Q{f(rx + h * 0.05)},{f(ry - h * 0.7)} {f(tx)},{f(ty)}", stroke=INK if rng.random() < 0.4 else GREY, w=1.3, op=0.8))
            o.append(path(f"M{f(tx)},{f(ty)} l{f(h * 0.12)},{f(h * 0.06)}", stroke=INK, w=3.2, op=0.7))
    fig, _ = windwalker(VCX - 20, FLOOR + 36, 2.5, mode="breeze")
    o.append(fig)
    return finish(o + [zen_pip_close()])


def wi07(rng):
    """Seven of Wind: a figure seated on a veranda cushion facing the garden, eyes half open; counting beads set aside on the boards, a paper screen bellying and a chime swinging in the breeze."""
    o = [zen_pip_open("wind", 7)]
    o.append(path(f"M{VX0 + 6},{FLOOR - 4} Q{VCX},{FLOOR - 10} {VX1 - 6},{FLOOR - 4} L{VX1 - 6},{FLOOR + 40} L{VX0 + 6},{FLOOR + 40} Z", fill=WOOD, stroke=INK, w=2.2, op=0.45, filt="brush"))
    for k in range(1, 4):
        o.append(path(f"M{VX0 + 6},{FLOOR - 4 + k * 11} Q{VCX},{FLOOR - 10 + k * 11} {VX1 - 6},{FLOOR - 4 + k * 11}", stroke=GREY, w=1.1, op=0.5))
    # eave beam and wind chime
    o.append(path(f"M{VX0 + 36},{FLOOR - 224} L{VX1 - 36},{FLOOR - 224}", stroke=INK, w=7, op=0.85, filt="brush"))
    o.append(chime(VCX + 110, FLOOR - 221, 24, 16))
    # the screen at the left, one panel bowed outward by the wind
    sx0, sx1, st, sb = VX0 + 30, VCX - 70, FLOOR - 214, FLOOR - 10
    o.append(shoji(sx0, st, sx0 + 56, sb, cols=2, rows=5))
    o.append(path(f"M{sx0 + 56},{st} L{sx1},{st} Q{sx1 + 22},{(st + sb) / 2} {sx1},{sb} L{sx0 + 56},{sb} Z", fill="#f3eddc", stroke=INK, w=2.4, filt="brush"))
    for j in range(1, 5):
        yy = st + (sb - st) * j / 5
        o.append(path(f"M{sx0 + 56},{yy} Q{(sx0 + 56 + sx1) / 2 + 8},{yy + 3} {sx1 + 8},{yy}", stroke=INK, w=1.3, op=0.65))
    # the garden beyond, at the right
    o.append(hills(rng, [(FLOOR - 70, 40, PALE, 0.25, 70)], VCX + 20, VX1 - 6))
    o.append(wind_grass(rng, VCX + 140, VX1 - 10, FLOOR - 12, FLOOR + 10, 22, 22, 44, dirn=1, bend=0.5))
    o.append(cushion(VCX + 20, FLOOR + 10, 124, col="#b3ad9f"))
    fig, _ = withdrawn(VCX + 20, FLOOR - 30, 1.9, view="side", eyes_closed=False, robe="#9c968a")
    o.append(fig)
    # beads laid in a loose ring on the boards
    bx, by = VCX - 70, FLOOR + 24
    for k in range(14):
        a = 2 * math.pi * k / 14
        o.append(f'<circle cx="{f(bx + 30 * math.cos(a))}" cy="{f(by + 7 * math.sin(a))}" r="3.6" fill="{SAND}" stroke="{INK}" stroke-width="1.3"/>')
    return finish(o + [zen_pip_close()])


def wi08(rng):
    """Eight of Wind: a wide pale sky, a layer of wash with a bird-shaped gap in it, and one faint ring of brush; no figure."""
    o = [zen_pip_open("wind", 8)]
    o.append(path(f"M{VX0 + 6},{FLOOR - 112} Q{VCX},{FLOOR - 126} {VX1 - 6},{FLOOR - 110} L{VX1 - 6},{FLOOR - 36} Q{VCX},{FLOOR - 26} {VX0 + 6},{FLOOR - 38} Z",
                  fill=GREY, stroke=None, op=0.24, filt="softwash"))
    bx, by = VCX + 100, FLOOR - 76
    o.append(path(f"M{bx - 44},{by + 2} Q{bx - 22},{by - 24} {bx},{by - 4} Q{bx + 22},{by - 24} {bx + 44},{by + 2} "
                  f"Q{bx + 22},{by - 8} {bx},{by + 8} Q{bx - 22},{by - 8} {bx - 44},{by + 2} Z", fill=ZEN_PAPER, stroke=None))
    o.append(path(f"M{VX0 + 6},{FLOOR + 10} Q{VCX},{FLOOR + 4} {VX1 - 6},{FLOOR + 10}", stroke=GREY, w=1.6, op=0.55, filt="brush"))
    cx, cy, r = VCX - 10, FLOOR - 190, 50
    a0, a1 = math.radians(-60), math.radians(280)
    o.append(path(f"M{f(cx + r * math.cos(a0))},{f(cy + r * math.sin(a0))} A{r},{r} 0 1 1 {f(cx + r * math.cos(a1))},{f(cy + r * math.sin(a1))}",
                  stroke=INK, w=6, op=0.45, filt="dry"))
    return finish(o + [zen_pip_close()])


def wi09(rng):
    """Nine of Wind: pines on a hillside drawn in fine needle strokes, mist threading the lower trunks, a small stone lantern unlit at the edge; no figure."""
    o = [zen_pip_open("wind", 9)]
    o.append(ground(FLOOR + 14, VX0 + 6, VX1 - 6, op=0.16))
    trees = [(VCX - 60, 150, 14, 0.4, 112), (VCX + 70, 140, 12, 0.5, 120), (VCX + 170, 120, 9, 0.5, 90), (VCX - 150, 100, 8, 0.4, 80), (VCX + 10, 90, 7, 0.3, 66)]
    for tx, th, tw, lean, cr in sorted(trees, key=lambda t: t[1]):
        by = FLOOR + 14 - (140 - th) * 0.15
        top = by - th * 1.6
        o.append(path(f"M{tx},{by} C{tx - 10},{by - th * 0.5} {tx + 12},{by - th * 0.9} {tx + lean * 10},{top}", stroke=INK, w=tw, filt="dry"))
        for k in range(3):
            ky = top + 14 + k * th * 0.28
            kx = tx + lean * 10 * (1 - (ky - top) / (by - top)) + (-1) ** k * 6
            tip = (kx + (-1) ** k * th * 0.4, ky - 12)
            o.append(path(f"M{f(kx)},{f(ky + 8)} Q{f((kx + tip[0]) / 2)},{f(ky - 4)} {f(tip[0])},{f(tip[1])}", stroke=INK, w=tw * 0.22, op=0.8))
            o.append(_needles(rng, tip[0], tip[1], 48, cr * 0.38, 0.6))
        o.append(_needles(rng, tx + lean * 10, top, 40, cr * 0.36, 0.6))
    for k, (mx, my, mw) in enumerate(((VCX + 20, FLOOR - 40, 230), (VCX - 30, FLOOR - 4, 220), (VCX + 120, FLOOR - 78, 140))):
        # a faint grey band behind, then paper-white mist over it, so the mist reads against the trunks
        o.append(ellipse(mx, my + 10, mw * 1.05, 30, "#cfc9bc", op=0.45, filt="mist"))
        o.append(mist(mx, my, mw, 26, 0.95))
    # the stone lantern, unlit
    lx, ly = VX0 + 50, FLOOR + 22
    st = "#b9b3a6"
    o.append(path(f"M{lx - 22},{ly} L{lx + 22},{ly} L{lx + 18},{ly - 10} L{lx - 18},{ly - 10} Z", fill=st, stroke=INK, w=2, filt="brush"))
    o.append(path(f"M{lx - 7},{ly - 10} L{lx + 7},{ly - 10} L{lx + 6},{ly - 58} L{lx - 6},{ly - 58} Z", fill=st, stroke=INK, w=2, filt="brush"))
    o.append(path(f"M{lx - 22},{ly - 58} L{lx + 22},{ly - 58} L{lx + 20},{ly - 66} L{lx - 20},{ly - 66} Z", fill=st, stroke=INK, w=2))
    o.append(path(f"M{lx - 16},{ly - 66} L{lx + 16},{ly - 66} L{lx + 16},{ly - 92} L{lx - 16},{ly - 92} Z", fill=st, stroke=INK, w=2, filt="brush"))
    o.append(path(f"M{lx - 8},{ly - 72} L{lx + 8},{ly - 72} L{lx + 8},{ly - 86} L{lx - 8},{ly - 86} Z", fill="#8a867e", stroke=INK, w=1.4))
    o.append(path(f"M{lx - 30},{ly - 92} L{lx + 30},{ly - 92} L{lx + 18},{ly - 108} L{lx - 18},{ly - 108} Z", fill=st, stroke=INK, w=2, filt="brush"))
    o.append(f'<circle cx="{lx}" cy="{ly - 113}" r="4.5" fill="{st}" stroke="{INK}" stroke-width="1.8"/>')
    return finish(o + [zen_pip_close()])


def wi10(rng):
    """Ten of Wind: a narrow market street under cloth awnings that billow in a gust; a barefoot traveller with a gourd on his staff speaks to a laughing fishmonger; lanterns and baskets at the edges."""
    o = [zen_pip_open("wind", 10), ground(FLOOR + 6, VX0 + 6, VX1 - 6, op=0.18)]
    ay = FLOOR - 212
    o.append(path(f"M{VX0 + 22},{ay} Q{VCX},{ay + 8} {VX1 - 22},{ay - 2}", stroke=INK, w=3.2, op=0.8))
    for i, (a, b) in enumerate(((VX0 + 22, VX0 + 128), (VX0 + 128, VX0 + 250), (VX0 + 250, VX0 + 372))):
        o.append(cloth(a, b, ay + 2, 34 + (i % 2) * 8, 22, amp=9, fill=("#ece6d6", "#dcd5c4", "#e9e3d6")[i], n=3, phase=i))
    o.append(_pole(VX0 + 22, ay - 6, FLOOR + 8, 6))
    o.append(_pole(VX0 + 372, ay - 6, FLOOR + 8, 6))
    # lanterns at the edges, unlit
    o.append(path(f"M{VX0 + 372},{ay + 6} l0,18", stroke=INK, w=1.6))
    o.append(lantern(VX0 + 372, ay + 24, 30, 40, lit=False))
    o.append(lantern(VX0 + 56, ay + 54, 24, 32, lit=False))
    # baskets at the left edge
    o.append(_basket(VX0 + 50, FLOOR + 10, 62, 44))
    o.append(_basket(VX0 + 104, FLOOR + 12, 46, 34))
    # the fishmonger's board with fish, and the fishmonger
    o.append(path(f"M{VCX + 56},{FLOOR - 40} L{VX1 - 16},{FLOOR - 40} L{VX1 - 22},{FLOOR - 28} L{VCX + 62},{FLOOR - 28} Z", fill=WOOD, stroke=INK, w=2.2, filt="brush"))
    o.append(path(f"M{VCX + 70},{FLOOR - 28} L{VCX + 66},{FLOOR + 10} M{VX1 - 34},{FLOOR - 28} L{VX1 - 30},{FLOOR + 10}", w=3.4))
    fm, _ = ordinary(VX1 - 40, FLOOR - 2, 1.5, flip=True, tool=None, robe="#a9a398")
    o.append(fm)
    mx, my = VX1 - 40 - 21 * 1.5, FLOOR - 2 - 74 * 1.5
    o.append(ellipse(mx, my, 3.6, 3.2, INK))
    for k in range(3):
        fx = VCX + 86 + k * 34
        o.append(path(f"M{fx},{FLOOR - 42} q12,-8 24,0 q-12,8 -24,0 Z M{fx + 24},{FLOOR - 42} l8,-6 l0,12 z", fill="#cfc9bc", stroke=INK, w=1.5))
    fig, _ = windwalker(VCX - 30, FLOOR - 2, 1.55, mode="speak")
    o.append(fig)
    return finish(o + [zen_pip_close()])


# ------------------------------------------------------------ ranks wi11-wi15

def wi11(rng):
    """First Rank of Wind: a monk sitting in a courtyard on a windless day, hands in the lap, face turned away; the gravel unmarked, a banner hanging straight, incense smoke in an unbroken column (its ember the one accent)."""
    o = [zen_rank_open("wind", 1)]
    base = SY1 - 170
    wy = base - 190
    o.append(mist(SCX, base - 560, 330, 40, 0.5))
    # a temple hall in pale wash behind the courtyard wall
    o.append(path(f"M{SX0 + 30},{wy - 100} Q{SX0 + 100},{wy - 120} {SX0 + 130},{wy - 190} L{SX1 - 130},{wy - 190} Q{SX1 - 100},{wy - 120} {SX1 - 30},{wy - 100} Z",
                  fill=GREY, stroke=None, op=0.2, filt="softwash"))
    o.append(path(f"M{SX0 + 24},{wy - 98} Q{SX0 + 100},{wy - 120} {SX0 + 130},{wy - 190} L{SX1 - 130},{wy - 190} Q{SX1 - 100},{wy - 120} {SX1 - 24},{wy - 98}",
                  stroke=INK, w=3, op=0.55, filt="brush"))
    o.append(path(f"M{SX0 + 40},{wy - 96} L{SX1 - 40},{wy - 96} L{SX1 - 40},{wy} L{SX0 + 40},{wy} Z", fill="#d8d2c6", stroke=None, op=0.4, filt="softwash"))
    for px in (SX0 + 80, SX0 + 190, SX1 - 190, SX1 - 110):
        o.append(path(f"M{px},{wy - 96} L{px},{wy}", stroke=INK, w=6, op=0.45, filt="dry"))
    o.append(path(f"M{SX0},{wy + 4} L{SX1},{wy + 4}", stroke=GREY, w=1.8, op=0.6, filt="brush"))
    # a banner on a pole at the right, hanging straight down
    px = SX1 - 64
    o.append(_pole(px, base - 20, wy - 250, 7))
    o.append(path(f"M{px - 42},{wy - 242} L{px + 44},{wy - 242}", stroke=INK, w=4))
    o.append(cloth(px - 36, px + 36, wy - 240, 190, 0, amp=2, fill="#e4ded0"))
    # a bare tree at the left, its twigs still
    o.append(trunk(rng, SX0 + 70, base - 10, base - 360, 16, 6, leafy=3))
    o.append(ground(base - 40, SX0, SX1, op=0.2))
    for _ in range(190):  # gravel, unmarked
        gx, gy = rng.uniform(SX0 + 8, SX1 - 8), rng.uniform(base - 20, base + 200)
        o.append(f'<circle cx="{f(gx)}" cy="{f(gy)}" r="{rng.uniform(0.8, 1.8):.1f}" fill="{GREY}" opacity="{rng.uniform(0.3, 0.6):.2f}"/>')
    fig, _ = withdrawn(SCX + 60, base + 70, 3.4, view="side", robe="#b3ad9f")
    o.append(fig)
    ix, iy = SCX - 130, base + 100
    o.append(ellipse(ix, iy, 24, 7, "#cfc9bc", stroke=INK, w=2))
    o.append(path(f"M{ix},{iy - 2} L{ix},{iy - 30}", stroke=INK, w=2.6))
    o.append(path(f"M{ix},{iy - 2} L{ix},{iy - 30}", stroke=STRAW, w=1.2))
    o.append(f'<circle cx="{ix}" cy="{iy - 32}" r="3.4" fill="{VERMILION}"/>')
    o.append(_smoke(ix, iy - 36, 360, 0, PALE, 1.3))
    return finish(o + [zen_rank_close()])


def wi12(rng):
    """Second Rank of Wind: a woman kneeling to sweep fallen leaves from a temple path in a light breeze; some leaves lift behind the broom and settle again (one red leaf, the accent)."""
    o = [zen_rank_open("wind", 2)]
    base = SY1 - 290
    o.append(mist(SCX, base - 520, 330, 40, 0.5))
    o.append(path(f"M{SX0},{base - 240} L{SX1},{base - 240} L{SX1},{base - 60} L{SX0},{base - 60} Z", fill="#d8d2c6", stroke=None, op=0.35, filt="softwash"))
    o.append(path(f"M{SX0},{base - 242} L{SX1},{base - 242}", stroke=INK, w=5, op=0.6, filt="brush"))
    for px in (SX0 + 50, SX0 + 230):
        o.append(path(f"M{px},{base - 240} L{px + 2},{base - 60}", stroke=INK, w=6, op=0.5, filt="dry"))
    # a maple at the right, its boughs and leaves all leaning with the breeze
    o.append(trunk(rng, SX1 - 80, base - 40, base - 440, 18, 24, leafy=3))
    o.append(ground(base - 60, SX0, SX1, op=0.2))
    for k, (sx0, sy0, sw, sh) in enumerate(((SX0 + 20, base - 40, 120, 40), (SX0 + 160, base - 42, 130, 42), (SX0 + 310, base - 40, 120, 40),
                                             (SX0 + 40, base + 70, 150, 50), (SX0 + 214, base + 72, 150, 50), (SX0 + 70, base + 170, 180, 56))):
        o.append(path(f"M{sx0},{sy0} L{sx0 + sw},{sy0 + 2} L{sx0 + sw + 8},{sy0 + sh} L{sx0 - 6},{sy0 + sh - 2} Z", fill="#cfc9bc", stroke=GREY, w=1.6, op=0.55, filt="brush"))
    fx, fy, fs = SCX - 100, base + 150, 3.0
    fig, a = attending(fx, fy, fs, flip=False, seat=18, lean=30, reach=(56, -4), robe=GREYROBE)
    o.append(fig)
    hx, hy = a["hands"][0]
    o.append(path(f"M{f(hx + 80)},{f(hy - 100)} L{f(hx + 4)},{f(hy + 2)}", stroke=INK, w=9))
    o.append(path(f"M{f(hx + 80)},{f(hy - 100)} L{f(hx + 4)},{f(hy + 2)}", stroke=BAMBOO, w=6))
    for k in range(-5, 6):
        o.append(path(f"M{f(hx + 2)},{f(hy)} l{f(k * 5 - 18)},{f(14 + abs(k))}", stroke=INK if k % 2 else GREY, w=2))
    rl = [(hx + 70, hy - 30), (hx + 110, hy - 70), (hx + 100, hy - 150), (hx + 130, hy - 40), (hx + 80, hy - 190), (hx + 50, hy - 12), (hx + 140, hy - 110)]
    o.append(scatter_leaves(rng, rl, (9, 14), (GREY, PALE, INK), (0.6, 0.9)))
    o.append(leaf(hx + 120, hy - 150, 130, 24, fill=VERMILION, veins=False))
    o.append(scatter_leaves(rng, [(hx - 120 + k * 36 + rng.uniform(-6, 6), hy + 14 + rng.uniform(-4, 10)) for k in range(9)], (7, 11), (GREY, PALE, INK), (0.55, 0.85)))
    o.append(scatter_leaves(rng, [(SX0 + 60 + rng.uniform(0, 360), base + 40 + rng.uniform(0, 200)) for _ in range(12)], (5, 9), (GREY, PALE), (0.4, 0.7)))
    o.append(wind_grass(rng, SX0 + 10, SX1 - 10, base + 230, base + 262, 14, 12, 24, dirn=1, bend=0.5))
    return finish(o + [zen_rank_close()])


def wi13(rng):
    """Third Rank of Wind: a wandering monk at a ford calls across the water to a ferryman, one arm raised and the sleeve full of wind; the far bank is a pale outline."""
    o = [zen_rank_open("wind", 3)]
    base = SY1 - 210
    wt, wb = base - 230, base - 20
    o.append(mist(SCX, wt - 120, 330, 40, 0.5))
    o.append(hills(rng, [(wt - 6, 56, PALE, 0.2, 90)], SX0 + 4, SX1 - 4))
    o.append(path(f"M{SX0},{wt - 4} Q{SCX},{wt - 16} {SX1},{wt - 2}", stroke=GREY, w=1.8, op=0.55, filt="brush"))
    o.append(water(SX0, SX1, wt, wb, op=0.55))
    o.append(ripple(SX1 - 130, wt + 120, 70, 3, op=0.7))
    o.append(stone_row(rng, SX0 + 30, SX0 + 190, wb - 36, 4, 12))
    o.append(ground(wb, SX0, SX1, op=0.2))
    o.append(boat(SX1 - 120, wt + 126, 150, 26))
    fm, _ = ordinary(SX1 - 112, wt + 108, 1.6, flip=True, tool=None, robe="#a9a398")
    o.append(fm)
    o.append(path(f"M{SX1 - 164},{wt + 20} L{SX1 - 98},{wt + 140}", stroke=INK, w=5.4))
    o.append(path(f"M{SX1 - 164},{wt + 20} L{SX1 - 98},{wt + 140}", stroke="#6b5a45", w=3.4))
    o.append(path(f"M{SX0 + 150 + 36 * 2.6},{base + 90} L{SX0 + 150 + 38 * 2.6},{base + 90 - 150 * 2.6}", stroke=INK, w=7.6))
    o.append(path(f"M{SX0 + 150 + 36 * 2.6},{base + 90} L{SX0 + 150 + 38 * 2.6},{base + 90 - 150 * 2.6}", stroke="#6b5a45", w=5))
    fig, a = acting(SX0 + 150, base + 90, 2.6, flip=False, strike=False, reach=(46, -130), robe=SKIN)
    o.append(fig)
    hand = a["hands"][0]
    elbow = _anchor(SX0 + 150, base + 90, 2.6, False, (28, -94))
    # the sleeve streams back from the raised forearm in the wind
    o.append(streamer(elbow[0] + 4, elbow[1] + 8, 58, -1, droop=-6, w0=20, w1=4, fill=GREYROBE))
    mx, my = _anchor(SX0 + 150, base + 90, 2.6, False, (17, -95))
    o.append(ellipse(mx, my, 4.6, 6, INK))
    o.append(wind_grass(rng, SX0 + 10, SX1 - 10, base + 150, base + 230, 26, 14, 30, dirn=1, bend=0.55))
    return finish(o + [zen_rank_close()])


def wi14(rng):
    """Fourth Rank of Wind: two people talking at a crossroads where several roads meet, their sleeves blowing toward each other, a child running between them with a kite (the accent); the grass leans in the same wind."""
    o = [zen_rank_open("wind", 4)]
    base = SY1 - 190
    hor = base - 330
    o.append(hills(rng, [(hor + 10, 40, PALE, 0.25, 80)], SX0 + 4, SX1 - 4))
    o.append(path(f"M{SX0},{hor + 8} Q{SCX},{hor + 2} {SX1},{hor + 10}", stroke=GREY, w=1.5, op=0.6, filt="brush"))
    jx, jy = SCX, base - 70
    rd = "#cfc6b6"
    o.append(path(f"M{SX0},{jy - 24} L{SX1},{jy - 30} L{SX1},{jy + 30} L{SX0},{jy + 36} Z", fill=rd, stroke=None, op=0.5, filt="softwash"))
    o.append(path(f"M{jx - 16},{hor + 10} L{jx + 20},{hor + 10} L{jx + 70},{jy} L{jx - 70},{jy} Z", fill=rd, stroke=None, op=0.5, filt="softwash"))
    o.append(path(f"M{jx - 70},{jy} L{jx + 70},{jy} L{jx + 150},{base + 220} L{jx - 150},{base + 220} Z", fill=rd, stroke=None, op=0.5, filt="softwash"))
    o.append(path(f"M{SX0},{jy + 38} Q{jx - 100},{jy + 36} {jx - 82},{jy + 18} M{SX1},{jy + 34} Q{jx + 100},{jy + 32} {jx + 82},{jy + 14}", stroke=GREY, w=1.4, op=0.55))
    o.append(path(f"M{jx - 16},{hor + 12} L{jx - 64},{jy - 4} M{jx + 20},{hor + 12} L{jx + 66},{jy - 6}", stroke=GREY, w=1.4, op=0.55))
    # a distant tree bending
    o.append(trunk(rng, SX0 + 56, hor + 30, hor - 150, 8, 18, leafy=2))
    # the two talkers; sleeves streaming toward each other
    s1x, s2x, gb = SCX - 120, SCX + 120, base + 90
    fig, a = engaged(s1x, gb, 2.2, flip=False, hat=False, tool=None, seat="stump")
    o.append(fig)
    hx, hy = a["hands"][0]
    o.append(streamer(hx + 2, hy + 6, 84, 1, droop=-10, w0=26, w1=6, fill=GREYROBE))
    fig2, _ = ordinary(s2x, gb, 2.3, flip=True, tool=None, robe="#b8b2a6")
    o.append(fig2)
    sh2 = _anchor(s2x, gb, 2.3, True, (6, -70))
    o.append(place(s2x, gb, 2.3, True, _arm((6, -70), (22, -90), (36, -98), SKIN, 4.6)))
    h2 = _anchor(s2x, gb, 2.3, True, (36, -98))
    o.append(streamer(h2[0] - 2, h2[1] + 6, 84, -1, droop=-8, w0=26, w1=6, fill="#b8b2a6"))
    # the child running between with a kite
    kx, ky = SCX + 6, base - 330
    cf, ca = ordinary(SCX + 4, base + 150, 1.3, flip=False, tool=None, robe="#c9c4ba")
    o.append(cf)
    ch = _anchor(SCX + 4, base + 150, 1.3, False, (30, -86))
    o.append(place(SCX + 4, base + 150, 1.3, False, _arm((8, -66), (24, -82), (30, -88), SKIN, 4.2)))
    o.append(path(f"M{f(ch[0])},{f(ch[1])} Q{f(ch[0] + 20)},{f(ky + 200)} {f(kx + 6)},{f(ky + 26)}", stroke=INK, w=1.2, op=0.8))
    o.append(kite(kx, ky, 1.5, 24))
    o.append(wind_grass(rng, SX0 + 10, SX1 - 10, base + 230, base + 270, 22, 14, 30, dirn=1, bend=0.55))
    o.append(wind_grass(rng, SX0 + 10, SX0 + 100, jy + 50, jy + 90, 10, 14, 30, dirn=1, bend=0.55))
    return finish(o + [zen_rank_close()])


def wi15(rng):
    """Fifth Rank of Wind: an old man hanging washing on a line in a steady wind, the sheets full and snapping, reaching for the next peg without looking up; a hand fan lies in a basket at his feet (the one accent)."""
    o = [zen_rank_open("wind", 5)]
    base = SY1 - 190
    o.append(mist(SCX, base - 470, 340, 40, 0.5))
    o.append(path(f"M{SX0},{base - 130} Q{SCX},{base - 138} {SX1},{base - 128}", stroke=GREY, w=2, op=0.5, filt="brush"))
    o.append(path(f"M{SX0},{base - 128} Q{SCX},{base - 136} {SX1},{base - 126} L{SX1},{base - 96} L{SX0},{base - 96} Z", fill="#cfc6b6", op=0.3, filt="softwash"))
    o.append(ground(base - 60, SX0, SX1, op=0.2))
    ly = base - 282
    px0, px1 = SX0 + 34, SX1 - 30
    o.append(_pole(px0, base + 20, ly - 20, 8))
    o.append(_pole(px1, base + 20, ly - 20, 8))
    o.append(path(f"M{px0},{ly - 14} Q{(px0 + px1) / 2},{ly - 8} {px1},{ly - 14}", stroke=INK, w=2.4))
    fy = ly - 11
    for i, (a, b, ln, sh, ph) in enumerate(((SCX + 30, SCX + 120, 230, 70, 0), (SCX + 134, SCX + 208, 190, 56, 1))):
        o.append(cloth(a, b, fy, ln, sh, amp=12, fill=("#ece6d6", "#e1dac8", "#f0eadb")[i], n=3, phase=ph))
        for pgx in (a + 8, b - 8):
            o.append(path(f"M{pgx},{fy - 6} l0,14", stroke=INK, w=3.6))
    fig, a = ordinary(SCX - 115, base + 40, 2.8, flip=False, tool=None)
    o.append(fig)
    # one arm bent up toward the line, a peg in the hand; the other hand at the waist
    reach = _arm((-4, -66), (-16, -92), (-12, -120), SKIN, 4.6) + _arm((2, -64), (14, -56), (24, -54), SKIN, 4.6)
    peg = '<path d="M-12,-122 l0,-10" stroke="#6b5a45" stroke-width="3" stroke-linecap="round"/>'
    o.append(place(SCX - 115, base + 40, 2.8, False, reach + peg))
    o.append(_basket(SCX - 60, base + 80, 90, 54))
    o.append(fan(SCX - 52, base + 8, 30, 22, accent=True))
    o.append(wind_grass(rng, SX0 + 10, SX1 - 10, base + 130, base + 200, 30, 14, 32, dirn=1, bend=0.6))
    o.append(scatter_leaves(rng, [(SX0 + 80 + rng.uniform(0, 340), base + 100 + rng.uniform(0, 80)) for _ in range(9)], (5, 9), (GREY, PALE), (0.4, 0.7)))
    return finish(o + [zen_rank_close()])


CARDS = {"wi01": wi01, "wi02": wi02, "wi03": wi03, "wi04": wi04, "wi05": wi05,
         "wi06": wi06, "wi07": wi07, "wi08": wi08, "wi09": wi09, "wi10": wi10,
         "wi11": wi11, "wi12": wi12, "wi13": wi13, "wi14": wi14, "wi15": wi15}
