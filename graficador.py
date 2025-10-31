# Implementación de un programa de dibujo usando Pygame
# Autor: [Tu Nombre]
# Fecha: [Fecha]

import pygame
import math
import numpy as np

# Funciones de dibujo ---------------
def lineaDDA(screen, x1, y1, x2, y2, color):
    """
    Implementa el algoritmo DDA (Digital Differential Analyzer) para dibujar una línea.
    
    Args:
        screen: Superficie de pygame donde se dibujará
        x1, y1: Coordenadas del punto inicial
        x2, y2: Coordenadas del punto final
        color: Color de la línea en formato RGB
    """
    dx = x2 - x1
    dy = y2 - y1

    steps = int(max(abs(dx), abs(dy)))

    if steps == 0:
        pygame.draw.circle(screen, color, (x1, y1), 1)
        return

    Xinc = dx / steps
    Yinc = dy / steps

    x = x1
    y = y1
    for i in range(steps):
        pygame.draw.circle(screen, color, ( (round(x), round(y) ) ), 1)
        x += Xinc
        y += Yinc
    
def polygon(screen, vertices, color):
    """
    Dibuja un polígono conectando una lista de vértices.
    
    Args:
        screen: Superficie de pygame donde se dibujará
        vertices: Lista de tuplas (x,y) que representan los vértices
        color: Color del polígono en formato RGB
    """
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        lineaDDA(screen, x1, y1, x2, y2, color)

def rectangle(screen, x, y, width, height, color):
    """
    Dibuja un rectángulo usando el algoritmo de línea DDA.
    
    Args:
        screen: Superficie de pygame donde se dibujará
        x, y: Coordenadas de la esquina superior izquierda
        width: Ancho del rectángulo
        height: Alto del rectángulo
        color: Color del rectángulo en formato RGB
    """
    vertices = [
        (x, y), (x + width, y),
        (x + width, y + height), (x, y + height)
    ]
    polygon(screen, vertices, color)

def circleBresenham(screen, xc, yc, r, color):
    """
    Implementa el algoritmo de Bresenham para dibujar círculos.
    
    Args:
        screen: Superficie de pygame donde se dibujará
        xc, yc: Coordenadas del centro del círculo
        r: Radio del círculo
        color: Color del círculo en formato RGB
    """
    x = 0
    y = r
    d = 3 - 2 * r

    def plot_circle_points(x, y):
        points = [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ]
        for point in points:
            pygame.draw.circle(screen, color, point, 1)

    while x <= y:
        plot_circle_points(x, y)
        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1

def drawTriangulo(screen, vertices, color):
    """
    Dibuja un triángulo usando el algoritmo de línea DDA.
    
    Args:
        screen: Superficie de pygame donde se dibujará
        vertices: Lista de 3 tuplas (x,y) que representan los vértices
        color: Color del triángulo en formato RGB
    """
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        lineaDDA(screen, x1, y1, x2, y2, color)

def drawElipse(screen, xc, yc, rx, ry, color):
    """
    Dibuja una elipse usando parametrización.
    
    Args:
        screen: Superficie de pygame donde se dibujará
        xc, yc: Coordenadas del centro de la elipse
        rx: Radio en el eje x
        ry: Radio en el eje y
        color: Color de la elipse en formato RGB
    """
    t_values =  np.linspace(0, 2 * np.pi, 100)
    for t in t_values:
        x = int(xc + rx * np.cos(t))
        y = int(yc + ry * np.sin(t))
        pygame.draw.circle(screen, color, (x, y), 1)

def drawCurvaBezier(screen, p0, p1, p2, p3, color):
    """
    Dibuja una curva de Bézier cúbica.
    
    Args:
        screen: Superficie de pygame donde se dibujará
        p0: Punto inicial (x,y)
        p1, p2: Puntos de control (x,y)
        p3: Punto final (x,y)
        color: Color de la curva en formato RGB
    """
    t_values = np.linspace(0, 1, 100)
    for t in t_values:
        x = int((1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0])
        y = int((1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1])
        pygame.draw.circle(screen, color, (x, y), 1)
# ----------------------------------


class Boton:
    def __init__(self, x, y, ancho, alto, imagenO, color_normal, color_hover, color_texto=(255, 255, 255), fuente=None, llenado=0):
        """
        Constructor de la clase Boton
        :param x: posición X del botón
        :param y: posición Y del botón
        :param ancho: ancho del botón
        :param alto: alto del botón
        :param texto: texto que se mostrará en el botón
        :param color_normal: color normal del botón (tuple RGB)
        :param color_hover: color cuando el mouse pasa sobre el botón
        :param color_texto: color del texto (tuple RGB)
        :param fuente: objeto pygame.font.Font o None
        """
        self.rect = pygame.Rect(x, y, ancho, alto)

        if imagenO:
            self.imagen = pygame.image.load(imagenO)
            self.imagen = pygame.transform.scale(self.imagen, (ancho-10, alto-10))
        else:
            self.imagen = False

        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.fuente = fuente or pygame.font.Font(None, 36)
        self.hover = False
        self.llenado = llenado

    def dibujar(self, pantalla):
        """Dibuja el botón en pantalla."""
        color_actual = self.color_hover if self.hover else self.color_normal
        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=8, width=self.llenado)

        # mostrar imagen
        if self.imagen:
            imagen_rect = self.imagen.get_rect(center=self.rect.center)
            pantalla.blit(self.imagen, imagen_rect)
        else:
            # Dibujar texto centrado
            texto_surf = self.fuente.render("", True, self.color_texto)
            texto_rect = texto_surf.get_rect(center=self.rect.center)
            pantalla.blit(texto_surf, texto_rect)

    def actualizar(self, eventos):
        """Actualiza el estado del botón (detecta hover y clics)."""
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.hover:
                    return True  # Retorna True si se hace clic sobre el botón
        return False



