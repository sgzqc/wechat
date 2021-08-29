import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib.animation as manim
from regression__utils import *


class linearRegression_simple(object):
    def __init__(self):
        self._m = 0
        self._b = 0
    @property
    def m(self):
        return self._m
    @property
    def b(self):
        return self._b
    
    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        X_ = X.mean()
        y_ = y.mean()
        num = ((X - X_)*(y - y_)).sum()
        den = ((X - X_)**2).sum()
        self._m = num/den
        self._b = y_ - self._m*X_
    
    def pred(self, x):
        x = np.array(x)
        return self._m*x + self._b


class linearRegression_multiple(object):
    def __init__(self):
        self._m = 0
        self._b = 0
    @property
    def m(self):
        return self._m
    @property
    def b(self):
        return self._b[0]
    def fit(self, X, y):
        X = np.array(X).T
        y = np.array(y).reshape(-1, 1)
        X_ = X.mean(axis = 0)
        y_ = y.mean(axis = 0)
        num = ((X - X_)*(y - y_)).sum(axis = 0)
        den = ((X - X_)**2).sum(axis = 0)
        self._m = num/den
        self._b = y_ - (self._m*X_).sum()
    
    def pred(self, x):
        x = np.array(x).T
        return (self._m*x).sum(axis = 1) + self._b


class linearRegression_GD(object):
    def __init__(self,
                 mo = 0,
                 bo = 0,
                 rate = 0.001):
        self._m = mo
        self._b = bo
        self.rate = rate

    @property
    def m(self):
        return self._m

    @property
    def b(self):
        return self._b

    def fit_step(self, X, y):
        x = np.array(X)
        y = np.array(y)
        n = X.size
        dm = (2/n)*np.sum(-x*(y - (self._m*x + self._b)))
        db = (2/n)*np.sum(-(y - (self._m*x + self._b)))
        self._m -= dm*self.rate
        self._b -= db*self.rate
        
    def pred(self, x):
        x = np.array(x)
        return self._m*x + self._b


def cellPlot(ax, x, y):
    ax.scatter(x, y, 32)
    ax.set_title('Correlation (ρ = {0:.2f})'.format(correlation(x, y)),fontsize=8,y=0.87)
    ax.grid(color = '0.9', linestyle = ':')
    ax.axis([-0.1, 1.1, -0.5, 1.5])


def test_linear_correlation():
    x, yA, yB, yC, yD = synthData1()
    fig, [[axA, axB], [axC, axD]] = plt.subplots(2, 2)
    cellPlot(axA, x, yA)
    cellPlot(axB, x, yB)
    cellPlot(axC, x, yC)
    cellPlot(axD, x, yD)
    fig.savefig('output/regression_linear_correlation.png', tight_layout=True)
    plt.show()


def cellPlot_v1(ax, x, y, lrs):
    ax.scatter(x, y, 32, label='data')
    ax.plot([x, x], [y, lrs.pred(x)], ':')
    ax.plot(0, 0, ':', alpha=0.5, label='error')
    ax.plot([-5, 5], lrs.pred([-5, 5]), color='red', label='regression')
    ax.set_title('ρ = {0:.2f}, m = {1:.2f}, b = {2:.2f}'.
                 format(correlation(x, y), lrs.m, lrs.b),fontsize=8,y=0.95)
    ax.grid(color='0.9', linestyle=':')
    ax.axis([-0.1, 1.1, -0.5, 1.5])
    ax.legend()


def cellPlot_mse(ax, x, y, lrs):
    erro = y - lrs.pred(x)
    MSE = (erro**2).sum()/erro.size
    ax.plot([x, x], [erro*0, erro])
    ax.set_title('MSE = {0:.2f}'.format(MSE),fontsize=8,y=0.88)
    ax.grid(color = '0.9', linestyle = ':')
    ax.axis([-0.1, 1.1, -0.75, 0.75])


#Synthetic data 1
def test_linear_regression():
    x, yA, yB, yC, yD = synthData1()
    lrs = linearRegression_simple()

    fig, [[axA, axB], [axC, axD]] = plt.subplots(2, 2)
    lrs.fit(x, yA)
    cellPlot_v1(axA, x, yA, lrs)
    lrs.fit(x, yB)
    cellPlot_v1(axB, x, yB, lrs)
    lrs.fit(x, yC)
    cellPlot_v1(axC, x, yC, lrs)
    lrs.fit(x, yD)
    cellPlot_v1(axD, x, yD, lrs)
    fig.savefig('output/regression_linear_pred.png', tight_layout=True)
    plt.show()

    fig2, [[axA, axB], [axC, axD]] = plt.subplots(2, 2)
    cellPlot_mse(axA, x, yA, lrs)
    cellPlot_mse(axB, x, yB, lrs)
    cellPlot_mse(axC, x, yC, lrs)
    cellPlot_mse(axD, x, yD, lrs)
    fig2.savefig('output//regression_linear_residual.png', tight_layout=True)


