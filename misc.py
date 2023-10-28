from typing import Optional, Union, List, Callable

from pyrogram import Client, filters, types

from config import API_ID, API_HASH, CLIENT_NAME

# from tts import STTWorker

app = Client(CLIENT_NAME, api_id=API_ID, api_hash=API_HASH,
             app_version="Terigram 0.0.1", device_model="UB")


# stt = STTWorker()
handlers = []
handlers_map = {}
def register_cmd(*commands: str, prefixes: Union[str, List[str]] = '!', on_group: Union[bool, None, str] = None,
                 public: bool = False):
    f = filters.command(prefixes=prefixes, commands=list(commands))
    if not public:
        f &= filters.me
    if on_group is not None:
        if isinstance(on_group, str):
            f &= filters.chat(on_group)
        elif on_group:
            f &= filters.group
        else:
            f &= ~filters.group

    _decorator = app.on_message(filters=f)

    def decorator(func: Callable) -> Callable:
        _prefixes = [prefixes] if isinstance(prefixes, str) else prefixes
        _commands = [f"{pre}{cmd}" for cmd in commands for pre in _prefixes]
        handlers.append((_commands, func, ))
        for command in tuple(_commands) + commands:
            handlers_map[command] = func
        return _decorator(func)

    return decorator

@register_cmd("help")
async def cmd_help(cl: Client, m: types.Message):
    """ help message and info command """
    _, *args = m.text.split(maxsplit=1)
    text = None
    if args:
        func = handlers_map.get(args[0], None)
        text = func.__doc__
        if not func:
            text = "Command not found 🤷‍♂️"
        elif not text:
            text = "Command not info :("
    else:
        text = "Commands list:"
        _text = ""
        for commands, func in handlers:
            if func.__doc__:
                command = ", ".join(commands)
                doc, *_ = func.__doc__.split('\n', maxsplit=1)
                _text += f"\n{command} - {doc}"
        if not _text:
            _text = "\nNot commands info"
        text += _text

    await m.edit(text=text)