"""
Download the public inputs of the EU pipeline and verify them by SHA-256.

The AXI task grades ship inside the package (itea/data/). The O*NET text
database and the BLS crosswalks are third-party files and are fetched from
their publishers instead of being redistributed.
"""

from __future__ import annotations

import hashlib
import os
import urllib.request
import zipfile

SOURCES = {
    "onet": {
        "url": "https://www.onetcenter.org/dl_files/database/db_30_2_text.zip",
        "file": "db_30_2_text.zip",
        "sha256": "b5479271931796b838f7173dc0f673a9ec961b7833ac87168fd11e92e7453741",
    },
    "isco_soc": {
        "url": "https://www.bls.gov/soc/ISCO_SOC_Crosswalk.xls",
        "file": "ISCO_SOC_Crosswalk.xls",
        "sha256": "0936c78c4ab2cb0b61d7cfe3dcf0f94d943a4e30b11dade1f11676307e2c0aae",
    },
    "soc_2010_2018": {
        "url": "https://www.bls.gov/soc/2018/soc_2010_to_2018_crosswalk.xlsx",
        "file": "soc_2010_to_2018_crosswalk.xlsx",
        "sha256": "f3a847561562d3e5a30eb848f2902a5f7b02e9c48b3d7f2cc8879899fbc242a7",
    },
}

# External references used only to validate itea.grading (never to build it).
VALIDATION_SOURCES = {
    "eloundou": {
        # Eloundou et al. (2024), human and GPT-4 exposure labels per O*NET task; MIT licence.
        "url": "https://raw.githubusercontent.com/openai/GPTs-are-GPTs/"
               "0471612fef3cc22b74fb884d27bff9dbd3770582/data/full_labelset.tsv",
        "file": "eloundou_full_labelset.tsv",
        "sha256": "094378905e1f3349e50a9a83dc69643a2ef227954d611c8316a46da08cb3d8de",
    },
}

# bls.gov rejects requests without a browser-like user agent
_HEADERS = {"User-Agent": "Mozilla/5.0 (ITEA Framework; https://github.com/Aval22/ITEA)"}


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(dest: str = "data/external", verify: bool = True) -> dict:
    """
    Download every source into `dest` (skipping files already present) and
    unpack the O*NET archive. Returns the local paths keyed as in SOURCES,
    plus "onet_dir" for the unpacked database.
    """
    os.makedirs(dest, exist_ok=True)
    paths = {}
    for key, src in {**SOURCES, **VALIDATION_SOURCES}.items():
        path = os.path.join(dest, src["file"])
        if not os.path.exists(path):
            req = urllib.request.Request(src["url"], headers=_HEADERS)
            with urllib.request.urlopen(req) as r, open(path, "wb") as f:
                f.write(r.read())
        if verify and sha256(path) != src["sha256"]:
            raise ValueError(f"{src['file']}: SHA-256 mismatch; the publisher may have "
                             "replaced the file. Re-run with verify=False to accept it.")
        paths[key] = path
    with zipfile.ZipFile(paths["onet"]) as z:
        z.extractall(dest)
    paths["onet_dir"] = os.path.join(dest, "db_30_2_text")
    return paths
