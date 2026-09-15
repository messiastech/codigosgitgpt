import unittest,tempfile,json
from pathlib import Path
from app import validate,validate_contract
class Tests(unittest.TestCase):
    def test_sample(self):
        contract=json.loads(Path('examples/contract.json').read_text());self.assertTrue(validate('examples/customers.csv',contract)['valid'])
    def test_reports_all_violations(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'data.csv';source.write_text('id,age\nA,2\nA,-1\n,wrong\n')
            result=validate(source,{'columns':{'id':{'required':True,'unique':True},'age':{'type':'integer','min':0}}})
            self.assertFalse(result['valid']);self.assertEqual(len(result['errors']),4)
    def test_contract_and_schema(self):
        with self.assertRaises(ValueError):validate_contract({'columns':{'a':{'type':'unknown'}}})
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'data.csv';source.write_text('wrong\na\n');self.assertFalse(validate(source,{'columns':{'a':{}}})['valid'])
    def test_min_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'data.csv';source.write_text('id\n');self.assertFalse(validate(source,{'columns':{'id':{}},'min_rows':1})['valid'])
