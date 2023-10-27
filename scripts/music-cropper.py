import os
import random
from pydub import AudioSegment
import threading
import math

MAX_THREADS = 20

# Function to crop 10-second clips from an MP3 file
def crop_mp3(file_path, output_folder):
    audio = AudioSegment.from_mp3(file_path)
    clip_length_ms = 10 * 1000  # 10 seconds in milliseconds

    # Iterate and crop 10-second clips from the audio
    for i, start_time in enumerate(range(0, len(audio), clip_length_ms)):
        clip = audio[start_time:start_time + clip_length_ms]
        output_path = f"{output_folder}/clip_{i + 1}.mp3"
        clip.export(output_path, format="mp3")

# Function to crop N clips with random starting points from an MP3 file
def crop_random_clips(file_path, clip_id, output_folder, clip_duration=10):
    audio = AudioSegment.from_mp3(file_path)
    # 10 seconds
    clip_length_ms = clip_duration * 1000  # Convert duration to milliseconds
    num_sections = int(math.sqrt(len(audio)//clip_length_ms))
    num_clips_per_section = len(audio)//clip_length_ms//num_sections

    print(num_sections, num_clips_per_section)

    for i in range(num_sections):
        for j in range(num_clips_per_section):
            # Generate a random starting point within the audio duration
            start_time = random.randint(i*num_clips_per_section*clip_length_ms, min((i+1)*num_clips_per_section*clip_length_ms, len(audio)) - clip_length_ms)
            
            # Crop the clip
            clip = audio[start_time:start_time + clip_length_ms]
            
            # Save the clip to the output folder
            output_path = os.path.join(output_folder, f"{clip_id}_{i*num_clips_per_section + j + 1}.mp3")
            clip.export(output_path, format="mp3")


def main():

    threads = []
    threads_counter = 0
    
    input_folder = "../raw-data/"
    tracks = os.listdir(input_folder)

    output_folder = "../sampled-data/"  # Output folder where clips will be saved
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    while len(tracks) != 0:

        print(f'{len(tracks)} left')
        track = tracks.pop()
        clip_id = track[:3] # id is a 3 digit number
        input_path = input_folder + track
        thread = threading.Thread(target=crop_random_clips, args=(input_path, clip_id, output_folder))
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
            clip_id = track[:3] # id is a 3 digit number
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

