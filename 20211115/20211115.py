import os
import sys
import cv2
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import matplotlib.tri as tri
from matplotlib.path import Path
import matplotlib.patches as patches

plt.rcParams['figure.figsize'] = (16, 8)


def test1():
    # data
    pn, cn = 64, 8
    px = np.random.normal(0, 1, pn)
    py = np.random.normal(0, 1, pn)
    cx = np.random.normal(0, 1, cn)
    cx = np.insert(cx, 0, 0)
    cy = np.random.normal(0, 1, cn)
    cy = np.insert(cy, 0, 0)
    angle = (np.arctan2(py, px) + np.pi) / (2 * np.pi)
    # param
    distrib = tri.Triangulation(np.concatenate([px, cx]),
                                np.concatenate([py, cy]))
    cmapRede = cm.get_cmap('hsv')
    fig, (axA, axB) = plt.subplots(1, 2)

    # left: draw each pt to the nearest center pt
    for s, t in zip(px, py):
        dist = ((s - cx) ** 2 + (t - cy) ** 2) ** 0.5
        csel = dist <= dist.min()
        for u, v in zip(cx[csel], cy[csel]):
            axA.plot([s, u], [t, v], color='black', alpha=0.5,
                     linewidth=1, zorder=1)
    # left: draw each center to (0,0)
    for u, v in zip(cx, cy):
        if u or v:
            axA.plot([u, 0], [v, 0], color='black', alpha=0.25,
                     linewidth=2, zorder=1)
    axA.scatter(px, py, c=cmapRede(angle), zorder=2)
    axA.scatter(cx, cy, color='black', s=64, zorder=2)
    axA.set_title('decentralized_network')

    # right
    axB.triplot(distrib, color='black', alpha=0.5, linewidth=1, zorder=1)
    axB.scatter(px, py, c=cmapRede(angle), zorder=2)
    axB.scatter(cx, cy, color='black', s=64, zorder=2)
    axB.set_title('distributed_network')
    plt.show()


def test2():
    # dataflow
    colecao = np.array(list('αβγδε'))
    n = len(colecao)
    indices = np.arange(n)
    sel = lambda x: np.random.choice(x, 16)
    mapa = np.array([sel(np.delete(indices, i)) for i in indices])
    rede = colecao[mapa]
    # param
    pontos = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    paleta = cm.get_cmap('gist_rainbow')
    fig, axA = plt.subplots(1, 1)
    # Flow horizontal
    getPy = lambda x: (1 - x / n) - 0.1
    for i, e in enumerate(colecao):
        conx, cont = np.unique(rede[i], return_counts=True)
        yo = getPy(i)
        *cor, _ = paleta(i / n)
        axA.text(-0.01, yo, e, ha='right', color=cor,
                 fontsize=16, fontweight='bold')
        axA.text(1.01, yo, e, ha='left', color=cor,
                 fontsize=16, fontweight='bold')
        for cx, ct in zip(conx, cont):
            yi = float(getPy(np.where(colecao == cx)[0]))
            verts = [(0.0, yo), (0.5, yo), (0.5, float(yi)), (1, float(yi))]
            path = Path(verts, pontos)
            patch = patches.PathPatch(path, facecolor='none', edgecolor=cor,
                                      lw=ct ** 2, alpha=1 / ct)
            axA.add_patch(patch)
    axA.set_title('Flow Horizontal')
    axA.axis('off')
    plt.show()


