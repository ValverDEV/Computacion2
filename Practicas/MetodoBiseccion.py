import numpy as np 
from sympy import symbols, sympify

x = symbols('x')

class Biseccion:

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


def crearExpresion():
    expr = sympify(input('ingresa la función: '))
    return expr



expr = crearExpresion()
Biseccion().Biseccion(float(input('límite inferior: ')), float(input('límite superior: ')), expr)