import pygame, random, math, numpy
from pygame.locals import *
from Cubo import Cubo
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import csv

with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Agent', 'State', 'Starting Node', 'Ending Node'])

NodosVisita = numpy.array([
    [-180, 0, -180], [-160, 0, -180], [-140, 0, -180], [-120, 0, -180], [-100, 0, -180], [-80, 0, -180], [-60, 0, -180], [-40, 0, -180], [-20, 0, -180], [0, 0, -180], [20, 0, -180], [40, 0, -180], [60, 0, -180], [80, 0, -180], [100, 0, -180], [120, 0, -180], [140, 0, -180], [160, 0, -180], [180, 0, -180],
    [-180, 0, -160], [-160, 0, -160], [-140, 0, -160], [-120, 0, -160], [-100, 0, -160], [-80, 0, -160], [-60, 0, -160], [-40, 0, -160], [-20, 0, -160], [0, 0, -160], [20, 0, -160], [40, 0, -160], [60, 0, -160], [80, 0, -160], [100, 0, -160], [120, 0, -160], [140, 0, -160], [160, 0, -160], [180, 0, -160],
    [-180, 0, -140], [-160, 0, -140], [-140, 0, -140], [-120, 0, -140], [-100, 0, -140], [-80, 0, -140], [-60, 0, -140], [-40, 0, -140], [-20, 0, -140], [0, 0, -140], [20, 0, -140], [40, 0, -140], [60, 0, -140], [80, 0, -140], [100, 0, -140], [120, 0, -140], [140, 0, -140], [160, 0, -140], [180, 0, -140],
    [-180, 0, -120], [-160, 0, -120], [-140, 0, -120], [-120, 0, -120], [-100, 0, -120], [-80, 0, -120], [-60, 0, -120], [-40, 0, -120], [-20, 0, -120], [0, 0, -120], [20, 0, -120], [40, 0, -120], [60, 0, -120], [80, 0, -120], [100, 0, -120], [120, 0, -120], [140, 0, -120], [160, 0, -120], [180, 0, -120],
    [-180, 0, -100], [-160, 0, -100], [-140, 0, -100], [-120, 0, -100], [-100, 0, -100], [-80, 0, -100], [-60, 0, -100], [-40, 0, -100], [-20, 0, -100], [0, 0, -100], [20, 0, -100], [40, 0, -100], [60, 0, -100], [80, 0, -100], [100, 0, -100], [120, 0, -100], [140, 0, -100], [160, 0, -100], [180, 0, -100],
    [-180, 0, -80], [-160, 0, -80], [-140, 0, -80], [-120, 0, -80], [-100, 0, -80], [-80, 0, -80], [-60, 0, -80], [-40, 0, -80], [-20, 0, -80], [0, 0, -80], [20, 0, -80], [40, 0, -80], [60, 0, -80], [80, 0, -80], [100, 0, -80], [120, 0, -80], [140, 0, -80], [160, 0, -80], [180, 0, -80],
    [-180, 0, -60], [-160, 0, -60], [-140, 0, -60], [-120, 0, -60], [-100, 0, -60], [-80, 0, -60], [-60, 0, -60], [-40, 0, -60], [-20, 0, -60], [0, 0, -60], [20, 0, -60], [40, 0, -60], [60, 0, -60], [80, 0, -60], [100, 0, -60], [120, 0, -60], [140, 0, -60], [160, 0, -60], [180, 0, -60],
    [-180, 0, -40], [-160, 0, -40], [-140, 0, -40], [-120, 0, -40], [-100, 0, -40], [-80, 0, -40], [-60, 0, -40], [-40, 0, -40], [-20, 0, -40], [0, 0, -40], [20, 0, -40], [40, 0, -40], [60, 0, -40], [80, 0, -40], [100, 0, -40], [120, 0, -40], [140, 0, -40], [160, 0, -40], [180, 0, -40],
    [-180, 0, -20], [-160, 0, -20], [-140, 0, -20], [-120, 0, -20], [-100, 0, -20], [-80, 0, -20], [-60, 0, -20], [-40, 0, -20], [-20, 0, -20], [0, 0, -20], [20, 0, -20], [40, 0, -20], [60, 0, -20], [80, 0, -20], [100, 0, -20], [120, 0, -20], [140, 0, -20], [160, 0, -20], [180, 0, -20],
    [-180, 0, 0], [-160, 0, 0], [-140, 0, 0], [-120, 0, 0], [-100, 0, 0], [-80, 0, 0], [-60, 0, 0], [-40, 0, 0], [-20, 0, 0], [0, 0, 0], [20, 0, 0], [40, 0, 0], [60, 0, 0], [80, 0, 0], [100, 0, 0], [120, 0, 0], [140, 0, 0], [160, 0, 0], [180, 0, 0],
    [-180, 0, 20], [-160, 0, 20], [-140, 0, 20], [-120, 0, 20], [-100, 0, 20], [-80, 0, 20], [-60, 0, 20], [-40, 0, 20], [-20, 0, 20], [0, 0, 20], [20, 0, 20], [40, 0, 20], [60, 0, 20], [80, 0, 20], [100, 0, 20], [120, 0, 20], [140, 0, 20], [160, 0, 20], [180, 0, 20],
    [-180, 0, 40], [-160, 0, 40], [-140, 0, 40], [-120, 0, 40], [-100, 0, 40], [-80, 0, 40], [-60, 0, 40], [-40, 0, 40], [-20, 0, 40], [0, 0, 40], [20, 0, 40], [40, 0, 40], [60, 0, 40], [80, 0, 40], [100, 0, 40], [120, 0, 40], [140, 0, 40], [160, 0, 40], [180, 0, 40],
    [-180, 0, 60], [-160, 0, 60], [-140, 0, 60], [-120, 0, 60], [-100, 0, 60], [-80, 0, 60], [-60, 0, 60], [-40, 0, 60], [-20, 0, 60], [0, 0, 60], [20, 0, 60], [40, 0, 60], [60, 0, 60], [80, 0, 60], [100, 0, 60], [120, 0, 60], [140, 0, 60], [160, 0, 60], [180, 0, 60],
    [-180, 0, 80], [-160, 0, 80], [-140, 0, 80], [-120, 0, 80], [-100, 0, 80], [-80, 0, 80], [-60, 0, 80], [-40, 0, 80], [-20, 0, 80], [0, 0, 80], [20, 0, 80], [40, 0, 80], [60, 0, 80], [80, 0, 80], [100, 0, 80], [120, 0, 80], [140, 0, 80], [160, 0, 80], [180, 0, 80],
    [-180, 0, 100], [-160, 0, 100], [-140, 0, 100], [-120, 0, 100], [-100, 0, 100], [-80, 0, 100], [-60, 0, 100], [-40, 0, 100], [-20, 0, 100], [0, 0, 100], [20, 0, 100], [40, 0, 100], [60, 0, 100], [80, 0, 100], [100, 0, 100], [120, 0, 100], [140, 0, 100], [160, 0, 100], [180, 0, 100],
    [-180, 0, 120], [-160, 0, 120], [-140, 0, 120], [-120, 0, 120], [-100, 0, 120], [-80, 0, 120], [-60, 0, 120], [-40, 0, 120], [-20, 0, 120], [0, 0, 120], [20, 0, 120], [40, 0, 120], [60, 0, 120], [80, 0, 120], [100, 0, 120], [120, 0, 120], [140, 0, 120], [160, 0, 120], [180, 0, 120],
    [-180, 0, 140], [-160, 0, 140], [-140, 0, 140], [-120, 0, 140], [-100, 0, 140], [-80, 0, 140], [-60, 0, 140], [-40, 0, 140], [-20, 0, 140], [0, 0, 140], [20, 0, 140], [40, 0, 140], [60, 0, 140], [80, 0, 140], [100, 0, 140], [120, 0, 140], [140, 0, 140], [160, 0, 140], [180, 0, 140],
    [-180, 0, 160], [-160, 0, 160], [-140, 0, 160], [-120, 0, 160], [-100, 0, 160], [-80, 0, 160], [-60, 0, 160], [-40, 0, 160], [-20, 0, 160], [0, 0, 160], [20, 0, 160], [40, 0, 160], [60, 0, 160], [80, 0, 160], [100, 0, 160], [120, 0, 160], [140, 0, 160], [160, 0, 160], [180, 0, 160],
    [-180, 0, 180], [-160, 0, 180], [-140, 0, 180], [-120, 0, 180], [-100, 0, 180], [-80, 0, 180], [-60, 0, 180], [-40, 0, 180], [-20, 0, 180], [0, 0, 180], [20, 0, 180], [40, 0, 180], [60, 0, 180], [80, 0, 180], [100, 0, 180], [120, 0, 180], [140, 0, 180], [160, 0, 180], [180, 0, 180]
], dtype=numpy.float64)

