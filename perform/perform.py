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


from random import randint

import aiohttp
import discord
from redbot.core import Config, commands


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

async def nekosembed(self, ctx, user, action: str, endpoint: str):
    embed = discord.Embed(
        description=f"**{ctx.author.mention}** {action} {f'**{str(user.mention)}**' if user else 'themselves'}!",
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
            "https://nekos.life/api/v2/img/" + endpoint
        )
    )
    await ctx.reply(embed=embed, mention_author=False)

async def shiroembed(self, ctx, action: str, endpoint: str, user = None):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://shiro.gg/api/images/" + endpoint) as r:
            res = await r.json()
            if user is None:
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** " + action,
                )
            else: 
                em = discord.Embed(
                    colour=discord.Colour.random(),
                    description=f"**{ctx.author.mention}** {action} {f'**{str(user.mention)}**' if user else 'themselves'}!",
                )
            em.set_footer(
                text=f"Requested by: {str(ctx.author)}",
                icon_url=ctx.author.avatar_url,
            )
            em.set_image(url=res["url"])
            await ctx.reply(embed=em, mention_author=False)

async def kawaiiembed(self, ctx, action: str, endpoint: str, user = None):
        api_key = (await self.bot.get_shared_api_tokens("perform")).get("api_key")
        if not api_key:
            return await ctx.send("Set a API token before using this command. If you are the bot owner, then use `[p]performapi` to see how to add the API.")
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
        embed.set_author(
                name = self.bot.user.display_name,
                icon_url = self.bot.user.avatar_url
            )

        embed.set_image(
            url=await api_call2(
                "https://kawaii.red/api/gif/"+ endpoint + "/token=" + api_key
            )
        )
        await ctx.reply(embed=embed, mention_author=False)


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
            "spank": [
                "https://media1.tenor.com/images/ef5f040254c2fbf91232088b91fe2341/tenor.gif?itemid=13569259",
                "https://media1.tenor.com/images/fa2472b2cca1e4a407b7772b329eafb4/tenor.gif?itemid=21468457",
                "https://media1.tenor.com/images/2eb222b142f24be14ea2da5c84a92b08/tenor.gif?itemid=15905904",
                "https://media1.tenor.com/images/86b5a47d495c0e8c5c3a085641a91aa4/tenor.gif?itemid=15964704",
                "https://media1.tenor.com/images/31d58e53313dc9bbd6435d824d2a5933/tenor.gif?itemid=11756736",
                "https://media1.tenor.com/images/97624764cb41414ad2c60d2028c19394/tenor.gif?itemid=16739345",
                "https://media1.tenor.com/images/f21c5c56e36ce0dfcdfe7c7993578c46/tenor.gif?itemid=21371415",
                "https://media1.tenor.com/images/58f5dcc2123fc73e8fb6b76f149441bc/tenor.gif?itemid=12086277",
                "https://media1.tenor.com/images/eafb13b900645ddf3b30cf9cc28e9f91/tenor.gif?itemid=4603671",
                "https://media1.tenor.com/images/be2bb9db1c8b8dc2194ec6a1b3d96b89/tenor.gif?itemid=18811244",
                "https://media.giphy.com/media/OoCuLoM6iEhYk/giphy.gif",
                "https://media.giphy.com/media/Qo3qovmbqaKT6/giphy.gif"
            ],
        }
        self.config.register_global(**default_global)


    __author__ = ["Onii-chan", "sravan"]
    __version__ = "5.0.0" #idk what im doing with version

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def cuddle(self, ctx, user: discord.Member):
        """Cuddle a user!"""
        await nekosembed(self, ctx, user, "cuddled", "cuddle")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="poke")
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx, user: discord.Member):
        """Poke a user!"""
        await shiroembed(self, ctx, "poked", "poke", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="kiss")
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx, user: discord.Member):
        """Kiss a user!"""
        await shiroembed(self, ctx, "just kissed", "kiss", user)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="hug")
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx, user: discord.Member):
        """Hugs a user!"""
        await shiroembed(self, ctx, "just hugged", "hug", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="pat")
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx, user: discord.Member):
        """Pats a user!"""
        await shiroembed(self, ctx, "just patted", "pat", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="tickle")
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx, user: discord.Member):
        """Tickles a user!"""
        await shiroembed(self, ctx, "just tickled", "tickle", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="smug")
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx):
        """Be smug towards someone!"""
        await shiroembed(self, ctx, "is acting so smug!", "smug")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="lick")
    @commands.bot_has_permissions(embed_links=True)
    async def lick(self, ctx, user: discord.Member):
        """Licks a user!"""
        await shiroembed(seld, ctx, "just licked", "lick", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="slap")
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx, user: discord.Member):
        """Slaps a user!"""
        await shiroembed(self, ctx, "just slapped", "slap", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="cry")
    @commands.bot_has_permissions(embed_links=True)
    async def cry(self, ctx):
        """Start crying!"""
        await shiroembed(self, ctx, "is crying!", "cry")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="sleep")
    @commands.bot_has_permissions(embed_links=True)
    async def sleep(self, ctx):
        """Act sleepy!"""
        await shiroembed(self, ctx, "is sleepy!, sleep")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="spank")
    @commands.bot_has_permissions(embed_links=True)
    async def spank(self, ctx, user: discord.Member):
        """Spanks a user!"""

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
        await shiroembed(self, ctx, "is acting pout!", "pout")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="blush")
    @commands.bot_has_permissions(embed_links=True)
    async def blush(self, ctx):
        """Act blush!"""
        await shiroembed(self, ctx, "is blushing!", "blush")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="feed")
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx, user: discord.Member):
        """Feeds a user!"""

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
        await shiroembed(self, ctx, "just punched", "punch", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="confuse", aliases=["confused"])
    @commands.guild_only()
    async def confuse(self, ctx):
        """Act confused!"""
        await kawaiiembed(self, ctx, "is confused!", "confused")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="amazed", aliases=["amazing"])
    @commands.guild_only()
    async def amazed(self, ctx):
        """Act amazed!"""
        await kawaiiembed(self, ctx, "is amazed!", "amazing")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def highfive(self, ctx, user: discord.Member):
        """Highfive a user!"""
        await kawaiiembed(self, ctx, "highfived", "highfive", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="plead", aliases=["ask"])
    @commands.guild_only()
    async def plead(self, ctx, user: discord.Member):
        """Asks a user!"""
        await kawaiiembed(self, ctx, "is pleading", "ask", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="clap")
    @commands.guild_only()
    async def clap(self, ctx):
        """Clap for someone!"""
        await kawaiiembed(self, ctx, "is clapping!", "clap")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="facepalm")
    @commands.guild_only()
    async def faceplam(self, ctx):
        """Do a facepalm!"""
        await kawaiiembed(self, ctx, "is facepalming!", "facepalm")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="headdesk", aliases=["facedesk"])
    @commands.guild_only()
    async def faceplam(self, ctx):
        """Do a facedesk!"""
        await kawaiiembed(self, ctx, "is facedesking!", "facedesk")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def kill(self, ctx, user: discord.Member):
        """Kill a user!"""
        await kawaiiembed(self, ctx, "killed", "kill", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def love(self, ctx, user: discord.Member):
        """Love a user!"""
        await kawaiiembed(self, ctx, "loves", "love", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="hide")
    @commands.guild_only()
    async def hide(self, ctx):
        """Hide yourself!"""
        await kawaiiembed(self, ctx, "is hideing!", "hide")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="laugh")
    @commands.guild_only()
    async def laugh(self, ctx):
        """Start laughing!"""
        await kawaiiembed(self, ctx, "is laughing!", "laugh")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="peek", aliases=["lurk"])
    @commands.guild_only()
    async def lurk(self, ctx):
        """Start lurking!"""
        await kawaiiembed(self, ctx, "is lurking!", "peek")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def bite(self, ctx, user: discord.Member):
        """Bite a user!"""
        await kawaiiembed(self, ctx, "is biting", "bite", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="dance")
    @commands.guild_only()
    async def dance(self, ctx):
        """Start dancing!"""
        await kawaiiembed(self, ctx, "is dancing", "dance")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def yeet(self, ctx, user: discord.Member):
        """Yeet someone!"""
        await kawaiiembed(self, ctx, "yeeted", "yeet", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="dodge")
    @commands.guild_only()
    async def dodge(self, ctx):
        """Dodge something!"""
        await kawaiiembed(self, ctx, "is dodging!", "dodge")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="happy")
    @commands.guild_only()
    async def happy(self, ctx):
        """Act happy!"""
        await kawaiiembed(self, ctx, "is happy!", "happy")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="cute")
    @commands.guild_only()
    async def cute(self, ctx):
        """Act cute!"""
        await kawaiiembed(self, ctx, "is acting cute!", "facepalm")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="lonely", aliases=["alone"])
    @commands.guild_only()
    async def lonely(self, ctx):
        """Act lonely!"""
        await kawaiiembed(self, ctx, "is lonely!", "lonely")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="mad", aliases=["angry"])
    @commands.guild_only()
    async def mad(self, ctx):
        """Act angry!"""
        await kawaiiembed(self, ctx, "is angry!", "mad")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="nosebleed")
    @commands.guild_only()
    async def nosebleed(self, ctx):
        """Start bleeding from nose!"""
        await kawaiiembed(self, ctx, "'s nose is bleeding!", "nosebleed")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def protect(self, ctx, user: discord.Member):
        """Protech someone!"""
        await kawaiiembed(self, ctx, "is protecting!", "protect", user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="run")
    @commands.guild_only()
    async def run(self, ctx):
        """Start running!"""
        await kawaiiembed(self, ctx, "is running!", "run")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="scared")
    @commands.guild_only()
    async def scared(self, ctx):
        """Act scared!"""
        await kawaiiembed(self, ctx, "is scared!", "scared")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="shrug")
    @commands.guild_only()
    async def shrug(self, ctx):
        """Start shrugging!"""
        await kawaiiembed(self, ctx, "is shrugging!", "shrug")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="scream")
    @commands.guild_only()
    async def scream(self, ctx):
        """Start screaming!"""
        await kawaiiembed(self, ctx, "is screaming!", "scream")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="stare")
    @commands.guild_only()
    async def stare(self, ctx):
        """Stare someone!"""
        await kawaiiembed(self, ctx, "is stareing!", "stare")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=["welcome"])
    @commands.guild_only()
    async def wave(self, ctx, user: discord.Member):
        """Wave to someone!"""
        await kawaiiembed(self, ctx, "is waving", "wave", user)

    @commands.is_owner()
    @commands.command()
    async def performapi(self, ctx):
        """Steps to get the API token needed for few commands."""
        embed=discord.Embed(title="How to set API for perform cog", description="1. Go to https://kawaii.red/\n2. Login using your discord account\n3. Click on dashboard and copy your token\n4. Use `[p]set api perform api_key <token>`")
    #    embed.description(")
        await ctx.send(embed=embed)
