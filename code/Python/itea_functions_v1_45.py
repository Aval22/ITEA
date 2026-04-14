"""
ITEA Framework v1.45 — Complete Python Functions
Author: Alberto García-Lluis Valencia (URJC)
Date: April 2026
License: CC BY-NC 4.0
"""

import numpy as np
from typing import Union, List

ArrayLike = Union[float, List[float], np.ndarray]


# --- 1. ITEA: Triple Automation Exposure Index ---
def calcular_itea(eac: ArrayLike, eig: ArrayLike, eia: ArrayLike) -> np.ndarray:
    """ITEA = (1/3)·EAC + (1/3)·EIG + (1/3)·EIA"""
    return (np.asarray(eac) + np.asarray(eig) + np.asarray(eia)) / 3


# --- 2. IRO v1.45: Occupational Resilience Index ---
def calcular_iro_v1_45(ca_items: list, cc_items: list,
                        si_reg: float, si_emp: float, si_sind: float) -> float:
    """
    IRO = 0.35·CA + 0.35·CC + 0.30·SI
    v1.45: CC uses 2 items (Critical Thinking, Problem Solving)
    """
    assert len(ca_items) == 5, "CA requires 5 items"
    assert len(cc_items) == 2, "CC v1.45 requires 2 items"
    CA = np.mean(ca_items)
    CC = np.mean(cc_items)
    SI = 0.5 * si_reg + 0.3 * si_emp + 0.2 * si_sind
    return 0.35 * CA + 0.35 * CC + 0.30 * SI


def calcular_iro_v1_3(ca_items: list, cc_items: list,
                       si_reg: float, si_emp: float, si_sind: float) -> float:
    """Legacy v1.3 with 4-item CC."""
    assert len(ca_items) == 5 and len(cc_items) == 4
    CA = np.mean(ca_items)
    CC = np.mean(cc_items)
    SI = 0.5 * si_reg + 0.3 * si_emp + 0.2 * si_sind
    return 0.35 * CA + 0.35 * CC + 0.30 * SI


# --- 3. ICT: Technical Complexity Index ---
def calcular_ict(itd: ArrayLike, ate: ArrayLike, dts: ArrayLike) -> np.ndarray:
    """ICT = 0.35·ITD + 0.30·ATE + 0.35·(1-DTS)"""
    return 0.35 * np.asarray(itd) + 0.30 * np.asarray(ate) + 0.35 * (1 - np.asarray(dts))


# --- 4. IFS: Social Friction Index ---
def calcular_ifs(cde: ArrayLike, dhs: ArrayLike, cc_comm: ArrayLike) -> np.ndarray:
    """IFS = 0.35·CDE + 0.40·DHS + 0.25·CC_comm"""
    return 0.35 * np.asarray(cde) + 0.40 * np.asarray(dhs) + 0.25 * np.asarray(cc_comm)


# --- 5. IPI: Interpersonal Presence Index ---
def calcular_ipi(ci_pres: ArrayLike, ci_rem: ArrayLike) -> np.ndarray:
    """IPI = 0.70·CI_presencial + 0.30·(1 - CI_remoto)"""
    return 0.70 * np.asarray(ci_pres) + 0.30 * (1 - np.asarray(ci_rem))


# --- 6. IEF: Functional Specificity Index ---
def calcular_ief(dpf: ArrayLike, era: ArrayLike, dcf: ArrayLike) -> np.ndarray:
    """IEF = 0.35·DPF + 0.30·ERA + 0.35·DCF"""
    return 0.35 * np.asarray(dpf) + 0.30 * np.asarray(era) + 0.35 * np.asarray(dcf)


# --- 7. GEE: Education-Experience Gradient ---
def calcular_gee_bruto_v1_3(c_rl: ArrayLike, c_rw: ArrayLike) -> np.ndarray:
    """GEE v1.3 OLS: 0.215·C_RL + 0.004·C_RW"""
    return 0.215 * np.asarray(c_rl) + 0.004 * np.asarray(c_rw)


def calcular_gee_bruto_ordinal(c_rl: ArrayLike, c_rw: ArrayLike) -> np.ndarray:
    """GEE v1.45 ordinal: 0.228·C_RL + 0.0035·C_RW"""
    return 0.228 * np.asarray(c_rl) + 0.0035 * np.asarray(c_rw)


def normalizar_gee(gee_bruto: np.ndarray) -> np.ndarray:
    """Min-max normalization to [0,1]."""
    return (gee_bruto - gee_bruto.min()) / (gee_bruto.max() - gee_bruto.min())


# --- 8. IMO: Occupational Mutation Index ---
def calcular_imo(ratio_v1: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """IMO = IMO_muta × min(1.0, log₂(1 + ratio))"""
    r = np.asarray(ratio_v1)
    muta = np.where(r > 0, 1, 0)
    intens = np.where(r > 0, np.minimum(1.0, np.log2(1 + r)), 0.0)
    return muta * intens


# --- TESTS ---
def test_all():
    assert calcular_itea(0, 0, 0) == 0
    assert calcular_itea(1, 1, 1) == 1
    assert round(calcular_itea(0, 1, 0.3), 4) == 0.4333
    assert round(float(calcular_ict(0.6492, 0.4851, 0.028)), 4) == 0.7129
    assert round(float(calcular_ifs(0.8667, 0.7025, 0.8692)), 4) == 0.8016
    assert round(float(calcular_ipi(0.6843, 0.50)), 4) == 0.6290
    assert round(float(calcular_ief(0.1944, 0.0544, 0.0262)), 4) == 0.0935
    assert float(calcular_imo(0)) == 0
    assert float(calcular_imo(1.5)) == 1.0
    print("✅ All ITEA v1.45 Python tests passed")


if __name__ == "__main__":
    test_all()
