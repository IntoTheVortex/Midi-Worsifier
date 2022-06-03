import sys
import numpy as np
from mido import MidiFile, tick2second
import sine_by_freq

#https://soundprogramming.net/file-formats/midi-note-frequencies/
NOTES = 'notes.txt'
TEST = 'test_3.wav'


#info:
'''
changed library to this:
https://mido.readthedocs.io/en/latest/installing.html
'''

## TODO
    # time is a problem



def read(midi_file):
    mid = MidiFile(midi_file)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_off':
                return read_midi_note_off(midi_file)

    #else no note_off messages in midi:
    return read_midi(midi_file)


def read_midi_note_off(midi_file):
    mid = MidiFile(midi_file)
    midi_length = mid.length

    #tempo:
    tempo = 500000 #default tempo from mido 

    all_notes = []
    input_notes = []
    deltas = []
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        input_notes = input_notes.clear
        input_notes = []
        for msg in track:
            print(msg) #TODO remove
            if msg.type == 'note_off':
                delta = tick2second(msg.time, mid.ticks_per_beat, tempo)
                deltas.append(delta)
                input_notes.append((msg.note, delta))
            elif msg.type == 'set_tempo':
                tempo = msg.tempo

        if(input_notes):
            all_notes.append(input_notes)

    ave_delta = sum(deltas)/len(deltas)
    return all_notes, ave_delta
    


def read_midi(midi_file):
    #ref https://mido.readthedocs.io/en/latest/midi_files.html
    #for mido:
    mid = MidiFile(midi_file)
    midi_length = mid.length
    print(midi_length)

    #tempo:
    tempo = 500000 #default tempo from mido 

    all_notes = []
    input_notes = []
    deltas = []
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        input_notes = input_notes.clear
        input_notes = []
        for msg in track:
            print(msg) #TODO remove
            if msg.type == 'note_on':
                #print(msg.note)
                #finally an answer: https://stackoverflow.com/questions/45772214/convert-time-tick-in-python-midi-mido-read-save-file
                if msg.time > 0:
                    #round to only 4 decimal places
                    #print(msg.time)
                    #delta = round(tick2second(msg.time, mid.ticks_per_beat, tempo), 4)
                    delta = tick2second(msg.time, mid.ticks_per_beat, tempo)
                    #print(delta)
                else:
                    delta = 0
                deltas.append(delta)
                input_notes.append((msg.note, delta))
            elif msg.type == 'set_tempo':
                tempo = msg.tempo
            elif msg.type == 'time_signature':
                pass
        if(input_notes):
            all_notes.append(input_notes)

    ave_delta = sum(deltas)/len(deltas)
    return all_notes, ave_delta
    

class Midi_chart:
    def __init__(self):
        self.setup_notes()

    def setup_notes(self):
        notes = []
        n = open(NOTES)
        for line in n:
            notes.append(line)
        self.notes = [float(x) for x in notes]
        self.notes = [round(x) for x in self.notes]

    def display(self):
        for i in range(len(self.notes)):
            print(i, self.notes[i])



def decode_midi(input, chart, delta):
    #n_tracks = len(input)
    n_tracks = 1
    freqs = np.array([])
    times = np.array([])

    for i in range(n_tracks):
        #convert each note to freq, and time in seconds
        for j in range(len(input[i])-1, 0, -1):
            note_tuple = input[i][j] 
            note = chart.notes[note_tuple[0]] #chart at index of note num is frequency
            delta_time = note_tuple[1]

            #cases: last note, not last but time=0
            if j+1 >= len(input[i]):
                time = delta
            else:
                time = input[i][j+1][1] #the delta from the following note
                if time > 0:
                    times = np.append(times, round(time, 4)) 
                    freqs = np.append(freqs, note)

    times = np.asarray(times)
    freqs = np.asarray(freqs)
    times = np.flip(times)
    freqs = np.flip(freqs)

    print("times in midi_in:", times)
    print("call sine_by_freq")
    sine_by_freq.write_from_midi(TEST, times, freqs)



def main():
    if len(sys.argv) < 2:
        print("Please enter a midi file as an argument.")
        sys.exit(1)
    midi_file = sys.argv[1]
    print(midi_file)
    input_notes, delta = read(midi_file)
    chart = Midi_chart()
    note_instructions = decode_midi(input_notes, chart, delta)





if __name__ == '__main__':
    main()