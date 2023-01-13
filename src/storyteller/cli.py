import argparse
import dataclasses
import logging
import os

from storyteller import StoryTeller, StoryTellerConfig
from storyteller.utils import set_log_level, set_seed


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--writer_prompt",
        type=str,
        default="Once upon a time, unicorns roamed the Earth.",
    )
    parser.add_argument(
        "--painter_prompt_prefix", type=str, default="Beautiful painting"
    )
    parser.add_argument("--num_images", type=int, default=10)
    parser.add_argument("--output_dir", type=str, default="out")
    parser.add_argument("--seed", type=int, default=42)
    default_config = StoryTellerConfig()
    for key, value in dataclasses.asdict(default_config).items():
        parser.add_argument(f"--{key}", type=type(value), default=value)
    args = parser.parse_args()
    return args


def main() -> None:
    args = get_args()
    set_seed(args.seed)
    set_log_level(logging.WARNING)
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    config = StoryTellerConfig()
    for field in dataclasses.fields(config):
        name = field.name
        setattr(config, name, getattr(args, name))
    story_teller = StoryTeller(config)
    os.makedirs(args.output_dir, exist_ok=True)
    story_teller.generate(
        args.writer_prompt, args.painter_prompt_prefix, args.num_images, args.output_dir
    )


if __name__ == "__main__":
    main()
