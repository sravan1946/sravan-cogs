import logging
from datetime import datetime, timedelta
from typing import Literal

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands.converter import TimedeltaConverter
from redbot.core.config import Config
from redbot.core.utils.chat_formatting import humanize_timedelta

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

log = logging.getLogger("red.sravan.dps")

# thanks to epic for letting me annoy him with this
# and the code from flare's antispam cog
class DontPingStaff(commands.Cog):
    """
    just dont!
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=32405723648956234756,
            force_registration=True,
        )
        default_guild = {
            "enabled": False,
            "ignored_channels": [],
            "ignored_roles": [],
            "ignored_users": [],
            "muted_role": None,
            "message": None,
            "action": None,
            "staff_role": [],
            "per": 30,
            "amount": 10,
        }
        self.config.register_guild(**default_guild)
        self.cache = {}

    async def gen_cache(self):
        self.config_cache = await self.config.all_guilds()

    @commands.group()
    @commands.admin_or_permissions(manage_guild=True)
    async def dps(self, ctx: commands.Context) -> None:
        """
        Dont ping staff
        """

    @dps.command()
    async def toggle(self, ctx: commands.Context) -> None:
        """
        Toggle the module
        """
        guild = ctx.guild
        enabled = await self.config.guild(guild).enabled()
        if enabled:
            await self.config.guild(guild).enabled.set(False)
            await ctx.send("Disabled")
        else:
            await self.config.guild(guild).enabled.set(True)
            await ctx.send("Enabled")

    @dps.group(aliases=["ignore"])
    async def whitelist(self, ctx: commands.Context) -> None:
        """manage whitelist"""

    @whitelist.group()
    async def add(self, ctx: commands.Context) -> None:
        """add users/roles/channels to the whitelist"""

    @add.command(name="user")
    async def whitelist_user(self, ctx: commands.Context, user: discord.User) -> None:
        """add a user to the whitelist"""
        guild = ctx.guild
        user_id = user.id
        ignored_users = await self.config.guild(guild).ignored_users()
        if user_id in ignored_users:
            await ctx.send("User is already whitelisted")
        else:
            async with self.config.guild(guild).ignored_users() as ignored_users:
                ignored_users.append(user_id)
            await ctx.send("User added to whitelist")

    @add.command(name="role")
    async def whitelist_role(self, ctx: commands.Context, role: discord.Role) -> None:
        """add a role to the whitelist"""
        guild = ctx.guild
        role_id = role.id
        ignored_roles = await self.config.guild(guild).ignored_roles()
        if role_id in ignored_roles:
            await ctx.send("Role is already whitelisted")
        else:
            async with self.config.guild(guild).ignored_roles() as ignored_roles:
                ignored_roles.append(role_id)
            await ctx.send("Role added to whitelist")

    @add.command(name="channel")
    async def whitelist_channel(
        self, ctx: commands.Context, channel: discord.TextChannel
    ) -> None:
        """add a channel to the whitelist"""
        guild = ctx.guild
        channel_id = channel.id
        ignored_channels = await self.config.guild(guild).ignored_channels()
        if channel_id in ignored_channels:
            await ctx.send("Channel is already whitelisted")
        else:
            async with self.config.guild(guild).ignored_channels() as ignored_channels:
                ignored_channels.append(channel_id)
            await ctx.send("Channel added to whitelist")

    @whitelist.group()
    async def remove(self, ctx: commands.Context) -> None:
        """remove users/roles/channels from the whitelist"""

    @remove.command(name="user")
    async def whitelist_user_remove(
        self, ctx: commands.Context, user: discord.User
    ) -> None:
        """remove a user from the whitelist"""
        guild = ctx.guild
        user_id = user.id
        ignored_users = await self.config.guild(guild).ignored_users()
        if user_id not in ignored_users:
            await ctx.send("User is not whitelisted")
        else:
            async with self.config.guild(guild).ignored_users() as ignored_users:
                ignored_users.remove(user_id)
            await ctx.send("User removed from whitelist")

    @remove.command(name="role")
    async def whitelist_role_remove(
        self, ctx: commands.Context, role: discord.Role
    ) -> None:
        """remove a role from the whitelist"""
        guild = ctx.guild
        role_id = role.id
        ignored_roles = await self.config.guild(guild).ignored_roles()
        if role_id not in ignored_roles:
            await ctx.send("Role is not whitelisted")
        else:
            async with self.config.guild(guild).ignored_roles() as ignored_roles:
                ignored_roles.remove(role_id)
            await ctx.send("Role removed from whitelist")

    @remove.command(name="channel")
    async def whitelist_channel_remove(
        self, ctx: commands.Context, channel: discord.TextChannel
    ) -> None:
        """remove a channel from the whitelist"""
        guild = ctx.guild
        channel_id = channel.id
        ignored_channels = await self.config.guild(guild).ignored_channels()
        if channel_id not in ignored_channels:
            await ctx.send("Channel is not whitelisted")
        else:
            async with self.config.guild(guild).ignored_channels() as ignored_channels:
                ignored_channels.remove(channel_id)
            await ctx.send("Channel removed from whitelist")

    @dps.command(name="muterole")
    async def set_mute_role(self, ctx: commands.Context, role: discord.Role) -> None:
        """set a role to be used for muting"""
        guild = ctx.guild
        role_id = role.id
        muted_role = await self.config.guild(guild).muted_role()
        if role_id == muted_role:
            await ctx.send("Role is already used for muting")
        else:
            await self.config.guild(guild).muted_role.set(role_id)
            await ctx.send("Role set for muting")

    @dps.command(name="message")
    async def set_message(self, ctx: commands.Context, *, message: str) -> None:
        """set the message to be sent to the user"""
        guild = ctx.guild
        message = message.replace("@", "@\u200b")
        await self.config.guild(guild).message.set(message)
        await ctx.send("Message set")

    @dps.command(name="action")
    async def set_action(self, ctx: commands.Context, *, action: str) -> None:
        """choose nothing, kick, ban or mute as the action"""
        guild = ctx.guild
        action = action.lower()
        if action not in ["kick", "ban", "mute", "none"]:
            await ctx.send("Invalid action. pick `none`, `kick`, `ban` or `mute`")
            return
        await self.config.guild(guild).action.set(action)
        await ctx.send("Action set to `{}`".format(action))

    @dps.group(name="staffrole")
    async def staff_role(self, ctx: commands.Context) -> None:
        """command for manageing the staff role"""

    @staff_role.command(name="add")
    async def staff_role_add(self, ctx: commands.Context, role: discord.Role) -> None:
        """add a role to the staff role"""
        guild = ctx.guild
        role_id = role.id
        staff_role = await self.config.guild(guild).staff_role()
        if role_id == staff_role:
            await ctx.send("Role is already used as a staff role")
        else:
            async with self.config.guild(guild).staff_role() as staff_role:
                staff_role.append(role_id)
            await ctx.send("Role added as staff role")

    @staff_role.command(name="remove")
    async def staff_role_remove(
        self, ctx: commands.Context, role: discord.Role
    ) -> None:
        """remove a role from the staff role"""
        guild = ctx.guild
        role_id = role.id
        staff_role = await self.config.guild(guild).staff_role()
        if role_id not in staff_role:
            await ctx.send("Role is not used as a staff role")
        else:
            async with self.config.guild(guild).staff_role() as staff_role:
                staff_role.remove(role_id)
            await ctx.send("Role removed as staff role")

    # TODO: the embed stuff is messed up.
    @dps.command(name="settings")
    async def settings(self, ctx: commands.Context) -> None:
        """show the current settings"""
        guild = ctx.guild
        await self.gen_cache()
        muted_role = await self.config.guild(guild).muted_role()
        ignored_users = await self.config.guild(guild).ignored_users()
        ignored_roles = await self.config.guild(guild).ignored_roles()
        ignored_channels = await self.config.guild(guild).ignored_channels()
        staff_role = await self.config.guild(guild).staff_role()
        per = await self.config.guild(guild).per()
        amount = await self.config.guild(guild).amount()
        action = await self.config.guild(guild).action() or "Not set"
        message = await self.config.guild(guild).message() or "Not set"
        embed = discord.Embed(title="Settings")
        embed.add_field(
            name="Muted Role", value=f"<@&{muted_role}>" if muted_role else "Not set"
        )
        embed.add_field(
            name="Ignored Users",
            value=", ".join(str(f"<@!{user}>") for user in ignored_users),
        ) if ignored_users else "None"
        embed.add_field(
            name="Ignored Roles",
            value=", ".join(str(f"<@&{role}>") for role in ignored_roles),
        ) if ignored_roles else "None"
        embed.add_field(
            name="Ignored Channels",
            value=", ".join(str(f"<#{channel}>") for channel in ignored_channels),
        ) if ignored_channels else "None"
        embed.add_field(
            name="Staff Role",
            value=", ".join(str(f"<@&{role}>") for role in staff_role),
        ) if staff_role else "None"
        embed.add_field(name="Action", value=action)
        embed.add_field(name="Message", value=message)
        embed.add_field(name="Per", value=per)
        embed.add_field(name="Amount", value=amount)
        embed.add_field(
            name="enabled", value=str(await self.config.guild(guild).enabled())
        )
        await ctx.send(embed=embed)

    @dps.command(name="per")
    async def per(self, ctx: commands.Context, *, time: TimedeltaConverter) -> None:
        """set how long to wait between actions"""
        guild = ctx.guild
        if not time:
            return await ctx.send("Invalid time")
        seconds = time.total_seconds()
        await self.config.guild(guild).per.set(seconds)
        await ctx.send(
            f"I will wait {humanize_timedelta(seconds=seconds).rstrip('s')} between actions"
        )
        await self.gen_cache()

    @dps.command(name="amount")
    async def amount(self, ctx: commands.Context, amount: int) -> None:
        """set how many pings are needed to trigger an action"""
        guild = ctx.guild
        if amount < 1:
            return await ctx.send("Must be at least 1")
        await self.config.guild(guild).amount.set(amount)
        await ctx.send(f"I will need {amount} pings to trigger an action")
        await self.gen_cache()

    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context) -> None:
        """checks for pings and acts accordingly"""
        guild = ctx.guild
        if not guild:
            return
        if ctx.author.bot:
            return
        if ctx.channel.id in await self.config.guild(guild).ignored_channels():
            return
        if ctx.author.id in await self.config.guild(guild).ignored_users():
            return
        for roles in ctx.author.roles:
            if roles.id in await self.config.guild(guild).ignored_roles():
                return
        if await self.config.guild(guild).enabled() is False:
            return
        await self.check_ping(ctx)

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    # All of the cache stuff was taken from the antispam cog by flare.
    # TODO: bot doesnt send the mes after the first ping after a load/reload.
    async def check_ping(self, ctx: commands.Context):
        """check for pings in a message. to be used in the listener"""
        guild = ctx.guild
        author = ctx.author
        now = datetime.now()
        staff_role = await self.config.guild(guild).staff_role()
        mes = await self.config.guild(guild).message()
        action = await self.config.guild(guild).action()
        for mentions in ctx.mentions:
            pings = [mentions.id]
            for ping in pings:
                member = guild.get_member(int(ping))
                if member.id == ctx.author.id:
                    return
                for role in member.roles:
                    if role.id in staff_role:
                        if author.id not in self.cache:
                            self.cache[author.id] = {"count": 1, "time": now}
                            await ctx.reply(mes)
                        else:
                            if now - self.cache[author.id]["time"] > timedelta(
                                seconds=self.config_cache[guild.id]["per"]
                            ):
                                self.cache[author.id] = {"count": 1, "time": now}
                                await ctx.reply(mes)
                                return
                            self.cache[author.id]["count"] += 1
                            if (
                                self.cache[author.id]["count"]
                                < self.config_cache[guild.id]["amount"]
                            ):
                                await ctx.reply(mes)
                            else:
                                self.cache[author.id]["count"] = 0
                                if action is None:
                                    return
                                elif action == "mute":
                                    await self.mute(ctx)
                                elif action == "kick":
                                    await self.kick(ctx)
                                elif action == "ban":
                                    await self.ban(ctx)
                        break
            break

    async def mute(self, ctx):
        """mute a member"""
        guild = ctx.guild
        muted_role = await self.config.guild(guild).muted_role()
        if muted_role is None:
            return await ctx.message.send("No muted role set")
        try:
            await ctx.author.add_roles(guild.get_role(muted_role))
            await ctx.reply(f"{ctx.author.mention} has been muted")
        except discord.Forbidden:
            return await ctx.reply("I don't have permission to mute this user")

    async def kick(self, ctx):
        """kick a member"""
        try:
            await ctx.message.author.kick()
            await ctx.reply(f"{ctx.message.author.mention} has been kicked")
        except discord.Forbidden:
            return await ctx.reply("I don't have permission to kick this user")

    async def ban(self, ctx):
        """ban a member"""
        try:
            await ctx.message.author.ban()
            await ctx.reply(f"{ctx.message.author.mention} has been banned")
        except discord.Forbidden:
            return await ctx.reply("I don't have permission to ban this user")
