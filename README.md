# StoryTeller

A multimodal AI story teller, built with [Stable Diffusion](https://huggingface.co/spaces/stabilityai/stable-diffusion), GPT, and neural text-to-speech (TTS).

Given a prompt as an opening line of a story, GPT writes the rest of the plot; Stable Diffusion draws an image for each sentence; a TTS model narrates each line, resulting in a fully animated video of a short story, replete with audio and visuals.

## Demo

https://user-images.githubusercontent.com/25360440/210068543-e66ebdd9-7d4b-4bca-8db2-9e8b4d145037.mp4

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

1. Load the model with defaults.

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

## License

Released under the [MIT License](LICENSE).
