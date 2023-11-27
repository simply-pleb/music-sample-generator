from audiolm_pytorch import MusicLMSoundStream, SoundStreamTrainer, HubertWithKmeans
import argparse as arg
from pathlib import Path
import torch

PWD = Path(__file__).parent.parent
MODELS = PWD / 'models'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

SOUNDSTREAM_TRAINER_KWARGS = {
    'folder': None,
    'num_train_steps': 20,
    'save_model_every': 2,
    'batch_size': 2,
    'data_max_length_seconds': 10,
    'force_clear_prev_results': False,
    'results_folder': str((MODELS / 'mulan').resolve()),
    'valid_frac': 0.
}

HUBERT_KWARGS = {
    'checkpoint_path': str((MODELS / 'hubert' / 'hubert_base_ls960.pt').resolve()),
    'kmeans_path': str((MODELS / 'hubert' / 'hubert_base_ls960_L9_km500.bin').resolve()),
}

if __name__ == '__main__':
    parser = arg.ArgumentParser()
    parser.add_argument('-n', '--num_train_steps', type=int, default=SOUNDSTREAM_TRAINER_KWARGS['num_train_steps'])
    parser.add_argument('-b', '--batch_size', type=int, default=SOUNDSTREAM_TRAINER_KWARGS['batch_size'])
    parser.add_argument('--audio_path', type=str, required=True)
    parser.add_argument('--ckpt_filename', type=str, required=True)
    parser.add_argument('--continue_training', action='store_true')

    args = parser.parse_args()
    
    train_steps, batch_size, audio_path, ckpt_filename = args.num_train_steps, args.batch_size, args.audio_path, args.ckpt_filename
    continue_training = args.continue_training
    
    SOUNDSTREAM_TRAINER_KWARGS['folder'] = str(Path(audio_path).resolve())
    SOUNDSTREAM_TRAINER_KWARGS['batch_size'] = batch_size
    SOUNDSTREAM_TRAINER_KWARGS['num_train_steps'] = train_steps
    
    soundstream_ckpt = ckpt_filename
    wav2vec = HubertWithKmeans(
        **HUBERT_KWARGS
    ).to(DEVICE)
    
    soundstream = MusicLMSoundStream(target_sample_hz=4000,
                                     codebook_size=wav2vec.codebook_size).to(DEVICE)
    
    soundstream_trainer = SoundStreamTrainer(
        soundstream,
        **SOUNDSTREAM_TRAINER_KWARGS
    )

    if continue_training:
        soundstream_trainer.load(str((MODELS / 'soundstream' / soundstream_ckpt).resolve()))

    soundstream_trainer.train()

    soundstream_trainer.save(str((MODELS / 'soundstream' / soundstream_ckpt).resolve()))