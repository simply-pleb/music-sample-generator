from glob import glob
from pathlib import Path
import os
import argparse
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, required=True)
    parser.add_argument('-n', '--num_samples_per_dir', type=int, default=10)
    args = parser.parse_args()
    path, num_samples = args.path, args.num_samples_per_dir

    files = glob(str(Path(path) / '*.mp3'), recursive=True) + glob(str(Path(path) / '*.wav'), recursive=True)
    prev_i, num_folder = 0, 0
    for i in range(num_samples, len(files), num_samples):
        splitted = files[prev_i].split('/')
        new_folder = str(Path('/'.join(splitted[:-1])) / str(num_folder)) 
        os.makedirs(new_folder, exist_ok=True)
        for j in range(prev_i, i):
            shutil.move(files[j], str(Path(new_folder) / files[j].split('/')[-1]))
        prev_i = i
        num_folder += 1

 
    if prev_i + num_samples < len(files):
        splitted = files[prev_i].split('/')
        new_folder = str(Path('/'.join(splitted[:-1])) / str(num_folder)) 
        os.makedirs(new_folder, exist_ok=True)
        for i in range(prev_i, prev_i + num_samples):
            shutil.move(files[i], str(Path(new_folder) / files[i].split('/')[-1]))
        num_folder += 1
    
    remaining = len(files) % num_samples

    if remaining:
        splitted = files[len(files) - remaining].split('/')
        new_folder = str(Path('/'.join(splitted[:-1])) / str(num_folder))
        os.makedirs(new_folder, exist_ok=True)
        for i in range(len(files) - remaining, len(files)):
            shutil.move(files[i], str(Path(new_folder) / files[i].split('/')[-1]))