from scipy import signal
import numpy as np


class LPFilter():

    def __init__(self, cutoff, sampling_time):
        """Initialize class internal parameters and states."""

        self._initialize_filter(cutoff)
        self._sampling_time = sampling_time

        # Reset internal state
        self.reset()


    def _initialize_filter(self, cutoff):
        """Change the cutoff frequency."""

        # Implement G(s) = omega_0 / (s + omega_0)
        omega_0 = 2 * np.pi * cutoff
        self._filter = signal.lti([omega_0], [1, omega_0])


    def reset(self):
        """Reset internal state."""

        self._prev_input = None
        self._prev_state = None


    def filter(self, input_signal):
        """Return the output of the filter given the new value of the input signal."""

        output = None


        if self._prev_input is None:
            output = input_signal
        else:
            _, output, state = self._filter.output([self._prev_input, input_signal], [0, self._sampling_time], X0 = self._prev_state)
            self._prev_state = state[1]
            output = output[1]

        self._prev_input = input_signal

        return output


class SlicedController():


    def __init__(self, max, res):

        self.filter = LPFilter(1, 0.03)
        self.res = res
        self.max = max

    def get_slice(self, value):
        slice = int((self.max - value) / self.res)

        return slice


    def update(self, value):

        slice = self.get_slice(value)
        new_value = self.max - self.res * (slice + 1.0 / 2.0)
        new_value_f = self.filter.filter(new_value)

        return new_value_f
