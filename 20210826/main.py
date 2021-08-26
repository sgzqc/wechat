import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def test1():
    x = np.linspace(0,2*np.pi,100)
    y = np.cos(x)
    fig = plt.figure()
    plt.plot(x,y)
    plt.grid(ls='--')
    plt.savefig("cos_test1.png")
    plt.show()


def update_points(num):
    point_ani.set_data(x[num], y[num])
    return point_ani,


def test2():
    global point_ani,x,y
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.cos(x)
    fig = plt.figure()
    plt.plot(x, y)
    point_ani, = plt.plot(x[0], y[0], "ro")
    plt.grid(ls="--")
    ani = animation.FuncAnimation(fig, update_points, np.arange(0, 100), interval=100, blit=True)
    ani.save('cos_test2.gif', writer='imagemagick', fps=10)
    plt.show()



def update_points_v2(num):
    if num % 5 == 0:
        point_ani.set_marker("*")
        point_ani.set_markersize(12)
    else:
        point_ani.set_marker("o")
        point_ani.set_markersize(8)
    point_ani.set_data(x[num], y[num])
    text_pt.set_text("x=%.2f, y=%.2f" % (x[num], y[num]))
    return point_ani, text_pt,


def test3():
    global x,y,point_ani,text_pt
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.cos(x)
    fig = plt.figure()
    plt.plot(x, y)
    point_ani, = plt.plot(x[0], y[0], "ro")
    plt.grid(ls="--")
    text_pt = plt.text(4, 0.8, '', fontsize=16)
    ani = animation.FuncAnimation(fig, update_points_v2, np.arange(0, 100), interval=100, blit=True)
    ani.save('cos_test3.gif', writer='imagemagick', fps=10)
    plt.show()


def update_points_v3(num):
    point_ani.set_data(x[num], y[num])
    if num % 5 == 0:
        point_ani.set_marker("*")
        point_ani.set_markersize(12)
    else:
        point_ani.set_marker("o")
        point_ani.set_markersize(8)
    text_pt.set_position((x[num], y[num]))
    text_pt.set_text("x=%.2f, y=%.2f" % (x[num], y[num]))
    return point_ani, text_pt,

def test4():
    global x,y,point_ani,text_pt
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.cos(x)
    fig = plt.figure()
    plt.plot(x, y)
    point_ani, = plt.plot(x[0], y[0], "ro")
    plt.grid(ls="--")
    text_pt = plt.text(4, 0.8, '', fontsize=16)
    ani = animation.FuncAnimation(fig, update_points_v3, np.arange(0, 100), interval=100, blit=True)
    ani.save('cos_test4.gif', writer='imagemagick', fps=10)
    plt.show()


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
