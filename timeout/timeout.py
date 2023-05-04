import contextlib
import datetime
from typing import List, Literal, Optional, Union

import discord
import humanize
from discord.utils import utcnow
from redbot.core import Config, commands, modlog
from redbot.core.bot import Red
from redbot.core.commands.converter import TimedeltaConverter

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Timeout(commands.Cog):
    """
    Manage Timeouts.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, identifier=190, force_registration=True)
        default_guild = {"dm": True, "showmod": False}
        self.config.register_guild(**default_guild)

    __author__ = ["sravan"]
    __version__ = "1.3.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    async def pre_load(self):
        with contextlib.suppress(RuntimeError):
            await modlog.register_casetype(
                name="timeout",
                default_setting=True,
                image=":mute:",
                case_str="Timeout",
            )
            await modlog.register_casetype(
                name="untimeout",
                default_setting=True,
                image=":sound:",
                case_str="Untimeout",
            )

    async def pre_load(self):
        with contextlib.suppress(RuntimeError):
            await modlog.register_casetype(
                name="timeout",
                default_setting=True,
                image=":mute:",
                case_str="Timeout",
            )
            await modlog.register_casetype(
                name="untimeout",
                default_setting=True,
                image=":sound:",
                case_str="Untimeout",
            )

    async def timeout_user(
        self,
        ctx: commands.Context,
        member: discord.Member,
        time: Optional[datetime.timedelta],
        reason: Optional[str] = None,
    ) -> None:
        await member.timeout(time, reason=reason)
        await modlog.create_case(
            bot=ctx.bot,
            guild=ctx.guild,
            created_at=utcnow(),
            action_type="timeout" if time else "untimeout",
            user=member,
            moderator=ctx.author,
            reason=reason,
            until=(utcnow() + time) if time else None,
            channel=ctx.channel,
        )
        if await self.config.guild(member.guild).dm():
            with contextlib.suppress(discord.HTTPException):
                embed = discord.Embed(
                    title="Server timeout" if time else "Server untimeout",
                    description=f"**Reason:** {reason}"
                    if reason
                    else "**Reason:** No reason given.",
                    timestamp=utcnow(),
                    colour=await ctx.embed_colour(),
                )

                if time:
                    timestamp = utcnow() + time
                    timestamp = int(datetime.datetime.timestamp(timestamp))
                    embed.add_field(
                        name="Until", value=f"<t:{timestamp}:f>", inline=True
                    )
                    embed.add_field(
                        name="Duration", value=humanize.naturaldelta(time), inline=True
                    )
                embed.add_field(name="Guild", value=ctx.guild, inline=False)
                if await self.config.guild(ctx.guild).showmod():
                    embed.add_field(name="Moderator", value=ctx.author, inline=False)
                await member.send(embed=embed)

    async def timeout_role(
        self,
        ctx: commands.Context,
        role: discord.Role,
        time: datetime.timedelta,
        reason: Optional[str] = None,
    ) -> List[discord.Member]:
        failed = []
        members = list(role.members)
        for member in members:
            try:
                await self.timeout_user(ctx, member, time, reason)
            except discord.HTTPException:
                failed.append(member)
        return failed

    @commands.command(aliases=["tt"])
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.admin_or_permissions(moderate_members=True)
    async def timeout(
        self,
        ctx: commands.Context,
        member_or_role: Union[discord.Member, discord.Role],
        time: TimedeltaConverter(
            minimum=datetime.timedelta(minutes=1),
            maximum=datetime.timedelta(days=28),
            default_unit="minutes",
            allowed_units=["minutes", "seconds", "hours", "days"],
        ) = None,
        *,
        reason: Optional[str] = None,
    ):
        """
        Timeout users.

        `<member_or_role>` is the username/rolename, ID or mention. If provided a role,
        everyone with that role will be timedout.
        `[time]` is the time to mute for. Time is any valid time length such as `45 minutes`
        or `3 days`. If nothing is provided the timeout will be 60 seconds default.
        `[reason]` is the reason for the timeout. Defaults to `None` if nothing is provided.

        Examples:
        `[p]timeout @member 5m talks too much`
        `[p]timeout @member 10m`

        """
        if not time:
            time = datetime.timedelta(seconds=60)
        timestamp = int(datetime.datetime.timestamp(utcnow() + time))
        if isinstance(member_or_role, discord.Member):
            if member_or_role.is_timed_out():
                return await ctx.send("This user is already timed out.")
            if not await is_allowed_by_hierarchy(ctx.bot, ctx.author, member_or_role):
                return await ctx.send("You cannot timeout this user due to hierarchy.")
            if ctx.channel.permissions_for(member_or_role).administrator:
                return await ctx.send("You can't timeout an administrator.")
            await self.timeout_user(ctx, member_or_role, time, reason)
            return await ctx.send(
                f"{member_or_role.mention} has been timed out till <t:{timestamp}:f>."
            )
        if isinstance(member_or_role, discord.Role):
            await ctx.send(
                f"Timeing out {len(member_or_role.members)} members till <t:{timestamp}:f>."
            )
            failed = await self.timeout_role(ctx, member_or_role, time, reason)
            return await ctx.send(f"Failed to timeout {len(failed)} members.")

    @commands.command(aliases=["utt"])
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.admin_or_permissions(moderate_members=True)
    async def untimeout(
        self,
        ctx: commands.Context,
        member_or_role: Union[discord.Member, discord.Role],
        *,
        reason: Optional[str] = None,
    ):
        """
        Untimeout users.

        `<member_or_role>` is the username/rolename, ID or mention. If
        provided a role, everyone with that role will be untimed.
        `[reason]` is the reason for the untimeout. Defaults to `None`
        if nothing is provided.

        """
        if isinstance(member_or_role, discord.Member):
            if not member_or_role.is_timed_out():
                return await ctx.send("This user is not timed out.")
            await self.timeout_user(ctx, member_or_role, None, reason)
            return await ctx.send(f"Removed timeout from {member_or_role.mention}")
        if isinstance(member_or_role, discord.Role):
            await ctx.send(
                f"Removing timeout from {len(member_or_role.members)} members."
            )
            members = list(member_or_role.members)
            for member in members:
                if member.is_timed_out():
                    await self.timeout_user(ctx, member, None, reason)
            return await ctx.send(f"Removed timeout from {len(members)} members.")

    @commands.group()
    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    async def timeoutset(self, ctx: commands.Context):
        """Manage timeout settings."""

    @timeoutset.command(name="showmoderator", aliases=["showmod"])
    async def timeoutset_showmoderator(self, ctx: commands.Context):
        """Change whether to show moderator on DM's or not."""
        current = await self.config.guild(ctx.guild).showmod()
        await self.config.guild(ctx.guild).showmod.set(not current)
        w = "Will not" if current else "Will"
        await ctx.send(f"I {w} show the moderator in timeout DM's.")

    @timeoutset.command(name="dm")
    async def timeoutset_dm(self, ctx: commands.Context):
        """Change whether to DM the user when they are timed out."""
        current = await self.config.guild(ctx.guild).dm()
        await self.config.guild(ctx.guild).dm.set(not current)
        w = "Will not" if current else "Will"
        await ctx.send(f"I {w} DM the user when they are timed out.")


# https://github.com/phenom4n4n/phen-cogs/blob/8727d6ee74b40709c7eb9300713dc22b88a17915/roleutils/utils.py#L34
async def is_allowed_by_hierarchy(
    bot: Red, user: discord.Member, member: discord.Member
) -> bool:
    return (
        user.guild.owner_id == user.id
        or user.top_role > member.top_role
        or await bot.is_owner(user)
    )
