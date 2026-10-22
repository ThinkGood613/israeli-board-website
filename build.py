#!/usr/bin/env python3
"""Build the bilingual static site.

Page bodies live in pages/<lang>/<name>.html. Each starts with two comment
lines giving the page title and meta description:

    <!-- title: About the Board -->
    <!-- description: Mission, governance and board members. -->

Hebrew pages are written to docs/, English pages to docs/en/.
Run:  python3 build.py
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ROOT / "pages"
STATIC = ROOT / "static"
OUT = ROOT / "docs"  # GitHub Pages serves this folder

# Placeholder organisation details — replace with the board's real ones.
SITE = {
    "he": {
        "name": "ICBAP – המועצה הישראלית להסמכת אנשי מקצוע בהתמכרויות",
        "sub": "מועצה חברה ב-IC&amp;RC",
        "dir": "rtl",
        "prefix": "",  # path from site root
        "other_label": "English",
        "skip": "דלג לתוכן הראשי",
        "menu": "תפריט",
        "nav": [
            ("about", "אודות"),
            ("certifications", "הסמכות"),
            ("apply", "הגשה ובחינה"),
            ("renew", "חידוש והשתלמויות"),
            ("ethics", "אתיקה ותלונות"),
            ("faq", "שאלות נפוצות"),
            ("contact", "צור קשר"),
        ],
        "cta": ("verify", "אימות בעל הסמכה"),
        "utility": [("apply#portal", "הגשת מועמדות ל-CASAP"), ("accessibility", "הצהרת נגישות")],
        "phone": "+1-786-368-5900",
        "email": "doctorj@live.com",
        "footer_about": "המועצה הישראלית להסמכת אנשי מקצוע בהתמכרויות (ICBAP) היא מועצה חברה בקונסורציום הבינלאומי להסמכה והדדיות (IC&amp;RC), ומעניקה את הסמכת CASAP — המקבילה הישראלית להסמכת יועץ אלכוהול וסמים (ADC) של IC&amp;RC.<br>3303 Flamingo Drive, Miami Beach, FL 33140, USA",
        "footer_cols": [
            ("הסמכה", [("certifications", "מסלולי הסמכה"), ("apply", "איך מגישים"), ("apply#exam", "הבחינה"), ("renew", "חידוש הסמכה")]),
            ("לציבור", [("verify", "אימות בעל הסמכה"), ("ethics#complaint", "הגשת תלונה"), ("ethics", "קוד האתיקה"), ("faq", "שאלות נפוצות")]),
            ("המועצה", [("about", "אודות"), ("about#board", "חברי המועצה"), ("renew#providers", "ספקי השתלמויות"), ("contact", "צור קשר")]),
        ],
        "rights": "כל הזכויות שמורות.",
        "disclaimer": "ההסמכה של המועצה היא הסמכה מקצועית וולונטרית ואינה מחליפה רישוי או הכרה על פי דין מטעם משרד הבריאות, משרד הרווחה או כל רשות מוסמכת אחרת.",
    },
    "en": {
        "name": "Israel Certification Board of Addiction Professionals",
        "sub": "ICBAP · An IC&amp;RC Member Board",
        "dir": "ltr",
        "prefix": "en/",
        "other_label": "עברית",
        "skip": "Skip to main content",
        "menu": "Menu",
        "nav": [
            ("about", "About"),
            ("certifications", "Certifications"),
            ("apply", "Apply & Exam"),
            ("renew", "Renew & CE"),
            ("ethics", "Ethics"),
            ("faq", "FAQ"),
            ("contact", "Contact"),
        ],
        "cta": ("verify", "Verify a Professional"),
        "utility": [("apply#portal", "Apply for CASAP"), ("accessibility", "Accessibility")],
        "phone": "+1-786-368-5900",
        "email": "doctorj@live.com",
        "footer_about": "The Israel Certification Board of Addiction Professionals (ICBAP) is a member board of the International Certification &amp; Reciprocity Consortium (IC&amp;RC). It awards the CASAP credential, Israel's equivalent of the IC&amp;RC Alcohol &amp; Drug Counselor (ADC) credential.<br>3303 Flamingo Drive, Miami Beach, FL 33140, USA",
        "footer_cols": [
            ("Certification", [("certifications", "Credentials"), ("apply", "How to Apply"), ("apply#exam", "The Exam"), ("renew", "Recertification")]),
            ("For the Public", [("verify", "Verify a Professional"), ("ethics#complaint", "File a Complaint"), ("ethics", "Code of Ethics"), ("faq", "FAQ")]),
            ("The Board", [("about", "About Us"), ("about#board", "Board Members"), ("renew#providers", "CE Providers"), ("contact", "Contact")]),
        ],
        "rights": "All rights reserved.",
        "disclaimer": "Board certification is a voluntary professional credential. It does not replace any license or statutory recognition granted by the Ministry of Health, the Ministry of Welfare or any other competent authority.",
    },
}

LOGO = """<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#0c2340"/><path d="M24 9l12 5v9c0 8-5.2 13.6-12 16-6.8-2.4-12-8-12-16v-9z" fill="none" stroke="#129a98" stroke-width="2.6"/><path d="M18.5 24.5l4 4 7.5-8" fill="none" stroke="#c9a227" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>"""


