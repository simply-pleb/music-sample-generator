
from musiclm_pytorch import MuLaN, TextTransformer, AudioSpectrogramTransformer, MuLaNTrainer
from audiolm_pytorch.data import SoundDataset
from .utils.mulan_dataset import MuLaNDataset
import argparse as arg
from pathlib import Path

PWD = Path(__file__).parent.parent 
DEVICE = 'cpu'

AUDIO_KWARGS = {
    'dim': 128,
    'depth': 6,
    'heads': 8,
    'accept_spec': False,
    'dim_head': 64,
    'spec_n_fft': 128,
    'spec_win_length': 24,
    'spec_aug_stretch_factor': 0.8,
    'patch_dropout_prob': 0.
}

TEXT_KWARGS = {
    'dim': 128,
    'depth': 6,
    'heads': 8,
    'dim_head': 64
}

MULAN_KWARGS = {
    'dataset': None,
    'num_train_steps': 25,
    'batch_size': 2,
    'force_clear_prev_results': False,
    'save_model_every': 100,
    'lr': 2e-6,
    'valid_frac': 0.01,
    'results_folder': str((PWD / 'models' / 'mulan').resolve())
}

if __name__ == '__main__':
    parser = arg.ArgumentParser()
    parser.add_argument('-n', '--num_steps', type=int, default=MULAN_KWARGS['num_train_steps'])
    parser.add_argument('-b', '--batch_size', type=int, default=MULAN_KWARGS['batch_size'])
    parser.add_argument('--audio_path', type=str, required=True)
    parser.add_argument('--caption_path', type=str, required=True)
    parser.add_argument('--ckpt_filename', type=str, required=True)
    parser.add_argument('--continue_training', action='store_true')

    args = parser.parse_args()
    (
        train_steps, batch_size, 
        audio_path, caption_path, 
        ckpt_filename, continue_training
    ) = (
        args.num_steps, args.batch_size, 
        args.audio_path, args.caption_path,
        args.ckpt_filename, args.continue_training
        )
    
    train_dataset = MuLaNDataset(folder=audio_path, captions=caption_path, target_sample_hz=8000)
    
    MULAN_KWARGS['dataset'] = train_dataset
    MULAN_KWARGS['batch_size'] = batch_size
    MULAN_KWARGS['num_train_steps'] = train_steps
    
    mulan_ckpt = ckpt_filename
    
    audio_transformer = AudioSpectrogramTransformer(**AUDIO_KWARGS)
    text_transformer = TextTransformer(**TEXT_KWARGS)
    
    mulan = MuLaN(audio_transformer=audio_transformer, 
                  text_transformer=text_transformer).to(DEVICE)
        
    trainer = MuLaNTrainer(mulan=mulan, **MULAN_KWARGS)
    
    if continue_training:
        trainer.load(str((PWD / 'models' / 'mulan' / mulan_ckpt).resolve()))
    
    trainer.train()
    
    trainer.save(str((PWD / 'models' / 'mulan' / mulan_ckpt).resolve()))