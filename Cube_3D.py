import pygame as pg
import numpy as np
from math import *
from operator import itemgetter
pg.init()

# Siraka a Vyska okna
# WIDTH, HEIGHT = 1000,800
WINDOW_SIZE = 800

# rychlost otacania
r_speed = 0.01
# Ako casto sa okno updatne
clock = pg.time.Clock()

# vytvorenie okna
WIN = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

# Nazvanie okna: kocka
pg.display.set_caption("Kocka")
pg.font.init()
# Konstanty farieb co budeme pouzivat
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TURQOUISE = (0, 255, 255)
PINK = (255, 0, 255)
ORANGE = (255, 128, 0)

L_YELLOW = (255, 255, 204)


# Body nasej kocky v 3D
Dots = [i for i in range(8)]
Dots[0] = [[1], [1], [-1]]
Dots[1] = [[-1], [1], [-1]]
Dots[2] = [[-1], [1], [1]]
Dots[3] = [[1], [1], [1]]
Dots[4] = [[1], [-1], [-1]]
Dots[5] = [[-1], [-1], [-1]]
Dots[6] = [[-1], [-1], [1]]
Dots[7] = [[1], [-1], [1]]

# strany kocky a ich stredy
Sides = [i for i in range(6)]
Center = [[i for i in range(4)] for _ in range(6)]
L_center = [i for i in range(12)]

Sides[0] = (0, 1, 2, 3, TURQOUISE)  #
Sides[1] = (0, 1, 5, 4, YELLOW)  # Z
Sides[2] = (0, 3, 7, 4, RED)  # X
Sides[3] = (2, 1, 5, 6, ORANGE)  # X
Sides[4] = (2, 3, 7, 6, GREEN)  # Z
Sides[5] = (4, 5, 6, 7, BLUE)  # Y


# funkcia na najdenie stredu strany


def get_center(points, sides):
    # vypocita stredy stran
    for i in range(6):
        Center[i][0] = (points[sides[i][0]][0] + points[sides[i][2]][0]) / 2
        Center[i][1] = (points[sides[i][0]][1] + points[sides[i][2]][1]) / 2


def get_Z_center():
    Center[i][2] = (points[i][2] + points[i][2]) / 2

    # prenesenie bodov na 2D priestor
'''projection_2D = [[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 0]]
'''

# uhol otacania
angle_x = angle_z = 0
# premenne
default = 0
angle_y = default
tlacitko = False
movement = 0
play = True

#premeny na posuvanie kocky
diffY = 0
diffX = 0
# Field of view
fov = 60

# znear
znear = 28

# zfar
zfar = 50

# funkcia na nasobenie matic


def M_multiply(A, B):

    A_rows = len(A)
    A_cols = len(A[0])

    # v nasom pripade toto bude vektor ktory vyzera asi takto: (x,y,z)T
    B_rows = len(B)
    B_cols = len(B[0])

    vysledok = [[0 for _ in range(B_cols)] for _ in range(A_rows)]

    if A_rows == B_rows:
        for i in range(A_rows):
            for j in range(B_cols):
                for k in range(B_rows):
                    vysledok[i][j] += A[i][k] * B[k][j]

    else:
        print("ERROR")
    return vysledok


