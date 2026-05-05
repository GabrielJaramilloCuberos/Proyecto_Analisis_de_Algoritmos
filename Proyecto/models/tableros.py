tableroFacil = [
    [2, 0, 0, 0, 4],
    [0, 0, 4, 0, 2],
    [0, 2, 0, 0, 0],
    [2, 0, 0, 3, 0],
    [0, 0, 4, 0, 2],
]

tableroMedio = [
    [0, 2, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 6, 3],
    [5, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 4],
    [0, 5, 0, 0, 0, 0],
]

tableroDificil = [
    [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 4, 0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0],
    [6, 5, 2, 4, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 5, 0, 0, 2, 0, 7],
    [0, 0, 2, 0, 0, 2, 4, 0, 2, 0, 0],
    [0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 12, 0, 6, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

TABLEROS = {
    "Nivel Facil": {
        "tablero": tableroFacil,
        "tamanioCelda": 150,
        "dimensionVentana": "900x900",
    },
    "Nivel Medio": {
        "tablero": tableroMedio,
        "tamanioCelda": 120,
        "dimensionVentana": "900x900",
    },
    "Nivel Dificil": {
        "tablero": tableroDificil,
        "tamanioCelda": 60,
        "dimensionVentana": "1500x1500",
    },
}


def obtenerNiveles():
    return list(TABLEROS.keys())


def obtenerTablero(nivel):
    return [fila[:] for fila in TABLEROS[nivel]["tablero"]]


def obtenerConfiguracion(nivel):
    configuracion = TABLEROS[nivel]
    return {
        "tamanioCelda": configuracion["tamanioCelda"],
        "dimensionVentana": configuracion["dimensionVentana"],
    }