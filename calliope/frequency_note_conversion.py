import numpy

def freq_to_note(frequency):
    if frequency <= 0:
        return
    #key number = 12 log_2 (f/440) + 49:
    key_number = round(12 * numpy.log2(frequency/440)+49)
    note_dict = {
        0: "G#",
        1: "A",
        2: "A#",
        3: "B",
        4: "C",
        5: "C#",
        6: "D",
        7: "D#",
        8: "E",
        9: "F",
        10: "F#",
        11: "G"
    }
    note_name = note_dict[(key_number % 12)]
    if (key_number % 12) - 1 < 3:
        note_number = (key_number // 12)
    else:
        note_number = (key_number // 12) + 1
    note = note_name + str(note_number)
    return note

def note_to_freq(note):
    if(note == "R"):
        return 0

    if(note[1] == "#"):
        note_number = int(note[2])
        note_name = note[0] + note[1]
    else:
        note_name = note[0]
        note_number = int(note[1])

    #octave difference from A4
    octave_semitone = (note_number - 4)*12
    note_dict = {
        "C": -9,
        "C#": -8,
        "D": -7,
        "D#": -6,
        "E": -5,
        "F": -4,
        "F#": -3,
        "G": -2,
        "G#": -1,
        "A": 0,
        "A#": 1,
        "B": 2
    }
    #note difference from A4
    note_semitone = note_dict[note_name]

    semitone_difference = note_semitone + octave_semitone
    freq = 2**(semitone_difference/12) * 440
    return freq






