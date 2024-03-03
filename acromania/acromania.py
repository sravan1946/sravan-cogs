import asyncio
import datetime
import time
from typing import Literal

import discord
from discord.utils import format_dt
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core.utils.chat_formatting import pagify

from .utils import (
    TimeConverter,
    add_guess,
    add_vote,
    gen_results,
    generate_acronym,
    is_manager,
    send_embed,
    valid_guess,
    valid_vote,
)

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Acromania(commands.Cog):
    """
    The Acromania Game.

    The acromania game is a fun and challenging wordplay activity where players create phrases or sentences using the letters from a chosen acronym.
    """

    __author__ = ["sravan"]
    __version__ = "1.2.0"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=24123,
            force_registration=True,
        )
        default_guild = {
            "manager": [],
            "guessing_time": 60,
            "voting_time": 60,
        }
        self.config.register_guild(**default_guild)
        self.cache = {}

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nVersion: {self.__version__}"

    @commands.group(aliases=["acro", "acronym"])
    @commands.guild_only()
    async def acromania(self, ctx: commands.Context) -> None:
        """
        An Acromania Game.

        You can now play the fun acronym game with all your friends directly from your Discord server.
        """

    @acromania.group(name="set")
    @commands.admin()
    async def _set(self, ctx: commands.Context) -> None:
        """
        Manage the acromania settings.

        Customize the game settings as per your liking.
        """

    @_set.group()
    async def manager(self, ctx: commands.Context) -> None:
        """
        Sets the manager `role` who can start an acro game."""

    @manager.command(name="add")
    async def add_manager(self, ctx: commands.Context, role: discord.Role) -> None:
        """
        Adds a role who can start acro game.

        Users with any of these roles will be able to manage/start an acromania game."""
        async with self.config.guild(ctx.guild).manager() as m:
            if role.id in m:
                await ctx.reply(f"{role.mention} is already set as manager role.")
                return
            m.append(role.id)
        await ctx.send(f"Successfully added {role.mention} as manager.")

    @manager.command(name="remove")
    async def remove_manager(self, ctx: commands.Context, role: discord.Role) -> None:
        """
        Removes a role from the list of managers, that can start acromania game."""
        async with self.config.guild(ctx.guild).manager() as m:
            if role.id not in m:
                await ctx.reply(f"{role.mention} is not a manager role.")
                return
            m.remove(role.id)
        await ctx.send(f"Successfully removed {role.mention} as manager.")

    @manager.command(name="list")
    async def list_manager(self, ctx: commands.Context) -> None:
        """
        Lists the manager roles."""
        m = await self.config.guild(ctx.guild).manager()
        if not m:
            return await ctx.send("No manager roles are set.")
        roles = [ctx.guild.get_role(role).mention for role in m]
        for page in pagify(", ".join(roles), delims=",", shorten_by=0):
            await ctx.send(page)

    @_set.command()
    async def guessingtime(self, ctx: commands.Context, time: TimeConverter) -> None:
        """
        This allows you to specify the duration for the voting window. 

        Once the specified time elapses, the voting process will be closed, and the winner will be declared based on the highest number of votes received.

        **Example**
        - `<p>acromania set votingtime 1m` - This will set the voting window to 1 minute.
        - `[p]acromania set votingtime 30s` - This will set the voting window to 30 seconds.
        """
        if time is None:
            return await ctx.send("Invalid time provided.")
        await self.config.guild(ctx.guild).guessing_time.set(time)
        await ctx.send(f"Time is set to {time}s")
        return

    @_set.command()
    async def votingtime(self, ctx: commands.Context, time: TimeConverter) -> None:
        """
        Sets the time after which the voting window is closed & winner is declared."""
        if time is None:
            return await ctx.send("Invalid time provided.")
        await self.config.guild(ctx.guild).voting_time.set(time)
        await ctx.send(f"Time is set to {time}s")
        return

    @_set.command(aliases=["ss"])
    @commands.bot_has_permissions(embed_links=True)
    async def showsettings(self, ctx: commands.Context) -> None:
        """
        Shows the current settings for acromania."""
        guessing_time = await self.config.guild(ctx.guild).guessing_time()
        voting_time = await self.config.guild(ctx.guild).voting_time()
        manager = await self.config.guild(ctx.guild).manager()
        manager = [ctx.guild.get_role(role).mention for role in manager]
        em = discord.Embed(
            title="Acromania Settings",
            color=await ctx.embed_color(),
            description=f"**Guessing Time**: {guessing_time}s\n**Voting Time**: {voting_time}s",
        )
        await ctx.send(embed=em)

    @acromania.command()
    @commands.bot_has_permissions(add_reactions=True, embed_links=True)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def start(self, ctx: commands.Context) -> None:
        """
        Starts the acromania game.
        """
        if not await is_manager(ctx):
            return await ctx.send("You are not allowed to start an acromania game.")
        acronym = await generate_acronym()
        guessing_time: int = await self.config.guild(ctx.guild).guessing_time()
        startem = discord.Embed(
            title="Acromania Game",
            description=f"Guess the acronym: **`{acronym}`**",
            color=await ctx.embed_color(),
        )
        startem.set_footer(text=f"You have {guessing_time}s to guess.")
        await ctx.send(embed=startem)
        endtime = time.time() + guessing_time
        guessed = set()
        while not time.time() >= endtime:
            try:
                guess: discord.Message = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.channel == ctx.channel and not m.author.bot,
                    timeout=1,
                )
            except asyncio.TimeoutError:
                continue
            if guess.author.id == ctx.author.id and guess.content == "CANCEL":
                return await ctx.send("Cancelled.")
            valid = await valid_guess(guess, acronym)
            if valid:
                if guess.author.id not in guessed:
                    await add_guess(self, ctx, guess, acronym)
                    guessed.add(guess.author.id)
                try:
                    await guess.delete()
                except discord.HTTPException:
                    await guess.add_reaction("✅")
        await ctx.send("Time's up! \nAll guesses have been collected.")

        try:
            data: dict = self.cache[ctx.channel.id][acronym]
        except KeyError:
            return await ctx.send("No guesses were made.")
        guesses_em = discord.Embed(
            title=f"Guesses for {acronym}", color=await ctx.embed_color()
        )
        data = {k: v for k, v in data.items() if k != "votes"}
        desc = "".join(
            f"{i}. {guess} \n" for i, (user, guess) in enumerate(data.items(), 1)
        )
        guesses_em.description = desc

        voting_time = await self.config.guild(ctx.guild).voting_time()
        timestamp = datetime.datetime.now() + datetime.timedelta(seconds=voting_time)
        endtime = time.time() + voting_time
        vote_em = discord.Embed(
            title="Vote for the best guess.",
            description=f"Use the number to vote for the guess. \nVoting time ends in {format_dt(timestamp, style='R')} \n :warning: You can only vote once.",
            color=await ctx.embed_color(),
        )
        await ctx.send(embeds=[guesses_em, vote_em])

        voted = set()
        while not time.time() >= endtime:
            try:
                vote = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.channel == ctx.channel and not m.author.bot,
                    timeout=1,
                )
            except asyncio.TimeoutError:
                continue
            if vote.author.id == ctx.author.id and vote.content == "CANCEL":
                return await ctx.send("Cancelled.")
            valid = await valid_vote(vote, data)
            if valid and vote.author.id not in voted:
                await add_vote(self, ctx, vote, acronym)
                voted.add(vote.author.id)
                await vote.add_reaction("✅")
        await ctx.send("Voting Time's up! \nAll votes have been collected.")
        result = await gen_results(self, ctx, acronym)
        await send_embed(ctx, result)

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)
