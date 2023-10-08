import random
from datetime import timedelta
from typing import List, Union

from pyrogram.types import Message, Chat


async def rand_delete(arr_m: List[Message], rand: Union[float, List[float]] = 0.5):
    if isinstance(rand, float):
        rand = [rand for _ in arr_m]
    for m, t in zip(arr_m, rand):
        if random.random() > t:
            await m.delete()


map_time = {
    "d": "days",
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "w": "weeks"
}


async def export_link(chat: Chat) -> str:
    if chat.username:
        link = f"@{chat.username}"
    elif chat.invite_link:
        link = chat.invite_link
    elif chat.linked_chat:
        link = chat.linked_chat
    else:
        link = await chat.export_invite_link()
    return link


def extract_time_args(args, default_type: str = "minutes",  default_param: dict = {"hours": 1}, error_ok: bool = True) -> timedelta:
    params = {}
    for arg in args:
        sufix: str = arg[-1].lower()
        num = arg
        if not sufix.isdecimal():
            num = arg[:-1]
        name = map_time.get(sufix, default_type)
        try:
            params[name] = float(num)
        except Exception as e:
            if not error_ok:
                raise e
            pass
    if not params:
        params = default
    print(args, params)
    return timedelta(**params)
