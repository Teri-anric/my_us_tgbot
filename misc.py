from pyrogram import Client

from config import API_ID, API_HASH, CLIENT_NAME
from tts import STTWorker

app = Client(CLIENT_NAME, api_id=API_ID, api_hash=API_HASH)
stt = STTWorker()

import handlers