# Inicialización de Pygame y configuración inicial
pygame.init()
screen = pygame.display.set_mode((1020, 650))  # Ventana de 1020x650 píxeles
screen.fill("white")  # Fondo blanco
clock = pygame.time.Clock()  # Para controlar los FPS
running = True  # Control del bucle principal

# Variables de estado para el dibujo
dibujar = False  # Controla si se debe dibujar
inicio = (0, 0)  # Punto inicial del dibujo
final = (0, 0)   # Punto final del dibujo
color = (0,0,0)  # Color actual (negro por defecto)

# Estados de las herramientas de dibujo
linea = True      # Herramienta activa por defecto
rectangulo = False
circulo = False
elipse = False
triangulo = False
curva = False
vaciar = False

# Configuración de los botones de herramientas
colorBoton = (0,0,0)      # Color normal de los botones
hoover = (100,160,210)    # Color cuando el mouse está sobre el botón

# Creación de los botones de herramientas
botonLinea = Boton(10, 10, 50, 50, "Imagenes/Linea.jpg", colorBoton, hoover, llenado=1)
botonRectangulo = Boton(10, 70, 50, 50, "Imagenes/Rectangulo.jpeg", colorBoton, hoover, llenado=1)
botonCirculo = Boton(10, 130, 50, 50, "Imagenes/Circulo.jpg", colorBoton, hoover, llenado=1)
botonElipse = Boton(10, 190, 50, 50, "Imagenes/Elipse.jpg", colorBoton, hoover, llenado=1)
botonTriangulo = Boton(10, 250, 50, 50, "Imagenes/Triangulo.jpg", colorBoton, hoover, llenado=1)
botonCurva = Boton(10, 310, 50, 50, "Imagenes/Curva.jpg", colorBoton, hoover, llenado=1)

botonVaciar = Boton(10, 370, 50, 50, "Imagenes/Vaciar.jpeg", colorBoton, hoover, llenado=1)

# Creación de la paleta de colores
colorRojo = Boton(960, 10, 50, 50, "", (255,0,0), (200,0,0), llenado=0)
colorNaranja = Boton(960, 70, 50, 50, "", (255,165,0), (50,50,50), llenado=0)
colorAmarillo = Boton(960, 130, 50, 50, "", (255,255,0), (200,200,0), llenado=0)
colorVerde = Boton(960, 190, 50, 50, "", (0,255,0), (0,200,0), llenado=0)
colorAzul = Boton(960, 250, 50, 50, "", (0,0,255), (0,0,200), llenado=0)   
colorMorado = Boton(960, 310, 50, 50, "", (160,32,240), (200,0,200), llenado=0)
colorRosado = Boton(960, 370, 50, 50, "", (255,0,128), (200,0,100), llenado=0)
colorMarron = Boton(960, 430, 50, 50, "", (150, 75, 0), (100,50,0), llenado=0)
colorGris = Boton(960, 490, 50, 50, "", (128,128,128), (100,100,100), llenado=0)
colorNegro = Boton(960, 550, 50, 50, "", (0,0,0), (50,50,50), llenado=0)




