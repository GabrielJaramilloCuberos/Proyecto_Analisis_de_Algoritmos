import tkinter as tk
import tableros as tablerosJuego
import random

tableroFacil = tablerosJuego.tableroFacil
tableroMedio = tablerosJuego.tableroMedio
tableroDificil = tablerosJuego.tableroDificil

opciones = ["Nivel Facil","Nivel Medio","Nivel Dificil"]
colores = [
    "red", "blue", "green", "yellow", "purple",
    "orange", "pink", "cyan", "magenta", "lime",
    "teal", "lavender", "brown", "beige", "maroon",
    "mint cream", "navy", "aquamarine", "turquoise", "gold",
    "coral", "salmon", "khaki", "plum", "orchid",
    "crimson", "indigo", "violet", "tan", "sky blue",
    "light green", "light blue", "light coral", "light pink",
    "dark green", "dark blue", "dark red", "dark orange",
    "deep pink", "dodger blue", "forest green", "hot pink",
    "medium purple", "royal blue", "spring green"
]
rect_preview = None
color_actual = None
posibleSeleccion = None
selecciones = []

def resolverJuego():
        #TODO
        print("Resolviendo...")

# Definir tipo de tablero
def getOpcion(value_inside,root):
        eleccion = value_inside.get()
        if eleccion == 'Nivel Facil':
            root.destroy()
            crearTablero(tableroFacil,"900x900",150)
            
        elif eleccion == 'Nivel Medio':
            root.destroy()
            crearTablero(tableroMedio,"900x900", 120)
        else: 
            root.destroy()
            crearTablero(tableroDificil,"1500x1500",60)

def opcionVolver(root):
    root.destroy()
    selecciones.clear()
    initGame()

def clickInicial(event,tamanio):
    global inicio, color_actual
    fila = event.y // tamanio
    columna = event.x // tamanio
    inicio = (fila,columna)
    #Nota que cuando se elige uno de los aleatorios, puede caer en repeticiones
    #Como ya tienes muchas opciones simplemente crea un iterador global para el arreglo de los colores
    # https://en.wikipedia.org/wiki/KISS_principle
    color_actual = random.choice(colores)

    print(inicio)

def seleccionarRecuadros(event, tamanio, canvas):

    global rect_preview, posibleSeleccion

    posibleSeleccion = True

    fila1, columna1 = inicio
    x1 = columna1 * tamanio
    y1 = fila1 * tamanio
    
    fila2 = event.y // tamanio
    col2 = event.x // tamanio

    x2 = (col2 + 1) * tamanio
    y2 = (fila2 + 1) * tamanio

    rect_preview = canvas.create_rectangle((x1,y1,x2,y2),fill=color_actual, stipple = 'gray50', width = 2)


def cuadroFinal(event,canvas):

    global inicio, rect_preview, rectangulos, color_actual

    if inicio is None or rect_pre: 
        return

    coords = canvas.coords(rect_preview)

    rect = canvas.create_rectangle(
        coords,
        fill=color_actual,
        stipple='gray50',
        outline=color_actual
    )

    selecciones.append(rect)
    for i in range(len(selecciones)):
        print(canvas.coords(selecciones[i]))

    canvas.delete(rect_preview)
    rect_preview = None
    inicio = None

def initGame():

    root = tk.Tk()
    root.title("Shikaku Puzzle")
    root.geometry("200x200")

    value_inside = tk.StringVar(root)
    value_inside.set("Escoge un tablero")

    menuOpciones = tk.OptionMenu(root,value_inside, *opciones)
    menuOpciones.pack()

    enviarOpcion = tk.Button(root, text='Aceptar', command=lambda: getOpcion(value_inside, root))
    enviarOpcion.pack()

    root.mainloop()

def crearTablero(tablero, dimensionTablero, tamRecuadros):

    tamanio = tamRecuadros

    root = tk.Tk()
    root.title("Shikaku Puzzle")
    root.geometry(dimensionTablero)

    filas, columnas = len(tablero), len(tablero)

    canvas_altura = filas*tamanio
    canvas_ancho = columnas*tamanio

    canvas = tk.Canvas(root, width=canvas_ancho, height=canvas_altura)
    canvas.pack()

    color = 'white'

    for i in range(filas):    #TODO
        for j in range(columnas):

            x1 = j * tamanio
            y1 = i * tamanio
            x2 = x1 + tamanio
            y2 = y1 + tamanio

            canvas.create_rectangle((x1,y1,x2,y2),fill=color, outline='gray')

            if tablero[i][j] != 0:
                canvas.create_text((x1+x2)/2, (y1+y2)/2, text=tablero[i][j], font=("Arial", 20), fill='black')
    
    volver = tk.Button(root, text='Volver', command=lambda: opcionVolver(root))
    volver.pack()

    resolver = tk.Button(root, text='Resolver juego', command=resolverJuego)
    resolver.pack()

    canvas.bind("<Button-1>",lambda event: clickInicial(event,tamanio))
    canvas.bind("<B1-Motion>", lambda event: seleccionarRecuadros(event, tamanio, canvas))
    canvas.bind("<ButtonRelease-1>",lambda event: cuadroFinal(event,canvas))

    root.mainloop()

initGame()