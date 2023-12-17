from config import TTS_ENABLE

from . import runtime_modules
from . import admin
from . import execute
from . import fan_ro
if TTS_ENABLE:
    from . import speak
from . import auto_format
from . import userteg
