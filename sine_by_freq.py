
import wave 
from math import sin, pi
import struct
import numpy as np

#Author: Amber Shore
#Version: 2022-05-09

#Names of files to be created:
SINE_FILE = 'sine.wav'

#Sound generation parameters:
TIME = 1 #in seconds
#FREQ = 440.0 #variable
FRAMES = 48000.0
AMP = 8192  #TODO change

#takes time in seconds - will this need to change?
def write_sine(num_notes, freq_arr, time_arr):
    wave_file = wave.open(SINE_FILE, 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(FRAMES)
    wave_file.setnframes(int(FRAMES))

    frames = []
    for i in range(num_notes):
        for x in range(int(FRAMES*time_arr[i])):
            f = int((sin(2*pi*freq_arr[i]*(x/FRAMES))*AMP))
            frame = struct.pack('=h', f)
            wave_file.writeframes(frame)
    wave_file.close()


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
    notes = 4
    #A, D, E:
    freqs = [440, 587, 330, 440]
    times = [1, .5, .5, 1]
    write_sine(notes, freqs, times)
    show_file_parameters(SINE_FILE)


if __name__ == '__main__':
    main()