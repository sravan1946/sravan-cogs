import asyncio
import logging
import random
from typing import List, Literal, Optional

import discord
from redbot.core import commands
from redbot.core.bot import Red

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

log = logging.getLogger("red.sravan.gtn")

YES_ANSWERS = ["y", "yes"]
NO_ANSWERS = ["n", "no"]
CANCEL_ANSWERS = ["cancel"]


class GuessTheNumber(commands.Cog):
    """
    A simple gtn game.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot

    __author__ = ["sravan"]
    __version__ = "1.3.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    async def get_values(
        self, ctx: commands.Context, user: discord.User
    ) -> Optional[List[str]]:
        """
        Ask the range and the number to be guessed in the users DM.
        """
        await ctx.tick()

        def check(m):
            return m.author == ctx.author and m.channel == user.dm_channel

        try:
            await user.send(
                "Please enter the range of the number you want to guess. (e.g. 1-10, 1-100, 200-600)"
            )
        except discord.Forbidden:
            await ctx.channel.send("Could not send DM to user")
            return
        try:
            _range: discord.Message = await self.bot.wait_for(
                "message", check=check, timeout=60
            )
            if _range.content.count("-") != 1:
                await user.send("The range is not in the correct format")
                await ctx.channel.send("Could not start the gtn event")
                return
            _range = _range.content.split("-")
            try:  # for checking if the range is a number
                if int(_range[0]) < int(_range[1]):
                    return _range
                await user.send(
                    "The first number is higher than the second number"
                    if _range[0] != _range[1]
                    else "Both numbers are the same"
                )
                await ctx.channel.send("Could not start the gtn event")
                return
            except ValueError:
                await user.send("The range is not a number")
                await ctx.channel.send("Could not start the gtn event")
                return
        except asyncio.TimeoutError:
            await user.send("You took too long to enter a range")
            await ctx.channel.send("Could not start the gtn event")
            return

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def gtn(self, ctx: commands.Context):
        """
        Start a gtn event.
        """
        user: discord.Member = ctx.author
        _range = await self.get_values(ctx, user)

        if _range is None:
            return

        low, high = int(_range[0]), int(_range[1])
        number = await self.get_number_to_guess(ctx, user, low, high)

        if number is None:
            return

        await user.send(f"The number is {number}")
        startem = discord.Embed(
            title="Game started",
            description=f"{user.mention} has started a game of guess the number",
            colour=await ctx.embed_colour(),
        )
        startem.add_field(name="Range", value=f"{low}-{high}")
        starting_message = await ctx.message.reply(embed=startem)
        pinned = False
        try:
            await starting_message.pin()
            pinned = True
        except discord.Forbidden:
            await ctx.send("I do not have permissions to pin the message")
        except discord.HTTPException:
            await ctx.send("Could not pin the message due to too many pins")
        started = True
        guesses = 1
        participant = set()
        while started:
            guess = await self.bot.wait_for(
                "message", check=lambda m: m.channel == ctx.channel
            )
            if guess.content.isdigit():
                try:
                    guessed_number = int(guess.content)
                except ValueError:
                    continue
                participant.add(guess.author)
                if guessed_number == number:
                    winem = discord.Embed()
                    winem.set_author(
                        name=f"{guess.author.display_name} has won the gtn event",
                        icon_url=guess.author.display_avatar,
                    )
                    winem.color = await ctx.embed_colour()
                    winem.add_field(name="Number of guesses", value=f"> {guesses}")
                    winem.add_field(name="Participants", value=f"> {len(participant)}")
                    winem.add_field(
                        name="Number guessed", value=f"> {guess.content}", inline=False
                    )
                    winem.set_footer(
                        text="Thanks for playing!",
                    )
                    winem.set_thumbnail(url=ctx.guild.icon)
                    await guess.reply(embed=winem, content=ctx.author.mention)
                    if pinned:
                        await starting_message.unpin()
                    started = False
                    break
                else:
                    guesses += 1
            if (
                guess.content.lower() in CANCEL_ANSWERS
                and guess.author.id == ctx.author.id
            ):
                await ctx.channel.send(f"{user.mention} has cancelled the gtn event.")
                if pinned:
                    await starting_message.unpin()
                started = False
                break

    async def get_number_to_guess(
        self, ctx: commands.Context, user: discord.User, low: int, high: int
    ) -> Optional[int]:
        def check(m):
            return m.author == ctx.author and m.channel == user.dm_channel

        try:
            await user.send(
                "Do u want the bot to pick a random number in the range?(y/n)"
            )
            confirmation = await self.bot.wait_for("message", check=check, timeout=60)
            if confirmation.content.lower() in YES_ANSWERS:
                return random.randint(low, high)
            elif confirmation.content.lower() in NO_ANSWERS:
                await user.send("Please enter the number to be guessed")
                number = await self.bot.wait_for("message", check=check, timeout=60)
                try:
                    number = int(number.content)
                except ValueError:
                    await user.send("This is not a valid number")
                    await ctx.channel.send("Could not start the gtn event")
                    return None
                return number
            else:
                await user.send("Please enter a valid answer")
                await ctx.channel.send("Could not start the gtn event")
                return None
        except asyncio.TimeoutError:
            await user.send("You took too long to enter a number")
            await ctx.channel.send("Could not start the gtn event")
            return None
