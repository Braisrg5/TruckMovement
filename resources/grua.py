from copy import deepcopy
import stl
import vtkplotlib as vpl
import numpy
import math
from stl import mesh
import PyQt6


# función que carga las piezas de la grúa en una lista
def cargar_archivos(grúa):
    maquina = {}
    maquina["cabina"] = {"malla": stl.mesh.Mesh.from_file(grúa[0]), "padre": None, "mt": None}

    maquina["rueda_delantera_derecha"] = {
        "malla": stl.mesh.Mesh.from_file(grúa[1]),
        "padre": "cabina",
        "mt": None,
    }
    maquina["rueda_delantera_izquierda"] = {
        "malla": stl.mesh.Mesh.from_file(grúa[2]),
        "padre": "cabina",
        "mt": None,
    }
    maquina["plataforma_trasera"] = {
        "malla": stl.mesh.Mesh.from_file(grúa[3]),
        "padre": "cabina",
        "mt": None,
    }
    maquina["rueda_trasera_derecha"] = {
        "malla": stl.mesh.Mesh.from_file(grúa[4]),
        "padre": "plataforma_trasera",
        "mt": None,
    }
    maquina["rueda_trasera_izquierda"] = {
        "malla": stl.mesh.Mesh.from_file(grúa[5]),
        "padre": "plataforma_trasera",
        "mt": None,
    }
    maquina["plataforma_de_giro"] = {
        "malla": stl.mesh.Mesh.from_file(grúa[6]),
        "padre": "plataforma_trasera",
        "mt": None,
    }
    maquina["cubo"] = {
        "malla": stl.mesh.Mesh.from_file(grúa[7]),
        "padre": "plataforma_de_giro",
        "mt": None,
    }

    return maquina


# funcion para dibujar las partes de la grúa
def paint(meshes):
    vpl_meshes = []
    for mesh in meshes:
        vpl_mesh = vpl.mesh_plot(mesh)
        vpl_meshes.append(vpl_mesh)
    figure = vpl.gcf()
    figure.update()
    figure.show(block=False)
    for mesh in vpl_meshes:
        figure.remove_plot(mesh)
    return


# función para crear la matriz transformación
def matriz_transformacion(
    angulo_x,
    angulo_y,
    angulo_z,
    distancia_x,
    distancia_y,
    distancia_z,
):
    # Creamos la matriz de tranformacion para la rotación sobre el eje x
    matriz_x = numpy.identity(4)
    matriz_x[0:3, 0:3] = [
        [numpy.cos(angulo_x), -numpy.sin(angulo_x), 0.0],
        [numpy.sin(angulo_x), numpy.cos(angulo_x), 0.0],
        [
            0.0,
            0.0,
            1.0,
        ],
    ]

    # Creamos la matriz de tranformacion para la rotación sobre el eje y
    matriz_y = numpy.identity(4)
    matriz_y[0:3, 0:3] = [
        [numpy.cos(angulo_y), 0.0, numpy.sin(angulo_y)],
        [0.0, 1.0, 0.0],
        [-numpy.sin(angulo_y), 0.0, numpy.cos(angulo_y)],
    ]

    # Creamos la matriz de tranformacion para la rotación sobre el eje z
    matriz_z = numpy.identity(4)
    matriz_z[0:3, 0:3] = [
        [1.0, 0.0, 0.0],
        [0.0, numpy.cos(angulo_z), -numpy.sin(angulo_z)],
        [0.0, numpy.sin(angulo_z), numpy.cos(angulo_z)],
    ]

    # Creamos la matriz de traslacion
    matriz_traslacion = numpy.identity(4)
    matriz_traslacion[0, 3] = distancia_x
    matriz_traslacion[1, 3] = distancia_y
    matriz_traslacion[2, 3] = distancia_z

    # matriz resultante
    T = matriz_traslacion @ matriz_z @ matriz_y @ matriz_x
    return T


