import json
from typing import Dict


class Tokenbox:
    tokenfile = ""
    tokens = None

    def __init__(self, path):
        self.tokenfile = path
        try:
            with open(self.tokenfile, 'r') as infile:
                self.tokens = json.loads(infile.read())
        except Exception:
            self.tokens = dict()

    def file_update(self):
        with open(self.tokenfile, 'w') as outfile:
            outfile.write(json.dumps(self.tokens, indent=4))

    def save(self, name: str, token_dict: Dict):
        self.tokens[name] = token_dict
        self.file_update()

    def load(self, name: str):
        if name not in self.tokens:
            return None
        else:
            return self.tokens[name]

    def forget(self, name: str):
        del self.tokens[name]
        self.file_update()

    def forget_all(self):
        self.tokens = dict()
        self.file_update()
