from asyncio import sleep
from datetime import datetime

from pyrogram import Client
from pyrogram.types import Message, ChatPermissions

from misc import register_cmd
from utils import export_link, extract_time_args


@register_cmd("ban")
async def ban_user(cl: Client, m: Message):
    if m.reply_to_message and m.reply_to_message.from_user:
        try:
            await m.chat.ban_member(m.reply_to_message.from_user.id)
            await m.edit_text("Бан, бан, БАН!")
            return
        except:
            pass
    await m.edit_text("бан? :(")


@register_cmd("unban")
async def unban_user(cl: Client, m: Message):
    cmd, *args = m.text.lower().split()
    if m.reply_to_message and m.reply_to_message.from_user:
        try:
            await m.chat.unban_member(m.reply_to_message.from_user.id)
            if 'w' in args:
                await m.chat.add_members(m.reply_to_message.from_user.id)
                await m.edit_text("Вас було розбанено, подякуєш бан)")
            else:
                await m.edit_text("Живий?")
                await cl.send_message(m.reply_to_message.from_user.id,
                                      f"Вас було розбанено в товаристві: {m.chat.title}\n"
                                      f"посилання {await export_link(m.chat)}")
            return
        except:
            pass
    await m.edit_text("Помер? :(")


@register_cmd("ro")
async def ro_user(cl: Client, m: Message):
    cmd, *args = m.text.split()
    if m.reply_to_message and m.reply_to_message.from_user:
        try:
            await cl.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, ChatPermissions(),
                                          datetime.now() + extract_time_args(args))
            await m.edit_text("Тихо, тихо, спрокійно все буде добре.")
            return
        except Exception as e:
            print(e)
    await m.edit_text("Стули пельку вже :(")


@register_cmd("unmute")
async def unmute_user(cl: Client, m: Message):
    user = m.from_user
    if m.reply_to_message:
        user = m.reply_to_message.from_user
    await cl.restrict_chat_member(m.chat.id, user.id, m.chat.permissions)
    m2 = await m.reply(f"Страшно впасти у кайдани, Умирать в неволі, \nА ще гірше – спати, спати, І спати на волі…")
    await sleep(20)
    await rand_delete([m, m2], [0.8, 0.8])
