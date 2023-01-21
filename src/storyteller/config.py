from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict, Type

import torch


class StoryTellerConfigDefaults:
    MAX_NEW_TOKENS: int = 50
    WRITER_MODEL: str = "gpt2"
    PAINTER_MODEL: str = "stabilityai/stable-diffusion-2"
    SPEAKER_MODEL: str = "tts_models/en/ljspeech/glow-tts"
    WRITER_DEVICE: str = "cuda:0" if torch.cuda.is_available() else "cpu"
    PAINTER_DEVICE: str = "cuda:0" if torch.cuda.is_available() else "cpu"


@dataclass
class StoryTellerConfig:
    max_new_tokens: int = StoryTellerConfigDefaults.MAX_NEW_TOKENS
    writer: str = StoryTellerConfigDefaults.WRITER_MODEL
    painter: str = StoryTellerConfigDefaults.PAINTER_MODEL
    speaker: str = StoryTellerConfigDefaults.SPEAKER_MODEL
    writer_device: str = StoryTellerConfigDefaults.WRITER_DEVICE
    painter_device: str = StoryTellerConfigDefaults.PAINTER_DEVICE


class StoryTellerConfigArgparseHelpText:
    @staticmethod
    def _get_dataclass_var_name_from_f_string_eq(expression: str) -> str:
        return expression.split(".")[1].split("=")[0]

    # importing from typing for backwards compatibility
    _argparse_help_text: Dict[str, str] = {
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.max_new_tokens=}"
        ): f"Maximum number of new tokens to generate in the writer model. Default: {StoryTellerConfigDefaults.MAX_NEW_TOKENS}",
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.writer=}"
        ): f"Text generation model to use. Default: '{StoryTellerConfigDefaults.WRITER_MODEL}'",
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.painter=}"
        ): f"Image generation model to use. Default: '{StoryTellerConfigDefaults.PAINTER_MODEL}'",
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.speaker=}"
        ): f"Text-to-speech (TTS) generation model. Default: '{StoryTellerConfigDefaults.SPEAKER_MODEL}'",
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.writer_device=}"
        ): f"Text generation device to use. Default: '{StoryTellerConfigDefaults.WRITER_DEVICE}'",
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.painter_device=}"
        ): f"Image generation device to use. Default: '{StoryTellerConfigDefaults.PAINTER_DEVICE}'",
    }

    @classmethod
    def get_help_text_for_var_name(
        cls: Type[StoryTellerConfigArgparseHelpText], var_name: str
    ) -> str:
        try:
            return cls._argparse_help_text[var_name]
        except KeyError:
            print(
                f"Warning: Helper text for {var_name} not found. Returning empty string.",
                file=sys.stderr,
            )
            return ""
