import urllib.request
import os
import argparse as arg

hubert_ckpt = 'hubert/hubert_base_ls960.pt'
hubert_quantizer = 'hubert/hubert_base_ls960_L9_km500.bin'

if __name__ == '__main__':
    parser = arg.ArgumentParser()
    parser.add_argument('--hubert_path', type=str, required=True)
    args = parser.parse_args()
    hubert_path = args.hubert_path
    if not os.path.isdir(os.path.join(hubert_path, "hubert")):
        os.makedirs(os.path.join(hubert_path, "hubert"))
    if not os.path.isfile(hubert_ckpt):
        hubert_ckpt_download = f"https://dl.fbaipublicfiles.com/{hubert_ckpt}"
        urllib.request.urlretrieve(hubert_ckpt_download, os.path.join(hubert_path, hubert_ckpt))
    if not os.path.isfile(hubert_quantizer):
        hubert_quantizer_download = f"https://dl.fbaipublicfiles.com/{hubert_quantizer}"
        urllib.request.urlretrieve(hubert_quantizer_download, os.path.join(hubert_path, hubert_quantizer))