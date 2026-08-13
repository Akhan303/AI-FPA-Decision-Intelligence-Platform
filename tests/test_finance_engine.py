import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from finance_engine import build_model, build_monthly_detail

class FinanceEngineTests(unittest.TestCase):
    def test_model_is_deterministic(self):
        self.assertEqual(build_model(), build_model())

    def test_complete_region_month_grain(self):
        rows = build_monthly_detail()
        self.assertEqual(len(rows), 48)
        self.assertEqual(len({(r["month_index"], r["region"]) for r in rows}), 48)

    def test_kpis_reconcile(self):
        m = build_model()
        self.assertEqual(round(sum(r["outlook_revenue"] for r in m["detail"]), 2), m["kpis"][0]["revenue"])
        self.assertEqual(round(sum(r["outlook_ebitda"] for r in m["detail"]), 2), m["kpis"][0]["ebitda"])

    def test_scenarios_are_decision_useful(self):
        rows = {r["scenario"]: r for r in build_model()["scenarios"]}
        self.assertGreater(rows["Upside"]["revenue"], rows["Base"]["revenue"])
        self.assertGreater(rows["Base"]["revenue"], rows["Downside"]["revenue"])
        self.assertGreater(rows["Upside"]["free_cash_flow"], rows["Base"]["free_cash_flow"])
        self.assertGreater(rows["Base"]["free_cash_flow"], rows["Downside"]["free_cash_flow"])
        self.assertLess(rows["Upside"]["nwc_days"], rows["Base"]["nwc_days"])
        self.assertLess(rows["Base"]["nwc_days"], rows["Downside"]["nwc_days"])

    def test_all_controls_pass(self):
        self.assertEqual({r["status"] for r in build_model()["quality"]}, {"Passed"})

if __name__ == "__main__":
    unittest.main()

