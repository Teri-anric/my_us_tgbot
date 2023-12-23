import math
import string
from typing import Any, Mapping, Sequence

from pyrogram import Client
from pyrogram.types import Message

from misc import register_cmd, smart_edit_text


class EvalFormatter(string.Formatter):
    def get_field(self, field_name: str, args: Sequence[Any], kwargs: Mapping[str, Any]) -> Any:
        try:
            return super().get_field(field_name, args, kwargs)
        except KeyError:
            code = 'f"{' + field_name.replace('"', '\\"') + '}"'
            return eval(code, {}, kwargs), None


f = EvalFormatter()


@register_cmd("f", "а", "ф")
def cmd_eval(cl: Client, msg: Message):
    f""" auto format text
    """
    _, text = msg.text.split(maxsplit=1)
    try:
        text = f.format(text, msg=msg, math=math, cl=cl)
    except Exception as e:
        text += f"\n{e}"
    smart_edit_text(m, text)
