from pathlib import Path
from functools import partial, wraps

from beartype import beartype
from beartype.typing import Tuple, Union, Optional
from beartype.door import is_bearable

import torchaudio
from torchaudio.functional import resample

import torch
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader

from audiolm_pytorch.utils import curtail_to_multiple

from einops import rearrange, reduce
import pandas as pd

# helper functions

def exists(val):
    return val is not None

def cast_tuple(val, length = 1):
    return val if isinstance(val, tuple) else ((val,) * length)

def is_unique(arr):
    return len(set(arr)) == len(arr)

class MuLaNDataset(Dataset):
    @beartype
    def __init__(
        self,
        folder,
        captions,
        target_sample_hz: Union[int, Tuple[int, ...]],  # target sample hz must be specified, or a tuple of them if one wants to return multiple resampled
        exts = ['flac', 'wav', 'mp3', 'webm'],
        max_length: Optional[int] = None,               # max length would apply to the highest target_sample_hz, if there are multiple
        seq_len_multiple_of: Optional[Union[int, Tuple[Optional[int], ...]]] = None
    ):
        super().__init__()
        audio_path, caption_path = Path(folder), Path(captions)
        assert audio_path.exists(), f'folder "{str(audio_path)}" does not exist'

        files = [file for ext in exts for file in audio_path.glob(f'**/*.{ext}')]
        assert len(files) > 0, 'no sound files found'

        self.files = files
        self.captions = pd.read_csv(caption_path, sep='\t')
        
        self.max_length = max_length
        self.target_sample_hz = cast_tuple(target_sample_hz)
        num_outputs = len(self.target_sample_hz)

        # strategy, if there are multiple target sample hz, would be to resample to the highest one first
        # apply the max lengths, and then resample to all the others

        self.max_target_sample_hz = max(self.target_sample_hz)
        self.seq_len_multiple_of = cast_tuple(seq_len_multiple_of, num_outputs)

        assert len(self.target_sample_hz) == len(self.seq_len_multiple_of)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        file = self.files[idx]
        captions = self.captions[self.captions['filename'] == str(file).split('/')[-1]]

        data, sample_hz = torchaudio.load(file)
        artist, genre, decade = captions['artist'].tolist(), captions['genre'].tolist(), captions['decade'].tolist()
        decade = list(map(lambda x: str(round(x)) + 's', decade))
        texts = artist + genre + decade
        assert data.numel() > 0, f'one of your audio file ({file}) is empty. please remove it from your folder'

        if data.shape[0] > 1:
            # the audio has more than 1 channel, convert to mono
            data = reduce(data, 'c ... -> 1 ...', 'mean')

        # first resample data to the max target freq

        data = resample(data, sample_hz, self.max_target_sample_hz)
        sample_hz = self.max_target_sample_hz

        # then curtail or pad the audio depending on the max length

        max_length = self.max_length
        audio_length = data.size(1)

        if exists(max_length):
            if audio_length > max_length:
                max_start = audio_length - max_length
                start = torch.randint(0, max_start, (1, ))
                data = data[:, start:start + max_length]
            else:
                data = F.pad(data, (0, max_length - audio_length), 'constant')

        data = rearrange(data, '1 ... -> ...')

        # resample if target_sample_hz is not None in the tuple

        num_outputs = len(self.target_sample_hz)
        data = cast_tuple(data, num_outputs)

        data_tuple = tuple(resample(d, sample_hz, target_sample_hz) for d, target_sample_hz in zip(data, self.target_sample_hz))

        output = []

        # process each of the data resample at different frequencies individually for curtailing to multiple

        for data, seq_len_multiple_of in zip(data_tuple, self.seq_len_multiple_of):
            if exists(seq_len_multiple_of):
                data = curtail_to_multiple(data, seq_len_multiple_of)

            output.append(data.float())
            
        # return only one audio, if only one target resample freq
        if num_outputs == 1:
            return output[0]

        return texts, output