import unittest,tempfile,sqlite3
from contextlib import closing
from pathlib import Path
from app import run,extract
class Tests(unittest.TestCase):
    def test_idempotent_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/'warehouse.db';self.assertEqual(run('examples/orders.csv',db)['inserted'],3)
            result=run('examples/orders.csv',db);self.assertEqual(result,{'inserted':0,'skipped':3,'total_cents':25040})
    def test_conflict_rolls_back_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/'warehouse.db';run('examples/orders.csv',db)
            source=Path(tmp)/'orders.csv';source.write_text('order_id,date,customer,amount\nNEW,2026-01-01,C,1\nO001,2026-01-01,Changed,3\n')
            with self.assertRaises(ValueError):run(source,db)
            with closing(sqlite3.connect(db)) as conn:self.assertEqual(conn.execute('SELECT count(*) FROM orders').fetchone()[0],3)
    def test_rejects_bad_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'orders.csv'
            for amount in ('NaN','-1','0.001'):
                source.write_text('order_id,date,customer,amount\nA,2026-01-01,C,'+amount)
                with self.assertRaises(ValueError):extract(source)
