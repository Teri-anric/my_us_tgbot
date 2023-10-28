import re

from pyrogram import filters, Client
from pyrogram.types import Message

from misc import app, stt

url_regex = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"


def validate_text(text: str):
    text = re.sub(url_regex, "link", text)
    return text


def messsage_to_text(message: Message, include_chat: bool = False, include_reply: bool = True):
    # Озвучуємо отримане повідомлення
    m = ""
    if message.chat and include_chat:
        if message.chat.id != message.from_user.id:
            m += "чат "
            m += message.chat.title
            m += "\n"
    # юзер
    if message.from_user:
        m += message.from_user.first_name or "підкідеш"
        m += "\n"
    # reply
    if message.reply_to_message and include_reply:
        m += "відповідає "
        m += message.reply_to_message.from_user.first_name or "підкідешу"
        m += "\n"
    # type message
    if message.text:
        m += validate_text(message.text)
    if message.sticker:
        m += "Наліпка"
    elif message.photo or message.video:
        m += "фото" if message.photo else "ХЕНТАЙ!!!"
        m += "\n"
        if message.caption:
            m += message.caption
            m += "\n"
    elif message.voice:
        m += "Голосочок"
    return m


@app.on_message((filters.chat("yaslovoblud") | filters.private) & ~(filters.me | filters.bot))
async def handle_message(client: Client, message: Message):
    stt.add_message(messsage_to_text(message))
