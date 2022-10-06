import json
from typing import Literal
import os


def get_token(token_name: Literal['discord', 'neis']):
    with open('./token.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())[token_name]
