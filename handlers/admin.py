from asyncio import sleep
from datetime import datetime

from pyrogram import Client
from pyrogram.types import Message, ChatPermissions

from misc import register_cmd, smart_edit_text
from utils import export_link, extract_time_args


@register_cmd("ban")
async def ban_user(cl: Client, m: Message):
    """ ban user from chat """
    if m.reply_to_message and m.reply_to_message.from_user:
        try:
            await m.chat.ban_member(m.reply_to_message.from_user.id)
            await smart_edit_text(m, "Бан, бан, БАН!")
            return
        except:
            pass
    await smart_edit_text(m, "бан? :(")


@register_cmd("unban")
async def unban_user(cl: Client, m: Message):
    """ remote user from ban list
    and send unban message
    args:
        w - add to member chat
    """
    cmd, *args = m.text.lower().split()
    if m.reply_to_message and m.reply_to_message.from_user:
        try:
            await m.chat.unban_member(m.reply_to_message.from_user.id)
            if 'w' in args:
                try:
                    await m.chat.add_members(m.reply_to_message.from_user.id)
                except:
                    pass
                return await smart_edit_text(m, "Вас було розбанено, подякуєш бан)")
            await smart_edit_text(m, "Живий?")
            await cl.send_message(m.reply_to_message.from_user.id,
                                  f"Вас було розбанено в товаристві: {m.chat.title}\n"
                                  f"посилання {await export_link(m.chat)}")
        except:
            pass
    await smart_edit_text(m, "Помер? :(")


@register_cmd("ro")
async def ro_user(cl: Client, m: Message):
    """ read only
    int and suffix parrse to time
    not suffix default minutes
    default time 1 hour
    suffix:
        d - days
        s - seconds
        m - minutes
        h - hours
        w - weeks
    """
    cmd, *args = m.text.split()
    if m.reply_to_message and m.reply_to_message.from_user:
        try:
            await cl.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, ChatPermissions(),
                                          datetime.now() + extract_time_args(args))
            await smart_edit_text(m, "Тихо, тихо, спрокійно все буде добре.")
            return
        except Exception as e:
            print(e)
    await smart_edit_text(m, "Стули пельку вже :(")


@register_cmd("unmute")
async def unmute_user(cl: Client, m: Message):
    """ set default premmision """
    user = m.from_user
    if m.reply_to_message:
        user = m.reply_to_message.from_user
    await cl.restrict_chat_member(m.chat.id, user.id, m.chat.permissions)
    m2 = await m.reply(f"Страшно впасти у кайдани, Умирать в неволі, \nА ще гірше – спати, спати, І спати на волі…")
    await sleep(20)
    await rand_delete([m, m2], [0.8, 0.8])


@register_cmd("slowmode")
async def slowmode(cl: Client, m: Message):
    """ set slowmode in chat
    default time 30 sec.
    Valid values are: 0 or None (off), 10, 30, 60 (1m), 300 (5m), 900 (15m) or 3600 (1h).
    """
    cmd, *args = m.text.split()
    try:
        time = 30 if not args else int(args[0])
        await cl.set_slow_mode(m.chat.id, time)
        await smart_edit_text(m, f"Слов мод {time}сек")
        return
    except Exception as e:
        print(e)
    await smart_edit_text(m, "Тишина!")
