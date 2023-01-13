import os
from typing import List

import soundfile as sf
import torch
from diffusers import StableDiffusionPipeline
from nltk.tokenize import sent_tokenize
from PIL.Image import Image
from transformers import pipeline
from TTS.api import TTS

from storyteller import StoryTellerConfig
from storyteller.utils import (
    make_timeline_string,
    require_ffmpeg,
    require_punkt,
    subprocess_run,
)


class StoryTeller:
    @require_ffmpeg
    @require_punkt
    def __init__(self, config: StoryTellerConfig):
        self.config = config
        writer_device = torch.device(config.writer_device)
        painter_device = torch.device(config.writer_device)
        self.writer = pipeline(
            "text-generation", model=config.writer, device=writer_device
        )
        self.painter = StableDiffusionPipeline.from_pretrained(
            config.painter,
            use_auth_token=False,
        ).to(painter_device)
        self.speaker = TTS(config.speaker)
        self.sample_rate = self.speaker.synthesizer.output_sample_rate
        self.output_dir = None

    @classmethod
    def from_default(cls):
        config = StoryTellerConfig()
        return cls(config)

    @torch.inference_mode()
    def paint(self, prompt: str) -> Image:
        return self.painter(prompt).images[0]

    @torch.inference_mode()
    def speak(self, prompt: str) -> List[int]:
        return self.speaker.tts(prompt)

    @torch.inference_mode()
    def write(self, prompt: str) -> str:
        return self.writer(prompt, max_new_tokens=self.config.max_new_tokens)[0][
            "generated_text"
        ]

    def get_output_path(self, file: str) -> str:
        return os.path.join(self.output_dir, file)

    def generate(
        self,
        writer_prompt: str,
        painter_prompt_prefix: str,
        num_images: int,
        output_dir: str,
    ) -> None:
        video_paths = []
        self.output_dir = output_dir
        sentences = self.write_story(writer_prompt, num_images)
        for i, sentence in enumerate(sentences):
            video_path = self._generate(i, sentence, painter_prompt_prefix)
            video_paths.append(video_path)
        self.concat_videos(video_paths)

    def concat_videos(self, video_paths: List[str]) -> None:
        files_path = self.get_output_path("files.txt")
        output_path = self.get_output_path("out.mp4")
        with open(files_path, "w+") as f:
            for video_path in video_paths:
                f.write(f"file {os.path.split(video_path)[-1]}\n")
        subprocess_run(f"ffmpeg -f concat -i {files_path} -c copy {output_path}")

    def _generate(self, id_: int, sentence: str, painter_prompt_prefix: str) -> str:
        image_path = self.get_output_path(f"{id_}.png")
        audio_path = self.get_output_path(f"{id_}.wav")
        subtitle_path = self.get_output_path(f"{id_}.srt")
        video_path = self.get_output_path(f"{id_}.mp4")
        image = self.paint(f"{painter_prompt_prefix} {sentence}")
        image.save(image_path)
        audio = self.speak(sentence)
        duration, remainder = divmod(len(audio), self.sample_rate)
        if remainder:
            duration += 1
            audio.extend([0] * (self.sample_rate - remainder))
        sf.write(audio_path, audio, self.sample_rate)
        subtitle = f"0\n{make_timeline_string(0, duration)}\n{sentence}"
        with open(subtitle_path, "w+") as f:
            f.write(subtitle)
        subprocess_run(
            f"ffmpeg -loop 1 -i {image_path} -i {audio_path} -vf subtitles={subtitle_path} -tune stillimage -shortest {video_path}"
        )
        return video_path

    def write_story(self, writer_prompt: str, num_sentences: int) -> List[str]:
        sentences = []
        while len(sentences) < num_sentences + 1:
            writer_prompt = self.write(writer_prompt)
            sentences = sent_tokenize(writer_prompt)
        while len(sentences) > num_sentences:
            sentences.pop()
        return sentences
