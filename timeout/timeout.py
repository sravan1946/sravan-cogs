import datetime
from typing import Literal

import discord
from discord.http import Route
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands.converter import TimedeltaConverter
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Timeout(commands.Cog):
    """
    manage cooldowns
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=202342309123,
            force_registration=True,
        )

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    async def timeout_user(self, ctx, member, time, reason: str = None):
        r = Route(
            "PATCH",
            "/guilds/{guild_id}/members/{user_id}",
            guild_id=ctx.guild.id,
            user_id=member.id,
        )
        payload = {
            "communication_disabled_until": str(datetime.datetime.utcnow() + time)
            if time
            else None
        }

        await ctx.bot.http.request(r, json=payload, reason=reason)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.mod_or_permissions(administrator=True)
    async def timeout(
        self,
        ctx,
        member: discord.Member,
        time: TimedeltaConverter(
            minimum=datetime.timedelta(minutes=1),
            maximum=datetime.timedelta(days=28),
            default_unit="minutes",
            allowed_units=["minutes", "seconds", "hours", "days"],
        ) = None,
        *,
        reason: str = None,
    ):
        if not time:
            time = datetime.timedelta(seconds=60)
        check = await is_allowed_by_hierarchy(ctx.bot, ctx.author, member)
        if not check:
            return await ctx.send("You cannot timeout this user due to hierarchy.")
        if member.permissions_in(ctx.channel).administrator:
            return await ctx.send("You can't timeout an administrator.")
        await self.timeout_user(ctx, member, time, reason)
        timestamp = datetime.datetime.utcnow() + time
        timestamp = int(datetime.datetime.timestamp(timestamp))
        await ctx.send(f"{member.mention} has been timed out till <t:{timestamp}:f>.")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.mod_or_permissions(administrator=True)
    async def untimeout(
        self,
        ctx,
        member: discord.Member,
        *,
        reason: str = None,
    ):
        await self.timeout_user(ctx, member, None, reason)
        await ctx.send(f"Removed timeout from {member.mention}")


# https://github.com/phenom4n4n/phen-cogs/blob/8727d6ee74b40709c7eb9300713dc22b88a17915/roleutils/utils.py#L34
async def is_allowed_by_hierarchy(
    bot: Red, user: discord.Member, member: discord.Member
) -> bool:
    return (
        user.guild.owner_id == user.id
        or user.top_role > member.top_role
        or await bot.is_owner(user)
    )
