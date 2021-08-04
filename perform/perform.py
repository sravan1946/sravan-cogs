"""
Copyright 2021 Onii-chan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import aiohttp
import discord
from redbot.core import commands, Config
from random import randint


async def api_call(call_uri, returnObj=False):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{call_uri}") as response:
            response = await response.json()
            if returnObj == False:
                return response["url"]
            elif returnObj == True:
                return response
    await session.close()

async def api_call2(call_uri, returnObj=False):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{call_uri}") as response:
            response = await response.json()
            if returnObj == False:
                return response["response"]
            elif returnObj == True:
                return response
    await session.close()



class Perform(commands.Cog):
    """Perform different actions, like cuddle, poke etc."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=8423644625413)
        default_global = {
            "feed": [
                "https://media1.tenor.com/images/93c4833dbcfd5be9401afbda220066ee/tenor.gif?itemid=11223742",
                "https://media1.tenor.com/images/33cfd292d4ef5e2dc533ff73a102c2e6/tenor.gif?itemid=12165913",
                "https://media1.tenor.com/images/72268391ffde3cd976a456ee2a033f46/tenor.gif?itemid=7589062",
                "https://media1.tenor.com/images/4b48975ec500f8326c5db6b178a91a3a/tenor.gif?itemid=12593977",
                "https://media1.tenor.com/images/187ff5bc3a5628b6906935232898c200/tenor.gif?itemid=9340097",
                "https://media1.tenor.com/images/15e7d9e1eb0aad2852fabda1210aee95/tenor.gif?itemid=12005286",
                "https://media1.tenor.com/images/d08d0825019c321f21293c35df8ed6a9/tenor.gif?itemid=9032297",
                "https://media1.tenor.com/images/571da4da1ad526afe744423f7581a452/tenor.gif?itemid=11658244",
                "https://media1.tenor.com/images/6bde17caa5743a22686e5f7b6e3e23b4/tenor.gif?itemid=13726430",
                "https://media1.tenor.com/images/fd3616d34ade61e1ac5cd0975c25a917/tenor.gif?itemid=13653906",
                "https://imgur.com/v7jsPrv",
            ],
            "spank":[
                "https://media1.tenor.com/images/ef5f040254c2fbf91232088b91fe2341/tenor.gif?itemid=13569259",
                "https://media1.tenor.com/images/d0f32f61c2964999b344c6846b30e1d6/tenor.gif?itemid=13665166",
                "https://media1.tenor.com/images/b51750728709353206263f0407f0be96/tenor.gif?itemid=16173937",
                "https://media1.tenor.com/images/1235505dc4abd822a7f540ad00e24a17/tenor.gif?itemid=15788982",
                "https://media1.tenor.com/images/996159e911ae816c153bfa523e18d7c4/tenor.gif?itemid=17299734",
                "https://media1.tenor.com/images/2eb222b142f24be14ea2da5c84a92b08/tenor.gif?itemid=15905904",
                "https://media1.tenor.com/images/c9b1fa86a103a3bf878ab1741d0bfdfe/tenor.gif?itemid=19349444",
                "https://media1.tenor.com/images/a7ed1e6575b047ae219c8bdef3cdb799/tenor.gif?itemid=16082139", 
                "https://media1.tenor.com/images/0d202a5b98b413a88a4611feae8cd855/tenor.gif?itemid=16910479f",
                "https://media1.tenor.com/images/5250cae3a499250ee32627109c4cec0b/tenor.gif?itemid=19431854",
                "https://media1.tenor.com/images/02e7e815066e728e721a44eb3e1118d3/tenor.gif?itemid=16055441",
                "https://media1.tenor.com/images/d7d63622652099676fd345d1ad0589b7/tenor.gif?itemid=18714058",
                "https://media1.tenor.com/images/051be15e85edb4cf90e639b986ad861d/tenor.gif?itemid=17314327",
                "https://media1.tenor.com/images/64a98f91d57957204c7e57b374912af0/tenor.gif?itemid=21371415",
                "https://media1.tenor.com/images/693afd5812160c00a1fa8582de15a83e/tenor.gif?itemid=5458569",
                "https://media1.tenor.com/images/86b5a47d495c0e8c5c3a085641a91aa4/tenor.gif?itemid=15964704",
                "https://media1.tenor.com/images/6f086e496d3e2650603caa21cc22046d/tenor.gif?itemid=18105116",
                "https://media1.tenor.com/images/4587f9a7c71519cb86fcdda746c434ed/tenor.gif?itemid=9583397",
                "https://media1.tenor.com/images/cbb47488c390edbddfe299d18d2909ae/tenor.gif?itemid=12178033"
            ],
        }
        self.config.register_global(**default_global)


    __author__ = ["Onii-chan", "sravan"]
    __version__ = "4.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def cuddle(self, ctx, user: discord.Member):
        """Cuddle a user!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** cuddled {f'**{str(user.mention)}**' if user else 'themselves'}!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call(
                "https://nekos.life/api/v2/img/cuddle"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="poke")
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx, user: discord.Member):
        """Poke a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/poke") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** poked {f'**{str(user.mention)}**' if user else 'themselves'}!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="kiss")
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx, user: discord.Member):
        """Kiss a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/kiss") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** just kissed {f'**{str(user.mention)}**' if user else 'themselves'}!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="hug")
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx, user: discord.Member):
        """Hugs a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/hug") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** just hugged {f'**{str(user.mention)}**' if user else 'themselves'}!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="pat")
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx, user: discord.Member):
        """Pats a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/pat") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** just patted {f'**{str(user.mention)}**' if user else 'themselves'}!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="tickle")
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx, user: discord.Member):
        """Tickles a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/tickle") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** just tickled {f'**{str(user.mention)}**' if user else 'themselves'}!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="smug")
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx):
        """Be smug towards someone!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/smug") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** is acting so smug!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="lick")
    @commands.bot_has_permissions(embed_links=True)
    async def lick(self, ctx, user: discord.Member):
        """Licks a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/lick") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** just licked {f'**{str(user.mention)}**' if user else 'themselves'}!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="slap")
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx, user: discord.Member):
        """Slaps a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/slap") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** just slapped {f'**{str(user.mention)}**' if user else 'themselves'}!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="cry")
    @commands.bot_has_permissions(embed_links=True)
    async def cry(self, ctx):
        """Start crying!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/cry") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** is crying!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="sleep")
    @commands.bot_has_permissions(embed_links=True)
    async def sleep(self, ctx):
        """Act sleepy!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/sleep") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** is sleepy!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="spank")
    @commands.bot_has_permissions(embed_links=True)
    async def spank(self, ctx, user: discord.Member):
        """Spanks a user!"""

        author = ctx.message.author
        images = await self.config.spank()

        mn = len(images)
        i = randint(0, mn - 1)

        em = discord.Embed(
            colour=discord.Colour.random(),
            description=f"**{ctx.author.mention}** just spanked {f'**{str(user.mention)}**' if user else 'themselves'}!",
        )
        em.set_footer(
            text=f"Requested by: {str(ctx.author)}",
            icon_url=ctx.author.avatar_url,
        )
        em.set_image(url=images[i])
        await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="pout")
    @commands.bot_has_permissions(embed_links=True)
    async def pout(self, ctx):
        """Act pout!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/pout") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** is acting pout!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="blush")
    @commands.bot_has_permissions(embed_links=True)
    async def blush(self, ctx):
        """Act blush!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/blush") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** is blushing!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="feed")
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx, user: discord.Member):
        """Feeds a user!"""

        author = ctx.message.author
        images = await self.config.feed()

        mn = len(images)
        i = randint(0, mn - 1)

        em = discord.Embed(
            colour=discord.Colour.random(),
            description=f"**{ctx.author.mention}** feeds {f'**{str(user.mention)}**' if user else 'themselves'}!",
        )
        em.set_footer(
            text=f"Requested by: {str(ctx.author)}",
            icon_url=ctx.author.avatar_url,
        )
        em.set_image(url=images[i])
        await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="punch")
    @commands.bot_has_permissions(embed_links=True)
    async def punch(self, ctx, user: discord.Member):
        """Punch a user!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://shiro.gg/api/images/punch") as r:
                res = await r.json()
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** just punched {f'**{str(user.mention)}**' if user else 'themselves'}!",
                )
                em.set_footer(
                    text=f"Requested by: {str(ctx.author)}",
                    icon_url=ctx.author.avatar_url,
                )
                em.set_image(url=res["url"])
                await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="confuse", aliases=["confused"])
    @commands.guild_only()
    async def confuse(self, ctx):
        """Act confused!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is confused!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/confused/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="amazed", aliases=["amazing"])
    @commands.guild_only()
    async def amazed(self, ctx):
        """Act amazed!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is amazed!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/amazing/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def highfive(self, ctx, user: discord.Member):
        """Highfive a user!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** highfived {f'**{str(user.mention)}**' if user else 'themselves'}!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/highfive/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="plead", aliases=["ask"])
    @commands.guild_only()
    async def plead(self, ctx, user: discord.Member):
        """Asks a user!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is begging {f'**{str(user.mention)}**' if user else 'themselves'}!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/ask/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="clap")
    @commands.guild_only()
    async def clap(self, ctx):
        """Clap for someone!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is clapping!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/clap/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="facepalm")
    @commands.guild_only()
    async def faceplam(self, ctx):
        """Do a facepalm!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is faceplaming!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/facepalm/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="headdesk", aliases=["facedesk"])
    @commands.guild_only()
    async def faceplam(self, ctx):
        """Do a facedesk!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is facedesking!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/facedesk/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def kill(self, ctx, user: discord.Member):
        """Kill a user!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** killed {f'**{str(user.mention)}**' if user else 'themselves'}!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/kill/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def love(self, ctx, user: discord.Member):
        """Love a user!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** loves {f'**{str(user.mention)}**' if user else 'themselves'}!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/love/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)


    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="hide")
    @commands.guild_only()
    async def hide(self, ctx):
        """Hide yourself!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is hiding!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/hide/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="laugh")
    @commands.guild_only()
    async def laugh(self, ctx):
        """Start laughing!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is laughing!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/laugh/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="peek", aliases=["lurk"])
    @commands.guild_only()
    async def lurk(self, ctx):
        """Start lurking!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is lurking!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/peek/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def bite(self, ctx, user: discord.Member):
        """Bite a user!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is biting {f'**{str(user.mention)}**' if user else 'themselves'}!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/bite/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="dance")
    @commands.guild_only()
    async def lurk(self, ctx):
        """Start dancing!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is dancing!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/dance/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def yeet(self, ctx, user: discord.Member):
        """Yeet someone!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** yeeted {f'**{str(user.mention)}**' if user else 'themselves'}!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/yeet/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="dodge")
    @commands.guild_only()
    async def dodge(self, ctx):
        """Dodge something!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is dodging!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/dodge/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="happy")
    @commands.guild_only()
    async def happy(self, ctx):
        """Act happy!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is happy!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/happy/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="cute")
    @commands.guild_only()
    async def cute(self, ctx):
        """Act cute!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is acting cute!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/cute/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="lonely", aliases=["alone"])
    @commands.guild_only()
    async def lonely(self, ctx):
        """Act lonely!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is lonely!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/lonely/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="mad", aliases=["angry"])
    @commands.guild_only()
    async def mad(self, ctx):
        """Act angry!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is angry!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/mad/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="nosebleed")
    @commands.guild_only()
    async def nosebleed(self, ctx):
        """Start bleeding from nose!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}**'s nose is bleeding!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/nosebleed/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def protect(self, ctx, user: discord.Member):
        """Protech someone!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is protecting {f'**{str(user.mention)}**' if user else 'themselves'}!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/protect/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="run")
    @commands.guild_only()
    async def run(self, ctx):
        """Start running!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is running!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/run/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="scared")
    @commands.guild_only()
    async def scared(self, ctx):
        """Act scared!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is scared!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/scared/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="shrug")
    @commands.guild_only()
    async def shrug(self, ctx):
        """Start shrugging!"""
        embed = discord.Embed(
            description=f"**{ctx.author.mention}** is shrugging!",
            color=discord.Colour.random(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.message.author.display_name}",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(
                name=self.bot.user.display_name,
                icon_url=self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/shrug/token=468386640155508737.m2glPraTYnRPNMdEzW8K"
            )
        )
        await ctx.reply(embed=embed, mention_author=False)
