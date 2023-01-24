"""
Copyright 2021 Onii-chan.

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


import logging
from random import randint

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

from .utils import kawaiiembed, send_embed

log = logging.getLogger("red.onii.perform")


class Perform(commands.Cog):
    """
    Perform different actions, like cuddle, poke etc.
    """

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=8423644625413, force_registration=True
        )
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
                "https://media.giphy.com/media/Qo3qovmbqaKT6/giphy.gif",
            ],
            "nut": [
                "https://c.tenor.com/2U9tTXuO_gUAAAAC/kick-anime.gif",
                "https://c.tenor.com/uHQL8xtAwaUAAAAd/kick-in-the-balls-anime.gif",
                "https://c.tenor.com/D67kRWw_cEEAAAAC/voz-dap-chym-dap-chym.gif",
                "https://c.tenor.com/_mW88MVAnrYAAAAC/heion-sedai-no-idatentachi-paula.gif",
                "https://c.tenor.com/CZT8alpjzzwAAAAd/ball-kick.gif",
                "https://c.tenor.com/KlvWYCEumXAAAAAd/kick-anime.gif",
                "https://c.tenor.com/9x-loeWpLyoAAAAC/talho-eureka-seven.gif",
                "https://c.tenor.com/6qtGbz6_894AAAAC/kick.gif",
                "https://c.tenor.com/NpMUvPFLwCEAAAAC/ow-balls-kick.gif",
                "https://c.tenor.com/pbyIf8fSIJsAAAAC/kick-balls-kick-in-the-balls.gif",
            ],
        }
        default_member = {
            "cuddle_s": 0,
            "poke_s": 0,
            "kiss_s": 0,
            "hug_s": 0,
            "slap_s": 0,
            "pat_s": 0,
            "tickle_s": 0,
            "smug_s": 0,
            "lick_s": 0,
            "cry": 0,
            "sleep": 0,
            "spank_s": 0,
            "pout": 0,
            "blush": 0,
            "feed_s": 0,
            "punch_s": 0,
            "confused": 0,
            "amazed": 0,
            "highfive_s": 0,
            "plead_s": 0,
            "clap": 0,
            "facepalm": 0,
            "facedesk": 0,
            "kill_s": 0,
            "love_s": 0,
            "hide": 0,
            "laugh": 0,
            "lurk": 0,
            "bite_s": 0,
            "dance": 0,
            "yeet_s": 0,
            "dodge": 0,
            "happy": 0,
            "cute": 0,
            "lonely": 0,
            "mad": 0,
            "nosebleed": 0,
            "protect_s": 0,
            "run": 0,
            "scared": 0,
            "shrug": 0,
            "scream": 0,
            "stare": 0,
            "wave_s": 0,
            "nut_s": 0,
        }
        default_target = {
            "cuddle_r": 0,
            "poke_r": 0,
            "kiss_r": 0,
            "hug_r": 0,
            "slap_r": 0,
            "pat_r": 0,
            "tickle_r": 0,
            "smug_r": 0,
            "lick_r": 0,
            "spank_r": 0,
            "feed_r": 0,
            "punch_r": 0,
            "highfive_r": 0,
            "plead_r": 0,
            "kill_r": 0,
            "love_r": 0,
            "bite_r": 0,
            "yeet_r": 0,
            "protect_r": 0,
            "wave_r": 0,
            "nut_r": 0,
        }
        self.config.register_global(**default_global)
        self.config.register_user(**default_member)
        self.config.init_custom("Target", 2)
        self.config.register_custom("Target", **default_target)
        self.cache = {}

    __author__ = ["Onii-chan", "sravan"]
    __version__ = "5.6.6"  # idk what im doing with version

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    def cog_unload(self):
        global hug
        if hug:
            try:
                self.bot.remove_command("hug")
            except Exception as e:
                log.info(e)
            self.bot.add_command(hug)

    # @commands.command()
    # async def rstats(self, ctx, action: str):
    #     embed = discord.Embed()
    #     embed.set_author(name=f"{ctx.author.name}'s {action} statistics")
    #     embed.add_field(name=f"Sent {action}s", value=)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def cuddle(self, ctx: commands.Context, user: discord.Member):
        """
        Cuddle a user!
        """
        embed = await kawaiiembed(self, ctx, "cuddled", "cuddle", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).cuddle_r()
        used = await self.config.user(ctx.author).cuddle_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total cuddles: {used + 1} | {ctx.author.name} has cuddled {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).cuddle_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).cuddle_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="poke")
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx: commands.Context, user: discord.Member):
        """
        Poke a user!
        """
        embed = await kawaiiembed(self, ctx, "poked", "poke", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).poke_r()
        used = await self.config.user(ctx.author).poke_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total pokes: {used + 1} | {ctx.author.name} has poked {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).poke_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).poke_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="kiss")
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx: commands.Context, user: discord.Member):
        """
        Kiss a user!
        """
        embed = await kawaiiembed(self, ctx, "just kissed", "kiss", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).kiss_r()
        used = await self.config.user(ctx.author).kiss_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total kisses: {used + 1} | {ctx.author.name} has kissed {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).kiss_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).kiss_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="hug")
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx: commands.Context, user: discord.Member):
        """
        Hugs a user!
        """
        embed = await kawaiiembed(self, ctx, "just hugged", "hug", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).hug_r()
        used = await self.config.user(ctx.author).hug_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total hugs: {used + 1} | {ctx.author.name} has hugged {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).hug_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).hug_r.set(target + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="pat")
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx: commands.Context, user: discord.Member):
        """
        Pats a user!
        """
        embed = await kawaiiembed(self, ctx, "just patted", "pat", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).pat_r()
        used = await self.config.user(ctx.author).pat_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total pats: {used + 1} | {ctx.author.name} has patted {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).pat_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).pat_r.set(target + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="tickle")
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx: commands.Context, user: discord.Member):
        """
        Tickles a user!
        """
        embed = await kawaiiembed(self, ctx, "just tickled", "tickle", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).tickle_r()
        used = await self.config.user(ctx.author).tickle_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total tickles: {used + 1} | {ctx.author.name} has tickled {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).tickle_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).tickle_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="smug")
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx: commands.Context):
        """
        Be smug towards someone!
        """
        embed = await kawaiiembed(self, ctx, "is acting so smug!", "smug")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).smug_s()
        embed.set_footer(text=f"{ctx.author.name}'s total smugs: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).smug_s.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="lick")
    @commands.bot_has_permissions(embed_links=True)
    async def lick(self, ctx: commands.Context, user: discord.Member):
        """
        Licks a user!
        """
        embed = await kawaiiembed(self, ctx, "just licked", "lick", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).lick_r()
        used = await self.config.user(ctx.author).lick_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total licks: {used + 1} | {ctx.author.name} has licked {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).lick_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).lick_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="slap")
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx: commands.Context, user: discord.Member):
        """
        Slaps a user!
        """
        embed = await kawaiiembed(self, ctx, "just slapped", "slap", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).slap_r()
        used = await self.config.user(ctx.author).slap_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total slaps: {used + 1} | {ctx.author.name} has slapped {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).slap_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).slap_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="cry")
    @commands.bot_has_permissions(embed_links=True)
    async def cry(self, ctx: commands.Context):
        """
        Start crying!
        """
        embed = await kawaiiembed(self, ctx, "is crying!", "cry")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).cry()
        embed.set_footer(text=f"{ctx.author.name}'s total cries: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).cry.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="sleep")
    @commands.bot_has_permissions(embed_links=True)
    async def sleep(self, ctx: commands.Context):
        """
        Act sleepy!
        """
        embed = await kawaiiembed(self, ctx, "is sleepy!", "sleepy")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).sleep()
        embed.set_footer(text=f"{ctx.author.name}'s total sleeps: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).sleep.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="spank")
    @commands.bot_has_permissions(embed_links=True)
    async def spank(self, ctx: commands.Context, user: discord.Member):
        """
        Spanks a user!
        """

        images = await self.config.spank()

        mn = len(images)
        i = randint(0, mn - 1)

        embed = discord.Embed(
            colour=discord.Colour.random(),
            description=f"**{ctx.author.mention}** just spanked {f'**{str(user.mention)}**' if user else 'themselves'}!",
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url
        )
        embed.set_image(url=images[i])
        target = await self.config.custom("Target", ctx.author.id, user.id).spank_r()
        used = await self.config.user(ctx.author).spank_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total spanks: {used + 1} | {ctx.author.name} has spanked {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).spank_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).spank_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="pout")
    @commands.bot_has_permissions(embed_links=True)
    async def pout(self, ctx: commands.Context):
        """
        Act pout!
        """
        embed = await kawaiiembed(self, ctx, "is acting pout!", "pout")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).pout()
        embed.set_footer(text=f"{ctx.author.name}'s total pouts: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).pout.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="blush")
    @commands.bot_has_permissions(embed_links=True)
    async def blush(self, ctx: commands.Context):
        """
        Act blush!
        """
        embed = await kawaiiembed(self, ctx, "is blushing!", "blush")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).blush()
        embed.set_footer(text=f"{ctx.author.name}'s total blushes: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).blush.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="feed")
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx: commands.Context, user: discord.Member):
        """
        Feeds a user!
        """

        images = await self.config.feed()

        mn = len(images)
        i = randint(0, mn - 1)

        embed = discord.Embed(
            colour=discord.Colour.random(),
            description=f"**{ctx.author.mention}** feeds {f'**{str(user.mention)}**' if user else 'themselves'}!",
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url
        )
        embed.set_image(url=images[i])
        target = await self.config.custom("Target", ctx.author.id, user.id).feed_r()
        used = await self.config.user(ctx.author).feed_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total feeds: {used + 1} | {ctx.author.name} has feeded {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).feed_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).feed_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="punch")
    @commands.bot_has_permissions(embed_links=True)
    async def punch(self, ctx: commands.Context, user: discord.Member):
        """
        Punch a user!
        """
        embed = await kawaiiembed(self, ctx, "just punched", "punch", user)
        if embed is False:
            return await ctx.send("api is down")
        target = await self.config.custom("Target", ctx.author.id, user.id).punch_r()
        used = await self.config.user(ctx.author).punch_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total punches: {used + 1} | {ctx.author.name} has punched {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.custom("Target", ctx.author.id, user.id).punch_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="confuse", aliases=["confused"])
    @commands.guild_only()
    async def confuse(self, ctx: commands.Context):
        """
        Act confused!
        """
        embed = await kawaiiembed(self, ctx, "is confused!", "confused")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).confused()
        embed.set_footer(text=f"{ctx.author.name}'s total confusions: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).confused.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="amazed", aliases=["amazing"])
    @commands.guild_only()
    async def amazed(self, ctx: commands.Context):
        """
        Act amazed!
        """
        embed = await kawaiiembed(self, ctx, "is amazed!", "amazing")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).amazed()
        embed.set_footer(text=f"{ctx.author.name}'s total amazes: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).amazed.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def highfive(self, ctx: commands.Context, user: discord.Member):
        """
        Highfive a user!
        """
        embed = await kawaiiembed(self, ctx, "highfived", "highfive", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).highfive_r()
        used = await self.config.user(ctx.author).highfive_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total highfives: {used + 1} | {ctx.author.name} has highfived {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).highfive_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).highfive_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="plead", aliases=["ask"])
    @commands.guild_only()
    async def plead(self, ctx: commands.Context, user: discord.Member):
        """
        Asks a user!
        """
        embed = await kawaiiembed(self, ctx, "is pleading", "ask", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).plead_r()
        used = await self.config.user(ctx.author).plead_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total pleads: {used + 1} | {ctx.author.name} has pleaded {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).plead_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).plead_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="clap")
    @commands.guild_only()
    async def clap(self, ctx: commands.Context):
        """
        Clap for someone!
        """
        embed = await kawaiiembed(self, ctx, "is clapping!", "clap")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).clap()
        embed.set_footer(text=f"{ctx.author.name}'s total claps: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).clap.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="facepalm")
    @commands.guild_only()
    async def facepalm(self, ctx: commands.Context):
        """
        Do a facepalm!
        """
        embed = await kawaiiembed(self, ctx, "is facepalming!", "facepalm")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).facepalm()
        embed.set_footer(text=f"{ctx.author.name}'s total facepalms: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).facepalm.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="headdesk", aliases=["facedesk"])
    @commands.guild_only()
    async def facedesk(self, ctx: commands.Context):
        """
        Do a facedesk!
        """
        embed = await kawaiiembed(self, ctx, "is facedesking!", "facedesk")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).facedesk()
        embed.set_footer(text=f"{ctx.author.name}'s total facedesks: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).facedesk.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def kill(self, ctx: commands.Context, user: discord.Member):
        """
        Kill a user!
        """
        embed = await kawaiiembed(self, ctx, "killed", "kill", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).kill_r()
        used = await self.config.user(ctx.author).kill_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total kills: {used + 1} | {ctx.author.name} has killed {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).kill_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).kill_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def love(self, ctx: commands.Context, user: discord.Member):
        """
        Love a user!
        """
        embed = await kawaiiembed(self, ctx, "loves", "love", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).love_r()
        used = await self.config.user(ctx.author).love_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total loves: {used + 1} | {ctx.author.name} has loved {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).love_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).love_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="hide")
    @commands.guild_only()
    async def hide(self, ctx: commands.Context):
        """
        Hide yourself!
        """
        embed = await kawaiiembed(self, ctx, "is hiding!", "hide")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).hide()
        embed.set_footer(text=f"{ctx.author.name}'s total hides: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).hide.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="laugh")
    @commands.guild_only()
    async def laugh(self, ctx: commands.Context):
        """
        Start laughing!
        """
        embed = await kawaiiembed(self, ctx, "is laughing!", "laugh")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).laugh()
        embed.set_footer(text=f"{ctx.author.name}'s total laughs: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).laugh.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="peek", aliases=["lurk"])
    @commands.guild_only()
    async def lurk(self, ctx: commands.Context):
        """
        Start lurking!
        """
        embed = await kawaiiembed(self, ctx, "is lurking!", "peek")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).lurk()
        embed.set_footer(text=f"{ctx.author.name}'s total lurks: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).lurk.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def bite(self, ctx: commands.Context, user: discord.Member):
        """
        Bite a user!
        """
        embed = await kawaiiembed(self, ctx, "is biting", "bite", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).bite_r()
        used = await self.config.user(ctx.author).bite_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total bites: {used + 1} | {ctx.author.name} has bitten {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).bite_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).bite_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="dance")
    @commands.guild_only()
    async def dance(self, ctx: commands.Context):
        """
        Start dancing!
        """
        embed = await kawaiiembed(self, ctx, "is dancing", "dance")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).dance()
        embed.set_footer(text=f"{ctx.author.name}'s total dances: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).dance.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def yeet(self, ctx: commands.Context, user: discord.Member):
        """
        Yeet someone!
        """
        embed = await kawaiiembed(self, ctx, "yeeted", "yeet", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).yeet_r()
        used = await self.config.user(ctx.author).yeet_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total yeets: {used + 1} | {ctx.author.name} has yeeted {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).yeet_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).yeet_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="dodge")
    @commands.guild_only()
    async def dodge(self, ctx: commands.Context):
        """
        Dodge something!
        """
        embed = await kawaiiembed(self, ctx, "is dodging!", "dodge")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).dodge()
        embed.set_footer(text=f"{ctx.author.name}'s total dodges: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).dodge.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="happy")
    @commands.guild_only()
    async def happy(self, ctx: commands.Context):
        """
        Act happy!
        """
        embed = await kawaiiembed(self, ctx, "is happy!", "happy")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).happy()
        embed.set_footer(text=f"{ctx.author.name}'s total happiness: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).happy.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="cute")
    @commands.guild_only()
    async def cute(self, ctx: commands.Context):
        """
        Act cute!
        """
        embed = await kawaiiembed(self, ctx, "is acting cute!", "cute")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).cute()
        embed.set_footer(text=f"{ctx.author.name}'s total cuteness: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).cute.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="lonely", aliases=["alone"])
    @commands.guild_only()
    async def lonely(self, ctx: commands.Context):
        """
        Act lonely!
        """
        embed = await kawaiiembed(self, ctx, "is lonely!", "lonely")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).lonely()
        embed.set_footer(text=f"{ctx.author.name}'s total loneliness: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).lonely.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="mad", aliases=["angry"])
    @commands.guild_only()
    async def mad(self, ctx: commands.Context):
        """
        Act angry!
        """
        embed = await kawaiiembed(self, ctx, "is angry!", "mad")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).mad()
        embed.set_footer(text=f"{ctx.author.name}'s total angriness: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).mad.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="nosebleed")
    @commands.guild_only()
    async def nosebleed(self, ctx: commands.Context):
        """
        Start bleeding from nose!
        """
        embed = await kawaiiembed(self, ctx, "'s nose is bleeding!", "nosebleed")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).nosebleed()
        embed.set_footer(text=f"{ctx.author.name}'s total nosebleeds: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).nosebleed.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def protect(self, ctx: commands.Context, user: discord.Member):
        """
        Protech someone!
        """
        embed = await kawaiiembed(self, ctx, "is protecting!", "protect", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).protect_r()
        used = await self.config.user(ctx.author).protect_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total protects: {used + 1} | {ctx.author.name} has protected {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).protect_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).protect_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="run")
    @commands.guild_only()
    async def run(self, ctx: commands.Context):
        """
        Start running!
        """
        embed = await kawaiiembed(self, ctx, "is running!", "run")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).run()
        embed.set_footer(text=f"{ctx.author.name}'s total runs: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).run.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="scared")
    @commands.guild_only()
    async def scared(self, ctx: commands.Context):
        """
        Act scared!
        """
        embed = await kawaiiembed(self, ctx, "is scared!", "scared")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).scared()
        embed.set_footer(text=f"{ctx.author.name}'s total scares: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).scared.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="shrug")
    @commands.guild_only()
    async def shrug(self, ctx: commands.Context):
        """
        Start shrugging!
        """
        embed = await kawaiiembed(self, ctx, "is shrugging!", "shrug")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).shrug()
        embed.set_footer(text=f"{ctx.author.name}'s total shrugs: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).shrug.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="scream")
    @commands.guild_only()
    async def scream(self, ctx: commands.Context):
        """
        Start screaming!
        """
        embed = await kawaiiembed(self, ctx, "is screaming!", "scream")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).scream()
        embed.set_footer(text=f"{ctx.author.name}'s total screams: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).scream.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="stare")
    @commands.guild_only()
    async def stare(self, ctx: commands.Context):
        """
        Stare someone!
        """
        embed = await kawaiiembed(self, ctx, "is stareing!", "stare")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).stare()
        embed.set_footer(text=f"{ctx.author.name}'s total stares: {used + 1}")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).stare.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=["welcome"])
    @commands.guild_only()
    async def wave(self, ctx: commands.Context, user: discord.Member):
        """
        Wave to someone!
        """
        embed = await kawaiiembed(self, ctx, "is waving", "wave", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).wave_r()
        used = await self.config.user(ctx.author).wave_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total waves: {used + 1} | {ctx.author.name} has waved {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).wave_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).wave_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="nutkick", aliases=["kicknuts"])
    @commands.bot_has_permissions(embed_links=True)
    async def kicknuts(self, ctx: commands.Context, user: discord.Member):
        """
        Kick a user on the nuts!
        """

        images = await self.config.nut()

        mn = len(images)
        i = randint(0, mn - 1)

        embed = discord.Embed(
            colour=discord.Colour.random(),
            description=f"**{ctx.author.mention}** just kicked nuts of {f'**{str(user.mention)}**' if user else 'themselves'}!",
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url
        )
        embed.set_image(url=images[i])
        target = await self.config.custom("Target", ctx.author.id, user.id).nut_r()
        used = await self.config.user(ctx.author).nut_s()
        embed.set_footer(
            text=f"{ctx.author.name}'s total nutkicks: {used + 1} | {ctx.author.name} has nutkicked {user.name} {target + 1} times"
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).nut_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).nut_r.set(target + 1)

    @commands.is_owner()
    @commands.command()
    async def performapi(self, ctx: commands.Context):
        """
        Steps to get the API token needed for few commands.
        """
        embed = discord.Embed(
            title="How to set API for perform cog",
            description=(
                """
                1. Go to https://kawaii.red/\n
                2. Login using your discord account\n
                3. Click on dashboard and copy your token\n
                4. Use `[p]set api perform api_key <token>`,
            """
            ),
        )
        await ctx.send(embed=embed)


#     @commands.command()
#     @commands.guild_only()
#     async def rstats(self, ctx: commands.Context, action: str, member: discord.Member = None):
#         """RStats cog commands."""
#         valid = [
#             "cuddle",
#             "poke",
#             "kiss",
#             "hug",
#             "pat",
#             "tickle",
#             "smug",
#             "lick",
#             "slap",
#             "cry",
#             "sleep",
#             "spank",
#             "pout",
#             "blush",
#             "feed",
#             "punch",
#             "confuse",
#             "amazed",
#             "highfive",
#             "plead",
#             "clap",
#             "facepalm",
#             "headdesk",
#             "kill",
#             "love",
#             "hide",
#             "laugh",
#             "peek",
#             "bite",
#             "dance",
#             "yeet",
#             "dodge",
#             "happy",
#             "cute",
#             "lonely",
#             "mad",
#             "nosebleed",
#             "protect",
#             "run",
#             "scared",
#             "shrug",
#             "scream",
#             "stare",
#             "wave",
#             ]
#         if action.lower() not in valid:
#             return await ctx.send("Invalid action.")
#         if member is None:
#             member = ctx.author
#         data = await self.config.custom("Target").all()
#         top_10 = get_top10(data, member.id)
#         embed = discord.Embed(title=f"Top 10 for {member.name}")
#         top_10 = tabulate(top_10, tablefmt="psql", headers=["User", "Spanks"])
#         embed.description = box(top_10)
#         await ctx.send(embed=embed)


# def get_top10(data, action: str):
#     targets = []
#     for i in data:
#         for key, value in data[i].items():
#             with contextlib.suppress(KeyError):
#                 targets.append((value["spank_r"], key))
#         targets.sort(key=lambda x: x[0], reverse = True)
#     return targets[:10]


def setup(bot):
    global hug

    hug = bot.remove_command("hug")
    bot.add_cog(Perform(bot))
