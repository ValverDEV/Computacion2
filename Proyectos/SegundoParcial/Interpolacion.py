import pandas as pd
import numpy as np
from sympy import symbols, init_printing, expand, lambdify
import matplotlib.pyplot as plt
from time import time
from random import randint
from Gauss import Gauss

x = symbols('x')


class NumMethods:

    def __init__(self, Xs=0, Ys=0):
        self.puntosX = Xs
        self.puntosY = Ys
        self.matriz = []
        self.expr = 0

    def llenarPuntos(self):
        numPuntos = int(input('Cuántos puntos vas a ingresar? '))
        x = []
        y = []
        for i in range(numPuntos):
            x.append(float(input('x = ')))
            y.append(float(input('y = ')))
        self.puntosX = x
        self.puntosY = y

    def NewtonInterpol(self):
        self.matriz.append(self.puntosX)
        self.matriz.append(self.puntosY)
        self.diferenciasFinitas(len(self.puntosX) - 1)
        # print(self.matriz)
        temp = 1
        expr = self.matriz[1][0]
        for i in range(2, len(self.matriz)):
            for j in range(0, i-1):
                temp *= x-self.matriz[0][j]
            expr += self.matriz[i][0]*temp
            temp = 1

        print('polinomio calculado:')
        print(expand(expr))
        self.expr = expr

    def diferenciasFinitas(self, actual):
        if actual == 0:
            return self.puntosY
        self.diferenciasFinitas(actual - 1)
        col = []

        for i in range(len(self.puntosY) - actual):
            fx1 = self.matriz[-1][i+1]
            fx0 = self.matriz[-1][i]
            x1 = self.matriz[0][len(self.matriz) - 1 + i]
            x0 = self.matriz[0][i]
            col.append(self.diferencia(fx1, fx0, x1, x0))
        if not col in self.matriz:
            self.matriz.append(col)
        return col

    def diferencia(self, fx1, fx0, x1, x0):
        return (fx1 - fx0)/(x1-x0)

    def Lagrange(self):
        X = self.puntosX
        Y = self.puntosY
        expr = 0
        for i in range(len(X)):
            temp = 1
            for j in range(len(X)):
                if j == i:
                    pass
                else:
                    temp *= (x - X[j])/(X[i] - X[j])
            expr += temp*Y[i]
        expr = expr.expand()
        print('Polinomio calculado:')
        print(expr)
        self.expr = expr

    def Grafica(self):
        a = np.linspace(min(self.puntosX), max(self.puntosX), 1000)
        b = [self.expr.subs(x, i) for i in a]
        plt.plot(a, b)
        plt.scatter(self.puntosX, self.puntosY)
        plt.show()

    def ordenar_puntos(self):
        desordenada = []
        for i in range(len(self.puntosX)):
            desordenada.append((self.puntosX[i], self.puntosY[i]))
        ordenada = []
        while desordenada:
            min = 0
            for i in range(len(desordenada)):
                if desordenada[i][0] < desordenada[min][0]:
                    min = i
            ordenada.append(desordenada.pop(min))
        self.puntosX = [x[0] for x in ordenada]
        self.puntosY = [y[1] for y in ordenada]

    def polinomios(self):
        matriz = self.matriz
        As = []
        Bs = []
        Cs = []
        for i in range(0, int(len(matriz)/3)):
            As.append(matriz[3*i][-1]/matriz[3*i][3*i])
            Bs.append(matriz[3*i+1][-1]/matriz[3*i+1][3*i+1])
            Cs.append(matriz[3*i+2][-1]/matriz[3*i+2][3*i+2])

        polis = []

        print('Coeficientes: \n')
        for i in range(len(As)):
            print(f'a{i} = {As[i]}')
            print(f'b{i} = {Bs[i]}')
            print(f'c{i} = {Cs[i]}')
            poli = As[i]*x**2 + Bs[i]*x + Cs[i]
            polis.append(poli)

        print('\n\nPolinomios:\n\n')

        self.polis = polis
        for i in polis:
            print(i)

    def spline(self):
        self.ordenar_puntos()
        Xs = self.puntosX
        Ys = self.puntosY
        # Xs=[3,4.5,7,9]
        # Ys=[2.5,1,2.5,0.5]
        dim = len(Xs) - 1
        m_spline = np.zeros((dim*3, dim*3), dtype=np.float)
        m_y = np.zeros((dim*3, 1), dtype=np.float)
        num_ecuaciones = dim
        # primera condición: fi(xi) =yi, fi+1(xi)=yi
        m_spline[0][0] = Xs[0]**2
        m_spline[0][1] = Xs[0]
        m_spline[0][2] = 1
        m_y[0][0] = Ys[0]
        for i in range(num_ecuaciones - 1):
            j = 2*i + 1
            m_spline[j][3*i + 0] = Xs[i+1]**2
            m_spline[j][3*i + 1] = Xs[i+1]
            m_spline[j][3*i + 2] = 1
            m_y[j] = Ys[i+1]

            m_spline[j+1][3*(i+1) + 0] = Xs[i+1]**2
            m_spline[j+1][3*(i+1) + 1] = Xs[i+1]
            m_spline[j+1][3*(i+1) + 2] = 1
            m_y[j+1] = Ys[i+1]

        m_spline[(num_ecuaciones-1)*2+1][-3] = Xs[-1]**2
        m_spline[(num_ecuaciones-1)*2+1][-2] = Xs[-1]
        m_spline[(num_ecuaciones-1)*2+1][-1] = 1

        m_y[(num_ecuaciones-1)*2+1] = Ys[-1]

        # segunda condicion: derivdadas
        for i in range(num_ecuaciones - 1):
            # m_spline[-2-i][i] = Xs[i+1]*2
            # m_spline[-2-i][i+1] = 1
            # m_spline[-2-i][i+3] = -Xs[i+2]*2
            # m_spline[-2-i][i+4] = -1

            m_spline[-2-i][3*i+0] = Xs[i+1]*2
            m_spline[-2-i][3*i+1] = 1
            m_spline[-2-i][3*(i+1)+0] = -Xs[i+1]*2
            m_spline[-2-i][3*(i+1)+1] = -1

        # tercera condicion: segunda derivada
        m_spline[-1][0] = 1

        matriz = np.concatenate((m_spline, m_y), axis=1)
        GJ = Gauss()
        resultado = GJ.solucion(matriz)
        self.matriz = resultado
        self.polinomios()

    def Grafica_spline(self):
        for i in range(len(self.puntosX) - 1):
            a = np.linspace(self.puntosX[i], self.puntosX[i+1], 1000)
            b = [self.polis[i].subs(x, j) for j in a]
            plt.plot(a, b)
        plt.scatter(self.puntosX, self.puntosY)
        plt.show()

    def Evaluar(self):
        eval = input('\n\nQuiere evaluar alguna corriente? (y/n)\n')
        if eval == 'n':
            return
        while True:
            punto = float(input('Corriente a evaluar (amperes): '))
            NewtonEval = self.expr.subs(x, punto)
            print(f'Mediante Newton/Lagrange: {NewtonEval} Volts')

            eval = input('\nQuiere evaluar otra corriente? (y/n)\n')
            if eval == 'n':
                break


Xs = [-2, -1, -0.5, 0.5, 1, 2]
Ys = [-637, -96.5, -20.5, 20.5, 96.5, 637]

print('Puntos de corriente (amperes) y voltaje (volts) para la interpolación.\n')
for i in range(len(Xs)):
    print(f'I = {Xs[i]}, V = {Ys[i]}')

NM = NumMethods(Xs, Ys)

print('\n\nMétodo de Newton:\n\n')
t = time()
NM.NewtonInterpol()
print(f'\nTiempo de ejecución: {time() - t} segundos.\n')
NM.Grafica()

print('\n\nMétodo de Lagrange:\n\n')
t = time()
NM.Lagrange()
print(f'\nTiempo de ejecución: {time() - t} segundos.\n')
NM.Grafica()

print('\n\nMétodo Spline:\n\n')
t = time()
NM.spline()
print(f'\nTiempo de ejecución: {time() - t} segundos.\n')
NM.Grafica_spline()

NM.Evaluar()
