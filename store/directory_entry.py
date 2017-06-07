from pathlib import PurePath
from store.enums import StoreSuffixes


# TODO class for directory, file and chunk
class DirectoryEntry:
    def __init__(self, name: str, is_directory=False):
        self.__node_name = name
        self.__is_dir = is_directory
        self.__is_chunk = False
        self.__is_recipe = False
        temp = PurePath(name)
        if temp.suffix == StoreSuffixes.CHUNK_FILE.value:
            self.__is_chunk = True

        if temp.suffix == StoreSuffixes.RECIPE_FILE.value:
            self.__is_recipe = True

    @property
    def name(self):
        return self.__node_name

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
    def is_chunk(self):
        return self.__is_chunk

    @property
    def is_recipe(self):
        return self.__is_recipe