def cellPlot_multi(ax, m, alt, azi,x1,x2,y,p,up,down,cmapUp,cmapDown,px,py,pz,M):
    ax.view_init(alt, azi)
    ax.scatter3D(x1[up], x2[up], y[up], zorder=1)
    for i, j, k, l in zip(x1[up], x2[up], y[up], p[up]):
        ax.plot([i, i], [j, j], [k, l], ':',
                zorder=2, alpha=0.5,
                color=cmapUp((i ** 2 + j ** 2) ** 0.5))
    for i, j, k, l in zip(x1[down], x2[down], y[down], p[down]):
        ax.plot([i, i], [j, j], [k, l], ':',
                zorder=5, alpha=0.5,
                color=cmapDown((i ** 2 + j ** 2) ** 0.5))
    ax.scatter3D(x1[down], x2[down], y[down], zorder=4)
    ax.plot_surface(px * m, py * m, pz * m,
                    rstride=M,
                    cstride=M,
                    color='red',
                    alpha=0.5,
                    zorder=3)


def cellPlot_multi_mse(ax, x1, x2, y,p,up,down,cmapUp,cmapDown,  alt, azi,fig):
    ax.view_init(alt, azi)
    error = y - p
    MSE = (error**2).sum()/error.size
    for i, j, e in zip(x1[up], x2[up], error[up]):
        ax.plot([i, i], [j, j], [e*0, e], zorder=1, color=cmapUp((i**2 + j**2)**0.5))
    for i, j, e in zip(x1[down], x2[down], error[down]):
        ax.plot([i, i], [j, j], [e*0, e], ':', zorder=2, color = cmapDown((i**2 + j**2)**0.5))
    fig.suptitle('Multiple Linear Regression\nMSE = {0:.2f}'.format(MSE))


# Synthetic data 2
def test_linear_regression_multi():
    M = 10
    s, t, x1, x2, y = synthData2(M)
    lrm = linearRegression_multiple()
    # Prediction
    lrm.fit([x1, x2], y)
    ####################
    px, py = s, t
    p = lrm.pred([x1, x2])
    up = y >= p
    down = y < p
    pz = p.reshape(M, M)
    ####################
    cmapUp = cm.get_cmap('spring')
    cmapDown = cm.get_cmap('winter')

    fig, (axA, axB) = plt.subplots(1, 2, subplot_kw={'projection': '3d'})
    fig.suptitle('Linear Regresion Multiple\nm1 = {0:.2f}, m2 = {1:.2f}, b = {2:.2f}'.format(*lrm.m, lrm.b))
    cellPlot_multi(axA, 1.75, 20, -250, x1, x2, y,p, up, down, cmapUp, cmapDown, px, py, pz, M)
    cellPlot_multi(axB, 1.75, 5, -50, x1, x2, y, p,up, down, cmapUp, cmapDown, px, py, pz, M)
    fig.savefig('output/regression_linear_multiple_pred.png', tight_layout=True)
    plt.show()

    fig2, (axA, axB) = plt.subplots(1, 2, subplot_kw={'projection': '3d'})
    cellPlot_multi_mse(axA, x1, x2, y, p, up, down, cmapUp, cmapDown, 20, -150, fig2)
    cellPlot_multi_mse(axB, x1, x2, y, p, up, down, cmapUp, cmapDown, 5, -85, fig2)
    fig2.savefig('output/regression_linear_multipla_residual.png', tight_layout=True)
    plt.show()

# Synthetic data 3

def cellPlot_GD(ax, title='',
             sx='', sy='',
             xlim=[-0.1, 1.1],
             ylim=[-0.5, 1.5],
             leg=True):
    ax.set_title(title,fontsize=8,y=0.88)
    ax.grid(color='0.9', linestyle=':')
    ax.axis([*xlim, *ylim])
    ax.set_xlabel(sx)
    ax.set_ylabel(sy)
    if leg:
        ax.legend()

