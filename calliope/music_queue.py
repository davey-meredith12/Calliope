import queue
import threading, time
from collections import namedtuple

Note = namedtuple("Note", ["octave", "letter", "length"])

START = 0
WHOLE = 1
HALF = 2
QUARTER = 4
EIGHTH = 8

class MusicQueue:
    _played: queue.Queue
    _thread: threading.Thread
    _stop: bool

    def __init__(self):
        self._played = queue.Queue()

    def play(self, notes, bpm):
        self._thread = threading.Thread(target=self._run, args=[notes, bpm], daemon=True)
        self._thread.start()

    def put(self, note):
        self._played.put(note)

    def poll(self):
        return None if self._played.empty() else self._played.get()

    def _run(self, notes, bpm):
        seconds = 60.0 / bpm
        time.sleep(5.0) # Pause before first note
        for note in notes:
            delay = seconds / 2 # Default to EIGHTH notes
            if note.length == QUARTER:
                delay = seconds
            elif note.length == HALF:
                delay = seconds * 2
            elif note.length == WHOLE:
                delay = seconds * 4
            self.put(Note(note.octave, note.letter, START))
            time.sleep(delay)
            self.put(note)

