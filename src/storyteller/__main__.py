import argparse
import dataclasses
from dataclasses import fields

from storyteller import StoryTeller, StoryTellerConfig


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt", type=str, default="Once upon a time, unicorns roamed the Earth."
    )
    default_config = StoryTellerConfig()
    for key, value in dataclasses.asdict(default_config).items():
        parser.add_argument(f"--{key}", type=type(value), default=value)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    config = StoryTellerConfig()
    for field in fields(config):
        name = field.name
        setattr(config, name, getattr(args, name))
    story_teller = StoryTeller(config)
    story_teller.generate(args.prompt, args.num_images)


if __name__ == "__main__":
    main()
