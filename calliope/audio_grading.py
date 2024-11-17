import time
import numpy as np
from frequency_note_conversion import note_to_freq

FREQ_DIFF_ALLOWED = 1

def _correct_contains_input_tolerance(input: float, arr) -> bool:
    for i in range(len(arr)):
        if abs(input - arr[i]) <= FREQ_DIFF_ALLOWED:
            return True
    return False

# tune builder, takes notes and gives back frequencies to use in compare
def _notes_arr_to_freq_arr(notes):
    to_return = []
    for note_arr in notes:
        freq = []
        for note in note_arr:
            freq.append(note_to_freq(note))
            to_return.append(freq)
    return to_return

class AudioGrading:
    tune_arr: list[list[str]]
    bpm: int
    correct_notes: list[list[float]]
    start_time: float

    def __init__(self, tune_arr: list[list[str]], bpm: int):
        self.tune_arr = tune_arr
        self.bpm = bpm
        self.correct_notes = _notes_arr_to_freq_arr(tune_arr)
        self.start_time = time.time()

    # Compared one at a time against the correct_notes
    # Must be called timed based on the beat, timed for quarter notes currently
    def _compare(self, input: list[float], time_since_start: float):
        arr_loc = round(time_since_start / (60 / self.bpm))

        if arr_loc >= len(self.correct_notes):
            return
        #compare arrays with tolerance of values,try and match the input against the output
        output = []
        for i in range(len(input)):
            output.append(_correct_contains_input_tolerance(input[i], self.correct_notes[arr_loc]))
        return output

    #expects to be sent a new "input" on each call
    #boolean array indexes match input indexes
    def grade(self) -> list[bool]:
        while True:
            current_time = time.time()
            time_since_start = current_time - self.start_time
            input: list[float] = yield
            yield self._compare(input, time_since_start)


#currently written for quarter notes
#simple_tune = [["A4"], ["R"], ["A4"], ["R"]]








#
# if __name__ == '__main__':
#     print("running")
#     print(simple_tune)
#     tune_freq = notes_arr_to_freq_arr(simple_tune)
#     print(tune_freq)
#
#
#
#
#     user_input = [[440.3, 444], [0], [441], [0]]
#     for i in range(4):
#         timeToSleep = 60/BPM
#         timing = i * timeToSleep
#         print(compare(user_input[i], timing))
#         # print(timing)
#         time.sleep(timeToSleep)