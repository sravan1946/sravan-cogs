"""
MIT License

Copyright (c) 2020-2023 phenom4n4n
Copyright (c) 2023-present sravan1946

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# this is a modified version of Bobloy's forcemention cog
# this is also a fork of phenom4n4n's forcemention cog

import asyncio

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red


class ForceMention(commands.Cog):
    """
    Mention the unmentionables
    """

    __version__ = "1.1.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=634534234, force_registration=True
        )
        default_guild = {"editroles": False}
        self.config.register_guild(**default_guild)

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.bot_has_permissions(manage_roles=True)
    @commands.admin_or_permissions(mention_everyone=True)
    @commands.guild_only()
    @commands.command("forcemention")
    async def cmd_forcemention(
        self, ctx: commands.Context, role: discord.Role, *, message: str = None
    ):
        """
        Mentions that role, regardless if it's unmentionable.

        Will automatically delete the command invocation.
        """
        message = f"{role.mention}\n{message}" if message else role.mention
        try:
            await ctx.message.delete()
        except:
            pass
        await self.forcemention(ctx.channel, role, message)

    @commands.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.group("forcementionset")
    async def forcementionset(self, ctx: commands.Context):
        """
        Settings for forcemention
        """

    @forcementionset.command("editrole")
    async def forcementionset_editrole(self, ctx: commands.Context, toggle: bool):
        """
        Toggle whether forcemention can edit roles
        """
        if toggle:
            await ctx.send(
                "Are you sure you want to allow me to edit roles? This could potentially be dangerous as this will edit the role to `mentionable` for a split second. Type **`yes`** to confirm."
            )
            try:
                pred = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                    timeout=15,
                )
            except asyncio.TimeoutError:
                return await ctx.send("Confirmation timed out.")
            if pred.content.lower() != "yes":
                return await ctx.send("Confirmation failed.")
        await self.config.guild(ctx.guild).editroles.set(toggle)
        await ctx.send(f"Role editing set to {toggle}")

    async def forcemention(
        self, channel: discord.TextChannel, role: discord.Role, message: str, **kwargs
    ):
        mention_perms = discord.AllowedMentions(roles=[role])
        me = channel.guild.me
        if (
            not role.mentionable
            and not channel.permissions_for(me).mention_everyone
            and channel.permissions_for(me).manage_roles
            and me.top_role > role
        ):
            if await self.config.guild(channel.guild).editroles():
                await role.edit(mentionable=True)
                await channel.send(message, allowed_mentions=mention_perms, **kwargs)
                await role.edit(mentionable=False)
            else:
                prefix = (await self.bot.get_prefix(channel))[0]
                await channel.send(
                    f"{role.mention} is unmentionable or I don't have `mention_everyone` permission in {channel.mention}. \nYou can allow me to edit roles by running `{prefix}forcementionset editrole true` so that I can mention it without `mention_everyone` permission."
                )
        else:
            await channel.send(message, allowed_mentions=mention_perms, **kwargs)
