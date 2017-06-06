import unittest
import pathlib
from tokenbox import Tokenbox


class TestTokenbox(unittest.TestCase):
    tokenfile_path = None

    @classmethod
    def setUpClass(cls):
        cls.tokenfile_path = (pathlib.Path(__file__).resolve()).parents[1] / 'tokenbox_test.json'

    @classmethod
    def tearDownClass(cls):
        cls.tokenfile_path.unlink()

    def setUp(self):
        self.tokenbox = Tokenbox(self.tokenfile_path)

    def tearDown(self):
        self.tokenbox.forget_all()
        del self.tokenbox

    def test_load_empty_token(self):
        test_name = 'FalseKey@GoogleDrive'
        self.assertIsNone(self.tokenbox.load(test_name))

    def test_save_load_forget_token(self):
        test_name = 'example@GoogleDrive'
        test_token = {'AccessToken': 'abc', 'RefreshToken': 'def'}
        self.tokenbox.save(test_name, test_token)
        self.assertDictEqual(test_token, self.tokenbox.load(test_name))
        self.tokenbox.forget(test_name)
        self.assertIsNone(self.tokenbox.load(test_name))

    def test_file_update(self):
        test_name = 'example@GoogleDrive'
        test_token = {'AccessToken': 'abc', 'RefreshToken': 'def'}
        self.tokenbox.save(test_name, test_token)

        del self.tokenbox
        self.tokenbox = Tokenbox(self.tokenfile_path)

        self.assertDictEqual(test_token, self.tokenbox.load(test_name))
        self.tokenbox.forget(test_name)

        del self.tokenbox
        self.tokenbox = Tokenbox(self.tokenfile_path)

        self.assertIsNone(self.tokenbox.load(test_name))