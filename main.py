from misc import app
from config import TTS_ENABLE
import handlers


if __name__ == '__main__':
    if TTS_ENABLE:
        from misc import tts
        tts.start()
    app.run()
