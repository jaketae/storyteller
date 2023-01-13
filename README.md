# StoryTeller

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A multimodal AI story teller, built with [Stable Diffusion](https://huggingface.co/spaces/stabilityai/stable-diffusion), GPT, and neural text-to-speech (TTS).

Given a prompt as an opening line of a story, GPT writes the rest of the plot; Stable Diffusion draws an image for each sentence; a TTS model narrates each line, resulting in a fully animated video of a short story, replete with audio and visuals.

![out](https://user-images.githubusercontent.com/25360440/210071764-51ed5872-ba56-4ed0-919b-d9ce65110185.gif)

## Installation

### PyPI

Story Teller is available on [PyPI](https://pypi.org/project/storyteller-core/).

```
$ pip install storyteller-core
```

### Source

1. Clone the repository.

```
$ git clone https://github.com/jaketae/storyteller.git
$ cd storyteller
```

2. Install dependencies.

```
$ pip install .
```

*Note: For Apple M1/2 users, [`mecab-python3`](https://github.com/SamuraiT/mecab-python3) is not available. You need to install `mecab` before running `pip install`. You can do this with [Hombrew](https://www.google.com/search?client=safari&rls=en&q=homebrew&ie=UTF-8&oe=UTF-8) via `brew install mecab`. For more information, refer to [this issue](https://github.com/SamuraiT/mecab-python3/issues/84).*


3. (Optional) To develop locally, install `dev` dependencies and install pre-commit hooks. This will automatically trigger linting and code quality checks before each commit.

```
$ pip install -e .[dev]
$ pre-commit install
```

## Quickstart

The quickest way to run a demo is through the CLI. Simply type

```
$ storyteller
```

The final video will be saved as `/out/out.mp4`, alongside other intermediate images, audio files, and subtitles.

To adjust the defaults with custom parametes, toggle the CLI flags as needed.

```
$ storyteller --help
usage: storyteller [-h] [--writer_prompt WRITER_PROMPT]
                   [--painter_prompt_prefix PAINTER_PROMPT_PREFIX] [--num_images NUM_IMAGES]
                   [--output_dir OUTPUT_DIR] [--seed SEED] [--max_new_tokens MAX_NEW_TOKENS]
                   [--writer WRITER] [--painter PAINTER] [--speaker SPEAKER]
                   [--writer_device WRITER_DEVICE] [--painter_device PAINTER_DEVICE]

optional arguments:
  -h, --help            show this help message and exit
  --writer_prompt WRITER_PROMPT
  --painter_prompt_prefix PAINTER_PROMPT_PREFIX
  --num_images NUM_IMAGES
  --output_dir OUTPUT_DIR
  --seed SEED
  --max_new_tokens MAX_NEW_TOKENS
  --writer WRITER
  --painter PAINTER
  --speaker SPEAKER
  --writer_device WRITER_DEVICE
  --painter_device PAINTER_DEVICE
```

## Usage

For more advanced use cases, you can also directly interface with Story Teller in Python code.

1. Load the model with defaults.

```python
from storyteller import StoryTeller

story_teller = StoryTeller.from_default()
story_teller.generate(...)
```

2. Alternatively, configure the model with custom settings.

```python
from storyteller import StoryTeller, StoryTellerConfig

config = StoryTellerConfig(
    writer="gpt2-large",
    painter="CompVis/stable-diffusion-v1-4",
    max_new_tokens=100,
)

story_teller = StoryTeller(config)
story_teller.generate(...)
```

## License

Released under the [MIT License](LICENSE).
