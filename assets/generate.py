#!/usr/bin/env python3
"""Draws Figure 1 of the profile README: the HPDP data chain.

Writes figure-light.svg and figure-dark.svg next to this file. The fonts
(Anybody and IBM Plex Sans, the same as the website) are subset to the
characters used and embedded, because an SVG shown through <img> cannot load
web fonts.

    pip install fonttools brotli
    python3 assets/generate.py path/to/fonts

The fonts folder needs anybody.woff2 (static, width 125 %, weight 800),
plex.woff2 (IBM Plex Sans, variable weight) and plexi.woff2 (IBM Plex Sans
Italic 400), all from Google Fonts.
"""

import base64
import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

OUT = Path(__file__).resolve().parent

# GitHub's own text colours, so the figure reads as part of the page. The
# background stays transparent; boxes are filled with the page colour.
THEMES = {
    "light": dict(page="#ffffff", ink="#1f2328", quiet="#59636e"),
    "dark": dict(page="#0d1117", ink="#e6edf3", quiet="#9198a1"),
}


def wavelength_rgb(nm):
    """Approximate colour of light at a wavelength (after Dan Bruton)."""
    if nm < 440:
        r, g, b = (440 - nm) / 60, 0, 1
    elif nm < 490:
        r, g, b = 0, (nm - 440) / 50, 1
    elif nm < 510:
        r, g, b = 0, 1, (510 - nm) / 20
    elif nm < 580:
        r, g, b = (nm - 510) / 70, 1, 0
    elif nm < 645:
        r, g, b = 1, (645 - nm) / 65, 0
    else:
        r, g, b = 1, 0, 0
    f = 0.3 + 0.7 * (nm - 400) / 20 if nm < 420 else 0.3 + 0.7 * (700 - nm) / 20 if nm > 680 else 1
    return "#%02x%02x%02x" % tuple(round(255 * (c * f) ** 0.8) for c in (r, g, b))


class Fonts:
    """Records the characters each face uses, then embeds subset WOFF2s."""

    def __init__(self, folder):
        self.folder = Path(folder)
        self.used = {"anybody": set(), "plex400": set(), "plex600": set(), "plexi": set()}

    def text(self, face, x, y, s, size, fill, anchor="start", extra=""):
        self.used[face].update(s)
        s = s.replace("&", "&amp;").replace("<", "&lt;")
        return (f'<text x="{x}" y="{y}" class="{face}" font-size="{size}" fill="{fill}" '
                f'text-anchor="{anchor}"{extra}>{s}</text>')

    def _woff2(self, face):
        src = {"anybody": "anybody", "plex400": "plex", "plex600": "plex", "plexi": "plexi"}[face]
        font = TTFont(self.folder / f"{src}.woff2")
        if "fvar" in font:
            font = instancer.instantiateVariableFont(font, {"wght": 600 if face == "plex600" else 400})
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga"]
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(self.used[face]))
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        return base64.b64encode(buf.getvalue()).decode()

    def css(self):
        rules = []
        for face in self.used:
            rules.append(
                f"@font-face {{ font-family: '{face}'; src: url(data:font/woff2;base64,{self._woff2(face)}) format('woff2'); }}\n"
                f"    .{face} {{ font-family: '{face}', 'IBM Plex Sans', 'Segoe UI', Helvetica, Arial, sans-serif; }}"
            )
        return "\n    ".join(rules)