# movimiento horizontal de la grua
def mov_horizontal(piezas):
    inicio = 0
    final = 60
    n_pasos = 10
    transformaciones = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.3, -0.1, -1.2],
        [0.0, 0.0, 0.0, 1.3, -0.1, 1.2],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, -1.4, -0.1, -1.2],
        [0.0, 0.0, 0.0, -1.4, -0.1, 1.2],
        [0.0, 0.0, 0.0, -1.05, 0.25, 0.0],
        [0.0, 0.0, 0.0, -2.09, 0.88, 0.0],
    ]
    lista_piezas = []
    copia_piezas = deepcopy(piezas)
    for pasos in range(0, n_pasos + 1):
        x = pasos * final / n_pasos
        transformaciones[0][3] = x
        for nombre_pieza, t in zip(copia_piezas, transformaciones):
            pieza = copia_piezas[nombre_pieza]
            nombre_padre = pieza["padre"]
            if nombre_padre == None:
                pieza["mt"] = matriz_transformacion(*t)
            else:
                pieza_padre = copia_piezas[nombre_padre]
                pieza["mt"] = pieza_padre["mt"] @ matriz_transformacion(*t)
            pieza["malla"].transform(pieza["mt"])
            lista_piezas.append(pieza["malla"])
        paint(lista_piezas)


def curva(piezas):
    inicio_x = 60
    fin_x = 65
    inicio_z = 0
    fin_z = 5
    inicio_a = 0.0
    fin_a = -math.pi / 2
    n_pasos = 10
    transformaciones = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.3, -0.1, -1.2],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, -1.4, -0.1, -1.2],
        [0.0, 0.0, 0.0, -1.4, -0.1, 1.2],
        [0.0, 0.0, 0.0, -1.05, 0.25, 0.0],
        [0.0, 0.0, 0.0, -1.04, 0.63, 0.0],
    ]
    lista_piezas = []
    copia_piezas = deepcopy(piezas)
    for pasos in range(0, n_pasos + 1):
        x = pasos * (fin_x - inicio_x) / n_pasos + inicio_x
        z = pasos * (fin_z - inicio_z) / n_pasos + inicio_z
        a = pasos * (fin_a - inicio_a) / n_pasos + inicio_a
        transformaciones[0][4] = x
        transformaciones[0][6] = z
        transformaciones[0][3] = a
        for nombre_pieza, t in zip(copia_piezas, transformaciones):
            pieza = copia_piezas[nombre_pieza]
            nombre_padre = pieza["padre"]
            if nombre_padre == None:
                pieza["mt"] = matriz_transformacion(*t)
            else:
                pieza_padre = copia_piezas[nombre_padre]
                pieza["mt"] = pieza_padre["mt"] @ matriz_transformacion(*t)
            pieza["malla"].transform(pieza["mt"])
            lista_piezas.append(pieza)
        paint(lista_piezas)


def otra_recta(piezas):
    inicio_z = 5
    fin_z = 45
    n_pasos = 100
    transformaciones = [
        [0.0, 0.0, 0.0, 65.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.3, -0.1, -1.2],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, -1.4, -0.1, -1.2],
        [0.0, 0.0, 0.0, -1.4, -0.1, 1.2],
        [0.0, 0.0, 0.0, -1.05, 0.25, 0.0],
        [0.0, 0.0, 0.0, -1.04, 0.63, 0.0],
    ]
    lista_piezas = []
    copia_piezas = deepcopy(piezas)
    for pasos in range(0, n_pasos + 1):
        z = pasos * (fin_z - inicio_z) / n_pasos + inicio_z
        transformaciones[0][6] = z
        transformaciones[0][2] = -math.pi / 2
        for nombre_pieza, t in zip(copia_piezas, transformaciones):
            pieza = copia_piezas[nombre_pieza]
            nombre_padre = pieza["padre"]
            if nombre_padre == None:
                pieza["mt"] = matriz_transformacion(*t)
            else:
                pieza_padre = copia_piezas[nombre_padre]
                pieza["mt"] = pieza_padre["mt"] @ matriz_transformacion(*t)
            pieza["malla"].transform(pieza["mt"])
            lista_piezas.append(pieza)
        paint(lista_piezas)


