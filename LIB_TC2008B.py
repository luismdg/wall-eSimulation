import yaml, pygame, random, glob, math, numpy
from Lifter import Lifter
from Basura import Basura

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

textures = [];
lifters = [];
basuras = [];
delta = 0;

def generarPath(filas=19, columnas=19, tipo_exploracion="Aleatorio", num_lifters=1):
    """
    Genera los PATH(s) para los lifters dependiendo del tipo de exploración.
    Si hay 2 lifters en modo 'Planeado', devuelve [PATH_1, PATH_2].
    """
    if tipo_exploracion == "Planeado" and num_lifters == 1:
        path = []
        # Recorrido tipo serpiente
        for i in range(filas):
            inicio = i * columnas
            fin = inicio + columnas

            if i % 2 == 0:
                path.extend(list(range(inicio, fin)))
            else:
                path.extend(list(range(fin - 1, inicio - 1, -1)))
        return path

    elif tipo_exploracion == "Planeado" and num_lifters == 2:
        path1 = []
        path2 = []
        mitad = columnas // 2

        # Agente 1: derecha del tablero
        for i in range(filas):
            if i % 2 == 0:
                # Fila par: izquierda → derecha (solo derecha)
                for j in range(mitad, columnas):
                    path1.append((j, 0, i))
            else:
                # Fila impar: derecha → izquierda (solo derecha)
                for j in range(columnas - 1, mitad - 1, -1):
                    path1.append((j, 0, i))

        # Agente 2: izquierda del tablero
        for i in range(filas):
            if i % 2 == 0:
                # Fila par: izquierda → derecha (solo izquierda)
                for j in range(0, mitad):
                    path2.append((j, 0, i))
            else:
                # Fila impar: derecha → izquierda (solo izquierda)
                for j in range(mitad - 1, -1, -1):
                    path2.append((j, 0, i))

        return [path1, path2]

    elif tipo_exploracion == "Aleatorio":
        return list(range(filas * columnas))

    else:
        raise ValueError(f"Tipo de exploración '{tipo_exploracion}' o número de lifters ({num_lifters}) no válido.")



def GeneracionDeNodos():
	print("")

def loadSettingsYAML(File):
	class Settings: pass
	with open(File) as f:
		docs = yaml.load_all(f, Loader = yaml.FullLoader)
		for doc in docs:
			for k, v in doc.items():
				setattr(Settings, k, v)
	return Settings;


Settings = loadSettingsYAML("Settings.yaml");	
	
