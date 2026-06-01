#!/usr/bin/env python3
"""
ECPSE 729 — Course Site Build Script
====================================

Stitches shared chrome (head, header, nav, footer) around per-page bodies so
header/nav/footer changes happen in ONE place instead of every HTML file.

Usage:
    python build.py

Outputs (overwrites):
    index.html, module-01.html, module-02.html, module-03.html, module-04.html

To add or modify content:
    - Edit MODULES below to change module summaries, lock states, themes
    - Edit PAGES below to change titles, descriptions, header/footer text
    - Edit body files in _src/pages/<slug>.body.html for page content
    - For modules without a body file, a "Coming Soon" stub is generated
      automatically from MODULES data — write _src/pages/module-NN.body.html
      to replace the stub with real content
"""

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
SRC_PAGES = ROOT / "_src" / "pages"


# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------

LAST_UPDATED = datetime.now().strftime("%Y / %m / %d")
# Cache-bust the linked stylesheet so changes show up without manual hard-refresh.
# Uses styles.css mtime as integer seconds, so the URL changes only when CSS changes.
import os as _os
_styles_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'styles.css')
CSS_VERSION = str(int(_os.path.getmtime(_styles_path))) if _os.path.exists(_styles_path) else '1'

# Module summaries — drive both the home page cards AND the nav bar
MODULES = [
    {
        "num": "01",
        "slug": "module-01",
        "label": "Module 01",
        "status": "open",  # "open" or "locked"
        "title_html": "Foundations &amp; the<br>Self as <span class=\"ital\">Ethical Practitioner</span>",
        "meta_pips": ["WEEK 01", "SECTION 1.0", "3 PODCASTS · 2 VIDEOS · 1 READING"],
        "summary_html": "The <b>history</b> that shaped behavior-analytic ethics — Sunland, Willowbrook, FABA, the BACB. The architecture of the 2022 Code. The 11-step decision model. <b>Cultural responsiveness</b> as foundation, not afterthought.",
        "week_label": "— Now Open",
        "theme": "\"CLD<br>Ethics.\"",
        "arrow": "Enter →",
        "page_title_short": "Foundations & The Self",
        "page_subhead": "Module I · Week 1",
        "header_meta": "Module 01 · Week 01 · Section 1.0",
        "theme_label": "CLD Ethics",
    },
    {
        "num": "02",
        "slug": "module-02",
        "label": "Module 02",
        "status": "open",
        "title_html": "Effective Treatment, Clients<br>&amp; <span class=\"ital\">ABA's Critics</span>",
        "meta_pips": ["WEEK 02", "SECTIONS 2.0 + 3.0", "2 PODCASTS · 1 VIDEO · 2 READINGS"],
        "summary_html": "The <b>hardest module</b>. Effective treatment when stakeholders disagree. Assent vs. consent. Trauma-informed practice. Listening seriously to autistic self-advocacy and the ABA reckoning.",
        "week_label": "— Now Open",
        "theme": "\"Autistic<br>self-advocacy.\"",
        "arrow": "Enter →",
        "page_title_short": "Effective Treatment, Clients & ABA's Critics",
        "page_subhead": "Module II · Week 2",
        "header_meta": "Module 02 · Week 02 · Sections 2.0 + 3.0",
        "theme_label": "Autistic Self-Advocacy",
    },
    {
        "num": "03",
        "slug": "module-03",
        "label": "Module 03",
        "status": "open",
        "title_html": "Clients, Supervision <span class=\"amp\">&amp;</span> the<br><span class=\"ital\">Digital Practitioner</span>",
        "meta_pips": ["WEEK 03", "SECTIONS 3.0 + 4.0 + 5.0", "1 PODCAST · 3 VIDEOS · 3 READINGS"],
        "summary_html": "Service agreements, third-party contracts, and stakeholder management. Supervision in fieldwork, RBT, and school contexts. Testimonials and social media. <b>Telehealth.</b> AI-assisted clinical work. The restraint debates that won't go away.",
        "week_label": "— Now Open",
        "theme": "\"Relational<br>architecture.\"",
        "arrow": "Enter →",
        "page_title_short": "Clients, Supervision & the Digital Practitioner",
        "page_subhead": "Module III · Week 3",
        "header_meta": "Module 03 · Week 03 · Sections 3.0 + 4.0 + 5.0",
        "theme_label": "Relational Architecture",
    },
    {
        "num": "04",
        "slug": "module-04",
        "label": "Module 04",
        "status": "open",
        "title_html": "Public Statements, Research <span class=\"amp\">&amp;</span><br>Enforcement <span class=\"amp\">·</span> <span class=\"ital\">Becoming an Ethical BA</span>",
        "meta_pips": ["WEEK 04", "SECTIONS 5.0 + 6.0 + ENFORCEMENT", "1 PODCAST · INTERVIEW · CAPSTONE"],
        "summary_html": "Public statements and social media (§5.0). Research ethics, informed consent, and authorship (§6.0). The <b>Code-Enforcement Procedures</b> with real Notices of Disciplinary Action and the BACB Summary of Ethics Violations. Capstone integration across all four modules.",
        "week_label": "— Now Open",
        "theme": "\"The<br>capstone.\"",
        "arrow": "Enter →",
        "page_title_short": "Public Statements, Research, Enforcement & Becoming an Ethical BA",
        "page_subhead": "Module IV · Week 4",
        "header_meta": "Module 04 · Week 04 · Sections 5.0 + 6.0 + Enforcement",
        "theme_label": "The Capstone",
    },
]

