#!/usr/bin/env python3
"""
Build the ITEA v4.0 data workbook (data/processed/ITEA_v4_0_Workbook.xlsx)
from the canonical CSV/JSON outputs in v4.0/outputs/. The CSV files remain the
reference; the workbook is a convenience copy for reading and teaching.

Usage:
    python scripts/build_workbook_v4.py [--external data/external] [--out data/processed/ITEA_v4_0_Workbook.xlsx]

--external is optional: if the BLS ISCO–SOC crosswalk is there, ISCO-08
unit-group titles are added to the OAXI-EU sheet.
"""

import argparse
import datetime
import json
import os

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import itea
from itea.oaxi_eu import convergence

OUT = "v4.0/outputs"
GR = os.path.join(OUT, "grading")
HEAD = PatternFill("solid", fgColor="1F3A5F")


def isco_titles(external: str) -> pd.DataFrame | None:
    path = os.path.join(external, "ISCO_SOC_Crosswalk.xls")
    if not os.path.exists(path):
        return None
    x = pd.read_excel(path, header=6, dtype=str)
    x = x.rename(columns={"ISCO-08 Code": "isco", "ISCO-08 Title EN": "isco_title"})
    return x[["isco", "isco_title"]].dropna().assign(isco=lambda d: d["isco"].str.strip()).drop_duplicates("isco")


def hypotheses() -> pd.DataFrame:
    s = json.load(open(os.path.join(GR, "validation_structural.json")))
    d = json.load(open(os.path.join(GR, "validation_discriminant.json")))
    rows = [
        ("H1", "E1 vs Eloundou human exposure (+)", s["H1_E1_vs_eloundou_human_beta"], "Supported"),
        ("H2", "K1 vs non-routine analytical (+)", s["H2_K1_vs_nonroutine_analytical"], "Supported"),
        ("H3", "K1 vs routine cognitive (+, weaker than H2)", s["H3_K1_vs_routine_cognitive"], "Not supported (opposite sign)"),
        ("H4", "|K1 vs Job Zone| < 0.70", s["H4_K1_vs_job_zone"], "Borderline"),
        ("H6", "K1 vs non-routine analytical, net of Job Zone (+)", d["H6_K1_vs_nonroutine_analytical_net_of_job_zone"], "Supported"),
        ("H7", "K1 vs routine cognitive in non-manual occupations (+)", d["H7_K1_vs_routine_cognitive_non_manual"], "Not supported (opposite sign)"),
        ("H8", "K1 vs Eloundou human exposure, net of Job Zone (partial ρ > 0.10)", d["H8_K1_vs_eloundou_net_of_job_zone"], "Supported"),
    ]
    out = pd.DataFrame([{"hypothesis": h, "test": t, "rho": round(r["r"], 3),
                         "ci95_low": round(r["ci95"][0], 3), "ci95_high": round(r["ci95"][1], 3),
                         "n": r["n"], "verdict": v} for h, t, r, v in rows])
    h5 = pd.DataFrame([{"hypothesis": "H5", "test": "Within-GWA share of K1 variance < 0.20 (diagnostic)",
                        "rho": round(s["H5_K1_within_gwa_variance_share"], 3), "n": s["n_tasks"],
                        "verdict": "As expected"}])
    table = pd.concat([out.iloc[:4], h5, out.iloc[4:]], ignore_index=True)
    return pd.concat([table, later_hypotheses()], ignore_index=True)


