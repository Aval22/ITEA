#!/usr/bin/env python3
"""
05_build_dashboard.py — Paso 4: dashboard de 3 entornos ITEA (prototipo).

Genera un HTML autocontenido (datos embebidos, sin dependencias externas) con
conmutador O*NET / ESCO / Híbrido / Comparativo sobre el eje ISCO-08.
Salida: 08_outputs/entornos/dashboard.html
"""
import argparse, os, json
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".")
    a = ap.parse_args()
    B = a.base
    u = pd.read_parquet(f"{B}/08_outputs/entornos/comparativo/itea_by_isco.parquet")
    # etiquetas ISCO (4 díg)
    isco = pd.read_csv(f"{B}/01_ESCO_v1.2.1/ESCO dataset - v1.2.1 - classification - en - csv/ISCOGroups_en.csv")
    isco["code"] = isco["code"].astype(str)
    lab = dict(zip(isco["code"], isco["preferredLabel"]))
    u["label"] = u["isco"].astype(int).astype(str).map(lab).fillna("(sin etiqueta)")
    # JSON limpio (NaN -> None)
    recs = json.loads(u.round(3).to_json(orient="records"))
    meta = {
        "n_isco": int(len(u)),
        "n_3": int((u["n_entornos"] == 3).sum()),
        "n_onet": int(u["in_onet"].sum()),
        "n_esco": int(u["in_esco"].sum()),
        "n_hib": int(u["in_hibrido"].sum()),
    }
    html = TEMPLATE.replace("__DATA__", json.dumps(recs, ensure_ascii=False))
    html = html.replace("__META__", json.dumps(meta, ensure_ascii=False))
    out = f"{B}/08_outputs/entornos/dashboard.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Dashboard guardado: {out} ({len(recs)} ISCO) | meta={meta}")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ITEA — Dashboard de 3 entornos</title>
