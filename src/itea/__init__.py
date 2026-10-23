"""
ITEA Framework — occupational exposure and algorithmic expropriability.

Two layers share this package:

    itea.v3        ITEA v3.0 indicators on O*NET (ITEA, IRA, OAEI), US SOC axis
    itea.rollup    generic task -> activity -> occupation -> ISCO-08 roll-up
    itea.axi       AXI task grades rolled up to activities and occupations
    itea.crosswalk official BLS SOC 2018 -> ISCO-08 crosswalk
    itea.oaxi_eu   OAXI-EU, the expropriability index on the ISCO-08 / ESCO axis
    itea.datasets  packaged AXI grades and the JRC145832 ISCO-3 benchmark

Repository: https://github.com/Aval22/ITEA · concept DOI 10.5281/zenodo.19578915
"""

__version__ = "4.0.0"

from .axi import axi_to_occupations, load_axi  # noqa: E402
from .crosswalk import build_crosswalk  # noqa: E402
from .datasets import axi_path, jrc_benchmark  # noqa: E402
from .rollup import to_activities, to_isco, to_occupations  # noqa: E402
from .oaxi_eu import KAPPA, convergence, kappa_grid, oaxi_eu  # noqa: E402

__all__ = ["__version__", "axi_to_occupations", "load_axi", "build_crosswalk", "axi_path", "jrc_benchmark",
           "KAPPA", "oaxi_eu", "convergence", "kappa_grid",
           "to_activities", "to_occupations", "to_isco"]
