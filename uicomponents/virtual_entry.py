from store import DirectoryEntry
from pathlib import PurePath
from typing import List


class VirtualEntry:
    def __init__(self, dir_entry: DirectoryEntry):
        self.__node_name = dir_entry.name
        self.__is_dir = dir_entry.is_dir
        temp = PurePath(dir_entry.name)
        self.__node_ext = temp.suffix
        self.__pure_name = temp.stem

    @property
    def name(self):
        return self.__node_name

    @name.setter
    def name(self, name: str):
        self.__node_name = name

    @property
    def is_dir(self):
        return self.__is_dir

    @is_dir.setter
    def is_dir(self, val: bool):
        if val:
            self.__is_dir = True
        else:
            self.__is_dir = False

    @property
    def ext(self):
        return self.__node_ext

    @ext.setter
    def ext(self, ext: str):
        self.__node_ext = ext

    @property
    def pure_name(self):
        return self.__pure_name

    @pure_name.setter
    def pure_name(self, pure_name: str):
        self.__pure_name = pure_name

    @staticmethod
    def list_to_virtual(list: List[DirectoryEntry]):
        result = []
        for entry in list:
            result.append(VirtualEntry(entry))
        return result
