import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from sympy.utilities.lambdify import lambdify
from Regresiones import NumMethods
from sympy import symbols
from pprint import pprint
x = symbols('x')


class Autopylot:

    def pylot(self):
        img_num = 0
        # rango de datos que servirá para las gráficas
        a = np.arange(20, 80, 1)
        # listas con trayectoria y control total
        total_tray = []
        total_control = []

        while True:
            try:  # lectura de la imagen
                img = mpimg.imread(f'road{img_num}.png')
            except:
                print("FIN DEL CAMINO")
                break

            n = len(img)  # pixeles de la imagen (debe ser cuadrada)

            # identificación de los puntos de los bordes del camino
            # y transformación en horizontal
            Xs = []
            Ys = []
            matriz = np.zeros((n, n))
            for row in range(99, -1, -1):
                for col in range(99, -1, -1):
                    if img[row][col][0] > 0:
                        matriz[row][col] = 1
                        print(row, col)
                        Xs.append(100-row)
                        Ys.append(100-col)

            # separamos los bordes del camino en conjuntos de puntos diferentes
            X1, Y1, X2, Y2 = self.split_lines(Xs, Ys)

            # interpolaciones
            NM1 = NumMethods(X1, Y1)
            pol1 = NM1.polinomial(2)  # 2 por 2o grado
            NM2 = NumMethods(X2, Y2)
            pol2 = NM2.polinomial(2)

            # la trayectoria es el promedio de ambos puntos: aprox la mitad
            trayectoria = (pol1+pol2)/2

            # el control en este intervalo es su derivada
            control = trayectoria.diff(x)

            # evaluamos las posiciones para ver donde se encontrará el auto
            f_tray = lambdify(x, trayectoria, 'numpy')
            f_pol1 = lambdify(x, pol1, 'numpy')
            f_pol2 = lambdify(x, pol2, 'numpy')
            f_control = lambdify(x, control, 'numpy')

            b_tray = f_tray(a).tolist()
            b_pol1 = f_pol1(a)
            b_pol2 = f_pol2(a)
            b_control = f_control(a).tolist()

            # creamos la gráfica
            plt.scatter(Xs, Ys)
            plt.plot(a, b_tray, color='r')
            plt.plot(a, b_pol1, color='b')
            plt.plot(a, b_pol2, color='b')
            plt.title(f'Trayectoria intervalo {img_num}')
            plt.show()

            # grafica del control
            plt.plot(a, b_control)
            plt.title(f'Control intervalo {img_num}')
            plt.show()

            # agregamos el trayecto al total
            for i in range(len(b_tray)):
                total_tray.append(b_tray[i])
                total_control.append(b_control[i])

            # imprimimos los valores del trayecto
            print('\nTrayectoria predicha en el intervalo:')
            pprint(b_tray)

            print('\nControl en el intervalo:')
            pprint(b_control)

            # pasamos a la siguientes imagen
            img_num += 1

        # Graficamos la trayectoria y control total
        c = list(range(len(total_tray)))
        plt.scatter(c, total_tray)
        plt.plot(c, total_tray)
        plt.title('Trayectoria')
        plt.show()

        plt.scatter(c, total_control)
        plt.plot(c, total_control)
        plt.title('Control')
        plt.show()

        print('\nLa trayectoria total fue:')
        pprint(total_tray)
        print('\nEl control total fue:')
        pprint(total_control)

    def split_lines(self, Xs, Ys):
        dist = 20  # distancia entre puntos
        # definición de listas para caminos separados
        Xs1 = []
        Ys1 = []

        Xs2 = [Xs[0]]
        Ys2 = [Ys[0]]

        # encontrar puntos iniciales del segundo borde
        for i in range(1, len(Xs)):
            if not(abs(Xs2[-1] - Xs[i]) <= dist and abs(Ys2[-1] - Ys[i]) <= dist):
                Xs1.append(Xs[i])
                Ys1.append(Ys[i])
                break

        # separamos los bordes en listas diferentes
        for i in range(1, len(Xs)):
            if abs(Xs2[-1] - Xs[i]) <= dist and abs(Ys2[-1] - Ys[i]) <= dist:
                Xs2.append(Xs[i])
                Ys2.append(Ys[i])
            else:
                Xs1.append(Xs[i])
                Ys1.append(Ys[i])

        return Xs1, Ys1, Xs2, Ys2


def main():
    Pylot = Autopylot()
    Pylot.pylot()


if __name__ == '__main__':
    main()
