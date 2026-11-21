import unittest
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from clean_superstore import clean_orders, monthly_kpis

class CleaningTests(unittest.TestCase):
    def test_margin_and_order_count(self):
        x = pd.DataFrame({"Order ID": ["A", "A", "B"], "Order Date": ["2022-01-10"]*3,
                          "Sales": [100, 50, 200], "Profit": [10, -5, 40],
                          "Quantity": [1, 2, 3], "Discount": [0, .2, 0]})
        clean, report = clean_orders(x)
        self.assertEqual(report["distinct_orders"], 2)
        m = monthly_kpis(clean)
        self.assertEqual(m.iloc[0]["orders"], 2)
        self.assertEqual(m.iloc[0]["sales"], 350)
        self.assertAlmostEqual(m.iloc[0]["profit_margin"], 45/350)
    def test_missing_required_field_raises(self):
        with self.assertRaises(ValueError):
            clean_orders(pd.DataFrame({"Sales": [1]}))

if __name__ == "__main__":
    unittest.main()
