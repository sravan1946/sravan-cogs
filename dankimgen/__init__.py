import asyncio
import json
from pathlib import Path

from redbot.core.bot import Red

from .dankimgen import DankImgen

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


async def setup_after_ready(bot: Red) -> None:
    await bot.wait_until_red_ready()
    cog = DankImgen(bot)
    await cog.initalize()
    for name, command in cog.all_commands.items():
        if not command.parent:
            if bot.get_command(name):
                command.name = f"dm{command.name}"
            for alias in command.aliases:
                if bot.get_command(alias):
                    command.aliases[command.aliases.index(alias)] = f"dm{alias}"
    await bot.add_cog(cog)


async def setup(bot: Red) -> None:
    asyncio.create_task(setup_after_ready(bot))
