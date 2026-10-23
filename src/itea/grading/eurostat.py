"""
Layer U adoption: enterprise use of ERP, CRM, supply-chain integration and AI,
from Eurostat's survey on ICT usage in enterprises (dissemination API).

    isoc_eb_iip   integration of internal processes (ERP, CRM…) by size class
    isoc_eb_ics   integration with customers/suppliers, supply chain management
    isoc_eb_ai    artificial intelligence by size class

Figures are downloaded at run time (Eurostat revises them) and saved with the
retrieval date. Eurostat data are reusable with attribution (© European Union).
"""

from __future__ import annotations

import datetime
import itertools
import json
import urllib.parse
import urllib.request

import pandas as pd

API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
DATASETS = ("isoc_eb_iip", "isoc_eb_ics", "isoc_eb_ai")


def parse_jsonstat(doc: dict) -> pd.DataFrame:
    """Flatten a JSON-stat 2.0 dataset (as served by Eurostat) into a tidy table."""
    dims = doc["id"]
    sizes = doc["size"]
    labels = []
    for d in dims:
        cat = doc["dimension"][d]["category"]
        index = cat["index"]
        order = sorted(index, key=index.get) if isinstance(index, dict) else list(index)
        labels.append(order)
    values = doc.get("value", {})
    if isinstance(values, list):
        values = {str(i): v for i, v in enumerate(values) if v is not None}
    rows = []
    for pos, combo in enumerate(itertools.product(*labels)):
        if str(pos) in values:
            rows.append((*combo, values[str(pos)]))
    assert len(labels) == len(sizes)
    return pd.DataFrame(rows, columns=[*dims, "value"])


def fetch_dataset(code: str, **filters) -> pd.DataFrame:
    """Download one Eurostat dataset (optionally filtered, e.g. geo='ES') as a tidy table."""
    query = urllib.parse.urlencode({"format": "JSON", "lang": "EN", **filters}, doseq=True)
    with urllib.request.urlopen(f"{API}{code}?{query}") as r:
        doc = json.load(r)
    df = parse_jsonstat(doc)
    df.insert(0, "dataset", code)
    df["retrieved"] = datetime.date.today().isoformat()
    return df


def indicator_labels(code: str) -> dict:
    """Code → label for the indic_is dimension of a dataset (for documentation)."""
    with urllib.request.urlopen(f"{API}{code}?format=JSON&lang=EN&geo=EU27_2020") as r:
        doc = json.load(r)
    return doc["dimension"]["indic_is"]["category"]["label"]


# Layer U by sector: the *n2 datasets break adoption down by NACE Rev. 2.
# The ICT survey does not cover the financial sector (NACE K) in these tables.
SECTOR_INDICATORS = {
    "isoc_eb_iipn2": ("E_ERP1", "E_CRM1", "E_ITBI", "E_BSANY"),
    "isoc_eb_ain2": ("E_AI_TANY",),
    "isoc_eb_icsn2": ("E_SISC",),
}
SECTORS = ("C10-S951_X_K", "C", "D", "E", "F", "G", "H", "I", "J", "L", "M", "N", "ICT")

# Utilisation depth: share of a system's functionality in effective use, given
# adoption. Declared assumption (DECISIONES D10), not an estimate.
DEPTH = {"low": 0.10, "central": 0.27, "high": 0.35}


def adoption_by_sector(years=("2023", "2024", "2025"), fetch=None) -> pd.DataFrame:
    """
    Share of enterprises (10+ employees) using ERP, CRM, BI, any business software,
    supply-chain integration and AI, by country and NACE sector.

    `fetch` defaults to `fetch_dataset`; tests pass a stub.
    """
    fetch = fetch or fetch_dataset
    parts = []
    for code, indicators in SECTOR_INDICATORS.items():
        d = fetch(code, indic_is=list(indicators), unit="PC_ENT", size_emp="GE10",
                  nace_r2=list(SECTORS), time=list(years))
        parts.append(d[["dataset", "geo", "nace_r2", "indic_is", "time", "value", "retrieved"]])
    return pd.concat(parts, ignore_index=True)


def latest(adoption: pd.DataFrame) -> pd.DataFrame:
    """Most recent year available for each country × sector × indicator."""
    a = adoption.assign(time=adoption["time"].astype(int))
    return a.sort_values("time").groupby(["geo", "nace_r2", "indic_is"], as_index=False).last()


def utilisation(adoption: pd.DataFrame, depth: dict = DEPTH) -> pd.DataFrame:
    """U = adoption share × utilisation depth, for each depth scenario (columns U_low, U_central, U_high)."""
    out = adoption.copy()
    for name, k in depth.items():
        out[f"U_{name}"] = out["value"] / 100 * k
    return out
