from concurrent.futures import ThreadPoolExecutor
from typing import List
from store import *
from tokenbox import *
from exceptions import *
from pathlib import Path, PurePath
import json
import Locator


class UniDrive:
    MB = 1024*1024
    __chunking_threshold = 4*MB  # 4 * 1024 * 1024 byte

    def __init__(self, app_dir):
        self.app_dir = Path(app_dir)
        if self.app_dir.is_dir() is False:
            raise Exception("{0} does not exists".format(self.app_dir))
        if (self.app_dir/'config.json').is_file() is False:
            raise Exception("config.json does not exists")

        with open(self.app_dir/'config.json', 'r') as conf:
            self.__config = json.loads(conf.read())
        try:
            with open(self.app_dir/'store_list.json', 'r') as storelist:
                self.__store_list = json.loads(storelist.read())['stores']
        except Exception:
            self.__store_list = []
        self.__tokenbox = Tokenbox(self.app_dir / 'tokenbox.json')

        self.stores = {}
        for store in self.__store_list:
            self.stores[store['name']] = StoreFactory.create_store(store['type'], self.__config, store['name'],
                                                                   self.__tokenbox)

    def __update_store_list(self):
        with open(self.app_dir/'store_list.json', 'w') as conf:
            conf.write(json.dumps({'stores': self.__store_list}, indent=4))

    def register_store(self, store_type, name):
        if name in self.stores:
            raise Exception('Duplicate store name')
        self.stores[name] = StoreFactory.create_store(store_type, self.__config, name, self.__tokenbox)
        return self.stores[name].get_authorization_url()

    def activate_store(self, name, redirect_url):
        try:
            self.stores[name].fetch_token(redirect_url)

        except Exception:
            self.stores[name].delete_token()
            del self.stores[name]
            return False

        else:
            self.__store_list.append({'name': name, 'type': self.stores[name].type_name()})
            self.__update_store_list()
            return True

    def remove_store(self, name):
        if name not in self.stores:
            return
        self.__store_list.remove({'name': name, 'type': self.stores[name].type_name()})
        self.stores[name].delete_token()
        del self.stores[name]
        self.__update_store_list()

    def get_usage(self):
        res = []
        for name, store in self.stores.items():
            x = store.get_usage()
            x['name'] = name
            res.append(x)
        return res

    @staticmethod
    def get_list_filter(future):
        ret = []
        for entry in future.result():
            if entry.is_recipe:
                strip = PurePath(entry.name).stem
                ret.append(DirectoryEntry(strip))
            elif not entry.is_chunk:
                ret.append(entry)
        return ret

    def get_list(self, path: str) -> List[DirectoryEntry]:
        path = PurePath(path)
        dir_filter = set()
        results = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for name, store in self.stores.items():
                futures.append(executor.submit(store.get_list, path))
            futures2 = []
            for future in futures:
                futures2.append(executor.submit(self.get_list_filter, future))

            for future in futures2:
                for entry in future.result():
                    if entry.is_dir:
                        if entry.name not in dir_filter:
                            dir_filter.add(entry.name)
                            results.append(entry)
                    else:
                        results.append(entry)
        return results

    def upload_file(self, path: str, data) -> bool:
        path = PurePath(path)
        parent_path = path.parent
        file_name = path.name
        need_chunking = (len(data) > self.__chunking_threshold)
        if need_chunking:
            try:
                dest_name = Locator.locate(path, self.__store_list)
                self.stores[dest_name].download_file(path)
            except NoEntryError:
                idx = 0
                with ThreadPoolExecutor(max_workers=3) as executor:
                    futures = []
                    off = 0
                    while off < len(data):
                        if (len(data) - off) < (4 * self.MB):
                            sz = len(data) - off
                        else:
                            sz = 4 * self.MB
                        chunk_path = parent_path / (file_name + '.{0}'.format(idx) + StoreSuffixes.CHUNK_FILE.value)
                        chunk_dest = Locator.locate(chunk_path, self.__store_list)
                        futures.append(executor.submit(self.stores[chunk_dest].upload_file,
                                                       chunk_path, data[off:(off+sz)]))
                        off = off + sz
                        idx = idx + 1

                    for future in futures:
                        if future.result() is False:
                            return False
                recipe_path = parent_path / (file_name + StoreSuffixes.RECIPE_FILE.value)
                recipe_dest = Locator.locate(recipe_path, self.__store_list)
                recipe = str.encode(json.dumps({'chunks': idx}))
                self.stores[recipe_dest].upload_file(recipe_path, recipe)
            else:
                raise DuplicateEntryError('small file is already there')
        else:
            try:
                recipe_path = parent_path / (file_name + StoreSuffixes.RECIPE_FILE.value)
                recipe_dest = Locator.locate(recipe_path, self.__store_list)
                self.stores[recipe_dest].download_file(recipe_path)
            except NoEntryError:
                dest_name = Locator.locate(path, self.__store_list)
                self.stores[dest_name].upload_file(path, data)
            else:
                raise DuplicateEntryError('recipe is already there')
        return True

    def download_maybe_chunked(self, path):
        parent_path = path.parent
        file_name = path.name
        recipe_path = parent_path / (file_name + StoreSuffixes.RECIPE_FILE.value)
        dest = Locator.locate(recipe_path, self.__store_list)
        recipe = self.stores[dest].download_file(recipe_path)
        chunks = json.loads(recipe.decode())['chunks']
        data = bytearray()
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for idx in range(chunks):
                chunk_path = parent_path / (file_name + '.{0}'.format(idx) + StoreSuffixes.CHUNK_FILE.value)
                dest = Locator.locate(chunk_path, self.__store_list)
                futures.append(executor.submit(self.stores[dest].download_file, chunk_path))
            for idx in range(chunks):
                data.extend(futures[idx].result())
        return data

    def download_file(self, path: str) -> bytearray:
        path = PurePath(path)
        dest_name = Locator.locate(path, self.__store_list)
        try:
            data = self.stores[dest_name].download_file(path)
        except NoEntryError:
            data = self.download_maybe_chunked(path)

        return data

    def make_directory(self, path: str, directory_name: str) -> bool:
        path = PurePath(path)
        for name, store in self.stores.items():
            store.make_dir(path, directory_name)
        return True

    def __remove(self, path: str) -> bool:
        path = PurePath(path)
        dest = Locator.locate(path, self.__store_list)
        self.stores[dest].remove(path)
        return True

    def __remove_chunked(self, path: str) -> bool:
        path = PurePath(path)
        parent_path = path.parent
        file_name = path.name
        recipe_path = parent_path / (file_name + StoreSuffixes.RECIPE_FILE.value)
        recipe_dest = Locator.locate(recipe_path, self.__store_list)
        recipe = self.stores[recipe_dest].download_file(recipe_path)
        chunks = json.loads(recipe.decode())['chunks']
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for idx in range(chunks):
                chunk_path = parent_path / (file_name + '.{0}'.format(idx) + StoreSuffixes.CHUNK_FILE.value)
                chunk_dest = Locator.locate(chunk_path, self.__store_list)
                futures.append(executor.submit(self.stores[chunk_dest].remove, chunk_path))
        self.stores[recipe_dest].remove(recipe_path)
        return True

    def remove_file(self, path: str) -> bool:
        try:
            return self.__remove(path)
        except NoEntryError:
            return self.__remove_chunked(path)

    def remove_directory(self, path: str) -> bool:
        path = PurePath(path)
        success = True
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for name, store in self.stores.items():
                futures.append(executor.submit(store.remove, path))
            for future in futures:
                try:
                    future.result()

                except BaseStoreException:
                    success = False
        if success is False:
            raise BaseStoreException('rm dir error')
        else:
            return success

    def rename(self, path, new_path):
        data = self.download_file(path)
        self.upload_file(new_path, data)
        self.remove_file(path)
        return True

    def get_store_list(self):
        return self.__store_list[0:]