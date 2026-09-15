import unittest,tempfile,json
from pathlib import Path
from app import snapshot,verify
class Tests(unittest.TestCase):
    def test_all_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'files';folder.mkdir();manifest=root/'manifest.json'
            (folder/'a').write_text('a');(folder/'b').write_text('b');snapshot(folder,manifest)
            self.assertFalse(any(verify(folder,manifest).values()))
            (folder/'a').write_text('changed');(folder/'b').unlink();(folder/'c').write_text('c')
            self.assertEqual(verify(folder,manifest),{'added':['c'],'removed':['b'],'changed':['a']})
    def test_no_overwrite_and_nested_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'files';folder.mkdir();manifest=root/'manifest.json';snapshot(folder,manifest)
            with self.assertRaises(FileExistsError):snapshot(folder,manifest)
            with self.assertRaises(ValueError):snapshot(folder,folder/'manifest.json')
    def test_invalid_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'files';folder.mkdir();manifest=root/'manifest.json';manifest.write_text('[]')
            with self.assertRaises(ValueError):verify(folder,manifest)
