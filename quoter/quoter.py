import asyncio
from typing import Literal, Optional

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Quoter(commands.Cog):
    """
    A simple cog to quote some text.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=298742345,
            force_registration=True,
        )
        default_guild = {
            "channel": None,
            "autodelete": False,
            "autothread": False,
        }
        self.config.register_guild(**default_guild)

    __author__ = ["sravan"]
    __version__ = "1.1.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    @commands.group(name="quoteset")
    @commands.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    async def quoteset(self, ctx: commands.Context) -> None:
        """
        Quote configuration commands.
        """

    @quoteset.command(name="channel")
    async def quoteset_channel(
        self, ctx: commands.Context, channel: Optional[discord.TextChannel]
    ) -> None:
        """
        Set the channel where quotes will be sent.

        If no channel is provided, it will show the current setting.
        """
        if channel:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(f"Quotes will now be sent to {channel.mention}.")
        else:
            channel_id = await self.config.guild(ctx.guild).channel()
            if channel_id:
                channel = ctx.guild.get_channel(channel_id)
                if channel:
                    await ctx.send(f"Quotes are currently sent to {channel.mention}.")
                else:
                    await ctx.send(
                        "The quote channel no longer exists. Please set a new one using `[p]quoteset channel #channel`."
                    )
            else:
                await ctx.send(
                    "No quote channel set. Use `[p]quoteset channel #channel` to set one."
                )
                return

    @quoteset.command(name="autodelete")
    async def quoteset_autodelete(
        self, ctx: commands.Context, enabled: Optional[bool] = None
    ) -> None:
        """
        Toggle auto-deletion for the `quote` command.

        When enabled:
        - The command message (the user's `[p]quote ...`) is deleted.
        - After the user presses `Send` or `Cancel`, the prompt message is deleted after ~3 seconds.
        """
        if enabled is None:
            current = await self.config.guild(ctx.guild).autodelete()
            await ctx.send(
                f"Auto-delete is currently {'enabled' if current else 'disabled'}."
            )
            return

        await self.config.guild(ctx.guild).autodelete.set(enabled)
        await ctx.send(
            f"Auto-delete has been {'enabled' if enabled else 'disabled'} for quotes."
        )

    @quoteset.command(name="autothread")
    async def quoteset_autothread(
        self, ctx: commands.Context, enabled: Optional[bool] = None
    ) -> None:
        """
        Toggle automatic thread creation for posted quotes.

        When enabled, after the quote is posted as an embed, the bot creates a
        message thread using that posted message as the thread starter.
        """
        if enabled is None:
            current = await self.config.guild(ctx.guild).autothread()
            await ctx.send(
                f"Auto-thread is currently {'enabled' if current else 'disabled'}."
            )
            return

        await self.config.guild(ctx.guild).autothread.set(enabled)
        await ctx.send(
            f"Auto-thread has been {'enabled' if enabled else 'disabled'} for quotes."
        )

    @commands.command(name="quote")
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def quote(self, ctx: commands.Context, *, text: str = "") -> None:
        """
        Send a quote to the configured channel.

        Usage: `[p]quote <text>`

        You will be prompted to optionally choose a user as the quote author.
        If no user is selected, the quote author will be `Anonymous`.
        """
        channel_id = await self.config.guild(ctx.guild).channel()

        if not channel_id:
            await ctx.send(
                "No quote channel set. Use `[p]quoteset channel #channel` to set one."
            )
            return

        channel = ctx.guild.get_channel(channel_id)
        if not channel:
            await ctx.send(
                "The quote channel no longer exists. Please set a new one using `[p]quoteset channel #channel`."
            )
            return
        if not isinstance(channel, discord.TextChannel):
            await ctx.send(
                "The configured quote channel is not a text channel. Please set a new one."
            )
            return

        perms = channel.permissions_for(ctx.guild.me)
        missing = []
        if not perms.send_messages:
            missing.append("Send Messages")
        if not perms.embed_links:
            missing.append("Embed Links")
        if missing:
            await ctx.send(
                f"I need the following permission(s) in {channel.mention}: {', '.join(missing)}."
            )
            return

        if not text:
            await ctx.send("Please provide the quote text.")
            return

        autodelete = await self.config.guild(ctx.guild).autodelete()
        autothread = await self.config.guild(ctx.guild).autothread()

        color = await ctx.embed_color()
        view = QuoteView(
            author_id=ctx.author.id,
            quote_text=text,
            quote_channel=channel,
            color=color,
            autodelete_prompt=autodelete,
            autothread=autothread,
        )
        message = await ctx.send(embed=view.preview_embed, view=view)
        view.message = message

        if autodelete:
            try:
                await ctx.message.delete()
            except (discord.Forbidden, discord.NotFound):
                pass

        await ctx.tick()


class QuoteUserSelect(discord.ui.UserSelect):
    """Optional user picker for the quote author."""

    def __init__(self, view: "QuoteView"):
        super().__init__(
            placeholder="Select quote author (optional)",
            min_values=0,
            max_values=1,
        )
        self.quote_view = view

    async def callback(self, interaction: discord.Interaction) -> None:
        self.quote_view.selected_user = self.values[0] if self.values else None
        self.quote_view.update_preview_author()
        await interaction.message.edit(embed=self.quote_view.preview_embed)


class QuoteView(discord.ui.View):
    def __init__(
        self,
        *,
        author_id: int,
        quote_text: str,
        quote_channel: discord.TextChannel,
        color: discord.Color,
        autodelete_prompt: bool = False,
        autothread: bool = False,
        timeout: int = 60,
    ):
        super().__init__(timeout=timeout)
        self.author_id = author_id
        self.quote_text = quote_text
        self.quote_channel = quote_channel
        self.color = color
        self.autodelete_prompt = autodelete_prompt
        self.autothread = autothread

        self.selected_user: Optional[discord.User] = None

        # Message the user interacts with (filled in by the command).
        self.message: Optional[discord.Message] = None

        self.preview_embed = discord.Embed(color=self.color)
        self.preview_embed.description = f'"{self.quote_text}"'
        self.preview_embed.set_author(name="Anonymous")

        self.user_select = QuoteUserSelect(self)
        self.add_item(self.user_select)

    async def _delete_prompt_after_delay(self, message: discord.Message) -> None:
        """Delete the prompt message after a short delay (best-effort)."""
        if not self.autodelete_prompt:
            return
        await asyncio.sleep(3)
        try:
            await message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "This isn't your quote prompt.", ephemeral=True
            )
            return False
        # We will only edit the original message in callbacks.
        await interaction.response.defer()
        return True

    def update_preview_author(self) -> None:
        if self.selected_user:
            # `UserSelect` returns `discord.User` for both guild users and strangers.
            icon_url = getattr(
                getattr(self.selected_user, "display_avatar", None), "url", None
            )
            self.preview_embed.set_author(
                name=self.selected_user.display_name,
                icon_url=icon_url,
            )
        else:
            self.preview_embed.set_author(name="Anonymous")

    async def on_timeout(self) -> None:
        if self.message:
            try:
                await self.message.edit(view=None)
            except discord.HTTPException:
                pass
            if self.autodelete_prompt:
                asyncio.create_task(self._delete_prompt_after_delay(self.message))
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
    async def cancel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.message.edit(content="Cancelled.", embed=None, view=None)
        asyncio.create_task(self._delete_prompt_after_delay(interaction.message))
        self.stop()

    @discord.ui.button(label="Send", style=discord.ButtonStyle.green)
    async def send(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        embed = discord.Embed(color=self.color)
        embed.description = f'"{self.quote_text}"'

        if self.selected_user:
            icon_url = getattr(
                getattr(self.selected_user, "display_avatar", None), "url", None
            )
            embed.set_author(
                name=self.selected_user.display_name,
                icon_url=icon_url,
            )
        else:
            embed.set_author(name="Anonymous")

        quote_message: Optional[discord.Message] = None
        try:
            quote_message = await self.quote_channel.send(embed=embed)
        except discord.HTTPException:
            await interaction.message.edit(
                content="Failed to send the quote (missing permissions?).",
                embed=None,
                view=None,
            )
            self.stop()
            return

        thread_created = False
        if self.autothread and quote_message:
            try:
                author_name = (
                    self.selected_user.display_name
                    if self.selected_user is not None
                    else "Anonymous"
                )
                snippet = self.quote_text.strip().replace("\n", " ")
                name = f"Quote by {author_name}: {snippet}"
                if len(name) > 100:
                    name = name[:97].rstrip() + "..."

                await quote_message.create_thread(
                    name=name,
                )
                thread_created = True
            except (discord.Forbidden, discord.HTTPException, discord.NotFound):
                thread_created = False

        success_text = (
            "Quote sent (thread created)." if thread_created else "Quote sent."
        )
        await interaction.message.edit(content=success_text, embed=None, view=None)
        asyncio.create_task(self._delete_prompt_after_delay(interaction.message))
        self.stop()
