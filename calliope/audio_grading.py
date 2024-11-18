import time
import numpy as np
from frequency_note_conversion import note_to_freq, freq_to_note


def _correct_contains_input(input: str, arr) -> bool:
    for i in range(len(arr)):
        if input == arr[i-1]:
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

# def _notes_arr_to_bool_arr(notes):
#     to_return = []
#     for note_arr in notes:
#         freq = []
#         for note in note_arr:
#             freq.append(False)
#         to_return.append(freq)
#     return to_return


class AudioGrading:
    tune_arr: list[list[str]]
    bpm: int
    correct_freqs: list[list[float]]
    correct_notes: list[list[str]]
    start_time: float

    def __init__(self, tune_arr: list[list[str]], bpm: int):
        self.tune_arr = tune_arr
        self.bpm = bpm
        self.correct_freqs = _notes_arr_to_freq_arr(tune_arr)
        self.correct_notes = tune_arr
        self.start_time = time.time()

    # Compared one at a time against the correct_notes
    # Must be called timed based on the beat, timed for quarter notes currently
    def _compare(self, input: list[float], time_since_start: float):
        arr_loc = round(time_since_start / (60 / self.bpm))
        note_input = []
        for freq in input:
            note_input.append(freq_to_note(freq))

        if arr_loc >= len(self.correct_freqs):
            return
        #compare arrays with tolerance of values,try and match the input against the output
        output = []
        for i in range(len(input)):
            i_correct = _correct_contains_input(note_input[i], self.correct_notes[arr_loc])
            #self.bool_notes[arr_loc][i] = i_correct
            output.append(i_correct)
        return output

    #expects to be sent a new "input" on each call
    #boolean array indexes match input indexes
    def grade(self) -> list[bool]:
        while True:
            current_time = time.time()
            time_since_start = current_time - self.start_time
            input: list[float] = yield
            yield self._compare(input, time_since_start)

    # def get_final_grade(self):
    #     correct = 0
    #     total = 0
    #     for bool_arr in self.bool_notes:
    #         for bool in bool_arr:
    #             total += 1
    #             if bool == True:
    #                 correct += 1
    #
    #     return correct/total

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