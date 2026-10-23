"""
SOC 2018 -> ISCO-08 crosswalk built from the two official BLS tables.

O*NET-SOC 2019 codes share their first six digits with SOC 2018. BLS
publishes a SOC 2010 <-> ISCO-08 crosswalk and a SOC 2010 <-> SOC 2018
crosswalk; chaining them gives a many-to-many SOC 2018 -> ISCO-08 map.
When one SOC code maps to several ISCO groups its weight is split equally,
so every SOC code contributes a total weight of one.

Sources (U.S. Bureau of Labor Statistics, public domain):
    https://www.bls.gov/soc/ISCO_SOC_Crosswalk.xls
    https://www.bls.gov/soc/2018/soc_2010_to_2018_crosswalk.xlsx
"""

from __future__ import annotations

import pandas as pd


def _header_row(path: str, label: str, sheet_name=0) -> int:
    """Row index of the header line that contains `label` (BLS files carry a preamble)."""
    raw = pd.read_excel(path, sheet_name=sheet_name, header=None, dtype=str)
    hit = raw.apply(lambda r: r.astype(str).str.strip().eq(label).any(), axis=1)
    if not hit.any():
        raise ValueError(f"'{label}' header not found in {path}")
    return int(hit.idxmax())


def _strip(df: pd.DataFrame) -> pd.DataFrame:
    # BLS cells carry trailing spaces (e.g. "13-1011 "), which silently break joins.
    return df.apply(lambda c: c.astype(str).str.strip())


def read_soc2010_soc2018(path: str) -> pd.DataFrame:
    """BLS SOC 2010 -> SOC 2018 table as columns soc2010, soc2018."""
    df = pd.read_excel(path, header=_header_row(path, "2010 SOC Code"), dtype=str)
    df = df.rename(columns={"2010 SOC Code": "soc2010", "2018 SOC Code": "soc2018"})
    return _strip(df[["soc2010", "soc2018"]].dropna()).drop_duplicates()


def read_soc2010_isco08(path: str) -> pd.DataFrame:
    """BLS SOC 2010 -> ISCO-08 table as columns soc2010, isco (4-digit unit groups only)."""
    sheet = "2010 SOC to ISCO-08"
    df = pd.read_excel(path, sheet_name=sheet, header=_header_row(path, "2010 SOC Code", sheet), dtype=str)
    df = df.rename(columns={"2010 SOC Code": "soc2010", "ISCO-08 Code": "isco"})
    df = _strip(df[["soc2010", "isco"]].dropna())
    return df[df["isco"].str.fullmatch(r"\d{4}")].drop_duplicates()


def build_crosswalk(isco_soc_path: str, soc_2010_2018_path: str,
                    isco_weights: pd.Series | None = None) -> pd.DataFrame:
    """
    Chain the two BLS tables into a weighted SOC 2018 -> ISCO-08 crosswalk.

    Returns columns soc2018, isco, w, with w summing to 1 within each soc2018.

    By default a SOC code's weight is split equally among its ISCO groups.
    `isco_weights` (a Series indexed by 4-digit ISCO code, e.g. a country's
    employment by unit group) splits it in proportion instead; ISCO groups
    missing from the Series get weight zero, and a SOC code whose groups all
    get zero falls back to the equal split.
    """
    cw = read_soc2010_soc2018(soc_2010_2018_path).merge(
        read_soc2010_isco08(isco_soc_path), on="soc2010", how="inner")
    cw = cw[["soc2018", "isco"]].drop_duplicates().sort_values(["soc2018", "isco"])
    return reweight(cw, isco_weights)


def reweight(cw: pd.DataFrame, isco_weights: pd.Series | None = None) -> pd.DataFrame:
    """Set the split weights w of a soc2018-isco table (equal, or proportional to `isco_weights`)."""
    cw = cw[["soc2018", "isco"]].copy()
    equal = 1.0 / cw.groupby("soc2018")["isco"].transform("size")
    if isco_weights is None:
        cw["w"] = equal
    else:
        raw = cw["isco"].map(isco_weights.rename(index=str)).fillna(0.0).astype(float)
        total = raw.groupby(cw["soc2018"]).transform("sum")
        cw["w"] = (raw / total).where(total > 0, equal)
    return cw.reset_index(drop=True)
