import io
import os
from time import sleep
import pygame
from gtts import gTTS
from tempfile import NamedTemporaryFile
from threading import Thread
from queue import Queue


class TTSWorker(Thread):
    _time_out = 0.1

    def __init__(self):
        self._not_stop = False
        self._queue = Queue()
        super().__init__(daemon=True)

    def get_temp_path(self):
        temp_fp = NamedTemporaryFile('x', delete=False, dir="temps")
        temp_fp.close()
        return temp_fp.name

    def add_message(self, text: str):
        tts = gTTS(text=text, lang='uk')
        temp_path = self.get_temp_path()
        tts.save(temp_path)
        self._queue.put(temp_path)

    def add_audio(self, path: str, deleted: bool = False, buf_size: int = 1024):
        if not deleted:
            temp_path = self.get_temp_path()
            with open(path, 'r') as infp:
                with open(temp_path, 'w') as outfp:
                    while not outfp.write(infp.read(buf_size)):
                        pass
        else:
            temp_path = path
        self._queue.put(temp_path)

    def run(self):
        self._not_stop = True
        while self._not_stop:
            temp_path = self._queue.get(block=True)
            try:
                if temp_path is None:
                    continue
                pygame.mixer.init()
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                sleep(self._time_out)
            finally:
                while pygame.mixer.music.get_busy():
                    sleep(self._time_out)
                pygame.mixer.quit()
                os.remove(temp_path)

    def close(self):
        self._not_stop = False
        self._queue.put(None)
        self.join()

    @property
    def running(self):
        return self._not_stop