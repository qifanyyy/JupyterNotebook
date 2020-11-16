import wave,  utility, os, scipy.ndimage as ndi
from scipy.io import wavfile
import matplotlib.pyplot as plt, matplotlib.animation as animation
import highspeed_audio_automata
import numpy as np
import time, sys


f0 = [[2,2,2,1,2,2],
      [2,1,1,1,1,2],
      [2,1,3,3,1,2],
      [1,1,3,3,1,1],
      [2,1,1,1,1,2],
      [2,2,2,2,2,2]]

f1 = [[1,1,1,1,1],
      [1,1,1,1,1],
      [1,1,0,1,1],
      [1,1,1,1,1],
      [1,1,1,1,1]]


def get_song(path_to_song, song, verbose):
    cmd = 'cp ' + path_to_song + ' $PWD; ffmpeg -i '+song+' song.wav;clear'
    utility.execute(cmd)
    song_data = wave.open('song.wav')

    acquire_song('song.wav')

    utility.execute('rm song.wav; rm deify.mp3')
    if verbose:
        os.system('clear')
        n_frames = song_data.getnframes()
        sample_size = song_data.getsampwidth()
        frame_rate = song_data.getframerate()
        print ("N Frames: " + str(n_frames))
        print ("Sample Size: " + str(sample_size))
        print ("Frame Rate: " + str(frame_rate))

    return song_data


def convert_and_move(path_to_song,song):
    cmd = 'cp ' + path_to_song + ' $PWD; ffmpeg -i ' + song + ' song.wav;clear'
    os.system(cmd)
    os.system('rm '+song)


def acquire_song(path_to_song, frame_rate):
    f = plt.figure()
    rate, audio = wavfile.read(path_to_song, 'r')

    buff = 89600

    animate = []
    N = np.array(audio).shape[0]/buff

    for i in range(N):
        sampled = np.array(audio[0+i*buff:buff/2+i*buff, :])*10
        sound_space = np.abs(np.fft.fft(sampled.reshape(280, 320),axis=1))
        if np.array(sound_space).mean() > 2e7:
            sound_space = np.abs(np.fft.fft(sampled.reshape(280, 320), axis=0))
        animate.append([plt.imshow(ndi.convolve(sound_space, f1), 'gray')])
        animate.append([plt.imshow(ndi.convolve(sound_space, f0), 'gray')])
        for image in highspeed_audio_automata.instant_annealer(sound_space,5,False):
            animate.append([plt.imshow(np.array(image).reshape(280,320), 'gray')])
    print ("Rendering " + str(len(animate)) + " Frames")
    print (str(len(animate)*frame_rate/float(1000)) + "s")
    a = animation.ArtistAnimation(f, animate, interval=frame_rate,blit=True,repeat_delay=900)
    plt.show()


def slow_wav_grab(wave_file):
    length = wave_file.getnframes()
    WAVE_FILE_DATA = []
    t0 = time.time()
    for i in range(0, length):
        WAVE_FILE_DATA.append(np.fromstring(wave_file.readframes(i), 'Int16'))
        # WAVE_FILE_DATA.append)
    print ("FINDISHED PRE-PROCESSING " + str(length) + " FRAMES [" + str(time.time() - t0) + 's]')
    print (np.array(WAVE_FILE_DATA.pop()).shape)
    return np.array()


def main():
    if '-demo' in sys.argv:
        convert_and_move('/media/root/CoopersDB/MUSIC/Disturbed/deify.mp3', 'deify.mp3')
        acquire_song('song.wav', 700)
        os.system('rm song.wav')


if __name__ == '__main__':
    main()
