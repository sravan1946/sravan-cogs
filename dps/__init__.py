import json
from pathlib import Path

from redbot.core.bot import Red

from .dps import DontPingStaff

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


async def setup(bot: Red) -> None:
    cog = DontPingStaff(bot)
    await cog.gen_cache()
    await bot.add_cog(cog)
