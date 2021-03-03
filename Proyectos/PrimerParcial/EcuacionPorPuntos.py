import numpy as np
from sympy import symbols
from Gauss import Gauss

x = symbols('x')

class PuntosToEcuacion:

    '''
    Crea una Polinomio a partir de puntos
    '''

    def __init__(self):
        self.puntos = []
        self.matriz = 0
        self.ecuacion = 0

    def Puntos(self):
        numDots = int(input('Cuantos puntos vas a ingresar?\n'))
        for i in range(numDots):
            self.puntos.append((float(input('x = ')),float(input('y = '))))

    def CrearMatriz(self):
        numRows = len(self.puntos)
        matriz = []
        for i in range(numRows):
            row = []
            row.append(self.puntos[i][1])
            row.append(1)
            for j in range(numRows - 1):
                expr = x**(j+1)
                row.append(expr.subs(x, self.puntos[i][0]))
            matriz.append(row)

        matriz = np.flip(np.array(matriz, dtype=float),1)
        self.matriz = matriz
        print(self.matriz)

    def ObtenerEcuacion(self):
        GJ = Gauss()
        resultados = GJ.solucion(self.matriz)
        resultados =resultados[::-1]
        for i in range(len(resultados)):
            self.ecuacion += resultados[i]*x**(i)


Puntos = PuntosToEcuacion()
Puntos.Puntos()
Puntos.CrearMatriz()
Puntos.ObtenerEcuacion()
print(Puntos.ecuacion)