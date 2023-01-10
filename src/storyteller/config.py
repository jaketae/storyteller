from dataclasses import dataclass
from pathlib import Path


@dataclass
class StoryTellerConfig:
    image_size: int = 512
    max_new_tokens: int = 50
    writer: str = "gpt2"
    painter: str = "stabilityai/stable-diffusion-2"
    speaker: str = "tts_models/en/ljspeech/glow-tts"
    writer_device: str = "cuda:0"
    painter_device: str = "cuda:0"
    output_dir: str = Path(__file__).parent.parent / "out"
    seed: int = 42
    diffusion_prompt_prefix: str = "Beautiful painting"
