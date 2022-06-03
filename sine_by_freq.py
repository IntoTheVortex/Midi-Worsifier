import sys
import wave 
from math import sin, pi
import struct
import numpy as np

#Author: Amber Shore
#Version: 2022-06-03


#Sound generation parameters:
FRAMES = 48000  #Frames per second
AMP = 16384     #amplitude
ENV = 0.05      #fraction of start & end of note to apply ramp/reverse


# open and set up a .wav file
#def open_file(file_name, total_frames):

# write the given frames to the .wav file
def write_file(frames, filename):
    #print(frames.shape)
    file = wave.open(filename, 'wb')
    file.setnchannels(1)
    file.setsampwidth(2)
    file.setframerate(FRAMES)
    file.setnframes(len(frames))

    #print(frames.shape)
    frames = np.ravel(frames)
    frames = frames.astype('int16')
    print(frames.shape)
    print(frames.dtype)
    #for f in frames:
    file.writeframes(frames)
    file.close()


# create a sequence of notes using a sine wave at the given 
# frequencies and for the given number of frames
def write_sine(freq_arr, frames_arr):
    all_frames = np.array([])

    for i in range(len(freq_arr)):
        print(freq_arr[i])
        frames = []
        length = int(frames_arr[i])

        #use number of frames
        for x in range(length):
            f = sin(2*pi*freq_arr[i]*(x/FRAMES))*AMP
            frames.append(f)
        
        frames = apply_envelope(frames, length)
        all_frames = np.append(all_frames, frames)

    return all_frames


# create a sequence of notes using a square wave at the given 
# frequencies and for the given number of frames
#https://github.com/pdx-cs-sound/sounddevice-demos/blob/master/nbsquare.py
def write_square(freq_arr, frames_arr):
    all_frames = np.array([])

    for i in range(len(freq_arr)):
        frames = []
        halfcycle = FRAMES // (2 * freq_arr[i])
        length = frames_arr[i]

        #use number of frames
        period = -1
        cycle_counter = 0
        for x in range(length):
            f = period * (AMP/5)
            cycle_counter += 1
            if cycle_counter >= halfcycle:
                period = -period
                cycle_counter = 0
            frames.append(f)

        frames = apply_envelope(frames, length)
        all_frames = np.append(all_frames, frames)
    
    return all_frames


# create a sequence of notes using a sawtooth wave at the given 
# frequencies and for the given number of frames
def write_saw(freq_arr, frames_arr):
    all_frames = np.array([])

    for i in range(len(freq_arr)):
        frames = []
        length = frames_arr[i]
        cycle = FRAMES // freq_arr[i]

        arr = np.linspace(-1, 1, cycle)
        for x in range(length):
            f = (AMP/5) * arr[x%len(arr)]
            frames.append(f)

        frames = apply_envelope(frames, length)
        all_frames = np.append(all_frames, frames)

    return all_frames


# create a sequence of notes using a triangle wave at the given 
# frequencies and for the given number of frames
def write_triangle(freq_arr, frames_arr):
    all_frames = np.array([])

    for i in range(len(freq_arr)):
        frames = []
        halfcycle = FRAMES // (2 * freq_arr[i])
        length = frames_arr[i]

        up_arr = np.linspace(-1, 1, halfcycle)
        down_arr = np.linspace(1, -1, halfcycle)
        cycle_counter = 0

        for x in range(length):
            if cycle_counter == halfcycle*2:
                cycle_counter = 0

            if cycle_counter >= halfcycle:
                f = AMP * down_arr[x%halfcycle]
                cycle_counter += 1
            else:
                f = AMP * up_arr[x%halfcycle]
                cycle_counter += 1

            frames.append(f)

        frames = apply_envelope(frames, length)
        all_frames = np.append(all_frames, frames)

    return all_frames


# create a sequence of notes using a 'glitched triangle' wave at the given 
# frequencies and for the given number of frames
def write_mod_1(freq_arr, frames_arr):
    all_frames = np.array([])

    for i in range(len(freq_arr)):
        frames = []
        cycle = FRAMES // freq_arr[i]
        halfcycle = cycle//2
        up_arr = np.linspace(-1, 1, halfcycle)
        down_arr = np.linspace(1, -1, halfcycle)
        cycle_counter = 0

        for x in range(frames_arr[i]):
            if cycle_counter >= cycle:
                f = (AMP/2) * up_arr[x%len(up_arr)]
                cycle_counter = 0
            elif cycle_counter >= halfcycle:
                f = (AMP/2) * down_arr[x%len(down_arr)]
                cycle_counter += 1
            else:
                f = (AMP/2) * up_arr[x%len(up_arr)]
                cycle_counter += 1
            frames.append(f)

        frames = apply_envelope(frames, frames_arr[i])
        all_frames = np.append(all_frames, frames)

    return all_frames


