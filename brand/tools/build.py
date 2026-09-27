"""Builds the Rêve by Rija logo and profile-picture SVGs.

All lettering is converted to vector outlines, so the SVGs look identical
everywhere (Canva, phones, printers) without needing the fonts installed.

    ./fetch_fonts.sh && python3 build.py && node render.mjs
"""
import math
import os

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "..", "svg")

# Brand palette
SLATE = "#29373F"
ROSE = "#E9A6A0"
GOLD = "#E8C476"
CREAM = "#F6EFE4"

TAGLINE = "EVERY BITE, A LITTLE DREAM"


class Font:
    def __init__(self, filename):
        path = os.path.join(FONTS, filename)
        self.tt = TTFont(path)
        self.hb = hb.Font(hb.Face(open(path, "rb").read()))
        self.upem = self.tt["head"].unitsPerEm
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()


DISPLAY = Font("CormorantGaramond-Regular.ttf")
SERIF = Font("CormorantGaramond-Medium.ttf")
SCRIPT = Font("PinyonScript-Regular.ttf")


class Text:
    """A shaped line of text that can be measured and drawn as SVG paths."""

    def __init__(self, font, text, size, tracking=0.0):
        self.font, self.size = font, size
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font.hb, buf, {"kern": True, "liga": True})
        self.glyphs, x = [], 0
        extra = tracking * font.upem
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            self.glyphs.append((font.order[info.codepoint], x + pos.x_offset, pos.y_offset))
            x += pos.x_advance + extra
        self.scale = size / font.upem
        self.bounds = self._bounds()

    def _transform(self, gx, gy, ox, oy):
        s = self.scale
        return (s, 0, 0, -s, ox + gx * s, oy - gy * s)

    def _bounds(self):
        bp = BoundsPen(self.font.glyphs)
        for name, gx, gy in self.glyphs:
            self.font.glyphs[name].draw(TransformPen(bp, self._transform(gx, gy, 0, 0)))
        return bp.bounds  # (xmin, ymin, xmax, ymax) relative to origin/baseline

    @property
    def width(self):
        return self.bounds[2] - self.bounds[0]

    @property
    def height(self):
        return self.bounds[3] - self.bounds[1]

    def draw(self, cx, top, color, accent=None, accent_above=None, accent_drop=0):
        """Draws with ink centred on cx and the ink top at `top`.

        Contours whose ink sits entirely above `accent_above` (font units)
        are painted in `accent` and lowered by `accent_drop` font units —
        used to colour the circumflex on the ê and nestle it closer.
        """
        ox = cx - (self.bounds[0] + self.bounds[2]) / 2
        oy = top - self.bounds[1]
        main, acc = SVGPathPen(self.font.glyphs), SVGPathPen(self.font.glyphs)
        for name, gx, gy in self.glyphs:
            rec = RecordingPen()
            self.font.glyphs[name].draw(rec)
            for contour in _split_contours(rec.value):
                ymin = min(p[1] for op, pts in contour for p in pts)
                is_accent = accent and accent_above is not None and ymin > accent_above
                pen = acc if is_accent else main
                dy = -accent_drop if is_accent else 0
                tp = TransformPen(pen, self._transform(gx, gy + dy, ox, oy))
                for op, pts in contour:
                    getattr(tp, op)(*pts)
        out = f'<path fill="{color}" d="{main.getCommands()}"/>'
        if acc.getCommands():
            out += f'<path fill="{accent}" d="{acc.getCommands()}"/>'
        return out


def _split_contours(ops):
    contours, cur = [], []
    for op, pts in ops:
        cur.append((op, pts))
        if op in ("closePath", "endPath"):
            contours.append(cur)
            cur = []
    return [c for c in contours if any(pts for _, pts in c)]


def sparkle(cx, cy, r, color, pinch=0.16):
    """Four-point star with softly curved sides."""
    p = r * pinch
    return (
        f'<path fill="{color}" d="M{cx},{cy - r} '
        f"Q{cx + p},{cy - p} {cx + r},{cy} Q{cx + p},{cy + p} {cx},{cy + r} "
        f'Q{cx - p},{cy + p} {cx - r},{cy} Q{cx - p},{cy - p} {cx},{cy - r}Z"/>'
    )


def crescent(cx, cy, r, color, cut=0.78, shift=(0.42, -0.30)):
    """Crescent moon: circle (cx,cy,r) minus an offset circle, as one path."""
    r2 = r * cut
    bx, by = cx + shift[0] * r, cy + shift[1] * r
    d = math.hypot(bx - cx, by - cy)
    a = (r * r - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r * r - a * a)
    ux, uy = (bx - cx) / d, (by - cy) / d
    mx, my = cx + a * ux, cy + a * uy
    p1 = (mx - h * uy, my + h * ux)
    p2 = (mx + h * uy, my - h * ux)
    return (
        f'<path fill="{color}" d="M{p1[0]:.2f},{p1[1]:.2f} '
        f"A{r},{r} 0 1 1 {p2[0]:.2f},{p2[1]:.2f} "
        f'A{r2},{r2} 0 1 0 {p1[0]:.2f},{p1[1]:.2f}Z"/>'
    )


