# Practica Regesion Lineal
# Mario Valverde, Daniela Jiménez

from sympy import symbols, lambdify
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

X = symbols('x')


class NumMethods:

    def __init__(self, Xs, Ys):
        self.puntosX = Xs
        self.puntosY = Ys

    def linear(self):
        x = self.puntosX
        y = self.puntosY

        n = len(x)
        x_avg = sum(x)/n
        y_avg = sum(y)/n

        x_sum = sum(x)
        xsquared_sum = sum([i**2 for i in x])
        y_sum = sum(y)

        xy_sum = sum([x[i]*y[i] for i in range(n)])

        a1 = (n*xy_sum - x_sum*y_sum)/(n*xsquared_sum - x_sum**2)
        a0 = y_avg - a1*x_avg

        expr = a0 + a1*X

        print(expr)
        self.expr = expr
        return expr

    def grafica(self):
        a = np.arange(min(self.puntosX), max(self.puntosX), 0.1)
        f = lambdify(X, self.expr, "numpy")
        b = f(a)
        plt.plot(a, b, color='b')
        plt.scatter(self.puntosX, self.puntosY, color='g')
        plt.show()

    def polinomial(self, deg):
        x = self.puntosX
        y = self.puntosY

        deg += 1

        n = len(x)

        x_sums = [n]
        xy_sums = [sum(y)]

        for i in range(deg*deg):
            x_sums.append(sum([j**(i+1) for j in x]))

        for i in range(deg):
            xy_sums.append(sum([y[j]*x[j]**(i+1) for j in range(n)]))

        matrix = np.zeros((deg, deg))

        matrixY = np.zeros((deg, 1))

        for row in range(deg):
            for col in range(deg):
                matrix[row][col] = x_sums[col+row]

            matrixY[row] = xy_sums[row]

        coeficientes = np.linalg.solve(matrix, matrixY).tolist()

        expr = 0

        for i in range(len(coeficientes)):
            ai = coeficientes[i][0]
            expr += ai*X**i

        print('\n\n', expr)

        self.expr = expr
        return expr

    def error(self):
        expr = self.expr
        x = self.puntosX
        y = self.puntosY
        n = len(x)
        error = 0
        for i in range(n):
            error += (y[i] - expr.subs(X, x[i]))**2

        error = error/n

        # print(f'\n\nError cuadrático medio: {error}')

        return error


def main():
    dataset = pd.read_csv(
        'https://gist.githubusercontent.com/seankross/a412dfbd88b3db70b74b/raw/5f23f993cd87c283ce766e7ac6b329ee7cc2e1d1/mtcars.csv')

    print('Trabajando con el set de datos "mtcars", con el rendimiento mpg vs el desplazamiento disp.')

    x = dataset['disp'].tolist()
    y = dataset['mpg'].tolist()

    degs = [1, 2, 4, 6, 8]

    NM = NumMethods(x, y)

    for deg in degs:
        print(f'\n\nSe está calculando un regresión de grado {deg}')
        print('\n\nPolinomio Calculado:')
        NM.polinomial(deg)
        NM.error()
        NM.grafica()

    return

# def main():
#     x = [0, 1, 2, 3, 4, 5]
#     y = [2.1, 7.7, 13.6, 27.2, 40.9, 61.1]

#     deg = int(input('grado: '))

#     NM = NumMethods(x, y)
#     NM.polinomial(deg)
#     NM.grafica()
#     NM.error()


if __name__ == '__main__':
    main()
