"""
make_ascii_svg.py  –  turn source-prepped.png into hxni-ascii.svg
  • Single gold fill (no rainbow chaos)
  • Each row wipes left→right via SMIL clipPath animation
  • Prints once, then freezes — no looping
  • GitHub renders SMIL inside <img> tags

Usage:
  python scripts/make_ascii_svg.py
"""

from pathlib import Path
import numpy as np
from PIL import Image


# ── Tunables ─────────────────────────────────────────────────────────
SRC      = "source-prepped.png"
OUT      = "hxni-ascii.svg"

COLS     = 80           # character columns — increase for more detail
ASPECT   = 0.46         # height/width ratio correction for Courier New chars
                        # characters are ~2x taller than wide; 0.46 ≈ 1/2.17
FONT_PX  = 9            # font-size in px
FONT_W   = 5.5          # px per char (Courier New 0.6em at 9px)
LINE_H   = 11           # px per line (font + leading)
GOLD     = "#D4AF37"    # The Cipher Stack gold

# Density ramp: leftmost = bright (white → space), rightmost = dark (black → @)
RAMP = " .`:-=+*cs#%@"

# Animation
WIPE_DUR    = 0.12      # wipe duration per row (seconds)
TOTAL_SECS  = 2.6       # total time for all rows to appear


def img_to_ascii(src: str) -> list[str]:
    img  = Image.open(src).convert("L")
    rows = max(1, int(COLS * (img.height / img.width) * ASPECT))
    img  = img.resize((COLS, rows), Image.LANCZOS)
    arr  = np.array(img)
    ramp_len = len(RAMP) - 1
    return [
        "".join(RAMP[int(v / 255 * ramp_len)] for v in row)
        for row in arr
    ]


def build_svg(lines: list[str]) -> str:
    n_rows = len(lines)
    n_cols = max(len(l) for l in lines)
    svg_w  = n_cols * FONT_W
    svg_h  = n_rows * LINE_H + LINE_H      # +1 line bottom breathing room

    row_delay = TOTAL_SECS / max(n_rows, 1)

    # ── CSS Animation Rules ──────────────────────────────────────────
    css_rules = [
        "<style>",
        f'text {{ font-family: "Courier New", Courier, monospace; font-size: {FONT_PX}px; fill: {GOLD}; }}',
        "@keyframes fin { from { opacity: 0; } to { opacity: 1; } }",
        ".row { animation: fin 0.3s ease-out both; }",
    ]
    for i in range(n_rows):
        delay = i * row_delay
        css_rules.append(f".r{i} {{ animation-delay: {delay:.3f}s; }}")
    css_rules.append("</style>")

    # ── <defs>: one clipPath per row ─────────────────────────────────
    defs_parts = ["<defs>"]
    for i in range(n_rows):
        delay = i * row_delay
        y     = i * LINE_H
        defs_parts.append(
            f'  <clipPath id="r{i}">'
            f'<rect x="0" y="{y}" width="0" height="{LINE_H}">'
            f'<animate attributeName="width" from="0" to="{svg_w:.1f}" '
            f'dur="{WIPE_DUR}s" begin="{delay:.3f}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
    defs_parts.append("</defs>")

    # ── Text rows ────────────────────────────────────────────────────
    text_parts = []
    for i, line in enumerate(lines):
        baseline = (i + 1) * LINE_H
        safe = (line
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))
        text_parts.append(
            f'<text class="row r{i}" x="0" y="{baseline}" '
            f'xml:space="preserve" '
            f'clip-path="url(#r{i})">{safe}</text>'
        )

    # ── Assemble SVG ─────────────────────────────────────────────────
    svg = "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{svg_w:.0f}" height="{svg_h:.0f}" '
        f'viewBox="0 0 {svg_w:.0f} {svg_h:.0f}">',

        # Background
        '<rect width="100%" height="100%" fill="#0d0d0d" rx="8"/>',
        f'<rect x="1" y="1" width="{svg_w-2:.0f}" height="{svg_h-2:.0f}" fill="none" stroke="#8B6914" stroke-width="1" rx="7.5"/>',

        "\n".join(css_rules),
        "\n".join(defs_parts),
        "\n".join(text_parts),
        "</svg>",
    ])
    return svg


if __name__ == "__main__":
    lines = img_to_ascii(SRC)
    svg   = build_svg(lines)
    Path(OUT).write_text(svg, encoding="utf-8")
    cols  = max(len(l) for l in lines)
    print(f"Generated {OUT} ({cols} cols x {len(lines)} rows)")
