import logging
import os
import random
import shutil
import subprocess
from functools import wraps
from typing import Callable

import nltk
import numpy as np
import torch


def require_ffmpeg(func: Callable) -> Callable:
    """Decorator for checking ffmpeg installation."""

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if shutil.which("ffmpeg") is None:
            raise RuntimeError(
                "`ffmpeg` not found. Please install `ffmpeg` and try again."
            )
        func(*args, **kwargs)

    return wrapper_func


def require_punkt(func: Callable) -> Callable:
    """Decorator for checking nltk punkt module."""

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")
        func(*args, **kwargs)

    return wrapper_func


def make_timeline_string(start: int, end: int) -> str:
    """Create timeline string to write onto .srt subtitle files."""
    start = format_time(start)
    end = format_time(end)
    return f"{start} --> {end}"


def format_time(time: int):
    """Transform time (seconds) to .srt format."""
    mm, ss = divmod(time, 60)
    hh, mm = divmod(mm, 60)
    return f"{hh:02d}:{mm:02d}:{ss:02d},000"


def subprocess_run(command: str) -> None:
    """Wrapper around `subprocess.run()` with /dev/null redirection in stdout and stderr."""
    subprocess.run(
        command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def set_seed(seed: int) -> None:
    """Set seed."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True


def set_log_level(level: int) -> None:
    """Disables specified logging level and below."""
    logging.disable(level)