def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Texturas(filepath):
    # Arreglo para el manejo de texturas
    global textures;
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    
def Init(Options):
    global textures, basuras, lifters
    screen = pygame.display.set_mode( (Settings.screen_width, Settings.screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")
    

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(Settings.FOVY, Settings.screen_width/Settings.screen_height, Settings.ZNEAR, Settings.ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
    Settings.EYE_X,
    Settings.EYE_Y,
    Settings.EYE_Z,
    Settings.CENTER_X,
    Settings.CENTER_Y,
    Settings.CENTER_Z,
    Settings.UP_X,
    Settings.UP_Y,
    Settings.UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    for File in glob.glob(Settings.Materials + "*.*"):
        Texturas(File)
    
    # Posiciones iniciales de los montacargas (agents) - placed randomly inside the board
    # Support both 'lifters' and possible alternative attribute names
    num_lifters = getattr(Options, 'lifters', None)
    if num_lifters is None:
        # fallback to lowercase or 1 if missing
        num_lifters = getattr(Options, 'Lifters', 1)

    Positions = numpy.zeros((num_lifters, 3))
    CurrentNode = 0
    
    # Número de lifters
    num_lifters = getattr(Options, 'lifters', 1)
    
    # Generar PATH global
    PATH = generarPath(filas=19, columnas=19, tipo_exploracion=Options.TipoExploracion, num_lifters=num_lifters)

    # Crear lifters con su PATH correspondiente
    for i in range(num_lifters):
        if Options.TipoExploracion == "Aleatorio":
            x = random.uniform(-Settings.DimBoard * 0.8, Settings.DimBoard * 0.8)
            z = random.uniform(-Settings.DimBoard * 0.8, Settings.DimBoard * 0.8)
            p = numpy.asarray([x, 6, z], dtype=numpy.float64)
            lifters.append(Lifter(Settings.DimBoard, 0.7, textures, i, p, 0, Options.TipoExploracion, PATH))
        else:  # Planeado
            p = numpy.asarray([-180, 6, -180], dtype=numpy.float64)
            if num_lifters == 1:
                lifters.append(Lifter(Settings.DimBoard, 0.7, textures, i, p, 0, Options.TipoExploracion, PATH))
            else:
                lifters.append(Lifter(Settings.DimBoard, 0.7, textures, i, p, 0, Options.TipoExploracion, PATH[i]))


    # Generar basuras en posiciones aleatorias
    # CLI uses '--Basuras' (capital B) in Main.py, so support that name
    num_basuras = getattr(Options, 'Basuras', None)
    if num_basuras is None:
        num_basuras = getattr(Options, 'basuras', 10)

    for i in range(num_basuras):
        x = random.uniform(-Settings.DimBoard * 0.9, Settings.DimBoard * 0.9)
        z = random.uniform(-Settings.DimBoard * 0.9, Settings.DimBoard * 0.9)
        pos = [x, 0, z]
        basuras.append(Basura(Settings.DimBoard, 0.5, textures, 3, i, pos))
        
def planoText():
    # activate textures
    glColor(1.0, 1.0, 1.0)
    #glEnable(GL_TEXTURE_2D)
    # front face
    #glBindTexture(GL_TEXTURE_2D, textures[0])  # Use the first texture
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-Settings.DimBoard, 0, -Settings.DimBoard)
    
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-Settings.DimBoard, 0, Settings.DimBoard)
    
    glTexCoord2f(1.0, 1.0)
    glVertex3d(Settings.DimBoard, 0, Settings.DimBoard)
    
    glTexCoord2f(1.0, 0.0)
    glVertex3d(Settings.DimBoard, 0, -Settings.DimBoard)
    
    glEnd()
    # glDisable(GL_TEXTURE_2D)

def checkCollisions():
    for c in lifters:
        for b in basuras:
            distance = math.sqrt(math.pow((b.Position[0] - c.Position[0]), 2) + math.pow((b.Position[2] - c.Position[2]), 2))
            if distance <= c.radiusCol:
                if c.status == "searching" and b.alive:
                    b.alive = False
                    c.status = "lifting"
                #print("Colision detectada")

def display():
    global lifters, basuras, delta
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    #Se dibuja cubos
    for obj in lifters:
        obj.draw()
        obj.update(delta)

    # Se dibuja el incinerador
    glColor3f(1.0, 0.5, 0.0)  # Color: Naranja
    square_size = 20.0  # Tamaño

    half_size = square_size / 2.0
    glBegin(GL_QUADS)
    glVertex3d(-half_size, 0.5, -half_size)
    glVertex3d(-half_size, 0.5, half_size)
    glVertex3d(half_size, 0.5, half_size)
    glVertex3d(half_size, 0.5, -half_size)
    glEnd()
    
    #Se dibujan basuras
    for obj in basuras:
        obj.draw()
        #obj.update()    
    #Axis()
    
    #Se dibuja el plano gris
    planoText()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-Settings.DimBoard, 0, -Settings.DimBoard)
    glVertex3d(-Settings.DimBoard, 0, Settings.DimBoard)
    glVertex3d(Settings.DimBoard, 0, Settings.DimBoard)
    glVertex3d(Settings.DimBoard, 0, -Settings.DimBoard)
    glEnd()
    
    # Draw the walls bounding the plane
    wall_height = 50.0  # Adjust the wall height as needed
    
    glColor3f(0.8, 0.8, 0.8)  # Light gray color for walls
    
    # Draw the left wall
    glBegin(GL_QUADS)
    glVertex3d(-Settings.DimBoard, 0, -Settings.DimBoard)
    glVertex3d(-Settings.DimBoard, 0, Settings.DimBoard)
    glVertex3d(-Settings.DimBoard, wall_height, Settings.DimBoard)
    glVertex3d(-Settings.DimBoard, wall_height, -Settings.DimBoard)
    glEnd()
    
    # Draw the right wall
    glBegin(GL_QUADS)
    glVertex3d(Settings.DimBoard, 0, -Settings.DimBoard)
    glVertex3d(Settings.DimBoard, 0, Settings.DimBoard)
    glVertex3d(Settings.DimBoard, wall_height, Settings.DimBoard)
    glVertex3d(Settings.DimBoard, wall_height, -Settings.DimBoard)
    glEnd()
    
    # Draw the front wall
    glBegin(GL_QUADS)
    glVertex3d(-Settings.DimBoard, 0, Settings.DimBoard)
    glVertex3d(Settings.DimBoard, 0, Settings.DimBoard)
    glVertex3d(Settings.DimBoard, wall_height, Settings.DimBoard)
    glVertex3d(-Settings.DimBoard, wall_height, Settings.DimBoard)
    glEnd()
    
    # Draw the back wall
    glBegin(GL_QUADS)
    glVertex3d(-Settings.DimBoard, 0, -Settings.DimBoard)
    glVertex3d(Settings.DimBoard, 0, -Settings.DimBoard)
    glVertex3d(Settings.DimBoard, wall_height, -Settings.DimBoard)
    glVertex3d(-Settings.DimBoard, wall_height, -Settings.DimBoard)
    glEnd()

    checkCollisions()
    
def lookAt(theta):
    glLoadIdentity()
    rad = theta * math.pi / 180
    newX = Settings.EYE_X * math.cos(rad) + Settings.EYE_Z * math.sin(rad)
    newZ = -Settings.EYE_X * math.sin(rad) + Settings.EYE_Z * math.cos(rad)
    gluLookAt(
    newX,
    Settings.EYE_Y,
    newZ,
    Settings.CENTER_X,
    Settings.CENTER_Y,
    Settings.CENTER_Z,
    Settings.UP_X,
    Settings.UP_Y,
    Settings.UP_Z)	

def Simulacion(Options):
    # Variables para el control del observador
    global delta
    theta = Options.theta
    radius = Options.radious
    delta = Options.Delta
    Init(Options)
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        # Keyboard state for camera rotation
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if theta > 359.0:
                theta = 0
            else:
                theta += 1.0
            lookAt(theta)
        if keys[pygame.K_LEFT]:
            if theta < 1.0:
                theta = 360.0
            else:
                theta -= 1.0
            lookAt(theta)

        # Update basura movement (they move by themselves if alive)
        # Basuras son estaticas: no se actualizan cada frame. Seran removidas cuando
        # un lifter colisione con ellas (checkCollisions marca b.alive = False)

        display()
        pygame.display.flip()
        pygame.time.wait(int(max(1, delta * 1000)))
    
    
    # Check termination condition: all basuras have been collected (alive == False)
    all_collected = all((not b.alive) for b in basuras)
    if all_collected:
        print("Simulacion finalizada: todas las basuras fueron recolectadas.")
    pygame.quit()
    return