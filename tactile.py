import numpy

class Tactile():

    def __init__(self, base):

        self.x0 = 0.05
        self.base = base


    def get_output(self, position):

        output = None

        if (position - self.x0) < 0.0:
            output = self.base + 40000.0 * abs(position - self.x0)
        else:
            output = self.base

        output += numpy.random.normal(scale = 1.0)

        return output