def figure(t, fonts):
    W, H = 1200, 430
    ym = 276  # centre line of the chain
    ink, quiet, page = t["ink"], t["quiet"], t["page"]
    o = []

    o.append(fonts.text("anybody", 0, 76, "Shubham Draveriya", 72, ink, extra=' letter-spacing="-1"'))
    o.append(fonts.text("plex400", 2, 122, "RTL design and FPGA bring-up", 25, quiet))

    # The spectrum: one pixel's bands, blue at the top, red at the bottom.
    stops = "".join(
        f'<stop offset="{(nm - 400) / 300:.3f}" stop-color="{wavelength_rgb(nm)}"/>' for nm in range(400, 701, 10)
    )
    o.append(f'<defs><linearGradient id="spectrum" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient></defs>')

    def arrow(x1, x2, note=None):
        s = f'<path d="M{x1} {ym} H{x2 - 9}" stroke="{ink}" stroke-width="1.5"/>'
        s += f'<path d="M{x2} {ym} l-10 -5 v10 z" fill="{ink}"/>'
        if note:
            s += fonts.text("plexi", (x1 + x2) / 2, ym - 14, note, 15, quiet, "middle")
        return s

    def notes(x, lines, anchor="middle"):
        return "".join(fonts.text("plex400", x, ym + 72 + i * 21, s, 15, quiet, anchor) for i, s in enumerate(lines))

    boxes = [
        (118, 160, "Correction", ["dark, gain and", "bad-pixel fixes"]),
        (356, 176, "CCSDS 123", ["lossless, on the", "FPGA at 250 MHz"]),
        (654, 150, "Framing", ["Reed-Solomon,", "AOS frames"]),
        (938, 162, "Ground station", ["decode and", "compare"]),
    ]

    # Connections first, so the boxes sit on top of them.
    o.append(arrow(32, 118))
    o.append(arrow(278, 356))
    o.append(arrow(532, 654, "about 3 : 1"))
    o.append(f'<path d="M804 {ym} H928" stroke="{ink}" stroke-width="3.5" stroke-linecap="round"/>')
    o.append(f'<path d="M938 {ym} l-10 -5 v10 z" fill="{ink}"/>')
    o.append(fonts.text("plexi", 868, ym - 14, "1.25 Gbaud fiber", 15, quiet, "middle"))
    o.append(arrow(1100, 1164))

    # One scan line travelling the chain: spectrum until the compressor,
    # ink-coloured bits (a third of the height) until the ground station,
    # then spectrum again. Boxes and end columns hide the swaps.
    x0, x1 = 36, 1164
    span = x1 - x0
    move = 0.72

    def at(x):
        return f"{move * (x - x0) / span:.4f}"

    p_comp, p_ground = at(444 - 6), at(1019 - 6)
    travel = (f'<animateTransform attributeName="transform" type="translate" values="0 0;{span} 0;{span} 0" '
              f'keyTimes="0;{move};1" dur="9s" repeatCount="indefinite"/>')
    bits = "".join(
        f'<rect x="{x0}" y="{ym - 9 + k * 3}" width="12" height="{2 if k % 3 else 1.2}" fill="{ink}"/>' for k in range(6)
    )
    o.append(
        f'<g>{travel}'
        f'<rect x="{x0}" y="{ym - 28}" width="12" height="56" fill="url(#spectrum)" opacity="1">'
        f'<animate attributeName="opacity" values="1;0;1;0;0" keyTimes="0;{p_comp};{p_ground};{move};1" '
        f'calcMode="discrete" dur="9s" repeatCount="indefinite"/></rect>'
        f'<g opacity="0">{bits}<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;{p_comp};{p_ground};1" '
        f'calcMode="discrete" dur="9s" repeatCount="indefinite"/></g></g>'
    )

    for x, w, title, lines in boxes:
        heart = title == "CCSDS 123"
        o.append(
            f'<rect x="{x}" y="{ym - 40}" width="{w}" height="80" fill="{ink if heart else page}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
        )
        o.append(fonts.text("plex600", x + w / 2, ym + 6, title, 19, page if heart else ink, "middle"))
        o.append(notes(x + w / 2, lines))

    # The sensor's line going in, and the same line coming out.
    for x in (0, 1164):
        o.append(f'<rect x="{x}" y="{ym - 80}" width="32" height="160" fill="url(#spectrum)"/>')
    o.append(fonts.text("plex600", 0, ym + 112, "Sensor line", 16, ink))
    o.append(fonts.text("plex400", 0, ym + 133, "512 pixels × 150 bands", 15, quiet))
    o.append(fonts.text("plex600", 1196, ym + 112, "Same line", 16, ink, "end"))
    o.append(fonts.text("plex400", 1196, ym + 133, "bit for bit", 15, quiet, "end"))

    body = "\n  ".join(o)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Shubham Draveriya, RTL design and FPGA bring-up. Figure 1: a sensor line passes through '
        f'correction, CCSDS 123 compression, framing, a 1.25 Gbaud fiber and a ground station, and comes out bit for bit.">\n'
        f"  <style>\n    {fonts.css()}\n"
        f"  </style>\n"
        f"  {body}\n</svg>\n"
    )


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "fonts"
    for mode, t in THEMES.items():
        fonts = Fonts(folder)
        data = figure(t, fonts)
        (OUT / f"figure-{mode}.svg").write_text(data, encoding="utf-8")
        print(f"figure-{mode}.svg", len(data) // 1024, "KB")


if __name__ == "__main__":
    main()
