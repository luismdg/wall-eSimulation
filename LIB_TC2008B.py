import yaml, pygame, random, glob, math, numpy, time
from Lifter import Lifter
from Basura import Basura
from Cubo import Cubo

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


class IntersectionSim:
    """Simple text-mode 4-way intersection simulator.

    - Four approaches: N, S, E, W (traffic flows both ways by pairing N/S and E/W)
    - Two phases: NS green, then EW green. Each green lasts `TS` seconds.
    - Arrivals per approach follow a Poisson process; one road may be heavier with probability P.
    - `lifters` parameter is used as a scaling factor for arrival rates.
    """
    def __init__(self, lifters, TS, P, duration):
        self.lifters = max(1, int(lifters))
        self.TS = float(TS)
        self.P = float(P)
        self.duration = float(duration)
        # base arrival rate (cars/sec) per approach scaled by lifters (increased for visible traffic)
        self.base_rate = 0.2 * self.lifters
        self.arrival = {d: self.base_rate for d in ['N','S','E','W']}
        # With probability P, pick one road to be heavy
        if random.random() < self.P:
            heavy = random.choice(['N','S','E','W'])
            self.arrival[heavy] *= 2.5
            print(f"Via {heavy} seleccionada como alto flujo (P={self.P}) -> tasa {self.arrival[heavy]:.3f} c/s")
        else:
            print(f"Ninguna via marcada como alta (P={self.P})")

        self.queues = {d: 0 for d in ['N','S','E','W']}
        self.passed = {d: 0 for d in ['N','S','E','W']}
        self.dt = 0.5
        self.service_rate = 1.0  # cars per second when lane has green
        self.time = 0.0

    def step(self):
        # arrivals
        for d in ['N','S','E','W']:
            lam = self.arrival[d]
            arrivals = numpy.random.poisson(lam * self.dt)
            self.queues[d] += arrivals

        # determine current phase: 0 -> NS green, 1 -> EW green
        cycle = int(self.time // self.TS) % 2 if self.TS > 0 else 0
        if cycle == 0:
            green = ['N','S']
        else:
            green = ['E','W']

        cap = self.service_rate * self.dt
        for d in green:
            serve = min(self.queues[d], int(math.floor(cap)))
            frac = cap - math.floor(cap)
            if self.queues[d] - serve > 0 and random.random() < frac:
                serve += 1
            self.queues[d] -= serve
            self.passed[d] += serve

        self.time += self.dt

    def run(self):
        next_print = 0.0
        while self.time < self.duration:
            self.step()
            if self.time >= next_print:
                cycle = int(self.time // self.TS) % 2 if self.TS > 0 else 0
                phase = 'NS' if cycle == 0 else 'EW'
                print(f"[t={self.time:.1f}s] Phase={phase} Queues: N={self.queues['N']} S={self.queues['S']} E={self.queues['E']} W={self.queues['W']} | Passed: N={self.passed['N']} S={self.passed['S']} E={self.passed['E']} W={self.passed['W']}")
                next_print += max(1.0, self.duration / 10.0)
            # small sleep so output is readable when run from terminal
            time.sleep(0.01)

        self.total = sum(self.passed.values())

    def summary(self):
        print('\n--- Resumen Interseccion ---')
        for k in ['N','S','E','W']:
            print(f"Via {k}: Pasaron {self.passed[k]} autos")
        print(f"Total autos pasaron: {self.total}")
        print(f"Parametros: lifters={self.lifters}, TS={self.TS}, P={self.P}, duration={self.duration}")


def Interseccion(Options):
    """CLI entry point for the intersection simulator.

    Expected Options: lifters, TS, P, duration
    """
    lifters = getattr(Options, 'lifters', 1)
    TS = getattr(Options, 'TS', 10.0)
    P = getattr(Options, 'P', 0.0)
    duration = getattr(Options, 'duration', 60.0)

    print(f"Iniciando simulacion de interseccion: lifters={lifters} TS={TS} P={P} duration={duration} visual={getattr(Options,'visual',False)}")
    # If visual requested, run the pygame visual simulator, otherwise run text-mode
    if getattr(Options, 'visual', False):
        # Ensure Options has values expected by Init()
        if not hasattr(Options, 'TipoExploracion'):
            Options.TipoExploracion = 'Aleatorio'
        if not hasattr(Options, 'Delta'):
            Options.Delta = 0.05
        if not hasattr(Options, 'theta'):
            Options.theta = 0
        if not hasattr(Options, 'radious'):
            Options.radious = 30

        # Run a 3D OpenGL visual using existing Lifter objects as forklifts
        # Initialize OpenGL window and textures
        Init(Options)

        # Parameters
        # shorten spawn distance for visibility and ensure movement is noticeable
        spawn_dist = min(Settings.DimBoard * 0.9, 120.0)
        stop_line = 30.0
        dt = 0.05
        # increase base arrival for visible traffic in demo
        arrival = {d: 0.2 * max(1, int(lifters)) for d in ['N','S','E','W']}
        if random.random() < P:
            heavy = random.choice(['N','S','E','W'])
            arrival[heavy] *= 2.5
            print(f"Via {heavy} seleccionada como alto flujo (P={P}) -> tasa {arrival[heavy]:.3f} c/s")
        else:
            print(f"Ninguna via marcada como alta (P={P})")

        queues = {d: [] for d in ['N','S','E','W']}  # lists of vehicles waiting (positions along approach)
        moving = []  # list of vehicle dicts: {'lifter': Lifter, 'approach':d, 'state':..., 'pos':...}
        passed = {d: 0 for d in ['N','S','E','W']}

        # helper to create a visual lifter wrapper
        def make_visual_lifter(idx, approach, position):
            # create a Lifter instance for drawing but we will control its Position and angle
            lf = Lifter(Settings.DimBoard, 0.7, textures, idx, position, 0, 'Aleatorio', [])
            return lf

        sim_time = 0.0
        next_print = 0.0
        service_rate = 1.0  # cars per second when green
        visual_id = 0
        total_created = 0
        max_visual = max(6, int(lifters) * 4)  # cap total visual forklifts to avoid explosion
        lane_offset = 12.0  # lateral offset so opposite directions don't overlap

        running = True
        while running and sim_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    break

            # arrivals: create queued lifter objects so they visibly stop at the stop line
            for d in ['N','S','E','W']:
                lam = arrival[d]
                arrivals = numpy.random.poisson(lam * dt)
                for _ in range(arrivals):
                    # create a queued lifter positioned at spawn_dist
                    if d == 'N':
                        pos = numpy.array([0.0, 6.0, -spawn_dist], dtype=numpy.float64)
                    # Respect global cap
                    if total_created >= max_visual:
                        continue
                    if d == 'N':
                        pos = numpy.array([-lane_offset, 6.0, -spawn_dist], dtype=numpy.float64)
                    elif d == 'S':
                        pos = numpy.array([lane_offset, 6.0, spawn_dist], dtype=numpy.float64)
                    elif d == 'W':
                        pos = numpy.array([-spawn_dist, 6.0, -lane_offset], dtype=numpy.float64)
                    else:  # E
                        pos = numpy.array([spawn_dist, 6.0, lane_offset], dtype=numpy.float64)
                    lfq = make_visual_lifter(visual_id, d, pos)
                    visual_id += 1
                    total_created += 1
                    queues[d].append(lfq)
            # traffic light phase
            cycle = int(sim_time // TS) % 2 if TS > 0 else 0
            if cycle == 0:
                green = ['N','S']
            else:
                green = ['E','W']

            # serve vehicles from queues when green using fractional capacity (works for dt<1)
            expected = service_rate * dt
            for d in green:
                # check intersection occupancy by conflicting approaches; if occupied, delay serving
                conflicting = ['E','W'] if d in ['N','S'] else ['N','S']
                intersection_entry = spawn_dist - 20.0
                occupied = any((v['progress'] >= intersection_entry and v['progress'] <= (v['total'] - intersection_entry)) for v in moving if v['approach'] in conflicting)
                if occupied:
                    serve = 0
                else:
                    serve = min(len(queues[d]), int(math.floor(expected)))
                    frac = expected - math.floor(expected)
                    if len(queues[d]) - serve > 0 and random.random() < frac:
                        serve += 1
                for i in range(serve):
                    lfq = queues[d].pop(0)
                    # spawn queued lifter into moving with progress=0
                    lf = lfq
                    moving.append({'lifter': lf, 'approach': d, 'progress': 0.0, 'total': spawn_dist * 2.0, 'state': 'crossing'})

            # update moving vehicles using progress-based spacing
            min_gap = 12.0  # minimum gap between vehicles (in same units as progress)
            move_amount = service_rate * dt * 60.0
            # group by approach and sort by progress descending (closest to center first)
            by_app = {d: [] for d in ['N','S','E','W']}
            for v in moving:
                by_app[v['approach']].append(v)

            new_moving = []
            for d, lst in by_app.items():
                # sort closest-first (highest progress first)
                lst.sort(key=lambda x: x['progress'], reverse=True)
                new_progress_vals = {}
                prev_new = None
                for v in lst:
                    old_p = v['progress']
                    # desired new progress
                    desired = min(v['total'], old_p + move_amount)
                    if prev_new is None:
                        new_p = desired
                    else:
                        # ensure gap: this vehicle's new progress must be <= prev_new - min_gap
                        max_allowed = prev_new - min_gap
                        # cannot move backward: new_p >= old_p
                        new_p = min(desired, max_allowed)
                        if new_p < old_p:
                            new_p = old_p
                    prev_new = new_p
                    new_progress_vals[id(v)] = new_p

                # apply new progress and compute positions; collect survivors
                for v in lst:
                    new_p = new_progress_vals[id(v)]
                    v['progress'] = new_p
                    # compute world pos from progress
                    # apply lateral lane offsets so opposite approaches use different lanes
                    if v['approach'] == 'N':
                        x = -lane_offset
                        z = -spawn_dist + new_p
                        v['lifter'].Position = numpy.array([x, 6.0, z], dtype=numpy.float64)
                    elif v['approach'] == 'S':
                        x = lane_offset
                        z = spawn_dist - new_p
                        v['lifter'].Position = numpy.array([x, 6.0, z], dtype=numpy.float64)
                    elif v['approach'] == 'W':
                        x = -spawn_dist + new_p
                        z = -lane_offset
                        v['lifter'].Position = numpy.array([x, 6.0, z], dtype=numpy.float64)
                    else:  # E
                        x = spawn_dist - new_p
                        z = lane_offset
                        v['lifter'].Position = numpy.array([x, 6.0, z], dtype=numpy.float64)

                    # check if finished crossing
                    if v['progress'] >= v['total']:
                        passed[v['approach']] += 1
                        # do not re-add
                    else:
                        # set angle for lifter facing direction of travel
                        if v['approach'] in ('N','S'):
                            ang = 180.0 if v['approach'] == 'S' else 0.0
                        else:
                            ang = 270.0 if v['approach'] == 'E' else 90.0
                        v['lifter'].angle = ang
                        new_moving.append(v)

            moving = new_moving

            # render scene: clear and draw ground, roads and lifters
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # draw simple roads as quads
            glPushMatrix()
            glColor3f(0.2,0.2,0.2)
            road_w = 40.0
            # horizontal road
            glBegin(GL_QUADS)
            glVertex3f(-Settings.DimBoard, 0.1, road_w/2)
            glVertex3f(-Settings.DimBoard, 0.1, -road_w/2)
            glVertex3f(Settings.DimBoard, 0.1, -road_w/2)
            glVertex3f(Settings.DimBoard, 0.1, road_w/2)
            glEnd()
            # vertical road
            glBegin(GL_QUADS)
            glVertex3f(road_w/2, 0.1, -Settings.DimBoard)
            glVertex3f(-road_w/2, 0.1, -Settings.DimBoard)
            glVertex3f(-road_w/2, 0.1, Settings.DimBoard)
            glVertex3f(road_w/2, 0.1, Settings.DimBoard)
            glEnd()
            glPopMatrix()

            # draw stop lines as thin quads
            glColor3f(1.0,1.0,1.0)
            # north stop line (z = -stop_line)
            glBegin(GL_QUADS)
            glVertex3f(-20, 0.2, -stop_line)
            glVertex3f(20, 0.2, -stop_line)
            glVertex3f(20, 0.2, -stop_line+1)
            glVertex3f(-20, 0.2, -stop_line+1)
            glEnd()

            # draw lifters (positions already updated in movement step)
            for v in moving:
                lf = v['lifter']
                # angle already set during movement update, but ensure it's present
                if not hasattr(lf, 'angle'):
                    lf.angle = 0
                lf.draw()

            # draw queued lifters and position them as a queue up to the stop line
            for d in ['N','S','W','E']:
                q = queues[d]
                for j, lfq in enumerate(q[:10]):
                    # compute queued position relative to stop line
                    offset = (j + 1) * 8.0
                    if d == 'N':
                        x = 0.0
                        z = -stop_line - offset
                    elif d == 'S':
                        x = 0.0
                        z = stop_line + offset
                    elif d == 'W':
                        x = -stop_line - offset
                        z = 0.0
                    else:  # E
                        x = stop_line + offset
                        z = 0.0
                    lfq.Position = numpy.array([x, 6.0, z], dtype=numpy.float64)
                    lfq.draw()

            pygame.display.flip()
            pygame.time.wait(int(max(1, dt * 1000)))
            sim_time += dt

            if sim_time >= next_print:
                cycle = int(sim_time // TS) % 2 if TS > 0 else 0
                phase = 'NS' if cycle == 0 else 'EW'
                print(f"[t={sim_time:.1f}s] Phase={phase} Queues: N={len(queues['N'])} S={len(queues['S'])} E={len(queues['E'])} W={len(queues['W'])} | Passed: N={passed['N']} S={passed['S']} E={passed['E']} W={passed['W']}")
                next_print += max(1.0, duration / 10.0)

        total = sum(passed.values())
        print('\n--- Resumen Interseccion 3D ---')
        for k in ['N','S','E','W']:
            print(f"Via {k}: Pasaron {passed[k]} autos")
        print(f"Total autos pasaron: {total}")
    else:
        sim = IntersectionSim(lifters, TS, P, duration)
        sim.run()
        sim.summary()


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