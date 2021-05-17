# 2o Examen Parcial Práctico
# Mario Valverde

import numpy as np
from sympy import *
from pprint import pprint
from random import randint
from copy import copy


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

    def verticalVector(self, lista):
        x = [[i] for i in lista]
        return np.asarray(x)

    def flatten(self, vector):
        return [i[0] for i in vector]

    def NewtonNL(self, num, eqs, X):
        Jacob = Jacobiana(X)
        J = Jacob.generar(eqs)
        X0 = [0.1 for i in range(num)]
        maxIter = 100
        error = 0.001
        FX0 = [0 for i in range(len(eqs))]
        for i in range(maxIter):
            for j in range(num):
                ecuacion = eqs[j]
                for n in range(num):
                    ecuacion = ecuacion.subs(X[n], X0[n])
                FX0[j] = float(ecuacion)
            A = Jacob.evaluar(X0, X, copy(J))
            Jinv = np.linalg.inv(A)
            Y0 = np.matmul(Jinv, FX0)
            X1 = X0-Y0

            if np.linalg.norm(X1-X0) <= error:
                print(f'\nLa solución calculada en {i} iteraciones.\n')
                print('La solución estimada')
                self.printSolucion(X1)
                return X1
            X0 = X1
        print('limite de iteraciones alcanzado, se calculó: \n\n')
        print(X1)
        return X1

    def evaluarFX(self, X, X0, eqs):
        FX = [0 for i in range(len(eqs))]
        for i in range(num):
            ecuacion = eqs[i]
            for j in range(num):
                ecuacion = ecuacion.subs(X[j], X0[j])
            FX[i] = float(ecuacion)
        return np.asarray(FX)

    def Broyden(self, num, eqs, Xs):
        evaluarFX = self.evaluarFX
        Jacob = Jacobiana(X)
        J = Jacob.generar(eqs)
        X0 = [0.1 for i in range(num)]
        error = 0.001
        maxIter = 10
        FX0 = evaluarFX(Xs, X0, eqs)
        A = Jacob.evaluar(X0, Xs, copy(J))
        A0inv = np.linalg.inv(copy(A))
        Y0 = np.matmul(A0inv, FX0)
        X1 = X0-Y0

        FX1 = evaluarFX(Xs, X1, eqs)

        for i in range(maxIter):

            flatX0 = X0
            flatX1 = X1
            flatFX0 = FX0
            flatFX1 = FX1

            X0 = self.verticalVector(X0)
            X1 = self.verticalVector(X1)
            FX0 = self.verticalVector(FX0)
            FX1 = self.verticalVector(FX1)

            s = X1 - X0
            st = np.transpose(s)
            y = FX1 - FX0
            y = y.astype(float)

            a = np.matmul(A0inv, y)
            a = s - a
            b = np.matmul(a, st)
            c = np.matmul(b, A0inv)
            d = np.matmul(st, A0inv)
            e = np.matmul(d, y)
            A1inv = copy(A0inv) + c/e[0]
            Z = np.matmul(copy(A1inv), FX1)
            X2 = X1 - Z

            if np.linalg.norm(X2-X1) < error:
                print(f'\nResultado alcanzado en {i} iteraciones')
                print('\nsolución encontrada:\n')
                self.printSolucion(self.flatten(X2))
                return X2

            flatX2 = self.flatten(X2)

            A0inv = copy(A1inv)
            X0 = flatX1
            X1 = flatX2
            FX0 = flatFX1
            FX1 = evaluarFX(Xs, flatX2, eqs)

        print('Límite de iteraciones alcanzado. Valores aproximados:')
        self.printSolucion(X1)


def makeSymbolics(num):
    return [symbols(f'x{i}') for i in range(num)]


def sysEquations(num):
    eqs = []
    eqs.append(sympify('x0*33/3 - sin(x1*x2) - 0.7'))
    eqs.append(sympify('(52/5)*x0**4 - 81*(x1+0.1)**2 + sin(x2) + 1.06'))
    eqs.append(sympify('exp(-x1*x0**2) + 3*x1**1 + x2*(43/3) - ((10*3.1416)-3)/3'))
    return eqs


num = 3
X = makeSymbolics(num)
print('Variables simbólicas:\n', X)
eqs = sysEquations(num)
print('Ecuaciones:\n')
for i in eqs:
    print(i)

NM = NumMethods()
print('\n\nMediante NewtonNL\n\n')
NM.NewtonNL(num, eqs, X)
print('\n\nMediante Broyden\n\n')
NM.Broyden(num, eqs, X)
