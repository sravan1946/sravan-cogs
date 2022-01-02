import asyncio
from typing import Literal
import random
import logging

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

log = logging.getLogger("red.sravan.gtn")

class GuessTheNumber(commands.Cog):
    """
    a simple gtn game
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=43624556345246235424236,
            force_registration=True,
        )

    
    
    @commands.command()
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def gtn(self, ctx: commands.Context):
        """start a gtn event"""
        user = ctx.author
        range = await self.get_vaules(ctx, user)
        def check(m):
            return m.author == ctx.author and m.channel == user.dm_channel
        if range is None:
            return
        low, high = int(range[0]), int(range[1])
        try:
            await user.send("Do u want the bot to pick a random number in the range?(y/n)")
            confirmation = await self.bot.wait_for("message", check=check, timeout=60)
            if confirmation.content.lower() in ["y", "yes"]:
                number = random.randint(int(low), int(high))
            elif confirmation.content.lower() in ["n", "no"]:
                await user.send("Please enter the number to be guessed")
                number = await self.bot.wait_for("message", check=check, timeout=60)
                number = number.content
            else:
                await user.send("Please enter a valid answer")
                await ctx.channel.send("Could not start the gtn event")
                return
        except asyncio.TimeoutError:
            await user.send("You took too long to enter a number")
            await ctx.channel.send("Could not start the gtn event")
            return
        if int(number) <= low or int(number) >= high:
            await user.send("The number is not in the range")
            await ctx.channel.send("Could not start the gtn event")
            return
        await user.send(f"The number is {number}")
        await ctx.channel.send(f"{user.mention} has started a gtn event for number between {low} and {high}")
        started = True
        guesses = 1
        while started:
            guess = await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel)
            if guess.content.isdigit() and int(guess.content) == number:
                await ctx.channel.send(f"{guess.author.mention} has guessed the number. It took {guesses} guesses")
                started = False
                break
            else:
                guesses += 1
            if (
                guess.content.lower() == "cancel"
                and guess.author.id == ctx.author.id
            ):
                await ctx.channel.send(f"{user.mention} has cancelled the gtn event.")
                started = False
                break

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    async def get_vaules(self, ctx: commands.Context, user):
        """ask the range and the number to be guessed in the users DM"""
        await ctx.tick()
        def check(m):
            return m.author == ctx.author and m.channel == user.dm_channel

        await user.send("Please enter the range of the number you want to guess. (e.g. 1-10, 1-100, 200-600)")
        try:
            _range = await self.bot.wait_for("message", check=check, timeout=60)
            # check if the range is a number and in the correct format
            if _range.content.count("-") == 1:
                _range = _range.content.split("-")
                if _range[0].isdigit() and _range[1].isdigit():
                    if int(_range[0]) < int(_range[1]):
                        return _range
                    await user.send("The first number is higher than the second number")
                    await ctx.channel.send("Could not start the gtn event")
                    return
                else:
                    await user.send("The range is not a number")
                    await ctx.channel.send("Could not start the gtn event")
                    return
            else:
                await user.send("The range is not in the correct format")
                await ctx.channel.send("Could not start the gtn event")
                return
        except asyncio.TimeoutError:
            await user.send("You took too long to enter a range")
            await ctx.channel.send("Could not start the gtn event")
            return
        except Exception as e:
            await user.send('Something went wrong, please try again')
            await ctx.channel.send("Could not start the gtn event")
            return 
