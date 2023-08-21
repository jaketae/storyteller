from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict, Type

import torch


@dataclass(frozen=True)
class StoryTellerConfigDefaults:
    MAX_NEW_TOKENS: int = 50
    WRITER_MODEL: str = "gpt2"
    PAINTER_MODEL: str = "stabilityai/stable-diffusion-2"
    SPEAKER_MODEL: str = "tts_models/en/ljspeech/glow-tts"
    WRITER_DEVICE: str = "cpu"
    PAINTER_DEVICE: str = "cpu"
    WRITER_DTYPE: str = "float32"
    PAINTER_DTYPE: str = "float32"
    ENABLE_ATTENTION_SLICING: bool = False
    USE_DPM_SOLVER: bool = True
    NUM_PAINTER_STEPS: int = 20


@dataclass
class StoryTellerConfig:
    max_new_tokens: int = StoryTellerConfigDefaults.MAX_NEW_TOKENS
    writer: str = StoryTellerConfigDefaults.WRITER_MODEL
    painter: str = StoryTellerConfigDefaults.PAINTER_MODEL
    speaker: str = StoryTellerConfigDefaults.SPEAKER_MODEL
    writer_device: str = StoryTellerConfigDefaults.WRITER_DEVICE
    painter_device: str = StoryTellerConfigDefaults.PAINTER_DEVICE
    writer_dtype: str = StoryTellerConfigDefaults.WRITER_DTYPE
    painter_dtype: str = StoryTellerConfigDefaults.PAINTER_DTYPE
    enable_attention_slicing: bool = StoryTellerConfigDefaults.ENABLE_ATTENTION_SLICING
    use_dpm_solver: bool = StoryTellerConfigDefaults.USE_DPM_SOLVER
    num_painter_steps: int = StoryTellerConfigDefaults.NUM_PAINTER_STEPS

    def __post_init__(self):
        if not hasattr(torch, self.writer_dtype):
            raise ValueError(f"Unsupported torch writer dtype {self.writer_dtype}")
        if not hasattr(torch, self.painter_dtype):
            raise ValueError(f"Unsupported torch painter dtype {self.painter_dtype}")


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
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.writer_dtype=}"
        ): f"Text generation dtype to use. Default: '{StoryTellerConfigDefaults.WRITER_DTYPE}'",
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.painter_dtype=}"
        ): f"Image generation dtype to use. Default: '{StoryTellerConfigDefaults.PAINTER_DTYPE}'",
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.enable_attention_slicing=}"
        ): f"Whether to enable attention slicing for diffusion. Default: '{StoryTellerConfigDefaults.ENABLE_ATTENTION_SLICING}'",
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.use_dpm_solver=}"
        ): f"Whether to use DPM solver for faster generation. Default: '{StoryTellerConfigDefaults.USE_DPM_SOLVER}'",
        _get_dataclass_var_name_from_f_string_eq(
            f"{StoryTellerConfig.num_painter_steps=}"
        ): f"Number of inference steps for stable diffusion. Default: '{StoryTellerConfigDefaults.NUM_PAINTER_STEPS}'",
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
