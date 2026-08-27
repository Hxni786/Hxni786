"""
make_info_card.py  –  generate info-card.svg (neofetch style, Cipher Stack gold)
  • Title bar with terminal handle
  • Gold keys / silver values
  • CSS keyframe fade-in per line (no JS, plays inside GitHub <img>)
  • Set env STATIC=1 for a frozen frame (useful for local preview)

Usage:
  python scripts/make_info_card.py
  STATIC=1 python scripts/make_info_card.py    # frozen frame
"""

import os
from pathlib import Path

STATIC = os.environ.get("STATIC") == "1"
OUT    = "info-card.svg"

# ── Your details ─────────────────────────────────────────────────────
HANDLE  = "The Cipher Stack"
DIVIDER = "\u2500" * 40          # ────────────────── (box-drawing dash)

#   (key, value)  –  empty key = continuation / indent line
FIELDS = [
    ("OS",       "The Cipher Stack v2026"),
    ("Host",     "Islamabad, Pakistan  |  PKT (UTC+5)"),
    ("Role",     "Full-Stack Dev + Content Creator"),
    ("Stack",    "React 19 \u00b7 Vite \u00b7 Tailwind v4 \u00b7 Framer Motion"),
    ("",         "Flutter \u00b7 Python \u00b7 MySQL \u00b7 Supabase"),
    ("Brand",    "The Cipher Stack"),
    ("Social",   "fb.com/Hxni786  |  @the.cipher.stack (IG)"),
    ("LinkedIn", "Syed Hassan Dildar"),
    ("Web",      "a-talking-cinematic-portfolio-yfq6.vercel.app"),
    ("Study",    "BSCS \u2192 ML / AI Research"),
    ("GitHub",   "github.com/Hxni786"),
]

# ── Palette ──────────────────────────────────────────────────────────
BG       = "#0d0d0d"
GOLD     = "#D4AF37"
DIM_GOLD = "#8B6914"
SILVER   = "#b0b0b0"
FONT     = '"Courier New", Courier, monospace'

# ── Geometry ─────────────────────────────────────────────────────────
SVG_W    = 490
FONT_PX  = 12
LINE_H   = 19
PAD_X    = 18
TITLE_H  = 36           # height of the title-bar strip
# Lines: title + divider + fields
N_LINES  = 2 + len(FIELDS)
SVG_H    = TITLE_H + (N_LINES * LINE_H) + 22   # 22 bottom padding


def css_block() -> str:
    if STATIC:
        return "<style></style>"
    rules = "@keyframes fin{from{opacity:0}to{opacity:1}}\n"
    for i in range(N_LINES):
        delay = i * 0.06
        rules += f".l{i}{{animation:fin .4s {delay:.2f}s both}}\n"
    return f"<style>{rules}</style>"


def text_tag(i: int, x: float, y: float, fill: str,
             weight: str, size: int, content: str) -> str:
    cls = "" if STATIC else f' class="l{i}"'
    op  = "" if STATIC else ' opacity="0"'
    return (
        f'<text{cls} x="{x:.0f}" y="{y:.0f}"{op} '
        f'font-family={FONT!r} font-size="{size}px" '
        f'font-weight="{weight}" fill="{fill}">{content}</text>'
    )


def encode(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def make_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SVG_W}" height="{SVG_H}" '
        f'viewBox="0 0 {SVG_W} {SVG_H}">',

        # ── Background ──────────────────────────────────────────────
        f'<rect width="{SVG_W}" height="{SVG_H}" fill="{BG}" rx="8"/>',

        # ── Gold border ─────────────────────────────────────────────
        f'<rect x="1" y="1" width="{SVG_W-2}" height="{SVG_H-2}" '
        f'fill="none" stroke="{DIM_GOLD}" stroke-width="1" rx="7.5"/>',

        # ── Title bar strip ─────────────────────────────────────────
        f'<rect width="{SVG_W}" height="{TITLE_H}" fill="{DIM_GOLD}" '
        f'fill-opacity="0.18" rx="8"/>',
        # keep bottom edge of strip square
        f'<rect x="0" y="{TITLE_H//2}" width="{SVG_W}" height="{TITLE_H//2}" '
        f'fill="{DIM_GOLD}" fill-opacity="0.18"/>',

        # ── Decorative terminal dots (top-left) ─────────────────────
        f'<circle cx="16" cy="{TITLE_H//2}" r="4" fill="#ff5f56" opacity="0.7"/>',
        f'<circle cx="30" cy="{TITLE_H//2}" r="4" fill="#ffbd2e" opacity="0.7"/>',
        f'<circle cx="44" cy="{TITLE_H//2}" r="4" fill="#27c93f" opacity="0.7"/>',

        css_block(),
    ]

    # ── Title (line 0) ───────────────────────────────────────────────
    title_y = TITLE_H - 9          # baseline in the title bar
    parts.append(text_tag(
        0, 58, title_y,
        GOLD, "bold", FONT_PX + 1,
        encode(HANDLE),
    ))

    # ── Divider (line 1) ─────────────────────────────────────────────
    div_y = TITLE_H + LINE_H
    parts.append(text_tag(
        1, PAD_X, div_y,
        DIM_GOLD, "normal", FONT_PX - 1,
        encode(DIVIDER),
    ))

    # ── Fields (lines 2 … N) ─────────────────────────────────────────
    for idx, (key, val) in enumerate(FIELDS):
        line_i = idx + 2
        y      = div_y + (idx + 1) * LINE_H

        if key:
            # "KEY     : value"
            padded_key = f"{key:<8}"
            content = (
                f'<tspan font-weight="bold" fill="{GOLD}">{encode(padded_key)}</tspan>'
                f'<tspan fill="{DIM_GOLD}"> : </tspan>'
                f'<tspan fill="{SILVER}">{encode(val)}</tspan>'
            )
        else:
            # continuation / indent line (no key)
            content = f'<tspan fill="{SILVER}">{" " * 11}{encode(val)}</tspan>'

        cls = "" if STATIC else f' class="l{line_i}"'
        op  = "" if STATIC else ' opacity="0"'
        parts.append(
            f'<text{cls} x="{PAD_X}" y="{y}"{op} '
            f'font-family={FONT!r} font-size="{FONT_PX}px">'
            f'{content}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    mode = "STATIC" if STATIC else "animated"
    print(f"Generating {OUT} ({mode}) …")
    Path(OUT).write_text(make_svg(), encoding="utf-8")
    print(f"  ✓  {OUT}  ({SVG_W}\u00d7{SVG_H}px, {N_LINES} lines)")
