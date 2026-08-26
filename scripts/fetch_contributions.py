"""
fetch_contributions.py  –  scrape your public GitHub contribution calendar
  • No API key, no GraphQL — just the same public HTML GitHub serves itself
  • Writes data/contributions.json with raw day data + derived stats
  • Robust to GitHub's HTML changes (two selector strategies)

Usage:
  python scripts/fetch_contributions.py
"""

import json, re
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME    = "Hxni786"
URL         = f"https://github.com/users/{USERNAME}/contributions"
HEADERS     = {"User-Agent": "Mozilla/5.0 (compatible; profile-art-bot/1.0)"}
TIMEOUT     = 20    # seconds


# ── Parsing ──────────────────────────────────────────────────────────

def parse_html(html: str) -> list[dict]:
    """Return a list of {date, level, count} dicts, sorted by date."""
    soup = BeautifulSoup(html, "html.parser")

    # Strategy 1: modern GitHub HTML (ContributionCalendar-day td cells)
    cells = soup.find_all("td", class_="ContributionCalendar-day")

    # Strategy 2: fallback — any element with data-date + data-level
    if not cells:
        cells = soup.find_all(attrs={"data-date": True, "data-level": True})

    days = []
    for cell in cells:
        date_str = cell.get("data-date")
        if not date_str:
            continue

        level = int(cell.get("data-level", 0))

        # Try to get exact count from sr-only text (e.g. "3 contributions on …")
        count = 0
        sr_el = cell.find(class_="sr-only") or cell.find("span", string=re.compile(r"\d"))
        if sr_el:
            m = re.search(r"(\d+)\s+contribution", sr_el.get_text())
            if m:
                count = int(m.group(1))
        elif level > 0:
            # GitHub levels: 0=none, 1=1–3, 2=4–6, 3=7–9, 4=10+
            count = [0, 2, 5, 8, 10][min(level, 4)]

        days.append({"date": date_str, "level": level, "count": count})

    return sorted(days, key=lambda d: d["date"])


# ── Stats ─────────────────────────────────────────────────────────────

def compute_stats(days: list[dict]) -> dict:
    if not days:
        return {"total": 0, "current_streak": 0, "longest_streak": 0,
                "best_day": {"date": "N/A", "count": 0}}

    total = sum(d["count"] for d in days)

    # Best day
    best = max(days, key=lambda d: d["count"])

    # Current streak (count backwards from today; yesterday if today = 0)
    day_map = {d["date"]: d["count"] for d in days}
    today   = date.today()
    cur     = today
    if not day_map.get(cur.isoformat(), 0):
        cur -= timedelta(days=1)          # use yesterday as anchor
    streak = 0
    while day_map.get(cur.isoformat(), 0):
        streak += 1
        cur -= timedelta(days=1)

    # Longest streak
    longest = run = 0
    for d in days:
        if d["count"] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0

    return {
        "total":          total,
        "current_streak": streak,
        "longest_streak": longest,
        "best_day":       best,
    }


# ── Main ──────────────────────────────────────────────────────────────

def fetch():
    print(f"Fetching {URL} …")
    resp = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()

    days  = parse_html(resp.text)
    stats = compute_stats(days)

    if not days:
        raise RuntimeError(
            "No contribution data found — GitHub may have changed its HTML. "
            "Check the selector in parse_html()."
        )

    output = {
        "username":       USERNAME,
        "fetched":        date.today().isoformat(),
        "days":           days,
        **stats,
    }

    Path("data").mkdir(exist_ok=True)
    out_path = Path("data/contributions.json")
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(
        f"  ✓  {len(days)} days fetched  |  "
        f"{stats['total']:,} total contributions  |  "
        f"streak: {stats['current_streak']} days  |  "
        f"best: {stats['best_day']['count']} on {stats['best_day']['date']}"
    )


if __name__ == "__main__":
    fetch()
