import json
from typing import Literal
import os


def get_token(token_name: Literal['DISCORD_TOKEN', 'NEIS_TOKEN']):
    return os.environ[token_name]
