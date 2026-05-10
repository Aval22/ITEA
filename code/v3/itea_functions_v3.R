# ============================================================
# ITEA Framework v3.0 — R reference implementation
# ============================================================
# Author: Alberto García-Lluis Valencia
# License: MIT
# Version: 3.0 (April 2026)
# Repository: https://github.com/Aval22/ITEA
# DOI: 10.5281/zenodo.20083102 (v3.0 version DOI; concept DOI: 10.5281/zenodo.19578915)
#
# This implementation reproduces the values stored in
# data/processed/ITEA_v3_0_Workbook.xlsx within numerical
# precision (Δ < 1e-6 over the 1,016 occupations).
#
# THREE KEY FUNCTIONS:
#   itea_v3()        — z-score equal-weight aggregation
#   ira_v3()         — triple residualisation
#   oaei_v3_mult()   — multiplicative canonical OAEI
#   oaei_v3_add()    — additive alternative OAEI v3.0+
#
# ============================================================

#' ITEA v3.0 — Triple Index of Exposure to Automation
#'
#' Aggregates the three components (EAC, EIG, EIA) using z-score
#' normalisation followed by equal-weight averaging and final
#' min-max projection to [0, 1]. This corrects the variance
#' asymmetry pathology of the v2.1 equal-weight-in-[0,1] approach
#' that was diluting the EIA Agentic-regime signal.
#'
#' Reference: ITEA v3.0 Consolidated Methodology, §4.
#' Motivation: Paper 8A "The Structural Flaw" (García-Lluis
#' Valencia, 2026a). See §4.4 of the methodology document for
#' the case-study reasoning.
#'
#' @param eac numeric vector — Cognitive Automation Exposure
#' @param eig numeric vector — Generative AI Exposure
#' @param eia numeric vector — Agentic AI Exposure
#' @return numeric vector of ITEA v3.0 values in [0, 1]
#'
#' @examples
#' df <- read.csv("data/processed/itea_components.csv")
#' df$ITEA_v30 <- itea_v3(df$EAC, df$EIG, df$EIA)
itea_v3 <- function(eac, eig, eia) {
  z <- function(x) {
    valid <- !is.na(x)
    out <- rep(NA_real_, length(x))
    out[valid] <- (x[valid] - mean(x[valid])) / sd(x[valid])
    out
  }
  raw <- (z(eac) + z(eig) + z(eia)) / 3
  rmin <- min(raw, na.rm = TRUE)
  rmax <- max(raw, na.rm = TRUE)
  (raw - rmin) / (rmax - rmin)
}


#' IRA v3.0 — Adaptive Resilience Index with triple residualisation
#'
#' Combines CA (raw, weight 0.60) with IRO_residual (weight 0.40),
#' where IRO_residual is the residual of OLS(IRO_v1.45 ~ GEE +
#' ITEA_v3.0 + ICT) min-max-normalised to [0, 1]. The triple
#' residualisation against all structural moderators ensures
#' clean discriminant validity while preserving 84% of the
#' original IRO variance.
#'
#' Reference: ITEA v3.0 Consolidated Methodology, §5.
#' Motivation: Paper 8C "QE and Senior Workforce Restructuring"
#' (García-Lluis Valencia, 2026c). See §5.4 of the methodology
#' document for the case-study reasoning.
#'
#' DEPENDENCY: ITEA v3.0 must be computed first.
#'
#' @param ca       numeric vector — Cognitive Adaptability component
#' @param iro_v145 numeric vector — IRO from v1.45 (legacy input)
#' @param gee      numeric vector — Education-Experience Gradient
#' @param itea_v3  numeric vector — ITEA v3.0 (computed via itea_v3())
#' @param ict      numeric vector — Technical Complexity Index
#' @return numeric vector of IRA v3.0 values in [0, 1]
ira_v3 <- function(ca, iro_v145, gee, itea_v3, ict) {
  # Triple residualisation
  valid <- !is.na(ca) & !is.na(iro_v145) & !is.na(gee) &
           !is.na(itea_v3) & !is.na(ict)

  if (sum(valid) < 4) {
    stop("Insufficient non-missing observations for triple residualisation")
  }

  # OLS on complete cases
  fit <- lm(iro_v145 ~ gee + itea_v3 + ict, subset = valid)
  iro_residual <- rep(NA_real_, length(iro_v145))
  iro_residual[valid] <- residuals(fit)

  # Min-max normalisation
  rmin <- min(iro_residual, na.rm = TRUE)
  rmax <- max(iro_residual, na.rm = TRUE)
  iro_residual_n <- (iro_residual - rmin) / (rmax - rmin)

  ca_min <- min(ca, na.rm = TRUE)
  ca_max <- max(ca, na.rm = TRUE)
  ca_n <- (ca - ca_min) / (ca_max - ca_min)

  # Weighted combination (60% CA + 40% IRO_residual)
  0.60 * ca_n + 0.40 * iro_residual_n
}


