import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math


class Basura:
    def __init__(self, dim, vel, textures, txtIndex, idx, position):
        # Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [1,1,1,1,1,-1,1,-1,-1,1,-1,1,-1,1,1,-1,1,-1,-1,-1,-1,-1,-1,1,]
        self.elementArray = [0,1,2,3,0,3,7,4,0,4,5,1,6,2,1,5,6,5,4,7,6,7,3,2,]


        # Se guardan los limites del tablero
        self.dim = dim
        # Se guarda la posicion de la basura
        self.Position = position
        
        
        # Se inicializa un vector de direccion aleatorio
        dirX = random.randint(-10, 10) or 1
        dirZ = random.randint(-1, 1) or 1
        # Busca la magnitud del vector * velocidad (que tan rapido se movera)
        magnitude = math.sqrt(dirX * dirX + dirZ * dirZ) * vel
        # Se normaliza la funcion (asi se evitan magnitudes mas grandes que otras alterando la velocidad de movimiento)
        self.Direction = [dirX / magnitude, 0, dirZ / magnitude]
        
        
        # Lista de imágenes cargadas
        self.textures = textures
        # Index de la textura a utilizar
        self.txtIndex = txtIndex
        # Si el cubo sigue activo o debe dejar de dibujarse (dibujar o no dibujar la basura).
        self.alive = True

    def update(self):
        # Accede a las variables de posicion y de direccion para extraer los valores deseados
        # Suma la direccion (la magnitud normalizada), asi cada suma significa un paso (cambio de posicion)
        newX = self.Position[0] + self.Direction[0]
        newZ = self.Position[2] + self.Direction[2]
        
        # Si el cubo toca el borde (-dim o dim), rebota:
        if newX < -self.dim or newX > self.dim:
            self.Direction[0] *= -1
        else:
            self.Position[0] = newX
        if newZ < -self.dim or newZ > self.dim:
            self.Direction[2] *= -1
        else:
            self.Position[2] = newZ

    def draw(self):
        if self.alive:
            # Guarda la posicion del mundo
            glPushMatrix()
            # Mueve la basura a su lugar
            glTranslatef(self.Position[0], self.Position[1], self.Position[2])
            glScaled(2, 2, 2)
            glColor3f(1.0, 1.0, 1.0)

            # Agrega la imagen a las caras de la basura
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures[self.txtIndex])

            glBegin(GL_QUADS)

            # Front face
            glTexCoord2f(0.0, 0.0)
            glVertex3d(1, 1, 1)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(-1, 1, 1)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(-1, -1, 1)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(1, -1, 1)

            # Back face
            glTexCoord2f(0.0, 0.0)
            glVertex3d(-1, 1, -1)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(1, 1, -1)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(1, -1, -1)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(-1, -1, -1)

            # Left face
            glTexCoord2f(0.0, 0.0)
            glVertex3d(-1, 1, 1)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(-1, 1, -1)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(-1, -1, -1)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(-1, -1, 1)

            # Right face
            glTexCoord2f(0.0, 0.0)
            glVertex3d(1, 1, -1)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(1, 1, 1)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(1, -1, 1)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(1, -1, -1)

            # Top face
            glTexCoord2f(0.0, 0.0)
            glVertex3d(-1, 1, 1)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(1, 1, 1)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(1, 1, -1)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(-1, 1, -1)

            # Bottom face
            glTexCoord2f(0.0, 0.0)
            glVertex3d(-1, -1, 1)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(1, -1, 1)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(1, -1, -1)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(-1, -1, -1)

            glEnd()
            glDisable(GL_TEXTURE_2D)

            glPopMatrix()