# funkcia na spajanie dvoch bodov kocky
def Connect_point(i, j, points):
    pg.draw.line(
        WIN, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

# funkcia na vyplnenie stran kocky


def cube_fill(i, j, x, y, points, col):
    pg.draw.polygon(WIN, col, (
        (points[i][0], points[i][1]),
        (points[j][0], points[j][1]),
        (points[x][0], points[x][1]),
        (points[y][0], points[y][1]),
    ))

# funkcia na usporiadanie stredov kocky podla vzdialenosti


def sort_key(suradnice):
    return suradnice[2]


WIN.fill(BLACK)


# funkcia na obnovenie okna
def draw_window():
    # Refreshovanie okna
    pg.display.update()


scale = 500
distance = 8
while True:
    # Nakresli okno a necha nastavi 60 refreshov za sekundu
    WIN.fill(WHITE)
    clock.tick(60)

    # stlacenie tlacitka
    key = pg.key.get_pressed()

    # rotacne matice o kazdu os
    rotation_y = [[cos(angle_y), 0, sin(angle_y)],
                  [0,           1,           0],
                  [-sin(angle_y), 0, cos(angle_y)]]

    rotation_x = [[1, 0, 0],
                  [0, cos(angle_x), -sin(angle_x)],
                  [0, sin(angle_x), cos(angle_x)]]

    rotation_z = [[cos(angle_z), -sin(angle_z), 0],
                  [sin(angle_z), cos(angle_z), 0],
                  [0, 0, 1]]

    # Treba zistit kde su body po rotacii aby sme ich mohli spojit
    points = [0 for _ in range(len(Dots))]

    index = 0
    colour = [BLACK, BLUE, YELLOW, GREEN, RED, TURQOUISE, PINK, ORANGE]
    # Rotacia bodov a premenenie ich do 2D
    for point in Dots:
        # bod 1

        Rotate_X = M_multiply(rotation_x, point)
        Rotate_Y = M_multiply(rotation_y, Rotate_X)
        Rotate_Z = M_multiply(rotation_z, Rotate_Y)

        # moja vlastna projection matrix
        w = Rotate_Z[2][0]
        Z = 1 / (distance - w)

        projection_2D_3 = [[Z*2, 0, 0],
                           [0, Z*2, 0],
                           [0, 0, 1]]

        point_2D = M_multiply(projection_2D_3, Rotate_Z)

        # vykreslenie bodov na 2D
        x = point_2D[0][0] * scale + WINDOW_SIZE // 2
        y = point_2D[1][0] * scale + WINDOW_SIZE // 2
        z = Rotate_Z[2][0]
        # ulozenie bodov na spojenie
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! z suradnica je suradnica bodu !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        points[index] = [x, y, z]

        # vykreslenie bodov

        # pg.draw.circle(WIN, colour[index], (x, y), 50/(distance))

        index += 1

    # spajanie bodov, nakreslenie hran kocky
    '''for i in range(4):
        Connect_point(i, (i+1) % 4, points)
        Connect_point(i+4, ((i+1) % 4) + 4, points)
        Connect_point(i, (i % 4)+4, points)'''

    # najdenie stredu
    get_center(points, Sides)

    # najdenie Z suradnice stredu

    # vypocitanie z suradnic stredov stran
    L_center[0] = (points[0][2] + points[2][2]) / 2
    L_center[1] = (points[1][2] + points[3][2]) / 2
    Center[0][2] = (L_center[0] + L_center[1]) / 2
    Center[0][3] = 0

    L_center[2] = (points[0][2] + points[5][2]) / 2
    L_center[3] = (points[1][2] + points[4][2]) / 2
    Center[1][2] = (L_center[2] + L_center[3]) / 2
    Center[1][3] = 1

    L_center[4] = (points[3][2] + points[4][2]) / 2
    L_center[5] = (points[0][2] + points[7][2]) / 2
    Center[2][2] = (L_center[4] + L_center[5]) / 2
    Center[2][3] = 2

    L_center[6] = (points[2][2] + points[5][2]) / 2
    L_center[7] = (points[1][2] + points[6][2]) / 2
    Center[3][2] = (L_center[6] + L_center[7]) / 2
    Center[3][3] = 3

    L_center[8] = (points[1][2] + points[7][2]) / 2
    L_center[9] = (points[3][2] + points[6][2]) / 2
    Center[4][2] = (L_center[8] + L_center[9])
    Center[4][3] = 4

    L_center[10] = (points[4][2] + points[6][2]) / 2
    L_center[11] = (points[5][2] + points[7][2]) / 2
    Center[5][2] = (L_center[10] + L_center[11]) / 2
    Center[5][3] = 5

    # usporiadat strany
    Center.sort(key=sort_key)

    # vyplnanie stran kocky
    j = 0

    for stred in Center:

        # if Center[j][2] >= 0.96 / distance:
        cube_fill(Sides[stred[3]][0], Sides[stred[3]][1], Sides[stred[3]]
                  [2], Sides[stred[3]][3], points, Sides[stred[3]][4])
        # nakreslenie stredov bodkami
        # pg.draw.circle(WIN, colour[j], (Center[j][0], Center[j][1]), 50/(distance))
        j += 1

    # ak zavrieme okno tak sa vypne
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        # ak chceme skoncit
        if key[pg.K_ESCAPE]:
            pg.quit()

        # checkovanie stlacenia tlacitka apohyb mysi
        # dokym nestlacim tlacitko, stale si uklada kde je, hned jak stlacim, ulozi poslednu poziciu pred stlacenim a mozem rotovat kocku
        if not pg.mouse.get_pressed()[0]:
            pozicia = pg.mouse.get_pos()

        # stlacenie tlacitka
        elif pg.mouse.get_pressed()[0]:
            tlacitko = True
            mouse_position = pg.mouse.get_pos()
            # otacanie kocky pomocou mysi !!!!!!!!!!!!!!!!!! treba doladit !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            movement = ((mouse_position[0]-pozicia[0]),
                        (mouse_position[1]-pozicia[1]))
            angle_x -= movement[1] / 1000
            angle_y += movement[0] / 1000

            if event.type == pg.MOUSEMOTION:
                mouse_position = pg.mouse.get_pos()

                print(angle_x, angle_y)
        else:
            tlacitko = False
        if event.type == pg.MOUSEWHEEL:
            print(event.y)
            distance -= event.y / 6

    # X Rotation
    if key[pg.K_w]:
        angle_x += r_speed
    elif key[pg.K_s]:
        angle_x -= r_speed

    # Y Rotation
    if key[pg.K_e]:
        angle_z += r_speed
    elif key[pg.K_q]:
        angle_z -= r_speed

    # Z Rotation
    if key[pg.K_d]:
        angle_y += r_speed
    elif key[pg.K_a]:
        angle_y -= r_speed

    # moving away and closer
    if key[pg.K_DOWN]:
        distance += 0.1  # predtym to bol fov
    elif key[pg.K_UP]:
        if distance > 3.2:
            distance -= 0.1
    
    #moving the cube left right
    if key[pg.K_l]:
        for p in Dots:
            p[0][0] -= 0.05
    elif key[pg.K_j]:
        for p in Dots:
            p[0][0] += 0.05
    
    #moving the cube up down
    if key[pg.K_i]:
        for p in Dots:
            p[1][0] += 0.05

    elif key[pg.K_k]:
        for p in Dots:
            p[1][0] -= 0.05

    # vypisanie vektora
    font = pg.font.Font('freesansbold.ttf', 15)
    vector = [i for i in range(4)]
    Axis = [i for i in range(4)]
    Axis[0] = " X:"
    Axis[1] = " Z:"
    Axis[2] = " Y:"
    Axis[3] = "RS:"

    # vektor ukazovania
    vector[0] = str(round(sin(angle_x), 4))
    vector[1] = str(round(sin(angle_z), 4))
    vector[2] = str(round(sin(angle_y), 4))
    vector[3] = str(round(r_speed, 4))

    # vypisanie ukazovantelovho vektora
    for i in range(4):
        text = font.render(vector[i], True, BLACK, WHITE)
        os = font.render(Axis[i], True, BLACK, WHITE)
        textRect = text.get_rect()
        Osy = os.get_rect()
        textRect.center = (100, (i*i+20)+i*20+10)
        Osy.center = (50, (i*i+20)+i*20+10)
        WIN.blit(text, textRect)
        WIN.blit(os, Osy)

    # vypisanie rychlosti

    # Rotation speed
    if key[pg.K_z]:
        r_speed += 0.01
    elif key[pg.K_x]:
        r_speed -= 0.01
    if key[pg.K_RIGHT]:
        r_speed += 1000
    elif key[pg.K_LEFT]:
        r_speed -= 1000

    # resetovanie pozicie a rotacie
    if key[pg.K_r]:
        r_speed = 0.01
        angle_x = angle_z = 0
        angle_y = default
        Dots[0] = [[1], [1], [-1]]
        Dots[1] = [[-1], [1], [-1]]
        Dots[2] = [[-1], [1], [1]]
        Dots[3] = [[1], [1], [1]]
        Dots[4] = [[1], [-1], [-1]]
        Dots[5] = [[-1], [-1], [-1]]
        Dots[6] = [[-1], [-1], [1]]
        Dots[7] = [[1], [-1], [1]]

    if key[pg.K_SPACE]:
        angle_x += 0.1

    draw_window()
