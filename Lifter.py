import pygame, random, math, numpy
from pygame.locals import *
from Cubo import Cubo
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# No longer using fixed nodes - random movement instead
ORIGIN = numpy.array([0, 0, 0], dtype=numpy.float64)

NodosVisita = numpy.array([
    [0, 0, 0], [20, 0, 0], [40, 0, 0], [60, 0, 0], [80, 0, 0],
    [0, 0, 20], [20, 0, 20], [40, 0, 20], [60, 0, 20], [80, 0, 20],
    [0, 0, 40], [20, 0, 40], [40, 0, 40], [60, 0, 40], [80, 0, 40],
    [0, 0, 60], [20, 0, 60], [40, 0, 60], [60, 0, 60], [80, 0, 60],
    [0, 0, 80], [20, 0, 80], [40, 0, 80], [60, 0, 80], [80, 0, 80]
], dtype=numpy.float64)

class Lifter:
	def __init__(self, dim, vel, textures, idx, position, currentNode):
		# Limites del mapa y ID del robot
		self.dim = dim
		self.idx = idx
		# Se inicializa una posicion aleatoria en el tablero
		# self.Position = [random.randint(-dim, dim), 6, random.randint(-dim, dim)]
		self.Position = position

		# Se inicializa un vector que apunta al [0, 0, 0]
		self.Direction = numpy.zeros(3);
		self.angle = 0
		self.vel = vel
		self.directionTimer = 0;  # Tiempo en que se tarda para cambiar direccion
		self.Direction = self.getRandomDirection();  # Asigna direccion random al vector (antes era de [0, 0, 0])

		# Arreglo de texturas
		self.textures = textures
		# Control variables for platform movement
		self.platformHeight = -1.5
		self.platformUp = False
		self.platformDown = False
		#Control variable for collisions
		self.radiusCol = 10
		#Control variables for animations
		self.status = "searching"
		self.trashID = -1

	def search(self):
		# Vector random
		u = numpy.random.rand(3);
		u[1] = 0;
		u /= numpy.linalg.norm(u); # Normaliza el vector
		self.Direction = u;

	def targetCenter(self):
		# Funcion para mover la basura al centro\
		# Calcula el vector y magnitud para moverse al centro
		dirX = -self.Position[0]
		dirZ = -self.Position[2]
		magnitude = math.sqrt(dirX**2 + dirZ**2)
		# Normaliza la magnitud
		self.Direction = [(dirX / magnitude), 0, (dirZ / magnitude)]

	def getRandomDirection(self):
		# Direccion Random
		direction = numpy.array([
			numpy.random.uniform(-1, 1),  # X component
			0,                            # Y component (fixed)
			numpy.random.uniform(-1, 1)   # Z component
		])
		# Normalize the direction vector
		direction = direction / numpy.linalg.norm(direction)
		return direction

	def update(self, delta):
		# Change direction randomly every few seconds during search
		if self.status == "searching":
			self.directionTimer -= delta
			if self.directionTimer <= 0:
				self.Direction = self.getRandomDirection()
				self.directionTimer = numpy.random.uniform(2, 5)  # Change direction every 2-5 seconds
			
			# Check boundaries and bounce if needed
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
		
		# Update angle based on direction
		self.angle = math.acos(self.Direction[0]) * 180 / math.pi
		if self.Direction[2] > 0:
			self.angle = 360 - self.angle
		# Muestra en la consola su posicion
		mssg = "Agent:%d \t State:%s \t Position:[%0.2f,0,%0.2f]" %(self.idx, self.status, self.Position[0], self.Position[2]); 
		print(mssg);

		match self.status:
			case "lifting":
				if self.platformHeight >= 0:
					self.targetCenter()
					self.status = "delivering"
				else:
					self.platformHeight += (delta * 25)
			case "delivering":
				if (self.Position[0] <= 10 and self.Position[0] >= -10) and (self.Position[2] <= 10 and self.Position[2] >= -10):
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
					self.angle = math.acos(self.Direction[0]) * 180 / math.pi
					if self.Direction[2] > 0:
						self.angle = 360 - self.angle
			case "dropping":
				if self.platformHeight <= -1.5:
					self.status = "searching"
				else:
					self.platformHeight -= (delta * 25)
			case "returning":
				if (self.Position[0] <= 20 and self.Position[0] >= -20) and (self.Position[2] <= 20 and self.Position[2] >= -20):
					self.Position[0] -= (self.Direction[0] * (self.vel/4))
					self.Position[2] -= (self.Direction[2] * (self.vel/4))
				else:
					self.search()
					self.status = "searching"


	def draw(self):
		glPushMatrix()
		glTranslatef(self.Position[0], self.Position[1], self.Position[2])
		glRotatef(self.angle, 0, 1, 0)
		glScaled(5, 5, 5)
		glColor3f(1.0, 1.0, 1.0)
		# front face
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.textures[2])
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(1, 1, -1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(1, -1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, -1, 1)

		# 2nd face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(-2, 1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(1, -1, 1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(-2, -1, 1)

		# 3rd face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(-2, 1, -1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-2, 1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(-2, -1, 1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(-2, -1, -1)

		# 4th face
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, -1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-2, 1, -1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(-2, -1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, -1, -1)

		# top
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(-2, 1, 1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(-2, 1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(1, 1, -1)
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
		glPushMatrix()
		glTranslatef(-1.2, -1, 1)
		glScaled(0.3, 0.3, 0.3)
		glColor3f(1.0, 1.0, 1.0)
		wheel = Cubo(self.textures, 0)
		wheel.draw()
		glPopMatrix()

		glPushMatrix()
		glTranslatef(0.5, -1, 1)
		glScaled(0.3, 0.3, 0.3)
		wheel = Cubo(self.textures, 0)
		wheel.draw()
		glPopMatrix()

		glPushMatrix()
		glTranslatef(0.5, -1, -1)
		glScaled(0.3, 0.3, 0.3)
		wheel = Cubo(self.textures, 0)
		wheel.draw()
		glPopMatrix()

		glPushMatrix()
		glTranslatef(-1.2, -1, -1)
		glScaled(0.3, 0.3, 0.3)
		wheel = Cubo(self.textures, 0)
		wheel.draw()
		glPopMatrix()
		glDisable(GL_TEXTURE_2D)

		# Lifter
		glPushMatrix()
		if self.status in ["lifting","delivering","dropping"]:
			self.drawTrash()
		glColor3f(0.0, 0.0, 0.0)
		glTranslatef(0, self.platformHeight, 0)  # Up and down
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3d(1, 1, 1)
		glTexCoord2f(0.0, 1.0)
		glVertex3d(1, 1, -1)
		glTexCoord2f(1.0, 1.0)
		glVertex3d(3, 1, -1)
		glTexCoord2f(1.0, 0.0)
		glVertex3d(3, 1, 1)
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
