import re
from contextlib import suppress

from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.filters import create

from misc import app, register_cmd, smart_edit_text
from tts import TTSWorker


url_regex = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

tts: TTSWorker = TTSWorker()
speaking_chat_ids = []

def validate_text(text: str):
    text = re.sub(url_regex, "силка", text)
    return text


def messsage_to_text(message: Message, include_chat: bool = False, include_user: bool = True, include_reply: bool = True):
    # Озвучуємо отримане повідомлення
    m = ""
    if message.chat and include_chat:
        if message.chat.id != message.from_user.id:
            m += "чат "
            m += message.chat.title
            m += "\n"
    # юзер
    if message.from_user and include_user:
        m += message.from_user.first_name or "підкідеш"
        m += "\n"
    # reply
    if message.reply_to_message and include_reply:
        m += "відповідає на"
        m += message.reply_to_message.from_user.first_name or "підкідеш"
        #msg += messsage_to_text(message.reply_to_message, False, False, False)
        m += "\n"
    # type message
    if message.text:
        m += validate_text(message.text)
    if message.sticker:
        m += "Наліпка"
    if message.animation:
        m += "GIF"
    if message.photo or message.video:
        m += "фото" if message.photo else "ХЕНТАЙ"
        m += "\n"
        if message.caption:
            m += message.caption
            m += "\n"
    if message.voice:
        m += "Голосочок"
    if message.voice:
        m += "Файлик"
    return m


@register_cmd("speak")
async def speak_cmd(cl: Client, m: Message):
    """ Speak a message on/off
    arg:
        on - start speak all message
        off - stop speak
        add - add chat to speaking
        remove - remove chat to speaking
    """
    global tts
    _, *args = m.text.split(maxsplit=1)
    if "add" in args:
        speaking_chat_ids.append(m.chat.id)
        return await smart_edit_text(m, "chat add to speaking")
    if "remove" in args:
        with suppress(ValueError):
            speaking_chat_ids.remove(m.chat.id)
        return await smart_edit_text(m, "chat remove from speaking")
    if tts.running:
        tts.close()
    if "off" in args:
        return await smart_edit_text(m, "speak is stopped")
    tts = TTSWorker()
    tts.start()
    await smart_edit_text(m, "speak is started")

active_tts_filter = create(lambda _, __, m: tts.running, "active_tts_filter")
speaking_chat_filter = create(lambda _, __, m: m.chat.id in speaking_chat_ids, "speaking_chat_filter")

@app.on_message(active_tts_filter & (speaking_chat_filter | filters.private) & ~filters.me)
async def handle_message(client: Client, message: Message):
    tts.add_message(messsage_to_text(message).lower())
