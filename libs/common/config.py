import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    """
    기본 Configuration
    """
    pass


@dataclass
class LocalConfig(Config):
    TEST_GUILD_ID: Optional[list[int]] = field(default_factory=lambda: [802077280074465280, 1053873141237153822])


@dataclass
class ProductConfig(Config):
    TEST_GUILD_ID: Optional[list[int]] = None


def conf():
    config = dict(product=ProductConfig(), local=LocalConfig())
    return config.get(os.environ.get("BOT_ENV", "local"))
