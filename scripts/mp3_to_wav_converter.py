from os import path
from pydub import AudioSegment


import os
import random
from pydub import AudioSegment
import threading
import math

MAX_THREADS = 32

def convert_mp3_to_wav(src_dir, out_dir, track):
    # files                                                                         
    # src = "transcript.mp3"
    # dst = "test.wav"

    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(src_dir+track)
    sound.export(out_dir+track[:-3]+"wav", format="wav")



def main():

    threads = []
    threads_counter = 0
    
    input_folder = "../data/raw-data/"
    tracks = os.listdir(input_folder)

    output_folder = "../wav-data/"  # Output folder where clips will be saved
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    while len(tracks) != 0:

        print(f'{len(tracks)} left')
        track = tracks.pop()
        clip_id = track[:4] # id is a 3 digit number
        # input_path = input_folder + track
        thread = threading.Thread(target=convert_mp3_to_wav, args=(input_folder, output_folder, track))
        thread.start()
        threads.append(thread)

        threads_counter += 1

        if threads_counter == MAX_THREADS:

            for thread in threads:
                thread.join()

            threads = []
            threads_counter = 0
            print('\n')

    while len(tracks) != 0 or len(threads) != 0:

        for thread in threads:
            thread.join()
        threads = []

        if len(tracks) != 0:
            track = tracks.pop()
            clip_id = track[:4] # id is a 4 digit number
            input_path = input_folder + track
            thread = threading.Thread(target=crop_random_clips, args=(input_path, clip_id, output_folder))
            thread.start()
            threads.append(thread)

    # crop_mp3(input_mp3, output_folder)
    # num_clips = 5  # Number of random clips to generate
    # crop_random_clips(input_mp3, output_folder, num_clips)


if __name__ == "__main__":
    # MAX_THREADS = int(input('Enter number of threads: '))
    main()

