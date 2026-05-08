# Deployment Report — ITEA Framework Repository

**Date:** 2026-05-07
**Operator:** Cowork session (on behalf of Alberto García-Lluis Valencia)
**Target:** `/Framework ITEA/` workspace
**Released version:** ITEA Framework **v3.0** (release date in MANIFEST: 2026-04-30)

## 1. Decisions taken

| # | Decision | Choice |
|---|----------|--------|
| 1 | Repository structure | v3.0 deployed at the root, prior versions archived under `versions/v2.0/` and `versions/v2.1/`; v3.0 source documents preserved under `versions/v3.0_originals/`. |
| 2 | READMEs (4 languages) | Used the READMEs bundled inside `ITEA-Framework_v3.0_Repo.zip`. The set inside `readmes_update.zip` was discarded — its files were the legacy v1.45 READMEs (O\*NET 29.1, 8 indicators) misnamed as "update". |
| 3 | CITATION.cff | Used the version inside the v3.0 ZIP (complete, with concept DOI, correct repository URL `AVAL22/ITEA-Framework`, v3.0 metadata). The standalone uploaded `CITATION.cff` was an older v1.45-style file pointing at `Aval22/ITEA` and Streamlit URL. |
| 4 | Pre-existing working files (`Diagnostico_Framework_ITEA_2026-04-29.docx`, `ITEA_Development_Roadmap_v2.md`, `paper.md`) | Moved to `docs/legacy/working/` to keep the published surface clean. |
| 5 | Integrity verification | All 14 files declared in `MANIFEST.json` were re-hashed (SHA-256) after deployment and matched the declared digests. |

## 2. Final tree

```
Framework ITEA/
├── CHANGELOG.md
├── CITATION.cff
├── LICENSE
├── MANIFEST.json
├── README.md / README_ES.md / README_PT.md / README_ZH.md
├── code/
│   ├── legacy/                       (kept empty for future v1.45 archival)
│   └── v3/
│       ├── itea_functions_v3.R
│       ├── itea_functions_v3.py
│       └── tests/test_itea_v3.py
├── data/
│   ├── legacy/                       (v1.45 multilingual READMEs — historical)
│   └── processed/ITEA_v3_0_Workbook.xlsx
├── docs/
│   ├── ITEA_v3_0_Consolidated_Methodology.docx
│   ├── MIGRATION.md
│   ├── DEPLOYMENT_REPORT_2026-05-07.md   (this file)
│   └── legacy/working/
│       ├── Diagnostico_Framework_ITEA_2026-04-29.docx
│       ├── ITEA_Development_Roadmap_v2.md
│       └── paper.md
├── paper/
│   ├── paper.md
│   └── paper.bib
└── versions/
    ├── README.md
    ├── v2.0/
    │   ├── ITEA_Methodology_v2.0_EN.docx
    │   ├── ITEA_Metodologia_v2.0_ES.docx
    │   └── Research_Data_Workbook_v2.0.xlsx
    ├── v2.1/
    │   ├── Anexo_ITEA_v2.0_Memo_Actualizacion_v2.1.docx
    │   └── Research_Data_Workbook_v2.1.xlsx
    └── v3.0_originals/
        ├── ITEA_Memo_v3.0_ES.docx
        ├── ITEA_Methodology_v3.0_EN.docx
        ├── ITEA_v3.0_Consolidated_Methodology_source.docx
        └── ITEA_v3.0_Workbook_source.xlsx
```

## 3. SHA-256 verification (against `MANIFEST.json`)

All 14 files listed in the manifest were verified — every digest matched.

```
OK  data/processed/ITEA_v3_0_Workbook.xlsx                    260449  2ded73eeb8c1…
OK  code/v3/itea_functions_v3.R                                 9273  17f28109d8ab…
OK  code/v3/itea_functions_v3.py                                9642  da3d0b2c5fd5…
OK  code/v3/tests/test_itea_v3.py                               6587  8a6ac5f58307…
OK  README.md                                                  15074  e063a3078e5c…
OK  README_ES.md                                                8482  8fc76f6e8f3b…
OK  README_PT.md                                                6340  be6a0a08cf81…
OK  README_ZH.md                                                5757  6c5cfc5d929d…
OK  CHANGELOG.md                                                6564  4dbb716b8bcf…
OK  LICENSE                                                     1759  7e1c5d7ef4ee…
OK  CITATION.cff                                                2814  2d4e3e3b56b2…
OK  docs/MIGRATION.md                                           5284  2d78671a9e45…
OK  paper/paper.md                                              7012  68b51a1e163b…
OK  paper/paper.bib                                             3550  82e21681abc9…
```

## 4. Provenance notes

- The four files in `versions/v3.0_originals/` are byte-identical to the active v3.0 release (verified: SHA-256 matches `docs/ITEA_v3_0_Consolidated_Methodology.docx` and `data/processed/ITEA_v3_0_Workbook.xlsx`). They are kept solely for archival traceability of the original uploads.
- `data/legacy/` already contained the four v1.45 READMEs as part of the v3.0 ZIP — that content was preserved untouched (it documents the legacy dataset, not the current README set).
- `code/legacy/` was created empty by the v3.0 ZIP and was preserved as-is for future archival of v1.45 code.

## 5. Suggested next actions

1. Initialise (or push to) the GitHub repository `AVAL22/ITEA-Framework`. Suggested first commit message: `chore: deploy v3.0 + archive v2.0/v2.1 sources`.
2. Tag `v3.0` after the first push; the legacy tag `v1.45-legacy` referenced in `MANIFEST.json` should be created from the historical commit if you want it discoverable on GitHub.
3. Submit `paper/paper.md` to JOSS (the README badge already declares "submission mid-2026").
4. If you still want to expose the previous v1.45 READMEs separately (e.g., for users coming from old links), they remain in `data/legacy/` — no further action needed.
