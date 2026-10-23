"""Tests for the layer-T inventory and the Eurostat JSON-stat parser (layer U)."""
import os

import pandas as pd
import pytest

from itea.grading.eurostat import parse_jsonstat
from itea.grading.technology import inventory, pilot_targets, vendor_presence

EXTERNAL = os.environ.get("ITEA_EXTERNAL", os.path.join(os.path.dirname(__file__), "..", "data", "external"))
ONET = os.path.join(EXTERNAL, "db_30_2_text")


def test_parse_jsonstat_sparse_values():
    doc = {"id": ["geo", "time"], "size": [2, 2],
           "dimension": {"geo": {"category": {"index": {"ES": 0, "DE": 1}}},
                         "time": {"category": {"index": {"2023": 0, "2024": 1}}}},
           "value": {"0": 10.0, "3": 30.0}}               # ES-2023 and DE-2024 only
    df = parse_jsonstat(doc)
    assert df.values.tolist() == [["ES", "2023", 10.0], ["DE", "2024", 30.0]]


def test_inventory_on_synthetic(tmp_path):
    sw = pd.DataFrame({"O*NET-SOC Code": ["13-2041.00", "13-2041.00", "47-2061.00"],
                       "Example": ["SAP ERP", "Microsoft Excel", "AutoCAD"],
                       "Commodity Code": ["1", "2", "3"],
                       "Commodity Title": ["ERP software", "Spreadsheet software", "CAD software"],
                       "Hot Technology": ["Y", "Y", "N"], "In Demand": ["N", "Y", "N"]})
    sw.to_csv(tmp_path / "Technology Skills.txt", sep="\t", index=False)
    pd.DataFrame({"O*NET-SOC Code": ["47-2061.00"], "Example": ["Shovels"], "Commodity Code": ["9"],
                  "Commodity Title": ["Shovels"]}).to_csv(tmp_path / "Tools Used.txt", sep="\t", index=False)
    inv = inventory(str(tmp_path))
    assert inv.set_index("product").loc["SAP ERP", "vendor"] == "SAP"
    assert inv.set_index("product").loc["AutoCAD", "vendor"] == "Autodesk"
    assert set(vendor_presence(inv)["vendor"]) == {"SAP", "Microsoft", "Autodesk"}
    # only software used in pilot occupations (13-2041 is a finance occupation; 47-2061 is not)
    assert set(pilot_targets(inv)["product"]) == {"Microsoft Excel", "SAP ERP"}


@pytest.mark.skipif(not os.path.isdir(ONET), reason="O*NET not fetched (run `itea fetch`)")
def test_real_inventory_size():
    inv = inventory(ONET)
    assert inv.loc[inv["kind"] == "software", "product"].nunique() == 8785
    assert vendor_presence(inv).set_index("vendor").loc["Microsoft", "occupations"] > 800
