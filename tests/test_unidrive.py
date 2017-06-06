import unittest
import pathlib
import webbrowser
from UniDrive import UniDrive


class TestUniDrive(unittest.TestCase):
    sample_dir = None
    project_dir = None

    @classmethod
    def setUpClass(cls):
        cls.project_dir = (pathlib.Path(__file__).resolve()).parents[1]
        cls.sample_dir = cls.project_dir / 'tests' / 'samples'
        unidrive = UniDrive(cls.project_dir)
        # google
        try:
            auth_url = unidrive.register_store('GoogleDriveStore', 'test-googledrive')
            webbrowser.open_new(auth_url)
            res = input('response url for test-googledrive :')
            if unidrive.activate_store('test-googledrive', res):
                print('success test-googledrive')
            else:
                print('fail test-googledrive')
        except Exception:
            print('test-googledrive is already registered')
        # dropbox
        try:
            auth_url = unidrive.register_store('DropboxStore', 'test-dropbox')
            webbrowser.open_new(auth_url)
            res = input('response url for test-dropbox :')
            if unidrive.activate_store('test-dropbox', res):
                print('success test-dropbox')
            else:
                print('fail test-dropbox')
        except Exception:
            print('test-dropbox is already registered')
        del unidrive

    def setUp(self):
        self.unidrive = UniDrive(self.project_dir)

    def tearDown(self):
        res = self.unidrive.get_list('/')
        for entry in res:
            if entry.is_dir:
                self.unidrive.remove_directory('/{0}'.format(entry.name))
            else:
                self.unidrive.remove_file('/{0}'.format(entry.name))
        del self.unidrive

    def test_upload(self):
        test_path = '/sample1'
        with open(self.sample_dir / 'sample1', 'rb') as f:
            test_data = f.read()
        self.assertTrue(self.unidrive.upload_file(test_path, test_data))

    def test_download(self):
        test_path = '/sample1'
        with open(self.sample_dir / 'sample1', 'rb') as f:
            test_data = f.read()
        self.assertTrue(self.unidrive.upload_file(test_path, test_data))
        self.assertEqual(self.unidrive.download_file(test_path), test_data)

    def test_upload_chunked(self):
        test_path = '/sample_large'
        with open(self.sample_dir / 'sample_large', 'rb') as f:
            test_data = f.read()
        self.assertTrue(self.unidrive.upload_file(test_path, test_data))

    def test_download_chunked(self):
        test_path = '/sample1'
        with open(self.sample_dir / 'sample_large', 'rb') as f:
            test_data = f.read()
        self.assertTrue(self.unidrive.upload_file(test_path, test_data))
        self.assertEqual(self.unidrive.download_file(test_path), test_data)

    def test_get_list(self):
        test_file_names = ['sample1', 'sample2', 'sample3', 'sample_large']
        for sample in test_file_names:
            with open(self.sample_dir / sample, 'rb') as f:
                self.unidrive.upload_file('/{0}'.format(sample), f.read())
        entries = self.unidrive.get_list('/')
        self.assertCountEqual([x.name for x in entries], test_file_names)

    def test_rename(self):
        test_path = '/sample1'
        test_path2 = '/sample2'
        with open(self.sample_dir / 'sample1', 'rb') as f:
            test_data = f.read()
        self.assertTrue(self.unidrive.upload_file(test_path, test_data))
        self.assertTrue(self.unidrive.rename(test_path, test_path2))
        entries = self.unidrive.get_list('/')
        self.assertIn('sample2', [x.name for x in entries])

    def test_rename_chunked(self):
        test_path = '/sample_large'
        test_path2 = '/sample1'
        with open(self.sample_dir / 'sample_large', 'rb') as f:
            test_data = f.read()
        self.assertTrue(self.unidrive.upload_file(test_path, test_data))
        self.assertTrue(self.unidrive.rename(test_path, test_path2))
        entries = self.unidrive.get_list('/')
        self.assertIn('sample1', [x.name for x in entries])

    def test_usage(self):
        res = self.unidrive.get_usage()
        self.assertCountEqual([x['name'] for x in res], self.unidrive.stores.keys())

    def test_mkdir(self):
        self.unidrive.make_directory('/', 'temp')
        res = self.unidrive.get_list('/')
        for e in res:
            if e.name == 'temp':
                self.assertTrue(e.is_dir)

    def test_rm(self):
        self.unidrive.make_directory('/', 'temp')
        res = self.unidrive.get_list('/')
        for e in res:
            if e.name == 'temp':
                self.assertTrue(e.is_dir)
        test_path = '/sample1'
        with open(self.sample_dir / 'sample1', 'rb') as f:
            test_data = f.read()
        self.assertTrue(self.unidrive.upload_file(test_path, test_data))
        test_path = '/sample_large'
        with open(self.sample_dir / 'sample_large', 'rb') as f:
            test_data = f.read()
        self.assertTrue(self.unidrive.upload_file(test_path, test_data))
        self.assertTrue(self.unidrive.remove_directory('/temp'))
        self.assertTrue(self.unidrive.remove_file('/sample1'))
        self.assertTrue(self.unidrive.remove_file('/sample_large'))