def rule_with_diamond(cx, y, half, gap, color, w=2):
    d = 7
    return (
        f'<g stroke="{color}" stroke-width="{w}" stroke-linecap="round">'
        f'<line x1="{cx - half}" y1="{y}" x2="{cx - gap}" y2="{y}"/>'
        f'<line x1="{cx + gap}" y1="{y}" x2="{cx + half}" y2="{y}"/></g>'
        f'<path fill="{color}" d="M{cx},{y - d} L{cx + d},{y} L{cx},{y + d} L{cx - d},{y}Z"/>'
    )


def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">{rect}{body}</svg>\n'
    )


# x-height of Cormorant: anything above this (and above the e bowl) is the accent
ACCENT_ABOVE = 470
# the stock circumflex floats high at display sizes; lower it to sit snug
ACCENT_DROP = 42


def wordmark(cx, top, size, main, accent, script_color, with_by=True):
    """'Rêve' with a sparkle over the e and 'by Rija' in script beneath.

    Returns (svg, bottom_y).
    """
    reve = Text(DISPLAY, "Rêve", size, tracking=0.02)
    body = reve.draw(cx, top, main, accent=accent, accent_above=ACCENT_ABOVE, accent_drop=ACCENT_DROP)
    # tiny sparkle floating up-right of the final 'e', like a star in a dream
    right = cx + reve.width / 2
    body += sparkle(right + size * 0.10, top + size * 0.20, size * 0.075, accent)
    body += sparkle(right + size * 0.20, top + size * 0.04, size * 0.035, accent)
    bottom = top + reve.height
    if with_by:
        by = Text(SCRIPT, "by Rija", size * 0.42)
        # tuck the script slightly up under the wordmark, offset right
        by_top = bottom + size * 0.04
        body += by.draw(cx + size * 0.30, by_top, script_color)
        bottom = by_top + by.height
    return body, bottom


def tagline(cx, top, size, color, rule_color):
    t = Text(SERIF, TAGLINE, size, tracking=0.28)
    body = t.draw(cx, top, color)
    y = top + t.height / 2
    half = t.width / 2
    for sgn in (-1, 1):
        x0 = cx + sgn * (half + size * 1.0)
        x1 = cx + sgn * (half + size * 3.2)
        body += (
            f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{rule_color}" '
            f'stroke-width="{max(1.5, size * 0.07):.2f}" stroke-linecap="round"/>'
        )
    return body, top + t.height


def primary_logo(bg, main, accent, script_color, tag_color):
    W, H = 2000, 1250
    cx = W / 2

    def compose(top):
        mark, bottom = wordmark(cx - 40, top, 430, main, accent, script_color)
        tag, end = tagline(cx, bottom + 110, 34, tag_color, accent)
        return mark + tag, end

    _, end = compose(0)
    body, _ = compose((H - end) / 2)
    return svg(W, H, body, bg)


def profile_wordmark():
    """Profile picture A: the full wordmark on slate inside a fine gold ring."""
    S, c = 1080, 540
    body = f'<circle cx="{c}" cy="{c}" r="470" fill="none" stroke="{GOLD}" stroke-width="4"/>'
    body += f'<circle cx="{c}" cy="{c}" r="452" fill="none" stroke="{GOLD}" stroke-width="1.5" opacity=".55"/>'
    _, bottom = wordmark(c - 26, 0, 330, CREAM, GOLD, ROSE)
    # measure, then re-draw vertically centred
    mark, _ = wordmark(c - 26, (S - bottom) / 2, 330, CREAM, GOLD, ROSE)
    return svg(S, S, body + mark, SLATE)


def profile_monogram():
    """Profile picture B: a large 'R' cradled by a crescent moon."""
    S, c = 1080, 540
    body = f'<circle cx="{c}" cy="{c}" r="470" fill="none" stroke="{GOLD}" stroke-width="4"/>'
    body += crescent(c - 10, c + 5, 330, GOLD, cut=0.90, shift=(0.24, -0.16))
    r = Text(DISPLAY, "R", 470)
    body += r.draw(c + 40, c - r.height / 2 - 10, CREAM)
    body += sparkle(c + 215, c - 215, 34, ROSE)
    body += sparkle(c + 262, c - 155, 15, ROSE)
    return svg(S, S, body, SLATE)


def main():
    os.makedirs(OUT, exist_ok=True)
    files = {
        "reve-logo-on-slate.svg": primary_logo(SLATE, CREAM, GOLD, ROSE, CREAM),
        "reve-logo-on-cream.svg": primary_logo(CREAM, SLATE, GOLD, ROSE, SLATE),
        "reve-logo-transparent-light.svg": primary_logo(None, CREAM, GOLD, ROSE, CREAM),
        "reve-logo-transparent-dark.svg": primary_logo(None, SLATE, GOLD, ROSE, SLATE),
        "reve-profile-wordmark.svg": profile_wordmark(),
        "reve-profile-monogram.svg": profile_monogram(),
    }
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w") as f:
            f.write(content)
        print("wrote", name)


if __name__ == "__main__":
    main()
