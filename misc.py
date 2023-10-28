from typing import Optional, Union, List

from pyrogram import Client, filters

from config import API_ID, API_HASH, CLIENT_NAME

# from tts import STTWorker

app = Client(CLIENT_NAME, api_id=API_ID, api_hash=API_HASH,
             app_version="Terigram 0.0.1", device_model="UB")


# stt = STTWorker()

def register_cmd(*commands: str, prefixes: Union[str, List[str]] = '!', on_group: Union[bool, None, str] = None,
                 public: bool = False):
    f = filters.command(prefixes=prefixes, commands=list(commands))
    if not public:
        f &= filters.me
    if on_group is not None:
        if isinstance(on_group, str):
            f &= filters.chat(on_group)
        elif on_group:
            f &= filters.group
        else:
            f &= ~filters.group
    return app.on_message(filters=f)
