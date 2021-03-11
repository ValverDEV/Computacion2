from sympy import symbols, sympify, diff, lambdify
from copy import copy
import numpy as np
from time import time

x = symbols('x')


class RaicesMN:

    def Biseccion(self, bot, sup, expr, maxIter=1000):
        """
        Implementacion del metodo de biseccion para calcular
        raíces de función.
        Recibe limite inferior y superior, y la expresión.
        Opcionalmente recibe el número máximo de iteraciones.
        """
        print('método de bisección')
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
        print('método exhaustivo')
        a = np.arange(inf, sup, 0.001)
        f = lambdify(x, expr, 'numpy')
        b = f(a)

        raizX = []
        raizY = []

        for i in range(0, len(b)):
            if round(b[i], 2) == 0:
                raizX.append(a[i])
                raizY.append(b[i])
        if raizX:
            print('Se estimaron los siguientes valores como posibles raíces:')
            for i in raizX:
                print(i)
        else:
            print('No se encontraron raíces')

    def Newton(self, x0, expr, error=0.001, maxIter=100):
        '''
        (opcional) error:
            valor mínimo de error para que se pueda considerar 
            a un número como raíz, considerando el error absoluto
            |x_i+1-x_i|
        (opcional) maxIter:
            número máximo de iteraciones
        '''
        print('método de Newton')
        dexpr = diff(expr, x)
        for i in range(maxIter):
            x1 = x0 - (expr.subs(x, x0) / dexpr.subs(x, x0))
            if abs(x1-x0) < error:
                print('raíz encontrada: ', x1)
                return x1
            else:
                x0 = x1
        print('no se encontró una raíz')
        print('se aproximó el siguiente valor:\n', x1)
        return x1

    def Secante(self, x0, expr, error=0.001, maxIter=100):
        '''
        (opcional) error:
            valor mínimo de error para que se pueda considerar 
            a un número como raíz, considerando el error absoluto
            |x_i+1-x_i|
        (opcional) maxIter:
            número máximo de iteraciones
        '''
        print('método de la secante')
        xp = x0 - 1
        for i in range(maxIter):
            f_x0 = expr.subs(x, x0)
            f_xp = expr.subs(x, xp)
            x1 = x0 - (f_x0 * (copy(x0) - copy(xp)))/(f_x0-f_xp)
            if abs(x1-x0) < error:
                print('raiz encontrada: ', x1)
                return x1
            else:
                xp = x0
                x0 = x1

        print('no se econtró un raíz')
        print('se aproximó el siguiente valor:\n', x1)
        return x1

    def swap(self, a, b, fa, fb):
        return b, a, fb, fa

    def Hibrido(self, a, b, expr, error=0.001, maxIter=100):
        print('método de Brent-Decker')
        fa = expr.subs(x, a)
        fb = expr.subs(x, b)
        if fa*fb >= 0:
            print('No se puede encontrar una raíz en este intervalo')
            return False

        if abs(fa) < abs(fb):
            a, b, fa, fb = self.swap(a, b, fa, fb)

        c = a
        fc = fa

        mflag = True
        s = False

        for i in range(maxIter):

            if abs(b - a) < error:
                print('se encontró la siguiente raíz: ', b)
                return b
            elif fb == 0:
                print('se encontró la siguiente raíz: ', b)
                return b
            elif s:
                if expr.subs(x, s) == 0:
                    print('se encontró la siguiente raíz: ', s)
                    return s

            if fa != fc and fb != fc:
                s = a*fb*fc / ((fa - fb)*(fa - fc)) + b*fa*fc / \
                    ((fb - fa)*(fb - fc)) + c*fa*fb / ((fc - fa) * (fc - fb))

            else:
                s = b - fb * (b-a) / (fb-fa)

            if (not((3*a+b)/4 <= s and s <= b)) or (mflag and abs(s-b) >= abs(b-c)/2) or (not mflag and abs(s-b) >= (c-d)/2) or (mflag and abs(b-c) < abs(error)) or (not mflag and abs(c-d) < abs(error)):
                s = (a+b) / 2
                mflag = True
            else:
                mflag = False

            fs = expr.subs(x, s)
            d = c
            c = b

            if fa*fs < 0:
                b = s
                fb = expr.subs(x, b)
            else:
                a = s
                fa = expr.subs(x, a)

            if abs(fa) < abs(fb):
                a, b, fa, fb = self.swap(a, b, fa, fb)

        print('limite alcanzado de iteraciones')
        print('se encontró la siguiente raíz: ', b)
        return b


MN = RaicesMN()
expr = sympify(input('ingrese la funcíon a evaluar: '))
inf = float(input('ingrese un límite inferior: '))
sup = float(input('ingrese un límiter superior: '))

t = time()
MN.exhaustivo(inf, sup, expr)
print(f'el tiempo de ejecución del método exhaustivo fue {time()- t}\n')
t = time()
MN.Biseccion(inf, sup, expr)
print(f'el tiempo de ejecución del método bisección fue {time()- t}\n')
t = time()
MN.Newton(inf, expr)
print(f'el tiempo de ejecución del método Newton fue {time()- t}\n')
t = time()
MN.Secante(inf, expr)
print(f'el tiempo de ejecución del método de la secante fue {time()- t}\n')
t = time()
MN.Hibrido(inf, sup, expr)
print(f'el tiempo de ejecución del método de Brent-Decker fue {time()- t}\n')