<style>
:root{--bg:#0f1419;--card:#1a2230;--ink:#e6edf3;--mut:#8b98a9;--acc:#4ea1ff;--line:#2a3441;
--onet:#f0883e;--esco:#3fb950;--hib:#a371f7;--comp:#4ea1ff;}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 system-ui,sans-serif;background:var(--bg);color:var(--ink)}
.wrap{max-width:1100px;margin:0 auto;padding:24px}
h1{font-size:20px;margin:0 0 2px}.sub{color:var(--mut);font-size:13px;margin-bottom:18px}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.tab{padding:8px 16px;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;cursor:pointer;font-weight:600}
.tab.on{border-color:transparent}
.tab[data-e=onet].on{background:var(--onet);color:#1a1205}.tab[data-e=esco].on{background:var(--esco);color:#04220c}
.tab[data-e=hibrido].on{background:var(--hib);color:#1a0f2e}.tab[data-e=comparativo].on{background:var(--comp);color:#04162e}
.bar{display:flex;gap:14px;align-items:center;margin-bottom:12px;flex-wrap:wrap}
input{background:var(--card);border:1px solid var(--line);color:var(--ink);padding:8px 12px;border-radius:8px;width:260px}
.stat{color:var(--mut);font-size:13px}.stat b{color:var(--ink)}
.note{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--acc);padding:10px 14px;border-radius:8px;margin-bottom:14px;color:var(--mut);font-size:13px}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
th,td{text-align:right;padding:7px 10px;border-bottom:1px solid var(--line)}
th{position:sticky;top:0;background:var(--card);cursor:pointer;color:var(--mut);font-weight:600;white-space:nowrap}
th:first-child,td:first-child,th:nth-child(2),td:nth-child(2){text-align:left}
td:nth-child(2){color:var(--mut);max-width:340px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
tr:hover td{background:#11202f}.tablewrap{max-height:62vh;overflow:auto;border:1px solid var(--line);border-radius:10px}
.foot{color:var(--mut);font-size:12px;margin-top:14px}
</style></head><body><div class="wrap">
<h1>ITEA — Dashboard de 3 entornos</h1>
<div class="sub">Análisis comparativo y unificado sobre el eje ISCO-08 · prototipo (datos embebidos)</div>
<div class="tabs">
<button class="tab on" data-e="onet">ITEA-US <small>· O*NET</small></button>
<button class="tab" data-e="esco">ITEA-UE <small>· ESCO</small></button>
<button class="tab" data-e="hibrido">BRIDGE US–UE <small>· híbrido</small></button>
<button class="tab" data-e="comparativo">Comparativo</button>
</div>
<div class="note" id="note"></div>
<div class="bar"><input id="q" placeholder="Filtrar por código ISCO o etiqueta…"><span class="stat" id="stat"></span></div>
<div class="tablewrap"><table><thead id="th"></thead><tbody id="tb"></tbody></table></div>
<div class="foot">Fuente: <code>comparativo/itea_by_isco.parquet</code>. AEI/OAEI escala O*NET; K = peso de codificabilidad (reuseLevel); exposición = señal AXI media. Celdas vacías = el entorno no cubre ese ISCO.</div>
</div>
<script>
const DATA=__DATA__, META=__META__;
const ENVS={
 onet:{note:"<b>ITEA-US</b> (instancia nacional sobre O*NET; task-based, eje SOC→ISCO). Indicadores ITEA v3.0 nativos. Límite: mercado laboral USA.",
   flag:"in_onet", cols:[["isco","ISCO",0],["label","Grupo ocupacional",-1],["onet_n_soc","#SOC",0],["onet_mean_AEI","AEI",1],["onet_mean_OAEI_v3","OAEI v3",1],["onet_mean_ITEA_v3","ITEA v3",3],["onet_mean_AIOE","AIOE",2],["onet_mean_wage","Salario med.",0]]},
 esco:{note:"<b>ITEA-UE</b> (instancia nacional sobre ESCO; competence-based). Aporta de forma nativa la codificabilidad (K). Límite: no modela tareas.",
   flag:"in_esco", cols:[["isco","ISCO",0],["label","Grupo ocupacional",-1],["esco_n_occ","#Ocup.",0],["esco_n_essential","Essential",0],["esco_n_optional","Optional",0],["esco_mean_k","K medio",3]]},
 hibrido:{note:"<b>ITEA BRIDGE (US–UE)</b> — marco puente bilateral (tarea O*NET→skill ESCO). Recupera lo task-based sobre ISCO. Límite: error crosswalk + ruido de mapeo.",
   flag:"in_hibrido", cols:[["isco","ISCO",0],["label","Grupo ocupacional",-1],["hib_n_skills","#Skills",0],["hib_n_tasks","#Tareas",0],["hib_mean_score","Score pond.",3],["hib_mean_exposure","Exposición",3],["hib_mean_k","K medio",3]]},
 comparativo:{note:"<b>Comparativo</b>: ITEA-US · ITEA-UE · BRIDGE por ISCO. <code>n</code>=cuántos entornos cubren ese grupo.",
   flag:null, cols:[["isco","ISCO",0],["label","Grupo ocupacional",-1],["n_entornos","n",0],["onet_mean_OAEI_v3","OAEI (O*NET)",1],["esco_mean_k","K (ESCO)",3],["hib_mean_exposure","Exposic. (Híb)",3],["hib_mean_k","K (Híb)",3]]}
};
let cur="onet", sortKey="isco", sortDir=1;
const $=id=>document.getElementById(id);
function fmt(v,d){if(v===null||v===undefined||v!=v)return"·";if(d<0)return v;if(d===0)return Math.round(v).toLocaleString("es");return Number(v).toFixed(d);}
function render(){
 const e=ENVS[cur]; $("note").innerHTML=e.note;
 const q=$("q").value.trim().toLowerCase();
 let rows=DATA.filter(r=>e.flag?r[e.flag]:true);
 if(q)rows=rows.filter(r=>String(r.isco).includes(q)||(r.label||"").toLowerCase().includes(q));
 rows.sort((a,b)=>{let x=a[sortKey],y=b[sortKey];if(x===null)return 1;if(y===null)return -1;
   if(typeof x==="string")return x.localeCompare(y)*sortDir;return (x-y)*sortDir;});
 $("th").innerHTML="<tr>"+e.cols.map(c=>`<th data-k="${c[0]}">${c[1]}${sortKey===c[0]?(sortDir>0?" ▲":" ▼"):""}</th>`).join("")+"</tr>";
 $("tb").innerHTML=rows.map(r=>"<tr>"+e.cols.map(c=>`<td>${fmt(r[c[0]],c[2])}</td>`).join("")+"</tr>").join("");
 $("stat").innerHTML=`Mostrando <b>${rows.length}</b> grupos ISCO`;
 document.querySelectorAll("#th th").forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=1;}render();});
}
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
 document.querySelectorAll(".tab").forEach(x=>x.classList.remove("on"));t.classList.add("on");
 cur=t.dataset.e;sortKey="isco";sortDir=1;render();});
$("q").oninput=render;
document.title=`ITEA — 3 entornos (${META.n_isco} ISCO)`;
render();
</script></body></html>"""

if __name__ == "__main__":
    main()
