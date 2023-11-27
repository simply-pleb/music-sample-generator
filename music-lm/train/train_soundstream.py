from audiolm_pytorch import MusicLMSoundStream, SoundStreamTrainer, HubertWithKmeans
import argparse as arg
from pathlib import Path

PWD = Path(__file__).parent.parent
MODELS = PWD / 'models'

SOUNDSTREAM_TRAINER_KWARGS = {
    'folder': None,
    'num_train_steps': 20,
    'save_model_every': 2,
    'batch_size': 2,
    'data_max_length_seconds': 10,
    'valid_frac': 0.
}

HUBERT_KWARGS = {
    'checkpoint_path': str((MODELS / 'hubert' / 'hubert_base_ls960.pt').resolve()),
    'kmeans_path': str((MODELS / 'hubert' / 'hubert_base_ls960_L9_km500.bin').resolve()),
}

if __name__ == '__main__':
    parser = arg.ArgumentParser()
    parser.add_argument('-n', '--num_train_steps', type=int, default=20)
    parser.add_argument('-b', '--batch_size', type=int, default=2)
    parser.add_argument('--audio_path', type=str, required=True)
    parser.add_argument('--ckpt_filename', type=str, required=True)
    args = parser.parse_args()
    
    train_steps, batch_size, audio_path, ckpt_filename = args.num_train_steps, args.batch_size, args.audio_path, args.ckpt_filename
    
    SOUNDSTREAM_TRAINER_KWARGS['folder'] = str(Path(audio_path).resolve())
    SOUNDSTREAM_TRAINER_KWARGS['batch_size'] = batch_size
    SOUNDSTREAM_TRAINER_KWARGS['num_train_steps'] = train_steps
    
    soundstream_ckpt = ckpt_filename
    wav2vec = HubertWithKmeans(
        **HUBERT_KWARGS
    )
    
    soundstream = MusicLMSoundStream(target_sample_hz=4000,
                                     codebook_size=wav2vec.codebook_size)
    soundstream_trainer = SoundStreamTrainer(
        soundstream,
        **SOUNDSTREAM_TRAINER_KWARGS
    )

    soundstream_trainer.train()

    soundstream_trainer.save(str((PWD / 'models' / 'soundstream' / soundstream_ckpt).resolve()))