import json
from pathlib import Path

from redbot.core.bot import Red

from .devlogs import DevLogs

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]

try:
    from redbot.core.errors import CogLoadError
except ImportError:
    CogLoadError = RuntimeError

async def setup(bot: Red) -> None:
    if "Dev" not in bot.cogs:
        raise CogLoadError("This cog requires the bot to be started with the `--dev` flag.")
    bot.add_cog(DevLogs(bot))
