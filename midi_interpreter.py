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
    # interpret note_on with time=0 as note_off
    # problem is don't have a way to parse rests for files 
    #  that don't have the note_off messages




def read(midi_file):
    mid = MidiFile(midi_file)

    #check to see if midi file contains note_off events
    #for i, track in enumerate(mid.tracks):
    if False:
        for msg in track:
            if msg.type == 'note_off':
                return read_midi_note_off(midi_file), True

    #else no note_off messages in midi:
    return read_midi(midi_file), False


def read_midi_note_off(midi_file):
    mid = MidiFile(midi_file)
    #midi_length = mid.length

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

    return all_notes
    


def read_midi(midi_file):
    #ref https://mido.readthedocs.io/en/latest/midi_files.html
    #ref for tick2second: https://stackoverflow.com/questions/45772214/convert-time-tick-in-python-midi-mido-read-save-file
    mid = MidiFile(midi_file)
    #midi_length = mid.length

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
            #if msg.type == 'note_on' and msg.velocity == 0:
            if (msg.type == 'note_on'  and msg.velocity == 0) or msg.type == 'note_off':
                if msg.time != 0:
                    #delta = tick2second(msg.time, mid.ticks_per_beat, tempo)
                    delta = tick2second(msg.time, 110, tempo)
                    print("ticks", mid.ticks_per_beat)
                    input_notes.append((msg.note, delta))
            elif msg.type == 'set_tempo':
                tempo = msg.tempo
                print(msg)
            elif msg.type == 'time_signature':
                print(msg)
        if(input_notes):
            all_notes.append(input_notes)

    return all_notes
    

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



def decode_midi(input, chart, has_note_off=False):
    #n_tracks = len(input)
    n_tracks = 1
    freqs = np.array([])
    times = np.array([])

    #if has_note_off:
    if True:
        for i in range(len(input[0])):
            note = chart.notes[input[0][i][0]]
            times = np.append(times, input[0][i][1])
            #print("note", note) #TODO remove
            freqs = np.append(freqs, note)

    else:
        #convert each note to freq, and time in seconds
        print("input", input) #TODO remove
        for i in range(len(input[0])-1, 0, -1):
            note_tuple = input[0][i] 
            if note_tuple[0] == 0:
                print(note_tuple)
                continue
            else:
                note = chart.notes[note_tuple[0]] #chart at index of note num is frequency
                delta_time = note_tuple[1]

                #cases: last note, not last but time=0
                if i+1 >= len(input[0]):
                    time = note_tuple[1]
                    times = np.append(times, round(time, 4)) 
                    freqs = np.append(freqs, note)
                    #print("times", times)
                    #print("freqs", freqs)
                else:
                    time = input[0][i+1][1] #the delta from the following note
                    if time > 0:
                        times = np.append(times, round(time, 4)) 
                        freqs = np.append(freqs, note)
                        #print("times", times)
                        #print("freqs", freqs)

    times = np.asarray(times)
    freqs = np.asarray(freqs)
    #if not has_note_off:
        #freqs = np.flip(freqs)
        #times = np.flip(times)

    sine_by_freq.write_from_midi(TEST, times, freqs)



def main():
    if len(sys.argv) < 2:
        print("Please enter a midi file as an argument.")
        sys.exit(1)
    midi_file = sys.argv[1]
    print(midi_file)
    input_notes, has_note_off = read(midi_file)
    chart = Midi_chart()
    decode_midi(input_notes, chart, has_note_off)





if __name__ == '__main__':
    main()