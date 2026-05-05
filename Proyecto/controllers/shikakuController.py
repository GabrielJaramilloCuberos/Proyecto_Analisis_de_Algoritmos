from Proyecto.models import tableros as repositorio_tableros
from Proyecto.models.Shikaku import Shikaku
from Proyecto.models.rectangulo import Rectangulo
from Proyecto.view.shikakuView import ShikakuView

class ShikakuController:
    def __init__(self):
        self.vista = ShikakuView()
        self.modelo = None
        self.nivelActual = None
        self.filaInicio = None
        self.colInicio = None
        self.colorActual = None
        self.tamanioCelda = 0
        self.dimensionVentana = "200x200"
        self.juegoGanado = False

    def iniciar(self):
        self.vista.mostrarMenu(self)
        self.vista.mainloop()

    def iniciarJuego(self, nivelSeleccionado):
        self.nivelActual = nivelSeleccionado
        matriz = repositorio_tableros.obtenerTablero(nivelSeleccionado)
        configuracion = repositorio_tableros.obtenerConfiguracion(nivelSeleccionado)

        self.modelo = Shikaku(matriz)
        self.tamanioCelda = configuracion["tamanioCelda"]
        self.dimensionVentana = configuracion["dimensionVentana"]
        self.filaInicio = None
        self.colInicio = None
        self.colorActual = None
        self.juegoGanado = False
        self.vista.reiniciarColoresDisponibles()
        self.vista.title("Shikaku Puzzle")

        filas = len(matriz)
        columnas = len(matriz[0]) if matriz else 0
        self.vista.mostrarTablero(
            filas,
            columnas,
            self.tamanioCelda,
            self,
            matriz,
            self.dimensionVentana,
        )

    def volverAlMenu(self):
        self.modelo = None
        self.nivelActual = None
        self.filaInicio = None
        self.colInicio = None
        self.colorActual = None
        self.tamanioCelda = 0
        self.dimensionVentana = "200x200"
        self.juegoGanado = False
        self.vista.reiniciarColoresDisponibles()
        self.vista.title("Shikaku Puzzle")
        self.vista.mostrarMenu(self)

    def resolverJuego(self):
        print("Resolviendo...")

    def actualizarTituloJuego(self):
        if self.modelo is not None and self.modelo.tableroCompleto():
            self.juegoGanado = True
            self.vista.title("Gano!")
        else:
            self.juegoGanado = False
            self.vista.title("Shikaku Puzzle")

    def onClickInicial(self, event):
        if self.tamanioCelda <= 0 or self.juegoGanado:
            return

        if self.modelo is not None:
            rectanguloInfo = self.vista.obtenerRectanguloUsuarioEnPunto(event.x, event.y)
            if rectanguloInfo is not None:
                rectanguloId, coords = rectanguloInfo

                colInicio = int(coords[0] // self.tamanioCelda)
                filaInicio = int(coords[1] // self.tamanioCelda)
                colFin = int(coords[2] // self.tamanioCelda) - 1
                filaFin = int(coords[3] // self.tamanioCelda) - 1

                eliminado = self.modelo.eliminarRectangulo(
                    filaInicio,
                    filaFin,
                    colInicio,
                    colFin,
                )
                if eliminado:
                    colorRectangulo = self.vista.eliminarRectanguloPorId(rectanguloId)
                    if colorRectangulo is not None:
                        self.vista.liberarColor(colorRectangulo)
                    self.actualizarTituloJuego()

                self.filaInicio = None
                self.colInicio = None
                self.colorActual = None
                self.vista.borrarRectangulo()
                return

        self.filaInicio = event.y // self.tamanioCelda
        self.colInicio = event.x // self.tamanioCelda
        self.colorActual = self.vista.obtenerColorDisponible()

        if self.colorActual is None:
            self.filaInicio = None
            self.colInicio = None
            return

    def onArrastrar(self, event):
        if self.juegoGanado or self.filaInicio is None or self.colInicio is None:
            return

        filaActual = event.y // self.tamanioCelda
        colActual = event.x // self.tamanioCelda

        filaMin = min(self.filaInicio, filaActual)
        filaMax = max(self.filaInicio, filaActual)
        colMin = min(self.colInicio, colActual)
        colMax = max(self.colInicio, colActual)

        x1 = colMin * self.tamanioCelda
        y1 = filaMin * self.tamanioCelda
        x2 = (colMax + 1) * self.tamanioCelda
        y2 = (filaMax + 1) * self.tamanioCelda

        self.vista.dibujarRecuadroTemporal(x1, y1, x2, y2, self.colorActual)

    def onSoltarClic(self, event):
        if self.juegoGanado or self.filaInicio is None or self.colInicio is None:
            return

        filaFinal = event.y // self.tamanioCelda
        colFinal = event.x // self.tamanioCelda

        filaInicio = min(self.filaInicio, filaFinal)
        filaFin = max(self.filaInicio, filaFinal)
        colInicio = min(self.colInicio, colFinal)
        colFin = max(self.colInicio, colFinal)

        x1 = colInicio * self.tamanioCelda
        y1 = filaInicio * self.tamanioCelda
        x2 = (colFin + 1) * self.tamanioCelda
        y2 = (filaFin + 1) * self.tamanioCelda

        esValido = False
        if self.modelo is not None:
            esValido = self.modelo.validarRectangulo(
                filaInicio,
                filaFin,
                colInicio,
                colFin,
            )

        if esValido:
            self.modelo.crearRectangulo(
                Rectangulo(filaInicio, filaFin, colInicio, colFin)
            )
            self.vista.consolidarRectangulo(x1, y1, x2, y2, self.colorActual)
            self.actualizarTituloJuego()
        elif self.colorActual is not None:
            self.vista.liberarColor(self.colorActual)

        self.vista.borrarRectangulo()

        self.filaInicio = None
        self.colInicio = None
        self.colorActual = None

if __name__ == "__main__":
    app = ShikakuController()
    app.iniciar()