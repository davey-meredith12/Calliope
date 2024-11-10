import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Cube:
    _vertices = (
        # Column 0 - Left:   -1, Right: +1
        # Column 1 - Bottom: -1, Top:   +1
        # Column 2 - Front:  -1, Back:  +1
        (+1, -1, -1), # 0: FRB *
        (+1, +1, -1), # 1: FRT
        (-1, +1, -1), # 2: FLT *
        (-1, -1, -1), # 3: FLB
        (+1, -1, +1), # 4: BRB
        (+1, +1, +1), # 5: BRT *
        (-1, +1, +1), # 6: BLT
        (-1, -1, +1), # 7: BLB *
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

    def draw(self):
        glColor(0.0, 0.0, 0.0, 1.0)
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
        gluPerspective(45, self.width / self.height, 0.005, 100.0)
        glTranslatef(0.0, 0.0, -5)
        glRotatef(0, 0, 0, 0)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pygame.display.flip()
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._cube.draw()
        pygame.display.flip()

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
            pygame.display.flip()
            pygame.time.wait(10)
        self.on_cleanup()

if __name__ == '__main__':
    app = App()
    app.on_execute()
