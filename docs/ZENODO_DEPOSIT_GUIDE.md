# Zenodo Deposit Guide — ITEA Framework v3.0

This document is the operational playbook to obtain (or update) a citable
DOI for this repository on [Zenodo](https://zenodo.org/), the CERN-operated
open repository that JOSS treats as the canonical archival channel.

It covers two scenarios:

- **A. GitHub-Zenodo automated integration** (recommended — one-click, reproducible, ties each git tag to a fresh DOI automatically).
- **B. Manual upload via the Zenodo web UI or REST API** (fallback — useful when GitHub is not yet public or when Zenodo's GitHub link cannot be used).

> **Sole prerequisite for JOSS:** by the time JOSS accepts the paper, the
> repository must have a Zenodo deposit whose archived snapshot matches the
> exact commit reviewed. JOSS does not mint the DOI — *you* do, and you give
> the DOI to the editor.

---

## 0. Two DOIs to keep clear in your head

Zenodo issues two related DOIs for any deposit that has more than one version:

| DOI type | What it resolves to | Where to use it |
|----------|---------------------|------------------|
| **Concept DOI** | A landing page that *always points at the latest version*. Stable across versions. | `CITATION.cff`, `README*.md`, paper bibliography "cite the software" entry, generic "use this DOI" badges. |
| **Version DOI** | The specific version snapshot (e.g. v3.0, v3.1, …). New DOI minted on every release. | The JOSS submission form, `MANIFEST.json` for v3.0, any reference to a *specific* reproducible state. |

The current `CITATION.cff` declares `10.5281/zenodo.19578916` as the concept
DOI. **Verify** by visiting <https://doi.org/10.5281/zenodo.19578916>. If it
404s, treat it as a placeholder and follow Scenario A or B below to mint the
real DOIs.

---

## A. GitHub → Zenodo integration (recommended)

This is the path JOSS reviewers expect. Total time: ~10 minutes.

### A.1 — One-time account setup

1. Sign in to <https://zenodo.org/> using your **GitHub** account (the same account that owns `AVAL22/ITEA-Framework`). This creates the Zenodo↔GitHub link automatically.
2. Confirm your ORCID at <https://zenodo.org/account/settings/profile/> — set it to `0009-0003-1438-1633`. Doing this *now* means the ORCID will be embedded in every future deposit metadata block.

### A.2 — Enable the repository for archiving

1. Visit <https://zenodo.org/account/settings/github/>.
2. Find `AVAL22/ITEA-Framework` in the list. (If absent, click "Sync" and reload.)
3. Flip the toggle to **ON**. From this moment, every new GitHub *release* (not just a tag — a *release*) will be mirrored to Zenodo and assigned a DOI.

### A.3 — Add the Zenodo metadata file

Drop the supplied `docs/zenodo_metadata.json` (sibling of this guide) at
**`.zenodo.json`** at the root of the repository. The Zenodo bot reads that
file to populate the deposit metadata automatically. Schema reference:
<https://developers.zenodo.org/#representation>.

```bash
cp docs/zenodo_metadata.json .zenodo.json
git add .zenodo.json
git commit -m "ci: add Zenodo deposit metadata"
git push
```

### A.4 — Cut the v3.0 GitHub release

1. Tag the commit you want archived: `git tag -a v3.0 -m "ITEA Framework v3.0"` then `git push origin v3.0`.
2. Go to **Releases → Draft a new release** in GitHub.
3. Choose the tag `v3.0`, title "ITEA Framework v3.0", and paste the v3.0 entry from `CHANGELOG.md` as the description.
4. Click **Publish release**.
5. Within ~60 seconds Zenodo creates the deposit. Refresh <https://zenodo.org/account/settings/github/> until you see a green badge with the new DOI on the row for `AVAL22/ITEA-Framework`. Click the badge — it links to the version DOI; the concept DOI is one click away on the deposit's right-hand sidebar ("Cite all versions").

### A.5 — Backfill the DOIs into the repo

Once you have the two DOIs (let `CONCEPT_DOI` and `V3_DOI` stand for the values you got):

1. **`CITATION.cff`** — replace the placeholder concept DOI with `CONCEPT_DOI`.
2. **`README.md` / `README_ES.md` / `README_PT.md` / `README_ZH.md`** — replace the badge URL.
3. **`MANIFEST.json`** — replace `doi_concept` with `CONCEPT_DOI` and add `doi_version: "<V3_DOI>"`.
4. **`paper/paper.md`** — if you cite the software in the bibliography, point that entry at `CONCEPT_DOI`.
5. **`code/v3/itea_functions_v3.py`** and **`.R`** — update the `DOI:` header comment.
6. Commit:

   ```bash
   git commit -am "docs: backfill Zenodo DOIs (concept=$CONCEPT_DOI, v3.0=$V3_DOI)"
   git push
   ```

   This commit does **not** require a new release — Zenodo already archived the previous commit. Future v3.1, v4.0 etc. will inherit the same concept DOI automatically.

---

## B. Manual upload (fallback path)

Use this only if (i) the GitHub repository is not yet public, (ii) you want a single deposit independent of GitHub, or (iii) Zenodo's GitHub integration is failing.

### B.1 — Build the upload bundle

```bash
cd "/path/to/Framework ITEA"
git archive --format=zip --prefix=ITEA-Framework-v3.0/ HEAD -o ../ITEA-Framework-v3.0.zip
```

If the project is not under git yet:

```bash
cd ..
zip -r ITEA-Framework-v3.0.zip "Framework ITEA" -x "*.DS_Store" -x "*/.*"
```

The resulting ZIP must include `MANIFEST.json` so anyone can re-verify
file integrity against the SHA-256 digests after download.

### B.2 — Create the deposit (web UI)

1. Visit <https://zenodo.org/uploads/new>.
2. Drag `ITEA-Framework-v3.0.zip` into the upload area.
3. Fill the metadata block using the values from `docs/zenodo_metadata.json` (see §C below).
4. Click **Save** (creates the deposit) then **Publish** (mints the DOI). Publish is irreversible — review carefully first.

### B.3 — Create the deposit (REST API, optional)

```bash
ZENODO_TOKEN="<personal access token from https://zenodo.org/account/settings/applications/tokens/new/>"

# 1. Create empty deposit
DEPOSIT=$(curl -s -H "Authorization: Bearer $ZENODO_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "https://zenodo.org/api/deposit/depositions" -d '{}')

DEPOSIT_ID=$(echo "$DEPOSIT" | jq -r '.id')
BUCKET=$(echo "$DEPOSIT" | jq -r '.links.bucket')

# 2. Upload the ZIP into the deposit's bucket
curl -H "Authorization: Bearer $ZENODO_TOKEN" \
  -X PUT "$BUCKET/ITEA-Framework-v3.0.zip" \
  --upload-file ITEA-Framework-v3.0.zip

# 3. Push metadata
curl -H "Authorization: Bearer $ZENODO_TOKEN" \
  -H "Content-Type: application/json" \
  -X PUT "https://zenodo.org/api/deposit/depositions/$DEPOSIT_ID" \
  -d @docs/zenodo_metadata.json

# 4. Publish (mints the DOI — irreversible)
curl -H "Authorization: Bearer $ZENODO_TOKEN" \
  -X POST "https://zenodo.org/api/deposit/depositions/$DEPOSIT_ID/actions/publish"
```

The final `publish` call returns a JSON document containing both
`conceptdoi` and `doi` fields. Save those — they are the values you need to
backfill per §A.5.

---

## C. Required metadata (single source of truth)

The fields below are what Zenodo *requires* (★) or *strongly recommends* (☆)
for a software deposit. They live in `docs/zenodo_metadata.json`.

| Field | Value | Required? |
|-------|-------|-----------|
| `title` | ITEA Framework: A Multidimensional System for Measuring Occupational Exposure to Algorithmic Expropriation under the Agentic AI Regime | ★ |
| `version` | 3.0 | ★ |
| `publication_date` | 2026-04-30 | ★ |
| `upload_type` | software | ★ |
| `description` | (HTML allowed) See `zenodo_metadata.json` — abstract from `CITATION.cff` plus a "what changed" paragraph and the AIOE validation correlation. | ★ |
| `creators[].name` | García-Lluis Valencia, Alberto | ★ |
| `creators[].orcid` | 0009-0003-1438-1633 | ☆ |
| `creators[].affiliation` | Universidad Rey Juan Carlos | ☆ |
| `license` | MIT | ★ |
| `access_right` | open | ★ |
| `keywords` | labor economics, automation, Agentic AI, occupational exposure, algorithmic expropriation, psychometric validation, O\*NET, AIOE | ☆ |
| `related_identifiers` | Trilogy papers (8A, 8B, 8C) by DOI; the GitHub repo URL with relation `isSupplementTo`; the JOSS paper once it has a DOI | ☆ |
| `communities` | (optional) `joss` once accepted by JOSS — Zenodo will move the deposit into the JOSS community | ☆ |
| `language` | eng | ☆ |
| `notes` | "Concept DOI: <fill after first publish>; Version DOI: <fill after first publish>." | ☆ |

The supplied `docs/zenodo_metadata.json` already contains all the values
above formatted exactly as Zenodo's REST API expects.

---

## D. After the DOI is minted — quick verification

```bash
# Concept DOI must resolve to the latest version (v3.0 right now)
curl -sIL "https://doi.org/$CONCEPT_DOI" | grep -E "^location:"

# Version DOI must resolve to a Zenodo page whose listed version reads "3.0"
curl -sIL "https://doi.org/$V3_DOI" | grep -E "^location:"
```

Then re-hash the ZIP that Zenodo serves and confirm the digests match
`MANIFEST.json`:

```bash
curl -L -o /tmp/itea_v3.zip "https://zenodo.org/records/<RECORD_ID>/files/ITEA-Framework-v3.0.zip"
unzip -d /tmp/itea_v3 /tmp/itea_v3.zip
cd /tmp/itea_v3/ITEA-Framework-v3.0
python3 - <<'PY'
import json, hashlib, os
m = json.load(open("MANIFEST.json"))
for f in m["files"]:
    h = hashlib.sha256(open(f["path"], "rb").read()).hexdigest()
    print(("OK " if h == f["sha256"] else "DIFF "), f["path"])
PY
```

---

## E. Submitting to JOSS afterwards

1. Update `paper/paper.md` and `CITATION.cff` with the **concept DOI** and the **v3.0 version DOI**.
2. Open the JOSS submission form: <https://joss.theoj.org/papers/new>.
3. Provide:
   - **Repository URL**: `https://github.com/AVAL22/ITEA-Framework`
   - **Version**: `v3.0`
   - **Software DOI (concept)**: `<CONCEPT_DOI>`
   - **Software archive DOI (version)**: `<V3_DOI>`
4. The bot will build `paper.pdf` from `paper/paper.md`, validate the YAML, and run a citation check. Fix any flag, then a human editor is assigned.

---

## F. Versioning afterwards (e.g. v3.1)

When you cut a future release (v3.1):

1. `git tag -a v3.1 -m "ITEA Framework v3.1"` → `git push origin v3.1`.
2. Draft a new GitHub release as in §A.4 — Zenodo archives it automatically and mints a *new version DOI* under the same *concept DOI*.
3. Update the badges and citation files to reflect v3.1; the concept DOI does **not** change.

---

*Companion files:*

- `docs/zenodo_metadata.json` — machine-readable metadata for Zenodo's API and `.zenodo.json`.
- `docs/JOSS_SUBMISSION_CHECKLIST.md` — broader JOSS readiness audit.
- `docs/DEPLOYMENT_REPORT_2026-05-07.md` — operational record of the v3.0 deployment with SHA-256 verification.
