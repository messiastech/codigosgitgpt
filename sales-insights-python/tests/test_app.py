import unittest,tempfile
from pathlib import Path
from decimal import Decimal
from app import analyze,render
class Tests(unittest.TestCase):
    def test_sample(self):
        data=analyze('examples/sales.csv');self.assertEqual(data['total'],Decimal('2490'));self.assertEqual(data['units'],8)
    def test_precision_and_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'data.csv';path.write_text('date,product,quantity,unit_price\n2026-01-01,<script>,3,0.10\n'.replace('\n','\n'),encoding='utf-8')
            data=analyze(path);self.assertEqual(data['total'],Decimal('.30'));self.assertNotIn('<script>',render(data))
    def test_invalid_and_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'data.csv'
            for row in ('2026-01-01,A,-1,10','2026-01-01,A,1,NaN','2026-02-30,A,1,10','2026-01-01,A,1,0.001'):
                path.write_text('date,product,quantity,unit_price\n'+row,encoding='utf-8')
                with self.assertRaises(ValueError):analyze(path)
            path.write_text('date,product,quantity,unit_price\n',encoding='utf-8');self.assertEqual(analyze(path)['total'],0)
