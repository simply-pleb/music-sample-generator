import pandas as pd
import numpy as np
import os
import glob
import sys
import shutil

filenames = sorted(glob.glob(os.path.join('wav-data', '*.wav')))[:100]
author = 'Café Au Lait'
year = '1970s'

# for filename in filenames:
#     sound = AudioSegment.from_mp3(filename)
#     sound.export(filename[:-4] + '.wav', format='wav')
#     os.remove(filename)
#     filename = filename[:-4] + '.wav'

new_filenames = []

for filename in filenames:
    # shutil.copy(filename, f"./music-lm/data/wav/{filename[9:13]}.wav")
    # os.system(f"cp {filename} /music-lm/data/wav/{filename[9:13]}.wav")
    new_filenames.append(filename[9:13]+".wav")

mapping = {
    'filename': new_filenames,
    'author': [author for _ in range(len(new_filenames))],
    'year': [year for _ in range(len(new_filenames))]
}


df = pd.DataFrame(mapping)
df.to_csv('./music-lm/data/dataset.tsv', sep='\t', index=False)