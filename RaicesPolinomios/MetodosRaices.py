from sympy import symbols, sympify, diff
from copy import copy

x = symbols('x')

class RaicesMN:

    def Newton(self, error = 0.001, maxIter = 100):
        '''
        (opcional) error:
            valor mínimo de error para que se pueda considerar 
            a un número como raíz, considerando el error absoluto
            |x_i+1-x_i|
        (opcional) maxIter:
            número máximo de iteraciones
        '''
        expr = sympify(input('ingrese la función:\n'))
        x0 = float(input('infrese un valor de x inicial:\n'))
        dexpr = diff(expr, x)
        for i in range(maxIter):
            x1 = x0 - (expr.subs(x, x0)/ dexpr.subs(x, x0))
            if abs(x1-x0) < error:
                print('raíz encontrada: ', x1)
                return x1
            else:
                x0 = x1
        print('no se encontró una raíz')
        print('se aproximó el siguiente valor:\n', x1)
        return x1


    def Secante(self, error = 0.001, maxIter = 100):
        '''
        (opcional) error:
            valor mínimo de error para que se pueda considerar 
            a un número como raíz, considerando el error absoluto
            |x_i+1-x_i|
        (opcional) maxIter:
            número máximo de iteraciones
        '''
        expr = sympify(input('ingrese la función:\n'))
        x0 = float(input('infrese un valor de x inicial:\n'))
        xp = x0 - 1
        for i in range(maxIter):
            f_x0 = expr.subs(x, x0)
            f_xp = expr.subs(x, xp)
            x1 = x0 - (f_x0 *(copy(x0) - copy(xp)))/(f_x0-f_xp)
            print(x1)
            if abs(x1-x0) < error:
                print('raiz encontrada: ', x1)
                return x1
            else:
                xp = x0
                x0 = x1

        print('no se econtró un raíz')
        print('se aproximó el siguiente valor:\n', x1)
        return x1


MN = RaicesMN()
# MN.Newton()
MN.Secante()