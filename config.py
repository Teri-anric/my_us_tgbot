import json
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

CLIENT_NAME = os.getenv("CLIENT_NAME", "account")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SETTING_PATH = os.getenv("SETTING_PATH", f"{CLIENT_NAME}.json")

class Setting:
    def __init__(self, path: str):
        self.path = path
        self.data = {}

    def get(self, key, default=None):
        return self.get(key, default)

    def update(self, m, **kwargs):
        self.data.update(m, **kwargs)


    def load(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as fp:
            self.data = json.load(fp)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as fp:
            json.dump(self.data, fp, ensure_ascii=False, indent=4)

    def __enter__(self):
        return self.data

    def __exit__(self):
        self.save()


setting = Setting(SETTING_PATH)