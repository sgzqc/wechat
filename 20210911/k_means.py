import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as manim

from clustering__utils import *

plt.rcParams['figure.figsize'] = (16, 8)
plt.set_cmap('prism')


class kMeans(Distance):
    def __init__(self, K=2, iters=16, seed=1):
        super(kMeans, self).__init__()
        self._K = K
        self._iters = iters
        self._seed = seed
        self._C = None

    def _FNC(self, x, c, n):
        # for each point,
        # find the nearest center
        cmp = np.ndarray(n, dtype=int)
        for i, p in enumerate(x):
            d = self.distance(p, self._C)
            cmp[i] = np.argmin(d)
        return cmp

    def pred(self, X):
        # prediction
        n, dim = X.shape
        np.random.seed(self._seed)
        sel = np.random.randint(0, n, self._K)
        self._C = X[sel]
        cmp = self._FNC(X, self._C, n)
        for _ in range(self._iters):
            # adjust position of centroids
            # to the mean value
            for i in range(sel.size):
                P = X[cmp == i]
                self._C[i] = np.mean(P, axis=0)
            cmp = self._FNC(X, self._C, n)
        return cmp, self._C

def test1():
    x1, y1, x2, y2 = synthData()
    # visualization

    fig, (axA, axB) = plt.subplots(1, 2)
    axA.scatter(x1, y1, s=8);
    axA.set_title('dataset A')
    axB.scatter(x2, y2, s=8);
    axB.set_title('dataset B')

    plt.savefig('output/clustering_synthetic_data.png', bbox_inches='tight')
    plt.show()

def test_k_mean():
    x1, y1, x2, y2 = synthData()
    X1 = np.array([x1, y1]).T
    X2 = np.array([x2, y2]).T
    Cs = 12
    V1 = np.zeros(Cs)
    V2 = np.zeros(Cs)
    D = Distance()
    for k in range(Cs):
        kmeans = kMeans(K=k + 1, iters=48, seed=6)
        fnc1, C1 = kmeans.pred(X1)
        fnc2, C2 = kmeans.pred(X2)
        for i, [c1, c2] in enumerate(zip(C1, C2)):
            d1 = D.distance(c1, X1[fnc1 == i]) ** 2
            d2 = D.distance(c2, X2[fnc2 == i]) ** 2
            V1[k] += np.sum(d1)
            V2[k] += np.sum(d2)

    fig, (axA, axB) = plt.subplots(1, 2)

    axA.plot(range(1, Cs + 1), V1, marker='o')
    axA.scatter(3, V1[2], s=1024, edgecolor='red', facecolor='none')
    axA.set_xticks(range(Cs + 1))
    axA.set_xlim([1, Cs])

    axB.plot(range(1, Cs + 1), V2, marker='o')
    axB.scatter(6, V2[5], s=1024, edgecolor='red', facecolor='none')
    axB.set_xticks(range(Cs + 1))
    axB.set_xlim([1, Cs])

    plt.savefig('output/clustering_k-means_elbowMethod.png', bbox_inches='tight')
    plt.show()


def animation(frame):
    axA.cla();
    axB.cla()

    iters = frame;
    seed = 6

    K1 = 3
    kmeans1 = kMeans(K1, iters, seed)
    fnc1, C1 = kmeans1.pred(X1)

    K2 = 6
    kmeans2 = kMeans(K2, iters, seed)
    fnc2, C2 = kmeans2.pred(X2)

    axA.scatter(*X1.T, c=fnc1, s=8)
    axB.scatter(*X2.T, c=fnc2, s=8)
    axA.scatter(*C1.T, marker='*', s=256,
                c=range(K1), edgecolors='black')
    axB.scatter(*C2.T, marker='*', s=256,
                c=range(K2), edgecolors='black')
    axA.set_title('k = {0} ; i = {1:02d}'.format(K1, frame))
    axB.set_title('k = {0} ; i = {1:02d}'.format(K2, frame))

    return fig.canvas.draw()

def test3():
    global fig,axA,axB
    fig, (axA, axB) = plt.subplots(1, 2)
    iters = 21

    global X1,X2
    x1, y1, x2, y2 = synthData()
    X1 = np.array([x1, y1]).T
    X2 = np.array([x2, y2]).T

    anim = manim.FuncAnimation(fig, animation, frames=iters, interval=500)

    anim.save('output/clustering_k-means.gif', writer="imagemagick", extra_args="convert")
    plt.close()

if __name__ == "__main__":
    #test1()
    #test_k_mean()
    test3()