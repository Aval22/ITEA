# Writes the R reference v3 functions' outputs on a fixed input, for the
# Python parity test (tests/test_v3_r_parity.py).
# Usage: Rscript tests/r/v3_parity.R <repo_root> <out.csv>
args <- commandArgs(trailingOnly = TRUE)
source(file.path(args[1], "code", "v3", "itea_functions_v3.R"))
i <- 1:60
d <- data.frame(
  eac = (sin(i) + 1) / 2, eig = (cos(1.7 * i) + 1) / 2, eia = (i %% 7) / 6,
  ca = (sin(0.3 * i) + 1) / 2, iro = (cos(0.5 * i) + 1) / 2,
  gee = (i %% 11) / 10, ict = (sin(2.1 * i) + 1) / 2, ipi = (i %% 5) / 8
)
d$eig[c(5, 17)] <- NA
d$itea <- itea_v3(d$eac, d$eig, d$eia)
d$ira <- ira_v3(d$ca, d$iro, d$gee, d$itea, d$ict)
d$oaei_mult <- oaei_v3_mult(d$itea, d$gee, d$ict, d$ipi)
d$oaei_add <- oaei_v3_add(d$itea, d$gee, d$ict, d$ipi)
write.csv(d, args[2], row.names = FALSE)
