import unittest,tempfile
from pathlib import Path
from app import index,search,tokens
class Tests(unittest.TestCase):
    def test_normalization(self):self.assertEqual(tokens('AUTOMAÇÃO Python!'),['automacao','python'])
    def test_ranking_rebuild_and_no_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'docs';folder.mkdir();db=root/'search.db'
            (folder/'a.md').write_text('Python python automação',encoding='utf-8');(folder/'b.txt').write_text('Python',encoding='utf-8')
            self.assertEqual(index(folder,db),2);self.assertEqual(search('python',db)[0]['path'],'a.md')
            self.assertEqual(len(search('AUTOMACAO',db)),1);self.assertEqual(search('java',db),[])
            (folder/'a.md').unlink();index(folder,db);self.assertEqual(len(search('python',db)),1)
    def test_failed_rebuild_preserves_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'docs';folder.mkdir();db=root/'index.db'
            (folder/'a.txt').write_text('Python',encoding='utf-8');index(folder,db)
            (folder/'bad.txt').write_bytes(b'\xff')
            with self.assertRaises(UnicodeError):index(folder,db)
            self.assertEqual(len(search('python',db)),1)
