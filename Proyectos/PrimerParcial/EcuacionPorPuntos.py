import numpy as np
from sympy import symbols, lambdify, init_printing, sympify
from Gauss import Gauss
import matplotlib.pyplot as plt

init_printing()
x = symbols('x')

class PuntosToEcuacion:

    '''
    Crea una Polinomio a partir de puntos
    '''

    def __init__(self):
        self.puntosX= []
        self.puntosY= []
        self.matriz = 0
        self.ecuacion = ''

    def Puntos(self):
        numDots = int(input('Cuantos puntos vas a ingresar?\n'))
        for i in range(numDots):
            self.puntosX.append(float(input('x = ')))
            self.puntosY.append(float(input('y = ')))

    def CrearMatriz(self):
        numRows = len(self.puntosX)
        matriz = []
        for i in range(numRows):
            row = []
            row.append(self.puntosY[i])
            row.append(1)
            for j in range(numRows - 1):
                expr = x**(j+1)
                row.append(expr.subs(x, self.puntosX[i]))
            matriz.append(row)

        matriz = np.flip(np.array(matriz, dtype=float),1)
        self.matriz = matriz
        print(self.matriz)

    def ObtenerEcuacion(self):
        GJ = Gauss()
        resultados = GJ.solucion(self.matriz)
        resultados =resultados[::-1]
        for i in range(len(resultados)):
            self.ecuacion += str(resultados[i]*x**(i))
            print(self.ecuacion)

    def CearGrafica(self):
        a = np.linspace(min(self.puntosX), max(self.puntosX), 100)
        expr = sympify(self.ecuacion)
        f = lambdify(x, expr, 'numpy')
        b = f(a)
        plt.plot(a,b)
        plt.scatter(self.puntosX, self.puntosY)
        plt.show()



Puntos = PuntosToEcuacion()
Puntos.Puntos()
Puntos.CrearMatriz()
Puntos.ObtenerEcuacion()
print(Puntos.ecuacion)
Puntos.CearGrafica()