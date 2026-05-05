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

    def generarDominios(self):
        totalFilas = len(self.matriz)
        totalColumnas = len(self.matriz[0]) if totalFilas > 0 else 0
        dominios = []

        for fila in range(totalFilas):
            for columna in range(totalColumnas):
                valor = self.matriz[fila][columna]
                if valor != 0:
                    opcionesValidas = []
                    for alto in range(1, valor + 1):
                        if valor % alto != 0:
                            continue

                        ancho = valor // alto
                        filaMin = max(0, fila - alto + 1)
                        filaMax = min(totalFilas - alto + 1, fila + 1)
                        colMin = max(0, columna - ancho + 1)
                        colMax = min(totalColumnas - ancho + 1, columna + 1)

                        for filaInicial in range(filaMin, filaMax):
                            for colInicial in range(colMin, colMax):
                                valido = True
                                for r in range(filaInicial, filaInicial + alto):
                                    for c in range(colInicial, colInicial + ancho):
                                        if self.matriz[r][c] != 0 and (r != fila or c != columna):
                                            valido = False
                                            break
                                    if not valido:
                                        break

                                if valido:
                                    opcionesValidas.append(
                                        Rectangulo(
                                            filaInicial,
                                            filaInicial + alto - 1,
                                            colInicial,
                                            colInicial + ancho - 1,
                                        )
                                    )

                    dominios.append(
                        {
                            "id": f"Num_{valor}_en_{fila}_{columna}",
                            "opciones": opcionesValidas,
                        }
                    )

        return dominios

    def solapan(self, rectanguloUno, rectanguloDos):
        return not (
            rectanguloUno.filaFinal < rectanguloDos.filaInicio
            or rectanguloUno.filaInicio > rectanguloDos.filaFinal
            or rectanguloUno.columnaFinal < rectanguloDos.columnaInicio
            or rectanguloUno.columnaInicio > rectanguloDos.columnaFinal
        )

    def solucionador(self):
        dominios = self.generarDominios()

        def backtracking(restantes, colocados):
            if not restantes:
                return colocados

            restantes = sorted(restantes, key=lambda var: len(var["opciones"]))
            actual = restantes[0]

            for candidato in actual["opciones"]:
                nuevosDominios = []
                ramaMuerta = False

                for otroCandidato in restantes[1:]:
                    filtradas = []
                    for opcion in otroCandidato["opciones"]:
                        if not self.solapan(candidato, opcion):
                            filtradas.append(opcion)

                    if len(filtradas) == 0:
                        ramaMuerta = True
                        break

                    nuevosDominios.append(
                        {
                            "id": otroCandidato["id"],
                            "opciones": filtradas,
                        }
                    )

                if ramaMuerta:
                    continue

                solucion = backtracking(nuevosDominios, colocados + [candidato])
                if solucion is not None:
                    return solucion

            return None

        return backtracking(dominios, [])