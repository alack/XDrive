from . google_drive_store import GoogleDriveStore
from . dropbox_store import DropboxStore


class StoreFactory:
    store_types = {
        'GoogleDriveStore': GoogleDriveStore,
        'DropboxStore': DropboxStore
    }

    @classmethod
    def create_store(cls, store_type, config, name, tokenbox):
        return cls.store_types[store_type](config, name, tokenbox)