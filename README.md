# StoryTeller

A multimodal AI story teller, built with [Stable Diffusion](https://huggingface.co/spaces/stabilityai/stable-diffusion), GPT, and neural text-to-speech (TTS).

## Demo

## Quickstart

1. Clone the repository.

```
git clone https://github.com/jaketae/storyteller.git
```

2. Install package requirements.

```
pip install -U pip wheel
pip install -r requirements.txt
```

3. Run the demo. The final video will be saved as `/out/out.mp4`.

```
make run
```

## Usage

1. Load the model with defaults

```python
from storyteller import StoryTeller

story_teller = StoryTeller.from_defaults()
story_teller.generate(...)
```

2. Configure the model with custom settings.

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