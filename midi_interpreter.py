import sys
import numpy as np
from mido import MidiFile, tick2second
import sine_by_freq
import argparse

#https://soundprogramming.net/file-formats/midi-note-frequencies/
NOTES = 'notes.txt'
TEST = 'test_3.wav'


#info:
'''
changed library to this:
https://mido.readthedocs.io/en/latest/installing.html
'''



def read(midi_file):
    mid = MidiFile(midi_file)
    has_off = False

    #check to see if midi file contains note_off events
    for _, track in enumerate(mid.tracks):
        for msg in track:
            print(msg)
            if msg.type == 'note_off':
                has_off = True
                break

    if has_off:
        return read_midi_note_off(midi_file)
    #else no note_off messages in midi:
    return read_midi(midi_file)


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
    note_playing = False

    all_notes = []
    input_notes = []
    last_time = 0
    last_note = 0
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        input_notes = input_notes.clear
        input_notes = []
        for msg in track:
            print(msg) #TODO remove

            #actual note_on:
            if (msg.type == 'note_on'  and msg.velocity != 0):
                if note_playing:
                    #record the note that was playing and it's duration
                    delta = tick2second(msg.time, mid.ticks_per_beat, tempo)
                    input_notes.append((last_note, delta))
                    last_time = 0
                else:
                    #record the rest
                    delta = tick2second(msg.time, mid.ticks_per_beat, tempo)
                    input_notes.append((0, delta))

                #start a new note
                last_note = msg.note
                note_playing = True
                last_time = 0

            #note_off:
            if (msg.type == 'note_on'  and msg.velocity == 0):
                if last_note == msg.note:
                    delta = tick2second(msg.time + last_time, mid.ticks_per_beat, tempo)
                    input_notes.append((msg.note, delta))
                    note_playing = False
                else:
                    last_time += msg.time
            elif msg.type == 'set_tempo':
                tempo = msg.tempo
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



def decode_midi(input, chart, args):
    freqs = np.array([])
    times = np.array([])

    for i in range(len(input[0])):
        if input[0][i][0] == 0:
            note = 0
        else:
            note = chart.notes[input[0][i][0]]
        times = np.append(times, input[0][i][1])
        freqs = np.append(freqs, note)

    times = np.asarray(times)
    freqs = np.asarray(freqs)

    sine_by_freq.write_from_midi(TEST, times, freqs, args)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--midi", type=str, required=True)
    parser.add_argument("--wave_style", type=str, default="sine")
    parser.add_argument("--random", type=bool, default=False)
    args = parser.parse_args()
    return args



def main():
    if len(sys.argv) < 2:
        print("Please enter a midi file as an argument.")
        print("Usage: python midi_interpreter.y midi_file.mid ")
        sys.exit(1)

    args = get_arguments()

    #midi_file = sys.argv[1]
    midi_file = args.midi
    print(midi_file)
    input_notes = read(midi_file)
    chart = Midi_chart()

    decode_midi(input_notes, chart, args)






if __name__ == '__main__':
    main()