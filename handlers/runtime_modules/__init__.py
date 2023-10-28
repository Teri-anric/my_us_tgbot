import os
from datetime import datetime
from pathlib import Path
from traceback import format_exc
from shutil import rmtree

from pyrogram import filters, Client
from pyrogram.types import Message

from misc import app, register_cmd
from utils import extract_code


RESTART_CMD = "pm2 restart teri_us_bot"

SELF_MODULE_DIR = Path(__file__).parent
MODULES_DIR = SELF_MODULE_DIR / "modules"
TRACEBACKS_DIR = SELF_MODULE_DIR / "tracebacks"
# dir update
MODULES_DIR.mkdir(exist_ok=True)
rmtree(TRACEBACKS_DIR, True)
TRACEBACKS_DIR.mkdir(exist_ok=True)


def load_modules(name: str):
    modules = __import__("handlers.runtime_modules.modules", globals={"app": app}, fromlist=(f"{name}",))
    return getattr(modules, name, None)


for path in MODULES_DIR.glob('*.py'):
    try:
        load_modules(path.stem)
    except:
        pass

@register_cmd("run")
async def run_cmd(cl: Client, m: Message):
    _, *cmd = m.text.split(maxsplit=1)
    os.system(*cmd)

@register_cmd("restart")
async def restart(cl: Client, m: Message):
    """ restart user bot """
    os.system(RESTART_CMD)

@register_cmd("runtime_list")
async def list_modules(cl: Client, m: Message):
    """ list runtime modules """
    msg = "List modules:"
    for path in MODULES_DIR.glob('*.py'):
        msg += "\n"
        msg += path.stem
    await m.edit_text(msg)

@register_cmd("get_runtime")
async def list_modules(cl: Client, m: Message):
    """ get file runtime module """
    _, *modules = m.text.split(maxsplit=1)
    if not modules:
        return
    path = MODULES_DIR / f"{modules[-1]}.py"
    if not path.exists():
        return await m.edit_text(f'not found module name "{modules[0]}"')
    await m.reply_document(path.open('rb'))


@register_cmd("remove_runtime")
async def remove_module(cl: Client, m: Message):
    """ delete runtime module """
    _, *modules = m.text.split(maxsplit=1)
    if not modules:
        return
    path = MODULES_DIR / f"{modules[-1]}.py"
    if not path.exists():
        return await m.edit_text(f'not found module name "{modules[0]}"')
    path.unlink(True)
    await m.edit_text("delete and restart")
    os.system(RESTART_CMD)

@register_cmd("runtime_tb")
async def tb_module(cl: Client, m: Message):
    """ get full traceback error module """
    _, *tbs = m.text.split(maxsplit=1)
    if not tbs:
        return
    path = TRACEBACKS_DIR / f"{tbs[-1]}.txt"
    if not path.exists():
        return await m.edit_text(f'not found tb name "{tbs[0]}"')
    await m.edit_text(f"tb:{path.open().read()}")

@register_cmd("runtime_tb_list")
async def tb_list_module(cl: Client, m: Message):
    """ list traceback from modules """
    msg = "List traceback:"
    for path in TRACEBACKS_DIR.glob('*.txt'):
        msg += "\n"
        msg += path.stem
    await m.edit_text(msg)

@register_cmd("add_runtime")
async def add_module(cl: Client, m: Message):
    """ add module
    save and run code, auto load code from restart
    args:
        name=<NAME>
    """
    # parse args
    cmd, *args = m.text.split()
    name = datetime.now().strftime("m%y_%m_%d__%H_%M_%S")
    for arg in args:
        if arg.startswith("name="):
            _, name = arg.split('=')
    module_path = str(MODULES_DIR / f"{name}.py")
    # extract code
    msg = m.reply_to_message if m.reply_to_message else m
    if msg.document:
        await m.edit("~download module....")
        await cl.download_media(msg, module_path)
    else:
        code = extract_code(msg)
        if not code:
            code = msg.text
            if not m.reply_to_message:
                _, code = msg.text.split('\n', maxsplit=1)
        with open(module_path, 'w') as fp:
            fp.write(code)
    # run module
    try:
        await m.edit("~run module....")
        module = load_modules(name)
        await m.edit("success add module\n"
                     f"name: {name}\n"
                     f"raw module: {module}")
    except Exception as e:
        tb_name = datetime.now().strftime("m%y_%m_%d__%H_%M_%S")
        with open(TRACEBACKS_DIR / f"{tb_name}.txt", "w") as fp:
            fp.write(format_exc())
        await m.edit("fail add module\n"
                     f"name: {name}\n"
                     f"exc: {e}"
                     f"tb: {tb_name}")

