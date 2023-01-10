import argparse

from storyteller import StoryTeller


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt", type=str, default="Once upon a time, unicorns roamed the Earth."
    )
    parser.add_argument("--num_images", type=int, default=10)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    story_teller = StoryTeller.from_default()
    story_teller.generate(args.prompt, args.num_images)


if __name__ == "__main__":
    main()
