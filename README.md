# SkillGems — Curated AI Agent Skills Directory

**Live: https://skillgems.kuige.me/** · 中文主页：`?lang=zh`

A hand-curated, link-verified directory of **AI agent skills** (the open `SKILL.md` format). The catalog is **curated entirely by the owner** — entries are added manually, one at a time, and each link is opened and verified before it goes live. Every card explains what the skill does and how to install it, and links straight to GitHub. Verified author X profiles are linked where available; official write-ups live in the "Go deeper" section.

## Curating manually (owner workflow)

1. Open `scripts/gen_cards.py` and append an entry to `SKILLS`:

```python
S("my-entry-id", "Display Name", "author", "owner/repo", 1234, "dev",
  "English description…", "中文介绍……",
  "Install hint (EN)…", "安装提示（中文）……",
  "space separated search tags", f=False, xh=None)  # xh = verified X handle, optional
```

2. Run `python3 scripts/gen_cards.py` — it rebuilds the static cards, JSON data island, hero stats, ItemList JSON-LD, `data/catalog.json` and `llms.txt`, and swaps the empty state for the real grid.
3. Commit + push; Pages redeploys in ~1 minute.

Category is one of: `official / collections / dev / writing / design / science / security / business / toolbox`. Only add an `xh` handle after verifying the profile exists; post-level `x` links only once the post itself can be verified. The original AI-compiled 42-entry seed was removed on 2026-10-07 by owner decision and lives in git history: `git show 9650fad:scripts/gen_cards.py`.

## For AI agents

- [`/llms.txt`](https://skillgems.kuige.me/llms.txt) — llmstxt.org-style index with a quick-start for agents
- [`/data/catalog.json`](https://skillgems.kuige.me/data/catalog.json) — full machine-readable catalog

## Curation policy

- Every link is opened and verified by hand before inclusion; nothing is auto-scraped or AI-dumped.
- Quality over quantity: entries are picked for real utility and maintained status, not raw star count alone.
- Offensive-security tooling is out of scope; defensive security tooling is in.
- X links: profile links only when the handle is verified; post-level links (`x` field) are added once the post can be verified.

## Site

Single-file `index.html` (no build, no external JS), bilingual EN/中文 (`?lang=`), light/dark theme, category filters + bilingual search + sorting, JSON-LD (WebSite + FAQPage + ItemList), sitemap, robots.txt welcoming AI crawlers. Part of [kuige.me](https://kuige.me/) — 魁歌 KuiGe.
