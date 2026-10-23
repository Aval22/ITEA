"""
Layer T inventory: the technology each occupation uses, from O*NET.

O*NET lists, per occupation, the software ("Technology Skills") and the
tools and equipment ("Tools Used") its workers use, coded to UNSPSC commodity
classes and flagged as "Hot Technology" or "In Demand". This module builds
the inventory that the vendor-capability corpus (layer T) is collected for;
it does not grade tasks by itself.
"""

from __future__ import annotations

import os

import pandas as pd

# Vendors whose products and certification programmes the pilot documents first.
VENDORS = {
    "Microsoft": r"\bMicrosoft\b", "SAP": r"\bSAP\b", "Oracle": r"\bOracle\b",
    "IBM": r"\bIBM\b", "Cisco": r"\bCisco\b", "Salesforce": r"\bSalesforce\b",
    "Google": r"\bGoogle\b", "Amazon/AWS": r"\bAmazon\b|\bAWS\b", "Adobe": r"\bAdobe\b",
    "Autodesk": r"\bAutodesk\b|\bAutoCAD\b",
}

# Pilot: finance and consulting occupations (SOC 2018 prefixes).
PILOT_PREFIXES = ("13-2", "43-3", "11-3031", "13-1111")


def inventory(onet_dir: str) -> pd.DataFrame:
    """
    One row per occupation × product: SOC, kind (software/tool), product,
    UNSPSC code and title, hot/in-demand flags and detected vendor.
    """
    sw = pd.read_csv(os.path.join(onet_dir, "Technology Skills.txt"), sep="\t", dtype=str)
    sw = sw.assign(kind="software")
    tl = pd.read_csv(os.path.join(onet_dir, "Tools Used.txt"), sep="\t", dtype=str)
    tl = tl.assign(kind="tool", **{"Hot Technology": "N", "In Demand": "N"})
    inv = pd.concat([sw, tl], ignore_index=True).rename(columns={
        "O*NET-SOC Code": "SOC", "Example": "product", "Commodity Code": "unspsc",
        "Commodity Title": "unspsc_title", "Hot Technology": "hot", "In Demand": "in_demand"})
    inv["hot"] = inv["hot"].eq("Y")
    inv["in_demand"] = inv["in_demand"].eq("Y")
    inv["vendor"] = None
    for vendor, pattern in VENDORS.items():
        hit = inv["vendor"].isna() & inv["product"].str.contains(pattern, regex=True, na=False)
        inv.loc[hit, "vendor"] = vendor
    return inv[["SOC", "kind", "product", "unspsc", "unspsc_title", "hot", "in_demand", "vendor"]]


def vendor_presence(inv: pd.DataFrame) -> pd.DataFrame:
    """Occupations, products and mentions per detected vendor."""
    v = inv.dropna(subset=["vendor"])
    return (v.groupby("vendor").agg(occupations=("SOC", "nunique"), products=("product", "nunique"),
                                    mentions=("product", "size"))
             .sort_values("occupations", ascending=False).reset_index())


def pilot_targets(inv: pd.DataFrame, prefixes=PILOT_PREFIXES) -> pd.DataFrame:
    """
    Software products whose capabilities the pilot must document: products used
    in pilot occupations, ranked by how many pilot occupations use them.
    """
    p = inv[(inv["kind"] == "software") & inv["SOC"].str.startswith(prefixes)]
    return (p.groupby(["product", "unspsc_title", "vendor"], dropna=False)
             .agg(pilot_occupations=("SOC", "nunique"), hot=("hot", "max"))
             .sort_values(["pilot_occupations", "hot"], ascending=False).reset_index())
