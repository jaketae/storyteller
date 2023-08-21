import argparse
import dataclasses
import logging
import os
from dataclasses import dataclass

from storyteller import StoryTeller, StoryTellerConfig
from storyteller.config import StoryTellerConfigArgparseHelpText
from storyteller.utils import set_log_level, set_seed


@dataclass(frozen=True)
class ArgparseDefaults:
    WRITER_PROMPT: str = "Once upon a time, unicorns roamed the Earth."
    PAINTER_PROMPT: str = "Beautiful painting"
    OUTPUT_DIR: str = "out"
    NUM_IMAGES: int = 10
    SEED: int = 42


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--writer_prompt",
        type=str,
        default=ArgparseDefaults.WRITER_PROMPT,
        help=f"The prompt to be used for the writer model. This is the text with which your story will begin. Default: '{ArgparseDefaults.WRITER_PROMPT}'",
    )
    parser.add_argument(
        "--painter_prompt_prefix",
        type=str,
        default=ArgparseDefaults.PAINTER_PROMPT,
        help=f"The prefix to be used for the painter model's prompt. Default: '{ArgparseDefaults.PAINTER_PROMPT}'",
    )
    parser.add_argument(
        "--num_images",
        type=int,
        default=ArgparseDefaults.NUM_IMAGES,
        help=f"The number of images to be generated. Those images will be composed in sequence into a video. Default: {ArgparseDefaults.NUM_IMAGES}",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=ArgparseDefaults.OUTPUT_DIR,
        help=f"The directory to save the generated files to. Default: '{ArgparseDefaults.OUTPUT_DIR}'",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=ArgparseDefaults.SEED,
        help=f"The seed value to be used for randomization. Default: {ArgparseDefaults.SEED}",
    )
    default_config = StoryTellerConfig()
    for key, value in dataclasses.asdict(default_config).items():
        parser.add_argument(
            f"--{key}",
            type=type(value),
            default=value,
            help=StoryTellerConfigArgparseHelpText.get_help_text_for_var_name(key),
        )
    return parser.parse_args()


def main() -> None:
    args = get_args()
    set_seed(args.seed)
    set_log_level(logging.WARNING)
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    config = StoryTellerConfig(
        **{
            field.name: getattr(args, field.name)
            for field in dataclasses.fields(StoryTellerConfig)
        }
    )
    story_teller = StoryTeller(config)
    os.makedirs(args.output_dir, exist_ok=True)
    story_teller.generate(
        args.writer_prompt, args.painter_prompt_prefix, args.num_images, args.output_dir
    )


if __name__ == "__main__":
    main()