# Intro nav items (rendered between Home and the modules)
INTRO_NAV = [
    {"slug": "modules", "label": "Modules", "status": "open"},
]

# Extra nav items beyond modules (Syllabus, Resources)
# An open item with a "url" links to that URL (PDF/external); otherwise it links
# to "{slug}.html". Set "external": True to open in a new tab.
EXTRA_NAV = [
    {"slug": "syllabus", "label": "Syllabus", "status": "open",
     "url": "handouts/ECPSE-729-Syllabus-Summer-2026.pdf", "external": True},
    {"slug": "resources", "label": "Resources", "status": "locked",
     "aria": "Resources — link coming soon"},
]

# External nav (Brightspace, always last, styled .bs)
EXTERNAL_NAV = [
    {"slug": "brightspace", "label": "Brightspace ↗", "status": "open",
     "url": "https://brightspace.cuny.edu/d2l/home/1270447", "extra_class": "bs"},
]

# Pages to generate
PAGES = [
    {
        "slug": "index",
        "filename": "index.html",
        "title": "ECPSE 729 — Welcome · Queens College",
        "description": "Welcome to ECPSE 729 — a 4-week asynchronous summer seminar in ethics and professionalism for the BCBA Subplan at Queens College.",
        "og_type": "website",
        "og_title": "ECPSE 729 — Welcome",
        "og_description": "Welcome to ECPSE 729 — a 4-week asynchronous summer seminar in ethics and professionalism for the BCBA Subplan at Queens College.",
        "header_right": "<span aria-hidden=\"true\">⚜</span> Summer 2026 · Vol. I",
        "footer_center": "ECPSE 729 — Summer 2026 — In Knight Red",
        "current_nav": "index",
        "body_file": "index.body.html",
    },
    {
        "slug": "modules",
        "filename": "modules.html",
        "title": "ECPSE 729 — The Curriculum · Queens College",
        "description": "Queens College ECPSE 729 — Ethics and Professionalism in Applied Behavior Analysis. The four-module curriculum at a glance.",
        "og_type": "website",
        "og_title": "ECPSE 729 — The Curriculum",
        "og_description": "Queens College ECPSE 729 — Ethics and Professionalism in Applied Behavior Analysis. The four-module curriculum at a glance.",
        "header_right": "<span aria-hidden=\"true\">⚜</span> Modules · Summer 2026",
        "footer_center": "ECPSE 729 — Summer 2026 — In Knight Red",
        "current_nav": "modules",
        "body_file": "modules.body.html",
    },
]

# Auto-add a page entry per module
for mod in MODULES:
    page_title = f"Module {mod['num']} · {mod['page_title_short']} — ECPSE 729"
    if mod["status"] == "open":
        description = (
            f"ECPSE 729 Module {mod['num']} — {mod['page_title_short']}. "
            f"Week {int(mod['num'])} of ECPSE 729 at Queens College."
        )
    else:
        description = (
            f"ECPSE 729 Module {mod['num']} — {mod['page_title_short']}. "
            f"Coming Soon. Week {int(mod['num'])} of ECPSE 729 at Queens College."
        )
    PAGES.append({
        "slug": mod["slug"],
        "filename": f"{mod['slug']}.html",
        "title": page_title,
        "description": description,
        "og_type": "article",
        "og_title": f"Module {mod['num']} · {mod['page_title_short']} — ECPSE 729",
        "og_description": description,
        "header_right": f"<span aria-hidden=\"true\">⚜</span> {mod['page_subhead']}",
        "footer_center": f"ECPSE 729 · Module {mod['num']} · {mod['page_title_short']}",
        "current_nav": mod["slug"],
        "body_file": f"{mod['slug']}.body.html",
        "module_data": mod,
    })


