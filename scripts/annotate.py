import pandas as pd
import numpy as np
import os
import glob
from pydub import AudioSegment

filenames = sorted(glob.glob(os.path.join('music-lm', 'data', '*.mp3')))
author = 'Café Au Lait'
year = '1970s'

for filename in filenames:
    sound = AudioSegment.from_mp3(filename)
    sound.export(filename[:-4] + '.wav', format='wav')
    os.remove(filename)
    filename = filename[:-4] + '.wav'

mapping = {
    'filename': filenames,
    'author': [author for _ in range(len(filenames))],
    'year': [year for _ in range(len(filenames))]
}

df = pd.DataFrame(mapping)
df.to_csv('./music-lm/data/dataset.tsv', sep='\t', index=False)