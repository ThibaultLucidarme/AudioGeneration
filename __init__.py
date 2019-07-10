from contextlib import contextmanager
import pyaudio


@contextmanager
def AudioStream(*args, **kwargs):
    p = pyaudio.PyAudio()
    stream = p.open(*args, **kwargs)
    try:
        yield stream
    finally:
        stream.close()
        p.terminate()
