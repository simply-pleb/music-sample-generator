# Music Sample Generation

Team:

- Ahmadsho Akdodshoev
    - email: [a.akdodshoev@innopolis.university](a.akdodshoev@innopolis.university)
    - github: [simply-pleb](https://github.com/simply-pleb)
    - role: literature review and data preparation
    - group: BS20-AAI
- Robert Chen
    - email: [r.chen@innopolis.university]()
    - github: [BobIllumine](https://github.com/BobIllumine)
    - role: model implementation
    - group: BS20-AAI
- Philipp Timofeev
    - email: [p.timofeev@innopolis.university](p.timofeev@innopolis.university)
    - github: [beleet](https://github.com/beleet)
    - role: data collection, preparation and web
    - group: BS20-SD-02

## Description of the task

Sampling is the one of the fundamental hurdles in music creation. Most of the time DMCA and licensing issues can become the main roadblock for the artists around the world, both renowned and new to the scene. Our project is aiming to overcome this obstacle and give more freedom to the music creators. The main task is to construct a model that can generate new music samples in soul style based on the prompt given by the user. 

In order to mitigate our lack of data and resource limitations, we decided to keep the prompt simple: we combine the artist name, genre and a time period. This prompt helps to achieve some kind of stylistic resemblance to the music created by the artist in a given time period and genre.

## Usage

First, you will need to train a model. In order to do so, you can run a script `train_musiclm.sh` from root project folder:
```bash
[music-sample-generator] $ bash train_musiclm.sh
```
It will automatically download the dataset and train the model.

After the training is done, you can use the model by executing the following command:

```bash
$ python -m music-lm.musiclm --prompt <your_prompt> --output_path <your_output_file_with_extension>
```
## References
[MusicLM: Generating Music From Text](https://google-research.github.io/seanet/musiclm/examples/) - [arXiv](https://arxiv.org/abs/2301.11325),
[GitHub Repo](https://github.com/lucidrains/musiclm-pytorch)

### Papers (2023)

| Title and demo page | Paper | Code |
| - | - | - |
| [Noise2Music: Text-conditioned Music Generation with Diffusion Models](https://google-research.github.io/noise2music/) | [arXiv](https://arxiv.org/abs/2302.03917) | |
| [MusicLM: Generating Music From Text](https://google-research.github.io/seanet/musiclm/examples/)| [arXiv](https://arxiv.org/abs/2301.11325)| [GitHub (unofficial)](https://github.com/lucidrains/musiclm-pytorch) |
| [MusicGen: Simple and Controllable Music Generation](https://ai.honu.io/papers/musicgen/)| [arXiv](https://arxiv.org/abs/2306.05284) | [Github](https://github.com/facebookresearch/audiocraft) |
| [Moûsai: Text-to-Music Generation with Long-Context Latent Diffusion](https://anonymous0.notion.site/Mo-sai-Text-to-Audio-with-Long-Context-Latent-Diffusion-b43dbc71caf94b5898f9e8de714ab5dc)| [arXiv](https://arxiv.org/abs/2301.11757) | [GitHub](https://github.com/archinetai/audio-diffusion-pytorch) |
| [Msanii: High Fidelity Music Synthesis on a Shoestring Budget](https://kinyugo.github.io/msanii-demo/)| [arXiv](https://arxiv.org/abs/2301.06468) | [GitHub](https://github.com/Kinyugo/msanii) |
| [JEN-1: Text-Guided Universal Music Generation with Omnidirectional Diffusion Models](https://www.futureverse.com/research/jen/demos/jen1)| [arXiv](https://arxiv.org/abs/2308.04729)| |
| [MeLoDy: Efficient Neural Music Generation](https://efficient-melody.github.io/)| [arXiv](https://arxiv.org/abs/2305.15719) | |

- Thanks to [Audio AI Timeline](https://github.com/archinetai/audio-ai-timeline/blob/main/README.md)

### Repositories 

- [Musika](https://github.com/marcoppasini/musika)
- [Riffusion](https://github.com/riffusion/riffusion)
- [Multi-instrument Music Synthesis with Spectrogram Diffusion](https://github.com/magenta/music-spectrogram-diffusion)
