# ECPSE 729 — Where We Left Off (2026-05-05)

Status: Module 01 is production-ready. Modules 02-04 are stubs. Codex review punch list complete (MUST-FIX + SHOULD-FIX + NICE-TO-HAVE all addressed). Site uses a Python build system (`build.py` + `BUILD.md`).

## What's done

**Accessibility (Codex MUST-FIX, all 7):**
- Dead placeholder `href="#"` links converted to `nav-locked` / `btn-locked` non-focusable spans with `aria-disabled="true"` and descriptive `aria-label`s
- Lecture Module disabled link converted to a real disabled control
- Skip link + `<main id="main">` landmark on every page
- Module 01 card on home: `onclick` removed; stretched-link CSS pattern + `:focus-within` keeps it clickable AND keyboard-accessible
- Mobile nav wraps cleanly via `flex-wrap: wrap`
- Knight resources preview section added to home page (was missing vs. mockup)
- Knight typography values restored (side-widget h3, section-head padding/h2, module h3, preview-dark h3)

**Maintainability (Codex SHOULD-FIX, all 7):**
- Shared chrome (head, header, nav, footer) extracted to `build.py` PAGE_TEMPLATE
- Module summary cards generated from MODULES data
- Module 02-04 stub bodies auto-generated from MODULES data
- meta description, OG, Twitter, favicon, theme-color, apple-touch-icon added to all pages
- All 11 inline `style=` attributes extracted into utility classes (`.period-signal`, `.section-intro`, `.scenario.coming-soon`, `.pill.done`, `.preview-dark-note`)
- `@media print` stylesheet added (hides nav/footer/iframes/locked actions, simplifies colors, preserves URLs after links)
- `loading="lazy"` + `referrerpolicy="strict-origin-when-cross-origin"` on YouTube iframes

**Polish (Codex NICE-TO-HAVE):**
- Decorative ⚜ glyphs wrapped in `aria-hidden="true"` spans
- Card hover/cursor pattern: kept the more accessible "only `.linked` cards are clickable" — Knight mockup's "all cards cursor:pointer" was a regression in clarity
- "Lecture Module" label kept (canonical going forward, not "Nearpod 1")

## What needs YOUR input next

### 1. Real URLs (highest leverage — unlocks the whole site)

When you have these URLs in hand, search `_src/pages/module-01.body.html` for the relevant locked element and swap. Pattern:

```html
<!-- before -->
<span class="btn btn-edpuzzle btn-locked" aria-disabled="true">Open in Edpuzzle (link pending)</span>

<!-- after -->
<a href="https://edpuzzle.com/assignments/..." target="_blank" rel="noopener" class="btn btn-edpuzzle">Open in Edpuzzle ↗</a>
```

URLs needed:
- [ ] Brightspace course root URL (replaces `<span class="nav-locked bs">` in build.py PAGE_TEMPLATE → also lets you replace 6 nav locked spans in build.py: Module 02/03/04, Syllabus, Resources, Brightspace)
- [ ] Edpuzzle assignment URLs (5× — Willowbrook 1, Willowbrook 2/Unforgotten, BACB Ep. 6, BACB Ep. 15, JABA Series 12)
- [ ] Decision Lab 1 rubric (PDF) URL
- [ ] Toolkit Artifact 1 template (Word) URL
- [ ] Brightspace assignment submission URLs (4× — Decision Lab, Toolkit, Lecture Module, Podcast Discussion)
- [ ] Brightspace ethical-scenario document URL (Module 03 prep)
- [ ] Lecture Module 1 published URL (when you publish it)

After each swap, run `python build.py`. (Or just edit the generated HTML for the immediate Module 01 changes — the build script would overwrite though, so prefer editing the body files.)

### 2. Modules 02-04 content

Modules 02/03/04 currently render as auto-generated "Coming Soon" stubs. To replace with real content:

1. Copy `_src/pages/module-01.body.html` to `_src/pages/module-02.body.html`.
2. Adapt the content to Module 02's themes (Effective Treatment, Clients & ABA's Critics — Sections 2.0 + 3.0; theme: Autistic self-advocacy).
3. Run `python build.py`.

Consult MODULES list in `build.py` for the canonical metadata for each module (titles, themes, meta pips).

### 3. Pre-existing visual polish (not blocking, defer until comfortable)

- Hero `<h1>` floor font-size of 56px clips long words like "Professionalism" at 375px-wide mobile. Knight mockup has the same issue. Quick fix: lower the clamp floor in `styles.css` `.hero h1` or add `word-break: break-word`.

## How to verify the site visually

```bash
# from the 729_course_site folder
python -m http.server 8729
# then open http://localhost:8729 in a browser
```

Or use the `ecpse729-site` profile in `.claude/launch.json` (Claude Code preview).

## How to make global changes

- Header / nav / footer / `<head>` meta → edit `build.py` (PAGE_TEMPLATE), then `python build.py`
- Module summaries on home page → edit `build.py` (MODULES list), then re-run
- Lock / unlock a module → change `"status"` in MODULES from `"locked"` to `"open"`, re-run
- Page content → edit `_src/pages/<slug>.body.html`, re-run

Full reference in `BUILD.md`.
