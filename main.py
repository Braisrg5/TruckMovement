import vtkplotlib as vpl
from stl import mesh
import numpy
from copy import deepcopy
import PyQt6
from math import floor


def cargar_piezas():
    '''Función que carga todas las piezas y el escenario'''
    # Cargar escenario
    escenario = mesh.Mesh.from_file("./resources/escenario.stl")
    # Cargar assets
    cabina = mesh.Mesh.from_file("./resources/cabina.stl")
    plataforma_trasera = mesh.Mesh.from_file(
        "./resources/plataforma_trasera.stl")
    plataforma_giro = mesh.Mesh.from_file("./resources/plataforma_de_giro.stl")
    cubo = mesh.Mesh.from_file("./resources/cubo.stl")
    rueda_del_izq = mesh.Mesh.from_file(
        "./resources/rueda_delantera_izquierda.stl")
    rueda_del_der = mesh.Mesh.from_file(
        "./resources/rueda_delantera_derecha.stl")
    rueda_tras_izq = mesh.Mesh.from_file(
        "./resources/rueda_trasera_izquierda.stl")
    rueda_tras_der = mesh.Mesh.from_file(
        "./resources/rueda_trasera_derecha.stl")
    return escenario, [cabina, plataforma_trasera, plataforma_giro, cubo,
                       rueda_del_izq, rueda_del_der, rueda_tras_izq, rueda_tras_der]


def posicion_inicial(maquina):
    '''Coloca la máquina en la posición inicial'''
    Rx = Ry = Rz = numpy.identity(4)
    # Colocar plataforma de giro
    p_giro_c = deepcopy(maquina[2])
    Tl = translate([-1.05, 0.25, 0.0])
    Tf = Tl @ Rz @ Ry @ Rx
    p_giro_c.transform(Tf)
    # Colocar cubo
    cubo_c = deepcopy(maquina[3])
    Tl = translate([-2.09, 0.88, 0.0])
    Tf = Tl @ Rz @ Ry @ Rx
    cubo_c.transform(Tf)
    # Colocar rueda delantera izquierda
    rueda_di_c = deepcopy(maquina[4])
    Tl = translate([1.3, -0.1, 1.2])
    Tf = Tl @ Rz @ Ry @ Rx
    rueda_di_c.transform(Tf)
    # Colocar rueda delantera derecha
    rueda_dd_c = deepcopy(maquina[5])
    Tl = translate([1.3, -0.1, -1.2])
    Tf = Tl @ Rz @ Ry @ Rx
    rueda_dd_c.transform(Tf)
    # Colocar rueda trasera izquierda
    rueda_ti_c = deepcopy(maquina[6])
    Tl = translate([-1.4, -0.1, 1.2])
    Tf = Tl @ Rz @ Ry @ Rx
    rueda_ti_c.transform(Tf)
    # Colocar rueda trasera derecha
    rueda_td_c = deepcopy(maquina[7])
    Tl = translate([-1.4, -0.1, -1.2])
    Tf = Tl @ Rz @ Ry @ Rx
    rueda_td_c.transform(Tf)

    maquina = [maquina[0], maquina[1], p_giro_c, cubo_c,
               rueda_di_c, rueda_dd_c, rueda_ti_c, rueda_td_c]
    return maquina


def translate(translation):
    '''Transforma un vector en una matriz de traslación en 4d'''
    matrix = numpy.identity(4)
    matrix[0:3, 3] = translation
    return matrix


def paint(maquina, Tl, Rx=numpy.identity(4), Ry=numpy.identity(4), Rz=numpy.identity(4), erase=True):
    '''Función central del programa que coloca una lista de piezas (la máquina o el cubo) a partir
    de la matriz de traslación y las de rotación en la posición determinada por el producto de ellas'''
    lista = []
    Tf = Tl @ Rz @ Ry @ Rx
    for pieza in maquina:
        # Hacemos copia de la pieza
        pieza_c = deepcopy(pieza)
        pieza_c.transform(Tf)
        # Dibujamos y añadimos a la lista para luego borrar
        lista.append(vpl.mesh_plot(pieza_c))
    figure = vpl.gcf()
    figure.update()
    figure.show(block=False)
    if erase:
        for pieza_c in lista:
            figure.remove_plot(pieza_c)
    # Si erase == False y además, la variable máquina es, realmente, todas las piezas del vehículo,
    # borramos el cubo (para que no esté duplicado en el resto de su movimiento).
    elif len(lista) == 8:
        figure.remove_plot(lista[2])
        figure.remove_plot(lista[3])
    # Si la variable máquina es solamente [cubo] (al final de la ejecución del programa), la anterior línea
    # nos daría un error, por eso hacemos la comprobación de la longitud de la lista
    return


def rotate_y(degrees):
    '''Crea una matriz de transformación para rotar en el eje y.'''
    angle = numpy.radians(degrees)
    matrix = numpy.identity(4)
    matrix[0:3, 0:3] = [
        [numpy.cos(angle), 0.0, numpy.sin(angle)],
        [0.0, 1.0, 0.0],
        [-numpy.sin(angle), 0.0, numpy.cos(angle)]
    ]
    return matrix


