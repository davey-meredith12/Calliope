import pygame

from calliope.music_queue import MusicQueue, Note, START
from calliope.twinkle import TWINKLE_SONG, TWINKLE_NOTES, TWINKLE_BPM

BLANK = [
    "'&=4========='========'========'========'========'========!",
    "'&============'========'========'========'========'========!"]

NOTE_GLYPH = {
    # Whole Notes
    Note(4, "A", 1): "p======", Note(4, "B", 1): "q======", Note(4, "C", 1): "r======",
    Note(4, "D", 1): "s======", Note(4, "E", 1): "t======", Note(4, "F", 1): "u======",
    Note(4, "G", 1): "v======", Note(5, "A", 1): "w======", Note(5, "B", 1): "x======",
    Note(5, "C", 1): "y======", Note(5, "D", 1): "z======", Note(5, "E", 1): "{======",
    Note(5, "F", 1): "|======", Note(5, "G", 1): "}======", Note(6, "A", 1): "~======",

    # Half Notes
    Note(4, "A", 2): "`===", Note(4, "B", 2): "a===", Note(4, "C", 2): "b===",
    Note(4, "D", 2): "c===", Note(4, "E", 2): "d===", Note(4, "F", 2): "e===",
    Note(4, "G", 2): "f===", Note(5, "A", 2): "g===", Note(5, "B", 2): "h===",
    Note(5, "C", 2): "i===", Note(5, "D", 2): "j===", Note(5, "E", 2): "k===",
    Note(5, "F", 2): "l===", Note(5, "G", 2): "m===", Note(6, "A", 2): "n===",

    # Quarter Notes
    Note(4, "A", 4): "P=", Note(4, "B", 4): "Q=", Note(4, "C", 4): "R=",
    Note(4, "D", 4): "S=", Note(4, "E", 4): "T=", Note(4, "F", 4): "U=",
    Note(4, "G", 4): "V=", Note(5, "A", 4): "W=", Note(5, "B", 4): "X=",
    Note(5, "C", 4): "Y=", Note(5, "D", 4): "Z=", Note(5, "E", 4): "[=",
    Note(5, "F", 4): "\=", Note(5, "G", 4): "]=", Note(6, "A", 4): "^=",

    # Eighth Notes
    Note(4, "A", 8): "@", Note(4, "B", 8): "A", Note(4, "C", 8): "B",
    Note(4, "D", 8): "C", Note(4, "E", 8): "D", Note(4, "F", 8): "E",
    Note(4, "G", 8): "F", Note(5, "A", 8): "G", Note(5, "B", 8): "H",
    Note(5, "C", 8): "I", Note(5, "D", 8): "J", Note(5, "E", 8): "K",
    Note(5, "F", 8): "L", Note(5, "G", 8): "M", Note(6, "A", 8): "N"
}
NOTE_CHR = "pqrstuvwxyz{|}~`abcdefgohijklmnPQRSTUVW_XYZ[\]^@ABCDEFGOHIJKLMN"
NOTE_LTR = "ABCDEFGABCDEFGAABCDEFGABBCDEFGAABCDEFGABBCDEFGAABCDEFGABBCDEFGA"

TIMING = "'1=2=3=4=5=6!"

# Starts with "p" as A note
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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
VIOLET = (255, 0, 255)

