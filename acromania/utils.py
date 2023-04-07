import datetime
import re

from redbot.core import commands
from redbot.core.utils import mod

TIME_UNITS: dict = {
    "name": {
        "w": ("w", "week", "weeks"),
        "d": ("d", "day", "days"),
        "h": ("h", "hr", "hrs", "hour", "hours"),
        "m": ("m", "min", "mins", "minute", "minutes"),
        "s": ("s", "sec", "secs", "second", "seconds"),
    },
    "value": {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1},
}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, time: str):
        seconds = await self.parse(time)
        if seconds:
            delta = datetime.timedelta(seconds=seconds)
            return int(delta.total_seconds())

    @staticmethod
    async def parse(timestring: str):
        seconds: int = 0
        t_name, t_value = TIME_UNITS["name"], TIME_UNITS["value"]
        if objects := re.findall(r"(\d+)([a-zA-Z]+)", timestring.lower()):
            for item in objects:
                number, unit = item
                if unit in t_name["w"]:
                    seconds += int(number) * t_value["w"]
                elif unit in t_name["d"]:
                    seconds += int(number) * t_value["d"]
                elif unit in t_name["h"]:
                    seconds += int(number) * t_value["h"]
                elif unit in t_name["m"]:
                    seconds += int(number) * t_value["m"]
                elif unit in t_name["s"]:
                    seconds += int(number) * t_value["s"]
        return seconds or None


async def is_manager(ctx):
    if not ctx.guild:
        return False
    if await ctx.bot.is_owner(ctx.author):
        return True
    elif (
        ctx.channel.permissions_for(ctx.author).administrator
        or ctx.channel.permissions_for(ctx.author).manage_guild
    ):
        return True
    else:
        cog = ctx.bot.get_cog("Acronym")
        manager = await cog.config.guild(ctx.guild).manager()
        return manager in [r.id for r in ctx.author.roles] if manager else False
