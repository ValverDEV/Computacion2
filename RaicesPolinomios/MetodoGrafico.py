import numpy as np
from sympy import symbols, sympify, lambdify
import matplotlib.pyplot as plt

x = symbols('x')

class Grafico:

    def metodoGrafico(self, expr, inf, sup):
        a = np.arange(inf,sup, 0.001)
        f = lambdify(x, expr, 'numpy')
        b = f(a)

        raizX = []
        raizY = []

        for i in range(0,len(b)):
            if round(b[i], 1) == 0:
                raizX.append(a[i])
                raizY.append(b[i])

        plt.plot(a,b)
        plt.scatter(raizX, raizY)
        plt.show()

def crearExpresion():
    return sympify(input('Ingresa la expresión: '))

expr = crearExpresion()
Grafico().metodoGrafico(expr, float(input('límite inferior: ')), float(input('límite superior: ')))