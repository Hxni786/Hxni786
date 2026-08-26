# Setup Guide — Cipher Stack GitHub Profile Art

## Prerequisites
- Python 3.10+
- Git + GitHub CLI (`gh`) installed
- Your own photo (any size, JPG/PNG)

---

## Step 1 — Create the magic repo

GitHub renders `<username>/<username>/README.md` at the top of your profile.

```bash
gh repo create Hxni786 --public --clone
cd Hxni786
mkdir -p scripts data .github/workflows
```

Copy every file from this package into the repo root keeping folder structure.

---

## Step 2 — Install dependencies (local)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r scripts/requirements.txt
```

> **Note:** `rembg` downloads a ~180 MB U2Net model on first run.
> If you're on a slow connection, run `python -m rembg` once before prepping the photo.

---

## Step 3 — Prep your photo (run once)

Put your photo in the repo root and run:

```bash
python scripts/prep_photo.py source-photo.jpg
# → writes source-prepped.png
```

This removes the background, boosts local contrast (CLAHE), and composites on white so the ASCII art has clean highlights and shadows.

---

## Step 4 — Generate the ASCII SVG

```bash
python scripts/make_ascii_svg.py
# → writes hxni-ascii.svg
```

Tweak `COLS` in `make_ascii_svg.py` (default 80) if you want more/less density.

---

## Step 5 — Generate the info card SVG

Edit `FIELDS` in `make_info_card.py` if you want different text, then:

```bash
python scripts/make_info_card.py
# → writes info-card.svg
```

Preview locally: `STATIC=1 python scripts/make_info_card.py` for a frozen frame.

---

## Step 6 — Fetch your live contribution data

```bash
python scripts/fetch_contributions.py
# → writes data/contributions.json
```

---

## Step 7 — Render the heatmap SVG

```bash
python scripts/render_heatmap_svg.py
# → writes contrib-heatmap.svg
```

---

## Step 8 — Preview

Open `README.md` in VS Code with the Markdown preview, or push and check your GitHub profile.

---

## Step 9 — Commit and push

```bash
git add .
git commit -m "feat: add animated profile art"
git push -u origin main
```

Visit `github.com/Hxni786` — your README is live.

---

## Step 10 — Enable the daily refresh

The workflow `.github/workflows/update-profile-art.yml` auto-runs at 06:17 UTC (11:17 PKT) every day.

Trigger it once manually to verify it works:
1. Go to your repo → **Actions** tab
2. Select **"Refresh contribution heatmap"**
3. Click **"Run workflow"**

It should commit a fresh `contrib-heatmap.svg` within ~30 seconds.

---

## Updating your photo

When you want a new portrait, replace `source-photo.jpg` and rerun Steps 3–4:

```bash
python scripts/prep_photo.py source-photo.jpg
python scripts/make_ascii_svg.py
git add hxni-ascii.svg source-prepped.png
git commit -m "feat: update portrait"
git push
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| ASCII portrait looks like a dark blob | Re-run `prep_photo.py` — lighting preprocess is key |
| No contribution data fetched | GitHub changed HTML — update selector in `fetch_contributions.py` |
| Workflow fails with `ModuleNotFoundError` | Verify `requirements-ci.txt` path in workflow matches repo structure |
| SVG not animating on GitHub | GitHub only animates SVG inside `<img>` tags — do not use `<object>` |