def test3():
    # data
    n = 17
    indices = np.arange(n)
    sel = lambda x: np.random.choice(x, n // 4)
    mapa = np.array([sel(np.delete(indices, i)) for i in indices])
    rede = indices[mapa]
    print(rede)
    # param
    cmapArco = cm.get_cmap('rainbow')
    fig, (axA, axB) = plt.subplots(1, 2)
    # Arc
    getPx = lambda x: x / (n - 1)
    pontos = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    for i, e in enumerate(indices):
        print("i={} and e={}".format(i,e))
        conx, cont = np.unique(rede[i], return_counts=True)
        print("conx={} and cont={}".format(conx,cont))
        xo = getPx(i)
        *cor, _ = cmapArco(i / n)
        for cx, ct in zip(conx, cont):
            xi = getPx(np.where(indices == cx)[0])
            yoi = (xi - xo) * 2 ** 0.5
            verts = [(xo, 0), (xo, yoi), (xi, yoi), (xi, 0)]
            print("verts=")
            print(verts)
            path = Path(verts, pontos)
            patch = patches.PathPatch(path, facecolor='none', edgecolor=cor,
                                      lw=0.5 * ct ** 3, alpha=1 / ct)
            axA.add_patch(patch)

    axA.scatter(indices / (n - 1), indices * 0, color=cmapArco(indices / n),
                marker='s', s=256, zorder=2)
    axA.set_title('Arc')
    axA.set_xlim([-0.05, 1.05])
    axA.set_ylim([-1.2, 1.2])
    axA.axis('off')

    # Convergence radial
    getTheta = lambda x: 2 * np.pi * x / n
    for i, e in enumerate(indices):
        conx, cont = np.unique(rede[i], return_counts=True)
        thetao = getTheta(i)
        xo = np.sin(thetao)
        yo = np.cos(thetao)
        *cor, _ = cmapArco(i / n)
        for cx, ct in zip(conx, cont):
            thetai = getTheta(np.where(indices == cx)[0])
            xi = np.sin(thetai)
            yi = np.cos(thetai)
            xm = (xo + xi) * 0.5
            ym = (yo + yi) * 0.5
            verts = [(xo, yo), ((xo + xm * 0.25) * 0.5, (yo + ym * 0.25) * 0.5),
                     ((xi + xm * 0.25) * 0.5, (yi + ym * 0.25) * 0.5), (xi, yi)]
            path = Path(verts, pontos)
            patch = patches.PathPatch(path, facecolor='none', edgecolor=cor,
                                      lw=ct ** 3, alpha=1 / ct)
            axB.add_patch(patch)

    axB.scatter(np.sin(getTheta(indices)), np.cos(getTheta(indices)),
                color=cmapArco(indices / n), s=512, zorder=2)
    axB.set_title('Convergence radial')
    axB.set_xlim([-1.2, 1.2])
    axB.set_ylim([-1.2, 1.2])
    axB.axis('off')
    plt.show()


def test4():
    fig, ax = plt.subplots()
    path_data = [
        (Path.MOVETO, (0, 0.09)),
        (Path.CURVE4, (0.5, 0.09)),
        (Path.CURVE4, (0.5, 0.3)),
        (Path.CURVE4, (1, 0.3)),
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='r', alpha=0.9)
    ax.add_patch(patch)
    # 绘制控制多边形和连接点
    x, y = zip(*path.vertices)
    line, = ax.plot(x, y, 'go-')
    # 显示网格
    ax.grid()
    # 设置坐标轴刻度大小一致，可以更真实地显示图形
    ax.axis('equal')
    plt.show()


def test5():
    fig, ax = plt.subplots()

    xo = 0
    xi = 0.75
    yoi = (xi - xo)/2 * 2 ** 0.5
    #verts = [(xo, 0), (xo, yoi), (xi, yoi), (xi, 0)]


    path_data = [
        (Path.MOVETO, (0, 0)),
        (Path.CURVE4, (0, yoi)),
        (Path.CURVE4, (xi, yoi)),
        (Path.CURVE4, (xi, 0)),
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='r', alpha=0.9)
    ax.add_patch(patch)
    # 绘制控制多边形和连接点
    x, y = zip(*path.vertices)
    line, = ax.plot(x, y, 'go-')
    # 显示网格
    ax.grid()
    # 设置坐标轴刻度大小一致，可以更真实地显示图形
    ax.axis('equal')
    plt.show()


if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    #test4()
    test5()

    pass