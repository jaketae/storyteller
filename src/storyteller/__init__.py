from importlib import metadata

from storyteller.config import StoryTellerConfig
from storyteller.model import StoryTeller

__version__ = metadata.version("storyteller-core")
__all__ = ["__version__", "StoryTellerConfig", "StoryTeller"]
