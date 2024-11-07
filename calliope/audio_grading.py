import time
import numpy as np
from frequency_note_conversion import note_to_freq

#currently written for quarter notes
simple_tune = [["A4"], ["R"], ["A4"], ["R"]]

correct_notes = [[440] ,[0],[440],[0]]
BPM = 60
FREQ_DIFF_ALLOWED = 1
#correct notes and correct timing length will be the same

#tune builder, takes notes and gives back frequencies to use in compare
def notes_arr_to_freq_arr(notes):
    to_return = []
    for note_arr in notes:
        freq = []
        for note in note_arr:
            freq.append(note_to_freq(note))
        to_return.append(freq)
    return to_return

#compared one at a time against the correct_notes
#Must be called timed based on the beat
def compare(input: list[float], time_since_start: float):
    arr_loc = round(time_since_start/(60/BPM))
    print("looking at " , arr_loc)
    print("comparing ", input, " against ", correct_notes[arr_loc])
    #compare arrays with tolerance of values
    return np.isclose(input, correct_notes[arr_loc], atol = FREQ_DIFF_ALLOWED)

if __name__ == '__main__':
    print("running")
    print(simple_tune)
    tune_freq = notes_arr_to_freq_arr(simple_tune)
    print(tune_freq)




    # user_input = [[440.3, 444], [0], [441], [0]]
    # for i in range(4):
    #     timeToSleep = 60/BPM
    #     timing = i * timeToSleep
    #     print(compare(user_input[i], timing))
    #     print(timing)
    #     time.sleep(timeToSleep)