def test_linear_regression_GD():
    x, x_, y = synthData3()

    fig, [[axA, axB], [axC, axD]] = plt.subplots(2, 2)
    lrs = linearRegression_simple()
    lrgd = linearRegression_GD(rate=0.01)
    lrs.fit(x, y)

    global B, M, I, E, counter
    B, M, I, E = [], [], [], []
    iterations = 3072
    nframes = 64
    counter = 0

    def animation(frame):
        global B, M, I, E, counter
        for i_ in range(48):
            B += [lrgd.b]
            M += [lrgd.m]
            I += [counter]
            error = y - lrgd.pred(x)
            e = np.sum(error ** 2) / x.size
            E += [e]
            lrgd.fit_step(x, y)
            counter += 1
        i = counter

        axA.cla()
        axB.cla()
        axC.cla()
        axD.cla()
        axA.scatter(x, y, 32, label='data')
        axA.plot(x_, lrs.pred(x_), '--', color='red',
                 label='linear regression')
        axA.plot(x_, lrgd.pred(x_), color='green',
                 label='gradient descent')
        cellPlot_GD(axA)
        axB.plot([x, x], [error * 0, error])
        cellPlot_GD(axB, ylim=[-1, 1], leg=False)
        axC.plot(B, M)
        cellPlot_GD(axC, 'b = {0:.3f}, m = {1:.3f}'.format(lrgd.b, lrgd.m),
                 xlim=[-0.5, 0.5],
                 sx='linear coeficient (b)',
                 sy='angular coeficient (m)',
                 leg=False)
        axD.plot(I, E)
        axD.set_xscale('symlog', nonposx='clip')
        cellPlot_GD(axD, r'iteration = {0:04d}, $\epsilon$ = {1:.4f}'.format(i, e),
                 xlim=[0, iterations],
                 ylim=[-0.1, 0.6],
                 sx='iterations (log)',
                 sy='error',
                 leg=False)
        return fig.canvas.draw(),

    anim = manim.FuncAnimation(fig, animation, frames=nframes, interval=100)
    anim.save('output/regression_linear_gradDesc.gif', writer="imagemagick", extra_args="convert")
    plt.close()






# Synthetic data 4
def cellPlot_anscombe(ax, x, y, lrs):
    ax.scatter(x, y, 32, label='data')
    ax.plot([x, x], [y, lrs.pred(x)], ':')
    ax.plot(0, 0, ':', alpha=0.5, label='error')
    ax.plot([-50, 50], lrs.pred([-50, 50]), color='red', label='regression')
    ax.set_title('ρ = {0:.2f}, m = {1:.2f}, b = {2:.2f}'.
                 format(correlation(x, y), lrs.m, lrs.b),fontsize=8,y=0.88)
    ax.grid(color='0.9', linestyle=':')
    ax.axis([-0, 20, 0, 15])
    ax.legend()

def cellPlot_mse_anscombe(ax, x, y, lrs):
    error = y - lrs.pred(x)
    MSE = (error ** 2).sum() / error.size
    ax.plot([x, x], [error * 0, error])
    ax.set_title('MSE = {0:.2f}'.format(MSE),fontsize=8,y=0.88)
    ax.grid(color='0.9', linestyle=':')
    ax.axis([-0, 20, -5, 5])

def test_anscombe():
    x1, y1, x2, y2, x3, y3, x4, y4 = synthData4()
    lrs = linearRegression_simple()
    lrs.fit(x1, y1)
    lrs.fit(x2, y2)
    lrs.fit(x3, y3)
    lrs.fit(x4, y4)

    fig, [[axA, axB], [axC, axD]] = plt.subplots(2, 2)
    cellPlot_anscombe(axA, x1, y1, lrs)
    cellPlot_anscombe(axB, x2, y2, lrs)
    cellPlot_anscombe(axC, x3, y3, lrs)
    cellPlot_anscombe(axD, x4, y4, lrs)
    fig.savefig('output/regression_linear_anscombe_pred.png', tight_layout=True)
    plt.show()

    fig, [[axA, axB], [axC, axD]] = plt.subplots(2, 2)
    cellPlot_mse_anscombe(axA, x1, y1, lrs)
    cellPlot_mse_anscombe(axB, x2, y2, lrs)
    cellPlot_mse_anscombe(axC, x3, y3, lrs)
    cellPlot_mse_anscombe(axD, x4, y4, lrs)
    fig.savefig('output/regression_linear_anscombe_residual.png', tight_layout=True)
    plt.show()




if __name__ == "__main__":
    # test_linear_correlation()
    # test_linear_regression()
    # test_linear_regression_multi()
    # test_linear_regression_GD()
    test_anscombe()
	 




