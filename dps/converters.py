from redbot.core import commands


class ChannelCategoryConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        args = argument.split()
        res = {"guild": False, "category": [], "channel": []}
        if "guild" in args:
            res["guild"] = True
            return res
        for arg in args:
            try:
                channel = await commands.TextChannelConverter().convert(ctx, arg)
                if channel not in res["channel"]:
                    res["channel"].append(channel.id)
            except commands.BadArgument:
                try:
                    category = await commands.CategoryChannelConverter().convert(
                        ctx, arg
                    )
                    if category not in res["category"]:
                        res["category"].append(category.id)
                except commands.BadArgument as e:
                    continue
        if not res["channel"] and not res["category"]:
            raise commands.BadArgument("No valid channel or category found.")
        return res
