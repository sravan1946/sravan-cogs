import asyncio
import logging
import re

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

log = logging.getLogger("red.sravan.session")


class Session(commands.Cog):
    """
    Shows how many commands are invoked in a session (resets on reboot)
    """

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete.
        """
        return

    def __init__(self, bot: Red):
        self.bot = bot
        self.last_change = None
        self.config = Config.get_conf(self, 25298865439862, force_registration=True)
        self.commands = {}
        super(Session, self).__init__()

        self.presence_task = asyncio.create_task(self.maybe_update_presence())

        default_global = {
            "botstats": True,
            "delay": 60,
            "type": 0,
            "status": 0,
        }
        self.config.register_global(**default_global)

    __author__ = ["aikaterna", "sravan"]
    __version__ = "1.0.6"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    def cog_unload(self):
        self.presence_task.cancel()

    @commands.group(autohelp=True)
    @commands.guild_only()
    @commands.is_owner()
    async def session(self, ctx: commands.Context):
        """
        Session group commands.
        """

    @session.command()
    async def delay(self, ctx: commands.Context, seconds: int):
        """
        Sets interval of random status switch.

        Must be 20 or superior.

        """
        seconds = max(seconds, 20)
        await self.config.delay.set(seconds)
        await ctx.send(f"Interval set to {seconds} seconds.")

    @session.command(name="type")
    async def _session_type(self, ctx: commands.Context, status_type: int):
        """
        Define the session game type.

        Type list:
        0 = Playing
        2 = Listening
        3 = Watching
        5 = Competing

        """
        if status_type in {0, 2, 3, 5}:
            rnd_type = {0: "playing", 2: "listening", 3: "watching", 5: "competing"}
            await self.config.type.set(status_type)
            await self.presence_updater()
            await ctx.send(f"Session activity type set to {rnd_type[status_type]}.")
        else:
            await ctx.send(
                f"Status activity type must be between 0 or 1 or 3 or 5. "
                f"See `{ctx.prefix}help session type` for more information."
            )

    @session.command()
    async def status(self, ctx: commands.Context, status: int):
        """
        Define the session presence status.

        Status list:
        0 = Online
        1 = Idle
        2 = DND
        3 = Invisible

        """
        if 0 <= status <= 3:
            rnd_status = {0: "online", 1: "idle", 2: "DND", 3: "invisible"}
            await self.config.status.set(status)
            await self.presence_updater()
            await ctx.send(f"Session presence status set to {rnd_status[status]}.")
        else:
            await ctx.send(
                f"Status presence type must be between 0 and 3. "
                f"See `{ctx.prefix}help session status` for more information."
            )

    async def maybe_update_presence(self):
        await self.bot.wait_until_red_ready()
        delay = await self.config.delay()
        while True:
            try:
                await self.presence_updater()
            except Exception:
                log.exception("Something went wrong in maybe_update_presence task:")

            await asyncio.sleep(int(delay))

    async def presence_updater(self):
        cog_settings = await self.config.all()

        botstats = cog_settings["botstats"]
        _type = cog_settings["type"]
        _status = cog_settings["status"]

        if _status == 0:
            status = discord.Status.online
        elif _status == 1:
            status = discord.Status.idle
        elif _status == 2:
            status = discord.Status.dnd
        elif _status == 3:
            status = discord.Status.offline

        if botstats:

            def find_sum(s):
                return sum(map(int, re.findall("\d+", s)))

            message = "\n".join(
                "{count}".format(count=d[1]["count"])
                for d in sorted(
                    self.commands.items(),
                    key=lambda infos: infos[1]["count"],
                    reverse=True,
                )
            )
            s = find_sum(message)
            botstatus = f"{s} commands used in this session"
            await self.bot.change_presence(
                activity=discord.Activity(name=botstatus, type=_type), status=status
            )

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if ctx.message.author.bot is False:
            command = str(ctx.command)
            if command != "None":
                if command not in self.commands:
                    self.commands[command] = {"count": 1}
                    return
                self.commands[command]["count"] += 1