class UserInterface:
    _song: [str]
    _bpm: int
    _queue: MusicQueue
    _size: tuple[int, int]
    _width: int
    _height: int
    _clock: pygame.time.Clock
    _surface: pygame.SurfaceType
    _running: bool
    _note_font: pygame.font.Font
    _whole_size: tuple[int, int]
    _text_font: pygame.font.Font

    _beat_count: int
    _score: list[tuple[pygame.Surface, tuple[int, int]]]
    _note: list[tuple[pygame.Surface, tuple[int, int]]]
    _text: list[tuple[pygame.Surface, tuple[int, int]]]
    _pointer: tuple[pygame.Surface, tuple[int, int]]
    _note_dict: dict[str, str]

    _played: list[str]
    _position: int

    def __init__(self, song, bpm, queue):
        self._song = song
        self._bpm = bpm
        self._queue = queue
        self.size = self.width, self.height = 1280, 960
        self._running = False
        self._note_dict = {}
        for key, ltr in zip(NOTE_CHR, NOTE_LTR):
            self._note_dict[key] = ltr

        self._played = BLANK
        self._position = 1

    def _on_start(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._beat_count = 0

        self._surface = pygame.display.set_mode(self.size)
        self._text_font = pygame.font.SysFont('Futura', 32)
        self._note_font = pygame.font.Font('Musiqwik.ttf', 70)
        self._text = [
            (self._create_label(self._song[0]), (7, 25)),
            (self._create_label(self._song[1]), (7, 200)),
            (self._create_label(self._played[0]), (7, 550)),
            (self._create_label(self._played[1]), (7, 700)),
        ]
        self._note = [
            (self._note_font.render(self._song[0], True, BLACK), (7, 50)),
            (self._note_font.render(self._song[1], True, BLACK), (7, 225)),
            (self._note_font.render(self._played[0], True, BLACK), (7, 575)),
            (self._note_font.render(self._played[1], True, BLACK), (7, 725)),
        ]
        self._beat = [
            (self._create_beat(GREEN, 100, 1), (1050, 150)),
            (self._create_beat(GREEN, 100, 50), (1050, 150))
        ]
        self._update_pointer(BLACK)
        pygame.display.set_caption('Calliope')
        pygame.time.set_timer(pygame.USEREVENT, 30_000 // self._bpm)
        return True

    def _on_event(self, event):
        if event.type == pygame.USEREVENT:
            self._beat_count += 1
        elif event.type == pygame.QUIT:
            self._running = False

    def _on_update(self):
        note = self._queue.poll()
        if note:
            if note.length == START:
                self._note_started(note)
                self._update_pointer(VIOLET)
            else:
                self._update_pointer(BLACK)
                self._on_note_played(note)
        self._surface.fill(WHITE)
        for notes in self._note:
            self._surface.blit(*notes)
        for text in self._text:
            self._surface.blit(*text)
        self._surface.blit(*self._beat[self._beat_count % 2])
        self._surface.blit(*self._pointer, None, pygame.BLEND_SUB)
        pygame.display.flip()
        self._clock.tick(20)

    def _create_label(self, notes):
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

    def _create_beat(self, color, size, radius):
        beat = pygame.Surface((size, size))
        beat.fill(WHITE)
        pygame.draw.circle(beat, color, (size//2, size//2), radius)
        return beat

    def _update_pointer(self, color):
        row = self._position // 54
        indent = 1 if row > 0 else 0
        offset = self._position % 54 + 4 + indent
        widths = list(metrics[4] for metrics in self._note_font.metrics(self._song[row]))
        (x, y) = self._note[row][1]
        x += sum(widths[:offset])
        y += 15 # Shift the bar down a bit
        pointer = pygame.Surface((widths[offset], self._note_font.get_height() - 20))
        pointer.fill(color)
        self._pointer = (pointer, (x, y))

    def _note_started(self, note):
        pass

    def _on_note_played(self, note):
        row = self._position // 54
        indent = 1 if row > 0 else 0
        offset = self._position % 54 + 4 + indent
        stanza = self._played[row]
        glyph = NOTE_GLYPH[note]
        width = len(glyph)
        stanza = stanza[:offset] + glyph + stanza[offset + width:]
        self._played[row] = stanza
        self._note[row + 2] = (
            self._note_font.render(stanza, True, BLACK),
            self._note[row + 2][1])
        self._text[row + 2] = (
            self._create_label(stanza),
            self._text[row + 2][1])
        self._position += width
        if self._position % 9 == 0:
            self._position += 1

    def run(self):
        self._running = self._on_start()
        while self._running:
            for event in pygame.event.get():
                self._on_event(event)
            self._on_update()
        pygame.quit()


if __name__ == "__main__":
    queue = MusicQueue()
    ui = UserInterface(TWINKLE_SONG, TWINKLE_BPM, queue)
    queue.play(TWINKLE_NOTES, TWINKLE_BPM)
    ui.run()