def giro_cubo(piezas):
    inicio_a = -math.pi / 2
    fin_a = 0
    n_pasos = 40
    transformaciones = [
        [0.0, 0.0, 0.0, 65.0, 0.0, 45.0],
        [0.0, 0.0, 0.0, 1.3, -0.1, -1.2],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, -1.4, -0.1, -1.2],
        [0.0, 0.0, 0.0, -1.4, -0.1, 1.2],
        [0.0, 0.0, 0.0, -1.05, 0.25, 0.0],
        [0.0, 0.0, 0.0, -1.04, 0.63, 0.0],
    ]
    lista_piezas = []
    copia_piezas = deepcopy(piezas)
    for pasos in range(0, n_pasos + 1):
        a = pasos * (fin_a - inicio_a) / n_pasos + inicio_a
        transformaciones[0][2] = a
        for pieza, t in zip(copia_piezas, transformaciones):
            nombre_padre = pieza["padre"]
            if nombre_padre == None:
                pieza["mt"] = matriz_transformacion(*t)
            else:
                pieza_padre = copia_piezas[nombre_padre]
                pieza["mt"] = pieza_padre["mt"] @ matriz_transformacion(*t)
            pieza["malla"].transform(pieza["mt"])
            lista_piezas.append(pieza)
        paint(lista_piezas)


def echar_escombros(piezas):
    inicio_y = 0
    fin_y = 10
    n_pasos = 40
    transformaciones = [
        [0.0, -math.pi / 2, 0.0, 65.0, 0.0, 45.0],
        [0.0, 0.0, 0.0, 1.3, -0.1, -1.2],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, -1.4, -0.1, -1.2],
        [0.0, 0.0, 0.0, -1.4, -0.1, 1.2],
        [0.0, 0.0, 0.0, -1.05, 0.25, 0.0],
        [0.0, 0.0, 0.0, -1.04, 0.63, 0.0],
    ]
    lista_piezas = []
    copia_piezas = deepcopy(piezas)
    for pasos in range(0, n_pasos + 1):
        a = pasos * (fin_y - inicio_y) / n_pasos + inicio_y
        transformaciones[0][2] = a
        for pieza, t in zip(copia_piezas, transformaciones):
            nombre_padre = pieza["padre"]
            if nombre_padre == None:
                pieza["mt"] = matriz_transformacion(*t)
            else:
                pieza_padre = copia_piezas[nombre_padre]
                pieza["mt"] = pieza_padre["mt"] @ matriz_transformacion(*t)
            pieza["malla"].transform(pieza["mt"])
            lista_piezas.append(pieza)
        paint(lista_piezas)

    vpl.mesh_plot
    vpl.show()


def main():
    piezas_grua = [
        "cabina.stl",
        "rueda_delantera_derecha.stl",
        "rueda_delantera_izquierda.stl",
        "plataforma_trasera.stl",
        "rueda_trasera_derecha.stl",
        "rueda_trasera_izquierda.stl",
        "plataforma_de_giro.stl",
        "cubo.stl",
    ]
    # creamos la ventana para visualizar la animacion
    vpl.QtFigure()
    vpl.gcf().setWindowState(PyQt6.QtCore.Qt.WindowState.WindowMaximized)
    vpl.mesh_plot(mesh.Mesh.from_file("escenario.stl"))
    # cargamos las piezas utilizando la función
    piezas = cargar_archivos(piezas_grua)
    mov_horizontal(piezas)
    curva(piezas)
    otra_recta(piezas)
    giro_cubo(piezas)
    vpl.show()


if __name__ == "__main__":
    main()
