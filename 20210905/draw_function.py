import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = (16, 4)


def displayPlot(xlim=[-10, 10], ylim=[-0.1, 1.1], ncol=2):
    legend = plt.legend(loc=1, ncol=ncol, framealpha=0, bbox_to_anchor=(1, -0.1))
    plt.setp(legend.get_texts(), color='0.75', size=12)
    plt.grid(True, alpha=0.25)
    plt.xlim(xlim)
    plt.ylim(ylim)

    plt.legend()
    #plt.show()
    plt.savefig("./result/result.jpg")


def test1():
    v = np.linspace(-10, 10, 1000)
    phi = v
    phi_prime = v * 0 + 1
    plt.plot(v, phi, label='liner')
    plt.plot(v, phi_prime, '--', label='derivada')
    displayPlot(ylim=[-8, 8])

def test2():
    v = np.linspace(-10, 10, 1000)
    B = np.linspace(1, 9, 5)
    for b in B:
        phi = v * b
        plt.plot(v, phi, label='β = {0:.2f}'.format(b))
    displayPlot(ncol=len(B), ylim=[-8, 8])

def test3():
    v = np.linspace(-10, 10, 1000)
    phi = v >= 0
    phi_prime = ~(v != 0)
    plt.plot(v, phi, label='heaviside')
    plt.plot(v, phi_prime, '--', label='derivada')
    displayPlot()


def test4():
    v = np.linspace(-10, 10, 1000)
    phi = 1 / (1 + np.exp(-v))
    phi_prime = phi * (1 - phi)
    plt.plot(v, phi, label='Sigmoid')
    plt.plot(v, phi_prime, '--', label='derivada')
    displayPlot()


def test5():
    v = np.linspace(-10, 10, 1000)
    B = np.linspace(0, 2, 5)
    for b in B:
        phi = 1 / (1 + np.exp(-b * v))
        plt.plot(v, phi, label='β = {0:.2f}'.format(b))
    displayPlot(ncol=len(B))


def test6():
    v = np.linspace(-10, 10, 1000)
    phi = 2 / (1 + np.exp(-2 * v)) - 1
    phi_prime = 1 - phi ** 2
    plt.plot(v, phi, label='tanh')
    plt.plot(v, phi_prime, '--', label='derivada')
    displayPlot(ylim=[-1.1, 1.1])

def test7():
    v = np.linspace(-10, 10, 1000)
    B = np.linspace(0, 2, 5)
    for b in B:
        phi = 2 / (1 + np.exp(-2 * b * v)) - 1
        plt.plot(v, phi, label='β = {0:.2f}'.format(b))
    displayPlot(ncol=len(B), ylim=[-1.1, 1.1])


def test8():
    v = np.linspace(-10, 10, 1000)
    phi = v / (1 + np.abs(v))
    phi_prime = 1 / (1 + np.abs(v)) ** 2
    plt.plot(v, phi, label='softsign')
    plt.plot(v, phi_prime, '--', label='derivada')
    displayPlot(ylim=[-1.1, 1.1])

def test9():
    v = np.linspace(-10, 10, 1000)
    B = np.linspace(0, 2, 5)
    for b in B:
        phi = b * v / (1 + np.abs(b * v))
        plt.plot(v, phi, label='β = {0:.2f}'.format(b))
    displayPlot(ncol=len(B), ylim=[-1.1, 1.1])


def test10():
    v = np.linspace(-10, 10, 1000)
    phi = v * (v >= 0)
    phi_prime = (v >= 0)
    plt.plot(v, phi, label='relu')
    plt.plot(v, phi_prime, '--', label='derivada')
    displayPlot(xlim=[-2, 2], ylim=[-0.1, 1.1])

def test11():
    v = np.linspace(-10, 10, 1000)
    B = np.linspace(0, 2, 5)
    for b in B:
        phi = b * v * (v >= 0)
        plt.plot(v, phi, label='β = {0:.2f}'.format(b))
    displayPlot(ncol=len(B), xlim=[-2, 2], ylim=[-0.1, 1.1])

def test12():
    v = np.linspace(-10, 10, 1000)
    a = 0.2
    phi = np.where(v >= 0, v, a * v)
    phi_prime = np.where(v >= 0, 1, a)
    plt.plot(v, phi, label='PReLU (α = {0})'.format(a))
    plt.plot(v, phi_prime, '--', label='derivada')
    displayPlot(xlim=[-2, 2], ylim=[-0.6, 1.1])

def test13():
    v = np.linspace(-10, 10, 1000)
    A = np.linspace(0, 2, 5)
    for a in A:
        phi = np.where(v >= 0, v, a * v)
        plt.plot(v, phi, label='α = {0:.2f}'.format(a))
    displayPlot(ncol=len(A), xlim=[-2, 2], ylim=[-1.1, 1.1])

def test14():
    v = np.linspace(-10, 10, 1000)
    a = 1
    phi = np.where(v >= 0, v, a * (np.exp(v) - 1))
    phi_prime = np.where(v >= 0, 1, phi + a)
    plt.plot(v, phi, label='ELU (α = {0})'.format(a))
    plt.plot(v, phi_prime, '--', label='derivada')
    displayPlot(xlim=[-2, 2], ylim=[-1.1, 1.1])

def test15():
    v = np.linspace(-10, 10, 1000)
    A = np.linspace(0, 2, 5)
    for a in A:
        phi = np.where(v >= 0, v, a * (np.exp(v) - 1))
        plt.plot(v, phi, label='α = {0:.2f}'.format(a))
    displayPlot(ncol=len(A), xlim=[-2, 2], ylim=[-1.1, 1.1])

def test16():
    v = np.linspace(-10, 10, 1000)
    phi = np.log(1 + np.exp(v))
    phi_prime = 1 / (1 + np.exp(-v))
    plt.plot(v, phi, label='SoftPlus')
    plt.plot(v, phi_prime, '--', label='derivada')
    displayPlot(ylim=[-0.1, 2])

def test17():
    v = np.linspace(-10, 10, 1000)
    B = np.linspace(0, 2, 5)
    for b in B:
        phi = np.log(1 + np.exp(b * v))
        plt.plot(v, phi, label='β = {0:.2f}'.format(b))
    displayPlot(ncol=len(B), ylim=[-0.1, 2])

if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    test11()
    test12()
    test13()
    test14()
    test15()
    test16()
    test17()