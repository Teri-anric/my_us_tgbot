from pyrogram import filters, Client
from pyrogram.types import Message

from misc import app, stt


@app.on_message((filters.chat("yaslovoblud") | filters.private) & (~filters.me))
async def handle_message(client: Client, message: Message):
    # Озвучуємо отримане повідомлення
    m = ""
    # юзер
    if message.from_user:
        m += message.from_user.first_name or "підкідеш"
        m += "\n"
    # reply
    if message.reply_to_message and message.reply_to_message.text:
        m += "відповідає на "
        m += message.reply_to_message.text
        m += "\n"
    # type message
    if message.text:
        m += message.text
    elif message.photo or message.video:
        m += "фото" if message.photo else "ХЕНТАЙ!!!"
        m += "\n"
        if message.caption:
            m += message.caption
            m += "\n"
    elif message.voice:
        temp_path = stt.get_temp_path()
        await client.download_media(message.voice.file_id, file_name=temp_path)
        stt.add_message(m)
        stt.add_audio(temp_path)
        return
    stt.add_message(m)
