import time
import matplotlib
import matplotlib.pyplot as plt
import numpy
from gripper import Gripper
from traj import Traj
from tqdm import tqdm
from tactile import Tactile
from simple_pid import PID
from filter import LPFilter
from filter import SlicedController
from matplotlib import rc

matplotlib.use('Qt5Agg')
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)


def main():
    T = 10.0
    d = 1.0 / 100.0

    base_sensor = 100
    g = Gripper(0.05, False)
    traj = Traj()
    traj.init(0.05)
    traj.set_goal(0.045, 1.5)
    sensor = Tactile(base_sensor)
    f = LPFilter(3, 0.03)
    sc = SlicedController(0.085, 0.4 * 0.001)

    scd = []
    gd = []
    sd = []
    td = []
    spd = []
    trd = []
    t = 0.0

    pid = PID(Kp = 0.00005,
              Kd = 0.0,
              Ki = 0.0000,
              sample_time = 0.03,
              setpoint = -10.0)
    setpoint = 110
    pid.setpoint = setpoint
    dd = 0.05
    for i in range(100):
        f.filter(base_sensor)
        sc.update(dd)

    for i in range(int(T / d)):

        x = g.get_output()
        s = sensor.get_output(x)

        # print(i)
        if (i % 3) == 0:
            sf = f.filter(s)
            # sf = s
            dd -= (pid(sf) * 0.03)
            sdd = sc.update(dd)
            scd.append(sdd)
            # dd -= 0.00005 * (setpoint - sf) * 0.03

            if dd > 0.085:
                dd = 0.085
            if dd < 0:
                dd = 0.0

            g.set_setpoint(dd)
            # g.set_setpoint(sdd)

            spd.append(setpoint)
            gd.append(x)
            sd.append(sf)
            trd.append(dd)
            td.append(t)
            # t += d
            t += 0.03

        g.step()

        # time.sleep(0.1)

    fig, ax = plt.subplots(2)
    i0 = 0
    i1 = int(T / 0.03)
    # i0 = 0
    # i1 = int(2.0 / 0.03)
    ax[0].plot(numpy.array(td[i0:i1]), numpy.array(gd[i0:i1]), label = '$\mathrm{gripper}$')
    ax[0].plot(numpy.array(td[i0:i1]), numpy.array(trd[i0:i1]), label = '$\mathrm{desired}$')
    # ax[0].plot(numpy.array(td[i0:i1]), numpy.array(scd[i0:i1]), label = '$\mathrm{?x}$')
    ax[0].legend(fontsize = 15)
    ax[0].yaxis.set_tick_params(labelsize = 15)
    ax[0].xaxis.set_tick_params(bottom = False, labelbottom = False)
    ax[0].grid()

    ax[1].plot(numpy.array(td[i0:i1]), numpy.array(sd[i0:i1]), label = '$\mathrm{sensor}$')
    ax[1].plot(numpy.array(td[i0:i1]), numpy.array(spd[i0:i1]), label = '$\mathrm{desired}$')
    ax[1].legend(loc = 'upper left', fontsize = 15)
    ax[1].yaxis.set_tick_params(labelsize = 15)
    ax[1].xaxis.set_tick_params(labelsize = 15)
    ax[1].ticklabel_format(useOffset=False)
    ax[1].set_xlabel('$\mathrm{time(s)}$', fontsize = 15)
    ax[1].grid()

    # plt.yticks(fontsize = 16)
    plt.show()


if __name__ == '__main__':
    main()
