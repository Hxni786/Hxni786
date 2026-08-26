"""
render_heatmap_svg.py  –  render contrib-heatmap.svg from data/contributions.json
  • Gold-ramp palette (none → bright gold)  The Cipher Stack aesthetic
  • 53 weeks × 7 days (Sun → Sat), month labels, day labels
  • Diagonal cell reveal (SMIL opacity animate, freeze after — no loop)
  • Stats footer: total contributions, current streak, best streak

Usage:
  python scripts/render_heatmap_svg.py
"""

import json
from datetime import date, timedelta
from pathlib import Path


# ── Config ────────────────────────────────────────────────────────────
DATA_FILE = "data/contributions.json"
OUT       = "contrib-heatmap.svg"

CELL    = 11       # cell size in px
GAP     = 2        # gap between cells
WEEKS   = 53
DAYS    = 7        # Sun=0 … Sat=6

PAD_L   = 30       # left  (day-of-week labels)
PAD_T   = 22       # top   (month labels)
PAD_B   = 44       # bottom (stats footer + legend)
PAD_R   = 10

SVG_W = PAD_L + WEEKS * (CELL + GAP) - GAP + PAD_R
SVG_H = PAD_T + DAYS  * (CELL + GAP) - GAP + PAD_B

BG = "#0d0d0d"

# Gold ramp: level 0 (none) → level 4 (max activity)
PALETTE = [
    "#1a1a1a",   # 0 – no contributions
    "#2d1a00",   # 1 – low
    "#5c3a00",   # 2 – moderate
    "#8B6914",   # 3 – active
    "#D4AF37",   # 4 – high (Cipher Stack gold)
]
GOLD     = "#D4AF37"
DIM_GOLD = "#8B6914"
SILVER   = "#8a8a8a"

FONT     = '"Courier New", Courier, monospace'
FONT_SM  = 9       # month/day label size
FONT_MED = 10      # footer size

# Day-of-week labels (GitHub calendar: Sun=row0 … Sat=row6)
DOW_LABELS = ["", "Mon", "", "Wed", "", "Fri", ""]

# Animation
CELL_DUR = 0.30    # opacity animation duration per cell (s)
DIAG_STEP = 0.010  # extra delay per diagonal step (s)


# ── Grid builder ──────────────────────────────────────────────────────

def build_grid(days_data: dict) -> tuple[list, dict]:
    """
    Build a 53×7 grid (col=week, row=dow 0=Sun) aligned to GitHub's calendar.
    Returns (cells, month_labels_by_col).
    """
    today = date.today()

    # Find this week's Sunday (GitHub calendar row 0)
    # Python weekday(): Mon=0 … Sun=6  →  GitHub Sunday = Python 6
    days_since_sun = (today.weekday() + 1) % 7    # 0 if today is Sunday
    this_sunday = today - timedelta(days=days_since_sun)

    # Calendar starts 52 weeks before this Sunday
    first_sunday = this_sunday - timedelta(weeks=52)

    cells        = []
    month_labels = {}   # col → "Jan" etc.

    for col in range(WEEKS):
        week_start = first_sunday + timedelta(weeks=col)   # this week's Sunday
        for row in range(DAYS):                             # 0=Sun … 6=Sat
            d  = week_start + timedelta(days=row)
            ds = d.isoformat()

            info  = days_data.get(ds, {})
            level = min(int(info.get("level", 0)), len(PALETTE) - 1)
            count = int(info.get("count", 0))

            cells.append((col, row, ds, level, count))

            # First day of month → column gets a month label (row 0 preferred)
            if d.day == 1 and col not in month_labels:
                month_labels[col] = d.strftime("%b")

    return cells, month_labels


# ── SVG helpers ───────────────────────────────────────────────────────

def cell_xy(col: int, row: int) -> tuple[float, float]:
    x = PAD_L + col * (CELL + GAP)
    y = PAD_T + row * (CELL + GAP)
    return x, y


