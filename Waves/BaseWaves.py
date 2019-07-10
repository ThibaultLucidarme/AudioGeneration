import numpy as np

from Waves import ScaleWave as wave


class BaseWave:

    def __init__(self, frequency=440.0, samplingRate=44100, channels=1):
        self.freq_hz = frequency
        self.rate_hz = samplingRate
        self.channels = channels

        self.offset_s = 1.0 / self.freq_hz  # realign crafted waves

    def center0(self, x):
        '''Assumes x in [0,1] -> scale to [-1,1]'''
        return (x - 0.5) * 2

    def base(self, *args, **kwargs):
        raise NotImplementedError

    # @wave
    def __call__(self, input_s, volume=0.2):
        return self.base(input_s * self.freq_hz / self.rate_hz) * volume

    def into(self, classname):
        if issubclass(classname, BaseWave):
            return classname(self.freq_hz, self.rate_hz, self.channels)


class SineWave(BaseWave):
    def base(self, input_s):
        return np.sin(2 * np.pi * input_s)


class SquareWave(BaseWave):
    def base(self, input_s):
        return self.center0(np.mod(np.ceil(input_s * 2), 2))


class SawtoothWave(BaseWave):
    def base(self, input_s):
        return self.center0(np.mod(input_s, 1))


class TriangleWave(BaseWave):
    def base(self, input_s):
        scaled = np.abs(self.center0(np.mod(input_s, 1)))
        return self.center0(scaled)


if __name__ == "__main__":
    t = np.arange(100)
    sine = SineWave(frequency=440.0, samplingRate=44100)
    print(sine(t))
    square = sine.into(SquareWave)
    print(square(t))
