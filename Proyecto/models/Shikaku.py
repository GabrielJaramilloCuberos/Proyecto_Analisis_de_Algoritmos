from Proyecto.models.rectangulo import Rectangulo


class Shikaku:
    def __init__(self, matriz):
        self.matriz = matriz
        self.rectangulos = []
        """
        A modo de comentario, en la teoria toca tener cuidado y
        revisar que el contenido del arreglo de rectangulos sea
        de la clase Rectangulo, no insertarle nada mas

         
        """
    
    def validarRectangulo(self, filaInicio, filaFinal, columnaInicio, columnaFinal):
        filaMin = min(filaInicio, filaFinal)
        filaMax = max(filaInicio, filaFinal)
        colMin = min(columnaInicio, columnaFinal)
        colMax = max(columnaInicio, columnaFinal)

        totalFilas = len(self.matriz)
        if totalFilas == 0:
            return False
        totalColumnas = len(self.matriz[0])

        if filaMin < 0 or colMin < 0:
            return False
        if filaMax >= totalFilas or colMax >= totalColumnas:
            return False

        for rectangulo in self.rectangulos:
            seSolapan = not (
                filaMax < rectangulo.filaInicio
                or filaMin > rectangulo.filaFinal
                or colMax < rectangulo.columnaInicio
                or colMin > rectangulo.columnaFinal
            )
            if seSolapan:
                return False

        area = (filaMax - filaMin + 1) * (colMax - colMin + 1)
        cantidadNumeros = 0
        numeroObjetivo = None

        for fila in range(filaMin, filaMax + 1):
            for columna in range(colMin, colMax + 1):
                valor = self.matriz[fila][columna]
                if valor != 0:
                    cantidadNumeros += 1
                    numeroObjetivo = valor
                    if cantidadNumeros > 1:
                        return False

        if cantidadNumeros != 1:
            return False

        return numeroObjetivo == area

    
    def crearRectangulo(self, rectangulo):
        if(isinstance(rectangulo,Rectangulo)):
            self.rectangulos.append(rectangulo)

    def eliminarRectangulo(self, filaInicio, filaFinal, columnaInicio, columnaFinal):
        filaMin = min(filaInicio, filaFinal)
        filaMax = max(filaInicio, filaFinal)
        colMin = min(columnaInicio, columnaFinal)
        colMax = max(columnaInicio, columnaFinal)

        for indice, rectangulo in enumerate(self.rectangulos):
            if (
                rectangulo.filaInicio == filaMin
                and rectangulo.filaFinal == filaMax
                and rectangulo.columnaInicio == colMin
                and rectangulo.columnaFinal == colMax
            ):
                self.rectangulos.pop(indice)
                return True

        return False

    def tableroCompleto(self):
        if not self.matriz:
            return False

        totalFilas = len(self.matriz)
        totalColumnas = len(self.matriz[0])
        areaTotalTablero = totalFilas * totalColumnas

        areaRectangulos = 0
        for rectangulo in self.rectangulos:
            areaRectangulos += (
                (rectangulo.filaFinal - rectangulo.filaInicio + 1)
                * (rectangulo.columnaFinal - rectangulo.columnaInicio + 1)
            )

        return areaRectangulos == areaTotalTablero