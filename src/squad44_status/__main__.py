import asyncio
import logging
import os
from typing import Literal, Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

import squad44_status.cogs  # noqa

load_dotenv()

logger = logging.getLogger("discord")
logging.basicConfig(level="INFO")


async def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    await bot.login(os.getenv("token"))
    await bot.load_extension("squad44_status.cogs")
    await bot.connect()

def entrypoint():
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
