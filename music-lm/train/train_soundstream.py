from audiolm_pytorch import MusicLMSoundStream, SoundStreamTrainer
import argparse as arg
from pathlib import Path

PWD = Path(__file__).parent.parent

SOUNDSTREAM_TRAINER_KWARGS = {
    'folder': None,
    'num_train_steps': 20,
    'save_model_every': 2,
    'batch_size': 16,
    'data_max_length_seconds': 10
}

if __name__ == '__main__':
    parser = arg.ArgumentParser()
    parser.add_argument('-n', '--num_train_steps', type=int, default=20)
    parser.add_argument('-b', '--batch_size', type=int, default=16)
    parser.add_argument('--audio_path', type=str, required=True)
    parser.add_argument('--ckpt_filename', type=str, required=True)
    args = parser.parse_args()
    
    train_steps, batch_size, audio_path, ckpt_filename = args.num_train_steps, args.batch_size, args.audio_path, args.ckpt_filename
    
    SOUNDSTREAM_TRAINER_KWARGS['folder'] = str(Path(audio_path).resolve())
    SOUNDSTREAM_TRAINER_KWARGS['batch_size'] = batch_size
    SOUNDSTREAM_TRAINER_KWARGS['num_train_steps'] = train_steps
    
    soundstream_ckpt = ckpt_filename
    
    soundstream = MusicLMSoundStream(target_sample_hz=48000)
    soundstream_trainer = SoundStreamTrainer(
        soundstream,
        **SOUNDSTREAM_TRAINER_KWARGS
    )

    soundstream_trainer.train()

    soundstream_trainer.save(str((PWD / 'models' / 'soundstream' / soundstream_ckpt).resolve()))