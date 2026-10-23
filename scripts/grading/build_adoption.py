#!/usr/bin/env python3
"""
Layer U table (issue #7): enterprise adoption of business software and AI by
country and NACE sector (Eurostat ICT survey), latest year per cell, with
utilisation U = adoption × depth under the low/central/high depth assumptions.

Usage:
    python scripts/grading/build_adoption.py --out v4.0/outputs/grading
"""

import argparse
import os

from itea.grading.eurostat import adoption_by_sector, latest, utilisation


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="v4.0/outputs/grading")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    raw = adoption_by_sector()
    raw.to_csv(os.path.join(a.out, "eurostat_adoption_by_sector_raw.csv"), index=False)
    u = utilisation(latest(raw))
    u.round(4).to_csv(os.path.join(a.out, "utilisation_by_sector.csv"), index=False)
    print(f"{len(raw)} raw cells; {len(u)} country × sector × indicator cells "
          f"({u['geo'].nunique()} geos, {u['nace_r2'].nunique()} sectors)")


if __name__ == "__main__":
    main()
