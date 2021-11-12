import os
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

plt.rcParams['figure.figsize'] = (16, 8)


def test1():
    # left data
    M, N = 16, 4
    dadosEmp = np.random.random((N, M)) * 0.9 + 0.1
    empilha = 100 * dadosEmp / np.sum(dadosEmp, axis=0)
    # right data
    folhas = 64
    area = np.random.random(folhas) * 3 + 1
    area = np.round_(area, decimals=2)
    cores = np.random.random(folhas)
    lado = area.sum() ** 0.5
    # param
    cmapArvore = cm.get_cmap('rainbow')
    cores = cmapArvore(cores)
    from squarify import squarify
    partes = squarify(area, 0, 0, lado, lado)
    x = [parte['x'] for parte in partes]
    y = [parte['y'] for parte in partes]
    dx = [parte['dx'] for parte in partes]
    dy = [parte['dy'] for parte in partes]
    fig, (axA, axB) = plt.subplots(1, 2)
    # draw left
    axA.stackplot(np.arange(M), empilha, baseline='zero')
    axA.set_title('stack_plot')
    axA.set_ylabel('ratio')
    axA.set_xticks(np.arange(M))
    axA.set_yticks(np.linspace(0, 100, M))
    axA.set_xticklabels([chr(i + ord('a')) for i in range(M)])
    axA.legend(['G{}'.format(i + 1) for i in range(N)])
    axA.grid(alpha=0.75, linestyle=':')
    # draw right
    axB.bar(x, dy, width=dx, bottom=y, color=cores, align='edge')
    for p, a in zip(partes, area):
        x, y, dx, dy = p['x'], p['y'], p['dx'], p['dy']
        axB.text(x + dx * 0.5, y + dy * 0.5, a, va='center', ha='center')
    axB.set_title('squarify')
    plt.show()


def test2():
    # 统计数据
    entrev_dia = 1000
    dias = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    ndias = len(dias)
    mu = 4 + np.random.random(ndias) * 2
    sigma = 0.5 + np.random.random(ndias) * 2
    horas = np.random.normal(mu, sigma, (entrev_dia, ndias))
    horas += np.random.random((entrev_dia, ndias)) * 2 - 1
    # 显示参数
    cmapStat = cm.get_cmap('cool')
    posicao = np.arange(ndias) * 1.5
    fig, (axA, axB) = plt.subplots(1, 2)
    # 箱图和小提琴图
    bplots = axA.boxplot(horas, positions=posicao - 0.25,
                         vert=True, widths=0.25,
                         patch_artist=True, notch=True)
    violins = axA.violinplot(horas, positions=posicao + 0.25,
                             widths=0.25, showmeans=True)
    for i, (box, violin) in enumerate(zip(bplots['boxes'], violins['bodies'])):
        cor = cmapStat(i / ndias)
        box.set_facecolor(cor)
        violin.set_facecolor(cor)
        violin.set_edgecolor('black')
        violin.set_alpha(0.75)
    axA.set_title('box_violin')
    axA.set_ylabel('sleep time')
    axA.set_xticks(posicao)
    axA.set_yticks(range(1, 10))
    axA.set_xticklabels(dias)
    axA.set_xlim((-0.5, 6.5))
    axA.grid(alpha=0.75, linestyle=':')

    # Histogram
    n, bins, patches = axB.hist(horas, bins=50, stacked=True)
    for i, patchList in enumerate(patches):
        for patch in patchList:
            patch.set_facecolor(cmapStat(i / ndias))
    axB.set_title('Histograma')
    axB.set_xlabel('sleep time')
    axB.set_ylabel('count of people')
    axB.legend(dias)
    plt.show()

    pass



if __name__ == "__main__":
    test1()
    test2()