def later_hypotheses() -> pd.DataFrame:
    """H9B–H20 (layer 2B, layer 3 and the v4.1 composite), when their result files exist."""
    def row(h, test, r, verdict):
        if isinstance(r, dict):
            return {"hypothesis": h, "test": test, "rho": round(r["r"], 3), "ci95_low": round(r["ci95"][0], 3),
                    "ci95_high": round(r["ci95"][1], 3), "n": r["n"], "verdict": verdict}
        return {"hypothesis": h, "test": test, "rho": round(r, 3), "verdict": verdict}

    def ok(v, floor=0.0):
        return "Supported" if v["r"] > floor and v["ci95"][0] > 0 else "Not supported"

    rows = []
    path = os.path.join(GR, "validation_semantic_B.json")
    if os.path.exists(path):
        b = json.load(open(path))
        rows += [row("H9B", "E2 (ESCO, 5 nearest concepts) vs Eloundou (+)", b["H9_E2_vs_eloundou"], ok(b["H9_E2_vs_eloundou"])),
                 row("H10B", "E1+E2 vs Eloundou (ρ > 0.43)", b["H10_E12_vs_eloundou"],
                     "Supported" if b["H10_E12_vs_eloundou"]["r"] > 0.43 else "Not supported"),
                 row("H11B", "Within-GWA share of K2 variance > 0.20", b["H11_K2_within_gwa_variance_share"],
                     "Supported" if b["H11_K2_within_gwa_variance_share"] > 0.20 else "Not supported"),
                 row("H12B", "K2 vs non-routine analytical, net of Job Zone (+)",
                     b["H12_K2_vs_nonroutine_analytical_net_of_job_zone"], ok(b["H12_K2_vs_nonroutine_analytical_net_of_job_zone"])),
                 row("H13B", "K2 vs Eloundou, net of Job Zone (partial ρ > 0.10)",
                     b["H13_K2_vs_eloundou_net_of_job_zone"], ok(b["H13_K2_vs_eloundou_net_of_job_zone"], 0.10))]
    path = os.path.join(GR, "validation_anchors.json")
    if os.path.exists(path):
        c = json.load(open(path))
        rows += [row("H14", "E3 (NLI anchors) vs Eloundou (+)", c["H14_E3_vs_eloundou"], ok(c["H14_E3_vs_eloundou"])),
                 row("H15", "E1+E2+E3 vs Eloundou (ρ > 0.476)", c["H15_E123_vs_eloundou"],
                     "Supported" if c["H15_E123_vs_eloundou"]["r"] > 0.476 else "Not supported"),
                 row("H16", "K3 vs non-routine analytical, net of Job Zone (+)",
                     c["H16_K3_vs_nonroutine_analytical_net_of_job_zone"], ok(c["H16_K3_vs_nonroutine_analytical_net_of_job_zone"])),
                 row("H17", "K3 vs Eloundou, net of Job Zone (partial ρ > 0.10)",
                     c["H17_K3_vs_eloundou_net_of_job_zone"], ok(c["H17_K3_vs_eloundou_net_of_job_zone"], 0.10))]
    path = os.path.join(GR, "oaxi_eu_v41.meta.json")
    if os.path.exists(path):
        m = json.load(open(path))
        rows += [row("H18", "Final E vs Eloundou (ρ > 0.40)", m["H18_E_vs_eloundou"],
                     "Supported" if m["H18_supported"] else "Not supported"),
                 row("H19", "Final K vs non-routine analytical, net of Job Zone (+)",
                     m["H19_K_vs_nonroutine_analytical_net_of_job_zone"], "Supported" if m["H19_supported"] else "Not supported"),
                 row("H20", "Median 5–95 % band of the ISCO rank < 100 places (Monte Carlo)",
                     m["H20_median_rank_band_5_95"], "Supported" if m["H20_supported"] else "Not supported")]
    return pd.DataFrame(rows)


def rebuilt_index(titles) -> tuple[str, pd.DataFrame, dict] | None:
    """OAXI-EU rebuilt from itea.grading (scripts/grading/build_oaxi_eu_v41.py), v41 if present, else the layer-1 preview."""
    for label in ("v41", "layer1"):
        path = os.path.join(GR, f"oaxi_eu_{label}.csv")
        if os.path.exists(path):
            d = pd.read_csv(path, dtype={"isco": str, "isco3": str})
            if titles is not None:
                d = d.merge(titles, on="isco", how="left")
                d = d[["isco", "isco_title"] + [c for c in d.columns if c not in ("isco", "isco_title")]]
            return label, d, json.load(open(os.path.join(GR, f"oaxi_eu_{label}.meta.json")))
    return None


