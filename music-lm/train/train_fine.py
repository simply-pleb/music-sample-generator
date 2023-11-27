import torch
from audiolm_pytorch import FineTransformer, FineTransformerTrainer, HubertWithKmeans, SoundStream
from musiclm_pytorch import MuLaN, AudioSpectrogramTransformer, TextTransformer, MuLaNEmbedQuantizer
from pathlib import Path
import argparse as arg

PWD = Path(__file__).parent.parent
MODELS = PWD / 'models'

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

FINE_KWARGS = {
    'codebook_size': 1024,
    'num_coarse_quantizers': 4,
    'num_fine_quantizers': 8,
    'dim': 1024,
    'depth': 6,
    'audio_text_condition': True 
}

TRANSFORMER_TRAINER_KWARGS = {
    'folder': None,
    'num_train_steps': 10,
    'save_model_every': 2,
    'batch_size': 4,
    'data_max_length_seconds': 10,
    'results_folder': str((MODELS / 'mulan').resolve()),
    'valid_frac': 0.
}

AUDIO_KWARGS = {
    'dim': 512,
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
    'dim': 512,
    'depth': 6,
    'heads': 8,
    'dim_head': 64
}

MULAN_QUANTIZER_KWARGS = {
    'conditioning_dims': (1024, 1024, 1024),
    'namespaces': ('semantic', 'coarse', 'fine')
}

HUBERT_KWARGS = {
    'checkpoint_path': str((MODELS / 'hubert' / 'hubert_base_ls960.pt').resolve()),
    'kmeans_path': str((MODELS / 'hubert' / 'hubert_base_ls960_L9_km500.bin').resolve()),
}

if __name__ == '__main__':
    parser = arg.ArgumentParser()
    parser.add_argument('-n', '--num_train_steps', type=int, default=20)
    parser.add_argument('-b', '--batch_size', type=int, default=16)
    parser.add_argument('--audio_path', type=str, required=True)
    parser.add_argument('--ckpt_filename', type=str, required=True)
    args = parser.parse_args()
    
    train_steps, batch_size, audio_path, ckpt_filename = args.num_train_steps, args.batch_size, args.audio_path, args.ckpt_filename
    
    TRANSFORMER_TRAINER_KWARGS['folder'] = str(Path(audio_path).resolve())
    TRANSFORMER_TRAINER_KWARGS['batch_size'] = batch_size
    TRANSFORMER_TRAINER_KWARGS['num_train_steps'] = train_steps
    
    audio_transformer = AudioSpectrogramTransformer(**AUDIO_KWARGS)
    text_transformer = TextTransformer(**TEXT_KWARGS)
    
    mulan = MuLaN(audio_transformer=audio_transformer, 
                  text_transformer=text_transformer)
    pkg = torch.load(str((MODELS / 'mulan' / 'mulan.pt').resolve()), map_location = 'cpu')
    mulan.load_state_dict(pkg['model'])
    
    mulan = mulan.to(DEVICE)
    
    quantizer = MuLaNEmbedQuantizer(
        mulan=mulan,                         
        **MULAN_QUANTIZER_KWARGS
    ).to(DEVICE)

    wav2vec = HubertWithKmeans(
        **HUBERT_KWARGS
    ).to(DEVICE)
    
    soundstream = SoundStream.init_and_load_from(str((MODELS / 'soundstream' / 'soundstream.pt').resolve()))
    
    fine_ckpt = ckpt_filename
    
    fine_transformer = FineTransformer(
        codebook_size=wav2vec.codebook_size,
        **FINE_KWARGS
    ).to(DEVICE)

    fine_trainer = FineTransformerTrainer(
        wav2vec,
        fine_transformer,
        codec=soundstream,
        audio_conditioner=quantizer,
        **TRANSFORMER_TRAINER_KWARGS
    )

    fine_trainer.train()


    fine_trainer.save(str((MODELS / 'fine' / fine_ckpt).resolve()))