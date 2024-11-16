from typing import Callable

import pygame

add: Callable[[int, int], int] = lambda i, j: i + j

SCORE = (
    "'&=4=R=R=V=V='W=W=f==='U=U=T=T='S=S=b==='V=V=U=U='T=T=c==!",
    "'&====V=V=U=U='T-=T=c==='R=R=V=V='W=W=f==='U=U=T=T='S=S=b==!"
)

class App:
    size: tuple[int, int]
    width: int
    height: int
    _clock: pygame.time.Clock
    _surface: pygame.SurfaceType
    _running: bool
    _font: pygame.font.Font
    _score: list[pygame.Surface] = [None, None]
    _score_pos: list[tuple[int, int]] = [None, None]

    def __init__(self):
        self.size = self.width, self.height = 1280, 960
        self._running = False

    def on_start(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._surface = pygame.display.set_mode(self.size)
        self._font = pygame.font.Font('Musiqwik.ttf', 34)
        self._score[0] = self._font.render(SCORE[0], True, (0, 0, 0))
        self._score_pos[0] = (10, 10)
        self._score[1] = self._font.render(SCORE[1], True, (0, 0, 0))
        self._score_pos[1] = (10, 100)

        pygame.display.set_caption('Muse')
        pygame.time.set_timer(pygame.USEREVENT, 250)

        # Initial view
        return True

    def on_event(self, event):
        if event.type == pygame.USEREVENT:
            pass
        elif event.type == pygame.QUIT:
            self._running = False

    def on_update(self):
        self._surface.fill((255, 255, 255))
        self._surface.blit(self._score[0], self._score_pos[0])
        self._surface.blit(self._score[1], self._score_pos[1])
        pygame.display.flip()
        self._clock.tick(60)

    def run(self):
        self._running = self.on_start()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_update()
        pygame.quit()

if __name__ == '__main__':
    app = App()
    app.run()
