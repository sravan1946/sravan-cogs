import datetime
import random
import re
import string

import discord
from redbot.core import commands

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


async def is_manager(ctx) -> bool:
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
        cog = ctx.bot.get_cog("Acromania")
        manager = await cog.config.guild(ctx.guild).manager()
        return manager in [r.id for r in ctx.author.roles] if manager else False

async def generate_acronym() -> str:
    return ".".join(random.choices(string.ascii_uppercase, k=random.randint(3, 5)))


async def valid_guess(guess: discord.Message, acronym: str) -> bool:
    acro = acronym.split(".")
    for i, word in enumerate(guess.content.split()):
        if i >= len(acro):
            return False
        if word[0].lower() != acro[i][0].lower():
            return False
    return len(guess.content.split()) == len(acro)


async def valid_vote(vote: discord.Message, data: dict) -> bool:
    author = vote.author.id
    try:
        vote = int(vote.content)
    except ValueError:
        return False
    return next(
        (
            False
            for i, (k, v) in enumerate(data.items(), 1)
            if k == author and i == vote
        ),
        vote >= 1 and vote <= len(data),
    )


async def gen_cache(self, ctx: commands.Context, acronym: str) -> None:
    self.cache[ctx.channel.id] = {acronym: {"votes": {}}}


async def add_guess(
    self, ctx: commands.Context, guess: discord.Message, acronym: str
) -> None:
    if ctx.channel.id not in self.cache:
        await gen_cache(self, ctx, acronym)
    if acronym not in self.cache[ctx.channel.id]:
        await gen_cache(self, ctx, acronym)
    if guess.author.id not in self.cache[ctx.channel.id][acronym]:
        self.cache[ctx.channel.id][acronym][guess.author.id] = guess.content


async def add_vote(
    self, ctx: commands.Context, vote: discord.Message, acronym: str
) -> None:
    data = self.cache[ctx.channel.id][acronym]
    if vote.content not in data["votes"]:
        data["votes"][vote.content] = 1
    else:
        data["votes"][vote.content] += 1


async def gen_results(self, ctx: commands.Context, acronym: str) -> None:
    data = self.cache[ctx.channel.id][acronym]
    data = {k: v for k, v in data.items() if k != "votes"}
    votes = self.cache[ctx.channel.id][acronym]["votes"]
    results = {}
    for guess, vote in votes.items():
        guess = int(guess)
        for i, (k, v) in enumerate(data.items(), 1):
            if i == guess:
                results[v] = [k, vote]
    return results


async def send_embed(ctx: commands.Context, results: dict) -> None:
    embed = discord.Embed(title="Acromania Results", color=await ctx.embed_color())
    if not results:
        return await ctx.send("There was no votes for this round.")
    results = dict(sorted(results.items(), key=lambda item: item[1][1], reverse=True))
    mes = ""
    for k, v in results.items():
        user = ctx.guild.get_member(v[0])
        votes = v[1]
        mes += f"{user.mention}: {k} ({votes} votes) \n"
        embed.description = mes
    await ctx.send(embed=embed)
