from .perform import Perform


def setup(bot):
    bot.add_cog(Perform(bot))