def rotate_z(degrees):
    '''Crea una matriz de transformación para rotar en el eje z.'''
    angle = numpy.radians(degrees)
    matrix = numpy.identity(4)
    matrix[0:3, 0:3] = [
        [numpy.cos(angle), -numpy.sin(angle), 0.0],
        [numpy.sin(angle), numpy.cos(angle), 0.0],
        [0.0, 0.0, 1.0]
    ]
    return matrix


def calc_coords(degrees, r, x1):
    '''Calcula las coordenadas del giro del vehículo según el ángulo, el radio y la posición de inicio del giro'''
    angle = numpy.radians(degrees)
    x = r*numpy.sin(angle) + x1
    z = r*(1-numpy.cos(angle))
    return x, z


def movimiento_eje_x(maquina, x1, v):
    '''Mueve la máquina en el primer tramo del movimiento'''
    # Calculamos número de pasos según la velocidad
    n_steps = floor(x1/v)
    for step in range(n_steps+1):
        x = step * x1 / n_steps
        Tl = translate([x, 0, 0])
        paint(maquina, Tl)
    return


def giro_guapo(maquina, x1, x2, v):
    '''Mueve la máquina durante la curva'''
    r = x2-x1
    # De nuevo, número de pasos según la velocidad
    n_steps = floor(numpy.pi/(2*v) * r)
    angle = -90
    # Dividimos el ángulo entre n_steps para hacer el movimiento fluido
    for step in range(n_steps+1):
        alpha = step * angle / n_steps
        x, z = calc_coords(-alpha, r, x1)
        Tl = translate([x, 0, z])
        paint(maquina, Tl, Ry=rotate_y(alpha))
    return r


def movimiento_eje_z(maquina, z1, z2, v):
    '''Mueve la máquina en la recta final'''
    d = z2-z1
    n_steps = floor(d/v)
    # El vehículo ya está girado
    Ry = rotate_y(-90)
    for step in range(n_steps+1):
        z = step * d / n_steps + z1
        Tl = translate([65, 0, z])
        paint(maquina, Tl, Ry=Ry)
    # Pintamos y NO borramos todas las partes del vehículo menos el cubo
    paint(maquina, Tl, Ry=Ry, erase=False)
    return


def giro_cubo(mov):
    '''Hace el movimiento completo del cubo, en dos fases'''
    '''Si consideramos las posiciones en las que queremos que esté el cubo al final de cada fase,
    podríamos simplemente llevarlo de forma brusca a estos lugares, en este caso tenemos:
    Pos 0: Tl = translate([65, 0, 45]), Rx = Rz = numpy.identity(4), Ry = rotate_y(-90)
    Pos 1: Tl = translate([63.9, 0.0, 43.9]), Rx = Rz = numpy.identity(4), Ry = rotate_y(-180)
    Pos 2: Tl = translate([64.3, 2.2, 43.9]), Rx = numpy.identity(4), Ry = rotate_y(-180), Rz = rotate_z(-60)
    (Estas posiciones han sido calculadas... a ojo).
    Ahora, lo único que estamos haciendo es crear un movimiento fluido entre cada par de posiciones, de la manera más sencilla;
    es decir, creando una serie de puntos intermedios (tanto en las traslaciones como en las rotaciones)'''
    n_steps = 40
    angle1 = -90
    angle2 = -60
    for step in range(n_steps+1):
        alpha = step * angle1 / n_steps
        x = step * -1.1 / n_steps
        z = step * -1.1 / n_steps
        Tl = translate([65+x, 0.0, 45+z])
        Ry = rotate_y(-90 + alpha)
        paint(mov, Tl, Ry=Ry)
    paint([mov[0]], Tl, Ry=Ry, erase=False)

    for step in range(n_steps+1):
        alpha = step * angle2 / n_steps
        x = step * 0.3 / n_steps
        y = step * 2.2 / n_steps
        Tl = translate([63.9+x, y, 43.9])
        Rz = rotate_z(alpha)
        paint([mov[1]], Tl, Ry=Ry, Rz=Rz)

    paint([mov[1]], Tl, Ry=Ry, Rz=Rz, erase=False)
    return


if __name__ == "__main__":
    # Crear ventana
    vpl.QtFigure("Ventana")
    vpl.gcf().setWindowState(PyQt6.QtCore.Qt.WindowState.WindowMaximized)

    # Cargamos el escenario y la máquina
    escenario, maquina = cargar_piezas()

    # Colocamos escenario y máquina en sus posiciones iniciales
    vpl.mesh_plot(escenario)
    maquina = posicion_inicial(maquina)
    # Posición final de la máquina
    x2, z2 = 65, 45
    # Posición de inicio del giro
    x1 = 55
    # Velocidad de movimiento de la maquina
    v = 1.5

    vpl.view(camera_position=(0, 30, 100), focal_point=(40, 0, 10))
    movimiento_eje_x(maquina, x1, v)
    z1 = giro_guapo(maquina, x1, x2, v)
    movimiento_eje_z(maquina, z1, z2, v)

    vpl.view(camera_position=(45, 18, 70), focal_point=(65, 0, 45))
    giro_cubo(maquina[2:4])

    # Mostrar
    vpl.show()
