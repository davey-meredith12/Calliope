import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Cube:
    _vertices = (
        # Column 0 - Left:   -1, Right: +1
        # Column 1 - Bottom: -1, Top:   +1
        # Column 2 - Front:  -1, Back:  +1
        (+1, -1, -1), # *0: Front, Right, Bottom
        (+1, +1, -1), #  1: Front, Right, Top
        (-1, +1, -1), # *2: Front, Left,  Top
        (-1, -1, -1), #  3: Front, Left,  Bottom
        (+1, -1, +1), #  4: Back,  Right, Bottom
        (+1, +1, +1), # *5: Back,  Right, Top
        (-1, +1, +1), #  6: Back,  Left,  Top
        (-1, -1, +1), # *7: Back,  Left,  Bottom
    )
    _edges = (
        (0, 1), # FRB - FRT
        (0, 3), # FRB - FLB
        (0, 4), # FRB - BRB
        (2, 1), # FLT - FRT
        (2, 3), # FLT - FLB
        (2, 6), # FLT - BLT
        (5, 1), # BRT - FRT
        (5, 4), # BRT - BRB
        (5, 6), # BRT - BLT
        (7, 3), # BRB - FLB
        (7, 4), # BRB - BRB
        (7, 6), # BRB - BLT
    )
    _faces = (
        (0, 1, 2, 3),  # Front
        (4, 5, 6, 7),  # Back
        (2, 3, 7, 6),  # Left
        (0, 1, 5, 4),  # Right
        (1, 2, 6, 5),  # Top
        (0, 3, 7, 4),  # Bottom
    )
    _colors = (
        (1.0, 0.0, 0.0), # Red
        (0.0, 1.0, 0.0), # Green
        (0.0, 0.0, 1.0), # Blue
        (1.0, 1.0, 0.0), # Yellow
        (0.0, 1.0, 1.0), # Cyan
        (1.0, 0.0, 1.0), # Magenta
    )

    def draw(self):
        glBegin(GL_QUADS)
        for i, face in enumerate(self._faces):
            glColor3fv(self._colors[i])
            for vertex in face:
                glVertex3fv(self._vertices[vertex])
        glEnd()

        glColor3fv((0.0, 0.0, 0.0))
        glLineWidth(2)
        glBegin(GL_LINES)
        for edge in self._edges:
            for vertex in edge:
                glVertex3fv(self._vertices[vertex])
        glEnd()


class App:
    size: (int, int)
    width: int
    height: int
    _clock: pygame.time.Clock
    _surface: pygame.SurfaceType
    _running: bool
    _cube: Cube

    def __init__(self):
        self.size = self.width, self.height = 1280, 960
        self._running = False
        self._cube = Cube()

    def start(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._surface = pygame.display.set_mode(self.size, pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.display.set_caption('Muse')
        pygame.time.set_timer(pygame.USEREVENT, 10)

        gluPerspective(45, self.width / self.height, 0.005, 100.0)
        glTranslatef(0.0, 0.0, -5)
        glRotatef(0, 0, 0, 0)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pygame.display.flip()
        return True

    def on_event(self, event):
        if event.type == pygame.USEREVENT:
            glRotatef(1, 3, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self._cube.draw()
            pygame.display.flip()
        elif event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self._running = self.start()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == '__main__':
    app = App()
    app.on_execute()
