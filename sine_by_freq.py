
import wave 
from math import sin, pi
import struct
import numpy as np

#Author: Amber Shore
#Version: 2022-05-09

#Names of files to be created:
SINE_FILE = 'sine.wav'

#Sound generation parameters:
#FREQ = 440.0 #variable
FRAMES = 48000.0
AMP = 8192  #TODO change

#takes time in seconds - will this need to change?
def write_sine(num_notes, freq_arr, time_arr, file_name):
    wave_file = wave.open(file_name, 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(FRAMES)
    wave_file.setnframes(int(FRAMES*sum(time_arr)))

    frames = []
    for i in range(num_notes):
        for x in range(int(FRAMES*time_arr[i])):
            f = int((sin(2*pi*freq_arr[i]*(x/FRAMES))*AMP))
            frame = struct.pack('=h', f)
            wave_file.writeframes(frame)
    wave_file.close()


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

    if nframes1 == nframes2:
        new_data = (frames1 * .5) + (frames2 * .5)
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
    sine_1 = 'sine1.wav'
    sine_2 = 'sine2.wav'
    result = 'result.wav'
    notes = 4
    times = [1, .5, .5, 1]

    #A, D, E:
    freqs = [440, 587, 330, 440]
    write_sine(notes, freqs, times, sine_1)
    show_file_parameters(sine_1)
    #octave down:
    freqs = [220, 294, 165, 220]
    write_sine(notes, freqs, times, sine_2)
    show_file_parameters(sine_2)
    
    combine_wavs(sine_1, sine_2, result)
    show_file_parameters(result)



if __name__ == '__main__':
    main()