import random
from asyncio import sleep
from datetime import timedelta, datetime

from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions

from misc import app


@app.on_message(filters.command(["ban_me_please", "do_not_click"], case_sensitive=True) & filters.chat("yaslovoblud"))
async def ban_me_please(cl: Client, m: Message):
    if not m.from_user:
        return
    num = random.randint(1, 60)
    await cl.restrict_chat_member(m.chat.id, m.from_user.id, ChatPermissions(),
                                  datetime.now() + timedelta(minutes=num))
    m2 = await m.reply(f"Помовчи трохи, а саме {num}хв")
    await sleep(20)
    await rand_delete([m, m2], [0.6, 0.2])


@app.on_message(filters.command("unban_me_please", prefixes='!'))
async def unban_me_please(cl: Client, m: Message):
    user = m.from_user
    if m.reply_to_message:
        user = m.reply_to_message.from_user
    await cl.restrict_chat_member(m.chat.id, user.id, m.chat.permissions)
    m2 = await m.reply(f"Страшно впасти у кайдани, Умирать в неволі, \nА ще гірше – спати, спати, І спати на волі…")
    await sleep(20)
    await rand_delete([m, m2], [0.8, 0.8])
