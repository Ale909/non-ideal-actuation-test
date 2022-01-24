import copy
import numpy

class Gripper():

    def __init__(self, start, ideal):

        self.ideal = ideal

        self.mmax = 0.085
        self.mmin = 0.0
        self.res = 0.4 * 0.001
        self.rise_time = 0.04
        self.rise_v = (0.4 * 0.001) / self.rise_time

        start = self.mmax - self.get_slice(start) * self.res
        self.setpoint = start
        self.current = start
        self.output = start

        self.update_time = 10 # 100 Hz
        self.sample_time = 30 # 30 Hz
        self.time = 0

        self.current_slice = self.get_slice(start)
        self.switching = False
        self.switching_time = 0.3
        self.switching_time_count = 0.0


    def get_slice(self, value):
        slice = int((self.mmax - value) / self.res)

        return slice


    def get_output(self):

        return self.output


    def set_setpoint(self, setpoint):

        self.setpoint = setpoint


    def step(self):

        if self.ideal:
            self.output = copy.copy(self.setpoint)
        else:
            self.time += self.update_time

            if self.time >= self.sample_time:
                self.time = 0.0
                new_slice = self.get_slice(copy.copy(self.setpoint))

                if self.switching == True:
                    self.switching_time_count += 0.03
                    if self.switching_time_count > self.switching_time:
                        self.switching = False
                        self.current_slice = self.target_slice
                        self.switching_time_count = 0.0
                elif new_slice != self.current_slice:
                    self.target_slice = self.get_slice(copy.copy(self.setpoint))
                    self.switching_time = numpy.random.uniform(0.1, 0.25)
                    self.switching = True

                self.output = self.mmax - self.current_slice * self.res


            #############################################

            # self.output = self.mmax - self.get_slice(copy.copy(self.setpoint)) * self.res
            # self.time += self.update_time

            #############################################

            # if self.time >= self.sample_time:
            #     self.output = self.get_slice(self.setpoint) * self.res
            #     self.time = 0

            # self.time += self.update_time

            # current_slice = self.get_slice(self.current)
            # setpoint_slice = self.get_slice(self.setpoint)

            # # if current_slice != setpoint_slice and abs(current_slice * self.res - self.current) > 0.00001:
            # if current_slice != setpoint_slice:

            #     sign = 1
            #     if (setpoint_slice - current_slice) < 0:
            #         sign = -1

            #     self.current += self.rise_v * sign * (1.0 / 100.0)

            # if self.current <= self.mmin:
            #     self.current = 0
            # if self.current >= self.mmax:
            #     self.current = self.mmax

            # if self.time >= self.sample_time:
            #     self.time = 0
            #     self.output = self.current
