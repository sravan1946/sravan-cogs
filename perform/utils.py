from typing import Optional

import aiohttp
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from tabulate import tabulate


async def api_call(call_uri: str, returnObj: Optional[bool] = False):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{call_uri}") as response:
            response = await response.json()
            if returnObj is False:
                return response["response"]
            elif returnObj is True:
                return response
    await session.close()


async def check_perm(ctx: commands.Context):
    if isinstance(ctx.channel, discord.DMChannel):
        return False
    perm = ctx.channel.permissions_for(ctx.channel.guild.me).manage_webhooks
    return perm is True


async def send_embed(
    self,
    ctx: commands.Context,
    embed: discord.Embed,
    user: Optional[discord.Member] = None,
):
    if await check_perm(ctx) is True:
        try:
            if user:
                await print_it(self, ctx, embed, user)
            else:
                await print_it(self, ctx, embed)
        except discord.Forbidden:
            if user:
                await ctx.reply(embed=embed, content=user.mention, mention_author=False)
            else:
                await ctx.reply(embed=embed, mention_author=False)
    elif user:
        await ctx.reply(embed=embed, content=user.mention, mention_author=False)
    else:
        await ctx.reply(embed=embed, mention_author=False)


async def kawaiiembed(
    self, ctx: commands.Context, action: str, endpoint: str, user=None
) -> discord.Embed:
    api_key = (await self.bot.get_shared_api_tokens("perform")).get("api_key")
    if not api_key:
        return await ctx.send(
            "Set a API token before using this command. If you are the bot owner, then use `[p]performapi` to see how to add the API."
        )
    if user is None:
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** {action}",
            color=discord.Colour.random(),
        )
    else:
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** {action} {f'**{str(user.mention)}**' if user else 'themselves'}!",
            color=discord.Colour.random(),
        )
    embed.set_footer(
        text=f"Requested by {ctx.message.author.display_name}",
        icon_url=ctx.message.author.avatar_url,
    )
    embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
    try:
        url = await api_call(f"https://kawaii.red/api/gif/{endpoint}/token={api_key}")
    except aiohttp.client_exceptions.ContentTypeError:
        return "The API is currently down, please try again later."
    embed.set_image(url=url)

    return embed


# Thanks epic
async def get_hook(self, ctx: commands.Context):
    try:
        if ctx.channel.id not in self.cache:
            for i in await ctx.channel.webhooks():
                if i.user.id == self.bot.user.id:
                    hook = i
                    self.cache[ctx.channel.id] = hook
                    break
            else:
                hook = await ctx.channel.create_webhook(
                    name=f"red_bot_hook_{str(ctx.channel.id)}"
                )

        else:
            hook = self.cache[ctx.channel.id]
    except discord.NotFound:  # Probably user deleted the hook
        hook = await ctx.channel.create_webhook(
            name=f"red_bot_hook_{str(ctx.channel.id)}"
        )
    return hook


async def print_it(
    self,
    ctx: commands.Context,
    embed: discord.Embed,
    user: Optional[discord.User] = None,
    retried: bool = False,
):
    hook = await get_hook(self, ctx)
    try:
        if user:
            await hook.send(
                username=ctx.message.author.display_name,
                avatar_url=ctx.message.author.avatar_url,
                embed=embed,
                content=user.mention,
            )
        else:
            await hook.send(
                username=ctx.message.author.display_name,
                avatar_url=ctx.message.author.avatar_url,
                embed=embed,
            )
    except discord.NotFound:
        if retried:  # This is an edge case, just a hack to prevent infinite loops
            return await ctx.send("I can't find the webhook, sorry.")
        self.cache.pop(ctx.channel.id)
        await print_it(self, ctx, embed, retried=True)


async def rstats_embed(
    self,
    ctx: commands.Context,
    action: str,
    user: discord.User,
):
    custom = await self.config.custom("Target").all()
    em = discord.Embed(
        title=f"{user.name}'s {action} stats", color=await ctx.embed_color()
    )
    em.set_author(name=user, icon_url=user.avatar_url)
    em.set_footer(text=f"Requested by {ctx.author}")

    sent = {}
    for who, to_who_d in custom.items():
        for to_who, _ in to_who_d.items():
            if int(who) != user.id:
                continue
            if (
                custom.get(who)
                and custom[who].get(to_who)
                and custom[who][to_who].get(f"{action}_r")
            ):
                sent[to_who] = custom[who][to_who][f"{action}_r"]
    sent = sorted(sent.items(), key=lambda x: x[1], reverse=True)
    rsent = sum(v for _, v in sent)
    sent = [
        [self.bot.get_user(int(k)), v]
        if self.bot.get_user(int(k))
        else ["Deleted User", v]
        for k, v in sent[:10]
    ]
    sent = tabulate(sent, tablefmt="fancy", headers=["User", "Amount"])

    em.add_field(
        name=f"Sent {action}s: {rsent}",
        value=box(sent, lang="sml")
        if rsent != 0
        else f"You haven't sent any {action} yet.",
        inline=False,
    )

    received = {}
    for who, to_who_d in custom.items():
        for to_who, _ in to_who_d.items():
            if int(to_who) != user.id:
                continue
            if (
                custom.get(who)
                and custom[who].get(to_who)
                and custom[who][to_who].get(f"{action}_r")
            ):
                received[who] = custom[who][to_who][f"{action}_r"]
    received = sorted(received.items(), key=lambda x: x[1], reverse=True)
    rcount = sum(v for _, v in received)
    received = [
        [self.bot.get_user(int(k)), v]
        if self.bot.get_user(int(k))
        else ["Deleted User", v]
        for k, v in received[:10]
    ]
    received = tabulate(received, tablefmt="fancy", headers=["User", "Amount"])

    em.add_field(
        name=f"Received {action}s: {rcount}",
        value=box(received, lang="sml")
        if rcount != 0
        else f"You haven't received any {action} yet.",
        inline=False,
    )

    return em
