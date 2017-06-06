from pathlib import PurePath
from abc import ABC, abstractclassmethod
from typing import List
from . directory_entry import DirectoryEntry


class Store(ABC):
    authorization_base_url = ""
    token_url = ""
    redirect_url = "https://localhost"
    upload_url = ""
    scope = []
    token = None
    session = None
    client_secret = ""
    client_id = ""
    tokenbox = None
    store_name = ""

    def load_token(self):
        self.token = self.tokenbox.load(self.store_name)

    def save_token(self, token):
        self.token = token
        self.tokenbox.save(self.store_name, self.token)

    def delete_token(self):
        self.tokenbox.forget(self.store_name)

    def authorized(self):
        return self.session.authorized

    def get_authorization_url(self):
        authorization_url, state = self.session.authorization_url(self.authorization_base_url)
        return authorization_url

    def fetch_token(self, redirect_response):
        token = self.session.fetch_token(self.token_url, client_secret=self.client_secret,
                                         authorization_response=redirect_response)
        self.save_token(token)

    @abstractclassmethod
    def get_usage(self):
        pass

    @abstractclassmethod
    def type_name(self) -> str:
        pass

    @abstractclassmethod
    def download_file(self, path: PurePath) -> bytes:
        pass

    @abstractclassmethod
    def upload_file(self, path: PurePath, data: bytes) -> bool:
        pass

    @abstractclassmethod
    def get_list(self, path: PurePath) -> List[DirectoryEntry]:
        pass

    @abstractclassmethod
    def make_dir(self, path: PurePath, name: str) -> bool:
        pass

    @abstractclassmethod
    def remove(self, path: PurePath) -> bool:
        pass

    @abstractclassmethod
    def rename(self, from_path: PurePath, to_path: PurePath) -> bool:
        pass