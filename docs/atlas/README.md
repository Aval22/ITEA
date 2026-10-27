# Atlas of the alienable frontier — web explorer (v1.0)

Static, self-contained explorer of the ITEA atlas: 923 O\*NET 30.2 occupations, task by task.
Compare two occupations or two occupational families (SOC, with their ISCO-08 equivalents).
Interface in English, Spanish, French, Italian, Chinese and Japanese.

| File | Content |
|---|---|
| `index.html` | the explorer (vanilla JavaScript, no external dependencies) |
| `i18n.js` | interface strings, methodology and sources in six languages |
| `atlas_data_v1.0.json` | data behind the explorer, built by `scripts/atlas/export_atlas_data.py` |

To view it locally: `python3 -m http.server 8790 --directory docs/atlas`, then open http://localhost:8790.
All paths are relative, so the three files can be published in any folder of a web server.

Usage statistics: only when served from epistemica.eu (or with `?stats=test`), the page loads
`/stats/contador.js`, Epistémica's own cookie-free counter. It sends anonymous, banded usage counts (views,
comparisons, clicks, sections reached, scroll depth, visible time); the server derives country, city, operating
system and browser family and daily unique visitors (with a daily fingerprint deleted the next day), and keeps
only monthly totals, with no IP address, browser details or exact time. Nothing is sent when the browser signals
Do Not Track or Global Privacy Control, or anywhere else (GitHub Pages, a local server). The privacy note is in
the page footer, in all six languages.

The printable atlas (PDF, one card per occupation) is deposited on Zenodo: https://doi.org/10.5281/zenodo.23673121

## Licence

Unlike the code of this repository (MIT), the contents of this folder — the atlas data, texts and page — are
© 2026 Alberto García-Lluis Valencia, published by Epistémica, under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): they may be shared and adapted for
non-commercial purposes, with attribution. Commercial use requires the author's written permission.
Third-party data keep their own terms (O\*NET and Anthropic Economic Index: CC BY 4.0; BLS: U.S. public domain).

This product includes information from the O\*NET 30.2 Database (https://www.onetcenter.org/database.html) by the
U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license.
O\*NET® is a trademark of USDOL/ETA. Alberto García-Lluis Valencia has modified all or some of this information.
USDOL/ETA has not approved, endorsed, or tested these modifications.
