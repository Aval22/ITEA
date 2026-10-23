"""
itea.grading — documented, automated grading of O*NET tasks (ITEA v4.1, in development).

Replaces the legacy AXI grades (see docs/grading/AXI_PROVENANCE_EN.md) with
measures built from official taxonomies and validated against independent,
public references. It is never trained on the legacy grades.

    structural  layer 1: K and E priors from the O*NET linkage tables
    validation  external validation (Eloundou et al. human labels, routine-task
                indices, Job Zone), agreement statistics with bootstrap CIs
    technology  layer T inventory: software and tools used by each occupation
    eurostat    layer U adoption: enterprise use of ERP, CRM and AI (Eurostat)
"""
