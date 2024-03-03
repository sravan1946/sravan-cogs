from typing import Optional

import discord
from redbot.core import commands
from redbot.core.bot import Red


class HidePing(commands.Cog):
    """
    Hidden pings cuz its cool ig.
    """

    __author__ = ["sravan"]
    __version__ = "1.0.7"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command(name="hideping")
    @commands.mod_or_permissions(manage_messages=True)
    async def hideping(
        self, ctx: commands.Context, member: discord.Member, *, message: Optional[str]
    ):
        """
        Speak a message using a hidden ping!
        """
        if message is None:
            message = "ㅤ"
        msg = f"{message} " + "||\u200d" * 598 + f"<@{member.id}>"
        if len(msg) > 2000:
            return await ctx.send("Your message is too long.")
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            await ctx.tick()
        except discord.NotFound:  # when used with mock
            pass
        await ctx.send(msg)

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any data
        pass
