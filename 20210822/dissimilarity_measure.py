import numpy as np
from dissimilarity__utils import *

def test_euclidean():
    eucl = lambda x, y: np.sum((x - y)**2, axis=1)**0.5
    x = np.array([0, 0])
    dA = eucl(x, yA)
    dB = eucl(x, yB).reshape(s.shape)
    plotDist(x, dA, dB, 'euclidean_distance', save=True)


def test_manhattan():
    manh = lambda x, y: np.sum(np.absolute(x - y), axis=1)
    x = np.array([0, 0])
    dA = manh(x, yA)
    dB = manh(x, yB).reshape(s.shape)
    plotDist(x, dA, dB, 'manhattan_distance', save=True)


def test_chebyshev():
    cheb = lambda x, y: np.max(np.absolute(x - y), axis=1)
    x = np.array([0, 0])
    dA = cheb(x, yA)
    dB = cheb(x, yB).reshape(s.shape)
    plotDist(x, dA, dB, 'chebyshev_distance', save=True)


def test_minkowski():
    mink = lambda x, y, p: np.sum(np.absolute(x - y) ** p, axis=1) ** (1 / p)
    x = np.array([0, 0])
    p = 2 ** -1
    dA = mink(x, yA, p)
    dB = mink(x, yB, p).reshape(s.shape)
    plotDist(x, dA, dB, 'minkowski_distance_A', ctitle=r'$p=2^{0}{2}{1}={3}$'.format('{', '}', -1, p), save=True)

def test_minkowski_multi():
    mink = lambda x, y, p: np.sum(np.absolute(x - y) ** p, axis=1) ** (1 / p)
    x = np.array([0, 0])
    fig, axes = plt.subplots(2, 4, sharex=True, sharey=True)
    for j, axs in enumerate(axes):
        for i, ax in enumerate(axs):
            index = i + 4 * j
            exp = index - 3
            pi = 2 ** exp
            d = mink(x, yB, pi).reshape(s.shape)
            plotContour(ax, d,
                        r'$p=2^{0}{2}{1}={3}$'.format('{', '}', exp, pi),
                        fsize=8)
    figname = 'minkowski_distance_B'
    fig.suptitle(' '.join([e.capitalize() for e in figname.split('_')]))
    fig.savefig('_output/similarity_{}.png'.format(figname), bbox_inches='tight')


def canb(x, y):
    num = np.absolute(x - y)
    den = np.absolute(x) + np.absolute(y)
    return np.sum(num/den, axis = 1)

def test_canberra():
    x = np.array([0.25, 0.25])
    dA = canb(x, yA)
    dB = canb(x, yB).reshape(s.shape)
    plotDist(x, dA, dB, 'canberra_distance', save=True)

def coss(x, y):
    if x.ndim == 1:
        x = x[np.newaxis]
    num = np.sum(x*y, axis=1)
    den = np.sum(x**2, axis = 1)**0.5
    den = den*np.sum(y**2, axis = 1)**0.5
    return 1 - num/den

def test_cosine():
    x = np.array([1e-7, 1e-7])
    dA = coss(x, yA)
    dB = coss(x, yB).reshape(s.shape)
    plotDist(x, dA, dB, 'cosine_distance', save=True)


if __name__ == "__main__":
    test_euclidean()
    test_manhattan()
    test_chebyshev()
    test_minkowski()
    test_minkowski_multi()
    test_canberra()
    test_cosine()

