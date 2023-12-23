import random
from datetime import timedelta
from typing import List, Union

from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, Chat, MessageEntity
from pyrogram import emoji


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
        params = default_param
    return timedelta(**params)


key_emojis = [k for k in emoji.__dict__ if not k.startswith("_")]
def rand_emoji():
    key = random.choice(key_emojis)
    return getattr(emoji, key)

def extract_text_entity(text: str, entity: MessageEntity):
    return text[entity.offset:entity.offset+entity.length]


def extract_code(msg: Message):
    if not msg.entities:
        return None
    return "\n\n".join(
        map(lambda ent: extract_text_entity(msg.text, ent),
            filter(
                lambda ent: ent.type in (MessageEntityType.CODE, MessageEntityType.PRE),
                msg.entities
                )
            )
        )
