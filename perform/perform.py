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
from typing import Optional

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

from .utils import add_footer, kawaiiembed, rstats_embed, send_embed

log = logging.getLogger("red.sravan.perform")


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
                "https://c.tenor.com/ElNeJpOxlbwAAAAd/cat-cute.gif",
                "https://c.tenor.com/bLYH7iHAwVMAAAAd/food-eat.gif",
                "https://c.tenor.com/pK1b4j6p48oAAAAd/feeding-viralhog.gif",
                "https://c.tenor.com/6ug-53SkT58AAAAd/peach-and-goma-peach-loves-goma.gif",
                "https://c.tenor.com/3NUf0oM6g6YAAAAd/couplegoals-peachmad.gif",
                "https://c.tenor.com/mRzd9so9oXYAAAAd/yaomei-kowloon.gif",
                "https://c.tenor.com/sydLlIaisUYAAAAj/tkthao219-bunny.gif",
                "https://media.tenor.com/V_hsuJ1Tfl8AAAAj/bubu-dudu-sseeyall.gif",
                "https://media.tenor.com/k4ErRWys-BYAAAAj/love-teddy.gif",
                "https://c.tenor.com/CHTk5L8ls8cAAAAd/eat-food.gif",
                "https://c.tenor.com/AvmJQd6xjLMAAAAd/kasumi-anime.gif",
                "https://c.tenor.com/chcVVr4RMDAAAAAd/sumi-rent-a-girlfriemd.gif",
                "https://c.tenor.com/DAIktxe14-sAAAAd/can-a-boy-girl-friendship-survive-danjo.gif",
                "https://c.tenor.com/W88fpJ7X9D4AAAAd/rotte-no-omocha-anime-girl-eating.gif",
                "https://c.tenor.com/G8SdAGQ7EtsAAAAd/anime-eating.gif",
                "https://c.tenor.com/NRCCvND3mWgAAAAd/dandidave-anime.gif",
                "https://c.tenor.com/lRhU7bsRgYYAAAAd/acchi-kocchi-eats.gif",
                "https://c.tenor.com/h5mRD9EQU6QAAAAd/anime-feeding.gif",
                "https://c.tenor.com/h2NRWgapCUEAAAAd/100-girlfriends-hakari-hanazono.gif",
            ],
            "spank": [
                "https://media4.giphy.com/media/pRotk2UQTsozm/giphy.gif",
                "https://media.giphy.com/media/jdrgQXu2qdL1e/giphy.gif",
                "https://media.giphy.com/media/lmr7ac1Gn4kmc/giphy.gif",
                "https://media.giphy.com/media/cl3EMK5vlECNO2UJr2/giphy.gif",
                "https://media.giphy.com/media/1gv7WwUYJlaRKWVtok/giphy.gif",
                "https://media.giphy.com/media/ToMjGpqqkBX9Q8NcPJu/giphy.gif",
                "https://media.giphy.com/media/VWIeyyUQNpFra/giphy.gif",
                "https://media.giphy.com/media/Qo3qovmbqaKT6/giphy.gif",
                "https://media.giphy.com/media/IEaRGHp4mskzBeAukn/giphy.gif",
                "https://media.giphy.com/media/3o7ZepRuhAHlQygTCg/giphy.gif",
                "https://media.giphy.com/media/XHijbgZQ8JVuTLydxn/giphy.gif",
                "https://media.giphy.com/media/EuhidVsRs4g5a/giphy.gif",
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
            "bully": [
                "https://c.tenor.com/1e120JMrQoYAAAAj/bubu-dudu-sseeyall.gif",
                "https://c.tenor.com/AgLRHh_JIPoAAAAd/bully-maguire-cry.gif",
                "https://c.tenor.com/kxmhnMXKaRkAAAAC/meanie-cat-cat-meanie.gif",
                "https://c.tenor.com/Yv3P2LUfeLsAAAAC/nelson-simpsons.gif",
                "https://c.tenor.com/T_dGBOUNVVMAAAAj/peach-goma-peach-and-goma.gif",
                "https://c.tenor.com/zAbPcvcMGGwAAAAd/bully-surprise.gif",
                "https://c.tenor.com/dRt_TK4slXAAAAAC/balls-293.gif",
                "https://c.tenor.com/nFHxwVUqNZYAAAAC/taiga-toradora.gif",
                "https://c.tenor.com/6sOSSkpI2OQAAAAd/pig-smack.gif",
                "https://c.tenor.com/HuIASYb4WO8AAAAi/peach-goma-peach-and-goma.gif",
            ],
            "footer": True,
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
            "fight_s": 0,
            "boop_s": 0,
            "wink_s": 0,
            "sip": 0,
            "stomp_s": 0,
            "puke": 0,
            "ask_s": 0,
            "baka_s": 0,
            "destroy_s": 0,
            "nom": 0,
            "salute_s": 0,
            "shoot_s": 0,
            "alarm": 0,
            "coffee": 0,
            "blyat": 0,
            "die": 0,
            "disappear": 0,
            "error": 0,
            "money": 0,
            "ok": 0,
            "party": 0,
            "purr_s": 0,
            "pusheen": 0,
            "shocked": 0,
            "shame": 0,
            "sit": 0,
            "sleepy": 0,
            "smoke": 0,
            "spin_s": 0,
            "triggered": 0,
            "uwu": 0,
            "wasted_s": 0,
            "wiggle": 0,
            "bully_s": 0,
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
            "fight_r": 0,
            "boop_r": 0,
            "wink_r": 0,
            "stomp_r": 0,
            "ask_r": 0,
            "baka_r": 0,
            "destroy_r": 0,
            "salute_r": 0,
            "shoot_r": 0,
            "purr_r": 0,
            "spin_r": 0,
            "wasted_r": 0,
            "bully_r": 0,
        }
        self.config.register_global(**default_global)
        self.config.register_user(**default_member)
        self.config.init_custom("Target", 2)
        self.config.register_custom("Target", **default_target)
        self.cache = {}

        self.COMMANDS = [i[:-2] for i in default_target if i.endswith("_r")]

    __author__ = ["Onii-chan", "sravan"]
    __version__ = "5.8.9"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

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
        await add_footer(
            self, ctx, embed, used, "cuddles", target=target, word2="cuddled", user=user
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
        await add_footer(
            self, ctx, embed, used, "pokes", target=target, word2="poked", user=user
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
        await add_footer(
            self, ctx, embed, used, "kisses", target=target, word2="kissed", user=user
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
        await add_footer(
            self, ctx, embed, used, "hugs", target=target, word2="hugged", user=user
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
        await add_footer(
            self, ctx, embed, used, "pats", target=target, word2="patted", user=user
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
        await add_footer(
            self, ctx, embed, used, "tickles", target=target, word2="tickled", user=user
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
        await add_footer(self, ctx, embed, used, "smugs")
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
        await add_footer(
            self, ctx, embed, used, "licks", target=target, word2="licked", user=user
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
        await add_footer(
            self, ctx, embed, used, "slaps", target=target, word2="slapped", user=user
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
        await add_footer(self, ctx, embed, used, "cries")
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
        await add_footer(self, ctx, embed, used, "sleeps")
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
            name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar
        )
        embed.set_image(url=images[i])
        target = await self.config.custom("Target", ctx.author.id, user.id).spank_r()
        used = await self.config.user(ctx.author).spank_s()
        await add_footer(
            self, ctx, embed, used, "spanks", target=target, word2="spanked", user=user
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
        await add_footer(self, ctx, embed, used, "pouts")
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
        await add_footer(self, ctx, embed, used, "blushes")
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
            name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar
        )
        embed.set_image(url=images[i])
        target = await self.config.custom("Target", ctx.author.id, user.id).feed_r()
        used = await self.config.user(ctx.author).feed_s()
        await add_footer(
            self, ctx, embed, used, "feeds", target=target, word2="fed", user=user
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
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).punch_r()
        used = await self.config.user(ctx.author).punch_s()
        await add_footer(
            self, ctx, embed, used, "punches", target=target, word2="punched", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).punch_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).punch_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="fight")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def fight(self, ctx: commands.Context, user: discord.Member):
        """
        Fight a user!
        """
        embed = await kawaiiembed(self, ctx, "just fought", "fight", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).fight_r()
        used = await self.config.user(ctx.author).fight_s()
        await add_footer(
            self, ctx, embed, used, "fights", target=target, word2="fought", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).fight_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).fight_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="boop")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def boop(self, ctx: commands.Context, user: discord.Member):
        """
        Boop a user!
        """
        embed = await kawaiiembed(self, ctx, "just booped", "boop", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).boop_r()
        used = await self.config.user(ctx.author).boop_s()
        await add_footer(
            self, ctx, embed, used, "boops", target=target, word2="booped", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).boop_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).boop_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="wink")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def wink(self, ctx: commands.Context, user: discord.Member):
        """
        Wink at a user!
        """
        embed = await kawaiiembed(self, ctx, "just winked", "wink", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).wink_r()
        used = await self.config.user(ctx.author).wink_s()
        await add_footer(
            self, ctx, embed, used, "winks", target=target, word2="winked", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).wink_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).wink_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="sip")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def sip(self, ctx: commands.Context):
        """
        Sip on a user!
        """
        embed = await kawaiiembed(self, ctx, "is sipping!", "sip")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).sip()
        await add_footer(self, ctx, embed, used, "sips")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).sip.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="stomp")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def stomp(self, ctx: commands.Context, user: discord.Member):
        """
        Stomp on a user!
        """
        embed = await kawaiiembed(self, ctx, "just stomped", "stomp", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).stomp_r()
        used = await self.config.user(ctx.author).stomp_s()
        await add_footer(
            self, ctx, embed, used, "stomps", target=target, word2="stomped", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).stomp_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).stomp_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="puke")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def puke(self, ctx: commands.Context):
        """
        Act puking!
        """
        embed = await kawaiiembed(self, ctx, "is puking!", "puke")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).puke()
        await add_footer(self, ctx, embed, used, "pukes")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).puke.set(used + 1)

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
        await add_footer(self, ctx, embed, used, "confuses")
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
        await add_footer(self, ctx, embed, used, "amazes")
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
        await add_footer(
            self,
            ctx,
            embed,
            used,
            "highfives",
            target=target,
            word2="highfived",
            user=user,
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).highfive_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).highfive_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="plead")
    @commands.guild_only()
    async def plead(self, ctx: commands.Context, user: discord.Member):
        """
        Plead to a user!
        """
        embed = await kawaiiembed(self, ctx, "is pleading", "ask", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).plead_r()
        used = await self.config.user(ctx.author).plead_s()
        await add_footer(
            self, ctx, embed, used, "pleads", target=target, word2="pleaded", user=user
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
        await add_footer(self, ctx, embed, used, "claps")
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
        await add_footer(self, ctx, embed, used, "facepalms")
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
        await add_footer(self, ctx, embed, used, "facedesks")
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
        await add_footer(
            self, ctx, embed, used, "kills", target=target, word2="killed", user=user
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
        await add_footer(
            self, ctx, embed, used, "loves", target=target, word2="loved", user=user
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
        await add_footer(self, ctx, embed, used, "hides")
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
        await add_footer(self, ctx, embed, used, "laughs")
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
        await add_footer(self, ctx, embed, used, "lurks")
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
        await add_footer(
            self, ctx, embed, used, "bites", target=target, word2="bit", user=user
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
        await add_footer(self, ctx, embed, used, "dances")
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
        await add_footer(
            self, ctx, embed, used, "yeets", target=target, word2="yeeted", user=user
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
        await add_footer(self, ctx, embed, used, "dodges")
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
        await add_footer(self, ctx, embed, used, "happiness")
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
        await add_footer(self, ctx, embed, used, "cuteness")
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
        await add_footer(self, ctx, embed, used, "loneliness")
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
        await add_footer(self, ctx, embed, used, "madness")
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
        await add_footer(self, ctx, embed, used, "nosebleeds")
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
        await add_footer(
            self,
            ctx,
            embed,
            used,
            "protects",
            target=target,
            word2="protected",
            user=user,
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
        await add_footer(self, ctx, embed, used, "runs")
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
        await add_footer(self, ctx, embed, used, "scaredness")
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
        await add_footer(self, ctx, embed, used, "shrugs")
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
        await add_footer(self, ctx, embed, used, "screams")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).scream.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="stare")
    @commands.guild_only()
    async def stare(self, ctx: commands.Context):
        """
        Stare someone!
        """
        embed = await kawaiiembed(self, ctx, "is staring!", "stare")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).stare()
        await add_footer(self, ctx, embed, used, "stares")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).stare.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
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
        await add_footer(
            self, ctx, embed, used, "waves", target=target, word2="waved", user=user
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
            name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar
        )
        embed.set_image(url=images[i])
        target = await self.config.custom("Target", ctx.author.id, user.id).nut_r()
        used = await self.config.user(ctx.author).nut_s()
        await add_footer(
            self,
            ctx,
            embed,
            used,
            "nutkicks",
            target=target,
            word2="nutkicked",
            user=user,
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).nut_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).nut_r.set(target + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="bully")
    @commands.bot_has_permissions(embed_links=True)
    async def bully(self, ctx: commands.Context, user: discord.Member):
        """
        Bully a user!
        """

        images = await self.config.bully()

        mn = len(images)
        i = randint(0, mn - 1)

        embed = discord.Embed(
            colour=discord.Colour.random(),
            description=f"**{ctx.author.mention}** bullied {f'**{str(user.mention)}**' if user else 'themselves'}!",
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar
        )
        embed.set_image(url=images[i])
        target = await self.config.custom("Target", ctx.author.id, user.id).bully_r()
        used = await self.config.user(ctx.author).bully_s()
        await add_footer(
            self,
            ctx,
            embed,
            used,
            "bullies",
            target=target,
            word2="bullied",
            user=user,
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).bully_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).bully_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="ask")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def ask(self, ctx: commands.Context, user: discord.Member):
        """
        Ask a user!
        """
        embed = await kawaiiembed(self, ctx, "just asked", "ask", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).ask_r()
        used = await self.config.user(ctx.author).ask_s()
        await add_footer(
            self, ctx, embed, used, "asks", target=target, word2="asked", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).ask_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).ask_r.set(target + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="baka")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def baka(self, ctx: commands.Context, user: discord.Member):
        """
        Call a user baka!
        """
        embed = await kawaiiembed(self, ctx, "just called baka", "baka", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).baka_r()
        used = await self.config.user(ctx.author).baka_s()
        await add_footer(
            self,
            ctx,
            embed,
            used,
            "bakas",
            target=target,
            word2="called baka",
            user=user,
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).baka_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).baka_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="destroy")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def destroy(self, ctx: commands.Context, user: discord.Member):
        """
        Destroy a user!
        """
        embed = await kawaiiembed(self, ctx, "just destroyed", "destroy", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).destroy_r()
        used = await self.config.user(ctx.author).destroy_s()
        await add_footer(
            self,
            ctx,
            embed,
            used,
            "destroys",
            target=target,
            word2="destroyed",
            user=user,
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).destroy_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).destroy_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="nom")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def nom(self, ctx: commands.Context):
        """
        Nom!
        """
        embed = await kawaiiembed(self, ctx, "is nomming!", "nom")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).nom()
        await add_footer(self, ctx, embed, used, "noms")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).nom.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="salute")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def salute(self, ctx: commands.Context, user: discord.Member):
        """
        Salute a user!
        """
        embed = await kawaiiembed(self, ctx, "just saluted", "salute", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).salute_r()
        used = await self.config.user(ctx.author).salute_s()
        await add_footer(
            self, ctx, embed, used, "salutes", target=target, word2="saluted", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).salute_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).salute_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="shoot")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def shoot(self, ctx: commands.Context, user: discord.Member):
        """
        Shoot a user!
        """
        embed = await kawaiiembed(self, ctx, "just shot", "shoot", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).shoot_r()
        used = await self.config.user(ctx.author).shoot_s()
        await add_footer(
            self, ctx, embed, used, "shoots", target=target, word2="shot", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).shoot_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).shoot_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="alarm")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def alarm(self, ctx: commands.Context):
        """
        Act alarm!
        """
        embed = await kawaiiembed(self, ctx, "is alarming!", "alarm")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).alarm()
        await add_footer(self, ctx, embed, used, "alarms")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).alarm.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="coffee")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def coffee(self, ctx: commands.Context):
        """
        Drink coffee!
        """
        embed = await kawaiiembed(self, ctx, "is drinking coffee!", "coffee")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).coffee()
        await add_footer(self, ctx, embed, used, "coffees")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).coffee.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="die")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def die(self, ctx: commands.Context):
        """
        Act die!
        """
        embed = await kawaiiembed(self, ctx, "just died!", "die")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).die()
        await add_footer(self, ctx, embed, used, "dies")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).die.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="disappear")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def disappear(self, ctx: commands.Context):
        """
        Act disappear!
        """
        embed = await kawaiiembed(self, ctx, "disappeared!", "disappear")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).disappear()
        await add_footer(self, ctx, embed, used, "disappears")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).disappear.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="error")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def error(self, ctx: commands.Context):
        """
        Act error!
        """
        embed = await kawaiiembed(self, ctx, "errored!", "error")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).error()
        await add_footer(self, ctx, embed, used, "errors")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).error.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="money")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def money(self, ctx: commands.Context):
        """
        Act money!
        """
        embed = await kawaiiembed(self, ctx, "is rich!", "money")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).money()
        await add_footer(self, ctx, embed, used, "moneys")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).money.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="ok")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def ok(self, ctx: commands.Context):
        """
        Act ok!
        """
        embed = await kawaiiembed(self, ctx, "said ok!", "ok")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).ok()
        await add_footer(self, ctx, embed, used, "oks")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).ok.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="party")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def party(self, ctx: commands.Context):
        """
        Act party!
        """
        embed = await kawaiiembed(self, ctx, "is partying!", "party")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).party()
        await add_footer(self, ctx, embed, used, "parties")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).party.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="purr")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def purr(self, ctx: commands.Context, user: discord.Member):
        """
        Purr a user!
        """
        embed = await kawaiiembed(self, ctx, "is purring!", "purr", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).purr_r()
        used = await self.config.user(ctx.author).purr_s()
        await add_footer(
            self, ctx, embed, used, "purrs", target=target, word2="purred", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).purr_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).purr_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="pusheen")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def pusheen(self, ctx: commands.Context):
        """
        Act pusheen!
        """
        embed = await kawaiiembed(self, ctx, "is pusheen!", "pusheen")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).pusheen()
        await add_footer(self, ctx, embed, used, "pusheens")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).pusheen.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="shocked")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def shocked(self, ctx: commands.Context):
        """
        Act shocked!
        """
        embed = await kawaiiembed(self, ctx, "is shocked!", "shocked")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).shocked()
        await add_footer(self, ctx, embed, used, "shocks")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).shocked.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="shame")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def shame(self, ctx: commands.Context):
        """
        Act shame!
        """
        embed = await kawaiiembed(self, ctx, "is ashamed!", "shame")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).shame()
        await add_footer(self, ctx, embed, used, "shames")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).shame.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="sleepy")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def sleepy(self, ctx: commands.Context):
        """
        Act sleepy!
        """
        embed = await kawaiiembed(self, ctx, "is sleepy!", "sleepy")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).sleepy()
        await add_footer(self, ctx, embed, used, "sleepies")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).sleepy.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="smoke")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def smoke(self, ctx: commands.Context):
        """
        Act smoke!
        """
        embed = await kawaiiembed(self, ctx, "is smoking!", "smoke")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).smoke()
        await add_footer(self, ctx, embed, used, "smokes")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).smoke.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="spin")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def spin(self, ctx: commands.Context, user: discord.Member):
        """
        Spin a user!
        """
        embed = await kawaiiembed(self, ctx, "is spinning!", "spin", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).spin_r()
        used = await self.config.user(ctx.author).spin_s()
        await add_footer(
            self, ctx, embed, used, "spins", target=target, word2="spinned", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).spin_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).spin_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="triggered")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def triggered(self, ctx: commands.Context):
        """
        Act triggered!
        """
        embed = await kawaiiembed(self, ctx, "is triggered!", "triggered")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).triggered()
        await add_footer(self, ctx, embed, used, "triggereds")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).triggered.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="uwu")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def uwu(self, ctx: commands.Context):
        """
        Act uwu!
        """
        embed = await kawaiiembed(self, ctx, "is uwuing!", "uwu")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).uwu()
        await add_footer(self, ctx, embed, used, "uwus")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).uwu.set(used + 1)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="wasted")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def wasted(self, ctx: commands.Context, user: discord.Member):
        """
        Wasted a user!
        """
        embed = await kawaiiembed(self, ctx, "wasted", "wasted", user)
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        target = await self.config.custom("Target", ctx.author.id, user.id).wasted_r()
        used = await self.config.user(ctx.author).wasted_s()
        await add_footer(
            self, ctx, embed, used, "wasteds", target=target, word2="wasted", user=user
        )
        await send_embed(self, ctx, embed, user)
        await self.config.user(ctx.author).wasted_s.set(used + 1)
        await self.config.custom("Target", ctx.author.id, user.id).wasted_r.set(
            target + 1
        )

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="wiggle")
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    async def wiggle(self, ctx: commands.Context):
        """
        Act wiggle!
        """
        embed = await kawaiiembed(self, ctx, "is wiggling!", "wiggle")
        if not isinstance(embed, discord.Embed):
            return await ctx.send(embed)
        used = await self.config.user(ctx.author).wiggle()
        await add_footer(self, ctx, embed, used, "wiggles")
        await send_embed(self, ctx, embed)
        await self.config.user(ctx.author).wiggle.set(used + 1)

    @commands.is_owner()
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
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

    @commands.command(aliases=["rstats", "pstats", "roleplaystats"])
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def performstats(
        self, ctx: commands.Context, action: str, user: Optional[discord.User]
    ):
        """View your roleplay stats"""
        if user is None:
            user = ctx.author
        if action not in self.COMMANDS:
            return await ctx.send(
                f"The valid choices to view stats for are {', '.join(f'`{c}`' for c in self.COMMANDS)}"
            )
        embed = await rstats_embed(self, ctx, action, user)
        await ctx.send(embed=embed)

    @commands.group(aliases=["pset", "rset", "roleplayset"])
    @commands.is_owner()
    async def performset(self, ctx: commands.Context):
        """Settings for roleplay stats"""

    @performset.command()
    async def footer(self, ctx: commands.Context):
        """Toggle showing footers for roleplay stats"""
        value = await self.config.footer()
        await self.config.footer.set(not value)
        if value:
            await ctx.send("Footers will no longer be shown")
        else:
            await ctx.send("Footers will now be shown")

    def cog_unload(self):
        global hug
        if hug:
            try:
                self.bot.remove_command("hug")
            except Exception as e:
                log.info(e)
            self.bot.add_command(hug)


async def setup(bot: Red):
    global hug
    hug = bot.remove_command("hug")
    await bot.add_cog(Perform(bot))
