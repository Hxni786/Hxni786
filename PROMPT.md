# 🚀 Master AI Prompt Guide — Build Your Own Animated Cinematic GitHub Profile

This document contains the **exact, all-in-one system prompt** you can give to **Claude** (Claude 3.5 Sonnet / Claude 3.7 Sonnet) or any advanced AI coding assistant to build this exact animated GitHub profile for your own account from scratch.

---

## 📋 How to Use This Prompt
1. Copy the entire prompt in the box below.
2. Fill in the **[USER CONFIGURATION]** section with your details (GitHub username, social links, tech stack, portfolio URL, projects).
3. Paste it directly into Claude.
4. Drop your photo (e.g., `hero.png`) into your workspace.
5. Claude will generate the scripts, workflows, and README file automatically!

---

## 🤖 Copy-Paste Master Prompt for Claude

```markdown
You are an expert full-stack developer and SVG graphics engineer. Your goal is to build a complete, production-ready, ultra-cinematic, animated GitHub Profile README and automated daily update system for my GitHub profile.

### [USER CONFIGURATION]
- GitHub Username: [YOUR_GITHUB_USERNAME]
- Full Name: [YOUR_NAME]
- Title / Headline: [YOUR_TITLE] (e.g., Full Stack Engineer • React Architect • 3D Web Craftsman)
- Location: [YOUR_LOCATION] (e.g., Islamabad, Pakistan | PKT UTC+5)
- Email: [YOUR_EMAIL]
- Portfolio URL: [YOUR_PORTFOLIO_URL]
- Social Links:
  - LinkedIn: [YOUR_LINKEDIN_URL]
  - Instagram: [YOUR_INSTAGRAM_URL]
  - Facebook: [YOUR_FACEBOOK_URL]
- Frontend Stack: [e.g., React, TypeScript, Vite, Tailwind CSS, Three.js, Framer Motion]
- Backend Stack: [e.g., Node.js, Express, Python, MySQL, Supabase, Firebase]
- Mobile Stack: [e.g., React Native, Flutter]
- Tools: [e.g., Git, GitHub, VS Code, Postman, Vercel, Netlify]
- Featured Projects (up to 8 with links and titles):
  1. Title: [PROJECT_1] | URL: [URL_1] | Subtitle: [SUBTITLE_1]
  2. Title: [PROJECT_2] | URL: [URL_2] | Subtitle: [SUBTITLE_2]
  3. Title: [PROJECT_3] | URL: [URL_3] | Subtitle: [SUBTITLE_3]
  4. Title: [PROJECT_4] | URL: [URL_4] | Subtitle: [SUBTITLE_4]

---

### [TECHNICAL SPECIFICATIONS & DELIVERABLES]

Please create the following files in the project workspace:

#### 1. `scripts/prep_photo.py`
A Python script using `rembg` (U2Net) and `PIL` / `cv2`:
- Takes an input portrait photo (e.g., `hero.png`).
- Removes the background cleanly.
- Applies contrast enhancement (CLAHE) and crops/resizes appropriately.
- Saves the output as `source-prepped.png`.

#### 2. `scripts/make_ascii_svg.py`
A Python script that:
- Reads `source-prepped.png`.
- Converts pixels to ASCII characters using a custom brightness-to-character ramp (` .`:-=+*cs#%@`).
- Generates `hxni-ascii.svg` with gold monospace typography (`#D4AF37`) inside a sleek `#0d0d0d` terminal card with rounded corners and border.
- Implements animated line-by-line reveal using CSS keyframe animations (`@keyframes fin`) and SMIL `<clipPath>` wipe so it animates reliably inside GitHub README `<img>` tags.

#### 3. `scripts/make_info_card.py`
A Python script that generates `info-card.svg`:
- Neofetch / terminal system info style matching the height of the ASCII portrait.
- Top bar with macOS-style decorative dots (red/yellow/green) and header title `"The Cipher Stack"`.
- Gold key labels and silver value labels showcasing OS, Host, Role, Tech Stack, Socials, Portfolio Web URL, and GitHub.
- CSS keyframe staggered fade-in per line.

#### 4. `scripts/fetch_contributions.py`
A Python script that:
- Scrapes the public GitHub contribution calendar for `[YOUR_GITHUB_USERNAME]` (no API key required).
- Parses daily contribution levels and counts.
- Calculates total contributions, current streak, longest streak, and best day.
- Saves raw data and metrics into `data/contributions.json`.

#### 5. `scripts/render_heatmap_svg.py`
A Python script that:
- Reads `data/contributions.json`.
- Renders a custom, high-resolution SVG contribution heatmap (`contrib-heatmap.svg`) with custom color gradients matching the profile theme.

#### 6. `.github/workflows/update-profile-art.yml`
A GitHub Actions workflow that:
- Runs automatically on a daily cron schedule (e.g., every morning UTC).
- Also supports `workflow_dispatch` manual triggers.
- Runs `fetch_contributions.py` and `render_heatmap_svg.py`.
- Commits and pushes any updated `contrib-heatmap.svg` and `data/contributions.json` back to `main` with `[skip ci]`.

#### 7. `scripts/requirements.txt` & `scripts/requirements-ci.txt`
- Full requirements: `requests`, `beautifulsoup4`, `pillow`, `numpy`, `opencv-python-headless`, `rembg[cpu]`.
- CI requirements (lightweight): `requests`, `beautifulsoup4`.

#### 8. `README.md`
A master profile README structured with GitHub Flavored Markdown:
1. **Top Section: Terminal Portrait & Info Card**:
   - `<h3><code>The Cipher Stack</code></h3>`
   - Two-column table containing `<img src="./hxni-ascii.svg" width="370" />` and `<img src="./info-card.svg" width="490" />`.
2. **Middle Section: Cinematic Header**:
   - Venom-style animated banner from Capsule Render.
   - Profile views badge, open-to-work badge, and location badge.
   - Typing SVG animation banner cycling through impactful developer quotes.
3. **Third Section: Live Contribution Heatmap**:
   - `<h3><code>Contributions</code></h3>`
   - `<img src="./contrib-heatmap.svg" width="860" />`.
4. **Featured Gallery**:
   - 2-column responsive HTML table linking to top projects with preview images and descriptions.
5. **Tech Arsenal**:
   - Dark theme Skillicons badge grids organized by Frontend/3D, Backend/Database, Mobile, and Tools/DevOps.
6. **What I'm Up To**:
   - Clean markdown table for Currently Building, Learning, and Fun Facts.
7. **Achievements**:
   - Official GitHub achievement badges (Pair Extraordinaire, Pull Shark, YOLO, Starstruck).
8. **Socials & Connect**:
   - `<h3><code>Socials</code></h3>`
   - Custom Shields.io badges for LinkedIn, Instagram, Facebook, Gmail, GitHub, and Portfolio.
   - Dynamic QR code generator widget pointing to the live portfolio URL.
   - Footer wave banner.

---

### [EXECUTION STEPS]
1. Generate all the script files and workflows.
2. Initialize virtual environment and install dependencies.
3. Run the scripts in sequence:
   `python scripts/prep_photo.py hero.png`
   `python scripts/make_ascii_svg.py`
   `python scripts/make_info_card.py`
   `python scripts/fetch_contributions.py`
   `python scripts/render_heatmap_svg.py`
4. Assemble and verify the complete `README.md`.
```
