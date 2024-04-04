import json
from pathlib import Path

from .timeout import setup  # noqa

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]
