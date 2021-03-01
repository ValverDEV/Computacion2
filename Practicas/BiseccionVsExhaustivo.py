import numpy as np 
from sympy import symbols, sympify, lambdify
from time import time

x = symbols('x')

class Raices:

    def Biseccion(self, bot, sup, expr, maxIter = 1000):
        """
        Implementacion del metodo de biseccion para calcular
        raíces de función.
        Recibe limite inferior y superior, y la expresión.
        Opcionalmente recibe el número máximo de iteraciones.
        """
        print(expr)
        if expr.subs(x, bot)*expr.subs(x, sup) > 0:
            print('el intervalo ingresado no permite encontrar una solucion')
            return

        for i in range(maxIter):
            x_r = (bot + sup)/2
            f_x_i = expr.subs(x, bot)
            f_x_r = expr.subs(x, x_r)
            if round(f_x_i * f_x_r, 3) == 0:
                print(f'{x_r} es una raíz')
                return x_r
            elif f_x_i * f_x_r > 0:
                bot = x_r
            else:
                sup = x_r
        
        print('límite de iteraciones alcanzado')        
        print(f'se estimó la siguiente raíz: {x_r}')
        return x_r


    def exhaustivo(self, inf, sup, expr):
        a = np.arange(inf,sup, 0.001)
        f = lambdify(x, expr, 'numpy')
        b = f(a)

        raizX = []
        raizY = []

        for i in range(0,len(b)):
            if round(b[i], 2) == 0:
                raizX.append(a[i])
                raizY.append(b[i])
        if raizX:
            print('Se estimaron los siguientes valores como posibles raíces:')
            for i in raizX:
                print(i)
        else:
            print('No se encontraron raíces')

def crearExpresion():
    expr = sympify(input('ingresa la función: '))
    return expr



expr = crearExpresion()
inferior = float(input('límite inferior: '))
superior = float(input('límite superior: '))
t0 = time()
calc = Raices()
print('Por método de bisección:')
calc.Biseccion(inferior, superior, expr)
print(f'Tiempo de ejecución del método de bisección: {time() - t0}')
t0 = time()
print('Por método exhaustivo:')
calc.exhaustivo(inferior, superior, expr)
print(f'Tiempo de ejecución del método exhaustivo: {time()- t0}')