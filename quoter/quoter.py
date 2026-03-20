from typing import Literal, Optional

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Quoter(commands.Cog):
    """
    A simple cog to quote some text.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=298742345,
            force_registration=True,
        )
        default_guild = {
            "channel": None,
        }
        self.config.register_guild(**default_guild)

    __author__ = ["sravan"]
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    @commands.group(name="quoteset")
    @commands.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    async def quoteset(self, ctx: commands.Context) -> None:
        """
        Quote configuration commands.
        """

    @quoteset.command(name="channel")
    async def quoteset_channel(
        self, ctx: commands.Context, channel: Optional[discord.TextChannel]
    ) -> None:
        """
        Set the channel where quotes will be sent.

        If no channel is provided, it will show the current setting.
        """
        if channel:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(f"Quotes will now be sent to {channel.mention}.")
        else:
            channel_id = await self.config.guild(ctx.guild).channel()
            if channel_id:
                channel = ctx.guild.get_channel(channel_id)
                if channel:
                    await ctx.send(f"Quotes are currently sent to {channel.mention}.")
                else:
                    await ctx.send(
                        "The quote channel no longer exists. Please set a new one using `[p]quoteset channel #channel`."
                    )
            else:
                await ctx.send(
                    "No quote channel set. Use `[p]quoteset channel #channel` to set one."
                )
                return

    @commands.command(name="quote")
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def quote(
        self, ctx: commands.Context, user: Optional[discord.Member], *, text: str = ""
    ) -> None:
        """
        Send a quote to the configured channel.

        Usage: `[p]quote [user] [text]`

        If `user` is not provided, the quote will be sent as a general quote.
        """
        channel_id = await self.config.guild(ctx.guild).channel()

        if not channel_id:
            await ctx.send(
                "No quote channel set. Use `[p]quoteset channel #channel` to set one."
            )
            return

        channel = ctx.guild.get_channel(channel_id)
        if not channel:
            await ctx.send(
                "The quote channel no longer exists. Please set a new one using `[p]quoteset channel #channel`."
            )
            return
        if not isinstance(channel, discord.TextChannel):
            await ctx.send(
                "The configured quote channel is not a text channel. Please set a new one."
            )
            return

        perms = channel.permissions_for(ctx.guild.me)
        missing = []
        if not perms.send_messages:
            missing.append("Send Messages")
        if not perms.embed_links:
            missing.append("Embed Links")
        if missing:
            await ctx.send(
                f"I need the following permission(s) in {channel.mention}: {', '.join(missing)}."
            )
            return

        color = await ctx.embed_color()
        embed = discord.Embed(color=color)

        if user:
            if not text:
                await ctx.send("Please provide the quote text.")
                return
            embed.description = f'"{text}"'
            embed.set_author(name=user.display_name, icon_url=user.display_avatar)
        else:
            if not text:
                await ctx.send("Please provide the quote text.")
                return
            embed.description = f'"{text}"'
            embed.set_author(name="Anonymous")

        await channel.send(embed=embed)
        await ctx.tick()