#' OAEI v3.0 multiplicative — canonical Occupational Algorithmic Expropriation Index
#'
#' The canonical multiplicative OAEI preserves the structural
#' form of v2.1 with the upgraded ITEA v3.0 input. This variant
#' is used for backward compatibility with the trilogy of papers
#' (8A, 8B, 8C) that cite the multiplicative formula.
#'
#' OAEI_raw = ITEA × GEE × ICT × (1 − IPI)
#' OAEI = 1 + 99 × (OAEI_raw − min) / (max − min)   ∈ [1, 100]
#'
#' Reference: ITEA v3.0 Consolidated Methodology, §6.1.
#'
#' @param itea_v3 numeric vector — ITEA v3.0
#' @param gee     numeric vector — Education-Experience Gradient
#' @param ict     numeric vector — Technical Complexity Index
#' @param ipi     numeric vector — Interpersonal Presence Index
#' @return numeric vector of OAEI v3.0 values in [1, 100]
oaei_v3_mult <- function(itea_v3, gee, ict, ipi) {
  raw <- itea_v3 * gee * ict * (1 - ipi)
  rmin <- min(raw, na.rm = TRUE)
  rmax <- max(raw, na.rm = TRUE)
  1 + 99 * (raw - rmin) / (rmax - rmin)
}


#' OAEI v3.0+ additive — alternative for criterion-validity-priority applications
#'
#' The additive variant is provided for applications where
#' criterion validity (against wage, employment outcomes) is
#' the primary concern. It improves r(OAEI, Wage) from 0.58
#' (multiplicative) to 0.66, while preserving external
#' convergent validation against AIOE at 0.80.
#'
#' OAEI+_raw = 0.5·GEE + 0.3·ITEA + 0.2·ICT·(1 − IPI)
#' OAEI+ = 1 + 99 × (OAEI+_raw − min) / (max − min)   ∈ [1, 100]
#'
#' Reference: ITEA v3.0 Consolidated Methodology, §6.2.
#' Motivation: Paper 8B "Beyond the Pigouvian Trap" (García-
#' Lluis Valencia, 2026b). See §6.5 of the methodology document
#' for the case-study reasoning.
#'
#' @param itea_v3 numeric vector — ITEA v3.0
#' @param gee     numeric vector — Education-Experience Gradient
#' @param ict     numeric vector — Technical Complexity Index
#' @param ipi     numeric vector — Interpersonal Presence Index
#' @return numeric vector of OAEI v3.0+ values in [1, 100]
oaei_v3_add <- function(itea_v3, gee, ict, ipi) {
  raw <- 0.5 * gee + 0.3 * itea_v3 + 0.2 * ict * (1 - ipi)
  rmin <- min(raw, na.rm = TRUE)
  rmax <- max(raw, na.rm = TRUE)
  1 + 99 * (raw - rmin) / (rmax - rmin)
}


#' Use-case selector — guidance for choosing OAEI variant
#'
#' Returns a recommendation for which OAEI variant to use.
#' Reference: ITEA v3.0 Consolidated Methodology, §6.4 Table 6.2.
#'
#' @param use_case character string — one of:
#'   "trilogy_replication", "aioe_meta_analysis", "wage_modelling",
#'   "sectoral_aggregation", "theoretical_exposition", "new_research"
#' @return character — recommended variant
oaei_recommend <- function(use_case) {
  recommendations <- list(
    trilogy_replication      = "OAEI v3.0 multiplicative — for backward compatibility with cited formula",
    aioe_meta_analysis       = "OAEI v3.0+ additive — for maximum AIOE convergence",
    wage_modelling           = "OAEI v3.0+ additive — criterion validity = 0.66",
    sectoral_aggregation     = "Either variant — both produce similar SOC Major rankings",
    theoretical_exposition   = "OAEI v3.0 multiplicative — conceptual alignment with SECI",
    new_research             = "OAEI v3.0+ additive as primary, multiplicative as robustness check"
  )
  if (use_case %in% names(recommendations)) {
    recommendations[[use_case]]
  } else {
    paste0("Unknown use case. Choose one of: ",
           paste(names(recommendations), collapse = ", "))
  }
}

# ============================================================
# Validation utility — reconcile against stored workbook values
# ============================================================

#' Reconciliation check — confirm functions reproduce stored values
#'
#' Loads the v3.0 workbook and compares computed values against
#' stored values. Used in test suite and as an integrity check.
#'
#' @param workbook_path character — path to ITEA_v3_0_Workbook.xlsx
#' @return data.frame with reconciliation diffs per indicator
itea_reconcile <- function(workbook_path = "data/processed/ITEA_v3_0_Workbook.xlsx") {
  if (!requireNamespace("readxl", quietly = TRUE)) {
    stop("readxl package required for reconciliation")
  }
  df <- readxl::read_excel(workbook_path,
                            sheet = "ITEA_INDICATORS_v3.0",
                            skip = 2)

  itea_check <- itea_v3(df$EAC, df$EIG, df$EIA)
  ira_check  <- ira_v3(df$CA,
                       df$`IRO v1.45 (legacy)`,
                       df$`GEE v2.1`,
                       itea_check,
                       df$ICT)
  oaei_check <- oaei_v3_mult(itea_check, df$`GEE v2.1`,
                              df$ICT, df$IPI)
  oaei_plus_check <- oaei_v3_add(itea_check, df$`GEE v2.1`,
                                  df$ICT, df$IPI)

  data.frame(
    indicator = c("ITEA v3.0", "IRA v3.0",
                  "OAEI v3.0", "OAEI v3.0+ additive"),
    max_abs_diff = c(
      max(abs(itea_check - df$`ITEA v3.0`), na.rm = TRUE),
      max(abs(ira_check - df$`IRA v3.0`), na.rm = TRUE),
      max(abs(oaei_check - df$`OAEI v3.0`), na.rm = TRUE),
      max(abs(oaei_plus_check - df$`OAEI v3.0+ additive`), na.rm = TRUE)
    )
  )
}

# End of file
