import threading, time
from collections import namedtuple

Note = namedtuple("Note", ["note", "time"])

START = 0
WHOLE = 1
HALF = 2
QUARTER = 4
EIGHTH = 8

class MusicQueue:
    _played: [Note]
    _thread: threading.Thread

    def __init__(self):
        self._played = []

    def simulate(self, notes, bpm):
        self._thread = threading.Thread(target=self._play, args=[notes, bpm])

    def _play(self, notes, bpm):
        millis = 60_000 // bpm
        for note in notes:
            delay = millis # Default to EIGHTH notes
            if note.time == QUARTER:
                delay = millis * 2
            elif note.time == HALF:
                delay = millis * 4
            elif note.time == WHOLE:
                delay = millis * 8
            time.sleep(delay)
            self._played.append(note)