# ---------------------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="Dr. Lenwood Gibson, Queens College CUNY GPSE">
<meta name="theme-color" content="#a4232c">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_description}">
<meta property="og:site_name" content="Queens College CUNY GPSE">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{og_description}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="apple-touch-icon" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Italiana&family=DM+Serif+Display:ital@0;1&family=Manrope:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={css_version}">
</head>
<body>

<a class="skip-link" href="#main">Skip to main content</a>

<header class="site">
  <div class="left">QC / CUNY / GPSE</div>
  <div class="center"><a href="index.html">ECPSE <b>729</b></a></div>
  <div class="right">{header_right}</div>
</header>

<nav class="bar" aria-label="Course navigation">
{nav_items}
</nav>

<main id="main">

{body}

</main>

<footer>
  <div class="left"><span class="stamp" aria-hidden="true">⚜</span> Queens College CUNY GPSE</div>
  <div class="center">{footer_center}</div>
  <div class="right">Dr. Lenwood Gibson <span class="stamp" aria-hidden="true">⚜</span></div>
</footer>

</body>
</html>
"""

MODULE_CARD_TEMPLATE = """  <article class="module{linked_class}">
    <div class="num">{num}</div>
    <div class="body">
      <div class="meta-row">{meta_row}</div>
      <h3>{title_with_link}</h3>
      <p>{summary_html}</p>
    </div>
    <div class="side">
      <div class="week{now_class}">{week_label}</div>
      <div class="theme"><em>{theme}</em></div>
      <div class="arrow">{arrow}</div>
    </div>
  </article>"""

MODULE_STUB_TEMPLATE = """<!-- Module Hero (auto-generated stub — replace with real content in {slug}.body.html) -->
<section class="hero">
  <div class="hero-grid">
    <div>
      <div class="meta-bar">
        <span><span class="glyph" aria-hidden="true">⚜</span> &nbsp;{header_meta}</span>
        <span>Theme: {theme_label}</span>
      </div>
      <h1>{hero_h1}<span class="period-signal">.</span></h1>
      <p class="lede">{summary_html} <b>{lede_status}</b></p>
    </div>
    <div class="side-widget">
      <div class="label">— Status</div>
      <h3>{status_heading}</h3>
      <p>Resources, assignments, and the lecture module will be unlocked when this module opens. Check Brightspace announcements for the release.</p>
      <span class="submit-bs locked" aria-disabled="true">Module {num} (coming soon)</span>
    </div>
  </div>
</section>

<section class="module-section">
  <div class="section-label">Coming Soon · Module {num}</div>
  <h2>This module is being <span class="ital">prepared.</span></h2>
  <p class="section-intro">Module {num} of ECPSE 729 is in development. When it opens, you'll find learning objectives, required resources (videos, podcasts, readings) with Edpuzzle prompts, and the week's assignments here. In the meantime, focus on the currently open module and watch Brightspace for announcements.</p>

  <div class="scenario coming-soon">
    <div class="sl"><span aria-hidden="true">⚜</span> Coming Soon</div>
    <p>Module {num} content will be published here. To replace this auto-generated stub, create _src/pages/{slug}.body.html with the real module body content and re-run python build.py.</p>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# RENDERERS
# ---------------------------------------------------------------------------

def render_nav(current_nav):
    """Render the course navigation bar with the right link/locked states."""
    items = []

    home_attrs = ' class="current" aria-current="page"' if current_nav == "index" else ""
    items.append(f'  <a href="index.html"{home_attrs}>[ Home ]</a>')

    for item in INTRO_NAV:
        if item["status"] == "locked":
            items.append(
                f'  <span class="nav-locked" aria-disabled="true" '
                f'aria-label="{item.get("aria", item["label"] + " — coming soon")}">{item["label"]}</span>'
            )
        else:
            attrs = ' class="current" aria-current="page"' if item["slug"] == current_nav else ""
            items.append(f'  <a href="{item["slug"]}.html"{attrs}>{item["label"]}</a>')

    for mod in MODULES:
        if mod["status"] == "locked":
            items.append(
                f'  <span class="nav-locked" aria-disabled="true" '
                f'aria-label="{mod["label"]} — coming soon">{mod["label"]}</span>'
            )
        else:
            attrs = ' class="current" aria-current="page"' if mod["slug"] == current_nav else ""
            items.append(f'  <a href="{mod["slug"]}.html"{attrs}>{mod["label"]}</a>')

    for item in EXTRA_NAV:
        if item["status"] == "locked":
            items.append(
                f'  <span class="nav-locked" aria-disabled="true" '
                f'aria-label="{item["aria"]}">{item["label"]}</span>'
            )
        else:
            href = item.get("url", f'{item["slug"]}.html')
            tgt = ' target="_blank" rel="noopener"' if item.get("external") else ''
            items.append(f'  <a href="{href}"{tgt}>{item["label"]}</a>')

    for item in EXTERNAL_NAV:
        extra = item.get("extra_class", "")
        cls_suffix = f" {extra}" if extra else ""
        if item["status"] == "locked":
            items.append(
                f'  <span class="nav-locked{cls_suffix}" aria-disabled="true" '
                f'aria-label="{item["aria"]}">{item["label"]}</span>'
            )
        else:
            href = item.get("url", "#")
            items.append(
                f'  <a href="{href}" target="_blank" rel="noopener" class="{extra}">{item["label"]}</a>'
            )

    return "\n".join(items)


