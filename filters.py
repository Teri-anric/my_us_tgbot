from pyrogram.filters import Filter
from pyrogram import Client
from pyrogram.types import Message
from config import setting
from typing import List


class AccessFilter(Filter):
    def __init__(self, cmds: List[str]):
        self.cmds = cmds

    def __call__(self, cl: Client, m: Message):
        access_map: dict = setting.get("access_map", {})
        for ident in [m.from_user.id, m.chat.id]:
            access = access_map.get(str(ident), None)
            if self.check_access(access):
                return True
        return False

    def check_access(self, access=None):
        if access is None:
            return False
        if access == "full":
            return True
        if isinstance(access, list):
            for cmd in self.cmds:
                if cmd in access:
                    return True
        return False