# apply the envelope to the frames that are passed in
def apply_envelope(frames, length):
    env_length = int(ENV * length)

    #apply ramp to the beginning of the note
    for j in range(env_length):
        frames[j] = frames[j] * (j / env_length)

    #flip to do the same for the end of the note
    frames = np.flip(frames)
    for k in range(env_length):
        frames[k] = frames[k] * (k / env_length)

    #flip back
    frames = np.flip(frames)

    return frames


# combine the frames from two files to create frames values
# halfway between them
#referenced https://stackoverflow.com/questions/28743400/pyaudio-play-multiple-sounds-at-once
def combine_wavs(wav1, wav2, result):
    wav_1 = wave.open(wav1,'r')
    wav_2 = wave.open(wav2,'r')
    nframes1 = wav_1.getnframes()
    nframes2 = wav_2.getnframes()

    data_1 = wav_1.readframes(nframes1)
    data_2 = wav_2.readframes(nframes2)

    frames1 = np.frombuffer(data_1, np.int16)
    frames2 = np.frombuffer(data_2, np.int16)

    if nframes1 == 0 or nframes2 == 0:
        new_data = frames1 + frames2

    elif nframes1 == nframes2:
        new_data = (frames1 * .5) + (frames2 * .5)
    elif nframes1 > nframes2:
        new_data = (frames1[:nframes2] * .5) + (frames2 * .5)
        new_data = np.append(new_data, frames1[nframes2:])
    elif nframes1 < nframes2:
        new_data = (frames1 * .5) + (frames2[:nframes1] * .5)
        new_data = np.append(new_data, frames2[nframes1:])
    
    new_data = new_data.astype('int16')

    new_wav = wave.open(result, 'wb')
    new_wav.setnchannels(1)
    new_wav.setsampwidth(2)
    new_wav.setframerate(FRAMES)

    for i in range(new_data.size):
        frame = struct.pack('=h', new_data[i])
        new_wav.writeframes(frame)

    new_wav.close()


def show_file_parameters(filename):
    file = wave.open(filename,'r')
    print(filename)
    print("Channels:", file.getnchannels())
    print("Sample width:", file.getsampwidth())
    print("Frame rate:", file.getframerate())
    print("Frames:", file.getnframes())
    print("Parameters:", file.getparams())
    file.close()


def write_from_midi(filename, times_arr, freqs_arr):
    frames_arr = np.multiply(times_arr, FRAMES)
    frames = write_sine(freqs_arr, frames_arr)
    write_file(frames, filename)



def main():
    melody = 'melody.wav'

    num_frames = [FRAMES, int(FRAMES/2), int(FRAMES/2), FRAMES]
    num_sequences = 6

    wave_file = open_file(melody, sum(num_frames)*num_sequences)
    frames = np.array([])

    ## testing ## 

    #A, D, E:
    freqs = [440, 587, 330, 440]
    frames = np.append(frames, write_sine(freqs, num_frames))

    #square
    freqs = [220, 294, 165, 220]
    frames = np.append(frames, write_square(freqs, num_frames))
    
    #sawtooth
    freqs = [440, 587, 330, 440]
    frames = np.append(frames, write_saw(freqs, num_frames))

    #triangle
    freqs = [220, 294, 165, 220]
    frames = np.append(frames, write_triangle(freqs, num_frames))

    #mod
    freqs = [440, 587, 330, 440]
    frames = np.append(frames, write_mod_1(freqs, num_frames))

    #mod
    freqs = [220, 294, 165, 220]
    frames = np.append(frames, write_mod_1(freqs, num_frames))

    write_file(frames, wave_file)
    
    #combine_wavs('new_sine.wav', 'new_mod_220.wav', 'result.wav')
    show_file_parameters(melody)
    wave_file.close()



if __name__ == '__main__':
    main()