def readme(conv: dict, meta: dict, rebuilt=None) -> pd.DataFrame:
    today = datetime.date.today().isoformat()
    lines = [
        ("ITEA v4.0 — data workbook", ""),
        ("Generated", f"{today} by scripts/build_workbook_v4.py from v4.0/outputs/ (the CSV files are the reference)"),
        ("Package version", itea.__version__),
        ("", ""),
        ("Sheet", "Content / Contenido"),
        ("OAXI_EU", f"European index by ISCO-08 unit group ({meta['n_isco']} groups, κ = {meta['kappa']}): E, K, OAXI_EU (1–100) / Índice europeo por grupo ISCO-08"),
        *([(f"OAXI_EU_{rebuilt[0]}",
             f"OAXI-EU rebuilt from itea.grading ({'v4.1' if rebuilt[0] == 'v41' else 'preview with the structural layer only'}): "
             f"Spearman {rebuilt[2]['agreement_with_v40_axi']['spearman']:.2f} with the AXI-based index / "
             "Reconstruido con la graduación nueva")] if rebuilt else []),
        ("Validation_JRC", f"OAXI-EU vs JRC145832 at ISCO-3: n = {conv['n_isco3']}, Pearson {conv['pearson']:.3f}, Spearman {conv['spearman']:.3f} / Convergencia con el JRC"),
        ("Crosswalk", "Official BLS chain SOC 2018 → SOC 2010 → ISCO-08, equal weights / Crosswalk oficial"),
        ("Occupation_shares", "Share of legacy AXI grades per O*NET occupation / Cuotas de grados AXI por ocupación"),
        ("Grading_tasks", "v4.1 task grades for the 18,796 O*NET 30.2 tasks: final K and E and their components / Notas por tarea"),
        ("Grading_GWA", "K and E of the 41 generalised work activities, from O*NET linkage tables / K y E por actividad general"),
        ("Hypotheses", "Pre-registered validation hypotheses H1–H20 and results, failures included / Hipótesis registradas y resultados"),
        ("Layer_U", "Enterprise adoption by country × NACE sector and utilisation U = adoption × depth / Adopción y utilización"),
        ("Layer_T_vendors", "Vendor presence across O*NET occupations / Presencia de fabricantes"),
        ("", ""),
        ("Notes / Notas", ""),
        ("1", "OAXI-EU v4.0 is built on the legacy AXI task grades, which v4.1 replaces (docs/grading/). / OAXI-EU v4.0 usa los grados AXI heredados, que la v4.1 sustituye."),
        ("2", "Layer U: Eurostat tables do not cover the financial sector (NACE K); depth 0.10 / 0.27 / 0.35 is a declared assumption. / La capa U no cubre el sector financiero."),
        ("3", "Rebuild everything with: itea fetch; itea build-eu; python scripts/grading/*.py; python scripts/build_workbook_v4.py"),
        ("", ""),
        ("Licences / Licencias", "Code MIT. AXI grades CC BY 4.0. O*NET data CC BY 4.0 (USDOL/ETA; modified). JRC145832 CC BY 4.0. BLS crosswalks public domain. Eurostat © European Union, reuse with attribution."),
        ("Input SHA-256", "; ".join(f"{k}: {v[:12]}…" for k, v in meta["inputs_sha256"].items())),
    ]
    return pd.DataFrame(lines, columns=["Item", "Description"])


def style(ws, widths=None):
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = HEAD
        c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"
    for i, col in enumerate(ws.columns, 1):
        n = max(len(str(c.value)) if c.value is not None else 0 for c in list(col)[:200])
        ws.column_dimensions[get_column_letter(i)].width = min(max(10, n + 2), (widths or {}).get(i, 60))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", default="data/external")
    ap.add_argument("--out", default="data/processed/ITEA_v4_0_Workbook.xlsx")
    a = ap.parse_args()

    meta = json.load(open(os.path.join(OUT, "oaxi_eu.meta.json")))
    idx = pd.read_csv(os.path.join(OUT, "oaxi_eu.csv"), dtype={"isco": str, "isco3": str})
    jrc = itea.jrc_benchmark()
    conv = convergence(idx, jrc)
    titles = isco_titles(a.external)
    if titles is not None:
        idx = idx.merge(titles, on="isco", how="left")
        idx = idx[["isco", "isco_title"] + [c for c in idx.columns if c not in ("isco", "isco_title")]]
    rebuilt = rebuilt_index(titles)
    v3 = (idx.groupby("isco3")["OAXI_EU"].mean().rename("OAXI_EU_mean_isco3").reset_index()
          .merge(jrc.rename(columns={"score": "JRC145832_ai_exposure_2024"}), on="isco3", how="inner"))
    v3 = v3[["isco3", "occupation", "OAXI_EU_mean_isco3", "JRC145832_ai_exposure_2024"]].round(4)

    sheets = {
        "README": readme(conv, meta, rebuilt),
        "OAXI_EU": idx.sort_values("OAXI_EU", ascending=False),
        **({f"OAXI_EU_{rebuilt[0]}": rebuilt[1]} if rebuilt else {}),
        "Validation_JRC": v3,
        "Crosswalk": pd.read_csv(os.path.join(OUT, "crosswalk_soc2018_isco08.csv"), dtype={"isco": str}).round(4),
        "Occupation_shares": pd.read_csv(os.path.join(OUT, "occupation_shares.csv")),
        "Grading_tasks": pd.read_csv(os.path.join(GR, "task_grades_v41.csv") if os.path.exists(os.path.join(GR, "task_grades_v41.csv"))
                                     else os.path.join(GR, "task_prior_structural.csv"), dtype={"TaskID": str}),
        "Grading_GWA": pd.read_csv(os.path.join(GR, "gwa_scores.csv")),
        "Hypotheses": hypotheses(),
        "Layer_U": pd.read_csv(os.path.join(GR, "utilisation_by_sector.csv"), dtype={"nace_r2": str}),
        "Layer_T_vendors": pd.read_csv(os.path.join(GR, "vendor_presence.csv")),
    }
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with pd.ExcelWriter(a.out, engine="openpyxl") as xw:
        for name, df in sheets.items():
            df.to_excel(xw, sheet_name=name, index=False)
            style(xw.sheets[name], {2: 110} if name == "README" else None)
    print(f"{a.out}: {', '.join(f'{k} ({len(v)})' for k, v in sheets.items())}")
    print(f"JRC convergence: {conv}")


if __name__ == "__main__":
    main()
