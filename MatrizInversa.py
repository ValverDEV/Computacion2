import numpy as np
from random import randint


def matrizAleatoria():
    
    """
    Genear una matriz cuadrada aleatoria.
    """

    dim = int(input('Dimensiones de la matriz cuadrada aleatoria: '))
    return np.array([[randint(0,9) for i in range(0,dim)] for i in range(0,dim)], dtype=float)

def crearMatriz():

    """
    Crear matriz cuadrada por el usuaria
    """

    dim = int(input('Dimensiones de la matriz cuadrada: '))
    matriz = [[0 for i in range(0,dim)] for i in range(0,dim)]
    for i in range(0,len(matriz)):
        for j in range(0,len(matriz)):
            matriz[i][j] = float(input(f'x[{i+1}][{j+1}] = '))
    return np.array(matriz, dtype=float)


class Gauss:

    def cambiarFilas(self, matriz, fila):
        
        """
        Busca una fila válida para intercambiar (si existe)
        """

        cambio = 0
        for i in range(1, len(matriz) - fila):
            if matriz[fila + i][fila] != 0:
                cambio = i
                break
        
        if not cambio:
            return False
            
        fila1 = fila
        fila2 = fila + cambio

        temp = matriz[fila1].copy()
        matriz[fila1] = matriz[fila2]
        matriz[fila2] = temp
        return matriz

    def sumarFilas(self, matriz, fila):

        """
        Suma para reducir todas los números debajo
        """

        for i in range(1, len(matriz) -  fila):
            reduccion = matriz[fila][fila].copy()
            multiplo = -1*matriz[fila+i][fila].copy()
            matriz[fila + i] = matriz[fila+i] + matriz[fila] * multiplo / reduccion
        return matriz

    def checarCeros(self, matriz, fila):

        """
        Verifica que no haya únicamente 0s en la columna
        """

        if matriz[fila][fila] == 0:
            return True
        return False

    def transformar(self, matriz):
        """
        Invierte la matriz vertical y horizontalmente
        """
        copia = matriz.copy()
        finalInv = matriz.copy()
        for i in range(0,len(matriz)):
            finalInv[i] = copia[-1+-i]
        a = np.hsplit(finalInv, 2)[0]
        aCopia = a.copy()
        b = np.hsplit(finalInv, 2)[1]
        bCopia = b.copy()
        for i in range(0,len(a)):
            for j in range(0,len(a[0])):
                a[i][j] = aCopia[i][-1-j]
                b[i][j] = bCopia[i][-1-j]
        finalInv = np.concatenate((a,b), axis=1)
        return finalInv

    def Gauss(self, matriz):

        """
        Aplica el método de Gauss verificando que tenga solución
        """

        for fila in range(0,len(matriz)):
            if self.checarCeros(matriz, fila):
                matriz = self.cambiarFilas(matriz, fila)
                if not np.any(matriz):
                    return False
            self.sumarFilas(matriz, fila)
        return matriz

    def unos(self, matriz):

        """
        Simplifica la filas para que queden 1s en la diagonal
        """

        for i in range(0,len(matriz)):
            matriz[i] /= matriz[i][i]
        return matriz


    def inversa(self, matriz):

        """
        Método para calcular la inversa de una matriz
        """

        matriz = np.concatenate((matriz, np.identity(len(matriz))), axis=1)
        matriz = self.Gauss(matriz)
        if not np.any(matriz):
            print("La matriz no tiene solución")
            return False
        matriz = self.transformar(matriz)
        matriz = self.Gauss(matriz)
        matriz = self.transformar(matriz)
        matriz = self.unos(matriz)
        return np.hsplit(matriz, 2)[1]


while True:
    print('Resolver Matriz aleatoria (0) o ingresar una(1)?')
    x = input()
    if x == '0':
        M = matrizAleatoria()
        break
    elif x == '1':
        M = crearMatriz()
        break

print("La matriz ingresada es:")
print(M)
print("La matriz inversa es:")
print(Gauss().inversa(M))