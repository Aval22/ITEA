#!/usr/bin/env python3
"""
Stratified sample of O*NET 30.2 tasks for the human validation of layer F (hypothesis H25).

Implements section 6.2 of docs/grading/LIBRO_CRITERIOS_capa_F_v0.1_ES.md:
    - 300 tasks, stratified by the primary family of the structural rule (F1–F7), with
      equal allocation (families with fewer tasks contribute all of them; the remainder
      is spread over the others), and within family by SOC major group (proportional);
    - the coding form shows only the task statement and the occupation title, so coders
      stay blind to the GWA, the rule, K, E and any usage data;
    - two coders code independently; the key goes to a separate file outside the repo.

Usage:
    python scripts/grading/make_family_sample.py \
        --families v4.0/outputs/grading/task_families_v42.csv --onet <db_30_2_text dir> \
        --form docs/grading/codificacion_humana/ITEA_capaF_familias_300.xlsx \
        --key ITEA-EU_Datos/28_capaF_privado/muestra_capaF_300_clave.csv
"""
from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd

from itea.grading.families import FAM, FAMILIES

SEED = 20261026
N_SAMPLE = 300
CODES = FAM + ["N"]   # N = no AI family would perform it / not automatable today
HELP = {**{f: f"{f}. {FAMILIES[f][0]}" for f in FAM},
        "N": "N. Ninguna: hoy ninguna familia de IA ejecutaría la parte automatizable"}
DESCR_ES = {
    "F1": "Análisis de texto: buscar, extraer, clasificar o comprobar información escrita",
    "F2": "Generación de lenguaje o código: redactar, resumir, explicar, programar, conversar",
    "F3": "Voz: transcribir, entender o generar habla",
    "F4": "Visión: reconocer o procesar imágenes, planos o vídeo",
    "F5": "Aprendizaje automático: analizar datos, estimar, predecir, detectar patrones",
    "F6": "Automatización de flujos y decisión: reglas, RPA, programación de recursos, optimización",
    "F7": "Robótica: mover objetos o máquinas, conducir, manipular físicamente",
    "N": "Ninguna de las anteriores ejecutaría hoy la parte automatizable",
}


def allocate(counts: pd.Series, n: int) -> pd.Series:
    """Equal allocation capped by availability; leftover spread over the larger strata."""
    alloc = pd.Series(0, index=counts.index)
    remaining, open_ = n, list(counts.index)
    while remaining > 0 and open_:
        share = max(remaining // len(open_), 1)
        for s in list(open_):
            take = min(share, counts[s] - alloc[s], remaining)
            alloc[s] += take
            remaining -= take
            if alloc[s] >= counts[s]:
                open_.remove(s)
            if remaining == 0:
                break
    return alloc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--families", required=True)
    ap.add_argument("--onet", required=True)
    ap.add_argument("--form", required=True)
    ap.add_argument("--key", required=True)
    a = ap.parse_args()

    fam = pd.read_csv(a.families, dtype={"TaskID": str})
    ts = pd.read_csv(os.path.join(a.onet, "Task Statements.txt"), sep="\t", dtype=str)
    occ = pd.read_csv(os.path.join(a.onet, "Occupation Data.txt"), sep="\t", dtype=str)
    t = fam.merge(ts[["O*NET-SOC Code", "Task ID", "Task"]], left_on=["SOC", "TaskID"],
                  right_on=["O*NET-SOC Code", "Task ID"]).merge(occ[["O*NET-SOC Code", "Title"]], on="O*NET-SOC Code")
    t["primary"] = t[FAM].idxmax(axis=1)
    t["soc2"] = t.SOC.str[:2]
    t = t.drop_duplicates("Task")              # one statement once: repeated statements are one observation

    rng = np.random.default_rng(SEED)
    alloc = allocate(t.primary.value_counts(), N_SAMPLE)
    picks = []
    for f, k in alloc.items():
        g = t[t.primary == f]
        w = g.soc2.map(g.soc2.value_counts(normalize=True))
        picks.append(g.sample(n=int(k), weights=w, random_state=int(rng.integers(1e9))))
    s = pd.concat(picks).sample(frac=1, random_state=SEED).reset_index(drop=True)
    s["item"] = np.arange(1, len(s) + 1)

    os.makedirs(os.path.dirname(a.key), exist_ok=True)
    s[["item", "SOC", "TaskID", "primary", *FAM, "in_play", "K", "E"]].to_csv(a.key, index=False)

    form = s[["item", "Title", "Task"]].rename(columns={"item": "N.º", "Title": "Ocupación", "Task": "Tarea (O*NET)"})
    form["Familia principal (F1–F7 o N)"] = ""
    form["Familia secundaria (opcional)"] = ""
    form["Seguridad (1 baja – 3 alta)"] = ""
    form["Comentario"] = ""
    os.makedirs(os.path.dirname(a.form), exist_ok=True)
    with pd.ExcelWriter(a.form, engine="openpyxl") as xw:
        pd.DataFrame({
            "Instrucciones": [
                "Para cada tarea, indique QUÉ FAMILIA DE IA ejecutaría hoy (2026) la parte automatizable de la tarea.",
                "No se pregunta CUÁNTO es automatizable, sino CON QUÉ familia se haría si se hiciera con IA.",
                "Si ninguna familia la ejecutaría hoy, escriba N. Codifique sin consultar a la otra persona ni ningún modelo de IA.",
                "", *[f"{c}: {DESCR_ES[c]}" for c in CODES]]}).to_excel(xw, sheet_name="Instrucciones", index=False)
        for coder in ("Codificador_1", "Codificador_2"):
            form.to_excel(xw, sheet_name=coder, index=False)
        ws_list = [xw.book[c] for c in ("Codificador_1", "Codificador_2")]
        from openpyxl.worksheet.datavalidation import DataValidation
        for ws in ws_list:
            for col, opts in (("D", ",".join(CODES)), ("E", ",".join(CODES)), ("F", "1,2,3")):
                dv = DataValidation(type="list", formula1=f'"{opts}"', allow_blank=True)
                ws.add_data_validation(dv)
                dv.add(f"{col}2:{col}{len(form) + 1}")
            ws.column_dimensions["B"].width = 38
            ws.column_dimensions["C"].width = 90
            for c in "DEF":
                ws.column_dimensions[c].width = 22
    print("muestra:", len(s), "por familia de la regla:", alloc.to_dict())


if __name__ == "__main__":
    main()
