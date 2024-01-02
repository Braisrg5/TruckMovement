from copy import deepcopy
import stl
import vtkplotlib as vpl
import numpy
import math
from stl import mesh
import PyQt6


def cargar_archivos(grua):
    """función que carga los archivos de una lista"""
    lista = []
    for i in range(len(grua)):
        modelo = stl.mesh.Mesh.from_file(grua[i])
        lista.append(modelo)
    return lista


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


def mov_horizontal(piezas):
    inicio = 0
    final = 60
    n_pasos = 100
    for pasos in range(0, n_pasos + 1):
        copia_cabina = deepcopy(piezas[0])
        x = pasos * final / n_pasos
        T_cabina = matriz_transformacion(0.0, 0.0, 0.0, x, 0.0, 0.0)
        copia_cabina.transform(T_cabina)

        copia_rueda_delantera_derecha = deepcopy(piezas[1])
        T_rueda_delantera_derecha = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, -1.2)
        matriz = T_cabina @ T_rueda_delantera_derecha
        copia_rueda_delantera_derecha.transform(matriz)

        copia_rueda_delantera_izquierda = deepcopy(piezas[2])
        T_rueda_delantera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, 1.2)
        matriz = T_cabina @ T_rueda_delantera_izquierda
        copia_rueda_delantera_izquierda.transform(matriz)

        copia_plataforma_trasera = deepcopy(piezas[3])
        T_plataforma_trasera = matriz_transformacion(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        matriz_plataforma_trasera = T_cabina @ T_plataforma_trasera
        copia_plataforma_trasera.transform(matriz_plataforma_trasera)

        copia_rueda_trasera_derecha = deepcopy(piezas[4])
        T_rueda_trasera_derecha = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, -1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_derecha
        copia_rueda_trasera_derecha.transform(matriz)

        copia_rueda_trasera_izquierda = deepcopy(piezas[5])
        T_rueda_trasera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, 1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_izquierda
        copia_rueda_trasera_izquierda.transform(matriz)

        copia_plataforma_de_giro = deepcopy(piezas[6])
        T_plataforma_de_giro = matriz_transformacion(0.0, 0.0, 0.0, -1.05, 0.25, 0.0)
        matriz_plataforma_de_giro = matriz_plataforma_trasera @ T_plataforma_de_giro
        copia_plataforma_de_giro.transform(matriz_plataforma_de_giro)

        copia_cubo = deepcopy(piezas[7])
        T_cubo = matriz_transformacion(0.0, 0.0, 0.0, -1.04, 0.63, 0.0)
        matriz = matriz_plataforma_de_giro @ T_cubo
        copia_cubo.transform(matriz)

        paint(
            [
                copia_cabina,
                copia_rueda_delantera_derecha,
                copia_rueda_delantera_izquierda,
                copia_plataforma_trasera,
                copia_rueda_trasera_derecha,
                copia_rueda_trasera_izquierda,
                copia_plataforma_de_giro,
                copia_cubo,
            ]
        )


def curva(piezas):
    inicio_x = 60
    fin_x = 65
    inicio_z = 0
    fin_z = 5
    inicio_a = 0.0
    fin_a = -math.pi / 2
    n_pasos = 10
    for pasos in range(0, n_pasos + 1):
        x = pasos * (fin_x - inicio_x) / n_pasos + inicio_x
        z = pasos * (fin_z - inicio_z) / n_pasos + inicio_z
        a = pasos * (fin_a - inicio_a) / n_pasos + inicio_a
        copia_cabina = deepcopy(piezas[0])
        T_cabina = matriz_transformacion(0.0, a, 0.0, x, 0.0, z)
        copia_cabina.transform(T_cabina)

        copia_rueda_delantera_derecha = deepcopy(piezas[1])
        T_rueda_delantera_derecha = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, -1.2)
        matriz = T_cabina @ T_rueda_delantera_derecha
        copia_rueda_delantera_derecha.transform(matriz)

        copia_rueda_delantera_izquierda = deepcopy(piezas[2])
        T_rueda_delantera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, 1.2)
        matriz = T_cabina @ T_rueda_delantera_izquierda
        copia_rueda_delantera_izquierda.transform(matriz)

        copia_plataforma_trasera = deepcopy(piezas[3])
        T_plataforma_trasera = matriz_transformacion(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        matriz_plataforma_trasera = T_cabina @ T_plataforma_trasera
        copia_plataforma_trasera.transform(matriz_plataforma_trasera)

        copia_rueda_trasera_derecha = deepcopy(piezas[4])
        T_rueda_trasera_derecha = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, -1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_derecha
        copia_rueda_trasera_derecha.transform(matriz)

        copia_rueda_trasera_izquierda = deepcopy(piezas[5])
        T_rueda_trasera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, 1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_izquierda
        copia_rueda_trasera_izquierda.transform(matriz)

        copia_plataforma_de_giro = deepcopy(piezas[6])
        T_plataforma_de_giro = matriz_transformacion(0.0, 0.0, 0.0, -1.05, 0.25, 0.0)
        matriz_plataforma_de_giro = matriz_plataforma_trasera @ T_plataforma_de_giro
        copia_plataforma_de_giro.transform(matriz_plataforma_de_giro)

        copia_cubo = deepcopy(piezas[7])
        T_cubo = matriz_transformacion(0.0, 0.0, 0.0, -1.04, 0.63, 0.0)
        matriz = matriz_plataforma_de_giro @ T_cubo
        copia_cubo.transform(matriz)

        paint(
            [
                copia_cabina,
                copia_rueda_delantera_derecha,
                copia_rueda_delantera_izquierda,
                copia_plataforma_trasera,
                copia_rueda_trasera_derecha,
                copia_rueda_trasera_izquierda,
                copia_plataforma_de_giro,
                copia_cubo,
            ]
        )


def otra_recta(piezas):
    inicio_z = 5
    fin_z = 45
    n_pasos = 100
    for pasos in range(0, n_pasos + 1):
        z = pasos * (fin_z - inicio_z) / n_pasos + inicio_z
        copia_cabina = deepcopy(piezas[0])
        T_cabina = matriz_transformacion(0.0, -math.pi / 2, 0.0, 65, 0.0, z)
        copia_cabina.transform(T_cabina)

        copia_rueda_delantera_derecha = deepcopy(piezas[1])
        T_rueda_delantera_derecha = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, -1.2)
        matriz = T_cabina @ T_rueda_delantera_derecha
        copia_rueda_delantera_derecha.transform(matriz)

        copia_rueda_delantera_izquierda = deepcopy(piezas[2])
        T_rueda_delantera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, 1.2)
        matriz = T_cabina @ T_rueda_delantera_izquierda
        copia_rueda_delantera_izquierda.transform(matriz)

        copia_plataforma_trasera = deepcopy(piezas[3])
        T_plataforma_trasera = matriz_transformacion(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        matriz_plataforma_trasera = T_cabina @ T_plataforma_trasera
        copia_plataforma_trasera.transform(matriz_plataforma_trasera)

        copia_rueda_trasera_derecha = deepcopy(piezas[4])
        T_rueda_trasera_derecha = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, -1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_derecha
        copia_rueda_trasera_derecha.transform(matriz)

        copia_rueda_trasera_izquierda = deepcopy(piezas[5])
        T_rueda_trasera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, 1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_izquierda
        copia_rueda_trasera_izquierda.transform(matriz)

        copia_plataforma_de_giro = deepcopy(piezas[6])
        T_plataforma_de_giro = matriz_transformacion(0.0, 0.0, 0.0, -1.05, 0.25, 0.0)
        matriz_plataforma_de_giro = matriz_plataforma_trasera @ T_plataforma_de_giro
        copia_plataforma_de_giro.transform(matriz_plataforma_de_giro)

        copia_cubo = deepcopy(piezas[7])
        T_cubo = matriz_transformacion(0.0, 0.0, 0.0, -1.04, 0.63, 0.0)
        matriz = matriz_plataforma_de_giro @ T_cubo
        copia_cubo.transform(matriz)

        paint(
            [
                copia_cabina,
                copia_rueda_delantera_derecha,
                copia_rueda_delantera_izquierda,
                copia_plataforma_trasera,
                copia_rueda_trasera_derecha,
                copia_rueda_trasera_izquierda,
                copia_plataforma_de_giro,
                copia_cubo,
            ],
        )


def giro_cubo(piezas):
    inicio_a = 0
    fin_a = -math.pi / 2
    z = 45
    n_pasos = 50
    for pasos in range(0, n_pasos + 1):
        copia_cabina = deepcopy(piezas[0])
        T_cabina = matriz_transformacion(0.0, -math.pi / 2, 0.0, 65, 0.0, z)
        copia_cabina.transform(T_cabina)

        copia_rueda_delantera_derecha = deepcopy(piezas[1])
        T_rueda_delantera_derecha = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, -1.2)
        matriz = T_cabina @ T_rueda_delantera_derecha
        copia_rueda_delantera_derecha.transform(matriz)

        copia_rueda_delantera_izquierda = deepcopy(piezas[2])
        T_rueda_delantera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, 1.2)
        matriz = T_cabina @ T_rueda_delantera_izquierda
        copia_rueda_delantera_izquierda.transform(matriz)

        copia_plataforma_trasera = deepcopy(piezas[3])
        matriz_plataforma_trasera = matriz_transformacion(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        matriz_plataforma_trasera = T_cabina @ matriz_plataforma_trasera
        copia_plataforma_trasera.transform(matriz_plataforma_trasera)

        copia_rueda_trasera_derecha = deepcopy(piezas[4])
        T_rueda_trasera_derecha = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, -1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_derecha
        copia_rueda_trasera_derecha.transform(matriz)

        copia_rueda_trasera_izquierda = deepcopy(piezas[5])
        T_rueda_trasera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, 1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_izquierda
        copia_rueda_trasera_izquierda.transform(matriz)

        copia_plataforma_de_giro = deepcopy(piezas[6])
        a = pasos * (fin_a - inicio_a) / n_pasos + inicio_a
        T_plataforma_de_giro = matriz_transformacion(0.0, a, 0.0, -1.05, 0.25, 0.0)
        matriz_plataforma_de_giro = matriz_plataforma_trasera @ T_plataforma_de_giro
        copia_plataforma_de_giro.transform(matriz)

        copia_cubo = deepcopy(piezas[7])
        T_cubo = matriz_transformacion(0.0, 0.0, 0.0, -1.04, 0.63, 0.0)
        matriz = matriz_plataforma_de_giro @ T_cubo
        copia_cubo.transform(matriz)


def tirar_escombros(piezas):
    inicio_a = 0
    fin_a = -math.pi / 7
    z = 45
    n_pasos = 40
    for pasos in range(0, n_pasos + 1):
        copia_cabina = deepcopy(piezas[0])
        T_cabina = matriz_transformacion(0.0, -math.pi / 2, 0.0, 65, 0.0, z)
        copia_cabina.transform(T_cabina)

        copia_rueda_delantera_derecha = deepcopy(piezas[1])
        T_rueda_delantera_derecha = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, -1.2)
        matriz = T_cabina @ T_rueda_delantera_derecha
        copia_rueda_delantera_derecha.transform(matriz)

        copia_rueda_delantera_izquierda = deepcopy(piezas[2])
        T_rueda_delantera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, 1.3, -0.1, 1.2)
        matriz = T_cabina @ T_rueda_delantera_izquierda
        copia_rueda_delantera_izquierda.transform(matriz)

        copia_plataforma_trasera = deepcopy(piezas[3])
        matriz_plataforma_trasera = matriz_transformacion(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        matriz_plataforma_trasera = T_cabina @ matriz_plataforma_trasera
        copia_plataforma_trasera.transform(matriz_plataforma_trasera)

        copia_rueda_trasera_derecha = deepcopy(piezas[4])
        T_rueda_trasera_derecha = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, -1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_derecha
        copia_rueda_trasera_derecha.transform(matriz)

        copia_rueda_trasera_izquierda = deepcopy(piezas[5])
        T_rueda_trasera_izquierda = matriz_transformacion(0.0, 0.0, 0.0, -1.4, -0.1, 1.2)
        matriz = matriz_plataforma_trasera @ T_rueda_trasera_izquierda
        copia_rueda_trasera_izquierda.transform(matriz)

        copia_plataforma_de_giro = deepcopy(piezas[6])
        angulo_plataforma_de_giro = inicio_a + pasos * (fin_a - inicio_a) / n_pasos
        T_plataforma_de_giro = matriz_transformacion(
            0.0, -math.pi / 2, angulo_plataforma_de_giro, -1.05, 0.25, 0.0
        )
        matriz_plataforma_de_giro = matriz_plataforma_trasera @ T_plataforma_de_giro
        copia_plataforma_de_giro.transform(matriz)

        copia_cubo = deepcopy(piezas[7])
        T_cubo = matriz_transformacion(0.0, 0.0, 0.0, -1.04, 0.63, 0.0)
        matriz = matriz_plataforma_de_giro @ T_cubo
        copia_cubo.transform(matriz)
        paint(
            [
                copia_cabina,
                copia_rueda_delantera_derecha,
                copia_rueda_delantera_izquierda,
                copia_plataforma_trasera,
                copia_rueda_trasera_derecha,
                copia_rueda_trasera_izquierda,
                copia_plataforma_de_giro,
                copia_cubo,
            ],
        )
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
    tirar_escombros(piezas)
    vpl.show()


if __name__ == "__main__":
    main()
