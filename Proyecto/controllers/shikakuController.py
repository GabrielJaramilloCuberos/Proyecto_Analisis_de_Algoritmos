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
        self.vista.reiniciarColoresDisponibles()
        self.tamanioCelda = 0
        self.dimensionVentana = "200x200"

    def iniciar(self):
        self.vista.mostrarMenu(self)
        self.vista.mainloop()

    def iniciarJuego(self, nivelSeleccionado):
        print(f"[DEBUG] iniciarJuego nivel={nivelSeleccionado}")
        self.nivelActual = nivelSeleccionado
        matriz = repositorio_tableros.obtenerTablero(nivelSeleccionado)
        configuracion = repositorio_tableros.obtenerConfiguracion(nivelSeleccionado)

        self.modelo = Shikaku(matriz)
        self.tamanioCelda = configuracion["tamanioCelda"]
        self.dimensionVentana = configuracion["dimensionVentana"]
        self.filaInicio = None
        self.colInicio = None
        self.colorActual = None

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
        print("[DEBUG] volverAlMenu")
        self.modelo = None
        self.nivelActual = None
        self.filaInicio = None
        self.colInicio = None
        self.colorActual = None
        self.tamanioCelda = 0
        self.dimensionVentana = "200x200"
        self.vista.reiniciarColoresDisponibles()
        self.vista.mostrarMenu(self)

    def resolverJuego(self):
        print("[DEBUG] resolverJuego")
        print("Resolviendo...")

        if self.modelo is None:
            print("[DEBUG] resolverJuego cancelado: no hay modelo")
            return

        self.modelo.rectangulos.clear()
        self.vista.borrarRectangulo()
        self.vista.limpiarRectangulosUsuario()
        self.vista.reiniciarColoresDisponibles()

        solucion = self.modelo.solucionador()
        if solucion is None:
            print("[DEBUG] solver sin solucion")
            return

        print(f"[DEBUG] solver encontro {len(solucion)} rectangulos")
        for rectanguloSolucion in solucion:
            self.modelo.crearRectangulo(rectanguloSolucion)

            x1 = rectanguloSolucion.columnaInicio * self.tamanioCelda
            y1 = rectanguloSolucion.filaInicio * self.tamanioCelda
            x2 = (rectanguloSolucion.columnaFinal + 1) * self.tamanioCelda
            y2 = (rectanguloSolucion.filaFinal + 1) * self.tamanioCelda

            color = self.vista.obtenerColorDisponible()
            if color is None:
                color = "gray"
            self.vista.consolidarRectangulo(x1, y1, x2, y2, color)

    def onClickInicial(self, event):
        if self.tamanioCelda <= 0:
            return

        print(f"[DEBUG] onClickInicial x={event.x} y={event.y}")

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
                    print(
                        f"[DEBUG] rectangulo eliminado fila={filaInicio}-{filaFin} "
                        f"col={colInicio}-{colFin}"
                    )
                    colorRectangulo = self.vista.eliminarRectanguloPorId(rectanguloId)
                    self.vista.liberarColor(colorRectangulo)

                self.filaInicio = None
                self.colInicio = None
                self.colorActual = None
                self.vista.borrarRectangulo()
                return

        self.filaInicio = event.y // self.tamanioCelda
        self.colInicio = event.x // self.tamanioCelda
        self.colorActual = self.vista.obtenerColorDisponible()
        if self.colorActual is None:
            print("[DEBUG] no hay colores disponibles")
            self.filaInicio = None
            self.colInicio = None
            return
        print(
            f"[DEBUG] seleccion inicio fila={self.filaInicio} col={self.colInicio} "
            f"color={self.colorActual}"
        )

    def onArrastrar(self, event):
        if self.filaInicio is None or self.colInicio is None:
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
        if self.filaInicio is None or self.colInicio is None:
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

        print(
            f"[DEBUG] intento rectangulo fila={filaInicio}-{filaFin} "
            f"col={colInicio}-{colFin} valido={esValido}"
        )

        if esValido:
            self.modelo.crearRectangulo(
                Rectangulo(filaInicio, filaFin, colInicio, colFin)
            )
            self.vista.consolidarRectangulo(x1, y1, x2, y2, self.colorActual)
            print(f"[DEBUG] rectangulo creado total={len(self.modelo.rectangulos)}")
        else:
            print("[DEBUG] rectangulo rechazado")
            self.vista.liberarColor(self.colorActual)

        self.vista.borrarRectangulo()

        self.filaInicio = None
        self.colInicio = None
        self.colorActual = None

if __name__ == "__main__":
    app = ShikakuController()
    app.iniciar()