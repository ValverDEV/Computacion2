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

        # print('\n\nJacobiana evaluada:\n\n', matriz)
        return matriz


class NumMethods:

    def norma(self, vector):
        suma = 0
        for i in vector:
            suma += i**2
        #print('\n\n, suma:\n\n',suma)
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
        #X0 = [randint(-5,5) for i in range(num)]
        maxIter = 100
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
            A = Jacob.evaluar(X0, X, copy(J))
            Jinv = np.linalg.inv(A)
            #Jinv = np.linalg.inv(Jacob.evaluar(X0, X, copy(J)))
            # print('\n\nJacobiana original despues de calcular inversa:\n\n', J)
            Y0 = np.matmul(Jinv, FX0)
            X1 = X0-Y0

            # print('\n\nX0:\n\n', X0)
            # print('\n\nFX0:\n\n', FX0)
            # print('\n\nJacobiana OG:\n\n', A)
            # print('\n\nJacobiana inversa: \n\n', Jinv)
            # print('\n\nY0:\n\n', Y0)
            # print('\n\nX1:\n\n', X1)
            # print('\n\nEcuaciones:\n\n', eqs)
            if np.linalg.norm(X1-X0) <= error:
                print(f'\nLa solución calculada en {i} iteraciones.\n')
                print('La solución estimada')
                self.printSolucion(X1)
                return X1
            #print('loop pasado: ', i)
            X0 = X1
            # print(X1)
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
        # print(FX)
        return np.asarray(FX)

    def Broyden(self, num, eqs, Xs):
        evaluarFX = self.evaluarFX
        Jacob = Jacobiana(X)
        J = Jacob.generar(eqs)
        Jacob.printJacobiana(J)
        X0 = [0.1 for i in range(num)]
        error = 0.001
        maxIter = 10
        # Método de Newton para primera iteración
        FX0 = evaluarFX(Xs, X0, eqs)
        A = Jacob.evaluar(X0, Xs, copy(J))
        A0inv = np.linalg.inv(copy(A))
        Y0 = np.matmul(A0inv, FX0)
        X1 = X0-Y0

        # print('\n\nJacobiana OG\n\n', A)
        # print('\n\nA0inv:\n\n', A0inv)
        ####
        FX1 = evaluarFX(Xs, X1, eqs)

        for i in range(maxIter):

            # print(f'\n\n------------------------------\nITERACIÓN NÚMERO {i}\n--------------------------')

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
            # A1 = A0 +( (y - np.matmul(A0, s))/ (np.linalg.norm(s))**2 ) * st

            # print('\n\nFX0: \n\n', FX0)

            # print('\n\nX0:\n\n', X0)
            # print('\n\nX1:\n\n', X1)
            # print('\n\nFX0\n\n', FX0)
            # print('\n\nFX1\n\n', FX1)

            # print('\n\ns:\n\n', s)
            # print('\n\ny:\n\n', y)
            # # print('\n\nJacobiana OG\n\n', A)
            # print('\n\nA0inv:\n\n', A0inv)
            # # print('\n\nA1inv:\n\n', A1inv)

            # return st, A0inv, y
            a = np.matmul(A0inv, y)
            # # print('\n\na1:\n\n', a)
            a = s - a
            # print('\n\na2:\n\n', a)
            b = np.matmul(a, st)
            # print('\n\nb:\n\n', b)
            c = np.matmul(b, A0inv)
            # print('\n\nc:\n\n', c)
            d = np.matmul(st, A0inv)
            # print('\n\nd:\n\n', d)
            e = np.matmul(d, y)
            # print('\n\ne:\n\n', e)
            A1inv = copy(A0inv) + c/e[0]

            # print('\n\nX0 vector: \n\n', X0)
            # print('\n\nX0 flatten: \n\n', self.flatten(X0))
            Z = np.matmul(copy(A1inv), FX1)
            X2 = X1 - Z

            # print('\n\nA1inv:\n\n', A1inv)

            # print('\n\nZ:\n\n', Z)
            # print('\n\nX2:\n\n', X2)

            if np.linalg.norm(X2-X1) < error:
                print(f'\nResultado alcanzado en {i} iteraciones')
                print('\nsolución encontrada:\n')
                self.printSolucion(self.flatten(X2))
                return X2

            flatX2 = self.flatten(X2)

            # A0 = A1
            A0inv = copy(A1inv)
            X0 = flatX1
            X1 = flatX2
            #FX0 = evaluarFX(Xs, flatX1, eqs)
            FX0 = flatFX1
            FX1 = evaluarFX(Xs, flatX2, eqs)

        print('Límite de iteraciones alcanzado. Valores aproximados:')
        self.printSolucion(X1)


def makeSymbolics(num):
    return [symbols(f'x{i}') for i in range(num)]


def sysEquations(num):
    eqs = []
    # for i in range(num):
    #     eqs.append(sympify(input(f'ingrese la ecuacion {i}:\n')))
    # eqs.append(sympify('x0**2+x0*x1-10'))
    # eqs.append(sympify('x1 + 3*x0*x1**2 - 57'))
    eqs.append(sympify('x0**2+x1**2-13'))
    eqs.append(sympify('x0-x1 -1'))
    return eqs


# Main
# num = int(input('Ingese el número de incógnitas/ecuaciones: '))
num = 2
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
# A0inv, s, y, st = NM.Broyden(num, eqs, X)
NM.Broyden(num, eqs, X)
