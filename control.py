from typing import Optional, Union, List, Callable, Tuple, Dict

from pyrogram import Client, filters, types, errors

from config import API_ID, API_HASH, CLIENT_NAME, setting
from tts import TTSWorker
from filters import AccessFilter

from misc import app


# save handlers  (cmds, func)
handlers: List[Tuple[List[str], Callable]] = []
# save index (cmd, index)
handlers_map: Dict[str, int] = {}


async def smart_edit_text(m: types.Message, text):
    if m.from_user.is_self:
        return await m.edit(text)
    r = await m.reply_text(text)
    try:
        await m.delete()
    except errors.RPCError:
        pass
    return r



def register_cmd(*commands: str, prefixes: Union[str, List[str]] = '!', on_group: Union[bool, None, str] = None,
                 public: bool = False):
    # alias
    _prefixes = [prefixes] if isinstance(prefixes, str) else prefixes
    _commands = [f"{pre}{cmd}" for cmd in commands for pre in _prefixes]
    # create filter
    f = filters.command(prefixes=prefixes, commands=list(commands))
    if not public:
        f &= filters.me | AccessFilter(_commands)
    if on_group is not None:
        if isinstance(on_group, str):
            f &= filters.chat(on_group)
        elif on_group:
            f &= filters.group
        else:
            f &= ~filters.group
    # default decorator
    _decorator = app.on_message(filters=f)
    # new decorator
    def decorator(func: Callable) -> Callable:
        # add to handlers list
        handlers.append((_commands, func,))
        # add index to map
        index = len(handlers) - 1
        for command in tuple(_commands) + commands:
            handlers_map[command] = index
        # decorating
        return _decorator(func)

    return decorator

@register_cmd("op")
async def op(cl: Client, m: types.Message):
    """ add access to commands
    flags:
        chat - access to chat
        full - add full access to commands
    args - commands
    """
    _, *args = m.text.split()
    cmds = []
    params = {}
    for arg in args:
        if arg == "-chat":
            params["chat"] = True
        elif arg == "-full":
            params["full"] = True
        else:
            cmds.append(arg)
    ident = m.chat.id
    if not params.get("chat", False):
        if not m.reply_to_message:
            return await m.edit("Not selector")
        ident = m.reply_to_message.from_user.id
    if params.get("full", False):
        cmds = "full"
    with setting as data:
        access_map = data.setdefault("access_map", {})
        access_map[str(ident)] = cmds
    await m.edit("Successfully added access to commands")




@register_cmd("help")
async def cmd_help(cl: Client, m: types.Message):
    """ help message and info command """
    _, *args = m.text.split(maxsplit=1)
    text = None
    if args:
        index = handlers_map.get(args[0], None)
        text = "Command not found 🤷‍♂️"
        if index is not None:
            cmds, func = handlers[index]
            text = " ".join(cmds) + "\n"
            _text = "Command not info :("
            if func.__doc__ is not None:
                _text = func.__doc__
            text += _text
    else:
        text = "Commands list:"
        _text = ""
        _handlers = handlers
        # filter by not self
        if not m.from_user.is_self:
            access = setting.get("access_map", {}).get(str(m.from_user.id), [])
            if access != "full":
                _handlers = []
                for cmd in access:
                    index = handlers_map.get(cmd, None)
                    if index is not None:
                        _handlers.append(handlers[index])
        # generate text
        for commands, func in _handlers:
            if func.__doc__:
                command = ", ".join(commands)
                doc, *_ = func.__doc__.split('\n', maxsplit=1)
                _text += f"\n{command} - {doc}"
        if not _text:
            _text = "\nNot commands info"
        text += _text

    await smart_edit_text(m, text=text)
