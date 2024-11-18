import pygame

NOTE_KEY = "pqrstuvwxyz{|}~`abcdefgohijklmnPQRSTUVW_XYZ[\]^@ABCDEFGOHIJKLMN"
NOTE_LTR = "ABCDEFGABCDEFGAABCDEFGABBCDEFGAABCDEFGABBCDEFGAABCDEFGABBCDEFGA"

TWINKLE = (
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

WHOLE_TEXT = "ABCDEFGABCDEFGA"
PARTIAL_TEXT = "ABCDEFGABBCDEFGA"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class UserInterface:
    size: tuple[int, int]
    width: int
    height: int
    _clock: pygame.time.Clock
    _surface: pygame.SurfaceType
    _running: bool
    _note_font: pygame.font.Font
    _whole_size: tuple[int, int]
    _text_font: pygame.font.Font
    
    _score: list[tuple[pygame.Surface, tuple[int, int]]]
    _note: list[tuple[pygame.Surface, tuple[int, int]]]
    _text: list[tuple[pygame.Surface, tuple[int, int]]]
    _note_dict: dict[str, str]

    def __init__(self):
        self.size = self.width, self.height = 1280, 960
        self._running = False
        self._note_dict = {}
        for key, ltr in zip(NOTE_KEY, NOTE_LTR):
            self._note_dict[key] = ltr

    def _on_start(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._surface = pygame.display.set_mode(self.size)
        self._text_font = pygame.font.SysFont('Futura', 32)
        self._note_font = pygame.font.Font('Musiqwik.ttf', 70)
        self._text = [
            (self._label(TWINKLE[0]), (7, 25)),
            (self._label(TWINKLE[1]), (7, 200)),
            (self._label(WHOLE_NOTES), (7, 375)),
            (self._label(HALF_NOTES), (7, 550)),
            (self._label(QUARTER_NOTES), (647, 550)),
            (self._label(EIGHTH_NOTES), (7, 725)),
        ]
        self._note = [
            (self._note_font.render(TWINKLE[0], True, BLACK), (7, 50)),
            (self._note_font.render(TWINKLE[1], True, BLACK), (7, 225)),
            (self._note_font.render(WHOLE_NOTES, True, BLACK), (7, 400)),
            (self._note_font.render(TIMING, True, BLACK), (900, 400)),
            (self._note_font.render(HALF_NOTES, True, BLACK), (7, 575)),
            (self._note_font.render(QUARTER_NOTES, True, BLACK), (647, 575)),
            (self._note_font.render(EIGHTH_NOTES, True, BLACK), (7, 750))
        ]
        pygame.display.set_caption('Calliope')
        pygame.time.set_timer(pygame.USEREVENT, 250)
        return True

    def _on_event(self, event):
        if event.type == pygame.USEREVENT:
            pass
        elif event.type == pygame.QUIT:
            self._running = False

    def _on_update(self):
        self._surface.fill(WHITE)
        for notes in self._note:
            self._surface.blit(*notes)
        for text in self._text:
            self._surface.blit(*text)
        pygame.display.flip()
        self._clock.tick(60)

    def _label(self, notes):
        widths = list(metrics[4] for metrics in self._note_font.metrics(notes))
        height = self._text_font.get_height()
        label = pygame.Surface((sum(widths), height))
        label.fill(WHITE)
        position = 0
        for (i, width) in enumerate(widths):
            letter = self._note_dict.get(notes[i])
            if letter:
                label.blit(self._text_font.render(letter, True, BLACK), (position, 0))
            position += width
        return label

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
