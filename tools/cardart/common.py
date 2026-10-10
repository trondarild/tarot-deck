"""Shared pieces for code-drawn card art: canvas, filters, frames, palettes.

Every card function takes a seeded random.Random and returns a complete SVG
document string of size W x H. Frame helpers open and close a clipped group:
draw the scene between them.
"""

import math

W, H = 680, 1156  # 1:1.7, the aspect ratio of .card-image in main.css


def f(x):
    """Format a coordinate for SVG."""
    return f"{x:.1f}"


# Filters available to every card: paper grain, brush edge, dry brush,
# blurred wash, wash with a ragged edge, mist, aquatint grain.
PAPER_FILTERS = """
<filter id="paper" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="3" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -0.9 0.55" result="grain"/>
  <feComposite in="grain" in2="SourceGraphic" operator="in"/>
</filter>
<filter id="brush" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="7" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="5" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="dry" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9 0.08" numOctaves="2" seed="11" result="t"/>
  <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 1.5" result="gaps"/>
  <feComposite in="SourceGraphic" in2="gaps" operator="in" result="cut"/>
  <feDisplacementMap in="cut" in2="t" scale="4" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="wash" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="7"/>
</filter>
<filter id="mist" x="-20%" y="-50%" width="140%" height="200%">
  <feGaussianBlur stdDeviation="40"/>
</filter>
<filter id="softwash" x="-20%" y="-20%" width="140%" height="140%">
  <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3" seed="5" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="30" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feGaussianBlur in="d" stdDeviation="4"/>
</filter>
<filter id="aqua"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="21"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0.16  0 0 0 0 0.15  0 0 0 0 0.13  0 0 0 -3 1.6"/>
</filter>
"""


def svg(body, bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{PAPER_FILTERS}</defs>'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}'
            f'<rect width="{W}" height="{H}" fill="#7a6a50" filter="url(#paper)" opacity="0.35"/></svg>')


# ------------------------------------------------------------ Zen deck

ZEN_PAPER = "#f3ebdd"
INK, GREY, PALE, VERMILION = "#1f1d1b", "#55524d", "#8f8a82", "#b5452f"

# The Way (0-X): scene inside a hand-brushed ensō of fixed size and weight
ENSO_CX, ENSO_CY, ENSO_R = 340, 560, 288


def enso_open():
    """Start a group clipped to the inside of the ensō."""
    return (f'<clipPath id="inside"><circle cx="{ENSO_CX}" cy="{ENSO_CY}" r="{ENSO_R - 16}"/></clipPath>'
            '<g clip-path="url(#inside)">')


def _arc(r0, start, end, width, op, filt):
    cx, cy = ENSO_CX, ENSO_CY
    a0, a1 = math.radians(start), math.radians(end)
    x0, y0 = cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)
    x1, y1 = cx + r0 * math.cos(a1), cy + r0 * math.sin(a1)
    large = 1 if (end - start) % 360 > 180 else 0
    return (f'<path d="M{f(x0)},{f(y0)} A{r0},{r0} 0 {large} 1 {f(x1)},{f(y1)}" fill="none" stroke="{INK}" '
            f'stroke-width="{width}" stroke-linecap="round" opacity="{op}" filter="url(#{filt})"/>')


def enso_stroke():
    """The ensō: a heavy stroke with a dry, broken edge, open at the top right."""
    r = ENSO_R
    return "".join([_arc(r, -55, 268, 22, 0.92, "brush"), _arc(r + 6, -40, 250, 9, 0.8, "dry"),
                    _arc(r - 7, -60, 200, 6, 0.6, "dry"), _arc(r + 2, 230, 280, 12, 0.7, "dry")])


def seal(x=560, y=1000):
    """Small vermilion seal with an abstract mark."""
    return (f'<rect x="{x}" y="{y}" width="42" height="42" fill="{VERMILION}" opacity="0.9" filter="url(#brush)"/>'
            f'<path d="M{x + 10},{y + 12} h22 M{x + 21},{y + 12} v20 M{x + 10},{y + 32} h22" stroke="{ZEN_PAPER}" stroke-width="3"/>')


def enso_close(rng=None):
    """Close the clipped scene, then draw the ensō and the seal."""
    return "</g>" + enso_stroke() + seal()


# The Transmission (XI-XVII): tall hanging-scroll rectangle, no ensō
SCROLL_BOX = (110, 60, W - 110, H - 60)  # x0, y0, x1, y1 of the painted area


def scroll_open():
    """Start a group clipped to the scroll's painted area, with a silk mount around it."""
    x0, y0, x1, y1 = SCROLL_BOX
    return (f'<rect x="{x0 - 22}" y="{y0 - 22}" width="{x1 - x0 + 44}" height="{y1 - y0 + 44}" fill="#e4d9c4" stroke="#b9ab90" stroke-width="1.5"/>'
            f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{ZEN_PAPER}"/>'
            f'<clipPath id="scroll"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/></clipPath>'
            '<g clip-path="url(#scroll)">')


def scroll_close():
    x0, y0, x1, y1 = SCROLL_BOX
    return "</g>" + seal(x1 - 56, y1 - 56)


# ----------------------------------------------------- Pessimist deck

PESS_PAPER = "#f4f0e6"
ETCH_INK = "#2a2622"
# Watercolour washes; see docs/pessimistic-philosophy-illustration-description.md
WASH = {"bone": "#D8C59A", "slate": "#5E6B78", "caput": "#5A2E2E", "verdigris": "#6F8C7A"}
PLATE_BOX = (46, 46, W - 46, H - 46)   # the plate mark
IMAGE_BOX = (70, 70, W - 70, H - 70)   # the printed image inside it


def plate_open():
    """Plate mark and plate tone, then a group clipped to the image area."""
    px0, py0, px1, py1 = PLATE_BOX
    ix0, iy0, ix1, iy1 = IMAGE_BOX
    return (f'<rect x="{px0}" y="{py0}" width="{px1 - px0}" height="{py1 - py0}" fill="#eee8db" stroke="#b9b2a4" stroke-width="3"/>'
            f'<clipPath id="img"><rect x="{ix0}" y="{iy0}" width="{ix1 - ix0}" height="{iy1 - iy0}"/></clipPath>'
            '<g clip-path="url(#img)">')


def plate_close():
    return "</g>"


def aquatint(opacity=0.55, fade=True):
    """Aquatint grain over the image area; with fade, it thins toward the top."""
    ix0, iy0, ix1, iy1 = IMAGE_BOX
    mask = ""
    defs = ""
    if fade:
        defs = ('<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                '<stop offset="0.35" stop-color="#fff" stop-opacity="0.5"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>'
                f'<mask id="fadeMask"><rect x="{ix0}" y="{iy0}" width="{ix1 - ix0}" height="{iy1 - iy0}" fill="url(#fade)"/></mask>')
        mask = ' mask="url(#fadeMask)"'
    return defs + f'<rect x="{ix0}" y="{iy0}" width="{ix1 - ix0}" height="{iy1 - iy0}" filter="url(#aqua)"{mask} opacity="{opacity}"/>'
