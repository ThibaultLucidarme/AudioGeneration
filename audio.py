# from . import AudioStream
from contextlib import contextmanager

import pyaudio
from matplotlib import pyplot as plt

from Waves.BaseWaves import *
from fft import *


@contextmanager
def AudioStream(*args, **kwargs):
    p = pyaudio.PyAudio()
    stream = p.open(*args, **kwargs)
    try:
        yield stream
    finally:
        stream.close()
        p.terminate()


SIGNAL = dict(
    chunk=1024,
    format=pyaudio.paInt16,
    channels=1,
    rate=44100
)

duration_s = 1.0
freq_hz = 100.0
samplingRate_hz = 44100
volume = 0.3
max_peaks = 5

time_s = np.arange(duration_s * samplingRate_hz)
signal = SquareWave(440.0)(time_s) + SineWave(600.0)(time_s)
fourier = FourierAnalysis(signal, SIGNAL['rate'])

freq_hz, amplitude = fourier.fft()
harmonics_hz, harmonic_amplitude = fourier.dft()
# plt.plot(freq_hz, amplitude, 'r')
# plt.plot(harmonics_hz[:max_peaks], harmonic_amplitude[:max_peaks],'bx')


ifourier = InverseFourierAnalysis(freq_hz)
y_ifft_reconstructed = ifourier.ifft(amplitude)
y_idft_reconstructed = ifourier.idft(harmonics_hz, harmonic_amplitude)




# with AudioStream(format=SIGNAL['format'],
#                  channels=SIGNAL['channels'],
#                  rate=SIGNAL['rate'],
#                  output=True) as stream:
#     waveforms = [baseSignal.into(classname) for classname in (SineWave, SquareWave, TriangleWave, SawtoothWave)]
#     for wave in waveforms:
#         stream.write(wave(time_s))
#         gui.Plot(wave(time_s))

plt.show()
