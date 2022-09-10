import asyncio
import contextlib
from typing import Literal

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

EMOJIS = ["None", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


class Poll(commands.Cog):
    """
    make polls
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=23487129235,
            force_registration=True,
        )

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    @commands.command(name="quickpoll")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def quickpoll(self, ctx, *, question: str):
        """
        make a simple poll
        """
        with contextlib.suppress(discord.Forbidden):
            await ctx.message.delete()
        embed = discord.Embed(
            title=f"**{question}**",
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        e = await ctx.send(embed=embed)
        asyncio.sleep(1)
        await e.add_reaction("⬆")
        await e.add_reaction("⬇")

    @commands.command(name="poll")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def poll(self, ctx, *, question: str):
        """
        Make a poll with multiple options

        Each option must be seperated by a |.
        Maximum number options is 10.
        """
        with contextlib.suppress(discord.Forbidden):
            await ctx.message.delete()
        questions = question.split("|")
        questions = list(zip(EMOJIS, questions))
        num = len(questions)
        if num > 11:
            return await ctx.send("You can only have 10 options in a poll")
        if num < 3:
            return await ctx.send("You need at least 2 options to make a poll")
        embed = discord.Embed(
            title=f"**{questions[0][1]}**",
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.description = "\n".join([f"{i[0]} | {i[1]}" for i in questions[1:]])
        e = await ctx.send(embed=embed)
        for i in range(1, num):
            await e.add_reaction(EMOJIS[i])
