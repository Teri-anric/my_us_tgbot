import html

from pyrogram import filters, Client
from pyrogram.enums import ParseMode, ChatMembersFilter
from pyrogram.types import Message, Chat

from misc import app
from utils import rand_emoji


async def teg_users(cl: Client, m: Message, mention_func=None, filter=ChatMembersFilter.SEARCH):
    args = m.text.split(maxsplit=1)
    text = ""
    if len(args) == 2:
        text = html.escape(args[-1])
        text += "\n"
    users = []
    async for member in m.chat.get_members(limit=100, filter=filter):
        if not member.user:
            continue
        if member.user.is_deleted:
            continue
        if not (member.user.is_bot and filter == ChatMembersFilter.BOTS):
            continue
        users.append(member.user)
    # generate text
    for user in users:
        if mention_func is None:
            mention_text = None
        else:
            mention_text = mention_func(user)
        text += user.mention(mention_text, style=ParseMode.HTML)
    if not text:
        return
    await cl.send_message(m.chat.id, text=text, reply_to_message_id=m.reply_to_message_id,
                          parse_mode=ParseMode.HTML)


@app.on_message(filters.command(["all"], prefixes='!', case_sensitive=True) & filters.me & filters.group)
async def teg_first_100_users(cl: Client, m: Message):
    func = lambda chat: rand_emoji()
    await teg_users(cl, m, func)

@app.on_message(filters.command(["tegadmin"], prefixes='!', case_sensitive=True) & filters.me & filters.group)
async def teg_admins(cl: Client, m: Message):
    await teg_users(cl, m, mention_func=None, filter=ChatMembersFilter.ADMINISTRATORS)

@app.on_message(filters.command(["tegbot"], prefixes='!', case_sensitive=True) & filters.me & filters.group)
async def teg_admins(cl: Client, m: Message):
    await teg_users(cl, m, mention_func=None, filter=ChatMembersFilter.BOTS)

@app.on_message(filters.command(["tegban"], prefixes='!', case_sensitive=True) & filters.me & filters.group)
async def teg_admins(cl: Client, m: Message):
    await teg_users(cl, m, mention_func=None, filter=ChatMembersFilter.BANNED)
