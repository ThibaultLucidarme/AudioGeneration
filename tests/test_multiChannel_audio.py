import numpy as np
from numpy import testing as nptest
from multiChannel_audio import AdaptDimensiontoChannel as adaptDim


class TestAdaptDim:

    # expend number into 1d
    # example frequecy = 440.0 Hz into mono channel
    def test_0d_1c(self):
        input = 4
        output = adaptDim(input, 1)
        expected = [4]
        nptest.assert_array_equal(output, expected)

    # expend number into 2d
    # example frequecy = 440.0 Hz into stereo channel
    def test_0d_2c(self):
        input = 4
        output = adaptDim(input, 2)
        expected = [4, 4]
        nptest.assert_array_equal(output, expected)

    # expend arrayed number into 1d
    # example frequecy = [440.0] into mono channel
    def test_1d_1c(self):
        input = np.array([1, 2, 3, 4]).reshape(-1, 1)
        output = adaptDim(input, 1)
        expected = input
        nptest.assert_array_equal(output, expected)

    # expend arrayed number into 2d
    # example frequecy = [440.0] into stereo channel
    def test_1d_2c(self):
        input = np.array([1, 2, 3, 4]).reshape(-1, 1)
        output = adaptDim(input, 2)
        expected = [[1, 1], [2, 2], [3, 3], [4, 4]]
        nptest.assert_array_equal(output, expected)

    # expend arrayed numbers into 2d
    # example frequecy = [440.0 220.0] into stereo channel
    def test_2d_2c(self):
        input = [[1, 1], [2, 2], [3, 3], [4, 4]]
        output = adaptDim(input, 2)
        expected = input
        nptest.assert_array_equal(output, expected)

    # expend arrayed numbers into d
    # example frequecy = [440.0 220.0] into mono channel
    def test_2d_1c(self):
        input = [[1, 1], [2, 2], [3, 3], [4, 4]]
        output = adaptDim(input, 1)
        expected = np.array([1, 2, 3, 4]).reshape(-1, 1)
        nptest.assert_array_equal(output, expected)


if __name__ == '__main__':
    nptest.run_module_suite()
