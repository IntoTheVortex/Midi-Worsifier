
import wave 
from math import sin, pi, floor
import struct
import numpy as np
from scipy import signal 

#Author: Amber Shore
#Version: 2022-05-09

## TODO
    # change to returning frames instead of writing

#Names of files to be created:
SINE_FILE = 'sine.wav'

#Sound generation parameters:
#FREQ = 440.0 #variable
FRAMES = 48000
AMP = 16384


def open_file(file_name, total_frames):
    wave_file = wave.open(file_name, 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(FRAMES)
    wave_file.setnframes(total_frames)
    return wave_file

#takes time in seconds - will this need to change?
def write_sine(freq_arr, frames_arr, wave_file):
    for i in range(len(freq_arr)):
        #use number of frames
        for x in range(frames_arr[i]):
            f = int((sin(2*pi*freq_arr[i]*(x/FRAMES))*AMP))
            frame = struct.pack('=h', f)
            wave_file.writeframes(frame)

#inspired by https://github.com/pdx-cs-sound/sounddevice-demos/blob/master/nbsquare.py
def write_square(freq_arr, frames_arr, wave_file):
    for i in range(len(freq_arr)):
        halfcycle = FRAMES // (2 * freq_arr[i])
        #use number of frames
        period = -1
        cycle_counter = 0
        for x in range(frames_arr[i]):
            f = period * (AMP/6)
            cycle_counter += 1
            if cycle_counter >= halfcycle:
                period = -period
                cycle_counter = 0
            frame = struct.pack('=h', int(f))
            wave_file.writeframes(frame)


def write_saw(freq_arr, frames_arr, wave_file):
    for i in range(len(freq_arr)):
        cycle = FRAMES // freq_arr[i]
        arr = np.linspace(-1, 1, cycle)
        for x in range(frames_arr[i]):
            f = int((AMP/6) * arr[x%len(arr)])
            frame = struct.pack('=h', f)
            wave_file.writeframes(frame)


def write_triangle(freq_arr, frames_arr, wave_file):
    for i in range(len(freq_arr)):
        halfcycle = FRAMES // (2 * freq_arr[i])
        length = frames_arr[i]

        up_arr = np.linspace(-1, 1, halfcycle)
        down_arr = np.linspace(1, -1, halfcycle)
        number_ramp = int(.05 * length)
        number_release = length - number_ramp
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

            #envelope to reduce clicking
            if x <= number_ramp:
                f = f * (x / number_ramp)
            elif x == number_release:
                y = number_ramp
            elif x > number_release:
                y -= 1
                f = f * (y / number_ramp)

            frame = struct.pack('=h', int(f))
            wave_file.writeframes(frame)

#from broken triangle
def write_mod_1(freq_arr, frames_arr, wave_file):
    for i in range(len(freq_arr)):
        cycle = FRAMES // freq_arr[i]
        halfcycle = cycle//2
        up_arr = np.linspace(-1, 1, halfcycle)
        down_arr = np.linspace(1, -1, halfcycle)
        cycle_counter = 0

        for x in range(frames_arr[i]):
            if cycle_counter >= cycle:
                f = int(AMP * up_arr[x%len(up_arr)])
                cycle_counter = 0
            elif cycle_counter >= halfcycle:
                f = int(AMP * down_arr[x%len(down_arr)])
                cycle_counter += 1
            else:
                f = int(AMP * up_arr[x%len(up_arr)])
                cycle_counter += 1
            frame = struct.pack('=h', f)
            wave_file.writeframes(frame)




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




def main():
    melody = 'melody.wav'

    num_frames = [FRAMES, int(FRAMES/2), int(FRAMES/2), FRAMES]
    num_sequences = 4

    wave_file = open_file(melody, sum(num_frames)*num_sequences)

    #A, D, E:
    freqs = [440, 587, 330, 440]
    write_sine(freqs, num_frames, wave_file)

    #octave down:
    freqs = [220, 294, 165, 220]
    write_square(freqs, num_frames, wave_file)
    
    #sawtooth
    freqs = [440, 587, 330, 440]
    write_saw(freqs, num_frames, wave_file)

    #square
    freqs = [220, 294, 165, 220]
    write_triangle(freqs, num_frames, wave_file)


    
    #combine_wavs(sine_1, sine_2, result)
    show_file_parameters(melody)
    wave_file.close()



if __name__ == '__main__':
    main()