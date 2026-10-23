"""
Command-line entry point.

    itea fetch    [--dest data/external]
    itea build-eu [--axi PATH] [--external data/external] [--out outputs] [--kappa 0.40]
    itea validate [--index outputs/oaxi_eu.csv]

By default build-eu uses the AXI grades shipped with the package.
"""

from __future__ import annotations

import argparse
import json
import os

from . import __version__
from .axi import axi_to_occupations, load_axi
from .crosswalk import build_crosswalk
from .datasets import axi_path, jrc_benchmark
from .fetch import SOURCES, fetch, sha256
from .oaxi_eu import KAPPA, convergence, oaxi_eu


def _build_eu(a) -> None:
    ext = a.external
    onet_dir = os.path.join(ext, "db_30_2_text")
    if not os.path.isdir(onet_dir):
        raise SystemExit(f"{onet_dir} not found: run `itea fetch --dest {ext}` first.")
    os.makedirs(a.out, exist_ok=True)
    a.axi = a.axi or axi_path()

    occ = axi_to_occupations(load_axi(a.axi), onet_dir)
    cw = build_crosswalk(os.path.join(ext, SOURCES["isco_soc"]["file"]),
                         os.path.join(ext, SOURCES["soc_2010_2018"]["file"]))
    idx = oaxi_eu(occ, cw, kappa=a.kappa)

    occ.round(4).to_csv(os.path.join(a.out, "occupation_shares.csv"), index=False)
    cw.to_csv(os.path.join(a.out, "crosswalk_soc2018_isco08.csv"), index=False)
    out = os.path.join(a.out, "oaxi_eu.csv")
    idx.round(4).to_csv(out, index=False)

    meta = {"index": "OAXI-EU", "itea_version": __version__, "kappa": a.kappa,
            "n_onet_soc": int(occ["SOC"].nunique()), "n_isco": int(len(idx)),
            "inputs_sha256": {"axi": sha256(a.axi),
                              **{k: v["sha256"] for k, v in SOURCES.items()}},
            "output_sha256": sha256(out)}
    with open(os.path.join(a.out, "oaxi_eu.meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"OAXI-EU: {meta['n_isco']} ISCO-08 groups from {meta['n_onet_soc']} O*NET-SOC "
          f"occupations -> {out}")


def _validate(a) -> None:
    import pandas as pd
    idx = pd.read_csv(a.index, dtype={"isco": str, "isco3": str})
    c = convergence(idx, jrc_benchmark())
    print(f"OAXI-EU vs JRC145832 (ISCO-3, n={c['n_isco3']}): "
          f"Pearson {c['pearson']:.3f}, Spearman {c['spearman']:.3f}")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="itea", description=f"ITEA Framework {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="download O*NET 30.2 and the BLS crosswalks")
    f.add_argument("--dest", default="data/external")

    b = sub.add_parser("build-eu", help="build OAXI-EU on the ISCO-08 axis")
    b.add_argument("--axi", default=None, help="AXI grades file (default: packaged copy)")
    b.add_argument("--external", default="data/external")
    b.add_argument("--out", default="outputs")
    b.add_argument("--kappa", type=float, default=KAPPA)

    v = sub.add_parser("validate", help="convergence of an OAXI-EU table with the JRC145832 benchmark")
    v.add_argument("--index", default="outputs/oaxi_eu.csv")

    a = ap.parse_args(argv)
    if a.cmd == "fetch":
        for k, p in fetch(a.dest).items():
            print(f"{k:14s} {p}")
    elif a.cmd == "build-eu":
        _build_eu(a)
    else:
        _validate(a)


if __name__ == "__main__":
    main()
