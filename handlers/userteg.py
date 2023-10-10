import html

from pyrogram import filters, Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from misc import app
from utils import rand_emoji


@app.on_message(filters.command(["all"], prefixes='!', case_sensitive=True) & filters.me & filters.group)
async def ban_me_please(cl: Client, m: Message):
    args = m.text.split(maxsplit=1)
    text = ""
    if len(args) == 2:
        text = html.escape(args[-1])
        text += "\n"
    users = []
    async for member in m.chat.get_members(limit=100):
        if not member.user:
            continue
        if member.user.is_bot or member.user.is_deleted:
            continue
        users.append(member.user)
    # generate text
    for user in users:
        mention_text = rand_emoji()
        link = user.mention
        text += link(mention_text, style=ParseMode.HTML)
    await cl.send_message(m.chat.id, text=text, reply_to_message_id=m.reply_to_message_id,
                          parse_mode=ParseMode.HTML)
