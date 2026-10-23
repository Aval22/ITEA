"""
Backward-compatible import path for the ITEA v3.0 reference implementation.

The code now lives in the installable package (src/itea/v3.py); this shim
keeps `from itea_functions_v3 import ...` working for existing scripts.
"""
import os
import sys

try:
    from itea.v3 import *  # noqa: F401,F403
    from itea.v3 import __version__  # noqa: F401
except ImportError:  # package not installed: use the source tree
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
    from itea.v3 import *  # noqa: F401,F403
    from itea.v3 import __version__  # noqa: F401
