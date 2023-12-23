import io
import random
from functools import partial
from traceback import print_exc

from pyrogram import Client
from pyrogram.types import Message

from misc import register_cmd, smart_edit_text
from utils import extract_code


def get_code(m: Message):
    cmd, *args = m.text.split("\n", maxsplit=1)
    raw = False
    reply = False
    for arg in cmd.split():
        reply |= (arg == '-r')
        raw |= (arg == '-raw')
    if reply:
        if raw:
            return m.reply_to_message.text
        return extract_code(m.reply_to_message)
    if raw:
        return args[0] if args else None
    return extract_code(m)


@register_cmd("ev")
async def cmd_eval(cl: Client, m: Message):
    """ eval code
    args:
     -r - from reply message
     -raw - not extract block code
    """
    code = get_code(m)
    if not code:
        return await smart_edit_text(m, f"Code is empty")
    try:
        msg = m.reply_to_message if m.reply_to_message else m
        result = eval(code, globals(), locals())
        await smart_edit_text(m, str(result))
    except Exception as e:
        await smart_edit_text(m, f"Error: {e}")


@register_cmd("ex")
async def cmd_exec(cl: Client, m: Message):
    """ execute code
    input - return rand integer from 0 to 100
    print - print to result message

    args:
     -r - from reply message
     -raw - not extract block code
    """
    code = get_code(m)
    if not code:
        return await smart_edit_text(m, f"Code is empty")
    buf = io.StringIO()
    glo = globals().copy()
    glo.update({
        "print": partial(print, file=buf),
        "input": lambda x=0: str(random.randint(0, 100))
    })
    loc = locals()
    try:
        exec(code, glo, loc)
    except:
        print_exc(file=buf)
    buf.seek(0)
    await m.reply(f"result:\n{buf.read()}")
