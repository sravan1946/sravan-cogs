import logging
from datetime import datetime, timedelta
from typing import Literal

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands.converter import TimedeltaConverter
from redbot.core.config import Config
from redbot.core.utils.chat_formatting import humanize_timedelta, humanize_list

from .converters import ChannelCategoryConverter

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

log = logging.getLogger("red.sravan.dps")


# thanks to epic for letting me annoy him with this
# and the code from flare's antispam cog
class DontPingStaff(commands.Cog):
    """
    Punish users for pinging staff.
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
            "scope": {"guild": True, "category": [], "channel": []},
            "ignored_channels": [],
            "ignored_roles": [],
            "ignored_users": [],
            "muted_role": None,
            "message": None,
            "action": None,
            "staff_role": [],
            "per": 30,
            "amount": 10,
            "add_roles": [],
            "remove_roles": [],
        }
        self.config.register_guild(**default_guild)
        self.cache = {}

    __author__ = ["sravan"]
    __version__ = "2.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return (
            f"{pre_processed}\n\n"
            f"`Cog Authors:` {humanize_list(self.__author__)}\n"
            f"`Cog Version:` {self.__version__}\n"
        )

    async def gen_cache(self):
        self.config_cache = await self.config.all_guilds()

    @commands.group()
    @commands.admin_or_permissions(administrator=True)
    async def dps(self, ctx: commands.Context) -> None:
        """
        Dont ping staff.
        """

    @dps.command()
    async def toggle(self, ctx: commands.Context) -> None:
        """
        Toggle the module.
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
        """
        Manage whitelist.
        """

    @whitelist.group()
    async def add(self, ctx: commands.Context) -> None:
        """
        Add users/roles/channels to the whitelist.
        """

    @add.command(name="user")
    async def whitelist_user(
        self, ctx: commands.Context, users: commands.Greedy[discord.User] = None
    ) -> None:
        """
        Add users to the whitelist.
        """
        if users is None:
            return await ctx.send("`Users` is a required argument.")

        async with self.config.guild(ctx.guild).ignored_users() as ignored_users:
            for user in users:
                if user.id not in ignored_users:
                    ignored_users.append(user.id)

        ids = len(list(users))

        return await ctx.send(
            f"Successfully added {ids} "
            f"{'user' if ids == 1 else 'users'} "
            f"to the whitelist."
        )

    @add.command(name="role")
    async def whitelist_role(
        self, ctx: commands.Context, roles: commands.Greedy[discord.Role] = None
    ) -> None:
        """
        Add roles to the whitelist.
        """
        if roles is None:
            return await ctx.send("`Roles` is a required argument.")

        async with self.config.guild(ctx.guild).ignored_roles() as ignored_roles:
            for role in roles:
                if role.id not in ignored_roles:
                    ignored_roles.append(role.id)

        ids = len(list(roles))

        return await ctx.send(
            f"Successfully added {ids} "
            f"{'role' if ids == 1 else 'roles'} "
            f"to the whitelist."
        )

    @add.command(name="channel")
    async def whitelist_channel(
        self,
        ctx: commands.Context,
        channels: commands.Greedy[discord.TextChannel] = None,
    ) -> None:
        """
        Add channels to the whitelist.
        """
        if channels is None:
            return await ctx.send("`Channels` is a required argument.")

        async with self.config.guild(ctx.guild).ignored_channels() as ignored_channels:
            for channel in channels:
                if channel.id not in ignored_channels:
                    ignored_channels.append(channel.id)

        ids = len(list(channels))

        return await ctx.send(
            f"Successfully added {ids} "
            f"{'channel' if ids == 1 else 'channels'} "
            f"to the whitelist."
        )

    @whitelist.group()
    async def remove(self, ctx: commands.Context) -> None:
        """
        Remove users/roles/channels from the whitelist.
        """

    @remove.command(name="user")
    async def whitelist_user_remove(
        self, ctx: commands.Context, users: commands.Greedy[discord.User] = None
    ) -> None:
        """
        Remove users from the whitelist.
        """
        if users is None:
            return await ctx.send("`Users` is a required argument.")

        async with self.config.guild(ctx.guild).ignored_users() as ignored_users:
            for user in users:
                if user.id in ignored_users:
                    ignored_users.remove(user.id)

        ids = len(list(users))

        return await ctx.send(
            f"Successfully removed {ids} "
            f"{'user' if ids == 1 else 'users'} "
            f"from the whitelist."
        )

    @remove.command(name="role")
    async def whitelist_role_remove(
        self, ctx: commands.Context, roles: commands.Greedy[discord.Role] = None
    ) -> None:
        """
        Remove roles from the whitelist.
        """
        if roles is None:
            return await ctx.send("`Roles` is a required argument.")

        async with self.config.guild(ctx.guild).ignored_roles() as ignored_roles:
            for role in roles:
                if role.id in ignored_roles:
                    ignored_roles.remove(role.id)

        ids = len(list(roles))

        return await ctx.send(
            f"Successfully removed {ids} "
            f"{'role' if ids == 1 else 'roles'} "
            f"from the whitelist."
        )

    @remove.command(name="channel")
    async def whitelist_channel_remove(
        self,
        ctx: commands.Context,
        channels: commands.Greedy[discord.TextChannel] = None,
    ) -> None:
        """
        Remove channels from the whitelist.
        """
        if channels is None:
            return await ctx.send("`Channels` is a required argument.")

        async with self.config.guild(ctx.guild).ignored_channels() as ignored_channels:
            for channel in channels:
                if channel.id in ignored_channels:
                    ignored_channels.remove(channel.id)

        ids = len(list(channels))

        return await ctx.send(
            f"Successfully removed {ids} "
            f"{'channel' if ids == 1 else 'channels'} "
            f"from the whitelist."
        )

    @dps.command(name="muterole")
    async def set_mute_role(self, ctx: commands.Context, role: discord.Role) -> None:
        """
        Set a role to be used for muting.
        """
        guild = ctx.guild
        role_id = role.id
        muted_role = await self.config.guild(guild).muted_role()
        if role_id == muted_role:
            await ctx.send("Role is already used for muting")
        else:
            await self.config.guild(guild).muted_role.set(role_id)
            await ctx.send("Role set for muting")

    @dps.group(name="addroles")
    async def add_roles(self, ctx: commands.Context) -> None:
        """
        Manage roles to be added to the user.
        """

    @add_roles.command(name="add")
    async def add_roles_add(self, ctx: commands.Context, role: discord.Role) -> None:
        """
        Add a role to be added to the user.
        """
        guild = ctx.guild
        role_id = role.id
        add_roles = await self.config.guild(guild).add_roles()
        if role_id in add_roles:
            await ctx.send("Role is already used for adding")
        else:
            async with self.config.guild(guild).add_roles() as add_roles:
                add_roles.append(role_id)
            await ctx.send("Role added for adding")

    @add_roles.command(name="remove")
    async def add_roles_remove(self, ctx: commands.Context, role: discord.Role) -> None:
        """
        Remove a role from being added to the user.
        """
        guild = ctx.guild
        role_id = role.id
        add_roles = await self.config.guild(guild).add_roles()
        if role_id not in add_roles:
            await ctx.send("Role is not used for adding")
        else:
            async with self.config.guild(guild).add_roles() as add_roles:
                add_roles.remove(role_id)
            await ctx.send("Role removed for adding")

    @add_roles.command(name="list")
    async def add_roles_list(self, ctx: commands.Context) -> None:
        """
        List the roles to be added to the user.
        """
        guild = ctx.guild
        add_roles = await self.config.guild(guild).add_roles()
        if not add_roles:
            await ctx.send("No roles set")
        else:
            await ctx.send(", ".join(str(f"<@&{role}>") for role in add_roles))

    @dps.group(name="removeroles")
    async def remove_roles(self, ctx: commands.Context) -> None:
        """
        Manage roles to be removed from the user.
        """

    @remove_roles.command(name="add")
    async def remove_roles_add(self, ctx: commands.Context, role: discord.Role) -> None:
        """
        Add a role to be removed from the user.
        """
        guild = ctx.guild
        role_id = role.id
        remove_roles = await self.config.guild(guild).remove_roles()
        if role_id in remove_roles:
            await ctx.send("Role is already used for removing")
        else:
            async with self.config.guild(guild).remove_roles() as remove_roles:
                remove_roles.append(role_id)
            await ctx.send("Role added for removing")

    @remove_roles.command(name="remove")
    async def remove_roles_remove(
        self, ctx: commands.Context, role: discord.Role
    ) -> None:
        """
        Remove a role from being removed from the user.
        """
        guild = ctx.guild
        role_id = role.id
        remove_roles = await self.config.guild(guild).remove_roles()
        if role_id not in remove_roles:
            await ctx.send("Role is not used for removing")
        else:
            async with self.config.guild(guild).remove_roles() as remove_roles:
                remove_roles.remove(role_id)
            await ctx.send("Role removed for removing")

    @remove_roles.command(name="list")
    async def remove_roles_list(self, ctx: commands.Context) -> None:
        """
        List the roles to be removed from the user.
        """
        guild = ctx.guild
        remove_roles = await self.config.guild(guild).remove_roles()
        if not remove_roles:
            await ctx.send("No roles set")
        else:
            await ctx.send(", ".join(str(f"<@&{role}>") for role in remove_roles))

    @dps.command(name="message")
    async def set_message(self, ctx: commands.Context, *, message: str) -> None:
        """
        Set the message to be sent to the user.
        """
        guild = ctx.guild
        message = message.replace("@", "@\u200b")
        if len(message) > 1000:
            return await ctx.send("Message is too long")
        await self.config.guild(guild).message.set(message)
        await ctx.send("Message set")

    @dps.command(name="action")
    async def set_action(
        self,
        ctx: commands.Context,
        *,
        action: str,
    ) -> None:
        """
        Choose none, kick, ban, mute, addroles, removeroles as the action.
        """
        guild = ctx.guild
        action = action.lower()
        if action not in ["kick", "ban", "mute", "addroles", "removeroles", "none"]:
            await ctx.send(
                "Invalid action. pick `none`, `kick`, `ban`, `mute`, `addroles` or `removeroles`"
            )
            return
        await self.config.guild(guild).action.set(action)
        await ctx.send(f"Action set to `{action}`")

    @dps.group(name="staffrole")
    async def staff_role(self, ctx: commands.Context) -> None:
        """
        Command for managing the staff role.
        """

    @staff_role.command(name="add")
    async def staff_role_add(self, ctx: commands.Context, role: discord.Role) -> None:
        """
        Add a role to the staff role.
        """
        guild = ctx.guild
        role_id = role.id
        staff_role = await self.config.guild(guild).staff_role()
        if role_id in staff_role:
            await ctx.send("Role is already used as a staff role")
        else:
            async with self.config.guild(guild).staff_role() as staff_role:
                staff_role.append(role_id)
            await ctx.send("Role added as staff role")

    @staff_role.command(name="remove")
    async def staff_role_remove(
        self, ctx: commands.Context, role: discord.Role
    ) -> None:
        """
        Remove a role from the staff role.
        """
        guild = ctx.guild
        role_id = role.id
        staff_role = await self.config.guild(guild).staff_role()
        if role_id not in staff_role:
            await ctx.send("Role is not used as a staff role")
        else:
            async with self.config.guild(guild).staff_role() as staff_role:
                staff_role.remove(role_id)
            await ctx.send("Role removed as staff role")

    @staff_role.command(name="list")
    async def staff_role_list(self, ctx: commands.Context) -> None:
        """
        List the staff roles.
        """
        guild = ctx.guild
        staff_role = await self.config.guild(guild).staff_role()
        if not staff_role:
            await ctx.send("No staff roles set")
        else:
            await ctx.send(", ".join(str(f"<@&{role}>") for role in staff_role))

    # TODO: the embed stuff is messed up.
    @dps.command(name="settings")
    @commands.bot_has_permissions(embed_links=True)
    async def settings(self, ctx: commands.Context) -> None:
        """
        Show the current settings.
        """
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
        scope = await self.config.guild(guild).scope()

        guild_scope: bool = scope["guild"]
        category_scope: list[int] = scope["category"]
        channel_scope: list[int] = scope["channel"]

        if guild_scope:
            scope_value = "Guild"
        else:
            scope_value = ""
            if category_scope:
                scope_value += ", ".join(
                    [str(guild.get_channel(cat).mention) for cat in category_scope])
            if channel_scope:
                if category_scope:  # Separation between categories and channels if categories are there
                    scope_value += ", "
                scope_value += ", ".join(
                    [str(guild.get_channel(chan).mention) for chan in channel_scope])

        embed = discord.Embed(
            title=f"{ctx.guild} Settings",
            description=f"**Scope:** {scope_value}",
            color=await ctx.embed_color(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(
            name="Enabled", value=str(await self.config.guild(guild).enabled())
        )
        embed.add_field(
            name="Staff Role",
            value=", ".join(str(f"<@&{role}>") for role in staff_role) if staff_role else "None"
        )
        embed.add_field(
            name="Muted Role", value=f"<@&{muted_role}>" if muted_role else "Not set"
        )

        embed.add_field(name="Action", value=action)
        embed.add_field(name="Amount", value=amount)
        embed.add_field(name="Per", value=per)

        embed.add_field(
            name="Ignored Users",
            value=(", ".join(str(f"<@!{user}>") for user in ignored_users) if ignored_users else "None")
        )
        embed.add_field(
            name="Ignored Roles",
            value=(", ".join(str(f"<@&{role}>") for role in ignored_roles) if ignored_roles else "None")
        )
        embed.add_field(
            name="Ignored Channels",
            value=(", ".join(str(f"<#{channel}>") for channel in ignored_channels) if ignored_channels else "None")
        )

        embed.add_field(name="Message", value=message, inline=False)

        await ctx.send(embed=embed)

    @dps.command(name="per")
    async def per(self, ctx: commands.Context, *, time: TimedeltaConverter) -> None:
        """
        Set how long to wait between actions.
        """
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
        """
        Set how many pings are needed to trigger an action.
        """
        guild = ctx.guild
        if amount < 1:
            return await ctx.send("Must be at least 1")
        await self.config.guild(guild).amount.set(amount)
        await ctx.send(f"I will need {amount} pings to trigger an action")
        await self.gen_cache()

    @dps.command(name="scope")
    @commands.admin_or_permissions(manage_guild=True)
    @commands.bot_has_permissions(embed_links=True)
    async def scope(
        self, ctx: commands.Context, *, scope: ChannelCategoryConverter
    ) -> None:
        """
        Set the scope of the module.

        **Scope**
        - `guild` - Enable DPS __**server-wide**__ by passing **guild**.
        - `category` - Enable DPS for a specific category by passing its **category ID**.
        - `channel` - Enable DPS for a specific channel by passing its **channel ID**.

        **Note**: You can specify multiple categories and channels, separated **by a space**. Running the command again will **override** the previous configuration.

        **Example**
        - To enable DPS for **specific channels**, **categories**, or a **mix of both**: `dps scope 123456789 123456789 123456789`
        """
        guild = ctx.guild
        await self.config.guild(guild).scope.set(scope)
        guild_scope: bool = scope["guild"]
        if guild_scope:
            await ctx.send("I will check all messages in the guild")
        else:
            cat_em = discord.Embed(title="Categories", color=await ctx.embed_color())
            chan_em = discord.Embed(title="Channels", color=await ctx.embed_color())
            category_scope: list[int] = scope["category"]
            cat_em.description = "\n".join(
                ctx.guild.get_channel(cat).mention for cat in category_scope
            )
            channel_scope: list[int] = scope["channel"]
            chan_em.description = "\n".join(
                ctx.guild.get_channel(chan).mention for chan in channel_scope
            )
            embeds = [cat_em, chan_em]
            await ctx.send(
                embeds=embeds,
                content="I will check messages in these categories and channels",
            )

    async def allowed_in_channel(self, message: discord.Message):
        scope: dict = await self.config.guild(message.guild).scope()
        if scope["guild"]:
            return True
        channels: list[int] = scope.get("channel", [])
        categories: list[int] = scope.get("category", [])
        channel = message.channel
        if channel.id in channels:
            return True
        if channel.category and channel.category.id in categories:
            return True

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        Checks for pings and acts accordingly.
        """
        guild = message.guild
        if not guild:
            return
        if message.author.bot:
            return
        if await self.config.guild(guild).enabled() is False:
            return
        if message.channel.id in await self.config.guild(guild).ignored_channels():
            return
        if message.author.id in await self.config.guild(guild).ignored_users():
            return
        if not await self.allowed_in_channel(message):
            return
        for roles in message.author.roles:
            if roles.id in await self.config.guild(guild).ignored_roles():
                return
        await self.check_ping(message)

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    # All of the cache stuff was taken from the antispam cog by flare.
    async def check_ping(self, message: discord.Message):
        """
        Check for pings in a message,to be used in the listener.
        """
        guild = message.guild
        author = message.author
        now = datetime.now()
        staff_role = await self.config.guild(guild).staff_role()
        mes = await self.config.guild(guild).message()
        action = await self.config.guild(guild).action()
        for member in message.mentions:
            if member.id == message.author.id:
                continue
            for role in member.roles:
                if role.id in staff_role:
                    if self.config_cache[guild.id]["amount"] == 1:
                        if action is None or action == "none":
                            if mes:
                                await message.reply(mes)
                            return
                        return await self.take_action(action, message)
                    if author.id not in self.cache:
                        self.cache[author.id] = {"count": 1, "time": now}
                        await message.reply(mes)
                    else:
                        if now - self.cache[author.id]["time"] > timedelta(
                            seconds=self.config_cache[guild.id]["per"]
                        ):
                            self.cache[author.id] = {"count": 1, "time": now}
                            await message.reply(mes)
                            return
                        self.cache[author.id]["count"] += 1
                        if (
                            self.cache[author.id]["count"]
                            < self.config_cache[guild.id]["amount"]
                        ):
                            await message.reply(mes)
                        else:
                            self.cache[author.id]["count"] = 0
                            if action is None:
                                return
                            await self.take_action(action, message)
                    break

    async def take_action(self, action: str, message: discord.Message):
        """
        Take action on a member.
        """
        if action == "mute":
            await self.mute(message)
        elif action == "kick":
            await self.kick(message)
        elif action == "ban":
            await self.ban(message)
        elif action == "addroles":
            await self.addrole(message)
        elif action == "removeroles":
            await self.removerole(message)

    async def mute(self, message: discord.Message):
        """
        Mute a member.
        """
        guild = message.guild
        muted_role = await self.config.guild(guild).muted_role()
        if muted_role is None:
            return await message.channel.send("No muted role set")
        try:
            await message.author.add_roles(guild.get_role(muted_role))
            await message.reply(f"{message.author.mention} has been muted")
        except discord.Forbidden:
            return await message.reply("I don't have permission to mute this user")

    async def kick(self, message: discord.Message):
        """
        Kick a member.
        """
        try:
            await message.author.kick(reason="Pinged too many times")
            await message.channel.send(f"{message.author.mention} has been kicked")
        except discord.Forbidden:
            return await message.reply("I don't have permission to kick this user")

    async def ban(self, message: discord.Message):
        """
        Ban a member.
        """
        try:
            await message.author.ban(reason="Pinged too much", delete_message_days=0)
            await message.channel.send(f"{message.author.mention} has been banned")
        except discord.Forbidden:
            return await message.reply("I don't have permission to ban this user")

    async def addrole(self, message: discord.Message):
        """
        Add a role to a member.
        """
        guild = message.guild
        roles: list[int] = await self.config.guild(guild).add_roles()
        if not roles:
            return await message.channel.send("No roles set")
        failed = 0
        for role in roles:
            try:
                await message.author.add_roles(guild.get_role(role))
            except discord.Forbidden:
                failed += 1
        if failed:
            await message.reply(
                f"{len(roles) - failed} roles have been added to {message.author.mention}, but I don't have permission to add {failed} roles to them"
            )
        else:
            await message.reply(
                f"{len(roles)} roles have been added to {message.author.mention}"
            )

    async def removerole(self, message: discord.Message):
        """
        Remove a role from a member.
        """
        guild = message.guild
        roles = await self.config.guild(guild).remove_roles()
        if not roles:
            return await message.channel.send("No roles set")
        failed = 0
        for role in roles:
            try:
                await message.author.remove_roles(guild.get_role(role))
            except discord.Forbidden:
                failed += 1
        if failed:
            await message.reply(
                f"{len(roles) - failed} roles have been removed from {message.author.mention}, but I don't have permission to remove {failed} roles from them"
            )
        else:
            await message.reply(
                f"{len(roles)} roles have been removed from {message.author.mention}"
            )
