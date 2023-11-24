import argparse as arg
import torch
from musiclm_pytorch import MuLaN, MuLaNEmbedQuantizer, \
                            AudioSpectrogramTransformer, TextTransformer, MusicLM
from audiolm_pytorch import SemanticTransformer, SemanticTransformerTrainer, \
                            CoarseTransformer, CoarseTransformerTrainer, \
                            FineTransformer, FineTransformerTrainer, \
                            AudioLM, HubertWithKmeans, MusicLMSoundStream, \
                            SoundStreamTrainer, SoundStream 
from pathlib import Path
import torchaudio

                            
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
PWD = Path(__file__).parent
MODELS = PWD / 'models'

SEMANTIC_KWARGS = {
    'dim': 1024,
    'depth': 6,
    'audio_text_condition': True 
}

COARSE_KWARGS = {
    'codebook_size': 1024,
    'num_coarse_quantizers': 4,
    'dim': 1024,
    'depth': 6,
    'audio_text_condition': True 
}

FINE_KWARGS = {
    'codebook_size': 1024,
    'num_coarse_quantizers': 4,
    'num_fine_quantizers': 8,
    'dim': 1024,
    'depth': 6,
    'audio_text_condition': True 
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

if __name__ == "__main__":
    parser = arg.ArgumentParser()
    parser.add_argument('-n', '--num_samples', type=int, default=5)
    parser.add_argument('--prompt', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    args = parser.parse_args()
    num_samples, prompt, output_path = args.num_samples, args.prompt, args.output_path
    
    
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
    )

    wav2vec = HubertWithKmeans(
        **HUBERT_KWARGS
    )
    
    soundstream = SoundStream.init_and_load_from(str((MODELS / 'soundstream' / 'soundstream.pt').resolve()))
    
    semantic_transformer = SemanticTransformer(
        num_semantic_tokens=wav2vec.codebook_size,
        **SEMANTIC_KWARGS 
    ).to(DEVICE)
    semantic_transformer.load(str((MODELS / 'semantic' / 'semantic.pt').resolve()))
    
    coarse_transformer = CoarseTransformer(
        num_semantic_tokens=wav2vec.codebook_size,
        **COARSE_KWARGS
    ).to(DEVICE)
    coarse_transformer.load(str((MODELS / 'coarse' / 'coarse.pt').resolve()))
    
    fine_transformer = FineTransformer(
        codebook_size=wav2vec.codebook_size,
        **FINE_KWARGS
    ).to(DEVICE)
    fine_transformer.load(str((MODELS / 'fine' / 'fine.pt').resolve()))
    
    audio_lm = AudioLM(
        wav2vec=wav2vec,
        codec=soundstream,
        semantic_transformer=semantic_transformer,
        coarse_transformer=coarse_transformer,
        fine_transformer=fine_transformer   
    )
    music_lm = MusicLM(
        audio_lm=audio_lm,
        mulan_embed_quantizer=quantizer
    )

    music = music_lm(prompt, num_samples=3)
    sample_rate = 44100
    torchaudio.save(output_path, music.cpu(), sample_rate)