import random
from asyncio import sleep
from datetime import timedelta, datetime

from pyrogram import Client
from pyrogram.types import Message, ChatPermissions

from misc import register_cmd


@register_cmd("ban_me_please", "do_not_click", prefixes=["!", "/"], on_group="yaslovoblud", public=True)
async def ban_me_please(cl: Client, m: Message):
    """ fan read only for @yaslovoblud chat """
    if not m.from_user:
        return
    num = random.randint(1, 20)
    await cl.restrict_chat_member(m.chat.id, m.from_user.id, ChatPermissions(),
                                  datetime.now() + timedelta(minutes=num))
    m2 = await m.reply(f"Помовчи трохи, а саме {num}хв")
    await sleep(20)
    await rand_delete([m, m2], [0.6, 0.2])
