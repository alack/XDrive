import unittest
from store import DirectoryEntry


class TestDirectoryEntry(unittest.TestCase):
    def test_default_file(self):
        test_name = 'sample.txt'
        den = DirectoryEntry(test_name)
        self.assertEqual(test_name, den.name)
        self.assertFalse(den.is_dir)
        self.assertFalse(den.is_chunk)
        self.assertFalse(den.is_recipe)

    def test_chunk_file_name(self):
        test_name = 'sample.unidrive_chunk'
        den = DirectoryEntry(test_name)
        self.assertEqual(test_name, den.name)
        self.assertFalse(den.is_dir)
        self.assertTrue(den.is_chunk)
        self.assertFalse(den.is_recipe)

    def test_recipe_file_name(self):
        test_name = 'sample.unidrive_recipe'
        den = DirectoryEntry(test_name)
        self.assertEqual(test_name, den.name)
        self.assertFalse(den.is_dir)
        self.assertFalse(den.is_chunk)
        self.assertTrue(den.is_recipe)