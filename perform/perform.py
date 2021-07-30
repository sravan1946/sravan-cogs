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


class Perform(commands.Cog):
    """Perform different actions, like cuddle, poke etc."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=8423644625413)
        default_global = {
            "highfive": [
                "https://media1.tenor.com/images/0ae4995e4eb27e427454526c05b2e3dd/tenor.gif?itemid=12376992",
                "https://media1.tenor.com/images/7b1f06eac73c36721912edcaacddf666/tenor.gif?itemid=10559431",
                "https://media1.tenor.com/images/c3263b8196afc25ddc1d53a4224347cd/tenor.gif?itemid=9443275",
                "https://media1.tenor.com/images/56d6725009312574e4798c732cebc5fe/tenor.gif?itemid=12312526",
                "https://media1.tenor.com/images/e96d2396570a2fadd9c83e284a1ca675/tenor.gif?itemid=5390726",
                "https://media1.tenor.com/images/106c8e64e864230341b59cc892b5a980/tenor.gif?itemid=5682921",
                "https://media1.tenor.com/images/b714d7680f8b49d69b07bc2f1e052e72/tenor.gif?itemid=13400356",
                "https://media1.tenor.com/images/0c23b320822afd5b1ce3faf01c2b9b69/tenor.gif?itemid=14137078",
                "https://media1.tenor.com/images/e2f299d05a7b1832314ec7a331440d4e/tenor.gif?itemid=5374033",
                "https://media1.tenor.com/images/16267f3a34efb42598bd822effaccd11/tenor.gif?itemid=14137081",
                "https://media1.tenor.com/images/9730876547cb3939388cf79b8a641da9/tenor.gif?itemid=8073516",
                "https://media1.tenor.com/images/ce85a2843f52309b85515f56a0a49d06/tenor.gif?itemid=14137077",
            ],
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
            "facepalm":[
                "https://media1.tenor.com/images/bc3f3842afb1edcba095f9bf766405b2/tenor.gif?itemid=17778269",
                "https://media1.tenor.com/images/76d2ec47ec76fa36b2fce913331ba7e3/tenor.gif?itemid=5533025",
                "https://media1.tenor.com/images/be96db9b9acfd04fd2f5d890e2c51781/tenor.gif?itemid=14355381",
                "https://media1.tenor.com/images/5e29a1db9149211728b22bfd01f88771/tenor.gif?itemid=10336271",
                "https://media1.tenor.com/images/2e69f243490dedfdfc15c4a9aa52364c/tenor.gif?itemid=15580787",
                "https://media1.tenor.com/images/480cdeb59d3d5d50dd206283a944b8e1/tenor.gif?itemid=16327659",
                "https://media1.tenor.com/images/1aa0aa009ad5176e9bec54fe0e784323/tenor.gif?itemid=10405345",
                "https://media1.tenor.com/images/fce5aa9f4825a2adabfc9c91686167bc/tenor.gif?itemid=16842960",
                "https://media1.tenor.com/images/5b378a7894bc420954616a61eeb7f8c7/tenor.gif?itemid=21256762",
                "https://media1.tenor.com/images/04ce28c62c8cfeb102b3ac2a9bf28050/tenor.gif?itemid=12411417",
                "https://media1.tenor.com/images/2b8e5a43989d6fb81776267d1efba103/tenor.gif?itemid=21833649",
                "https://media1.tenor.com/images/5bbe44f124365864b1537f686d0a77f5/tenor.gif?itemid=20556956"            
            ],
            "kill":[
                "https://media1.tenor.com/images/55507aea306782b916659085fc062909/tenor.gif?itemid=8932977",
                "https://media1.tenor.com/images/2c945adbbc31699861f411f86ce8058f/tenor.gif?itemid=5459053",
                "https://media1.tenor.com/images/c3cbe5b795cd40c0b51d02711f6e3978/tenor.gif?itemid=17223062",
                "https://media1.tenor.com/images/28c19622e8d7362ccc140bb24e4089ec/tenor.gif?itemid=9363668",
                "https://media1.tenor.com/images/a80b2bf31635899ac0900ea6281a41f6/tenor.gif?itemid=5535365",
                "https://media1.tenor.com/images/15cd532af605deec12a680f7e6d17181/tenor.gif?itemid=13961185",
                "https://media1.tenor.com/images/e4db2e0888c2c85a042ea9e54fc4d771/tenor.gif?itemid=16079109",
                "https://media1.tenor.com/images/2706b52a7bf7b34cfe43d7f49381ee85/tenor.gif?itemid=13617665",
                "https://media1.tenor.com/images/b73f2fb18d2dcc2ea7fa0ac20830f91f/tenor.gif?itemid=11409825",
                "https://media1.tenor.com/images/9df97f1c83c532cc29ab8d9ec099acf5/tenor.gif?itemid=10616092"               
            ],
        }
        self.config.register_global(**default_global)


    __author__ = ["Onii-chan", "sravan"]
    __version__ = "3.0.0"

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
    @commands.command(name="highfive")
    @commands.bot_has_permissions(embed_links=True)
    async def highfive(self, ctx, user: discord.Member):
        """Highfives a user!"""

        author = ctx.message.author
        images = await self.config.highfive()

        mn = len(images)
        i = randint(0, mn - 1)

        em = discord.Embed(
            colour=discord.Colour.random(),
            description=f"**{ctx.author.mention}** highfives {f'**{str(user.mention)}**' if user else 'themselves'}!",
        )
        em.set_footer(
            text=f"Requested by: {str(ctx.author)}",
            icon_url=ctx.author.avatar_url,
        )
        em.set_image(url=images[i])
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
    @commands.command(name="facepalm")
    @commands.bot_has_permissions(embed_links=True)
    async def facepalm(self, ctx):
        """Do a facepalm!"""

        author = ctx.message.author
        images = await self.config.facepalm()

        mn = len(images)
        i = randint(0, mn - 1)
        
        em = discord.Embed(
            colour=discord.Colour.random(),
            description=f"**{ctx.author.mention}** is facepalming!",
        )
        em.set_footer(
            text=f"Requested by: {str(ctx.author)}",
            icon_url=ctx.author.avatar_url,
        )
        em.set_image(url=images[i])
        await ctx.reply(embed=em, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="kill")
    @commands.bot_has_permissions(embed_links=True)
    async def kill(self, ctx, user: discord.Member):
        """Kills a user!"""

        author = ctx.message.author
        images = await self.config.kill()

        mn = len(images)
        i = randint(0, mn - 1)

        em = discord.Embed(
            colour=discord.Colour.random(),
            description=f"**{ctx.author.mention}** kills {f'**{str(user.mention)}**' if user else 'themselves'}!",
        )
        em.set_footer(
            text=f"Requested by: {str(ctx.author)}",
            icon_url=ctx.author.avatar_url,
        )
        em.set_image(url=images[i])
        await ctx.reply(embed=em, mention_author=False)