# Bucle principal del juego
while running:
    # Dibuja los paneles laterales
    pygame.draw.rect(screen, (232, 223, 203), (0, 0, 70, 650))      # Panel izquierdo
    pygame.draw.rect(screen, (232, 223, 203), (950, 0, 70, 650))    # Panel derecho
    
    # Dibuja los botones de herramientas
    botonRectangulo.dibujar(screen)
    botonLinea.dibujar(screen)
    botonCirculo.dibujar(screen)
    botonElipse.dibujar(screen)
    botonTriangulo.dibujar(screen)
    botonCurva.dibujar(screen)
    botonVaciar.dibujar(screen)
    
    # Dibuja la paleta de colores
    colorRojo.dibujar(screen)
    colorNaranja.dibujar(screen)
    colorAmarillo.dibujar(screen)
    colorVerde.dibujar(screen)
    colorAzul.dibujar(screen)
    colorMorado.dibujar(screen)
    colorRosado.dibujar(screen)
    colorMarron.dibujar(screen)
    colorGris.dibujar(screen)
    colorNegro.dibujar(screen)
    

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if(botonLinea.rect.collidepoint(event.pos)):
                linea = True
                rectangulo = False
                circulo = False
                elipse = False
                triangulo = False
                curva = False
                vaciar = False
                print("Linea seleccionada")
            elif(botonRectangulo.rect.collidepoint(event.pos)):
                linea = False
                rectangulo = True
                circulo = False
                elipse = False
                triangulo = False
                curva = False
                vaciar = False
                print("Rectangulo seleccionada")
            elif(botonCirculo.rect.collidepoint(event.pos)):
                linea = False
                rectangulo = False
                circulo = True
                elipse = False
                triangulo = False
                curva = False
                vaciar = False
                print("Circulo seleccionada")
            elif(botonElipse.rect.collidepoint(event.pos)):
                linea = False
                rectangulo = False
                circulo = False
                elipse = True
                triangulo = False
                curva = False
                vaciar = False
                print("Elipse seleccionada")
            elif(botonTriangulo.rect.collidepoint(event.pos)):
                linea = False
                rectangulo = False
                circulo = False
                elipse = False
                triangulo = True
                curva = False
                vaciar = False
                print("Triangulo seleccionada")
            elif(botonCurva.rect.collidepoint(event.pos)):
                linea = False
                rectangulo = False
                circulo = False
                elipse = False
                triangulo = False
                curva = True
                vaciar = False
                print("Curva seleccionada")
            elif(botonVaciar.rect.collidepoint(event.pos)):
                linea = False
                rectangulo = False
                circulo = False
                elipse = False
                triangulo = False
                curva = False
                vaciar = True
                print("Regresar seleccionada")

            elif(colorRojo.rect.collidepoint(event.pos)):
                color = (230,0,0)
            elif(colorNaranja.rect.collidepoint(event.pos)):
                color = (255,165,0)
            elif(colorAmarillo.rect.collidepoint(event.pos)):
                color = (255,255,0)
            elif(colorVerde.rect.collidepoint(event.pos)):
                color = (0,255,0)
            elif(colorAzul.rect.collidepoint(event.pos)):
                color = (0,0,255)
            elif(colorMorado.rect.collidepoint(event.pos)):
                color = (160,32,240)
            elif(colorRosado.rect.collidepoint(event.pos)):
                color = (255,0,128)
            elif(colorMarron.rect.collidepoint(event.pos)):
                color = (150, 75, 0)
            elif(colorGris.rect.collidepoint(event.pos)):
                color = (128,128,128)
            elif(colorNegro.rect.collidepoint(event.pos)):
                color = (0,0,0)
            

            print("Mouse down at", event.pos)
            inicio = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            print("Mouse up at", event.pos)
            final = event.pos
            dibujar = True
        

    if(dibujar):
        if linea:
            lineaDDA(screen, inicio[0], inicio[1], final[0], final[1], color)

            dibujar = False
            
        elif rectangulo:
            left = min(inicio[0], final[0])
            top = min(inicio[1], final[1])
            ancho = abs(final[0] - inicio[0])
            alto = abs(final[1] - inicio[1])

            print(left, top, ancho, alto)

            #pygame.draw.rect(screen, color, (left, top, ancho, alto), 5)
            rectangle(screen, left, top, ancho, alto, color)

            dibujar = False

        elif circulo:
            x = final[0] - inicio[0]
            y = final[1] - inicio[1]

            centroX = (inicio[0] + final[0]) / 2
            centroY = (inicio[1] + final[1]) / 2

            r = math.sqrt(x**2 + y**2)

            circleBresenham(screen, int(centroX), int(centroY), int(r), color)

            dibujar = False

        elif elipse:
            left = min(inicio[0], final[0])
            top = min(inicio[1], final[1])
            ancho = abs(final[0] - inicio[0])
            alto = abs(final[1] - inicio[1])

            print(left, top, ancho, alto)

            #pygame.draw.ellipse(screen, color, (left, top, ancho, alto), 5)
            drawElipse(screen, left + ancho//2, top + alto//2, ancho//2, alto//2, color)

            dibujar = False
            
        elif triangulo:
            x1, y1 = inicio
            x2, y2 = final
            x3 = x1 - (x2 - x1)
            y3 = y2

            vertices = [(x1, y1), (x2, y2), (x3, y3)]
            drawTriangulo(screen, vertices, color)

            dibujar = False

        elif curva:
            x1, y1 = inicio
            x4, y4 = final
            x2 = x1 + (x4 - x1) // 3
            y2 = y1 - 100
            x3 = x1 + 2 * (x4 - x1) // 3
            y3 = y4 - 100

            p0 = (x1, y1)
            p1 = (x2, y2)
            p2 = (x3, y3)
            p3 = (x4, y4)

            drawCurvaBezier(screen, p0, p1, p2, p3, color)

            dibujar = False
            

        elif vaciar:
            screen.fill("white")

            vaciar = False
            dibujar = False    


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()