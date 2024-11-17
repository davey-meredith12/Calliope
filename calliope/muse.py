from typing import Callable

import pygame
from pygame import TEXTINPUT

add: Callable[[int, int], int] = lambda i, j: i + j

SCORE = (
    "'&=4=R=R=V=V='W=W=f==='U=U=T=T='S=S=b==='V=V=U=U='T=T=c==!",
    "'&====V=V=U=U='T-=T=c==='R=R=V=V='W=W=f==='U=U=T=T='S=S=b==!")

TIMING = "'1=2=3=4=5=6!"

# Starts with backtick (`) as A note
#              |  a b c d e f g a b c d e f g a|
WHOLE_NOTES = "'&=p=q=r=s=t=u=v=w=x=y=z={=|=}=~!"

# Starts with backtick (`) as A note
#             |  a b c d e f g a b B C D E F G A|
HALF_NOTES = "'&=`=a=b=c=d=e=f=g=o=h=i=j=k=l=m=n!"

# Starts with P as A note
#                |  a b c d e f g a b B C D E F G A|
QUARTER_NOTES = "'&=P=Q=R=S=T=U=V=W=_=X=Y=Z=[=\=]=^!"

# Starts with @ as A note
#               |  a b c d e f g a b B C D E F G A|
EIGHTH_NOTES = "'&=@=A=B=C=D=E=F=G=O=H=I=J=K=L=M=N!"

WHOLE_TEXT = "A   B   C   D   E   F   G   A   B   C   D   E   F   G   A"
NOTE_TEXT = "A B C D E F G A B B C D E F G A"

class UserInterface:
    size: tuple[int, int]
    width: int
    height: int
    _clock: pygame.time.Clock
    _surface: pygame.SurfaceType
    _running: bool
    _whole_font: pygame.font.Font
    _text_font: pygame.font.Font
    _note_font: pygame.font.Font
    _score: list[tuple[pygame.Surface, tuple[int, int]]]
    _notes: list[tuple[pygame.Surface, tuple[int, int]]]
    _text: list[tuple[pygame.Surface, tuple[int, int]]]

    def __init__(self):
        self.size = self.width, self.height = 1280, 960
        self._running = False

    def _on_start(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._surface = pygame.display.set_mode(self.size)
        self._whole_font = pygame.font.SysFont('Futura', 32)
        self._text_font = pygame.font.SysFont('Futura', 32)
        self._note_font = pygame.font.Font('Musiqwik.ttf', 70)
        self._score = [
            (self._note_font.render(SCORE[0], True, (0, 0, 0)), (7, 25)),
            (self._note_font.render(SCORE[1], True, (0, 0, 0)), (7, 175))
        ]
        self._notes = [
            (self._note_font.render(WHOLE_NOTES, True, (0, 0, 0)), (7, 375)),
            (self._note_font.render(TIMING, True, (0, 0, 0)), (900, 375)),
            (self._note_font.render(HALF_NOTES, True, (0, 0, 0)), (7, 550)),
            (self._note_font.render(QUARTER_NOTES, True, (0, 0, 0)), (647, 550)),
            (self._note_font.render(EIGHTH_NOTES, True, (0, 0, 0)), (7, 725))
        ]
        self._text = [
            (self._whole_font.render(WHOLE_TEXT, True, (0, 0, 0)), (80, 350)),
            (self._text_font.render(NOTE_TEXT, True, (0, 0, 0)), (80, 525)),
            (self._text_font.render(NOTE_TEXT, True, (0, 0, 0)), (715, 525)),
            (self._text_font.render(NOTE_TEXT, True, (0, 0, 0)), (80, 700)),
        ]

        pygame.display.set_caption('Calliope')
        pygame.time.set_timer(pygame.USEREVENT, 250)

        # Initial view
        return True

    def _on_event(self, event):
        if event.type == pygame.USEREVENT:
            pass
        elif event.type == pygame.QUIT:
            self._running = False

    def _on_update(self):
        self._surface.fill((255, 255, 255))
        for score in self._score:
            self._surface.blit(*score)
        for notes in self._notes:
            self._surface.blit(*notes)
        for text in self._text:
            self._surface.blit(*text)
        pygame.display.flip()
        self._clock.tick(60)

    def run(self):
        self._running = self._on_start()
        while self._running:
            for event in pygame.event.get():
                self._on_event(event)
            self._on_update()
        pygame.quit()


if __name__ == '__main__':
    app = UserInterface()
    app.run()
