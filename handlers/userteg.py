import html

from pyrogram import Client
from pyrogram.enums import ParseMode, ChatMembersFilter
from pyrogram.types import Message

from misc import register_cmd
from utils import rand_emoji


async def teg_users(cl: Client, m: Message, mention_func=None, filter=ChatMembersFilter.SEARCH):
    args = m.text.split(maxsplit=1)
    text = ""
    if len(args) == 2:
        text = html.escape(args[-1])
    users = []
    async for member in m.chat.get_members(limit=100, filter=filter):
        if not member.user:
            continue
        if member.user.is_deleted:
            continue
        if member.user.is_bot and not filter == ChatMembersFilter.BOTS:
            continue
        users.append(member.user)
    # generate text
    for user in users:
        if mention_func is None:
            mention_text = None
            text += "\n"
        else:
            mention_text = mention_func(user)
        text += user.mention(mention_text, style=ParseMode.HTML)
    if not text:
        return
    await cl.send_message(m.chat.id, text=text, reply_to_message_id=m.reply_to_message_id,
                          parse_mode=ParseMode.HTML)


@register_cmd("all", on_group=True)
async def teg_first_100_users(cl: Client, m: Message):
    """ teg all user from chat """
    await teg_users(cl, m, mention_func=lambda chat: rand_emoji() + "\n")

@register_cmd("tegadmin", on_group=True)
async def teg_admins(cl: Client, m: Message):
    """ teg all admin from chat """
    await teg_users(cl, m, filter=ChatMembersFilter.ADMINISTRATORS)

@register_cmd("tegbot", on_group=True)
async def teg_admins(cl: Client, m: Message):
    """ teg all bot from chat """
    await teg_users(cl, m, filter=ChatMembersFilter.BOTS)

@register_cmd("tegban", on_group=True)
async def teg_admins(cl: Client, m: Message):
    """ teg banned user from chat """
    await teg_users(cl, m, filter=ChatMembersFilter.BANNED)
