import numpy as np
import pyaudio
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from Waves.BaseWaves import BaseWave

fig, ax = plt.subplots()
plt.gca().set_ylim(np.iinfo(np.int16).min, np.iinfo(np.int16).max)

def Plot(*args):
    for arg in args:
        l, =plt.plot(arg[:CHUNK])
        axis=plt.axes([0.25, 0.15, 0.65, 0.03])
        slider=Slider(axis, 'Freq', 300.0, 800.0, valinit=440.0, valstep=10.0)
        slider.on_changed()
        l.set_ydata(amp * np.sin(2 * np.pi * freq * t))
        fig.canvas.draw_idle()


CHUNK = 1024
FORMAT = pyaudio.paInt16
# CHANNELS = 2
SAMPLINGRATE = 44100


def AdaptDimensiontoChannel(input, numChannel):
    # if data is not an array, turn into one
    try:
        iter(input)
    except:
        input = [input]
    # enforce numpy arrays
    input = np.asarray(input)

    print("len={}, ndim={}, shape={}".format(len(input), input.ndim, input.shape))
    metric = len(input) if input.ndim == 1 else input.shape[1]
    # if format is already amtching, do nothing
    if metric == numChannel:
        out = input
    # if input has more data than channels require, truncate
    elif metric > numChannel:
        out = np.delete(input, metric - numChannel - 1, axis=input.ndim - 1)
    # if input is missing data, expend by column stacking
    elif metric < numChannel:
        tmp = tuple(input for _ in range(numChannel))
        out = np.column_stack(tmp)
    # sqeeze useless dimensions
    if out.shape[0] == 1: out = np.squeeze(out, axis=0)
    return out



duration_s = 1.0
freq_hz = np.array([100.0, 150.0])
samplingRate_hz = 44100
volume = 0.3

time = np.arange(duration_s * samplingRate_hz).reshape(-1, 1)
w = BaseWave(time)

sine = w.SineWave()
square = w.SquareWave()
tooth = w.SawtoothWave()
triangle = w.TriangleWave()

# Plot(sine, square, tooth, triangle)
Plot(sine)
plt.show()

# p = pyaudio.PyAudio()
# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=SAMPLINGRATE,
#                 output=True)
# stream.write(y1)
# stream.write(y2)
# stream.write(y3)
# stream.write(y4)
# stream.close()
# p.terminate()
