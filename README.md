# ICBAP website

Website of the Israel Certification Board of Addiction Professionals (ICBAP), Israel's IC&RC member board.

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
| `certifications` | The CASAP credential (IC&RC ADC reciprocal): reciprocity, IC&RC minimum requirements, experience by degree, the four ADC domains | IC&RC |
| `apply` | Process, documents, fees, exam, accommodations, retakes, appeals, portal | IC&RC, ISAM, CCAPP |
| `renew` | 2-year CE requirements, audit, inactive/retired, reinstatement, CE provider approval | NAADAC, CCAPP, IITAP |
| `verify` | Public registry search (Hebrew/English) | NAADAC, FDAP |
| `ethics` | Code of Ethics principles, complaint form, disciplinary process, sanctions | NAADAC, IC&RC |
| `faq`, `contact`, `accessibility` | Includes the accessibility statement required under Israeli law (IS 5568) | — |

## Before launch

All placeholders are highlighted in yellow on the pages (search the source for `placeholder-note`). They include:

- Organisation name, registration number, address, phone and email, and board member profiles
- **CASAP requirements** follow IC&RC's published ADC minimums. Add any ICBAP-specific requirements, the full credential name, fees, renewal rules and exam logistics for Israel.
- **Contact details** are taken from the IC&RC Member Board Directory listing for ICBAP.
- `static/assets/js/registry-data.js` contains **fictional sample records**. Replace it with real data or an API call.
- The complaint and contact forms are not connected (`data-demo`): they tell the visitor nothing was sent and to email instead. Point their `action` at a form backend (e.g. Formspree) and remove `data-demo`.
- PDFs to link: Candidate Handbook, full Code of Ethics.
- An Arabic version is a natural next step, since exams are offered in Arabic. It would need an `ar` entry in `SITE`, a `pages/ar/` folder, and a three-way language switcher (`build.py` currently assumes two languages).
