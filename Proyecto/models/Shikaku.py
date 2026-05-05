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


    #Este no se usa, ahora se va a usar el ExactCover para que sea mas eficiente
    # Igual es que es un NP asi que eficiente eficiente tampoco sera  :/
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
                                    nuevoRectangulo = Rectangulo(
                                        filaInicial,
                                        filaInicial + alto - 1,
                                        colInicial,
                                        colInicial + ancho - 1,
                                    )

                                    nuevoRectangulo.calcularMascara(totalColumnas)
                                    opcionesValidas.append(nuevoRectangulo)

                    dominios.append(
                        {
                            "id": f"Num_{valor}_en_{fila}_{columna}",
                            "opciones": opcionesValidas,
                        }
                    )

        return dominios

    def generarOpcionesExactCover(self):
        totalFilas = len(self.matriz)
        totalColumnas = len(self.matriz[0]) if totalFilas > 0 else 0
        totalCeldas = totalFilas * totalColumnas
        
        todasLasOpciones = []
        idPistaActual = 0

        for fila in range(totalFilas):
            for columna in range(totalColumnas):
                valor = self.matriz[fila][columna]
                if valor != 0:
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
                                # Validación de encierro
                                valido = True
                                for r in range(filaInicial, filaInicial + alto):
                                    for c in range(colInicial, colInicial + ancho):
                                        if self.matriz[r][c] != 0 and (r != fila or c != columna):
                                            valido = False
                                            break
                                    if not valido:
                                        break

                                if valido:
                                    # Creado con el idPistaActual
                                    nuevoRectangulo = Rectangulo(
                                        filaInicial,
                                        filaInicial + alto - 1,
                                        colInicial,
                                        colInicial + ancho - 1,
                                        idPistaActual
                                    )
                                    nuevoRectangulo.calcularMascara(totalColumnas, totalCeldas)
                                    todasLasOpciones.append(nuevoRectangulo)

                    idPistaActual += 1

        return todasLasOpciones, idPistaActual

    def solapan(self, rectanguloUno, rectanguloDos):
        return (rectanguloUno.mascara & rectanguloDos.mascara) != 0

    def solucionador(self):
        opcionesRestantes, totalPistas = self.generarOpcionesExactCover()
        
        totalFilas = len(self.matriz)
        totalColumnas = len(self.matriz[0]) if totalFilas > 0 else 0
        totalCeldas = totalFilas * totalColumnas

        objetivoFinal = (1 << (totalCeldas + totalPistas)) - 1

        def algoritmoX(estadoActual, opciones):
            if estadoActual == objetivoFinal:
                return []
                
            bitsFaltantes = ~estadoActual & objetivoFinal
            bitMasBajoFaltante = (bitsFaltantes & -bitsFaltantes).bit_length() - 1
            
            candidatos = [op for op in opciones if (op.mascara & (1 << bitMasBajoFaltante)) != 0]
            
            if not candidatos:
                return None
                
            for candidato in candidatos:
                if (estadoActual & candidato.mascara) == 0:
                    nuevoEstado = estadoActual | candidato.mascara
                    
                    nuevasOpciones = [op for op in opciones if (op.mascara & candidato.mascara) == 0]
                    
                    resultado = algoritmoX(nuevoEstado, nuevasOpciones)
                    if resultado is not None:
                        return [candidato] + resultado
                        
            return None
            
        return algoritmoX(0, opcionesRestantes)

