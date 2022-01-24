import copy

class Traj():

    def __init__(self):

        self.x0 = 0
        self.xf = 0
        self.T = 0.1
        self.t = 0.0


    def step(self):

        self.t += (1.0 / 100.0)


    def init(self, x0):
        self.xf = x0
        self.x0 = x0


    def set_goal(self, goal, duration):

        self.x0 = copy.copy(self.xf)
        self.xf = goal
        self.T = duration


    def get_x(self):

        if self.t >= self.T:
            self.t = self.T

        return self.x0 + (10 * (self.xf - self.x0) / (pow(self.T, 3))) * pow(self.t , 3) \
            - (15 * (self.xf - self.x0) / (pow(self.T, 4))) * pow(self.t , 4) \
            + (6 * (self.xf - self.x0) / (pow(self.T, 5))) * pow(self.t , 5)