def render_module_cards():
    """Render the four summary cards for the home page."""
    cards = []
    pip = '<span class="pip" aria-hidden="true">⚜</span>'
    for mod in MODULES:
        linked_class = " linked" if mod["status"] == "open" else ""
        now_class = " now" if mod["status"] == "open" else ""

        meta_parts = []
        for i, p in enumerate(mod["meta_pips"]):
            if i > 0:
                meta_parts.append(pip)
            meta_parts.append(f"<span>{p}</span>")
        meta_row = "".join(meta_parts)

        if mod["status"] == "open":
            title_with_link = f'<a href="{mod["slug"]}.html">{mod["title_html"]}</a>'
        else:
            title_with_link = mod["title_html"]

        cards.append(MODULE_CARD_TEMPLATE.format(
            linked_class=linked_class,
            num=mod["num"],
            meta_row=meta_row,
            title_with_link=title_with_link,
            summary_html=mod["summary_html"],
            now_class=now_class,
            week_label=mod["week_label"],
            theme=mod["theme"],
            arrow=mod["arrow"],
        ))
    return "\n\n".join(cards)


def render_stub_body(mod):
    """Render a Coming-Soon body for a locked module that has no body file."""
    # Convert title HTML to a hero h1 by stripping <br> for cleaner display
    hero_h1 = mod["title_html"]
    return MODULE_STUB_TEMPLATE.format(
        slug=mod["slug"],
        num=mod["num"],
        header_meta=mod["header_meta"],
        theme_label=mod["theme_label"],
        hero_h1=hero_h1,
        summary_html=mod["summary_html"],
        lede_status=f"Opens in Week {int(mod['num'])}.",
        status_heading=f"Module {mod['num']} Opens Week {int(mod['num'])}",
    )


# ---------------------------------------------------------------------------
# BUILDER
# ---------------------------------------------------------------------------

def get_body(page):
    """Return the body for a page — from disk if present, else stub."""
    body_path = SRC_PAGES / page["body_file"]
    if body_path.exists():
        return body_path.read_text(encoding="utf-8").rstrip()

    # Fall back to stub for modules
    if "module_data" in page:
        return render_stub_body(page["module_data"]).rstrip()

    raise FileNotFoundError(
        f"No body file at {body_path} and no module_data fallback for "
        f"page '{page['slug']}'. Create the body file or add module_data."
    )


def build_page(page):
    body = get_body(page)

    # Substitute MODULE_CARDS placeholder (used in index.body.html)
    body = body.replace("{{MODULE_CARDS}}", render_module_cards())
    body = body.replace("{{LAST_UPDATED}}", LAST_UPDATED)

    nav_items = render_nav(page["current_nav"])

    html = PAGE_TEMPLATE.format(
        title=page["title"],
        description=page["description"],
        og_type=page["og_type"],
        og_title=page["og_title"],
        og_description=page["og_description"],
        header_right=page["header_right"],
        footer_center=page["footer_center"],
        nav_items=nav_items,
        body=body,
        css_version=CSS_VERSION,
    )

    output_path = ROOT / page["filename"]
    output_path.write_text(html, encoding="utf-8")
    return output_path


def main():
    print(f"Building site in {ROOT}")
    print(f"Last updated: {LAST_UPDATED}")
    print()
    for page in PAGES:
        path = build_page(page)
        body_source = "body file" if (SRC_PAGES / page["body_file"]).exists() else "STUB"
        print(f"  built  {path.name:20s}  ({body_source})")
    print()
    print(f"Done — {len(PAGES)} page(s) generated.")


if __name__ == "__main__":
    main()
