#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkillGems catalog — single source of truth.
Every entry below was verified via the GitHub API on VERIFIED_DATE
(full_name + stargazers_count + description fetched live; 404s dropped).
Adds/moves stars daily -> rerun:  python3 scripts/gen_cards.py
Regenerates (do NOT hand-edit these regions in index.html):
  - static cards        <!--CARDS:START/END-->
  - JSON data island    /*DATA:START*/ ... /*DATA:END*/
  - stats               <!--STATS:START/END-->
  - ItemList JSON-LD    <!--JSONLDLIST:START/END-->
  - data/catalog.json, llms.txt
Zero-entry mode: hides hero stats, injects a bilingual empty state into the grid,
and skips the ItemList JSON-LD until the first curated entry lands.
"""

import json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
SITE = "https://skillgems.kuige.me"
VERIFIED = "2026-10-07"
CATS = ["official","collections","dev","writing","design","science","security","business","toolbox"]

def S(id, n, a, repo, st, c, de, dz, h, hz, t, f=False, xh=None):
    return {"id": id, "n": n, "a": a, "u": "https://github.com/" + repo, "st": st, "c": c,
            "de": de, "dz": dz, "h": h, "hz": hz, "t": t, "f": f, "xh": xh, "x": None}

# Catalog is curated MANUALLY by the owner (2026-10-07 decision: 清空目录，站长手动精选添加).
# To add an entry, append S(...) dicts to SKILLS below and rerun this script.
# The original AI-compiled 42-entry seed (stars verified 2026-10-07) lives in git history:
#   git show 9650fad:scripts/gen_cards.py
SKILLS = [
]

EMPTY_HTML = ('<div class="empty" id="emptyState"><b data-i18n="emptyT">The catalog is being curated by hand.</b><br>'
              '<span data-i18n="emptyD">Entries are added one at a time — each link opened and verified before it goes live. Check back soon.</span></div>')










































# ---------- derived ----------
def fmt_k(n):
    if n >= 1e6: return ("%.2f" % (n/1e6)).rstrip("0").rstrip(".") + "M"
    if n >= 1000: return ("%.1f" % (n/1e3)).rstrip("0").rstrip(".") + "k"
    return str(n)

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def assert_sub(html, pat, label):
    if not re.search(pat, html):
        raise SystemExit("PATTERN MISSING (%s): %r" % (label, pat[:80]))

def build_card(s):
    cls = " feat" if s["f"] else ""
    feat = '<span class="c-feat" title="Featured">★</span>' if s["f"] else ""
    xchip = ""
    if s["xh"]:
        xchip = ' <a class="xchip" href="https://x.com/%s" target="_blank" rel="noopener" title="https://x.com/%s">𝕏 @%s</a>' % (s["xh"], s["xh"], s["xh"])
    stars = "{:,}".format(s["st"])
    return f'''<article class="card{cls}" data-id="{s["id"]}">
  <div class="c-top"><h3>{esc(s["n"])}{feat}</h3><span class="c-cat" data-cat="{s["c"]}"></span></div>
  <p class="c-desc" data-zh="{esc(s["dz"])}">{esc(s["de"])}</p>
  <p class="c-how"><b>⚙</b> <span data-zh="{esc(s["hz"])}">{esc(s["h"])}</span></p>
  <div class="c-meta"><span>{esc(s["a"])}</span>{xchip}<span class="stars" title="{stars}">★ {fmt_k(s["st"])}</span></div>
  <div class="c-actions"><a class="btn pri" href="{s["u"]}" target="_blank" rel="noopener">⭐ <span class="gh-t">GitHub</span> ↗</a></div>
</article>'''

def main():
    total = sum(s["st"] for s in SKILLS)
    n = len(SKILLS)
    ncats = len({s["c"] for s in SKILLS})
    ordered = sorted(SKILLS, key=lambda s: (not s["f"], -s["st"]))

    html = open(INDEX, encoding="utf-8").read()

    # cards
    m = re.search(r"(<!--CARDS:START-->)(.*?)(<!--CARDS:END-->)", html, re.S)
    assert m, "CARDS markers missing"
    body = ("\n" + "\n".join(build_card(s) for s in ordered) + "\n") if SKILLS else ("\n" + EMPTY_HTML + "\n")
    html = html[:m.start(2)] + body + html[m.end(2):]

    # data island (content only — the object braces live outside the markers in index.html)
    payload = json.dumps({"d": VERIFIED, "s": [{k: s[k] for k in ("id","n","a","u","st","c","de","dz","h","hz","t","f","xh","x")} for s in SKILLS]}, ensure_ascii=False, separators=(",",":")).replace("</", "<\\/")
    payload = payload[1:-1]
    m = re.search(r"(/\*DATA:START\*/)(.*?)(/\*DATA:END\*/)", html, re.S)
    assert m, "DATA markers missing"
    html = html[:m.start(2)] + payload + html[m.end(2):]

    # stats
    m = re.search(r"(<!--STATS:START-->)(.*?)(<!--STATS:END-->)", html, re.S)
    assert m, "STATS markers missing"
    if n:
        stats = ('<div class="stats">\n'
                 f'      <div class="stat"><b id="stSkills">{n}</b><span data-i18n="statSkills">Skills &amp; collections</span></div>\n'
                 f'      <div class="stat"><b id="stCats">{ncats}</b><span data-i18n="statCats">Categories</span></div>\n'
                 f'      <div class="stat"><b id="stStars">{fmt_k(total)}</b><span data-i18n="statStars">Combined GitHub stars</span></div>\n'
                 f'      <div class="stat"><b id="stDate">{VERIFIED}</b><span data-i18n="statVerified">Links verified</span></div>\n'
                 '    </div>')
    else:
        stats = '<!-- stats appear with the first curated entry -->'
    html = html[:m.start(2)] + stats + html[m.end(2):]

    # entry counters (hidden by JS when the catalog is empty)
    html = html.replace('<b id="cnt">42</b>', f'<b id="cnt">{n}</b>').replace('<b id="cntAll">42</b>', f'<b id="cntAll">{n}</b>')

    # ItemList JSON-LD
    ld = ""
    if n:
        items = [{"@type":"ListItem","position":i+1,"name":s["n"],"url":s["u"]} for i, s in enumerate(ordered)]
        ld = '\n<script type="application/ld+json">\n' + json.dumps({"@context":"https://schema.org","@type":"ItemList","name":"SkillGems catalog","numberOfItems":n,"itemListElement":items}, ensure_ascii=False) + "\n</script>\n"
    m = re.search(r"(<!--JSONLDLIST:START-->)(.*?)(<!--JSONLDLIST:END-->)", html, re.S)
    assert m, "JSONLD markers missing"
    html = html[:m.start(2)] + ld + html[m.end(2):]

    open(INDEX, "w", encoding="utf-8").write(html)

    # machine-readable catalog for AI agents
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    catalog = {
        "site": SITE, "generated": datetime.date.today().isoformat(), "verified": VERIFIED,
        "count": n, "total_stars": total,
        "skills": [{"id": s["id"], "name": s["n"], "author": s["a"], "url": s["u"], "stars": s["st"],
                    "category": s["c"], "description_en": s["de"], "description_zh": s["dz"],
                    "how_en": s["h"], "how_zh": s["hz"], "tags": s["t"].split(),
                    "featured": s["f"],
                    **({"x_profile": "https://x.com/" + s["xh"]} if s["xh"] else {}),
                    **({"x_post": s["x"]} if s.get("x") else {})} for s in SKILLS]}
    with open(os.path.join(ROOT, "data", "catalog.json"), "w", encoding="utf-8") as fp:
        json.dump(catalog, fp, ensure_ascii=False, indent=1)

    # llms.txt (llmstxt.org style)
    L = [f"# SkillGems", "",
         (f"> Curated, link-verified directory of {n} AI agent skills (SKILL.md format). Every entry is hand-picked and manually added by the curator; each link is opened and verified before it goes live. Agents: fetch {SITE}/data/catalog.json for the machine-readable catalog (currently {n} entries — the catalog fills up as curation proceeds)."), "",
         "## Quick start for agents", "",
         f"1. Fetch {SITE}/data/catalog.json (JSON: id, name, author, url, stars, category, bilingual descriptions, install hints).",
         "2. Filter by `category` (official/collections/dev/writing/design/science/security/business/toolbox) or search `tags`.",
         "3. Open the entry's GitHub `url` and follow its README for the exact install path (default: copy the skill folder to `~/.claude/skills/`).",
         "4. Treat skills as code: review contents and license before installing.", ""]
    for c in CATS:
        entries = [s for s in SKILLS if s["c"] == c]
        if not entries: continue
        L.append(f"## {c.capitalize()} ({len(entries)})")
        L.append("")
        for s in sorted(entries, key=lambda x: -x["st"]):
            L.append(f"- [{s['n']}]({s['u']}): {s['de']} (★{fmt_k(s['st'])})")
        L.append("")
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(L))

    print(f"OK: {n} skills, {ncats} cats, total stars {total:,} ({fmt_k(total)}) -> index.html, data/catalog.json, llms.txt")

if __name__ == "__main__":
    main()
