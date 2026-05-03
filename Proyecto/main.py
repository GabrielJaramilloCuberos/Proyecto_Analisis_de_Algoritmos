import tkinter as tk
import tableros as tablerosJuego

tableroFacil = tablerosJuego.tableroFacil
tableroMedio = tablerosJuego.tableroMedio
tableroDificil = tablerosJuego.tableroDificil

opciones = ["Nivel Facil","Nivel Medio","Nivel Dificil"]

def resolverJuego():
        print("Resolviendo...")

def initGame():
    root = tk.Tk()
    root.title("Shikaku Puzzle")
    root.geometry("200x200")



    value_inside = tk.StringVar(root)
    value_inside.set("Escoge un tablero")

    menuOpciones = tk.OptionMenu(root,value_inside, *opciones)
    menuOpciones.pack()

    def getOpcion():
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

    enviarOpcion = tk.Button(root, text='Aceptar', command=getOpcion)
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

    for i in range(filas):
        for j in range(columnas):

            x1 = j * tamanio
            y1 = i * tamanio
            x2 = x1 + tamanio
            y2 = y1 + tamanio

            canvas.create_rectangle((x1,y1,x2,y2),fill=color, outline='gray')

            if tablero[i][j] != 0:
                canvas.create_text((x1+x2)/2, (y1+y2)/2, text=tablero[i][j], font=("Arial", 20), fill='black')

    def opcionVolver():
        root.destroy()
        initGame()
    
    volver = tk.Button(root, text='Volver', command=opcionVolver)
    volver.pack()

    resolver = tk.Button(root, text='Resolver juego', command=resolverJuego)
    resolver.pack()

    root.mainloop()

initGame()