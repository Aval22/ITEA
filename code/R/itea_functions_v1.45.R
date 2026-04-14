# ============================================================
# ITEA Framework v1.45 — Complete R Functions
# Author: Alberto García-Lluis Valencia (URJC)
# Date: April 2026
# License: CC BY-NC 4.0
# ============================================================

# Dependencies
# install.packages(c("tidyverse", "readxl", "psych", "performance"))

# --- 1. ITEA: Triple Automation Exposure Index ---
calcular_itea <- function(eac, eig, eia) {
  stopifnot(all(c(eac, eig, eia) >= 0 & c(eac, eig, eia) <= 1))
  return((eac + eig + eia) / 3)
}

# --- 2. IRO v1.45: Occupational Resilience Index ---
# CHANGE v1.45: CC reduced from 4 to 2 items (removed Reasoning, Originality)
calcular_iro_v1.45 <- function(ca_items, cc_items, si_reg, si_emp, si_sind) {
  # ca_items: vector of 5 (Innovation, Adaptability, Tolerance, Curiosity, Initiative)
  # cc_items: vector of 2 (Critical Thinking, Problem Solving) -- v1.45
  stopifnot(length(ca_items) == 5, length(cc_items) == 2)
  CA <- mean(ca_items)
  CC <- mean(cc_items)
  SI <- 0.5 * si_reg + 0.3 * si_emp + 0.2 * si_sind
  return(0.35 * CA + 0.35 * CC + 0.30 * SI)
}

# Legacy v1.3 (4-item CC) for backward compatibility
calcular_iro_v1.3 <- function(ca_items, cc_items_4, si_reg, si_emp, si_sind) {
  stopifnot(length(ca_items) == 5, length(cc_items_4) == 4)
  CA <- mean(ca_items)
  CC <- mean(cc_items_4)
  SI <- 0.5 * si_reg + 0.3 * si_emp + 0.2 * si_sind
  return(0.35 * CA + 0.35 * CC + 0.30 * SI)
}

# --- 3. ICT: Technical Complexity Index ---
calcular_ict <- function(itd, ate, dts) {
  return(0.35 * itd + 0.30 * ate + 0.35 * (1 - dts))
}

# --- 4. IFS: Social Friction Index ---
calcular_ifs <- function(cde, dhs, cc_comm) {
  return(0.35 * cde + 0.40 * dhs + 0.25 * cc_comm)
}

# --- 5. IPI: Interpersonal Presence Index ---
calcular_ipi <- function(ci_presencial, ci_remoto) {
  return(0.70 * ci_presencial + 0.30 * (1 - ci_remoto))
}

# --- 6. IEF: Functional Specificity Index ---
calcular_ief <- function(dpf, era, dcf) {
  return(0.35 * dpf + 0.30 * era + 0.35 * dcf)
}

# --- 7. GEE: Education-Experience Gradient ---
# v1.3 OLS version (backward compatible)
calcular_gee_bruto_v1.3 <- function(c_rl_years, c_rw_months) {
  return(0.215 * c_rl_years + 0.004 * c_rw_months)
}

# v1.45 Ordinal version (recommended)
calcular_gee_bruto_ordinal <- function(c_rl_years, c_rw_months) {
  return(0.228 * c_rl_years + 0.0035 * c_rw_months)
}

# Normalization (apply to full population vector)
normalizar_gee <- function(gee_bruto_vector) {
  (gee_bruto_vector - min(gee_bruto_vector)) /
    (max(gee_bruto_vector) - min(gee_bruto_vector))
}

# --- 8. IMO: Occupational Mutation Index ---
calcular_imo <- function(ratio_v1) {
  imo_muta <- ifelse(ratio_v1 > 0, 1, 0)
  intensidad <- ifelse(ratio_v1 > 0, pmin(1.0, log2(1 + ratio_v1)), 0)
  return(imo_muta * intensidad)
}

# --- VALIDATION ---
test_all_indicators <- function() {
  # ITEA
  stopifnot(calcular_itea(0, 0, 0) == 0)
  stopifnot(calcular_itea(1, 1, 1) == 1)
  stopifnot(round(calcular_itea(0, 1, 0.3), 4) == 0.4333)

  # ICT
  stopifnot(round(calcular_ict(0.6492, 0.4851, 0.028), 4) == 0.7129)

  # IFS
  stopifnot(round(calcular_ifs(0.8667, 0.7025, 0.8692), 4) == 0.8016)

  # IPI
  stopifnot(round(calcular_ipi(0.6843, 0.50), 4) == 0.6290)

  # IEF
  stopifnot(round(calcular_ief(0.1944, 0.0544, 0.0262), 4) == 0.0935)

  # IMO
  stopifnot(calcular_imo(0) == 0)
  stopifnot(calcular_imo(1.5) == 1.0)  # cap test

  message("✅ All ITEA v1.45 R tests passed")
}

test_all_indicators()
