import io
import random
from functools import partial
from traceback import print_exc

from pyrogram import filters, Client
from pyrogram.types import Message

from misc import app
from utils import extract_code


@app.on_message(filters.command(["ev"], prefixes='!', case_sensitive=True) & filters.me)
async def cmd_eval(cl: Client, m: Message):
    cmd, *args = m.text.split(maxsplit=1)
    code = None
    if m.reply_to_message:
        code = m.reply_to_message.text
    if args:
        code = args[0]
    if not code:
        return
    try:
        result = eval(code, globals(), locals())
        await m.edit(str(result))
    except Exception as e:
        await m.edit(f"Error: {e}")


@app.on_message(filters.command(["ex"], prefixes='!', case_sensitive=True) & filters.me)
async def cmd_exec(cl: Client, m: Message):
    msg = m.reply_to_message if m.reply_to_message else m
    code = extract_code(msg)
    if not code:
        _, code = m.text.split(maxsplit=1)
        if m.reply_to_message:
            code = msg.text
    buf = io.StringIO()
    change = {
        "print": partial(print, file=buf),
        "input": lambda x=0: str(random.randint(0, 100))
    }
    g = globals()
    g.update(change)
    l = locals()
    try:
        exec(code, g, l)
    except:
        print_exc(file=buf)
    buf.seek(0)
    await m.reply(f"result:\n{buf.read()}")