def href(lang, target, depth_prefix):
    """Link from a page in `lang` to page `target` (may contain #anchor)."""
    name, _, anchor = target.partition("#")
    url = f"{depth_prefix}{SITE[lang]['prefix']}{name}.html"
    return url + (f"#{anchor}" if anchor else "")


def render(lang, name, title, description, body):
    s = SITE[lang]
    other = "en" if lang == "he" else "he"
    up = "../" if s["prefix"] else ""  # relative path back to site root
    def link(t):
        return href(lang, t, up)

    nav_items = "\n".join(
        f'        <li><a href="{link(k)}"{" aria-current=\"page\"" if k == name else ""}>{label}</a></li>'
        for k, label in s["nav"]
    )
    cta_k, cta_label = s["cta"]
    utility = "\n".join(f'        <a href="{link(k)}">{label}</a>' for k, label in s["utility"])
    footer_cols = "\n".join(
        f'      <div><h4>{h}</h4><ul>'
        + "".join(f'<li><a href="{link(k)}">{lbl}</a></li>' for k, lbl in items)
        + "</ul></div>"
        for h, items in s["footer_cols"]
    )
    other_url = href(other, name, up)
    full_title = s["name"] if name == "index" else f"{title} | {s['name']}"

    return f"""<!doctype html>
<html lang="{lang}" dir="{s['dir']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="noindex, nofollow">  <!-- draft: remove before launch -->
  <link rel="alternate" hreflang="{lang}" href="{href(lang, name, up)}">
  <link rel="alternate" hreflang="{other}" href="{other_url}">
  <link rel="icon" href="{up}assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Source+Sans+3:wght@400;600;700;800&family=Source+Serif+4:wght@600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{up}assets/css/style.css">
</head>
<body>
  <a class="skip-link" href="#main">{s['skip']}</a>
  <div class="utility-bar">
    <div class="container">
      <div class="utility-links">
{utility}
      </div>
      <a class="lang-switch" href="{other_url}" hreflang="{other}" lang="{other}">{s['other_label']}</a>
    </div>
  </div>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="{link('index')}">
        {LOGO}
        <span class="brand-text"><span class="brand-name">{s['name']}</span><span class="brand-sub">{s['sub']}</span></span>
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="main-nav" aria-label="{s['menu']}"><span></span><span></span><span></span></button>
      <nav class="main-nav" id="main-nav" aria-label="{s['menu']}">
        <ul>
{nav_items}
        <li><a class="nav-cta" href="{link(cta_k)}"{" aria-current=\"page\"" if cta_k == name else ""}>{cta_label}</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
      <div>
        <h4>{s['name']}</h4>
        <p>{s['footer_about']}</p>
        <p><a href="tel:{s['phone'].replace('-', '')}" class="ltr">{s['phone']}</a><br><a href="mailto:{s['email']}">{s['email']}</a></p>
      </div>
{footer_cols}
      </div>
      <div class="footer-bottom">
        <span>© <span data-year>2026</span> {s['name']}. {s['rights']}</span>
        <span>{s['disclaimer']}</span>
      </div>
    </div>
  </footer>
  <script src="{up}assets/js/main.js" defer></script>
</body>
</html>
"""


META = re.compile(r"<!--\s*(title|description):\s*(.*?)\s*-->\s*")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    names = {lang: sorted(p.stem for p in (PAGES / lang).glob("*.html")) for lang in SITE}
    if names["he"] != names["en"]:
        missing = set(names["he"]) ^ set(names["en"])
        raise SystemExit(f"Pages missing a translation: {sorted(missing)}")
    for lang in SITE:
        for path in sorted((PAGES / lang).glob("*.html")):
            text = path.read_text(encoding="utf-8")
            meta = {}
            while (m := META.match(text)):
                meta[m.group(1)] = m.group(2)
                text = text[m.end():]
            dest = OUT / SITE[lang]["prefix"] / path.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(render(lang, path.stem, meta.get("title", ""), meta.get("description", ""), text), encoding="utf-8")
            print("built", dest.relative_to(ROOT))


if __name__ == "__main__":
    main()
