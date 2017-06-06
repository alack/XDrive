from store import DirectoryEntry
from pathlib import PurePath


class VirtualEntry:
    def __init__(self, dir_entry: DirectoryEntry):
        self.__node_name = dir_entry.name
        self.__is_dir = dir_entry.is_dir
        self.__node_ext = PurePath(dir_entry.name).suffix

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
