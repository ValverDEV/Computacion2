import numpy as np
from sympy import symbols
from random import randint


class Gauss:

    def cambiarFilas(self, matriz, fila):
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
        for i in range(1, len(matriz) -  fila):
            reduccion = matriz[fila][fila].copy()
            multiplo = -1*matriz[fila+i][fila].copy()
            matriz[fila + i] = matriz[fila+i] + matriz[fila] * multiplo / reduccion
        return matriz

    def checarCeros(self, matriz, fila):
        if matriz[fila][fila] == 0:
            return True
        return False

    def transformar(self, matriz):
        copia = matriz.copy()
        finalInv = matriz.copy()
        for i in range(0,len(matriz)):
            for j in range(0,len(matriz[0]) - 1):
                finalInv[i][j] = copia[i][-2-j]
        copia = finalInv.copy()
        for i in range(0,len(matriz)):
            finalInv[i] = copia[-1+-i]
        return finalInv

    def checarDim(self, matriz):
        filas = len(matriz)
        columnas = len(matriz[0])
        if filas < columnas - 1 or filas > columnas - 1:
            return False
        return True


    def Gauss(self, matriz):
        for fila in range(0,len(matriz)):
            if self.checarCeros(matriz, fila):
                matriz = self.cambiarFilas(matriz, fila)
                if not np.any(matriz):
                    return False
            self.sumarFilas(matriz, fila)
        return matriz



    def solucion(self, matriz):
        if not self.checarDim(matriz):
            print("La matriz no tiene solución")
            return False
        matriz = self.Gauss(matriz)
        if not np.any(matriz):
            print("La matriz no tiene solución")
            return False
        matriz = self.transformar(matriz)
        matriz = self.Gauss(matriz)
        matriz = self.transformar(matriz)
        resultados = []
        for i in range(0,len(matriz)):
            resultados.append(matriz[i][-1]/matriz[i][i])
        for i in range(0,len(resultados)):
            print(f"x{i} = {resultados[i]}")
        return matriz


def matrizAleatoria():
    filas = randint(1,6)
    columnas = randint(2,6)
    M = [[randint(0,9) for i in range(0,columnas)] for i in range(0,filas)]
    M = np.array(M, dtype=float)
    return M


def crearMatriz():
    filas = int(input("numero de filas: "))
    columnas = int(input("numero de columnas: "))
    matriz = []
    for i in range(0,filas):
        fila = []
        for j in range(0,columnas):
            fila.append(input(f"elemento x[{i}][{j}]: "))
        matriz.append(fila)
    return np.array(matriz, dtype=float)


M = crearMatriz()


Gauss().solucion(M)


