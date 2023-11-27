from glob import glob
from pathlib import Path
import os
import argparse
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, required=True)
    args = parser.parse_args()
    path = args.path
    files = glob(str(Path(path) / '**' / '*.mp3'), recursive=True) + glob(str(Path(path) / '**' / '*.wav'), recursive=True)
    for file in files:
        shutil.move(file, str(Path(file).parent.parent / file.split('/')[-1]))