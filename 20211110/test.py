import os
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

plt.rcParams['figure.figsize'] = (16, 8)




def draw_line():
            N = 8
            t = np.linspace(0, 1, N)

            fig, (axA, axB) = plt.subplots(1, 2)
            # Line
            axA.plot(t, t, marker = 'o')
            axA.set_title('line')

            # Curve
            axB.plot(t, t, linestyle='--', marker='*', c='r', label='linear')
            axB.plot(t, t**2, linestyle='-.', marker='D',c='c', label='quadratic')
            axB.plot(t, t**3, linestyle=':', marker='^',c='y', label='cubic')
            axB.set_title('Curve')
            plt.legend()
            plt.show()

def  draw_scatter():
        N = 128
        x = np.random.rand(N)
        y = np.random.rand(N)
        c = np.random.rand(N)
        s = np.random.rand(N)
        s = np.pi*(32*s)**2

        cmapDisp = cm.get_cmap('rainbow')
        fig, (axA, axB) = plt.subplots(1, 2)
        # scatter
        axA.scatter(x, y, s=8,c=cmapDisp(c),alpha=0.75)
        axA.set_title('scatter')
        # bubble
        axB.scatter(x, y, c=cmapDisp(c), s=s, alpha=0.25, edgecolors='none')
        axB.set_title('bubble')
        plt.show()

def  draw_bar():
        N = 8
        Hx = np.random.randint(18, 65, size=N)
        Mx = np.random.randint(18, 65, size=N)
        Hs = np.random.randint(1, 5, size=N)
        Ms = np.random.randint(1, 5, size=N)
        indice = np.arange(N) + 1
        igrupos = ['G{}'.format(g) for g in indice]
        iidades = np.arange(0, 80, 5)
        larg = 0.25
        fig, (axA, axB) = plt.subplots(1, 2)
        
        # Bar
        axA.bar(indice - larg, Hx, width=larg, yerr=Hs,color='c', align='edge', label='man')
        axA.bar(indice, Mx, width=larg, yerr=Ms, color='r', align='edge', label='women')
        axA.set_title('Bar')
        axA.set_xticks(indice)
        axA.set_yticks(iidades)
        axA.set_xticklabels(igrupos)
        axA.legend()
        # Barras
        axB.bar(indice, Hx, color='c', label='man', yerr=Hs)
        axB.bar(indice, Mx, color='r', bottom=Hx, label='women', yerr=Ms)
        axB.set_title('Barras ')
        axB.set_xticks(indice)
        axB.set_xticklabels(igrupos)
        axB.set_yticks(iidades*2)
        axB.legend()
        plt.show()


def test_pie():
        etiqueta = list('ABCDEFGHIJKL')
        M, N = 128, len(etiqueta)
        valor = np.random.random(N)*0.9 + 0.1
        var = np.random.random(M)
        # param
        cmapRadial = cm.get_cmap('magma')
        theta = 2*np.pi*np.arange(N)/N
        omega = 2*np.pi*np.arange(M)/M
        valor_ = np.append(valor, [valor[0]])
        var_ = np.append(var, [var[0]])
        theta_ = np.append(theta, [theta[0]])
        omega_ = np.append(omega, [omega[0]])
        raio = 1.25
        mult = 0.15
        # draw
        fig = plt.figure()
        axA = fig.add_subplot(121, aspect='equal')
        axB = fig.add_subplot(122, projection='polar')
        
        # Pizza 
        axA.pie(valor, labels=etiqueta, pctdistance=0.9,autopct='%1.1f%%', radius=1.1)
        axA.pie(var, radius=0.9, colors=cmapRadial(var))
        axA.set_title('Pizza ')
        centro = plt.Circle((0,0), 0.75, fc='white')
        axA.add_patch(centro)
        
        # Radar
        axB.plot(theta_, valor_, marker='o', color='black', label='variable')
        axB.fill_between(theta_, 0, valor_, facecolor='black', alpha=0.25)
        axB.plot(omega_, raio + var_*mult, color='y', label='change')
        axB.plot(omega_, raio - var_*mult, color='y')
        axB.fill_between(omega_, raio - var_*mult, raio + var_*mult,facecolor='y', alpha=0.25)
        axB.set_title('Radar')
        axB.set_xticks(theta)
        axB.set_xticklabels(etiqueta)
        axB.set_rticks(np.linspace(0, 1.5, 7))
        axB.legend()
        plt.show()


if __name__ == "__main__":
        #draw_line()
        # draw_scatter()
        #draw_bar()
        test_pie()
