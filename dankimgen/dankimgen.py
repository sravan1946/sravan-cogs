import random
import urllib.parse
from io import BytesIO
from typing import Literal, Optional, Union

import aiohttp
import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

from .converter import ImageFinder

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


async def tokencheck(ctx: commands.Context) -> bool:
    token = await ctx.bot.get_shared_api_tokens("imgen")
    if token.get("token") is None:
        await ctx.send("The Imgen API token has not been set.")
        return False
    return True


# thanks to flare for the base dankmemer cog
class DankImgen(commands.Cog):
    """
    DankImgen commands for Red.
    """

    __version__ = "1.0.0"
    __author__ = ["sravan", "flare"]

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=29384723,
            force_registration=True,
        )
        self.api = "https://imgen.red/api/"
        self.session = aiohttp.ClientSession()
        self.header = {}

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    async def cog_unload(self):
        await self.session.close()

    async def initalize(self):
        token = await self.bot.get_shared_api_tokens("imgen")
        self.header = {"Authorization": token.get("token", "")}

    @commands.Cog.listener()
    async def on_red_api_tokens_update(self, service_name, api_tokens):
        if service_name == "imgen":
            self.header = {"Authorization": api_tokens.get("token")}

    def parse_text(self, text: str) -> str:
        return urllib.parse.quote(text)

    async def get(
        self, ctx: commands.Context, endpoint: str, json=False
    ) -> Union[dict, BytesIO]:
        async with ctx.typing():
            async with self.session.get(
                self.api + endpoint, headers=self.header
            ) as resp:
                if resp.status == 200:
                    if json:
                        return await resp.json()
                    file = BytesIO(await resp.read())
                    file.seek(0)
                    return file
                if resp.status == 404:
                    return {"error": "That endpoint does not exist"}
                try:
                    return await resp.json()
                except aiohttp.ContentTypeError:
                    return {"error": "Server did not return an image"}

    async def send_img(
        self, ctx: commands.Context, image: BytesIO, format="png"
    ) -> None:
        if not ctx.channel.permissions_for(ctx.me).send_messages:
            return
        if not ctx.channel.permissions_for(ctx.me).attach_files:
            await ctx.send("I need the Attach Files permission to send images.")
            return
        if format == "mp4":
            filename = "video.mp4"
        elif format == "gif":
            filename = "video.gif"
        else:
            filename = "image.png"
        try:
            await ctx.send(file=discord.File(image, filename=filename))
        except discord.HTTPException:
            await ctx.send("That image is too large to send.")
        except aiohttp.ClientOSError:
            await ctx.send("An error occurred while sending the image.")

    async def send_error(self, ctx: commands.Context, data: dict):
        if "error" in data:
            await ctx.send(data)
            await ctx.send(f"Oh no! An error occurred: `{data['error']}`")
        else:
            await ctx.send("An error occurred while processing the image.")

    @commands.is_owner()
    @commands.command()
    async def imgenapi(self, ctx: commands.Context):
        msg = (
            "# Instructions\n"
            "1. Go to [imgen.red](https://imgen.red)\n"
            "2. Click on the `Dashboard` button and login with your Discord account\n"
            "3. Request an API token\n"
            "4. Use the token to set the API token with `[p]set api imgen token <token>`"
        )
        await ctx.maybe_send_embed(msg)

    # -------------------- Text commands --------------------
    @commands.check(tokencheck)
    @commands.command()
    async def abandon(self, ctx: commands.Context, *, text: str):
        """Abandoning your son?"""
        text = self.parse_text(text)
        data = await self.get(ctx, f"abandon?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def armor(self, ctx: commands.Context, *, text: str):
        """Nothing gets through this armour."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"armor?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def balloon(self, ctx: commands.Context, *, text: str):
        """Pop a balloon.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"balloon?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def boo(self, ctx: commands.Context, *, text: str):
        """Boo!
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"boo?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def brain(self, ctx: commands.Context, *, text: str):
        """Big brain time.
        Text must be seperated by 3 commas."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"brain?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def chad(self, ctx: commands.Context, *, text: str):
        """Chad moment."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"chad?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def changemymind(self, ctx: commands.Context, *, text: str):
        """Change my mind?"""
        text = self.parse_text(text)
        data = await self.get(ctx, f"changemymind?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def cheating(self, ctx: commands.Context, *, text: str):
        """Cheating?
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"cheating?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def citation(self, ctx: commands.Context, *, text: str):
        """Citation needed.
        Text must be separated by 2 commas."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"citation?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def confusedcat(self, ctx: commands.Context, *, text: str):
        """Confused cat.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"confusedcat?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def crab(self, ctx: commands.Context, *, text: str):
        """Crab rave.
        Text must be separated by a `|`."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"crab?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "mp4")

    @commands.check(tokencheck)
    @commands.command()
    async def cry(self, ctx: commands.Context, *, text: str):
        """Drink my tears."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"cry?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def discordav(self, ctx: commands.Context):
        """Discord avatar."""
        data = await self.get(ctx, f"discordav")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def discordavalt(self, ctx: commands.Context):
        """Discord avatar alt.
        Text must be separated by a comma."""
        data = await self.get(ctx, f"discordavalt")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def doglemon(self, ctx: commands.Context, *, text: str):
        """Dog lemon.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"doglemon?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def emergencymeeting(self, ctx: commands.Context, *, text: str):
        """Emergency meeting."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"emergencymeeting?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def excuseme(self, ctx: commands.Context, *, text: str):
        """Excuse me?"""
        text = self.parse_text(text)
        data = await self.get(ctx, f"excuseme?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def expanddong(self, ctx: commands.Context, *, text: str):
        """Expand dong."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"expanddong?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def facts(self, ctx: commands.Context, *, text: str):
        """Open the facts book.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"facts?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def floor(self, ctx: commands.Context, *, text: str):
        """Floor gang."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"floor?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def kowalski(self, ctx: commands.Context, *, text: str):
        """Kowalski."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"kowalski?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def letmein(self, ctx: commands.Context, *, text: str):
        """LET ME IN."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"letmein?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "mp4")

    @commands.check(tokencheck)
    @commands.command()
    async def master(self, ctx: commands.Context, *, text: str):
        """Yes master.
        Text must be separated by 2 commas"""
        text = self.parse_text(text)
        data = await self.get(ctx, f"master?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def note(self, ctx: commands.Context, *, text: str):
        """Please take a note."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"note?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def nothing(self, ctx: commands.Context, *, text: str):
        """Nothing to see here."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"nothing?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def ohno(self, ctx: commands.Context, *, text: str):
        """Oh no, it's stupid."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"ohno?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # @commands.check(tokencheck)
    # @commands.command()
    # async def oldzerodays(self, ctx: commands.Context, *, text: str):
    #     """Old zero days."""
    #     text = self.parse_text(text)
    #     data = await self.get(ctx, f"oldzerodays?text={text}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def piccolo(self, ctx: commands.Context, *, text: str):
        """Piccolo."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"piccolo?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def plan(self, ctx: commands.Context, *, text: str):
        """Gru makes a plan.
        Text must be separated by 2 comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"plan?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def presentation(self, ctx: commands.Context, *, text: str):
        """Lisa makes a presentation."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"presentation?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def savehumanity(self, ctx: commands.Context, *, text: str):
        """The secret to save humanity."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"savehumanity?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def shit(self, ctx: commands.Context, *, text: str):
        """I stepped in crap."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"shit?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def sword(self, ctx: commands.Context, *, text: str):
        """Sword."""
        text = self.parse_text(text)
        data = await self.get(
            ctx, f"sword?text={text}&username1={ctx.author.display_name}"
        )
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def fuck(self, ctx: commands.Context, *, text: str):
        """Feck.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"fuck?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def humansgood(self, ctx: commands.Context, *, text: str):
        """Humans are wonderful things."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"humansgood?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def inator(self, ctx: commands.Context, *, text: str):
        """Xinator."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"inator?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def justpretending(self, ctx: commands.Context, *, text: str):
        """Just pretending.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"justpretending?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def knowyourlocation(self, ctx: commands.Context, *, text: str):
        """Know your location.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"knowyourlocation?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def lick(self, ctx: commands.Context, *, text: str):
        """Lick.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"lick?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def slapsroof(self, ctx: commands.Context, *, text: str):
        """This bad boy can fit so much in it."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"slapsroof?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def sneakyfox(self, ctx: commands.Context, *, text: str):
        """Sneaky fox.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"sneakyfox?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def stickynote(self, ctx: commands.Context, *, text: str):
        """Put up a sticky note."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"stickynote?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def stroke(self, ctx: commands.Context, *, text: str):
        """How to recognize a stroke."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"stroke?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def surprised(self, ctx: commands.Context, *, text: str):
        """Surprised Pikachu.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"surprised?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def thesearch(self, ctx: commands.Context, *, text: str):
        """The search for intelligent life."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"thesearch?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def violence(self, ctx: commands.Context, *, text: str):
        """Violence is never the answer."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"violence?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def violentsparks(self, ctx: commands.Context, *, text: str):
        """Violent sparks.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"violentsparks?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def vr(self, ctx: commands.Context, *, text: str):
        """VR is so realistic.
        Text must be separated by a comma."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"vr?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def walking(self, ctx: commands.Context, *, text: str):
        """Walking meme."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"walking?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def zerodays(self, ctx: commands.Context, *, text: str):
        """This server has worked for 0 days without a..."""
        text = self.parse_text(text)
        data = await self.get(ctx, f"zerodays?text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # -------------------- single image commands --------------------

    @commands.check(tokencheck)
    @commands.command()
    async def aaaa(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """AAAAAAA"""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"aaaa?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def aaaapng(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """AAAAAAA"""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"aaaapng?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def aborted(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Aborted."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"aborted?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def affect(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """It doesn't affect my baby."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"affect?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def airpods(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Wearing airpods."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"airpods?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def america(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Blend with the flag."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"america?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def animestyle(
        self,
        ctx: commands.Context,
        image1: Optional[ImageFinder] = None,
        model: Optional[str] = None,
    ):
        """Create an anime style image.
        Valid models:
            hayao, hosoda, paprika, shinkai
            If no model is chosen it will be picked at random.
        """
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        models = ["hayao", "hosoda", "paprika", "shinkai"]
        if model is None or model.lower() not in models:
            model = random.choice(models)
        data = await self.get(ctx, f"animestyle?avatar1={image1[0]}&model={model}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def bongocat(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Bongocar-ify your image."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"bongocat?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def brazzers(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Add the brazzers logo to your image"""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"brazzers?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def cancer(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Squidward shows cancer."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"cancer?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def care(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """I do care."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"care?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def communism(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Blending with the flag."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"communism?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def dab(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Show off your dabbing skills"""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"dab?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def dank(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Dank. no scope."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"dank?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def deepfry(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Deep fry your image."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"deepfry?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def delete(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Delete this."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"delete?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def disability(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Not all disabilities look the same."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"disability?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def docs(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Why read the docs?"""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"docs?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def door(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Kick down the door."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"door?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def draperize(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Draperize your image."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"draperize?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    # @commands.check(tokencheck)
    # @commands.command()
    # async def dream(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
    #     """Create"""
    #     if image1 is None:
    #         image1 = await ImageFinder().search_for_images(ctx)
    #     data = await self.get(ctx, f"dream?avatar1={image1[0]}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def egg(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Become an egg."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"egg?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def eyedetect(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Eye detection."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"eyedetect?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def failure(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Look at this failure."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"failure?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def fakenews(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Turn off the fake news."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"fakenews?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def fedora(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Tip your fedora."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"fedora?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def fingahs(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Fingahs."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"fingahs?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def gay(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Rainbow."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"gay?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def goggles(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Put on some goggles."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"goggles?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def hitler(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Worse than hitler."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"hitler?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def invert(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Invert the colors."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"invert?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def ipad(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Display your image on an ipad."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"ipad?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def jail(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Go to jail."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"jail?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def kimborder(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Kim Jong Un border."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"kimborder?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def laid(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Don't get laid."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"laid?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def loading(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Loading..."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"loading?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    # @commands.check(tokencheck)
    # @commands.command()
    # async def magik(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
    #     """Magik."""
    #     if image1 is None:
    #         image1 = await ImageFinder().search_for_images(ctx)
    #     data = await self.get(ctx, f"magik?avatar1={image1[0]}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def monke(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Become monke."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"monke?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def noman(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """I fear no man"""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"noman?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def nuke(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Nuke it."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"nuke?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def nukegif(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Nuke it."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"nukegif?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    # @commands.check(tokencheck)
    # @commands.command()
    # async def overlaytest(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
    #     """Overlay test."""
    #     if image1 is None:
    #         image1 = await ImageFinder().search_for_images(ctx)
    #     data = await self.get(ctx, f"overlaytest?avatar1={image1[0]}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def petpet(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Pet pet."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"petpet?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)  # should be gif?

    @commands.check(tokencheck)
    @commands.command()
    async def portals(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Fall into the portal."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"portals?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def purplefire(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Purple fire."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"purplefire?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def radialblur(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Add radial blur to your image."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"radialblur?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def redify(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Redify your image."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"redify?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def redtest(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Red smoke reveal."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"redtest?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command(aliases=["removebg", "removebackground"])
    async def rembg(
        self,
        ctx: commands.Context,
        image1: Optional[ImageFinder] = None,
        model: str = "u2net",
    ):
        """Remove the background of an image.
        Available models:
            u2net, u2netp, u2net_human_seg, silueta, u2net_cloth_seg, isnet-general-use, isnet-anime
        """
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        models = [
            "u2net",
            "u2netp",
            "u2net_human_seg",
            "silueta",
            "u2net_cloth_seg",
            "isnet-general-use",
            "isnet-anime",
        ]
        if model.lower() not in models:
            model = "u2net"
        data = await self.get(ctx, f"rembg?avatar1={image1[0]}&model={model}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def rip(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Rest in peace."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"rip?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def roblox(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Robloxify your image."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"roblox?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def salty(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Get salty."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"salty?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def satan(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Become satan."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"satan?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def sickban(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Sick ban."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"sickban?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def smeshnik(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Smeshnik."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"smeshnik?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def trash(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """All i see is trash."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"trash?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def trigger(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Triggered."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"trigger?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def ugly(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """It's uglier close up."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"ugly?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # @commands.check(tokencheck)
    # @commands.command()
    # async def upscalewaifu2x(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
    #     """Upscale your image using waifu2x."""
    #     if image1 is None:
    #         image1 = await ImageFinder().search_for_images(ctx)
    #     data = await self.get(ctx, f"upscalewaifu2x?avatar1={image1[0]}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def wanted(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Wanted."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"wanted?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def warp(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
        """Warp the image."""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"warp?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # @commands.check(tokencheck)
    # @commands.command()
    # async def webp(self, ctx: commands.Context, image1: Optional[ImageFinder] = None):
    #     """webp stuff."""
    #     if image1 is None:
    #         image1 = await ImageFinder().search_for_images(ctx)
    #     data = await self.get(ctx, f"webp?avatar1={image1[0]}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def whodidthis(
        self, ctx: commands.Context, image1: Optional[ImageFinder] = None
    ):
        """Who did this?"""
        if image1 is None:
            image1 = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"whodidthis?avatar1={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # -------------------- multi image commands --------------------

    @commands.check(tokencheck)
    @commands.command()
    async def bed(
        self,
        ctx: commands.Context,
        image1: ImageFinder,
        image2: Optional[ImageFinder] = None,
    ):
        """There's a monster under my bed."""
        if image2 is None:
            image2 = [ctx.author.display_avatar.replace(format="png").url]
        data = await self.get(ctx, f"bed?avatar1={image1[0]}&avatar2={image2[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def cena(
        self,
        ctx: commands.Context,
        image1: ImageFinder,
        image2: Optional[ImageFinder] = None,
    ):
        """John Cena."""
        if image2 is None:
            image2 = [ctx.author.display_avatar.replace(format="png").url]
        data = await self.get(ctx, f"cena?avatar1={image1[0]}&avatar2={image2[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def corporate(
        self,
        ctx: commands.Context,
        image1: ImageFinder,
        image2: Optional[ImageFinder] = None,
    ):
        """Corporate needs you to find the differences."""
        if image2 is None:
            image2 = [ctx.author.display_avatar.replace(format="png").url]
        data = await self.get(ctx, f"corporate?avatar1={image1[0]}&avatar2={image2[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # @commands.check(tokencheck)
    # @commands.command()
    # async def dreamgif(self, ctx: commands.Context, image1: ImageFinder, image2: Optional[ImageFinder] = None):
    #     """Create a dream."""
    #     if image2 is None:
    #         image2 = [ctx.author.display_avatar.replace(format="png").url]
    #     data = await self.get(ctx, f"dreamgif?avatar1={image1[0]}&avatar2={image2[0]}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data, "gif")

    # @commands.check(tokencheck)
    # @commands.command()
    # async def dreamgifv2(self, ctx: commands.Context, image1: ImageFinder, image2: Optional[ImageFinder] = None):
    #     """Create a dream."""
    #     if image2 is None:
    #         image2 = [ctx.author.display_avatar.replace(format="png").url]
    #     data = await self.get(ctx, f"dreamgifv2?avatar1={image1[0]}&avatar2={image2[0]}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data, "gif")

    # @commands.check(tokencheck)
    # @commands.command()
    # async def dreamstyle(self, ctx: commands.Context, image1: ImageFinder, image2: Optional[ImageFinder] = None):
    #     """Create an anime style image."""
    #     if image2 is None:
    #         image2 = [ctx.author.display_avatar.replace(format="png").url]
    #     data = await self.get(ctx, f"dreamstyle?avatar1={image1[0]}&avatar2={image2[0]}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def madethis(
        self,
        ctx: commands.Context,
        image1: ImageFinder,
        image2: Optional[ImageFinder] = None,
    ):
        """I made this."""
        if image2 is None:
            image2 = [ctx.author.display_avatar.replace(format="png").url]
        data = await self.get(ctx, f"madethis?avatar1={image1[0]}&avatar2={image2[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def screams(
        self,
        ctx: commands.Context,
        image1: ImageFinder,
        image2: Optional[ImageFinder] = None,
    ):
        """Why can't you just be normal?"""
        if image2 is None:
            image2 = [ctx.author.display_avatar.replace(format="png").url]
        data = await self.get(ctx, f"screams?avatar1={image1[0]}&avatar2={image2[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def shoo(
        self,
        ctx: commands.Context,
        image1: ImageFinder,
        image2: Optional[ImageFinder] = None,
    ):
        """Shoo."""
        if image2 is None:
            image2 = [ctx.author.display_avatar.replace(format="png").url]
        data = await self.get(ctx, f"shoo?avatar1={image1[0]}&avatar2={image2[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # @commands.check(tokencheck)
    # @commands.command()
    # async def shooalt(self, ctx: commands.Context, image1: ImageFinder, image2: Optional[ImageFinder] = None):
    #     """Shoo."""
    #     if image2 is None:
    #         image2 = [ctx.author.display_avatar.replace(format="png").url]
    #     data = await self.get(ctx, f"shooalt?avatar1={image1[0]}&avatar2={image2[0]}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def slap(
        self,
        ctx: commands.Context,
        image1: ImageFinder,
        image2: Optional[ImageFinder] = None,
    ):
        """Slap."""
        if image2 is None:
            image2 = [ctx.author.display_avatar.replace(format="png").url]
        data = await self.get(ctx, f"slap?avatar1={image2[0]}&avatar2={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def spank(
        self,
        ctx: commands.Context,
        image1: ImageFinder,
        image2: Optional[ImageFinder] = None,
    ):
        """Spank."""
        if image2 is None:
            image2 = [ctx.author.display_avatar.replace(format="png").url]
        data = await self.get(ctx, f"spank?avatar1={image2[0]}&avatar2={image1[0]}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # -------------------- rest all commands --------------------

    @commands.check(tokencheck)
    @commands.command()
    async def byemom(
        self, ctx: commands.Context, user: Optional[discord.Member] = None, *, text: str
    ):
        """Bye mom."""
        user = user or ctx.author
        text = self.parse_text(text)
        avatar = user.display_avatar.replace(format="png").url
        data = await self.get(
            ctx,
            f"byemom?avatar1={avatar}&text={text}&username1={ctx.author.display_name}",
        )
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def floor(
        self, ctx: commands.Context, user: Optional[discord.Member] = None, *, text: str
    ):
        """The floor is ..."""
        user = user or ctx.author
        text = self.parse_text(text)
        avatar = user.display_avatar.replace(format="png").url
        data = await self.get(ctx, f"floor?avatar1={avatar}&text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # @commands.check(tokencheck)
    # @commands.command()
    # async def fusion(self, ctx: commands.Context, user1: Optional[discord.Member], user2: Optional[discord.Member], *, text: str):
    #     """Fusion."""
    #     user1 = user1 or ctx.author
    #     user2 = user2 or ctx.author
    #     text = self.parse_text(text)
    #     avatar1 = user1.display_avatar.replace(format="png").url
    #     avatar2 = user2.display_avatar.replace(format="png").url
    #     data = await self.get(ctx, f"fusion?avatar1={avatar1}&avatar2={avatar2}&text={text}&username1={user1.display_name}&username2={user2.display_name}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data)

    # @commands.check(tokencheck)
    # @commands.command()
    # async def fusiongif(self, ctx: commands.Context, user1: Optional[discord.Member], user2: Optional[discord.Member], *, text: str):
    #     """Fusion."""
    #     user1 = user1 or ctx.author
    #     user2 = user2 or ctx.author
    #     text = self.parse_text(text)
    #     avatar1 = user1.display_avatar.replace(format="png").url
    #     avatar2 = user2.display_avatar.replace(format="png").url
    #     data = await self.get(ctx, f"fusiongif?avatar1={avatar1}&avatar2={avatar2}&text={text}&username1={user1.display_name}&username2={user2.display_name}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #     await self.send_img(ctx, data, "gif")

    @commands.check(tokencheck)
    @commands.command()
    async def garfield(
        self, ctx: commands.Context, user: Optional[discord.Member] = None, *, text: str
    ):
        """Garfield."""
        user = user or ctx.author
        text = self.parse_text(text)
        avatar = user.display_avatar.replace(format="png").url
        data = await self.get(ctx, f"garfield?avatar1={avatar}&text={text}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def glitch(
        self,
        ctx: commands.Context,
        user: Optional[ImageFinder] = None,
        amount: Optional[int] = 5,
    ):
        """Glitch."""
        if user is None:
            user = await ImageFinder().search_for_images(ctx)
        data = await self.get(ctx, f"glitch?avatar1={user[0]}&text={amount}")
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data, "gif")

    # TODO: Add meme and meme_v2

    @commands.check(tokencheck)
    @commands.command()
    async def obama(self, ctx: commands.Context, user: Optional[discord.Member] = None):
        """Obama."""
        user = user or ctx.author
        avatar = user.display_avatar.replace(format="png").url
        data = await self.get(
            ctx, f"obama?avatar1={avatar}&username1={user.display_name}"
        )
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    # @commands.check(tokencheck)
    # @commands.command()
    # async def profile(self, ctx: commands.Context, user: Optional[discord.Member] = None, *, text: str):
    #     """Profile picture."""
    #     user = user or ctx.author
    #     text = self.parse_text(text)
    #     avatar = user.display_avatar.replace(format="png").url
    #     data = await self.get(ctx, f"profile?avatar1={avatar}&text={text}&username1={user.display_name}")
    #     if isinstance(data, dict):
    #         await self.send_error(ctx, data)
    #         return
    #    await self.send_img(ctx, data)

    @commands.check(tokencheck)
    @commands.command()
    async def quote(
        self, ctx: commands.Context, user: Optional[discord.Member] = None, *, text: str
    ):
        """Quote a message"""
        user = user or ctx.author
        text = self.parse_text(text)
        avatar = user.display_avatar.replace(format="png").url
        data = await self.get(
            ctx, f"quote?avatar1={avatar}&text={text}&username1={user.display_name}"
        )
        if isinstance(data, dict):
            await self.send_error(ctx, data)
            return
        await self.send_img(ctx, data)

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)
