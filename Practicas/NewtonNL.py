import numpy as np
from sympy import *
from pprint import pprint
from random import randint
from copy import copy
from time import time


class Jacobiana:

    def __init__(self, Xs):
        self.Xs = Xs

    def generar(self, ecuaciones):
        Xs = self.Xs
        dim = len(ecuaciones)
        matriz = []
        for i in range(dim):
            fila = []
            ecuacion = ecuaciones[i]
            for j in range(dim):
                fila.append(diff(ecuacion, Xs[j]))
            matriz.append(fila)

        self.matriz = matriz
        return matriz

    def printJacobiana(self, M):
        dim = len(M)
        for i in range(dim):
            print(M[i])

    def evaluar(self, X0, X, A):
        num = len(A)
        matriz = np.zeros((num, num), dtype=np.float)
        for i in range(num):  # iteramos filas
            for j in range(num):  # iteramos columnas
                ecuacion = copy(A[i][j])
                for n in range(num):
                    ecuacion = ecuacion.subs(X[n], X0[n])
                matriz[i][j] = float(ecuacion)

        return matriz


class NumMethods:

    def norma(self, vector):
        suma = 0
        for i in vector:
            suma += i**2
        return sqrt(suma)

    def printSolucion(self, Xs):
        for i in range(len(Xs)):
            print(f'\n x{i} = {Xs[i]}')

    def NewtonNL(self, num, eqs, X):
        Jacob = Jacobiana(X)
        J = Jacob.generar(eqs)
        X0 = [0.1 for i in range(num)]
        maxIter = 1000
        error = 0.001
        FX0 = [0 for i in range(len(eqs))]
        for i in range(maxIter):
            # print('\n\nJacobiana:\n\n', J)
            #print('ecuaciones: ', eqs)
            for j in range(num):
                ecuacion = eqs[j]
                for n in range(num):
                    ecuacion = ecuacion.subs(X[n], X0[n])
                    # print('\n\npasó sustitución\n\n'
                FX0[j] = float(ecuacion)
            Jinv = np.linalg.inv(Jacob.evaluar(X0, X, copy(J)))
            # print('\n\nJacobiana original despues de calcular inversa:\n\n', J)
            Y0 = np.matmul(Jinv, FX0)
            X1 = X0-Y0

            # print('\n\nX0:\n\n', X0)
            # print('\n\nFX0:\n\n', FX0)
            # print('\n\nJacobiana inversa: \n\n', Jinv)
            # print('\n\nY0:\n\n', Y0)
            # print('\n\nX1:\n\n', X1)
            # print('\n\nEcuaciones:\n\n', eqs)
            if np.linalg.norm(X1-X0) <= error:
                print('\nLa solución calculada fue:')
                print('\nNúmero de iteraciones: ', i+1)
                self.printSolucion(X1)
                return X1
            #print('loop pasado: ', i)
            X0 = X1
            # print(X1)

        print(
            f'Límite de iteraciones alcanzado {maxIter}. Valores aproximados:')
        self.printSolucion(X1)
        return X1


def makeSymbolics(num):
    return [symbols(f'x{i}') for i in range(num)]


def sysEquations(num):
    eqs = []
    for i in range(num):
        eqs.append(sympify(input(f'ingrese la ecuacion {i}:\n')))
    return eqs


num = int(input('Ingese el número de incógnitas/ecuaciones: '))
X = makeSymbolics(num)
print('Variables simbólicas:\n', X)
eqs = sysEquations(num)
print('Ecuaciones:\n')
for i in eqs:
    print(i)

NM = NumMethods()
t = time()
NM.NewtonNL(num, eqs, X)
print(f'\nEl timepo de ejecución fue de {time() -t } segundos.')
