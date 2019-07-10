import numpy as np
from scipy.signal import find_peaks

def ManualFourier(x):
    """A vectorized, non-recursive version of the radix-2 Cooley-Tukey FFT
    https://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/

    limitation: size of x must be a power of 2

    """
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    # N_min here is equivalent to the stopping condition above,
    # and should be a power of 2
    N_min = min(N, 32)

    # Perform an O[N^2] DFT on all length-N_min sub-problems at once
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))

    # build-up each level of the recursive calculation all at once
    while X.shape[0] < N:
        X_even = X[:, :int(X.shape[1] / 2)]
        X_odd = X[:, int(X.shape[1] / 2):]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])
    return X.ravel()


class FourierAnalysis:

    def __init__(self, input, rate):
        self.x_hz = np.fft.fftshift(np.fft.fftfreq(input.shape[0], 1 / rate))
        self.y_amp = np.absolute( np.fft.fftshift(np.fft.fft(input)) )/ self.x_hz.shape[0]

    def fft(self):
        '''Todo: multiple dimension (2 channels)'''
        return self.x_hz, self.y_amp

    def dft(self,top_peaks=100):
        '''Todo: multiple dimension (2 channels)'''
        # find local maxima
        peaks_index, _ = find_peaks(self.y_amp)
        harmonics_hz = self.x_hz[peaks_index]
        harmonics_amp = self.y_amp[peaks_index]
        # sort and keep positive frequencies
        peaks_array = np.asarray(list(zip(harmonics_hz, harmonics_amp)), dtype=[('hz', float), ('amp', float)])
        peaks_important = np.sort(peaks_array[np.where(peaks_array['hz'] > 0)], order='amp')[::-1]
        # unpacking
        peaks_coordinates = list(map(list, zip(*peaks_important[:top_peaks])))

        return peaks_coordinates


class InverseFourierAnalysis:

    def __init__(self, x_hz ):
        self.x_s = np.arange(x_hz.shape[0])

    def ifft(self, y_input):
        y_amp = np.fft.ifft(np.fft.fftishift(y_input*self.x_s.shape[0]))
        return self.x_s, y_amp

    def idft(self, x_harmonics, y_input):
        from cmath import exp, pi
        y_amp = np.zeros(self.x_s)
        N = y_input.shape[0]
        for k in range(N):
            y_amp += y_input[k]*exp(-2*pi*1j*x_harmonics[k]*self.x_s/N)
            y_amp += y_input[k]*exp(-2*pi*1j*x_harmonics[k]*self.x_s/N)
        return self.x_s, y_amp
