import tkinter as tk


class ShikakuView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shikaku Puzzle")
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.frameActual = None
        self.canvas = None
        self.rectPreviewId = None
        self.coloresDisponibles = []
        self.reiniciarColoresDisponibles()

    def reiniciarColoresDisponibles(self):
        self.coloresDisponibles = [
            ["red", False], ["blue", False], ["green", False], ["yellow", False],
            ["purple", False], ["orange", False], ["pink", False], ["cyan", False],
            ["magenta", False], ["lime", False], ["teal", False], ["lavender", False],
            ["brown", False], ["beige", False], ["maroon", False], ["mint cream", False],
            ["navy", False], ["aquamarine", False], ["turquoise", False], ["gold", False],
            ["coral", False], ["salmon", False], ["khaki", False], ["plum", False],
            ["orchid", False], ["crimson", False], ["indigo", False], ["violet", False],
            ["tan", False], ["sky blue", False], ["light green", False], ["light blue", False],
            ["light coral", False], ["light pink", False], ["dark green", False],
            ["dark blue", False], ["dark red", False], ["dark orange", False],
            ["deep pink", False], ["dodger blue", False], ["forest green", False],
            ["hot pink", False], ["medium purple", False], ["royal blue", False],
            ["spring green", False],
        ]

    def obtenerColorDisponible(self):
        for colorInfo in self.coloresDisponibles:
            if not colorInfo[1]:
                colorInfo[1] = True
                return colorInfo[0]

        return None

    def liberarColor(self, color):
        if color is None:
            return

        for colorInfo in self.coloresDisponibles:
            if colorInfo[0] == color:
                colorInfo[1] = False
                return

    def limpiarFrameActual(self):
        if self.frameActual is not None:
            self.frameActual.destroy()
            self.frameActual = None

    def mostrarMenu(self, controlador):
        self.limpiarFrameActual()

        self.geometry("320x260")
        self.frameActual = tk.Frame(self.container, padx=24, pady=24)
        self.frameActual.pack(fill="both", expand=True)

        tk.Label(
            self.frameActual,
            text="Shikaku Puzzle",
            font=("Arial", 22, "bold"),
        ).pack(pady=(0, 12))

        tk.Label(
            self.frameActual,
            text="Escoge un tablero",
            font=("Arial", 12),
        ).pack(pady=(0, 18))

        for nivel in ["Nivel Facil", "Nivel Medio", "Nivel Dificil"]:
            tk.Button(
                self.frameActual,
                text=nivel,
                width=20,
                command=lambda dificultad=nivel: controlador.iniciarJuego(dificultad),
            ).pack(pady=5)

    def mostrarTablero(self, filas, columnas, tamanioCelda, controlador, tablero, dimensionVentana):
        self.limpiarFrameActual()

        self.geometry(dimensionVentana)
        self.frameActual = tk.Frame(self.container, padx=10, pady=10)
        self.frameActual.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            self.frameActual,
            width=columnas * tamanioCelda,
            height=filas * tamanioCelda,
            bg="white",
        )
        self.canvas.pack()
        self.rectPreviewId = None

        for fila in range(filas):
            for columna in range(columnas):
                x1 = columna * tamanioCelda
                y1 = fila * tamanioCelda
                x2 = x1 + tamanioCelda
                y2 = y1 + tamanioCelda

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

                valor = tablero[fila][columna]
                if valor != 0:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=str(valor),
                        font=("Arial", 20),
                        fill="black",
                    )

        barraBotones = tk.Frame(self.frameActual, pady=10)
        barraBotones.pack(fill="x")

        tk.Button(barraBotones, text="Volver", command=controlador.volverAlMenu).pack(side="left", padx=5)
        tk.Button(barraBotones, text="Resolver juego", command=controlador.resolverJuego).pack(side="left", padx=5)

        self.canvas.bind("<Button-1>", controlador.onClickInicial)
        self.canvas.bind("<B1-Motion>", controlador.onArrastrar)
        self.canvas.bind("<ButtonRelease-1>", controlador.onSoltarClic)

    def dibujarRecuadroTemporal(self, x1, y1, x2, y2, color):
        if self.canvas is None:
            return

        if self.rectPreviewId is None:
            self.rectPreviewId = self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                stipple="gray50",
                width=2,
            )
        else:
            self.canvas.coords(self.rectPreviewId, x1, y1, x2, y2)

    def borrarRectangulo(self):
        if self.canvas is not None and self.rectPreviewId is not None:
            self.canvas.delete(self.rectPreviewId)
            self.rectPreviewId = None

    def consolidarRectangulo(self, x1, y1, x2, y2, color):
        if self.canvas is None:
            return None

        return self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            stipple="gray50",
            outline=color,
            tags=("rectanguloUsuario",),
        )

    def obtenerRectanguloUsuarioEnPunto(self, x, y):
        if self.canvas is None:
            return None

        elementos = self.canvas.find_overlapping(x, y, x, y)
        for elementoId in reversed(elementos):
            if "rectanguloUsuario" in self.canvas.gettags(elementoId):
                return elementoId, self.canvas.coords(elementoId)

        return None

    def eliminarRectanguloPorId(self, rectanguloId):
        if self.canvas is not None:
            color = self.canvas.itemcget(rectanguloId, "fill")
            self.canvas.delete(rectanguloId)
            return color

        return None

    def obtenerIdsRectangulosUsuario(self):
        if self.canvas is None:
            return []

        return list(self.canvas.find_withtag("rectanguloUsuario"))

    def limpiarRectangulosUsuario(self):
        if self.canvas is None:
            return

        for rectanguloId in self.obtenerIdsRectangulosUsuario():
            self.canvas.delete(rectanguloId)