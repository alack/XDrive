from concurrent.futures import ThreadPoolExecutor
from typing import List
from store import *
from tokenbox import *
from exceptions import *
from pathlib import Path, PurePath
import json
import Locator

class UniDrive:
    __chunking_threshold = 4194304 # 4 * 1024 * 1024 byte
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

    def get_store_list(self):
        return self.__store_list

    def __update_store_list(self):
        with open(self.app_dir/'store_list.json', 'w') as conf:
            conf.write(json.dumps({'stores' : self.__store_list}, indent=4))

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

    def get_list(self, path: str) -> List[DirectoryEntry]:
        path = PurePath(path)
        list_filter = set()
        results = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for name, store in self.stores.items():
                futures.append(executor.submit(store.get_list, path))
            for future in futures:
                for entry in future.result():
                    if entry.name not in list_filter:
                        list_filter.add(entry.name)
                        results.append(entry)
        filtered = [x for x in results if not x.is_chunk and not x.is_recipe]
        return filtered

    def upload_file(self, path: str, data) -> bool:
        path = PurePath(path)
        # need_chunking = (len(data) > self.__chunking_threshold)
        need_chunking = False
        if need_chunking:
            pass
        else:
            dest_name = Locator.map(path, self.__store_list)
            self.stores[dest_name].upload_file(path, data)
        return True

    def download_file(self, path: str) -> bytearray:
        data = None
        path = PurePath(path)
        for name, store in self.stores.items():
            try:
                data = store.download_file(path)
            except NoEntryError:
                pass
            else:
                break
        if data is None:
            raise NoEntryError('data is None')
        else:
            return data

    def make_directory(self, path: str, directory_name: str) -> bool:
        path = PurePath(path)
        for name, store in self.stores.items():
            try:
                store.make_dir(path, directory_name)
            except BaseStoreException:
                return False

        return True

    def __remove(self, path: str) -> bool:
        path = Path(path)
        for name, store in self.stores.items():
            try:
                store.remove(path)
            except BaseStoreException:
                pass
        return True

    def __remove_chunked(self,path) -> bool:
        return False

    def remove_file(self, path: str) -> bool:
        try:
            return self.__remove(path)
        except NoEntryError as e:
            return self.__remove_chunked(path)

    def remove_directory(self, path: str) -> bool:
        return self.__remove(path)

    def rename(self, path, new_path):
        data = self.download_file(path)
        self.upload_file(new_path, data)
        self.remove_file(path)
        return True