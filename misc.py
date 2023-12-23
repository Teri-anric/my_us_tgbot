from typing import Optional, Union, List, Callable

from pyrogram import Client, filters, types

from config import API_ID, API_HASH, CLIENT_NAME

app = Client(CLIENT_NAME, api_id=API_ID, api_hash=API_HASH,
             app_version="Terigram 0.0.1", device_model="UB")

from control import register_cmd