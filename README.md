# SkillGems — Curated AI Agent Skills Directory

**Live: https://skillgems.kuige.me/** · 中文主页：`?lang=zh`

A hand-curated, link-verified directory of **AI agent skills** (the open `SKILL.md` format): official releases from Anthropic / Microsoft / Cloudflare / Angular / LambdaTest, flagship community frameworks, and the strongest collections — each card explains what it does and how to install it, and links straight to GitHub. Where an author's X presence is verified, their profile is linked; official write-ups live in the "Go deeper" section.

## Data pipeline (single source of truth)

All 42 entries live in **`scripts/gen_cards.py`** (name, repo, stars, category, bilingual description, install hint, tags, verified X handle). Regenerate everything with:

```bash
python3 scripts/gen_cards.py
```

which rewrites in `index.html`: the static cards (`<!--CARDS:START/END-->`), the JSON data island (`/*DATA:START/END*/`), hero stats (`<!--STATS:START/END-->`) and the ItemList JSON-LD (`<!--JSONLDLIST:START/END-->`), plus `data/catalog.json` and `llms.txt`. **Never hand-edit those regions** — add/edit entries in `SKILLS` and rerun.

Stars were fetched live from the GitHub API on **2026-10-07**; rerun after updating `st` values (or re-verify via `gh api repos/<owner>/<repo>`).

## For AI agents

- [`/llms.txt`](https://skillgems.kuige.me/llms.txt) — llmstxt.org-style index with a quick-start for agents
- [`/data/catalog.json`](https://skillgems.kuige.me/data/catalog.json) — full machine-readable catalog

## Curation policy

- Every link is opened and verified by hand before inclusion; the verification date is shown on the page.
- Quality over quantity: entries are picked for real utility and maintained status, not raw star count alone.
- Offensive-security tooling is out of scope; defensive security tooling is in.
- X links: profile links only when the handle is verified; post-level links (`x` field) are added once the post can be verified.

## Site

Single-file `index.html` (no build, no external JS), bilingual EN/中文 (`?lang=`), light/dark theme, category filters + bilingual search + sorting, JSON-LD (WebSite + FAQPage + ItemList), sitemap, robots.txt welcoming AI crawlers. Part of [kuige.me](https://kuige.me/) — 魁歌 KuiGe.
