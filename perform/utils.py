import aiohttp
import discord
from redbot.core import commands


async def api_call(call_uri, returnObj=False):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{call_uri}") as response:
            response = await response.json()
            if returnObj is False:
                return response["response"]
            elif returnObj is True:
                return response
    await session.close()


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
        url = await api_call(f"https://kawaii.red/api/{endpoint}/token={api_key}")
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
    user: discord.User = None,
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
