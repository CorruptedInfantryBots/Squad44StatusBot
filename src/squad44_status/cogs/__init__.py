from squad44_status.cogs.status_cog import StatusCog  # noqa
from discord.ext.commands import Bot


async def setup(bot: Bot):
    await bot.add_cog(StatusCog(bot))

__all__ = ["StatusCog", "setup"]