class Lifter:
    def __init__(self, dim, vel, textures, idx, position, currentNode, tipo_exploracion, path):
        # Limites del mapa y ID del robot
        self.dim = dim
        self.idx = idx
        self.tipo_exploracion = tipo_exploracion
        # Se inicializa la posicion
        self.Position = numpy.array(position, dtype=numpy.float64).flatten()

        # Vector de dirección
        self.Direction = numpy.zeros(3)
        self.angle = 0
        self.vel = vel
        self.directionTimer = 0
        self.Direction = self.getRandomDirection()

        # Texturas
        self.textures = textures
        # Control platform
        self.platformHeight = -1.5
        self.platformUp = False
        self.platformDown = False
        # Colisiones
        self.radiusCol = 10
        # Animaciones
        self.status = "searching"
        self.trashID = -1

        # Inicializar nodos
        self.PATH = path
        self.nextNodePosition = self.getNodePath()
        # Inicializar currentNodePosition para que no rompa en Aleatorio
        if tipo_exploracion == "Aleatorio":
            self.currentNodePosition = numpy.array(position, dtype=numpy.float64).copy()
        else:
            self.currentNodePosition = self.nextNodePosition.copy() if self.nextNodePosition is not None else numpy.array(position, dtype=numpy.float64).copy()

        
        
    # ----------------------
    # Métodos de movimiento
    # ----------------------
    def getNodePath(self):
        if self.tipo_exploracion == "Planeado":
            if self.PATH:  # Evitar errores si PATH está vacío
                node_idx = self.PATH.pop(0)
                return NodosVisita[node_idx].copy()
            else:
                return self.Position.copy()  # No moverse si no hay nodos
        elif self.tipo_exploracion == "Aleatorio":
            possible_nodes = list(range(len(NodosVisita)))
            if hasattr(self, 'currentNode'):
                possible_nodes.remove(self.currentNode)
            node_idx = random.choice(possible_nodes)
            return NodosVisita[node_idx].copy()


    def getDirectionToNode(self, targetPos):
        dir_vector = targetPos - self.Position
        dir_vector[1] = 0
        distance = numpy.linalg.norm(dir_vector)
        if distance > 0:
            dir_vector /= distance
        return dir_vector, distance

    def search(self):
        self.nextNodePosition = self.getNodePath()
        self.Direction, self.distanceToNext = self.getDirectionToNode(self.nextNodePosition)

    def targetCenter(self):
        dirX = -self.Position[0]
        dirZ = -self.Position[2]
        magnitude = math.sqrt(dirX**2 + dirZ**2)
        if magnitude != 0:
            self.Direction = numpy.array([dirX / magnitude, 0, dirZ / magnitude], dtype=numpy.float64)
        else:
            self.Direction = numpy.zeros(3)

    def getRandomDirection(self):
        direction = numpy.array([
            numpy.random.uniform(-1, 1),
            0,
            numpy.random.uniform(-1, 1)
        ])
        norm = numpy.linalg.norm(direction)
        if norm != 0:
            direction = direction / norm
        else:
            direction = numpy.array([1,0,0])
        return direction

    def update(self, delta):
        if self.status == "searching":
            self.Position = numpy.asarray(self.Position, dtype=numpy.float64)
            self.Position += self.Direction * self.vel
            self.Direction, self.distanceToNext = self.getDirectionToNode(self.nextNodePosition)

            if self.distanceToNext < 1.0:
                self.currentNodePosition = self.nextNodePosition
                self.nextNodePosition = self.getNodePath()
                self.Direction, self.distanceToNext = self.getDirectionToNode(self.nextNodePosition)

            # Evitar errores de acos
            self.angle = math.acos(max(-1, min(1, self.Direction[0]))) * 180 / math.pi
            if self.Direction[2] > 0:
                self.angle = 360 - self.angle
        
        mssg = "Agent:%d \t State:%s \t Node:[%0.0f,0,%0.0f] -> [%0.0f,0,%0.0f]" % (
			self.idx,
			self.status,
			self.currentNodePosition[0],
			self.currentNodePosition[2],
			self.nextNodePosition[0],
			self.nextNodePosition[2]
		)
        print(mssg)
        with open('data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.idx, self.status,
                            f"[{self.currentNodePosition[0]:.0f},0,{self.currentNodePosition[2]:.0f}]",
                            f"[{self.nextNodePosition[0]:.0f},0,{self.nextNodePosition[2]:.0f}]"])


        match self.status:
            case "lifting":
                if self.platformHeight >= 0:
                    self.targetCenter()
                    self.status = "delivering"
                else:
                    self.platformHeight += (delta * 25)
            case "delivering":
                if (-10 <= self.Position[0] <= 10) and (-10 <= self.Position[2] <= 10):
                    self.status = "dropping"
                else:
                    newX = self.Position[0] + self.Direction[0] * self.vel
                    newZ = self.Position[2] + self.Direction[2] * self.vel
                    if newX - 10 < -self.dim or newX + 10 > self.dim:
                        self.Direction[0] *= -1
                    else:
                        self.Position[0] = newX
                    if newZ - 10 < -self.dim or newZ + 10 > self.dim:
                        self.Direction[2] *= -1
                    else:
                        self.Position[2] = newZ
                    self.angle = math.acos(max(-1, min(1, self.Direction[0]))) * 180 / math.pi
                    if self.Direction[2] > 0:
                        self.angle = 360 - self.angle
            case "dropping":
                if self.platformHeight <= -1.5:
                    self.status = "searching"
                else:
                    self.platformHeight -= (delta * 25)
            case "returning":
                if (-20 <= self.Position[0] <= 20) and (-20 <= self.Position[2] <= 20):
                    self.Position[0] -= (self.Direction[0] * (self.vel/4))
                    self.Position[2] -= (self.Direction[2] * (self.vel/4))
                else:
                    self.search()
                    self.status = "searching"

    # ----------------------
    # Métodos de dibujo
    # ----------------------
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glRotatef(self.angle, 0, 1, 0)
        glScaled(5, 5, 5)
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures[2])
        glBegin(GL_QUADS)
        # front face
        glTexCoord2f(0.0, 0.0); glVertex3d(1, 1, 1)
        glTexCoord2f(0.0, 1.0); glVertex3d(1, 1, -1)
        glTexCoord2f(1.0, 1.0); glVertex3d(1, -1, -1)
        glTexCoord2f(1.0, 0.0); glVertex3d(1, -1, 1)
        # 2nd face
        glTexCoord2f(0.0, 0.0); glVertex3d(-2, 1, 1)
        glTexCoord2f(0.0, 1.0); glVertex3d(1, 1, 1)
        glTexCoord2f(1.0, 1.0); glVertex3d(1, -1, 1)
        glTexCoord2f(1.0, 0.0); glVertex3d(-2, -1, 1)
        # 3rd face
        glTexCoord2f(0.0, 0.0); glVertex3d(-2, 1, -1)
        glTexCoord2f(0.0, 1.0); glVertex3d(-2, 1, 1)
        glTexCoord2f(1.0, 1.0); glVertex3d(-2, -1, 1)
        glTexCoord2f(1.0, 0.0); glVertex3d(-2, -1, -1)
        # 4th face
        glTexCoord2f(0.0, 0.0); glVertex3d(1, 1, -1)
        glTexCoord2f(0.0, 1.0); glVertex3d(-2, 1, -1)
        glTexCoord2f(1.0, 1.0); glVertex3d(-2, -1, -1)
        glTexCoord2f(1.0, 0.0); glVertex3d(1, -1, -1)
        # top
        glTexCoord2f(0.0, 0.0); glVertex3d(1, 1, 1)
        glTexCoord2f(0.0, 1.0); glVertex3d(-2, 1, 1)
        glTexCoord2f(1.0, 1.0); glVertex3d(-2, 1, -1)
        glTexCoord2f(1.0, 0.0); glVertex3d(1, 1, -1)
        glEnd()
        # Head
        glPushMatrix()
        glTranslatef(0, 1.5, 0)
        glScaled(0.8, 0.8, 0.8)
        glColor3f(1.0, 1.0, 1.0)
        head = Cubo(self.textures, 0)
        head.draw()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

        # Wheels
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures[1])
        for x, z in [(-1.2, 1), (0.5, 1), (0.5, -1), (-1.2, -1)]:
            glPushMatrix()
            glTranslatef(x, -1, z)
            glScaled(0.3, 0.3, 0.3)
            wheel = Cubo(self.textures, 0)
            wheel.draw()
            glPopMatrix()
        glDisable(GL_TEXTURE_2D)

        # Lifter platform
        glPushMatrix()
        if self.status in ["lifting","delivering","dropping"]:
            self.drawTrash()
        glColor3f(0.0, 0.0, 0.0)
        glTranslatef(0, self.platformHeight, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3d(1, 1, 1)
        glTexCoord2f(0.0, 1.0); glVertex3d(1, 1, -1)
        glTexCoord2f(1.0, 1.0); glVertex3d(3, 1, -1)
        glTexCoord2f(1.0, 0.0); glVertex3d(3, 1, 1)
        glEnd()
        glPopMatrix()
        glPopMatrix()

    def drawTrash(self):
        glPushMatrix()
        glTranslatef(2, (self.platformHeight + 1.5), 0)
        glScaled(0.5, 0.5, 0.5)
        glColor3f(1.0, 1.0, 1.0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures[3])
        glBegin(GL_QUADS)
        # Front face
        glTexCoord2f(0.0, 0.0); glVertex3d(1, 1, 1)
        glTexCoord2f(1.0, 0.0); glVertex3d(-1, 1, 1)
        glTexCoord2f(1.0, 1.0); glVertex3d(-1, -1, 1)
        glTexCoord2f(0.0, 1.0); glVertex3d(1, -1, 1)
        # Back face
        glTexCoord2f(0.0, 0.0); glVertex3d(-1, 1, -1)
        glTexCoord2f(1.0, 0.0); glVertex3d(1, 1, -1)
        glTexCoord2f(1.0, 1.0); glVertex3d(1, -1, -1)
        glTexCoord2f(0.0, 1.0); glVertex3d(-1, -1, -1)
        # Left face
        glTexCoord2f(0.0, 0.0); glVertex3d(-1, 1, 1)
        glTexCoord2f(1.0, 0.0); glVertex3d(-1, 1, -1)
        glTexCoord2f(1.0, 1.0); glVertex3d(-1, -1, -1)
        glTexCoord2f(0.0, 1.0); glVertex3d(-1, -1, 1)
        # Right face
        glTexCoord2f(0.0, 0.0); glVertex3d(1, 1, -1)
        glTexCoord2f(1.0, 0.0); glVertex3d(1, 1, 1)
        glTexCoord2f(1.0, 1.0); glVertex3d(1, -1, 1)
        glTexCoord2f(0.0, 1.0); glVertex3d(1, -1, -1)
        # Top face
        glTexCoord2f(0.0, 0.0); glVertex3d(-1, 1, 1)
        glTexCoord2f(1.0, 0.0); glVertex3d(1, 1, 1)
        glTexCoord2f(1.0, 1.0); glVertex3d(1, 1, -1)
        glTexCoord2f(0.0, 1.0); glVertex3d(-1, 1, -1)
        # Bottom face
        glTexCoord2f(0.0, 0.0); glVertex3d(-1, -1, 1)
        glTexCoord2f(1.0, 0.0); glVertex3d(1, -1, 1)
        glTexCoord2f(1.0, 1.0); glVertex3d(1, -1, -1)
        glTexCoord2f(0.0, 1.0); glVertex3d(-1, -1, -1)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
