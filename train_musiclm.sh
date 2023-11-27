#!/usr/bin/bash
pip install -r requirements.txt
if [[ ! -f "soul-mzk.zip" ]]; then
    kaggle datasets download -d simplypleb/soul-mzk
fi
if [[ ! -d "./data/mini-dataset" ]]; then
    unzip soul-mzk.zip -d ./data
fi

python -m music-lm.train.download_hubert --hubert_path ./music-lm/models/
python -m music-lm.train.train_mulan --audio_path ./data/mini-dataset/sampled-data --caption_path ./data/mini-dataset/mini-dataset.tsv --ckpt_filename mulan.pt
python -m music-lm.train.train_soundstream --audio_path ./data/mini-dataset/sampled-data --ckpt_filename soundstream.pt
python -m music-lm.train.train_semantic --audio_path ./data/mini-dataset/sampled-data --ckpt_filename semantic.pt
python -m music-lm.train.train_coarse --audio_path ./data/mini-dataset/sampled-data --ckpt_filename coarse.pt
python -m music-lm.train.train_fine --audio_path ./data/mini-dataset/sampled-data --ckpt_filename fine.pt
