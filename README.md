# Israeli Board for Addiction Certification — website

A bilingual (Hebrew RTL / English) static site. Hebrew is served from the site root and English from `/en/`.

## Structure

```
build.py            # wraps page bodies in the shared header/nav/footer → docs/
pages/he/*.html     # Hebrew page bodies
pages/en/*.html     # English page bodies (same filenames as Hebrew)
static/assets/      # CSS, JS, images (copied as-is)
docs/             # generated site — deploy this folder
```

Build with `python3 build.py` (Python 3.8+, no dependencies). The build fails if a page exists in one language but not the other.

Site-wide text (organisation name, navigation, footer, phone, email) is in the `SITE` dictionary at the top of `build.py`.

## Publishing

GitHub Pages serves the `docs/` folder from the `main` branch. Run `python3 build.py` and commit `docs/` after every change. The draft has a `noindex` robots tag (in `build.py`) so search engines skip it; remove it at launch.

## Pages

| Page | Contents | Reference models |
|---|---|---|
| `index` | Hero with quick verify, quick-access tiles, credential ladder, stats, steps, news, complaint CTA | IC&RC, NAADAC, ABPM |
| `about` | Mission, values, scope, governance, committees, board, international alignment | IC&RC, FDAP |
| `certifications` | Comparison table, CAC I / CAC II / MAC / CCS, trainee status, specialty endorsements, physician pathway, 12 core functions | IC&RC, NAADAC, IGCCB, IITAP, ISAM |
| `apply` | Process, documents, fees, exam, accommodations, retakes, appeals, portal | IC&RC, ISAM, CCAPP |
| `renew` | 2-year CE requirements, audit, inactive/retired, reinstatement, CE provider approval | NAADAC, CCAPP, IITAP |
| `verify` | Public registry search (Hebrew/English) | NAADAC, FDAP |
| `ethics` | Code of Ethics principles, complaint form, disciplinary process, sanctions | NAADAC, IC&RC |
| `faq`, `contact`, `accessibility` | Includes the accessibility statement required under Israeli law (IS 5568) | — |

## Before launch

All placeholders are highlighted in yellow on the pages (search the source for `placeholder-note`). They include:

- Organisation name, registration number, address, phone and email, and board member profiles
- **Credential hour requirements and fees.** These are drafts modelled on IC&RC, NAADAC and IGCCB norms. The board must approve them.
- `static/assets/js/registry-data.js` contains **fictional sample records**. Replace it with real data or an API call.
- The complaint and contact forms are demo-only (`data-demo`). Point their `action` at a form backend (e.g. Formspree, or your CRM) and remove `data-demo`.
- PDFs to link: Candidate Handbook, full Code of Ethics.
- Don't claim affiliation with IC&RC, ISAM or other bodies until there are formal agreements.
- An Arabic version is a natural next step, since exams are offered in Arabic. It would need an `ar` entry in `SITE`, a `pages/ar/` folder, and a three-way language switcher (`build.py` currently assumes two languages).
