import json
import unittest
import pathlib
from exceptions import *
from tokenbox import Tokenbox
from store.enums import StoreSuffixes


class BaseTestStoreMethods:

    class TestStoreMethods(unittest.TestCase):
        store_name = ''
        store_class = None
        config = None
        project_dir = None
        tokenbox = None

        @classmethod
        def setUpClass(cls):
            # set project root directory
            cls.project_dir = (pathlib.Path(__file__).resolve()).parents[1]
            # load configuration file
            with open(cls.project_dir / 'config.json', 'r') as config_file:
                cls.config = json.loads(config_file.read())
            cls.tokenbox = Tokenbox(cls.project_dir / 'test_token.json')
            cls.config['__project_dir'] = cls.project_dir

        def test_authorized(self):
            self.assertTrue(self.store.authorized())

        def test_save_token(self):
            self.assertTrue(self.store.authorized())
            del self.store
            self.store = self.store_class(self.config, self.store_name, self.tokenbox)
            self.assertTrue(self.store.authorized())

        def test_upload_file(self):
            test_dir = pathlib.PurePath('/')
            test_data_name = 'sample1'
            test_path = test_dir / test_data_name
            with open(self.project_dir / 'tests' / 'samples' / test_data_name, 'rb') as testfile:
                test_data = testfile.read()
            self.store.upload_file(test_path, test_data)
            entries = self.store.get_list(test_dir)
            found = False
            for entry in entries:
                if entry.name == test_data_name and entry.is_dir is False:
                    found = True
                    break
            self.assertTrue(found)

        def test_download_file(self):
            test_dir = pathlib.PurePath('/')
            test_data_name = 'sample2'
            test_path = test_dir / test_data_name
            with open(self.project_dir / 'tests' / 'samples' / test_data_name, 'rb') as testfile:
                test_data = testfile.read()
            self.store.upload_file(test_path, test_data)
            download_data = self.store.download_file(test_path)
            self.assertEqual(test_data, download_data)

        def test_make_directory(self):
            test_dir = pathlib.PurePath('/')
            test_dir_name = 'myDir1'
            self.store.make_dir(test_dir, test_dir_name)
            entries = self.store.get_list(test_dir)
            found = False
            for entry in entries:
                if entry.name == test_dir_name and entry.is_dir is True:
                    found = True
                    break
            self.assertTrue(found)

        def test_get_list(self):
            test_samples_dir = pathlib.PurePath('/samples')
            sample_files = ['sample1', 'sample2', 'sample3']
            self.store.make_dir(test_samples_dir.parent, 'samples')
            for sample in sample_files:
                with open(self.project_dir / 'tests' / 'samples' / sample, 'rb') as infile:
                    self.store.upload_file(test_samples_dir / sample, infile.read())
            entries = self.store.get_list(test_samples_dir)
            # we gonna check only names
            names = []
            for entry in entries:
                names.append(entry.name)
            self.assertCountEqual(sample_files, names)

        def test_delete_file(self):
            # upload one file
            test_path = pathlib.PurePath('/sample1')
            with open(self.project_dir / 'tests' / 'samples' / 'sample1', 'rb') as testfile:
                self.store.upload_file(test_path, testfile.read())
            # try to download after removal
            self.store.remove(test_path)
            with self.assertRaises(NoEntryError):
                sample1_data = self.store.download_file(test_path)

        def test_delete_directory(self):
            # entries before upload samples directory
            test_root = pathlib.PurePath('/')
            before_upload = self.store.get_list(test_root)
            # upload samples directory
            test_samples_dir = pathlib.PurePath('/samples')
            sample_files = ['sample1', 'sample2', 'sample3']
            self.store.make_dir(test_samples_dir.parent, 'samples')
            for sample in sample_files:
                with open(self.project_dir / 'tests' / 'samples' / sample, 'rb') as infile:
                    self.store.upload_file(test_samples_dir / sample, infile.read())
            self.store.remove(test_samples_dir)
            # it will be same if removal was successful
            after_upload = self.store.get_list(test_root)
            self.assertCountEqual(before_upload, after_upload)

        def test_delete_entry_not_exists(self):
            test_path = pathlib.PurePath('/someEntry')
            with self.assertRaises(NoEntryError):
                self.store.remove(test_path)

        def test_upload_duplicate_name(self):
            test_path = pathlib.PurePath('/sample1')
            with open(self.project_dir / 'tests' / 'samples' / 'sample1', 'rb') as testfile:
                self.store.upload_file(test_path, testfile.read())
            # same name but different content
            with open(self.project_dir / 'tests' / 'samples' / 'sample2', 'rb') as testfile:
                with self.assertRaises(DuplicateEntryError):
                    self.store.upload_file(test_path, testfile.read())

        def test_make_duplicate_directory(self):
            test_dir = pathlib.PurePath('/')
            test_dir_name = 'myDir1'
            self.store.make_dir(test_dir, test_dir_name)
            with self.assertRaises(DuplicateEntryError):
                self.store.make_dir(test_dir, test_dir_name)

        def test_download_file_not_exists(self):
            test_path = pathlib.PurePath('/sample1')
            with self.assertRaises(NoEntryError):
                data = self.store.download_file(test_path)

        def test_get_list_on_invalid_path(self):
            test_samples_dir = pathlib.PurePath('/samples')
            with self.assertRaises(NoEntryError):
                entries = self.store.get_list(test_samples_dir)

        def test_updown_internal_only_name(self):
            test_path = pathlib.PurePath('/sample')
            with open(self.project_dir / 'tests' / 'samples' / 'sample1', 'rb') as testfile:
                test_data = testfile.read()
            # '.unidrive_chunk' is suffix for internal chunk file
            self.store.upload_file(test_path.with_suffix(StoreSuffixes.CHUNK_FILE.value), test_data)
            ret = self.store.download_file(test_path.with_suffix(StoreSuffixes.CHUNK_FILE.value))
            self.assertEqual(test_data, ret)

            # '.unidrive_recipe' is suffix for internal chunk file
            self.store.upload_file(test_path.with_suffix(StoreSuffixes.RECIPE_FILE.value), test_data)
            ret = self.store.download_file(test_path.with_suffix(StoreSuffixes.RECIPE_FILE.value))
            self.assertEqual(test_data, ret)

        def test_rename(self):
            test_path = pathlib.PurePath('/sample1')
            test_path2 = pathlib.PurePath('/sample2')
            with open(self.project_dir / 'tests' / 'samples' / 'sample1', 'rb') as testfile:
                self.assertTrue(self.store.upload_file(test_path, testfile.read()))
            self.assertTrue(self.store.rename(test_path, test_path2))
            entries = self.store.get_list(pathlib.PurePath('/'))
            self.assertIn('sample2', [x.name for x in entries])