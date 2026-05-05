class Rectangulo:
    def __init__(self, filaInicio, filaFinal, columnaInicio, columnaFinal, idPista):
        self.filaInicio = filaInicio
        self.filaFinal = filaFinal
        self.columnaInicio = columnaInicio
        self.columnaFinal = columnaFinal
        self.idPista = idPista
        self.mascara = 0
    
    def calcularMascara(self, totalColumnas, totalCeldas):
        self.mascara = 0
        for r in range(self.filaInicio, self.filaFinal + 1):
            for c in range(self.columnaInicio, self.columnaFinal + 1):
                indiceBit = (r * totalColumnas) + c
                self.mascara |= (1<< indiceBit)

        bitPista = totalCeldas + self.idPista
        self.mascara |= (1<< bitPista)


