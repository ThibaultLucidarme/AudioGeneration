import numpy as np


def ScaleWave(func):
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs) * np.iinfo(np.int16).max
        return output.astype(np.int16)
    return wrapper