def render(data: dict) -> str:
    days_map   = {d["date"]: d for d in data.get("days", [])}
    cells, month_labels = build_grid(days_map)

    total        = data.get("total", 0)
    cur_streak   = data.get("current_streak", 0)
    long_streak  = data.get("longest_streak", 0)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{SVG_W}" height="{SVG_H}" '
        f'viewBox="0 0 {SVG_W} {SVG_H}">',
        f'<rect width="{SVG_W}" height="{SVG_H}" fill="{BG}" rx="6"/>',
        f'<style>text{{font-family:{FONT};}}</style>',
    ]

    # ── Month labels ─────────────────────────────────────────────────
    for col, name in month_labels.items():
        x, _ = cell_xy(col, 0)
        y    = PAD_T - 5
        parts.append(
            f'<text x="{x:.0f}" y="{y}" '
            f'font-size="{FONT_SM}" fill="{SILVER}">{name}</text>'
        )

    # ── Day-of-week labels ────────────────────────────────────────────
    for row, label in enumerate(DOW_LABELS):
        if not label:
            continue
        _, y = cell_xy(0, row)
        baseline = y + CELL - 1
        parts.append(
            f'<text x="0" y="{baseline:.0f}" '
            f'font-size="{FONT_SM}" fill="{SILVER}">{label}</text>'
        )

    # ── Cells ─────────────────────────────────────────────────────────
    for col, row, ds, level, count in cells:
        x, y  = cell_xy(col, row)
        color = PALETTE[level]
        delay = (col + row) * DIAG_STEP
        tip   = f"{count} contribution{'s' if count != 1 else ''} on {ds}"
        future = ds > date.today().isoformat()
        fill_opacity = "0.25" if future else "1"

        parts.append(
            f'<rect x="{x:.0f}" y="{y:.0f}" '
            f'width="{CELL}" height="{CELL}" rx="2" '
            f'fill="{color}" fill-opacity="{fill_opacity}" '
            f'opacity="0">'
            f'<animate attributeName="opacity" '
            f'from="0" to="1" '
            f'dur="{CELL_DUR}s" begin="{delay:.3f}s" fill="freeze"/>'
            f'<title>{tip}</title>'
            f'</rect>'
        )

    # ── Stats footer ─────────────────────────────────────────────────
    footer_y  = PAD_T + DAYS * (CELL + GAP) - GAP + 14
    center_x  = SVG_W // 2
    stats_txt = (
        f'{total:,} contributions in the last year  \u00b7  '
        f'Streak: {cur_streak}d  \u00b7  '
        f'Best: {long_streak}d'
    )
    parts.append(
        f'<text x="{center_x}" y="{footer_y}" '
        f'font-size="{FONT_MED}" fill="{SILVER}" '
        f'text-anchor="middle">{stats_txt}</text>'
    )

    # ── Legend (Less → More) ─────────────────────────────────────────
    legend_y  = footer_y + 18
    legend_w  = len(PALETTE) * (CELL + 2) - 2
    legend_x  = SVG_W - PAD_R - legend_w - 36   # right-aligned

    parts.append(
        f'<text x="{legend_x - 4}" y="{legend_y + CELL - 1}" '
        f'font-size="{FONT_SM}" fill="{SILVER}" '
        f'text-anchor="end">Less</text>'
    )
    for i, pal in enumerate(PALETTE):
        lx = legend_x + i * (CELL + 2)
        parts.append(
            f'<rect x="{lx:.0f}" y="{legend_y}" '
            f'width="{CELL}" height="{CELL}" rx="2" fill="{pal}"/>'
        )
    more_x = legend_x + legend_w + (CELL + 2)
    parts.append(
        f'<text x="{more_x}" y="{legend_y + CELL - 1}" '
        f'font-size="{FONT_SM}" fill="{SILVER}">More</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


# ── Entry point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Reading {DATA_FILE} …")
    data = json.loads(Path(DATA_FILE).read_text(encoding="utf-8"))
    svg  = render(data)
    Path(OUT).write_text(svg, encoding="utf-8")
    print(
        f"  ✓  {OUT}  ({SVG_W}\u00d7{SVG_H}px)  "
        f"{len(data.get('days', []))} days  "
        f"{data.get('total', 0):,} contributions"
    )
